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
W = 105.6                  # V11 compact 55.0mm printed door + 0.3mm gaps + 11/39mm piers
D = 85.0                   # V12 compact: depth reduced 15mm, door/shell WIDTH stays V11
H_FRONT = 62.0             # roof TOP at front
H_BACK = 78.0              # roof top rear: 16mm rise across 100mm depth (V5)
WALL = 2.4                # minimum structural wall thickness >= 2
ROOF = 3.0                # roof solid thickness >= 2
BASE = 3.0                # floor solid thickness >= 2
FIT = 0.30                # clearance PER FACE for slide-on and hinged fits
ROOF_OVERHANG = 3.0
ROOF_SKIRT_DROP = 4.5
# V9 architectural detailing: shallow trapezoidal standing seams, on the
# TOP surface only, run in roof slope direction (garage +Y). The removable
# lid underside, slope and skirt engagement are intentionally unchanged.
ROOF_RIB_COUNT=9      # compact 105.6mm width: 9 ribs, same 11.5mm period
ROOF_RIB_FIRST_X=5.5
ROOF_RIB_PITCH=11.5
ROOF_RIB_BASE_W=2.5
ROOF_RIB_CROWN_W=1.1
ROOF_RIB_RISE=0.95
ROOF_RIB_OVERLAP=0.18
ROOF_RIB_Y0=-ROOF_OVERHANG  # connect top ribs to the visible FRONT folded fascia
ROOF_RIB_Y1=D+2.5
# V10: match the roof's standing seams on the DOWNWARD FRONT FASCIA too.
# Continuity over the front fold; strictly outside the white shell and above
# the orange LED optical opening (no structural change to the skirt inside).
ROOF_FASCIA_RIB_PROJECTION=0.85
ROOF_FASCIA_RIB_FUSE_OVERLAP=0.15
ROOF_FASCIA_RIB_BOTTOM_MARGIN=0.35
ROOF_FASCIA_RIB_BOTTOM_Z=H_FRONT-ROOF-ROOF_SKIRT_DROP-(
    H_BACK-H_FRONT)*ROOF_OVERHANG/D+ROOF_FASCIA_RIB_BOTTOM_MARGIN
ROOF_FASCIA_RIB_TOP_Z=H_FRONT-(H_BACK-H_FRONT)*ROOF_OVERHANG/D+ROOF_RIB_RISE
# V11 printed black door = 55mm EXACTLY; opening has 0.3mm
# clearance each side, so the opening itself is 55.6mm wide.
DOOR_TARGET_W=55.0
OPEN_W = DOOR_TARGET_W+2*FIT
OPEN_H = 42.0
LEFT_PIER_W = 11.0       # hinge bearing side, kept to preserve clearance
OPEN_X = LEFT_PIER_W
RIGHT_PIER_W = W-OPEN_X-OPEN_W  # 39mm motor-side pier maintained
OPEN_Z = BASE
if abs(RIGHT_PIER_W-39.0)>1e-8:
    raise ValueError("Servo-side pier must stay 39mm, not scaled with the door")
