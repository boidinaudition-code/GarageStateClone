#!/usr/bin/env python3
"""Small, OPTIONAL calibration STL parts; NOT part of the 9 printable garage bodies.

Print coupons first on the Bambu P1S at the same material, wall count and
orientation as the actual mechanical pieces. Do not assume these demonstrate
the unmeasured SER0039 horn spline / ears or PCB fastening geometry.
"""
from pathlib import Path
import cadquery as cq

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"coupons"
OUT.mkdir(parents=True,exist_ok=True)
V=cq.Vector

def box(x,y,z,l,w,h):
    return cq.Workplane("XY").box(l,w,h,centered=False).translate((x,y,z)).val()

def cylinder(z,x,y,diameter,height):
    return cq.Solid.makeCylinder(diameter/2,height,V(x,y,z),V(0,0,1))

def save(shape,name):
    if not shape.isValid() or len(shape.Solids())!=1:
        raise AssertionError(f"Invalid coupon {name}")
    from cadquery import exporters
    path=OUT/(name+".stl")
    exporters.export(shape,str(path),tolerance=0.05,angularTolerance=0.15)
    print("Coupon:",path.name,"volume=",round(shape.Volume(),1))

# A: same Ø3.2 integral door pin, trial holes with radial 0.2 / 0.3 / 0.4.
hinge=box(0,0,0,36,13,6)
for x,diameter in ((6,3.6),(18,3.8),(30,4.0)):
    hinge=hinge.cut(cylinder(-.1,x,6.5,diameter,6.2))
hinge=hinge.clean()
save(hinge,"A_axe_D3p2_alesages_D3p6_D3p8_D4p0")

# B: printed pilot holes for trial M2 machine screw and countersunk head.
# Pilot 1.6, 1.7, 1.8 => fit depends on material / screw / layer adhesion.
foot=box(0,0,0,40,12,8)
for x,diameter in ((7,1.6),(20,1.7),(33,1.8)):
    foot=foot.cut(cylinder(-.1,x,6,diameter,8.2))
    foot=foot.cut(cq.Solid.makeCone(2.1,1.15,1.2,V(x,6,-.01),V(0,0,1)))
foot=foot.clean()
save(foot,"B_vis_M2_pilotes_D1p6_D1p7_D1p8")

# C: face trial blank to offer up the EXACT horn delivered with the servo.
# Diameter Ø12, thickness 3.5mm; shallow center and 3mm registration dots.
# These are VISUAL datums only, not usable blind through-holes / screw pitch.
horn=cylinder(0,10,10,12,3.5)
for x,y in ((10,10),(7.0,10),(13.0,10)):
    horn=horn.cut(cylinder(3.15,x,y,.7,.45))
horn=horn.clean()
save(horn,"C_gabarit_face_palonnier_D12_SANS_ENTRAXE_VALIDE")

# D (V13): two ear-pilot centres exactly 29mm apart from DMS-MG90 drawing,
# centred on a simple 45mm × 10mm trial bridge. Use it only to check
# actual ear notch pitch / M2 supplied screws before printing full cradle.
# This is NOT a measured horn drill template.
lug=box(0,0,0,45,10,6)
for x in (8.0,37.0):
    lug=lug.cut(cylinder(-0.1,x,5.0,1.7,6.2))
    lug=lug.cut(cq.Solid.makeCone(1.15,0.85,0.45,
                                 V(x,5,5.6),V(0,0,1)))
lug=lug.clean()
save(lug,"D_DMS_MG90_oreilles_entraxe29_pilotes_D1p7")
