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
W = 150.0                  # external shell width; expanded from concept to fit servo right pier
D = 100.0                  # external shell depth
H_FRONT = 62.0             # roof TOP at front
H_BACK = 78.0              # roof top rear: 16mm rise across 100mm depth (V5)
WALL = 2.4                # minimum structural wall thickness >= 2
ROOF = 3.0                # roof solid thickness >= 2
BASE = 3.0                # floor solid thickness >= 2
FIT = 0.30                # clearance PER FACE for slide-on and hinged fits
ROOF_OVERHANG = 3.0
ROOF_SKIRT_DROP = 4.5
OPEN_W = 100.0
OPEN_H = 42.0
LEFT_PIER_W = 11.0        # compact LEFT pier for bearing
OPEN_X = LEFT_PIER_W      # deliberately asymmetric: door shifted to left
RIGHT_PIER_W = W-OPEN_X-OPEN_W # 39mm for MG90 + coupling + wall
OPEN_Z = BASE
PIVOT_Y = 9.5            # recess of axis; avoids front wall and servo body collision
PIVOT_Z = BASE + OPEN_H + 0.4
DOOR_T = 2.4
DOOR_W = OPEN_W - 2*FIT
DOOR_H = OPEN_H - 2*FIT
HINGE_D = 3.2
HINGE_SOCKET_D = HINGE_D + 2*FIT
HINGE_PIN_LEFT = 6.0
# V6 coupling INTERFACE: printed blank, drilled ONLY after inspecting actual horn.
# Delivers a centered datum and a useful door-side hub, NOT a final horn pattern.
DRIVE_DISC_R = 6.0
DRIVE_DISC_X0 = OPEN_X+OPEN_W-FIT-2.7
DRIVE_DISC_END_X = OPEN_X+OPEN_W+0.50 # face at x=111.5; shaft tip at x=113.7
DRIVE_JAMB_BORE_D = 2*(DRIVE_DISC_R+FIT)
# Actual attachment of cradle to printed base: four M2-size pilot bosses.
SERVO_FOOT_SIZE = 6.0
SERVO_FOOT_HEIGHT = 5.5
SERVO_SCREW_CLEARANCE_D = 2.3 # pilot / head tested on printed coupon
SERVO_SCREW_PILOT_D = 1.7
SERVO_SCREW_HEAD_D = 4.2
# Cable eyes and attic strap slots: real apertures, not marketing dimensions.
WIRE_EYE_OD = 8.0
WIRE_EYE_ID = 3.4
PCB_TIE_SLOT = (3.2, 4.2)
JAMB_RETURN_DEPTH = 10.0  # internal extension beyond front wall
JAMB_RETURN_THICK = WALL  # 2.4mm, outside door panel width
# V5: removable attic floor, XIAO/Wio stack ABOVE the garage, rear under roof.
ATTIC_Y0=55.0
ATTIC_DEPTH=40.0
ATTIC_Z0=46.0
ATTIC_PLATE_THICK=WALL
ATTIC_X0=WALL+FIT
ATTIC_W=W-2*(WALL+FIT)
ATTIC_LED_X=W/2
ATTIC_LED_Y=65.0
ATTIC_SUPPORT_WIDTH=4.0
ATTIC_SUPPORT_HEIGHT=WALL
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
LED_NOMINAL_D = 5.0 # WCS101 warm white et L7113NC orange : Ø nominal uniquement
LED_ENVELOPE = (6.0, 9.0) # enveloppe de service provisoire, pas une cote constructeur
LED_POCKET_D = 6.6 # envelope Ø6 + 0.30 mm radial par face
LED_ORANGE_APERTURE_D = 2.0 # ouverture optique discrete en facade
LED_ORANGE_RECESS = 3.4 # recul de l'optique dans le montant avant

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
# Two 10mm-deep interior returns, outside the door opening in X.
left_jamb_return=box(OPEN_X-JAMB_RETURN_THICK,WALL-0.05,BASE,
                     JAMB_RETURN_THICK,JAMB_RETURN_DEPTH+0.05,OPEN_H)
# Left hinge pin must retain 0.30mm radial clearance through this return.
left_jamb_return=left_jamb_return.cut(
  cyl_x(OPEN_X-JAMB_RETURN_THICK-0.1,PIVOT_Y,PIVOT_Z,
        HINGE_SOCKET_D,JAMB_RETURN_THICK+0.2))
