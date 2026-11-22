#!/usr/bin/env python3
"""Régression CAO : BREP source, 8 STEP, 8 STL et assemblage V2.

Lancer après: python cad/generate_cad.py
Ne prétend pas remplacer un essai d'impression ou un montage mécanique.
"""
from __future__ import annotations

import base64
import hashlib
import json
import math
from pathlib import Path
import tempfile
import zlib

import cadquery as cq
import trimesh
import generate_cad as g

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "vendor_models/manifest.json").read_text(encoding="utf-8"))
bom = json.loads((ROOT / "bom_dimensions_v1.json").read_text(encoding="utf-8"))
assert bom["system_state"]["sensor_count"] == 1
assert manifest["design"]["shell_mm"][0] == g.W == bom["cad"]["shell_width_mm"] == 150
assert manifest["design"]["door_opening_mm"][0] == g.OPEN_W == bom["cad"]["door_opening_mm"][0] == 100
assert g.WALL >= 2 and g.ROOF >= 2 and g.BASE >= 2 and g.FIT == 0.3
assert g.LED_ENVELOPE == (6.0, 9.0)
assert len(g.PRINTABLE) == 8
assert not any("liseret" in k or "bleu" in k for k in g.PRINTABLE)
assert g.JAMB_RETURN_DEPTH == 10.0
assert g.JAMB_RETURN_THICK >= 2.0
assert abs(g.SERVO_SHAFT_TIP_X-g.door_x1-3.0) < 1e-6
# Roof attic geometry, stack reserve and mounting plane.
assert g.H_FRONT == 62.0 and g.H_BACK == 78.0
assert g.H_BACK-g.H_FRONT == 16.0
assert manifest["design"]["roof_z_front_back_mm"] == [62,78]
assert bom["cad"]["front_height_mm"] == 62 and bom["cad"]["back_height_mm"] == 78
assert bom["cad"]["attic_ceiling_bottom_z_mm"] == g.ATTIC_Z0 == 46
assert bom["cad"]["attic_ceiling_depth_mm"] == g.ATTIC_DEPTH == 40
assert bom["cad"]["attic_ceiling_width_mm"] == g.ATTIC_W == 144.6
assert g.ATTIC_PLATE_THICK == g.WALL == 2.4
assert "07_faux_plafond_combles_XIAO" in g.PRINTABLE
assert g.LEFT_PIER_W == g.OPEN_X == 11.0
assert g.RIGHT_PIER_W == 39.0
assert g.door_x1 < g.right_jamb_return.BoundingBox().xmin
assert g.bearing_width == 5.0
assert bom["cad"]["left_pier_width_mm"] == 11
assert bom["cad"]["right_pier_width_mm"] == 39
assert bom["cad"]["door_offset_from_center_mm"] == -14.0

# Vérifier l'intégrité des fichiers BREP GitHub indépendamment des STEP d'origine.
for component in manifest["components"]:
    name = component["key"]
    source = ROOT / "refs" / (name + ".brep.z.b64")
    if not source.is_file():
        raise AssertionError(f"BREP de reference absente : {name}")
    packed = base64.b64decode(source.read_bytes().strip(), validate=True)
    brep = zlib.decompress(packed)
    actual = hashlib.sha256(brep).hexdigest()
    assert actual == component["brep_sha256"], f"Reference {name} modifiee/corrompue: {actual}"
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / (name + ".brep")
        path.write_bytes(brep)
        shape = cq.Shape.importBrep(str(path))
        assert shape.isValid()
        assert len(shape.Solids()) == component["solids"]
    print("BREP valide", name, component["solids"], "solides")