# V11: precisely 10mm between opening RIGHT EDGE and visible BLACK
# mailbox plaque LEFT EDGE, not between opening and the recess edge.
MAILBOX_GAP_OPEN_TO_BLACK=10.0
MAILBOX_POCKET_W=7.6
MAILBOX_POCKET_H=7.6
MAILBOX_POCKET_X0=OPEN_X+OPEN_W+MAILBOX_GAP_OPEN_TO_BLACK-FIT
MAILBOX_POCKET_Z0=29.3-MAILBOX_POCKET_H/2
MAILBOX_POCKET_DEPTH=1.05
MAILBOX_FACE_RELIEF_Y=0.10
MAILBOX_INSERT_W=MAILBOX_POCKET_W-2*FIT
MAILBOX_INSERT_H=MAILBOX_POCKET_H-2*FIT
MAILBOX_INSERT_THICK=0.75
MAILBOX_INSERT_X0=MAILBOX_POCKET_X0+FIT
MAILBOX_INSERT_Z0=MAILBOX_POCKET_Z0+FIT
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
# DMS-MG90/SER0039: drawing 33 mm across ears = garage Z,
# 30 mm along output axis = garage X, 12 mm transverse = garage Y.
# Supplied generic MG90-A STEP bounds (garage X,Y,Z)=(32.5,12.221,33.4).
# Earlier claim of 0.05mm end clearance mistakenly compared different axes.
# Actual DMS-MG90 dimensioned drawing supplied 23/11/2026.
# Garage axes: output shaft X, width Y, ear span Z.
# The 23mm case is centered in the 33mm ear span (5mm end margins).
# Shaft is 6mm from the NEAR case end => 11mm from near ear end.
SERVO_DRAWING_EAR_SPAN_Z=33.0
SERVO_DRAWING_CASE_SPAN_Z=23.0
SERVO_DRAWING_CASE_WIDTH_Y=12.0
SERVO_DRAWING_SHAFT_OFFSET_FROM_CASE_END_Z=6.0
SERVO_DRAWING_SHAFT_OFFSET_FROM_NEAR_EAR_END_Z=(SERVO_DRAWING_EAR_SPAN_Z-SERVO_DRAWING_CASE_SPAN_Z)/2+SERVO_DRAWING_SHAFT_OFFSET_FROM_CASE_END_Z
SERVO_DRAWING_SHAFT_FEATURE_DIAMETERS=(3.0,5.0)
SERVO_DRAWING_UPPER_LEVELS_FROM_BASE_X=(22.5,26.5,30.0)
SERVO_DRAWING_LUG_END_MARGIN_Z=(33.0-29.0)/2
SERVO_OFFICIAL_ORIENTED_XYZ=(30.0,12.0,33.0)
SERVO_VENDOR_ORIENTED_XYZ=(32.5,12.221,33.4)
SERVO_LUG_PITCH=29.0   # manufacturer drawing, two open-ended Ø2 notches
SERVO_LUG_NOTCH_D=2.0
SERVO_LUG_PILOT_D=1.7  # threaded pilot, trial fit supplied screws
SERVO_LUG_BOSS_D=5.8  # (5.8-1.7)/2=2.05 mm radial printed wall
# DMS-MG90 official drawing, measured from the BASE of the servo toward
# its output shaft: underside of mounting ears = exactly 16.00 mm.
# Garage X points FROM the shaft tip TOWARD the servo base, hence the
# underside-of-ear datum is 30 - 16 = 14 mm aft of the shaft tip.
SERVO_LUG_UNDERSIDE_FROM_BASE = 16.0  # dimensioned, authoritative datum
SERVO_LUG_BOSS_X_FROM_SHAFT_TIP = (
    SERVO_OFFICIAL_ORIENTED_XYZ[0] - SERVO_LUG_UNDERSIDE_FROM_BASE + FIT
)  # 14.30 mm: 0.30 mm printed clearance, not a tight press-fit
SERVO_LUG_BOSS_LENGTH=6.8
SERVO_LUG_PILOT_LEADIN_D=2.3
SERVO_LUG_PILOT_LEADIN_DEPTH=0.45
SERVO_SPINE_GUSSET_X_THICK=1.8
SERVO_SPINE_GUSSET_Y_REACH=5.4
SERVO_CABLE_WINDOW_WIDTH_X=5.0
# Provisional visual estimates supplied 2026-11-22, NOT machining datums.
# Do not use these to drive any tight feature or hole / fastener fit.
SERVO_LUG_THICKNESS_EST_MM=2.5
SERVO_LUG_TOP_TO_CASE_TOP_EST_MM=4.0
SERVO_LUG_TOP_TO_SHAFT_BOSS_TOP_EST_MM=8.0
# Unmeasured real horn and mounting screws remain explicitly unknown.
SERVO_HORN_MOUNTED_THICKNESS_MM=None
SERVO_MOUNT_SCREW_HEAD_D_MM=None
SERVO_MOUNT_SCREW_UNDER_HEAD_LENGTH_MM=None
# Lower four wire eyes removed in V11. Instead, C-shaped cable clips
# are printed on the INNER right wall from the removable attic shelf toward
# the servo. They follow Y and remain outside the door sweep and motor body.
SERVO_CABLE_CLIP_OUTER_D=7.4
SERVO_CABLE_CLIP_INNER_D=3.4
SERVO_CABLE_CLIP_WIDTH_Y=2.4
SERVO_CABLE_CLIP_ENTRY_GAP_Z=2.2
SERVO_CABLE_CLIP_YZ=((21.0,42.0),(31.0,42.5),(41.0,43.0),(51.0,43.5))
SERVO_CABLE_CLIP_X=W-WALL-2.1
PCB_TIE_SLOT = (3.2, 4.2)
JAMB_RETURN_DEPTH = 10.0  # internal extension beyond front wall
JAMB_RETURN_THICK = WALL  # 2.4mm, outside door panel width
# V5: removable attic floor, XIAO/Wio stack ABOVE the garage, rear under roof.
ATTIC_Y0=55.0
ATTIC_DEPTH=25.0  # V12 attic front edge Y55 unchanged; back edge moves 95 -> 80
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
# STEP original XYZ: X=ear span 33.4, Y=shaft direction 32.5,
# Z=transverse 12.22; MG90-A is not the exact DMS-MG90 SER0039.
# STEP fourni: servo complet avec pattes et arbre, repere d'origine XYZ.
SERVO_CASE = (33.4, 32.5, 12.22)
SERVO_OUTPUT_AXIS_LOCAL=(6.05,32.5,6.1)
CARD_ENVELOPE = (29.0, 25.0, 18.0) # enveloppe de service, non la taille des cartes
XIAO_BOARD_NOMINAL = (21.0, 17.8) # Seeed published PCB L x W, height unspecified
WIO_STACK_NOMINAL = (23.0, 22.0, 8.0) # Seeed marketing assembled approx; must measure physical stack
CAP_C1_BODY = (10.0, 13.0) # Gotronic 04947: diameter x height; lead pitch 5mm
RESISTOR_BODY = (6.5, 2.5) # all 0.5W specified Gotronic: axial length x diameter
LED_NOMINAL_D = 5.0 # white WCS101 nominal; exact warm-white profile unknown
LED_ENVELOPE = (6.0, 9.0) # conservative WHITE LED envelope; not published as exact
LED_POCKET_D = 6.6 # WHITE LED pocket Ø6 + 0.30mm radial per side
# V12 orange LED dimensions transcribed from the USER-SUPPLIED drawing.
# Body Ø5.0, retaining shoulder Ø5.9, overall front lens to rear shoulder
# 8.6mm, flange max 1mm, 2.54mm lead pitch, leads at least 27mm.
# Do not mistake 27mm exposed leads for the 8.6mm optical body length.
LED_ORANGE_BODY_D = 5.0
LED_ORANGE_FLANGE_D = 5.9
LED_ORANGE_LENS_TO_FLANGE_BACK = 8.6
LED_ORANGE_FLANGE_THICKNESS_MAX = 1.0
LED_ORANGE_PIN_PITCH = 2.54
LED_ORANGE_LEAD_LENGTH_MIN = 27.0
LED_ORANGE_BODY_BORE_D = LED_ORANGE_BODY_D + 2*FIT    # 5.6mm
LED_ORANGE_FLANGE_BORE_D = LED_ORANGE_FLANGE_D + 2*FIT  # 6.5mm
LED_ORANGE_HOLDER_OD = 9.0      # small integral socket (1.25mm ring at flange)
LED_ORANGE_HOLDER_LENGTH = 10.9
LED_ORANGE_FLANGE_SEAT_Y = 10.8
LED_ORANGE_APERTURE_D = 2.0    # discreet front pinhole, white wall remains solid
LED_ORANGE_RECESS = 3.4        # lens front face recessed 3.4mm from facade
LED_ORANGE_X = 5.3             # within 11mm left pier, below bearing, not by servo
LED_ORANGE_Z = 32.0            # holder top 36.5, left bearing shelf bottom Z37.0

