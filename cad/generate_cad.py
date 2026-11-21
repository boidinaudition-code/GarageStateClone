#!/usr/bin/env python3
"""GarageStateClone: prototype parametric CAD (units: millimetres).

Use: python generate_cad.py
Dependencies: cadquery 2.8+, trimesh, numpy, matplotlib (for QA/preview).

This is a measurable starting model, NOT a production-ready fit verified on the
physical DMS-MG90 or XIAO/Wio PCBs. Servo horn coupling remains a blank.
"""
from __future__ import annotations
import math
from pathlib import Path
import cadquery as cq

ROOT = Path(__file__).resolve().parent
STL = ROOT / "stl"
STEP = ROOT / "step"
for folder in [STL,STEP]: folder.mkdir(parents=True, exist_ok=True)

# ========= PARAMETERS (mm) =========
W = 184.0                  # external shell width; expanded from concept to fit servo right pier
D = 100.0                  # external shell depth
H_FRONT = 62.0             # roof TOP at front
H_BACK = 65.0              # roof TOP at rear (3 mm mono-pente)
WALL = 2.4                # minimum structural wall thickness >= 2
ROOF = 3.0                # roof solid thickness >= 2
BASE = 3.0                # floor solid thickness >= 2
FIT = 0.30                # clearance PER FACE for slide-on and hinged fits
ROOF_OVERHANG = 3.0
ROOF_SKIRT_DROP = 4.5
OPEN_W = 110.0
OPEN_H = 42.0
OPEN_X = (W-OPEN_W)/2
OPEN_Z = BASE
PIVOT_Y = 9.5            # recess of axis; avoids front wall and servo body collision
PIVOT_Z = BASE + OPEN_H + 0.4
DOOR_T = 2.4
DOOR_W = OPEN_W - 2*FIT
DOOR_H = OPEN_H - 2*FIT
HINGE_D = 3.2
HINGE_SOCKET_D = HINGE_D + 2*FIT
HINGE_PIN_LEFT = 6.0
LED_ORANGE_D = 3.0
LED_ORANGE_HOLE_D = LED_ORANGE_D + 2*FIT
# STEP fourni: servo complet avec pattes et arbre, repere d'origine XYZ.
SERVO_CASE = (33.4, 32.5, 12.22)
SERVO_OUTPUT_AXIS_LOCAL=(6.05,32.5,6.1)
CARD_ENVELOPE = (29.0, 25.0, 18.0) # enveloppe de service, non la taille des cartes
XIAO_BOARD_NOMINAL = (21.0, 17.8) # Seeed published PCB L x W, height unspecified
WIO_STACK_NOMINAL = (23.0, 22.0, 8.0) # Seeed marketing assembled approx; must measure physical stack
CAP_C1_BODY = (10.0, 13.0) # Gotronic 04947: diameter x height; lead pitch 5mm
RESISTOR_BODY = (6.5, 2.5) # all 0.5W specified Gotronic: axial length x diameter
LED_NOMINAL_D = 5.0 # Gotronic WCS101 warm white and L7113NC; detailed dimensions unknown

# Modeles STEP source fournis par l'utilisateur; emplacement des archives CAD.
VENDOR_REF_DIR=ROOT/'refs'
REF_FILES={'SERVO':VENDOR_REF_DIR/'servo.step',
           'XIAO':VENDOR_REF_DIR/'xiao.step',
           'WIO':VENDOR_REF_DIR/'wio.step',
           'BC547':VENDOR_REF_DIR/'transistor.step'}
# Helpers
V = cq.Vector

def box(x,y,z,sx,sy,sz):
    return cq.Workplane("XY").box(sx,sy,sz,centered=(False,False,False)).translate((x,y,z)).val()

def side_wedge(x0,xlen,ymin,ymax,z_bottom_front,z_bottom_back,z_top_front,z_top_back):
    """Solid extruded along +X, profile in (Y,Z), roof slope preserved."""
    slope_bot=(z_bottom_back-z_bottom_front)/D
    slope_top=(z_top_back-z_top_front)/D
    points=[(ymin,z_bottom_front+slope_bot*ymin),
            (ymax,z_bottom_front+slope_bot*ymax),
            (ymax,z_top_front+slope_top*ymax),
            (ymin,z_top_front+slope_top*ymin)]
    return cq.Workplane('YZ').polyline(points).close().extrude(xlen).translate((x0,0,0)).val()