# On teste la réimportation de chaque STEP, et pas simplement sa présence.
for name, printable in g.PRINTABLE.items():
    assert printable.isValid() and len(printable.Solids()) == 1
    step_path = ROOT / "step" / (name + ".step")
    stl_path = ROOT / "stl" / (name + ".stl")
    assert step_path.stat().st_size > 1000, step_path
    data = step_path.read_bytes()
    assert data.startswith(b"ISO-10303-21;") and b"END-ISO-10303-21;" in data[-200:], step_path
    imported = cq.importers.importStep(str(step_path)).val()
    assert imported.isValid() and len(imported.Solids()) == 1, step_path
    assert math.isclose(imported.Volume(), printable.Volume(), rel_tol=1e-5, abs_tol=1e-3)
    mesh = trimesh.load_mesh(str(stl_path))
    assert mesh.is_watertight and mesh.is_volume, stl_path
    print("STEP/STL valides", name, "volume =", round(printable.Volume(), 2), "mm³")

assy_path = ROOT / "step/GarageStateClone_V2_assemblage_STEP_references.step"
assert assy_path.stat().st_size > 1000000
assy_data = assy_path.read_bytes()
assert assy_data.startswith(b"ISO-10303-21;") and b"END-ISO-10303-21;" in assy_data[-200:]
# Onshape-safe XIAO: one shell and one solid, same overall XYZ bounding
# box as the unmodified 77-solid source model.
xiao_path = ROOT / "step/REF_XIAO_NRF52840_SIMPLIFIE_POUR_ONSHAPE.step"
assert xiao_path.is_file()
xiao = cq.importers.importStep(str(xiao_path)).val()
assert xiao.isValid() and len(xiao.Solids()) == 1 and len(xiao.Shells()) == 1
assert len(g.XIAO_DETAILED_REFERENCE.Solids()) == 77
assert len(g.XIAO_ONSHAPE_PROXY.Solids()) == 1
source_bbox = g.XIAO_DETAILED_REFERENCE.BoundingBox()
safe_bbox = xiao.BoundingBox()
for k in ("xmin","xmax","ymin","ymax","zmin","zmax"):
    assert abs(getattr(source_bbox,k)-getattr(safe_bbox,k)) < .005, ("XIAO bbox",k)
structure_path = ROOT / "step/GarageStateClone_V2_STRUCTURE_SANS_REFERENCES_ONSHAPE.step"
assert structure_path.stat().st_size > 1000
structure = cq.importers.importStep(str(structure_path)).val()
assert structure.isValid() and len(structure.Solids()) == 8
assert len(list((ROOT / "step").glob("*.step"))) == 11
assert len(list((ROOT / "stl").glob("*.stl"))) == 8

def overlap(a, b):
    aa, bb = a.BoundingBox(), b.BoundingBox()
    if (
        aa.xmax <= bb.xmin or aa.xmin >= bb.xmax or
        aa.ymax <= bb.ymin or aa.ymin >= bb.ymax or
        aa.zmax <= bb.zmin or aa.zmin >= bb.zmax
    ):
        return 0.0
    return a.intersect(b).Volume()