right_jamb_return=box(OPEN_X+OPEN_W,WALL-0.05,BASE,
                      JAMB_RETURN_THICK,JAMB_RETURN_DEPTH+0.05,OPEN_H)
# Circular relief through the right inner reveal for the door-side coupling hub.
# Outer front fascia stays solid; the return below the axis still hides servo.
right_jamb_return=right_jamb_return.cut(cyl_x(
  OPEN_X+OPEN_W-0.1,PIVOT_Y,PIVOT_Z,DRIVE_JAMB_BORE_D,
  JAMB_RETURN_THICK+0.2))
shell=shell.fuse(left_jamb_return).fuse(right_jamb_return).clean()
# Bearing is not left hanging: flush landing ledge against the front wall.
BEARING_SEAT_Z=PIVOT_Z-11
bearing_shelf=box(3.0,WALL,BEARING_SEAT_Z-2.4,5.3,15.5,2.4)
shell=shell.fuse(bearing_shelf).clean()
# Low cable routing eyelets on side walls, away from door sweep and electronics.
wire_eyes=[]
for xcenter in (WALL+3.0,W-WALL-3.0):
 for ey in (35.0,73.0):
  ring=cyl_y(xcenter,ey,12.0,WIRE_EYE_OD,3.0)
  ring=ring.cut(cyl_y(xcenter,ey-0.1,12.0,WIRE_EYE_ID,3.2))
  wire_eyes.append(ring)
shell=union_all([shell]+wire_eyes)
# Low-profile ledges fused to the walls to support the removable attic shelf.
attic_left_ledge=box(WALL,ATTIC_Y0+2,ATTIC_Z0-ATTIC_SUPPORT_HEIGHT,
                     ATTIC_SUPPORT_WIDTH,ATTIC_DEPTH-4,ATTIC_SUPPORT_HEIGHT)
attic_right_ledge=box(W-WALL-ATTIC_SUPPORT_WIDTH,ATTIC_Y0+2,
                      ATTIC_Z0-ATTIC_SUPPORT_HEIGHT,ATTIC_SUPPORT_WIDTH,
                      ATTIC_DEPTH-4,ATTIC_SUPPORT_HEIGHT)
shell=shell.fuse(attic_left_ledge).fuse(attic_right_ledge).clean()
# Back power cable exit : a 12 x 8 mm slot, away from printed floor
shell=shell.cut(box(W/2-6,D-WALL-0.2,6,12,WALL+0.5,8))
# Upper rear low-voltage entry to attic (USB-C / RF lead routing).
# Clearance for actual connector/strain relief still to be measured.
shell=shell.cut(box(W/2-8,D-WALL-0.2,ATTIC_Z0+3,16,WALL+0.5,9))
# Recessed 5mm amber LED: provisional rear pocket and small optical aperture.
orange_x=OPEN_X+OPEN_W-15.0 # above opening, clear of V6 drive hub
orange_z=BASE+OPEN_H+8.3 # assez haut pour ne pas toucher la porte basculante
orange_holder=cyl_y(orange_x,WALL-0.2,orange_z,10.8,10.2)  # paroi radial >=2.1mm
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
door=door.fuse(pin)
# Printed integral Ø12mm pilot face for the supplied servo HORN.
# No screw holes: the actual DMS-MG90 horn must be offered up and drilled
# to its real pattern. Do NOT glue to the servo shaft or assume spline fit.
drive_disc=cyl_x(DRIVE_DISC_X0,PIVOT_Y,PIVOT_Z,2*DRIVE_DISC_R,
                 DRIVE_DISC_END_X-DRIVE_DISC_X0)
door=door.fuse(drive_disc).clean()

# 5. Bearing block (LEFT) with cylindrical hole 3.8mm for 3.2mm pin
# Compact left bearing entirely inside the 11mm left pier; no collision with shell.
bearing_x=OPEN_X-7.8
bearing_width=5.0
bearing=box(bearing_x,WALL+FIT,PIVOT_Z-11,bearing_width,14.6,19.0)
bearing=bearing.cut(cyl_x(bearing_x-0.1,PIVOT_Y,PIVOT_Z,HINGE_SOCKET_D,bearing_width+0.2))
# Add a small flange to permit attaching the bearing to the left masonry with adhesive or screws.
# Narrower fastening lug, left wall of bearing stays >= 0.30mm from shell.
flange=box(OPEN_X-8.0,WALL+0.5,PIVOT_Z-10,5.0,2.4,18.0)
bearing=bearing.fuse(flange).clean()
# The bearing rests on the printed shell shelf and can be glued after dry-fit;
# it is NOT yet a captive screw-mounted bearing.