def cyl_x(xstart,y,z,diameter,length):
    return cq.Solid.makeCylinder(diameter/2,length,V(xstart,y,z),V(1,0,0))

def cyl_y(x,ystart,z,diameter,length):
    return cq.Solid.makeCylinder(diameter/2,length,V(x,ystart,z),V(0,1,0))

def union_all(seq):
    a=seq[0]
    for b in seq[1:]:a=a.fuse(b)
    return a.clean()

# 1. Main shell: 2.4mm structural walls with roof slope and wall opening
shell=side_wedge(0,W,0,D,BASE,BASE,H_FRONT-ROOF,H_BACK-ROOF)
inner_cavity=box(WALL,WALL,BASE-0.02,W-2*WALL,D-2*WALL,100)
shell=shell.cut(inner_cavity)
front_door_cut=box(OPEN_X,-0.1,BASE-0.03,OPEN_W,WALL+0.2,OPEN_H+0.03)
shell=shell.cut(front_door_cut)
# Back power cable exit : a 12 x 8 mm slot, away from printed floor
shell=shell.cut(box(W/2-6,D-WALL-0.2,6,12,WALL+0.5,8))
# Recessed 5mm amber LED: provisional rear pocket and small optical aperture.
orange_x=W-14.5
orange_z=BASE+OPEN_H+6
orange_holder=cyl_y(orange_x,WALL-0.2,orange_z,10.0,10.2)
shell=shell.fuse(orange_holder)
shell=shell.cut(cyl_y(orange_x,-0.1,orange_z,LED_ORANGE_APERTURE_D,LED_ORANGE_RECESS+0.2))
shell=shell.cut(cyl_y(orange_x,LED_ORANGE_RECESS,orange_z,LED_POCKET_D,10.0))
shell=shell.clean()

# 2. Base: floor 3mm and internal locating L rails with 0.30mm side gap
base_plate=box(0,0,0,W,D,BASE)
rail_z=BASE
rail_h=3.0
# Rails are INSIDE shell, their closest face 0.30 mm from the interior wall.
left_rail=box(WALL+FIT,14.0,rail_z,WALL,D-14.0-WALL-FIT-2.0,rail_h)
right_rail=box(W-2*WALL-FIT,14.0,rail_z,WALL,D-14.0-WALL-FIT-2.0,rail_h)
rear_rail=box(WALL+FIT+WALL,D-2*WALL-FIT,rail_z,W-2*(2*WALL+FIT),WALL,rail_h)
base_plate=union_all([base_plate,left_rail,right_rail,rear_rail])

# 3. Roof: wedge lid 3mm, 4.5mm deep overhanging slide-on skirt
roof_plate=side_wedge(-ROOF_OVERHANG,W+2*ROOF_OVERHANG,
                      -ROOF_OVERHANG,D+ROOF_OVERHANG,
                      H_FRONT-ROOF,H_BACK-ROOF,H_FRONT,H_BACK)
roof_outer_skirt=side_wedge(-ROOF_OVERHANG,W+2*ROOF_OVERHANG,
                            -ROOF_OVERHANG,D+ROOF_OVERHANG,
                            H_FRONT-ROOF-ROOF_SKIRT_DROP,H_BACK-ROOF-ROOF_SKIRT_DROP,
                            H_FRONT-ROOF,H_BACK-ROOF)
roof_inner_void=box(-FIT,-FIT,0,W+2*FIT,D+2*FIT,90)
roof_skirt=roof_outer_skirt.cut(roof_inner_void)
roof_lid=roof_plate.fuse(roof_skirt).clean()