# Gotronic 49067 USB-C 2.0 breakout; only 21x15x4.5 overall dimensions
# and 2.54mm pad pitch are published. Neither socket offset, board holes nor
# installed CC pull-downs are documented: this is a SERVICE ENVELOPE, not exact.
# Board long direction placed along garage Y, USB receptacle toward rear (+Y).
USB_C_BOARD_VENDOR_LWH_MM=(21.0,15.0,4.5)
USB_C_BOARD_X0=W/2-USB_C_BOARD_VENDOR_LWH_MM[1]/2 # 67.5
USB_C_BOARD_Y0=D-25.6  # V12:59.4; shifts 49067 rear to new shell wall
USB_C_BOARD_Z0=9.3
# V10 USB shell-only aperture is intentionally as small as practical:
# ~10 x 4.2mm, nominal USB-C metal receptacle face + printer clearance.
# Manufacturer publishes NO location of the actual receptacle on its board.
# This centered hole is a PROVISIONAL PARAMETRIC CUT, NOT a certified fit.
# Verify socket x/z with the received 49067 BEFORE printing final shell.
USB_C_REAR_APERTURE_WH=(10.0,4.2)
USB_C_REAR_APERTURE_Z0=9.45
USB_C_CARRIER_X0=USB_C_BOARD_X0-3.6
USB_C_CARRIER_Y0=USB_C_BOARD_Y0-2.0
USB_C_CARRIER_W=USB_C_BOARD_VENDOR_LWH_MM[1]+7.2
USB_C_CARRIER_D=USB_C_BOARD_VENDOR_LWH_MM[0]+3.2
USB_C_CARRIER_TOP_Z=USB_C_BOARD_Z0-FIT
USB_C_GUIDE_WIDTH=2.4
USB_C_GUIDE_HEIGHT=3.4
USB_C_STRAP_TUNNEL_YS=(D-21.0,D-10.5)  # V12 (64.0,74.5), two ties
USB_C_STRAP_TUNNEL_W=3.2 # for up-to-2.5mm nylon zip ties
USB_C_STRAP_TUNNEL_Z0=BASE+1.1
USB_C_STRAP_TUNNEL_H=2.7
USB_C_BOARD_ORIENTATION_STATUS="provisional: exact 49067 socket xy/z offset and actual plug clearance MUST be measured"
# V10 internal ONLY cable chase from rear USB/power distro up to attic,
# against the inner rear wall, shifted to X~95 to clear USB carrier X64..86.
# Open U guide + alternating small lips, no new hole through the shell.
CABLE_RISER_X0=W-15.6  # V10 x90.0 in V11, kept against rear-right interior
CABLE_RISER_INNER_W=7.2
CABLE_RISER_RAIL_W=1.8
CABLE_RISER_Y0=D-WALL-4.0
CABLE_RISER_DEPTH=4.12 # overlaps rear wall 0.12 to fuse solidly
CABLE_RISER_Z0=14.0
CABLE_RISER_HEIGHT=29.0 # ends Z43, below ceiling Z46
CABLE_RISER_LIP_ZS=(19.0,29.0,39.0)
CABLE_RISER_LIP_INSET=1.8
CABLE_RISER_LIP_DEPTH=1.2
CABLE_RISER_LIP_HEIGHT=2.0

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

def roof_standing_seam(xcenter):
    """Sloped trapezoidal roof standing seam, solid loft parallel to +Y.

    Its lower edge penetrates the solid top by 0.18mm to create a single
    watertight FDM printable roof. No changes underneath the existing lid.
    """
    def cross_section(y):
        roof_z=H_FRONT+(H_BACK-H_FRONT)*y/D
        zb=roof_z-ROOF_RIB_OVERLAP
        zt=roof_z+ROOF_RIB_RISE
        half_base=ROOF_RIB_BASE_W/2
        half_crown=ROOF_RIB_CROWN_W/2
        return cq.Wire.makePolygon([
            V(xcenter-half_base,y,zb), V(xcenter+half_base,y,zb),
            V(xcenter+half_crown,y,zt),V(xcenter-half_crown,y,zt),
            V(xcenter-half_base,y,zb)])
    return cq.Solid.makeLoft(
        [cross_section(ROOF_RIB_Y0),cross_section(ROOF_RIB_Y1)],True)

def front_fascia_standing_seam(xcenter):
    """Vertical trapezoidal rib down the front of the dark roof flashing.

    Uses the same X pitch/crown as the upper ribs and connects over the
    front fold at Y=-3.00, leaving the removable skirt's INNER face alone.
    """
    yface=-ROOF_OVERHANG
    outline=[
        (xcenter-ROOF_RIB_BASE_W/2,yface+ROOF_FASCIA_RIB_FUSE_OVERLAP),
        (xcenter+ROOF_RIB_BASE_W/2,yface+ROOF_FASCIA_RIB_FUSE_OVERLAP),
        (xcenter+ROOF_RIB_CROWN_W/2,yface-ROOF_FASCIA_RIB_PROJECTION),
        (xcenter-ROOF_RIB_CROWN_W/2,yface-ROOF_FASCIA_RIB_PROJECTION),
    ]
    return cq.Workplane("XY").polyline(outline).close().extrude(
        ROOF_FASCIA_RIB_TOP_Z-ROOF_FASCIA_RIB_BOTTOM_Z).translate(
        (0,0,ROOF_FASCIA_RIB_BOTTOM_Z)).val()

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
BEARING_SEAT_Z=PIVOT_Z-6.0
bearing_shelf=box(3.1,WALL,BEARING_SEAT_Z-2.4,5.0,12.0,2.4)
shell=shell.fuse(bearing_shelf).clean()
# The four former bottom Ø8 cable eyes are now absent altogether.
wire_eyes=[]
# V11: four C-shaped clips running along the right inside wall between
# the attic front edge (Y55) and the servo (Y<16). Each profile has an
# accessible 2.2mm opening facing inward (toward lower X), and a Ø3.4
# round cable passage aligned with Y. Ring wall is 2mm radially.
servo_cable_clips=[]
for cy,cz in SERVO_CABLE_CLIP_YZ:
    c=cyl_y(SERVO_CABLE_CLIP_X,cy-SERVO_CABLE_CLIP_WIDTH_Y/2,cz,
            SERVO_CABLE_CLIP_OUTER_D,SERVO_CABLE_CLIP_WIDTH_Y)
    c=c.cut(cyl_y(SERVO_CABLE_CLIP_X,cy-SERVO_CABLE_CLIP_WIDTH_Y/2-0.1,cz,
                  SERVO_CABLE_CLIP_INNER_D,SERVO_CABLE_CLIP_WIDTH_Y+0.2))
    c=c.cut(box(SERVO_CABLE_CLIP_X-SERVO_CABLE_CLIP_OUTER_D/2-0.15,
                cy-SERVO_CABLE_CLIP_WIDTH_Y/2-0.1,
                cz-SERVO_CABLE_CLIP_ENTRY_GAP_Z/2,
                (SERVO_CABLE_CLIP_OUTER_D-SERVO_CABLE_CLIP_INNER_D)/2+0.35,
                SERVO_CABLE_CLIP_WIDTH_Y+0.2,
                SERVO_CABLE_CLIP_ENTRY_GAP_Z))
    servo_cable_clips.append(c.clean())
shell=union_all([shell]+servo_cable_clips)
# Low-profile ledges fused to the walls to support the removable attic shelf.
attic_left_ledge=box(WALL,ATTIC_Y0+2,ATTIC_Z0-ATTIC_SUPPORT_HEIGHT,
                     ATTIC_SUPPORT_WIDTH,ATTIC_DEPTH-4,ATTIC_SUPPORT_HEIGHT)