# 6. Servo MG90 complet, dans le montant AVANT DROIT. Axe de sortie coaxial
# avec le pivot X de la porte (modele STEP: sortie suivant +Y d'origine).
# Rotations Z(+90) puis X(-90) : arbre dirigé selon -X du garage.
SERVO_SHAFT_TIP_X=door_x1+3.0  # provisional horn gap 3mm, 0.30mm clearance beside return
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
# Four thickened M2 pilot feet on cradle, secured FROM BELOW the base.
# Counterbores in base use flush-head screw geometry; test actual screw first.
SERVO_MOUNT_HOLES=[]
for xi in (cradle_xmin+4.0,cradle_xmax-7.5):
 for yi in (cradle_ymin+0.5,cradle_ymax-3.9):
  cradle=cradle.fuse(box(xi,yi,BASE,3.2,3.2,cradle_z_top-2.4-BASE+0.02))
  cradle=cradle.fuse(box(xi-1.4,yi-1.1,BASE,SERVO_FOOT_SIZE,
                         SERVO_FOOT_SIZE,SERVO_FOOT_HEIGHT))
  SERVO_MOUNT_HOLES.append((xi+1.6,yi+1.9))
cradle=cradle.clean()
for mx,my in SERVO_MOUNT_HOLES:
 base_plate=base_plate.cut(cq.Solid.makeCylinder(
   SERVO_SCREW_CLEARANCE_D/2,BASE+0.2,V(mx,my,-0.1),V(0,0,1)))
 base_plate=base_plate.cut(cq.Solid.makeCone(
   SERVO_SCREW_HEAD_D/2,SERVO_SCREW_CLEARANCE_D/2,1.2,
   V(mx,my,-0.01),V(0,0,1)))
 cradle=cradle.cut(cq.Solid.makeCylinder(
   SERVO_SCREW_PILOT_D/2,SERVO_FOOT_HEIGHT+0.01,
   V(mx,my,BASE-0.005),V(0,0,1)))
base_plate=base_plate.clean()
cradle=cradle.clean()
# Integrated slender RETENTION CLIP at back of servo, ~0.8mm lip intrusion.
# The STEP proxy still does not certify flexural life or servo variant fit.
servo_clip_stem=box(130.0,16.05,cradle_z_top-0.5,7.0,2.4,
                     57.6-(cradle_z_top-0.5))
servo_clip_lip=box(130.0,14.8,57.6,7.0,3.65,1.6)
cradle=cradle.fuse(servo_clip_stem).fuse(servo_clip_lip).clean()
# Horn drilling and precise case retainer strength require printed trial.

# 7. Removable full-width false ceiling at REAR, with XIAO/Wio above.
tray_x0=W/2-30
tray_y0=63.5
tray_z0=ATTIC_Z0
tray=box(ATTIC_X0,ATTIC_Y0,ATTIC_Z0,ATTIC_W,ATTIC_DEPTH,ATTIC_PLATE_THICK)
# Two underside ribs for stiffness, spaced clear of wall support ledges.
for y in (ATTIC_Y0+2.0,ATTIC_Y0+ATTIC_DEPTH-4.4):
    tray=tray.fuse(box(ATTIC_X0+5.2,y,ATTIC_Z0-2.4,
                       ATTIC_W-10.4,2.4,2.4))
# Rear PCB guides (no unverified exact holes/bolt positions).
tray=tray.fuse(box(tray_x0,tray_y0,ATTIC_Z0+ATTIC_PLATE_THICK,
                   60,2.4,2.4))
tray=tray.fuse(box(tray_x0,tray_y0+31-2.4,ATTIC_Z0+ATTIC_PLATE_THICK,
                   60,2.4,2.4))
# Wire feedthrough to the warm-white LED below, away from radio board.
tray=tray.cut(cq.Solid.makeCylinder(1.2,ATTIC_PLATE_THICK+0.2,
                     V(ATTIC_LED_X,ATTIC_LED_Y,ATTIC_Z0-0.1),V(0,0,1)))
