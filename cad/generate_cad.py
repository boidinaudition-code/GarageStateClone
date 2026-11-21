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
W = 168.0                  # external shell width; expanded from concept to fit servo right pier
D = 100.0                  # external shell depth
H_FRONT = 62.0             # roof TOP at front
H_BACK = 65.0              # roof TOP at rear (3 mm mono-pente)
WALL = 2.4                # minimum structural wall thickness >= 2
ROOF = 3.0                # roof solid thickness >= 2
BASE = 3.0                # floor solid thickness >= 2
FIT = 0.30                # clearance PER FACE for slide-on and hinged fits
ROOF_OVERHANG = 3.0
ROOF_SKIRT_DROP = 4.5
OPEN_W = 104.0
OPEN_H = 42.0
OPEN_X = (W-OPEN_W)/2
OPEN_Z = BASE
PIVOT_Y = 12.0            # recess of axis; avoids front wall and servo body collision
PIVOT_Z = BASE + OPEN_H + 0.4
DOOR_T = 2.4
DOOR_W = OPEN_W - 2*FIT
DOOR_H = OPEN_H - 2*FIT
HINGE_D = 3.2
HINGE_SOCKET_D = HINGE_D + 2*FIT
HINGE_PIN_LEFT = 6.0
LED_ORANGE_APERTURE_D = 2.0 # small visible point, NOT the 5mm LED mounting bore
LED_POCKET_D = 6.0 + 2*FIT # provisional collar/service envelope; measure both LEDs
LED_ENVELOPE = (6.0, 9.0) # DESIGN diameter x length, NOT vendor dimensions
LED_ORANGE_RECESS = WALL + 1.0 # entire LED behind facade, in +Y direction
SERVO_CASE = (22.3, 11.8, 26.3) # official DFRobot DMS-MG90 BODY only; tabs/shaft/horn not included
CARD_ENVELOPE = (52.0, 23.0, 12.0) # reserved service envelope, NOT PCB dimensions; include USB/antenna slack
XIAO_BOARD_NOMINAL = (21.0, 17.8) # Seeed published PCB L x W, height unspecified
WIO_STACK_NOMINAL = (23.0, 22.0, 8.0) # Seeed marketing assembled approx; must measure physical stack
CAP_C1_BODY = (10.0, 13.0) # Gotronic 04947: diameter x height; lead pitch 5mm
RESISTOR_BODY = (6.5, 2.5) # all 0.5W specified Gotronic: axial length x diameter
LED_NOMINAL_D = 5.0 # Gotronic WCS101 warm white and L7113NC; detailed dimensions unknown

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

# 6. Provisional servo cradle at FRONT RIGHT; fit slot is SERVO Y dimension + 0.6mm
servo_x=door_x1+3.0
servo_y=PIVOT_Y-SERVO_CASE[1]/2
servo_z=PIVOT_Z-SERVO_CASE[2]
cradle_x0=servo_x-1.0
cradle_y0=servo_y-(WALL+FIT)
cradle_dx=SERVO_CASE[0]+2.0
cradle_dy=SERVO_CASE[1]+2*(WALL+FIT)
cradle_z0=servo_z-3.0
cradle=box(cradle_x0,cradle_y0,cradle_z0,cradle_dx,cradle_dy,3.0)
cradle=cradle.fuse(box(cradle_x0,cradle_y0,cradle_z0+3.0,cradle_dx,WALL,6.0))
cradle=cradle.fuse(box(cradle_x0,cradle_y0+cradle_dy-WALL,cradle_z0+3.0,cradle_dx,WALL,6.0)).clean()
# The bottom tray is printable; actual servo tabs and horn adapters require measuring.

# 7. Rear electronics tray; board envelope reference 52 x 21, lower than roof.
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
led_white_y=60.0  # ~7 mm behind the end of the door when opened
roof_under_z=H_FRONT-ROOF+(H_BACK-H_FRONT)*led_white_y/D
holder_bottom=roof_under_z-9.8
# Pocket intentionally accommodates an UNKNOWN collar; no press-fit claim.
# Top overlaps roof underside by 0.2mm for later bonding, not a validated fixing.
holder=cq.Solid.makeCylinder(5.0,10.0,V(led_white_x,led_white_y,holder_bottom),V(0,0,1))
holder=holder.cut(cq.Solid.makeCylinder(LED_POCKET_D/2,10.2,V(led_white_x,led_white_y,holder_bottom-0.1),V(0,0,1))).clean()