attic_right_ledge=box(W-WALL-ATTIC_SUPPORT_WIDTH,ATTIC_Y0+2,
                      ATTIC_Z0-ATTIC_SUPPORT_HEIGHT,ATTIC_SUPPORT_WIDTH,
                      ATTIC_DEPTH-4,ATTIC_SUPPORT_HEIGHT)
shell=shell.fuse(attic_left_ledge).fuse(attic_right_ledge).clean()
# Rear USB-C service aperture centered on the BREAKOUT cradle (no exact
# mating-connector datum published by Gotronic). Replaces the old 12x8 low
# cable hole; keep power cabling wholly inside and strain-relieved.
shell=shell.cut(box(W/2-USB_C_REAR_APERTURE_WH[0]/2,D-WALL-0.2,
                   USB_C_REAR_APERTURE_Z0,USB_C_REAR_APERTURE_WH[0],
                   WALL+0.5,USB_C_REAR_APERTURE_WH[1]))
# The V8 upper rear 16x9 through-hole is REMOVED.
# All low-voltage wires now rise INSIDE along an open rear cable chase.
# No upper cutout is made in the shell.
# V12 orange LED relocation: just UNDER the compact LEFT bearing shelf.
# Small integral through-back socket: Ø5.6 body passage + Ø6.5 flange
# recess, no separate printable part or false 'snap-fit' assumptions.
# 3.4mm front optical recess leaves a discreet Ø2mm amber pinhole.
orange_x=LED_ORANGE_X
orange_z=LED_ORANGE_Z
orange_holder=cyl_y(orange_x,WALL-0.2,orange_z,
                    LED_ORANGE_HOLDER_OD,LED_ORANGE_HOLDER_LENGTH)
shell=shell.fuse(orange_holder)
shell=shell.cut(cyl_y(orange_x,-0.1,orange_z,
                      LED_ORANGE_APERTURE_D,LED_ORANGE_RECESS+0.2))
shell=shell.cut(cyl_y(orange_x,LED_ORANGE_RECESS,orange_z,
                      LED_ORANGE_BODY_BORE_D,
                      LED_ORANGE_FLANGE_SEAT_Y-LED_ORANGE_RECESS+0.15))
shell=shell.cut(cyl_y(orange_x,LED_ORANGE_FLANGE_SEAT_Y,orange_z,
                      LED_ORANGE_FLANGE_BORE_D,
                      WALL-0.2+LED_ORANGE_HOLDER_LENGTH-
                      LED_ORANGE_FLANGE_SEAT_Y+0.1))
# Insert from interior, optical tip rests against 2mm aperture shoulder.
# After checking light and polarity, fix flange with a small drop of
# NEUTRAL-CURE electronics-safe silicone; accessible rear for repair.
shell=shell.clean()
# Real garage: small black mailbox immediately RIGHT of the garage opening.
# Pocket cut only through 1.05mm of the 2.4mm front wall, NOT into the
# servo service envelope behind it. Black plaque printed as separate part.
mailbox_pocket=box(MAILBOX_POCKET_X0,-0.05,MAILBOX_POCKET_Z0,
                   MAILBOX_POCKET_W,MAILBOX_POCKET_DEPTH+0.05,
                   MAILBOX_POCKET_H)
shell=shell.cut(mailbox_pocket).clean()
mailbox_insert=box(MAILBOX_INSERT_X0,MAILBOX_FACE_RELIEF_Y,MAILBOX_INSERT_Z0,
                   MAILBOX_INSERT_W,MAILBOX_INSERT_THICK,MAILBOX_INSERT_H)
# Very shallow letter-slot cosmetic engraving on the black plaque front,
# not a functional opening; keeps the small adhesive plate one-piece.
MAILBOX_SLOT_X0=MAILBOX_INSERT_X0+0.85
MAILBOX_SLOT_Z0=MAILBOX_INSERT_Z0+MAILBOX_INSERT_H-1.7
mailbox_insert=mailbox_insert.cut(box(
    MAILBOX_SLOT_X0,MAILBOX_FACE_RELIEF_Y-0.02,MAILBOX_SLOT_Z0,
    MAILBOX_INSERT_W-1.7,0.22,0.40)).clean()

# Routed cable rise: two printed rear-side ribs and alternating partial lips
# form a NON-closed channel. Wires can be pushed in from the open interior.
# The external rear wall stays completely smooth, except the small USB-C port.
cable_riser_left=box(CABLE_RISER_X0,CABLE_RISER_Y0,CABLE_RISER_Z0,
    CABLE_RISER_RAIL_W,CABLE_RISER_DEPTH,CABLE_RISER_HEIGHT)
cable_riser_right=box(CABLE_RISER_X0+CABLE_RISER_RAIL_W+CABLE_RISER_INNER_W,
    CABLE_RISER_Y0,CABLE_RISER_Z0,CABLE_RISER_RAIL_W,
    CABLE_RISER_DEPTH,CABLE_RISER_HEIGHT)
cable_riser_lips=[]
for i,zc in enumerate(CABLE_RISER_LIP_ZS):
    xlip=(CABLE_RISER_X0+CABLE_RISER_RAIL_W-0.1
          if i%2==0 else CABLE_RISER_X0+CABLE_RISER_RAIL_W+
          CABLE_RISER_INNER_W-CABLE_RISER_LIP_INSET+0.1)
    lip=box(xlip,CABLE_RISER_Y0,zc,CABLE_RISER_LIP_INSET,
            CABLE_RISER_LIP_DEPTH,CABLE_RISER_LIP_HEIGHT)
    cable_riser_lips.append(lip)
shell=union_all([shell,cable_riser_left,cable_riser_right]+cable_riser_lips)

# 2. Base: floor 3mm and internal locating L rails with 0.30mm side gap
base_plate=box(0,0,0,W,D,BASE)
rail_z=BASE
rail_h=3.0
# Rails are INSIDE shell, their closest face 0.30 mm from the interior wall.
left_rail=box(WALL+FIT,14.0,rail_z,WALL,D-14.0-WALL-FIT-2.0,rail_h)
right_rail=box(W-2*WALL-FIT,14.0,rail_z,WALL,D-14.0-WALL-FIT-2.0,rail_h)
rear_rail=box(WALL+FIT+WALL,D-2*WALL-FIT,rail_z,W-2*(2*WALL+FIT),WALL,rail_h)
base_plate=union_all([base_plate,left_rail,right_rail,rear_rail])