# 4. Single rigid door, ornamental grooves, rotating around horizontal X-axis.
door_x0=OPEN_X+FIT
door_x1=door_x0+DOOR_W
door_z0=PIVOT_Z-DOOR_H
door_y0=PIVOT_Y-DOOR_T/2
# Panel occupies inside of frame, no interference with walls at y<2.4
door=box(door_x0,door_y0,door_z0,DOOR_W,DOOR_T,DOOR_H)
# Front of door is y=door_y0: 0.35 mm deep cosmetic groove, 4 lines
for i in range(1,5):
    z=door_z0+i*DOOR_H/5
    door=door.cut(box(door_x0+1.2,door_y0-0.03,z-0.45,DOOR_W-2.4,0.45,0.90))
# Rotating pin: 3.2mm diameter with 6mm projection into LEFT bearing only.
# Cylinder fully fused along top edge of door.
pin=cyl_x(door_x0-HINGE_PIN_LEFT,PIVOT_Y,PIVOT_Z,HINGE_D,DOOR_W+HINGE_PIN_LEFT)
door=door.fuse(pin).clean()

# 5. Bearing block (LEFT) with cylindrical hole 3.8mm for 3.2mm pin
bearing_x=OPEN_X-7.5
bearing_width=6.5
bearing=box(bearing_x,PIVOT_Y-7.8,PIVOT_Z-11,bearing_width,15.6,19.0)
bearing=bearing.cut(cyl_x(bearing_x-0.1,PIVOT_Y,PIVOT_Z,HINGE_SOCKET_D,bearing_width+0.2))
# Add a small flange to permit attaching the bearing to the left masonry with adhesive or screws.
flange=box(OPEN_X-18,WALL+0.5,PIVOT_Z-10,12.0,2.4,18.0)
bearing=bearing.fuse(flange).clean()

# 6. Servo MG90 complet, dans le montant AVANT DROIT. Axe de sortie coaxial
# avec le pivot X de la porte (modele STEP: sortie suivant +Y d'origine).
# Rotations Z(+90) puis X(-90) : arbre dirigé selon -X du garage.
SERVO_SHAFT_TIP_X=door_x1+1.5   # accouplement palonnier non defini
SERVO_ORIGIN=(SERVO_SHAFT_TIP_X+32.5,PIVOT_Y-6.1,PIVOT_Z+6.05)
SERVO_BBOX=(SERVO_SHAFT_TIP_X,SERVO_SHAFT_TIP_X+32.5,
            PIVOT_Y-6.1,PIVOT_Y+6.12,
            PIVOT_Z-22.1,PIVOT_Z+11.3)
servo_xmin,servo_xmax,servo_ymin,servo_ymax,servo_zmin,servo_zmax=SERVO_BBOX
cradle_z_top=servo_zmin-FIT
cradle_xmin=servo_xmin-FIT
cradle_xmax=servo_xmax+FIT
cradle_ymin=servo_ymin-FIT
cradle_ymax=servo_ymax+FIT
cradle=box(cradle_xmin,cradle_ymin,cradle_z_top-2.4,
           cradle_xmax-cradle_xmin,cradle_ymax-cradle_ymin,2.4)
cradle=cradle.fuse(box(cradle_xmin,cradle_ymax,cradle_z_top-2.4,
                      cradle_xmax-cradle_xmin,2.4,6.0))
for xi in (cradle_xmin+4.0,cradle_xmax-7.5):
 for yi in (cradle_ymin+0.5,cradle_ymax-3.9):
  cradle=cradle.fuse(box(xi,yi,BASE,3.2,3.2,cradle_z_top-2.4-BASE+0.02))
cradle=cradle.clean()
# Fixations et palonnier restent a mesurer physiquement.

# 7. Plateau electronique arriere pour les modeles 3D reels.
tray_x0=W/2-30
tray_y0=D-WALL-33.5
tray_z0=6.0
tray=box(tray_x0,tray_y0,tray_z0,60,31,2.4)
tray=tray.fuse(box(tray_x0,tray_y0,tray_z0+2.4,60,2.4,5.0))
tray=tray.fuse(box(tray_x0,tray_y0+31-2.4,tray_z0+2.4,60,2.4,5.0)).clean()
# Mounting of real board is not designed until exact stack/antenna measured.

# 8. Decorative blue accent separate part (adhesive above opening)
trim=box(OPEN_X+FIT,-1.2,BASE+OPEN_H+1.2,OPEN_W-2*FIT,1.2,2.0)