# Two strap slots OUTSIDE vendor PCB envelope. Use a soft insulating pad;
# do not tighten a tie directly onto fragile SMD components.
PCB_STRAP_SLOTS=[(56.8,77.0),(89.7,77.0)]
for sx,sy in PCB_STRAP_SLOTS:
 tray=tray.cut(box(sx,sy,ATTIC_Z0-0.1,PCB_TIE_SLOT[0],
                   PCB_TIE_SLOT[1],ATTIC_PLATE_THICK+0.2))
# Four low printed support pads under Wio 3D footprint; 0.3mm vertical gap.
PCB_PADS=[(64.0,70.5),(81.0,70.5),(64.0,84.0),(81.0,84.0)]
for px,py in PCB_PADS:
 tray=tray.fuse(box(px,py,ATTIC_Z0+ATTIC_PLATE_THICK,4.0,3.0,3.2))
tray=tray.clean()
# Exact USB bend/antenna and board fastening remain unvalidated.

# 8. Liseré bleu supprimé : façade blanche sans pièce additionnelle.

# 9. Single white LED holder BELOW the false ceiling, lighting the garage.
# 0.2mm design overlap with attic tray is intentional for adhesive mounting;
# do not glue to the removable pitched roof.
led_white_x=ATTIC_LED_X
led_white_y=ATTIC_LED_Y
roof_under_z=H_FRONT-ROOF+(H_BACK-H_FRONT)*led_white_y/D
holder_bottom=ATTIC_Z0-9.8
holder=cq.Solid.makeCylinder(5.0,9.8,V(led_white_x,led_white_y,holder_bottom),V(0,0,1))
holder=holder.cut(cq.Solid.makeCylinder(LED_POCKET_D/2,10.2,
                   V(led_white_x,led_white_y,holder_bottom-0.1),V(0,0,1)))
# Actual LED assembly fit: flush annular face PLUS 2 alignment pegs
# Ø2mm in Ø2.6mm holes, 0.30mm RADIAL clearance. No overlap with ceiling ribs.
LED_HOLDER_PINS=[]
for sign in (-1,1):
 flange_x=led_white_x-9.0 if sign<0 else led_white_x+4.0
 holder=holder.fuse(box(flange_x,led_white_y-2.0,ATTIC_Z0-2.4,
                       5.0,4.0,2.4))
 pin_x=led_white_x+sign*6.5
 holder=holder.fuse(cq.Solid.makeCylinder(1.0,2.0,
                          V(pin_x,led_white_y,ATTIC_Z0),V(0,0,1)))
 LED_HOLDER_PINS.append((pin_x,led_white_y))
holder=holder.clean()
for px,py in LED_HOLDER_PINS:
 tray=tray.cut(cq.Solid.makeCylinder(1.3,ATTIC_PLATE_THICK+0.2,
                     V(px,py,ATTIC_Z0-0.1),V(0,0,1)))
tray=tray.clean()

PRINTABLE={
  '01_coque_blanche':shell,
  '02_socle_noir':base_plate,
  '03_toit_noir_pente':roof_lid,
  '04_porte_noire':door,
  '05_palier_gauche':bearing,
  '06_support_servo_step_0p3mm_PROTOTYPE':cradle,
  '07_faux_plafond_combles_XIAO':tray,
  '09_support_led_blanche':holder,
}

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
 raise FileNotFoundError(f'Reference CAD absente: {key}. Attendu: {path} ou {b64path}')