# Integral USB-C 49067 carrier at center rear. The board is retained by
# two external nylon ties through HORIZONTAL tunnels under its support deck,
# never by invented PCB mounting holes or by clamping the USB receptacle.
# Fuses into the black floor: no additional printed part or captive screw.
usb_c_carrier=box(USB_C_CARRIER_X0,USB_C_CARRIER_Y0,BASE,
                  USB_C_CARRIER_W,USB_C_CARRIER_D,
                  USB_C_CARRIER_TOP_Z-BASE)
usb_c_guides=[
    box(gx,USB_C_BOARD_Y0+0.6,USB_C_CARRIER_TOP_Z,
        USB_C_GUIDE_WIDTH,USB_C_BOARD_VENDOR_LWH_MM[0]-2.0,
        USB_C_GUIDE_HEIGHT)
    for gx in (USB_C_CARRIER_X0,
               USB_C_CARRIER_X0+USB_C_CARRIER_W-USB_C_GUIDE_WIDTH)
]
usb_c_carrier=union_all([usb_c_carrier]+usb_c_guides)
usb_c_strap_tunnels=[]
for sy in USB_C_STRAP_TUNNEL_YS:
    tunnel=box(USB_C_CARRIER_X0-0.15,sy,USB_C_STRAP_TUNNEL_Z0,
               USB_C_CARRIER_W+0.30,USB_C_STRAP_TUNNEL_W,
               USB_C_STRAP_TUNNEL_H)
    usb_c_strap_tunnels.append(tunnel)
    usb_c_carrier=usb_c_carrier.cut(tunnel)
usb_c_carrier=usb_c_carrier.clean()
base_plate=base_plate.fuse(usb_c_carrier).clean()

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
# Raised, regularly spaced standing seams; structural roof plate stays
# exactly 3mm thick below the original roof face. The ribs are fused
# into the roof, not 13 separate loose or unprintable parts.
ROOF_RIB_XS=[ROOF_RIB_FIRST_X+i*ROOF_RIB_PITCH
             for i in range(ROOF_RIB_COUNT)]
roof_standing_seams=[roof_standing_seam(x) for x in ROOF_RIB_XS]
# Same standing-seam rhythm continues on the DOWNWARD front fascia.
roof_front_fascia_seams=[front_fascia_standing_seam(x) for x in ROOF_RIB_XS]
roof_lid=union_all([roof_lid]+roof_standing_seams+roof_front_fascia_seams)

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
bearing_x=OPEN_X-7.6
bearing_width=4.6
bearing_depth=12.0
bearing_height=12.0
bearing=box(bearing_x,WALL+FIT,PIVOT_Z-bearing_height/2,
            bearing_width,bearing_depth,bearing_height)
bearing=bearing.cut(cyl_x(bearing_x-0.1,PIVOT_Y,PIVOT_Z,
                          HINGE_SOCKET_D,bearing_width+0.2))
# Small glue flange matching the new 12mm tall bearing, no invented screw.
flange=box(OPEN_X-7.8,WALL+0.5,PIVOT_Z-5.8,4.6,2.4,11.6)
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
# Upper cable exit notch in the rear saddle wall (far end of servo).
# Leaves a continuous 2.4mm-high sill. The actual cable exit direction
# has not been manufacturer-dimensioned: this is open service clearance.
SERVO_CABLE_WINDOW_X0=cradle_xmax-8.5
SERVO_CABLE_WINDOW_Y0=cradle_ymax-0.2
SERVO_CABLE_WINDOW_Z0=cradle_z_top
cradle=cradle.cut(box(SERVO_CABLE_WINDOW_X0,SERVO_CABLE_WINDOW_Y0,
                      SERVO_CABLE_WINDOW_Z0,SERVO_CABLE_WINDOW_WIDTH_X,
                      2.8,4.0)).clean()
# Four M2 pilot feet attach the PRINTED cradle to the base from below.
# These 4 screws are distinct from the 2 manufacturer servo lug fasteners.
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
# Servo-specific attachment: TWO Ø2 open notches, 29mm between centres.
# M2 pilots run along garage X (parallel to shaft), at both Z extremities.
# The mounting pillars avoid the main body and are supported by a spine
# along its outboard side. X position derives ONLY from manufacturer datum
# base-to-ear underside 16mm, with FIT=0.30mm intentional relief.
# Supplied screw head/length and ear thickness must be trial-fitted.
# Dimensioned DMS-MG90 case-end shaft offset and ear span replace
# arbitrary centring on the third-party MG90-A STEP bounding box.
# Near ear end lies +Z, 11mm from shaft axis; notch centres 2mm
# from each ear end, giving pilot centres Z=(pivot-20, pivot+9).
SERVO_LUG_CENTERS_Z=(
 PIVOT_Z-(SERVO_DRAWING_EAR_SPAN_Z
          -SERVO_DRAWING_SHAFT_OFFSET_FROM_NEAR_EAR_END_Z
          -SERVO_DRAWING_LUG_END_MARGIN_Z),
 PIVOT_Z+(SERVO_DRAWING_SHAFT_OFFSET_FROM_NEAR_EAR_END_Z
          -SERVO_DRAWING_LUG_END_MARGIN_Z),
)
SERVO_LUG_CENTERS_YZ=[]
# Reference-only manufacturer datum for Onshape / dimensioning; computed
# from the CONFIRMED 16mm from base (not from three approximate offsets).
SERVO_MANUFACTURER_BASE_X = SERVO_SHAFT_TIP_X + SERVO_OFFICIAL_ORIENTED_XYZ[0]
SERVO_LUG_UNDERSIDE_DATUM_X = SERVO_MANUFACTURER_BASE_X - SERVO_LUG_UNDERSIDE_FROM_BASE
# Printed front face lies 0.30 mm aft of the nominal ear underside, so
# the surrogate MG90-A STEP and the actual ear are not force-fitted.
spine_x=SERVO_LUG_UNDERSIDE_DATUM_X+FIT
if abs(spine_x - (SERVO_SHAFT_TIP_X+SERVO_LUG_BOSS_X_FROM_SHAFT_TIP)) > 1e-8:
 raise ValueError("Inconsistent servo 16mm datum placement")
spine_y=cradle_ymax
spine_top=SERVO_LUG_CENTERS_Z[1]+2.5
spine=box(spine_x,spine_y,cradle_z_top-2.4,
          SERVO_LUG_BOSS_LENGTH,2.4,spine_top-(cradle_z_top-2.4))