# 9. Low-profile single-LED holder glued under the sloping roof, outside door sweep
led_white_x=W/2
led_white_y=69.0  # ~7 mm behind the end of the door when opened
roof_under_z=H_FRONT-ROOF+(H_BACK-H_FRONT)*led_white_y/D
holder_bottom=roof_under_z-9.8
# Pocket intentionally accommodates an UNKNOWN collar; no press-fit claim.
# Top overlaps roof underside by 0.2mm for later bonding, not a validated fixing.
holder=cq.Solid.makeCylinder(5.0,10.0,V(led_white_x,led_white_y,holder_bottom),V(0,0,1))
holder=holder.cut(cq.Solid.makeCylinder(LED_POCKET_D/2,10.2,V(led_white_x,led_white_y,holder_bottom-0.1),V(0,0,1))).clean()

# 10. Import des quatre vrais STEP. Pas de substitution silencieuse.
def import_ref(key):
 path=REF_FILES[key]
 if path.exists():
  return cq.importers.importStep(str(path)).val()
 # Geometry lossless from STEP, serialized as BREP + zlib + base64 (checked in Git).
 b64path=path.with_suffix('.brep.z.b64')
 if b64path.exists():
  import base64, zlib, tempfile
  packed=base64.b64decode(b64path.read_text(encoding='ascii').strip())
  brep_bytes=zlib.decompress(packed)
  with tempfile.TemporaryDirectory() as td:
   brep_file=Path(td)/'reference.brep'
   brep_file.write_bytes(brep_bytes)
   shape=cq.Shape.importBrep(str(brep_file))
  if not shape.isValid():
   raise ValueError(f'BREP geometrie invalide: {b64path}')
  print(f'REF BREP decompressee sans perte: {b64path.name}')
  return shape
 print(f'WARNING: STEP et BREP absents pour {key}; reference non incluse')
 return None

ref_servo=import_ref('SERVO')
ref_xiao=import_ref('XIAO')
ref_wio=import_ref('WIO')
ref_transistor=import_ref('BC547')
REFERENCES={}
if ref_servo is not None:
 ref_servo=ref_servo.rotate((0,0,0),(0,0,1),90).rotate((0,0,0),(1,0,0),-90)
 ref_servo=ref_servo.translate(SERVO_ORIGIN)
 REFERENCES['REF_MG90_STEP_NE_PAS_IMPRIMER']=ref_servo

TRAY_TOP=tray_z0+2.4
XIAO_LOCAL_CENTER_X=(-8.673+13.809)/2
XIAO_LOCAL_CENTER_Y=(-2.779+15.001)/2
XIAO_OFF_X=W/2-XIAO_LOCAL_CENTER_X
XIAO_OFF_Y=tray_y0+15.5-XIAO_LOCAL_CENTER_Y
# Module Wio EN DESSOUS du XIAO. Coaxialite XY des rows de 2.54 mm;
# hauteur de connexion approximate, a mesurer sur les broches physiques.
WIO_OFF_Z=TRAY_TOP+3.5+1.53
XIAO_OFF_Z=WIO_OFF_Z+6.362
if ref_xiao is not None:
 ref_xiao=ref_xiao.rotate((0,0,0),(1,0,0),90)
 ref_xiao=ref_xiao.translate((XIAO_OFF_X,XIAO_OFF_Y,XIAO_OFF_Z))
 REFERENCES['REF_XIAO_STEP_NE_PAS_IMPRIMER']=ref_xiao
if ref_wio is not None:
 ref_wio=ref_wio.rotate((0,0,0),(0,0,1),90)
 ref_wio=ref_wio.translate((XIAO_OFF_X-119.16,XIAO_OFF_Y-108.29,WIO_OFF_Z))
 REFERENCES['REF_WIO_STEP_NE_PAS_IMPRIMER']=ref_wio
if ref_transistor is not None:
 ref_transistor=ref_transistor.translate((tray_x0+52,tray_y0+14,TRAY_TOP+0.5))
 REFERENCES['REF_BC547_STEP_NE_PAS_IMPRIMER']=ref_transistor
