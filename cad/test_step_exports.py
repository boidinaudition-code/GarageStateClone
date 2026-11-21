#!/usr/bin/env python3
"""Régression CAO : BREP source, 9 STEP, 9 STL et assemblage V2.

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
assert manifest["design"]["shell_mm"][0] == g.W == bom["cad"]["shell_width_mm"] == 184
assert manifest["design"]["door_opening_mm"][0] == g.OPEN_W == bom["cad"]["door_opening_mm"][0] == 110
assert g.WALL >= 2 and g.ROOF >= 2 and g.BASE >= 2 and g.FIT == 0.3
assert g.LED_ENVELOPE == (6.0, 9.0)
assert len(g.PRINTABLE) == 9

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
assert structure.isValid() and len(structure.Solids()) == 9
assert len(list((ROOT / "step").glob("*.step"))) == 12
assert len(list((ROOT / "stl").glob("*.stl"))) == 9

def overlap(a, b):
    aa, bb = a.BoundingBox(), b.BoundingBox()
    if (
        aa.xmax <= bb.xmin or aa.xmin >= bb.xmax or
        aa.ymax <= bb.ymin or aa.ymin >= bb.ymax or
        aa.zmax <= bb.zmin or aa.zmin >= bb.zmax
    ):
        return 0.0
    return a.intersect(b).Volume()

servo = next(s for n, s in g.REFERENCES.items() if "MG90" in n)
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
assert overlap(g.holder, g.roof_lid) > 0  # overlap de collage intentionnel
assert overlap(g.orange_holder, g.roof_lid) < 1e-5

# Porte rigide pivotant vers l'intérieur : échantillonnage 0...90°.
for angle in range(0, 91, 5):
    door = g.door.rotate(
        (0, g.PIVOT_Y, g.PIVOT_Z),
        (1, g.PIVOT_Y, g.PIVOT_Z),
        angle,
    )
    for label, shape in {
        "LED orange": orange, "LED blanche": white,
        "support LED orange": g.orange_holder,
        "support LED blanche": g.holder,
    }.items():
        assert overlap(door, shape) < 1e-5, ("collision porte", angle, label)
print("PASS — BREP intacts, 12 STEP (XIAO simplifie), 9 STL et debattement LED/servo verifies")