cradle=cradle.fuse(spine)
# Add 2 tapered gussets behind the screw spine. No geometry intrudes
# into the servo case or the front screw-driver approach.
servo_spine_gussets=[]
for xg in (spine_x+0.3,spine_x+SERVO_LUG_BOSS_LENGTH
           -SERVO_SPINE_GUSSET_X_THICK-0.3):
    web=(cq.Workplane("YZ").polyline([
         (spine_y+1.2,cradle_z_top-2.2),
         (spine_y+SERVO_SPINE_GUSSET_Y_REACH,cradle_z_top-2.2),
         (spine_y+1.2,spine_top-2.0),
         ]).close().extrude(SERVO_SPINE_GUSSET_X_THICK)
         .translate((xg,0,0)).val())
    servo_spine_gussets.append(web)
cradle=union_all([cradle]+servo_spine_gussets)
for zc in SERVO_LUG_CENTERS_Z:
 boss=cyl_x(spine_x,PIVOT_Y,zc,SERVO_LUG_BOSS_D,SERVO_LUG_BOSS_LENGTH)
 rib=box(spine_x,PIVOT_Y+1.9,zc-1.15,
         SERVO_LUG_BOSS_LENGTH,spine_y-(PIVOT_Y+1.9)+0.5,2.3)
 cradle=cradle.fuse(boss).fuse(rib)
 cradle=cradle.cut(cyl_x(spine_x-0.1,PIVOT_Y,zc,
                          SERVO_LUG_PILOT_D,SERVO_LUG_BOSS_LENGTH+0.2))
 # Shallow conical lead-in only; preserve full-length pilot Ø1.7.
 cradle=cradle.cut(cq.Solid.makeCone(
     SERVO_LUG_PILOT_LEADIN_D/2,SERVO_LUG_PILOT_D/2,
     SERVO_LUG_PILOT_LEADIN_DEPTH,
     V(spine_x-0.01,PIVOT_Y,zc),V(1,0,0)))
 SERVO_LUG_CENTERS_YZ.append((PIVOT_Y,zc))
cradle=cradle.clean()
# Actual photo: round, cross, 2-arm and single-arm plastic horns are supplied.
# Round horn is the preferred option for torque transfer. The image does
# not provide a scale for horn holes, spline, hub thickness or screw length.
# Keep the door Ø12 interface blank, never pretend to know hole pitch.
# Dedicated mounting-ear coupon checks the genuine lug placement first.

# 7. Removable full-width false ceiling at REAR, with XIAO/Wio above.
tray_x0=W/2-30
# V12 radio stack center moves Y79 -> Y67.5 to fit 25mm deep attic.
# Vendor XIAO/Wio assembly Y envelope was ~70.1..87.9 in V11;
# shifting -11.5 puts it at ~58.6..76.4 inside [55,80].
tray_y0=ATTIC_Y0+ATTIC_DEPTH/2-15.5
tray_z0=ATTIC_Z0
tray=box(ATTIC_X0,ATTIC_Y0,ATTIC_Z0,ATTIC_W,ATTIC_DEPTH,ATTIC_PLATE_THICK)
# Two underside ribs for stiffness, spaced clear of wall support ledges.
for y in (ATTIC_Y0+2.0,ATTIC_Y0+ATTIC_DEPTH-4.4):
    tray=tray.fuse(box(ATTIC_X0+5.2,y,ATTIC_Z0-2.4,
                       ATTIC_W-10.4,2.4,2.4))
# V12: omit the two old full-width Y guide rails. A 25mm shelf has
# too little depth to keep both rails and the actual ~17.8mm Y board
# without trapping the 49067 cable or shorting vendor PCB components.
# Keep 4 insulating pads and the 2 outboard cable tie slots instead.
# Wire feedthrough to the warm-white LED below, away from radio board.
tray=tray.cut(cq.Solid.makeCylinder(1.2,ATTIC_PLATE_THICK+0.2,
                     V(ATTIC_LED_X,ATTIC_LED_Y,ATTIC_Z0-0.1),V(0,0,1)))
# Two strap slots OUTSIDE vendor PCB envelope. Use a soft insulating pad;
# do not tighten a tie directly onto fragile SMD components.
# The two strap slots and four pads must MOVE with the smaller cabinet.
# Old V10 values were anchored to global X and would miss the radio if not
# moved by the 22.2mm change in X centre; keep offsets from W/2 instead.
PCB_STRAP_SLOTS=[(W/2-18.2,ATTIC_Y0+10.5),(W/2+14.7,ATTIC_Y0+10.5)]
for sx,sy in PCB_STRAP_SLOTS:
 tray=tray.cut(box(sx,sy,ATTIC_Z0-0.1,PCB_TIE_SLOT[0],
                   PCB_TIE_SLOT[1],ATTIC_PLATE_THICK+0.2))
# Four low printed support pads under Wio 3D footprint; 0.3mm vertical gap.
PCB_PADS=[(W/2-11.0,ATTIC_Y0+4.0),(W/2+6.0,ATTIC_Y0+4.0),
          (W/2-11.0,ATTIC_Y0+17.5),(W/2+6.0,ATTIC_Y0+17.5)]
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
  '10_boite_aux_lettres_noire':mailbox_insert,
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
# Manufacturer published overall envelope only. This rectangular proxy is
# intentionally NOT an exact USB socket / PCB hole pattern.
usb_c_board_proxy=box(USB_C_BOARD_X0,USB_C_BOARD_Y0,USB_C_BOARD_Z0,
                      USB_C_BOARD_VENDOR_LWH_MM[1],
                      USB_C_BOARD_VENDOR_LWH_MM[0],
                      USB_C_BOARD_VENDOR_LWH_MM[2])
REFERENCES['REF_USB_C_49067_GABARIT_NON_CONTRACTUEL_NE_PAS_IMPRIMER']=usb_c_board_proxy
REFERENCES['REF_C1_470uF_16V_NE_PAS_IMPRIMER']=cq.Solid.makeCylinder(
 CAP_C1_BODY[0]/2,CAP_C1_BODY[1],V(W-14,35,BASE+5),V(0,0,1))