assert g.shell.isValid() and len(g.shell.Solids()) == 1
assert g.left_jamb_return.Volume() > 500
assert g.right_jamb_return.Volume() > 500
assert overlap(g.bearing,g.left_jamb_return) < 1e-5
assert overlap(g.bearing,g.shell) < 1e-5, "compact bearing / wall"
assert g.bearing.BoundingBox().xmin >= g.WALL + g.FIT - 1e-6
assert g.cradle.BoundingBox().xmax <= g.W-g.WALL-g.FIT + 1e-6
assert overlap(g.cradle,g.right_jamb_return) < 1e-5
# V6 mechanical features: real mounting features, NOT merely reference boxes.
assert len(g.SERVO_MOUNT_HOLES)==4
assert g.SERVO_LUG_PITCH == 29.0
assert g.SERVO_LUG_NOTCH_D == 2.0
assert g.SERVO_LUG_PILOT_D == 1.7
assert (g.SERVO_LUG_BOSS_D - g.SERVO_LUG_PILOT_D)/2 >= 2.0, "lug pilot boss wall too thin"
assert len(g.SERVO_LUG_CENTERS_YZ) == 2
assert len(g.SERVO_LUG_CENTERS_Z) == 2
assert math.isclose(g.SERVO_LUG_CENTERS_Z[1] - g.SERVO_LUG_CENTERS_Z[0], 29, abs_tol=1e-6)
assert [*g.SERVO_OFFICIAL_ORIENTED_XYZ] == bom["cad"]["servo_official_oriented_xyz_mm"]
assert [*g.SERVO_VENDOR_ORIENTED_XYZ] == bom["cad"]["servo_vendor_step_oriented_xyz_mm"]
assert bom["cad"]["servo_lug_screw_count"] == manifest["design"]["servo_ear_mount_count"] == 2
assert bom["cad"]["servo_base_mount_count"] == 4
assert len(g.wire_eyes)==4
assert len(g.PCB_STRAP_SLOTS)==2
assert len(g.PCB_PADS)==4
assert len(g.LED_HOLDER_PINS)==2
assert g.SERVO_SCREW_CLEARANCE_D==2.3
assert g.SERVO_SCREW_PILOT_D==1.7
assert (g.SERVO_FOOT_SIZE-g.SERVO_SCREW_PILOT_D)/2>=2
# Both genuine ear pilot holes run along garage X, outside the case centre.
for ey,ez in g.SERVO_LUG_CENTERS_YZ:
    hole=cq.Solid.makeCylinder(g.SERVO_LUG_PILOT_D/2,
                              g.SERVO_LUG_BOSS_LENGTH+0.2,
                              cq.Vector(g.spine_x-0.1,ey,ez), cq.Vector(1,0,0))
    assert overlap(g.cradle,hole)<1e-5, ("servo lug pilot blocked",ez)
assert not hasattr(g,"servo_clip_lip"), "fragile unverified hook should be removed"
assert (g.WIRE_EYE_OD-g.WIRE_EYE_ID)/2>=2
assert g.DRIVE_DISC_R==6
assert math.isclose(g.DRIVE_JAMB_BORE_D-2*g.DRIVE_DISC_R,2*g.FIT)
assert math.isclose(g.DRIVE_DISC_END_X,111.5)
assert math.isclose(g.SERVO_SHAFT_TIP_X-g.DRIVE_DISC_END_X,2.2)
assert g.door.distance(g.shell)>=g.FIT-0.01
assert g.bearing.distance(g.shell)<0.01 # bearing rests on integral shelf
assert g.cradle.distance(g.base_plate)<0.01 # M2 feet rest on 3mm base
# Four foot pilots and their base countersinks are coaxial.
for cx,cy in g.SERVO_MOUNT_HOLES:
    bore=cq.Solid.makeCylinder(g.SERVO_SCREW_CLEARANCE_D/2,
       g.BASE+0.2,cq.Vector(cx,cy,-0.1),cq.Vector(0,0,1))
    assert overlap(g.base_plate,bore)<1e-5
    pilot=cq.Solid.makeCylinder(g.SERVO_SCREW_PILOT_D/2,
       g.SERVO_FOOT_HEIGHT,cq.Vector(cx,cy,g.BASE),cq.Vector(0,0,1))
    assert overlap(g.cradle,pilot)<1e-5
# Wio support pads are 0.3mm below the detailed Wio model.
assert math.isclose(g.ATTIC_Z0+g.ATTIC_PLATE_THICK+3.2+g.FIT,
                    g.ref_wio.BoundingBox().zmin,abs_tol=0.02)
assert g.ATTIC_LED_Y == 65.0
assert g.orange_x == g.OPEN_X+g.OPEN_W-15.0
servo = next(s for n, s in g.REFERENCES.items() if "MG90" in n)
assert overlap(servo,g.right_jamb_return) < 1e-5
assert overlap(servo,g.shell) < 1e-5
orange = next(s for n, s in g.REFERENCES.items() if "LED_orange" in n)
white = next(s for n, s in g.REFERENCES.items() if "LED_blanche" in n)
for part, shape in {
    "coque": g.shell, "toit": g.roof_lid,
    "porte": g.door, "support servo": g.cradle,
    "logement orange": g.orange_holder
}.items():
    assert overlap(servo, shape) < 1e-5, ("collision servo", part)