def build_xiao_onshape_proxy(detailed):
    """One clean solid preserving the overall original PCB+USB dimensions.

    The vendor STEP contains 77 component solids, including microscopic details.
    Onshape may mark this valid OpenCascade assembly as containing faults.
    This approximation is for visualization and spatial clearance ONLY:
    it does NOT preserve footprints, mounting-hole locations or electrical pins.
    The source BREP is left unchanged for accurate component-level references.
    """
    solids=detailed.Solids()
    if len(solids)<2:
        raise ValueError('Unexpected XIAO STEP topology')
    pcb=max(solids,key=lambda shape:shape.Volume())
    p=pcb.BoundingBox()
    original=detailed.BoundingBox()
    connectors=[shape for shape in solids if
                shape.BoundingBox().xmax>p.xmax+0.5 and
                shape.BoundingBox().ymax>p.ymax+1.0 and
                shape.Volume()>2.0]
    if not connectors:
        raise ValueError('USB connector not found in XIAO source geometry')
    u=max(connectors,key=lambda shape:shape.Volume()).BoundingBox()
    board=box(p.xmin,p.ymin,p.zmin,p.xlen,p.ylen,p.zlen)
    usb=box(u.xmin,u.ymin,u.zmin,u.xlen,u.ylen,u.zlen)
    clean=board.fuse(usb).clean()
    if not clean.isValid() or len(clean.Solids())!=1 or len(clean.Shells())!=1:
        raise ValueError('Onshape XIAO proxy is not a single valid solid')
    result=clean.BoundingBox()
    for got,expected in zip((result.xlen,result.ylen,result.zlen),
                            (original.xlen,original.ylen,original.zlen)):
        if abs(got-expected)>0.002:
            raise ValueError('XIAO proxy lost the original external envelope')
    return clean

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
 # Preserve the user's original 77-solid BREP for measurements and future CAD.
 XIAO_DETAILED_REFERENCE=ref_xiao.rotate((0,0,0),(1,0,0),90)
 XIAO_DETAILED_REFERENCE=XIAO_DETAILED_REFERENCE.translate(
     (XIAO_OFF_X,XIAO_OFF_Y,XIAO_OFF_Z))
 # Use this one-solid mechanical envelope in the STEP exported for Onshape.
 XIAO_ONSHAPE_PROXY=build_xiao_onshape_proxy(ref_xiao)
 XIAO_ONSHAPE_PROXY=XIAO_ONSHAPE_PROXY.rotate((0,0,0),(1,0,0),90)
 XIAO_ONSHAPE_PROXY=XIAO_ONSHAPE_PROXY.translate(
     (XIAO_OFF_X,XIAO_OFF_Y,XIAO_OFF_Z))
 REFERENCES['REF_XIAO_NRF52840_SIMPLIFIE_ONSHAPE_NE_PAS_IMPRIMER']=XIAO_ONSHAPE_PROXY
if ref_wio is not None:
 ref_wio=ref_wio.rotate((0,0,0),(0,0,1),90)
 ref_wio=ref_wio.translate((XIAO_OFF_X-119.16,XIAO_OFF_Y-108.29,WIO_OFF_Z))
 REFERENCES['REF_WIO_STEP_NE_PAS_IMPRIMER']=ref_wio
if ref_transistor is not None:
 ref_transistor=ref_transistor.translate((tray_x0+52,tray_y0+14,TRAY_TOP+0.5))
 REFERENCES['REF_BC547_STEP_NE_PAS_IMPRIMER']=ref_transistor
REFERENCES['REF_C1_470uF_16V_NE_PAS_IMPRIMER']=cq.Solid.makeCylinder(
 CAP_C1_BODY[0]/2,CAP_C1_BODY[1],V(W-14,35,BASE+5),V(0,0,1))
# Enveloppes de service des LED 5 mm : non destinees a l'impression.
REFERENCES['REF_LED_orange_ENVELOPPE_PROVISOIRE_NE_PAS_IMPRIMER']=cq.Solid.makeCylinder(
 LED_ENVELOPE[0]/2,LED_ENVELOPE[1],V(orange_x,LED_ORANGE_RECESS,orange_z),V(0,1,0))
REFERENCES['REF_LED_blanche_ENVELOPPE_PROVISOIRE_NE_PAS_IMPRIMER']=cq.Solid.makeCylinder(
 LED_ENVELOPE[0]/2,LED_ENVELOPE[1],V(led_white_x,led_white_y,holder_bottom+0.4),V(0,0,1))