# Enveloppes de service des LED 5 mm : non destinees a l'impression.
# Actual LED head geometry from drawing (still no 27mm pin leads modelled).
# The 1mm shoulder thickness is the MAXIMUM drawing value, not a guaranteed
# precise measurement. This envelope must clear the body/flange recess.
REFERENCES['REF_LED_orange_ENVELOPPE_COTEE_NE_PAS_IMPRIMER']=(
    cyl_y(orange_x,LED_ORANGE_RECESS,orange_z,
          LED_ORANGE_BODY_D,LED_ORANGE_LENS_TO_FLANGE_BACK)
    .fuse(cyl_y(orange_x,
         LED_ORANGE_RECESS+LED_ORANGE_LENS_TO_FLANGE_BACK-
         LED_ORANGE_FLANGE_THICKNESS_MAX,
         orange_z,LED_ORANGE_FLANGE_D,LED_ORANGE_FLANGE_THICKNESS_MAX)).clean()
)
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
       '10_boite_aux_lettres_noire':cq.Color(0.06,0.07,0.08),
    }
    for name,s in PRINTABLE.items():
        assy.add(s,name=name,color=colors[name])
    for name,s in REFERENCES.items():
        assy.add(s,name=name,color=cq.Color(0.7,0.35,0.3,0.55))
    assy.save(str(STEP/'GarageStateClone_V2_assemblage_STEP_references.step'))
    # Fallback if any third-party STEP causes Onshape import issues:
    # all nine printable parts only, without manufacturer references.
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
        'roof_bac_acier_rib_count':ROOF_RIB_COUNT,
        'bottom_cable_eyelets_removed':len(wire_eyes)==0,
        'servo_cable_clip_count':len(servo_cable_clips),
        'servo_cable_clip_yz_mm':SERVO_CABLE_CLIP_YZ,
        'servo_cable_clip_axis':'Y, open toward decreasing X',
        'servo_cable_clip_inner_outer_diameters_mm':[SERVO_CABLE_CLIP_INNER_D,SERVO_CABLE_CLIP_OUTER_D],
        'servo_cable_clip_entry_gap_mm':SERVO_CABLE_CLIP_ENTRY_GAP_Z,
        'roof_front_fascia_rib_count':len(roof_front_fascia_seams),
        'roof_front_fascia_rib_projection_y_mm':ROOF_FASCIA_RIB_PROJECTION,
        'roof_front_fascia_rib_bottom_top_z_mm':[ROOF_FASCIA_RIB_BOTTOM_Z,ROOF_FASCIA_RIB_TOP_Z],
        'roof_front_fascia_ribs_aligned_with_top':True,
        'roof_bac_acier_rib_centres_x_mm':ROOF_RIB_XS,
        'roof_bac_acier_pitch_mm':ROOF_RIB_PITCH,
        'roof_bac_acier_trapezoid_base_crown_mm':[ROOF_RIB_BASE_W,ROOF_RIB_CROWN_W],
        'roof_bac_acier_rise_above_original_top_mm':ROOF_RIB_RISE,
        'roof_bac_acier_ribs_parallel_to':'Y, roof slope front to rear',
        'mailbox_pocket_xz_mm':[MAILBOX_POCKET_X0,MAILBOX_POCKET_Z0],
        'mailbox_visible_left_edge_x_mm':MAILBOX_INSERT_X0,
        'mailbox_gap_open_right_to_black_left_mm':MAILBOX_INSERT_X0-(OPEN_X+OPEN_W),
        'mailbox_insert_linear_reduction_from_v9_percent':30,
        'mailbox_insert_old_width_height_mm':[10.0,10.0],
        'mailbox_pocket_width_height_depth_mm':[MAILBOX_POCKET_W,MAILBOX_POCKET_H,MAILBOX_POCKET_DEPTH],
        'mailbox_wall_remaining_thickness_mm':WALL-MAILBOX_POCKET_DEPTH,
        'mailbox_insert_width_height_thickness_mm':[MAILBOX_INSERT_W,MAILBOX_INSERT_H,MAILBOX_INSERT_THICK],
        'mailbox_insert_surface_recession_y_mm':MAILBOX_FACE_RELIEF_Y,
        'mailbox_part_name':'10_boite_aux_lettres_noire',
        'fit_per_face':FIT,'opening_width':OPEN_W,'opening_height':OPEN_H,
        'exact_printed_door_target_width_mm':DOOR_TARGET_W,
        'door_width':DOOR_W,'door_height':DOOR_H,'hinge_diameter':HINGE_D,
        'bearing_hole_diameter':HINGE_SOCKET_D,
        'pivot_y':PIVOT_Y,'pivot_z':PIVOT_Z,
        'left_pier_width':LEFT_PIER_W,'right_pier_width':RIGHT_PIER_W,
        'door_offset_from_center':(OPEN_X+OPEN_W/2)-W/2,
        'compact_left_bearing_width':bearing_width,
        'compact_left_bearing_xyz_size_mm':[bearing_width,bearing_depth,bearing_height],
        'led_white_y':led_white_y,'led_orange_x':orange_x,
        'led_orange_z':orange_z,
        'orange_led_mount_under_left_bearing':True,
        'orange_led_housing_integral_shell':True,
        'orange_led_drawing_body_flange_d_mm':[LED_ORANGE_BODY_D,LED_ORANGE_FLANGE_D],
        'orange_led_drawing_length_flange_max_pitch_leads_mm':[
            LED_ORANGE_LENS_TO_FLANGE_BACK,LED_ORANGE_FLANGE_THICKNESS_MAX,
            LED_ORANGE_PIN_PITCH,LED_ORANGE_LEAD_LENGTH_MIN],
        'orange_led_body_flange_bore_d_mm':[LED_ORANGE_BODY_BORE_D,LED_ORANGE_FLANGE_BORE_D],
        'orange_led_holder_outer_d_length_mm':[LED_ORANGE_HOLDER_OD,LED_ORANGE_HOLDER_LENGTH],
        'orange_led_flange_seat_y_mm':LED_ORANGE_FLANGE_SEAT_Y,
        'door_drive_disc_outer_diameter':2*DRIVE_DISC_R,
        'door_drive_disc_face_x':DRIVE_DISC_END_X,
        'door_drive_gap_to_servo_shaft_nominal':SERVO_SHAFT_TIP_X-DRIVE_DISC_END_X,
        'door_drive_jamb_bore_diameter':DRIVE_JAMB_BORE_D,
        'servo_base_screw_centers_xy':SERVO_MOUNT_HOLES,
        'servo_lug_pitch_manufacturer_mm':SERVO_LUG_PITCH,
        'servo_dms_mg90_drawing_ear_case_width_mm':[
            SERVO_DRAWING_EAR_SPAN_Z,SERVO_DRAWING_CASE_SPAN_Z,
            SERVO_DRAWING_CASE_WIDTH_Y],
        'servo_dms_mg90_drawing_output_circular_d_mm':SERVO_DRAWING_SHAFT_FEATURE_DIAMETERS,
        'servo_dms_mg90_drawing_top_steps_from_base_mm':SERVO_DRAWING_UPPER_LEVELS_FROM_BASE_X,
        'servo_dms_mg90_drawing_shaft_from_case_end_mm':SERVO_DRAWING_SHAFT_OFFSET_FROM_CASE_END_Z,
        'servo_dms_mg90_drawing_shaft_from_near_ear_edge_mm':SERVO_DRAWING_SHAFT_OFFSET_FROM_NEAR_EAR_END_Z,
        'servo_dms_mg90_drawing_ear_notch_centres_z_mm':SERVO_LUG_CENTERS_Z,
        'servo_spine_gusset_count':len(servo_spine_gussets),
        'servo_cable_service_window_xyz_mm':[SERVO_CABLE_WINDOW_X0,
              SERVO_CABLE_WINDOW_Y0,SERVO_CABLE_WINDOW_Z0],
        'servo_cable_service_window_width_x_mm':SERVO_CABLE_WINDOW_WIDTH_X,
        'servo_lug_pilot_entry_d_depth_mm':[
            SERVO_LUG_PILOT_LEADIN_D,SERVO_LUG_PILOT_LEADIN_DEPTH],
        'servo_horn_preferred_shape':'round horn from supplied photo; dimensions NOT yet measured',
        'servo_lug_notch_diameter_manufacturer_mm':SERVO_LUG_NOTCH_D,
        'servo_lug_pilot_diameter_print_mm':SERVO_LUG_PILOT_D,
        'servo_lug_screw_centers_yz':SERVO_LUG_CENTERS_YZ,
        'servo_lug_screw_axis':'X (parallel to servo output axis)',
        'servo_manufacturer_base_plane_x_mm':SERVO_MANUFACTURER_BASE_X,
        'servo_lug_underside_from_base_manufacturer_mm':SERVO_LUG_UNDERSIDE_FROM_BASE,
        'servo_lug_underside_nominal_datum_x_mm':SERVO_LUG_UNDERSIDE_DATUM_X,
        'servo_lug_printed_boss_face_x_mm':spine_x,
        'servo_lug_nominal_axial_assembly_clearance_mm':FIT,
        'servo_ear_thickness_estimated_mm':SERVO_LUG_THICKNESS_EST_MM,
        'servo_ear_top_to_case_top_estimated_mm':SERVO_LUG_TOP_TO_CASE_TOP_EST_MM,
        'servo_ear_top_to_shaft_boss_top_estimated_mm':SERVO_LUG_TOP_TO_SHAFT_BOSS_TOP_EST_MM,
        'servo_horn_mounted_thickness_mm':SERVO_HORN_MOUNTED_THICKNESS_MM,
        'servo_mount_screw_head_diameter_mm':SERVO_MOUNT_SCREW_HEAD_D_MM,
        'servo_mount_screw_under_head_length_mm':SERVO_MOUNT_SCREW_UNDER_HEAD_LENGTH_MM,
        'servo_official_oriented_xyz_mm':list(SERVO_OFFICIAL_ORIENTED_XYZ),
        'servo_vendor_step_oriented_xyz_mm':list(SERVO_VENDOR_ORIENTED_XYZ),
        'servo_m2_pilot_diameter':SERVO_SCREW_PILOT_D,
        'servo_m2_clearance_diameter':SERVO_SCREW_CLEARANCE_D,
        'pcb_strap_slots_xy':PCB_STRAP_SLOTS,
        'pcb_strap_slot_size':PCB_TIE_SLOT,
        'pcb_support_pad_positions_xy':PCB_PADS,
        'led_holder_pin_xy':LED_HOLDER_PINS,
        'attic_ceiling_bottom_z':ATTIC_Z0,
        'attic_ceiling_top_z':ATTIC_Z0+ATTIC_PLATE_THICK,
        'attic_y_start':ATTIC_Y0,'attic_depth':ATTIC_DEPTH,
        'attic_back_edge_y_mm':ATTIC_Y0+ATTIC_DEPTH,
        'radio_y_shift_from_v11_mm':-11.5,
        'radio_old_xy_guides_removed':True,
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
        'usb_c_49067_vendor_lwh_mm':list(USB_C_BOARD_VENDOR_LWH_MM),
        'usb_c_49067_board_nominal_xyz_start_mm':[USB_C_BOARD_X0,USB_C_BOARD_Y0,USB_C_BOARD_Z0],
        'usb_c_rear_service_slot_width_height_mm':list(USB_C_REAR_APERTURE_WH),
        'usb_c_port_aperture_is_provisional':True,
        'rear_upper_attic_through_hole_removed':True,
        'cable_riser_inner_rear_wall_only':True,
        'cable_riser_x0_y0_z0_mm':[CABLE_RISER_X0,CABLE_RISER_Y0,CABLE_RISER_Z0],
        'cable_riser_inner_width_depth_height_mm':[CABLE_RISER_INNER_W,CABLE_RISER_DEPTH,CABLE_RISER_HEIGHT],
        'cable_riser_retaining_lip_count':len(cable_riser_lips),
        'usb_c_rear_service_slot_z0_mm':USB_C_REAR_APERTURE_Z0,
        'usb_c_carrier_xyz_min_mm':[USB_C_CARRIER_X0,USB_C_CARRIER_Y0,BASE],
        'usb_c_carrier_xy_width_depth_mm':[USB_C_CARRIER_W,USB_C_CARRIER_D],
        'usb_c_carrier_top_z_mm':USB_C_CARRIER_TOP_Z,
        'usb_c_carrier_guides_width_height_mm':[USB_C_GUIDE_WIDTH,USB_C_GUIDE_HEIGHT],
        'usb_c_carrier_tunnel_centres_y_mm':[sy+USB_C_STRAP_TUNNEL_W/2 for sy in USB_C_STRAP_TUNNEL_YS],
        'usb_c_carrier_strap_tunnel_width_height_mm':[USB_C_STRAP_TUNNEL_W,USB_C_STRAP_TUNNEL_H],
        'usb_c_carrier_integrated_into':'02_socle_noir',
        'usb_c_board_connector_face_and_fastener_holes':'UNKNOWN; actual 49067 placement to dry-fit',
        'usb_c_board_orientation_status':USB_C_BOARD_ORIENTATION_STATUS,
    },'parts':details,'reference_STEP_files':[k for k,v in REF_FILES.items() if v.exists()]},ensure_ascii=False,indent=2))
    print('Done:',STEP)