for led_name, shape in {"orange": orange, "blanche": white}.items():
    assert overlap(shape, servo) < 1e-5, ("collision LED/servo", led_name)
    assert overlap(shape, g.shell) < 1e-5, ("collision LED/coque", led_name)
assert overlap(white, g.roof_lid) < 1e-5
assert overlap(white, g.holder) < 1e-5
assert overlap(g.holder, g.roof_lid) < 1e-5  # roof remains removable
assert overlap(g.holder, g.tray) < 1e-5  # true assembly, not overlapping solids
assert g.holder.distance(g.tray) < 0.01  # contact / two aligned Ø2mm guide pins
# True attic: XIAO and Wio completely above the false ceiling, below pitched roof.
xiao = next(s for n,s in g.REFERENCES.items() if "XIAO" in n)
wio = next(s for n,s in g.REFERENCES.items() if "WIO" in n)
bc547 = next(s for n,s in g.REFERENCES.items() if "BC547" in n)
for refname, component in {"XIAO":xiao, "Wio":wio, "BC547":bc547}.items():
    assert component.BoundingBox().zmin > g.ATTIC_Z0+g.ATTIC_PLATE_THICK
    for name, part in {"false_ceiling":g.tray, "roof":g.roof_lid,
                       "walls":g.shell}.items():
        assert overlap(component,part)<1e-5, ("attic part collision",refname,name)
assert overlap(g.tray,g.shell) < 1e-5
assert overlap(g.tray,g.roof_lid) < 1e-5
assert overlap(g.tray,g.cradle) < 1e-5
assert overlap(g.tray,servo) < 1e-5
assert overlap(g.tray,g.attic_left_ledge) < 1e-5
assert overlap(g.tray,g.attic_right_ledge) < 1e-5
assert g.attic_left_ledge.Volume()>200 and g.attic_right_ledge.Volume()>200
# At the front of the XIAO envelope, even with a sloping roof there is a
# minimum theoretical roof clearance >5mm (connectors/cables remain unvalidated).
bb=xiao.BoundingBox()
roof_under=g.H_FRONT-g.ROOF+(g.H_BACK-g.H_FRONT)*bb.ymin/g.D
assert roof_under-bb.zmax>=5.0, ("insufficient XIAO roof clearance",roof_under-bb.zmax)
print("ATTIC XIAO roof clearance at forward edge:",round(roof_under-bb.zmax,2),"mm")
assert overlap(g.orange_holder, g.roof_lid) < 1e-5

# Porte rigide pivotant vers l'intérieur : échantillonnage 0...90°.
for angle in range(0, 91, 5):
    door = g.door.rotate(
        (0, g.PIVOT_Y, g.PIVOT_Z),
        (1, g.PIVOT_Y, g.PIVOT_Z),
        angle,
    )
    assert overlap(door,g.tray) < 1e-5, ("door / attic false ceiling",angle)
    assert overlap(door,g.holder) < 1e-5, ("door / attic LED",angle)
    assert overlap(door,g.shell) < 1e-5, ("door / shell", angle)
    assert door.distance(g.shell)>=g.FIT-0.01, ("door frame nominal gap",angle)
    assert overlap(door,g.left_jamb_return) < 1e-5, ("door / left jamb", angle)
    assert overlap(door,g.right_jamb_return) < 1e-5, ("door / right jamb", angle)
    assert overlap(door,servo) < 1e-5, ("door / servo", angle)
    for label, shape in {
        "LED orange": orange, "LED blanche": white,
        "support LED orange": g.orange_holder,
        "support LED blanche": g.holder,
    }.items():
        assert overlap(door, shape) < 1e-5, ("collision porte", angle, label)
print("PASS — V6 interfaces mecanique en CAO: porte/retours/berceau/LED/PCB, 11 STEP, 8 STL ; horn non mesure")