servo_reference=ref_servo # volume de reference a verifier contre les LED et supports

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
       '07_faux_plafond_combles_XIAO':cq.Color(0.96,0.96,0.95),
       '09_support_led_blanche':cq.Color(0.96,0.96,0.95),
    }
    for name,s in PRINTABLE.items():
        assy.add(s,name=name,color=colors[name])
    for name,s in REFERENCES.items():
        assy.add(s,name=name,color=cq.Color(0.7,0.35,0.3,0.55))
    assy.save(str(STEP/'GarageStateClone_V2_assemblage_STEP_references.step'))
    # Fallback if any third-party STEP causes Onshape import issues:
    # the eight printable parts only, without manufacturer references.
    clean_structure=cq.Assembly(name='GarageStateClone_V2_structure_seule_Onshape')
    for name,solid in PRINTABLE.items():
        clean_structure.add(solid,name=name,color=colors[name])
    clean_structure.save(str(STEP/'GarageStateClone_V2_STRUCTURE_SANS_REFERENCES_ONSHAPE.step'))
    if ref_xiao is not None:
        exporters.export(XIAO_ONSHAPE_PROXY,
            str(STEP/'REF_XIAO_NRF52840_SIMPLIFIE_POUR_ONSHAPE.step'))
    (ROOT/'metriques_validation.json').write_text(json.dumps({'parameters_mm':{
        'width':W,'depth':D,'front_height':H_FRONT,'rear_height':H_BACK,
        'roof_slope_rise':H_BACK-H_FRONT,'wall':WALL,'roof':ROOF,'base':BASE,
        'fit_per_face':FIT,'opening_width':OPEN_W,'opening_height':OPEN_H,
        'door_width':DOOR_W,'door_height':DOOR_H,'hinge_diameter':HINGE_D,
        'bearing_hole_diameter':HINGE_SOCKET_D,
        'pivot_y':PIVOT_Y,'pivot_z':PIVOT_Z,
        'left_pier_width':LEFT_PIER_W,'right_pier_width':RIGHT_PIER_W,
        'door_offset_from_center':(OPEN_X+OPEN_W/2)-W/2,
        'compact_left_bearing_width':bearing_width,
        'led_white_y':led_white_y,'led_orange_x':orange_x,
        'door_drive_disc_outer_diameter':2*DRIVE_DISC_R,
        'door_drive_disc_face_x':DRIVE_DISC_END_X,
        'door_drive_gap_to_servo_shaft_nominal':SERVO_SHAFT_TIP_X-DRIVE_DISC_END_X,
        'door_drive_jamb_bore_diameter':DRIVE_JAMB_BORE_D,
        'servo_base_screw_centers_xy':SERVO_MOUNT_HOLES,
        'servo_m2_pilot_diameter':SERVO_SCREW_PILOT_D,
        'servo_m2_clearance_diameter':SERVO_SCREW_CLEARANCE_D,
        'pcb_strap_slots_xy':PCB_STRAP_SLOTS,
        'pcb_strap_slot_size':PCB_TIE_SLOT,
        'pcb_support_pad_positions_xy':PCB_PADS,
        'led_holder_pin_xy':LED_HOLDER_PINS,
        'attic_ceiling_bottom_z':ATTIC_Z0,
        'attic_ceiling_top_z':ATTIC_Z0+ATTIC_PLATE_THICK,
        'attic_y_start':ATTIC_Y0,'attic_depth':ATTIC_DEPTH,
        'attic_width':ATTIC_W,
        'attic_xiao_top_z':XIAO_DETAILED_REFERENCE.BoundingBox().zmax,
        'attic_roof_inner_z_above_xiao_front':H_FRONT-ROOF+(H_BACK-H_FRONT)*XIAO_DETAILED_REFERENCE.BoundingBox().ymin/D,
        'servo_complete_STEP_local_bbox_xyz':list(SERVO_CASE),'servo_axis_tip_x':SERVO_SHAFT_TIP_X,'card_service_envelope_proposed':list(CARD_ENVELOPE),
        'xiao_pcb_nominal_LW':list(XIAO_BOARD_NOMINAL),
        'wio_stack_nominal_xyz_seeed_marketing':list(WIO_STACK_NOMINAL),
        'capacitor_body_diameter_height':list(CAP_C1_BODY),
        'resistor_body_length_diameter':list(RESISTOR_BODY),
        'orange_optical_aperture_mm':LED_ORANGE_APERTURE_D,
        'orange_led_recess_from_front_mm':LED_ORANGE_RECESS,
        'led_pocket_provisional_diameter_mm':LED_POCKET_D,
        'led_service_envelope_provisional_diameter_length_mm':list(LED_ENVELOPE),
    },'parts':details,'reference_STEP_files':[k for k,v in REF_FILES.items() if v.exists()]},ensure_ascii=False,indent=2))
    print('Done:',STEP)