REFERENCES['REF_C1_470uF_16V_NE_PAS_IMPRIMER']=cq.Solid.makeCylinder(
 CAP_C1_BODY[0]/2,CAP_C1_BODY[1],V(W-14,35,BASE+5),V(0,0,1))
REFERENCES['REF_LED_orange_NE_PAS_IMPRIMER']=cq.Solid.makeCylinder(
 1.5,6,V(orange_x,-0.6,orange_z),V(0,1,0))
REFERENCES['REF_LED_blanche_NE_PAS_IMPRIMER']=cq.Solid.makeCylinder(
 1.5,3.5,V(led_white_x,led_white_y,holder_bottom),V(0,0,1))

if __name__=='__main__':
    from cadquery import exporters
    import json
    details={}
    for name,s in PRINTABLE.items():
        if not s.isValid():
            raise RuntimeError(f'Invalid CAD shape: {name}')
        solids=s.Solids()
        if len(solids)!=1:
            raise RuntimeError(f'Unexpected count for {name}: {len(solids)}')
        bb=s.BoundingBox()
        exporters.export(s,str(STEP / (name+'.step')))
        exporters.export(s,str(STL / (name+'.stl')),tolerance=0.08,angularTolerance=0.15)
        details[name]={'volume_mm3':round(s.Volume(),1),
                       'bounds_mm':{c:round(getattr(bb,c),2) for c in ['xmin','xmax','ymin','ymax','zmin','zmax']},
                       'solids':len(solids),'valid':s.isValid()}
        print(name,'volume',round(s.Volume(),1),'mm3')
    assy=cq.Assembly(name='GarageStateClone_V2_STEP')
    colors={
       '01_coque_blanche':cq.Color(0.96,0.96,0.95),
       '02_socle_noir':cq.Color(0.12,0.13,0.15),
       '03_toit_noir_pente':cq.Color(0.12,0.13,0.15),
       '04_porte_noire':cq.Color(0.15,0.16,0.18),
       '05_palier_gauche':cq.Color(0.65,0.68,0.7),
       '06_support_servo_step_0p3mm_PROTOTYPE':cq.Color(0.50,0.55,0.6),
       '07_plateau_electronique_60x31':cq.Color(0.54,0.58,0.62),
       '08_liseret_bleu':cq.Color(0.07,0.27,0.65),
       '09_support_led_blanche':cq.Color(0.96,0.96,0.95),
    }
    for name,s in PRINTABLE.items():
        assy.add(s,name=name,color=colors[name])
    for name,s in REFERENCES.items():
        assy.add(s,name=name,color=cq.Color(0.7,0.35,0.3,0.55))
    assy.save(str(STEP/'GarageStateClone_V2_assemblage_STEP_references.step'))
    (ROOT/'metriques_validation.json').write_text(json.dumps({'parameters_mm':{
        'width':W,'depth':D,'front_height':H_FRONT,'rear_height':H_BACK,
        'roof_slope_rise':H_BACK-H_FRONT,'wall':WALL,'roof':ROOF,'base':BASE,
        'fit_per_face':FIT,'opening_width':OPEN_W,'opening_height':OPEN_H,
        'door_width':DOOR_W,'door_height':DOOR_H,'hinge_diameter':HINGE_D,
        'bearing_hole_diameter':HINGE_SOCKET_D,
        'pivot_y':PIVOT_Y,'pivot_z':PIVOT_Z,
        'led_white_y':led_white_y,'led_orange_x':orange_x,
        'servo_complete_STEP_local_bbox_xyz':list(SERVO_CASE),'servo_axis_tip_x':SERVO_SHAFT_TIP_X,'card_service_envelope_proposed':list(CARD_ENVELOPE),
        'xiao_pcb_nominal_LW':list(XIAO_BOARD_NOMINAL),
        'wio_stack_nominal_xyz_seeed_marketing':list(WIO_STACK_NOMINAL),
        'capacitor_body_diameter_height':list(CAP_C1_BODY),
        'resistor_body_length_diameter':list(RESISTOR_BODY),
        'warm_white_led_diameter_lens_height':list(WHITE_LED_BODY),
    },'parts':details,'reference_STEP_files':[k for k,v in REF_FILES.items() if v.exists()]},ensure_ascii=False,indent=2))
    print('Done:',STEP)