# 10. Reference solids (non printable) to inspect reserved volumes in STEP assembly
servo_reference=box(servo_x,servo_y,servo_z,*SERVO_CASE)
servo_shaft_reference=cyl_x(servo_x-3.0,PIVOT_Y,PIVOT_Z,5.0,3.0)
servo_reference=servo_reference.fuse(servo_shaft_reference).clean()
board_reference=box(W/2-CARD_ENVELOPE[0]/2,tray_y0+3.2,tray_z0+2.4,
                    CARD_ENVELOPE[0],CARD_ENVELOPE[1],CARD_ENVELOPE[2])

PRINTABLE={
  '01_coque_blanche':shell,
  '02_socle_noir':base_plate,
  '03_toit_noir_pente':roof_lid,
  '04_porte_noire':door,
  '05_palier_gauche':bearing,
  '06_support_servo_provisoire':cradle,
  '07_plateau_electronique':tray,
  '08_liseret_bleu':trim,
  '09_support_led_blanche':holder,
}
REFERENCES={
  'REF_servo_a_mesurer_NE_PAS_IMPRIMER':servo_reference,
  'REF_zone_service_XIAO_Wio_NE_PAS_IMPRIMER':board_reference,
  'REF_C1_470uF_16V_NE_PAS_IMPRIMER':cq.Solid.makeCylinder(CAP_C1_BODY[0]/2,CAP_C1_BODY[1],V(W-14,35,BASE+5),V(0,0,1)),
  'REF_LED_orange_ENVELOPPE_PROVISOIRE_NE_PAS_IMPRIMER':cq.Solid.makeCylinder(LED_ENVELOPE[0]/2,LED_ENVELOPE[1],V(orange_x,LED_ORANGE_RECESS,orange_z),V(0,1,0)),
  'REF_LED_blanche_ENVELOPPE_PROVISOIRE_NE_PAS_IMPRIMER':cq.Solid.makeCylinder(LED_ENVELOPE[0]/2,LED_ENVELOPE[1],V(led_white_x,led_white_y,holder_bottom),V(0,0,1)),
}

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
    assy=cq.Assembly(name='GarageStateClone_V1')
    colors={
       '01_coque_blanche':cq.Color(0.96,0.96,0.95),
       '02_socle_noir':cq.Color(0.12,0.13,0.15),
       '03_toit_noir_pente':cq.Color(0.12,0.13,0.15),
       '04_porte_noire':cq.Color(0.15,0.16,0.18),
       '05_palier_gauche':cq.Color(0.65,0.68,0.7),
       '06_support_servo_provisoire':cq.Color(0.50,0.55,0.6),
       '07_plateau_electronique':cq.Color(0.54,0.58,0.62),
       '08_liseret_bleu':cq.Color(0.07,0.27,0.65),
       '09_support_led_blanche':cq.Color(0.96,0.96,0.95),
    }
    for name,s in PRINTABLE.items():
        assy.add(s,name=name,color=colors[name])
    for name,s in REFERENCES.items():
        assy.add(s,name=name,color=cq.Color(0.7,0.35,0.3,0.55))
    assy.save(str(STEP/'GarageStateClone_V1_assemblage.step'))
    (ROOT/'metriques_validation.json').write_text(json.dumps({'parameters_mm':{
        'width':W,'depth':D,'front_height':H_FRONT,'rear_height':H_BACK,
        'roof_slope_rise':H_BACK-H_FRONT,'wall':WALL,'roof':ROOF,'base':BASE,
        'fit_per_face':FIT,'opening_width':OPEN_W,'opening_height':OPEN_H,
        'door_width':DOOR_W,'door_height':DOOR_H,'hinge_diameter':HINGE_D,
        'bearing_hole_diameter':HINGE_SOCKET_D,
        'pivot_y':PIVOT_Y,'pivot_z':PIVOT_Z,
        'led_white_y':led_white_y,'led_orange_x':orange_x,
        'servo_body_nominal':list(SERVO_CASE),'card_service_envelope_proposed':list(CARD_ENVELOPE),
        'xiao_pcb_nominal_LW':list(XIAO_BOARD_NOMINAL),
        'wio_stack_nominal_xyz_seeed_marketing':list(WIO_STACK_NOMINAL),
        'capacitor_body_diameter_height':list(CAP_C1_BODY),
        'resistor_body_length_diameter':list(RESISTOR_BODY),
        'led_nominal_diameter_only':LED_NOMINAL_D,
        'led_service_envelope_provisional_diameter_length':list(LED_ENVELOPE),
        'led_pocket_provisional_diameter':LED_POCKET_D,
        'orange_optical_aperture_diameter':LED_ORANGE_APERTURE_D,
        'orange_led_recess_from_front':LED_ORANGE_RECESS,
    },'parts':details},ensure_ascii=False,indent=2))
    print('Done:',STEP)