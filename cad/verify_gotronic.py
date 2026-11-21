#!/usr/bin/env python3
"""Run after generate_cad.py: python cad/verify_gotronic.py (CadQuery + trimesh).

Checks documentary consistency and sampled LED clearances, not hardware fit.
"""
import ast
import json
import re
import runpy
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

import trimesh

ROOT = Path(__file__).resolve().parent.parent
cad = runpy.run_path(str(ROOT / "cad/generate_cad.py"))
bom = json.loads((ROOT / "cad/bom_dimensions_v1.json").read_text())
components = {c["id"]: c for c in bom["components"]}
assert bom["system_state"]["sensor_count"] == 1
assert components["S1"]["qty"] == 1
for key, ref in (("LED1", "03989"), ("LED2", "03051")):
    led = components[key]
    assert led["manufacturer_ref"] == "Gotronic " + ref
    assert led["body_mm"] == {"diameter": 5, "length": None}
    assert led["lead_pitch_mm"] is None and led["collar_diameter_mm"] is None
assert bom["cad"]["led_pocket_provisional_diameter_mm"] == cad["LED_POCKET_D"]
assert bom["cad"]["orange_optical_aperture_mm"] == cad["LED_ORANGE_APERTURE_D"]
assert bom["cad"]["orange_led_recess_from_front_mm"] == cad["LED_ORANGE_RECESS"]
assert bom["cad"]["led_service_envelope_provisional_diameter_length_mm"] == list(cad["LED_ENVELOPE"])
print("JSON / generator: single sensor, 5mm LEDs, unknown dimensions, pockets consistent")

links = 0
for path in sorted(ROOT.rglob("*.md")):
    text = path.read_text()
    assert not re.search(r"rptronics\.fr|lextronic\.fr|304WC2J|LED3OLN", text), path
    for target in re.findall(r"\]\(([^\s)]+)\)", text):
        url = urlsplit(target)
        if url.scheme or not url.path:
            continue
        assert (path.parent / unquote(url.path)).exists(), (path, target)
        links += 1
for path in ROOT.glob("assets/**/*.svg"):
    ET.parse(path)
ast.parse((ROOT / "cad/generate_cad.py").read_text())
print(f"Local Markdown link paths: {links} OK; SVG XML and Python AST: OK")

stls = sorted((ROOT / "cad/stl").glob("*.stl"))
assert len(stls) == len(cad["PRINTABLE"]) == 9
for path in stls:
    mesh = trimesh.load_mesh(path)
    assert mesh.is_watertight and mesh.is_volume, path
    solid = cad["PRINTABLE"][path.stem]
    assert solid.isValid() and len(solid.Solids()) == 1, path
steps = sorted((ROOT / "cad/step").glob("*.step"))
assert len(steps) == 10
assert all(path.stat().st_size > 0 for path in steps)
print("9 STL watertight/positive volumes; 9 valid single solids; 10 STEP files present")

refs = {name: solid for name, solid in cad["REFERENCES"].items() if "LED_" in name}
assert len(refs) == 2
for name, solid in refs.items():
    assert "ENVELOPPE_PROVISOIRE" in name
    assert solid.intersect(cad["shell"]).Volume() < 1e-6, name
    assert solid.intersect(cad["servo_reference"]).Volume() < 1e-6, name
    assert solid.intersect(cad["holder"]).Volume() < 1e-6, name
white_ref = next(s for n, s in refs.items() if "blanche" in n)
assert white_ref.intersect(cad["roof_lid"]).Volume() < 1e-6
# White holder intentionally overlaps roof slightly for bonding.
assert cad["holder"].intersect(cad["roof_lid"]).Volume() > 0
orange_ref = next(s for n, s in refs.items() if "orange" in n)
assert orange_ref.BoundingBox().ymin > cad["WALL"]
for angle in range(0, 91, 5):
    door = cad["door"].rotate((0, cad["PIVOT_Y"], cad["PIVOT_Z"]),
                              (1, cad["PIVOT_Y"], cad["PIVOT_Z"]), angle)
    for name, solid in {**refs, "white_holder": cad["holder"],
                        "orange_holder": cad["orange_holder"]}.items():
        assert door.intersect(solid).Volume() < 1e-6, (angle, name)
print("LED envelopes fit reserved pockets, clear servo/roof; LED zones clear sampled door sweep 0..90 by 5 degrees")
print("PASS — numerical prototype checks only; no hardware, printing, radio or full assembly qualification")
