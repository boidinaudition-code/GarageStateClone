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
    assert led["body_mm"]["diameter"] == 5
white = components["LED1"]
orange = components["LED2"]
assert white["body_mm"]["length"] == cad["LED_WHITE_HEAD_LENGTH"] == 8.6
assert white["lead_pitch_mm"] == cad["LED_WHITE_LEAD_PITCH"] == 2.54
assert white["collar_diameter_mm"] == cad["LED_WHITE_FLANGE_D"] == 5.9
assert white["user_drawing_flange_thickness_max_mm"] == 1.0
assert white["user_drawing_lead_length_nominal_tolerance_mm"] == [29,0.5]
assert "GTG502WWC" in white["mechanical_dimensions_from"]
assert "not confirmed identical" in white["mechanical_dimensions_from"], "not verified identical to original BOM WCS101"
assert orange["body_mm"]["length"] == cad["LED_ORANGE_LENS_TO_FLANGE_BACK"] == 8.6
assert orange["lead_pitch_mm"] == cad["LED_ORANGE_PIN_PITCH"] == 2.54
assert orange["collar_diameter_mm"] == cad["LED_ORANGE_FLANGE_D"] == 5.9
assert orange["collar_thickness_max_mm"] == cad["LED_ORANGE_FLANGE_THICKNESS_MAX"] == 1.0
assert orange["leads_min_length_mm"] == cad["LED_ORANGE_LEAD_LENGTH_MIN"] == 27.0
assert "supplied in chat by user" in orange["drawing_source"]
assert orange["datasheet_warning"].startswith("Gotronic links L7113EC")
assert bom["cad"]["led_pocket_provisional_diameter_mm"] == cad["LED_POCKET_D"]
assert bom["cad"]["orange_optical_aperture_mm"] == cad["LED_ORANGE_APERTURE_D"]
assert bom["cad"]["orange_led_recess_from_front_mm"] == cad["LED_ORANGE_RECESS"]
assert bom["cad"]["led_service_envelope_provisional_diameter_length_mm"] == list(cad["LED_ENVELOPE"])
print("JSON / generator: white GTG502WWC dimensioned reference; Whadda WCS101 identity not confirmed; orange LED independent")

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
assert len(stls) == len(cad["PRINTABLE"]) == 13
for path in stls:
    mesh = trimesh.load_mesh(path)
    assert mesh.is_watertight and mesh.is_volume, path
    solid = cad["PRINTABLE"][path.stem]
    assert solid.isValid() and len(solid.Solids()) == 1, path
steps = sorted((ROOT / "cad/step").glob("*.step"))
assert len(steps) == 16
assert all(path.stat().st_size > 0 for path in steps)
print("13 STL watertight/positive volumes; 13 valid single solids; 16 STEP files present")

refs = {name: solid for name, solid in cad["REFERENCES"].items() if "LED_" in name}
assert len(refs) == 2
for name, solid in refs.items():
    if "blanche" in name:
        assert "GTG502WWC_COTEE" in name, "white dimensions must use user supplied PDF"
        assert cad["LED_WHITE_HEAD_LENGTH"] == 8.6
    else:
        assert "ENVELOPPE_COTEE" in name, "orange envelope follows supplied drawing"
    assert solid.intersect(cad["shell"]).Volume() < 1e-6, name
    assert solid.intersect(cad["servo_reference"]).Volume() < 1e-6, name
    assert solid.intersect(cad["holder"]).Volume() < 1e-6, name
white_ref = next(s for n, s in refs.items() if "blanche" in n)
assert white_ref.intersect(cad["roof_lid"]).Volume() < 1e-6
# V5: white LED socket bonds to the FALSE CEILING, not to removable roof.
assert cad["holder"].intersect(cad["roof_lid"]).Volume() < 1e-6
assert cad["holder"].intersect(cad["tray"]).Volume() < 1e-6
assert cad["holder"].distance(cad["tray"])<0.01  # dry-fit pegs rather than glue overlap
assert cad["H_BACK"] == 78.0 and cad["ATTIC_Z0"] == 46.0
for name in ("XIAO","WIO","BC547"):
    comp = next(v for k,v in cad["REFERENCES"].items() if name in k)
    assert comp.BoundingBox().zmin > cad["ATTIC_Z0"]+cad["ATTIC_PLATE_THICK"]
    assert comp.intersect(cad["tray"]).Volume() < 1e-6
    assert comp.intersect(cad["roof_lid"]).Volume() < 1e-6
assert cad["ATTIC_LED_Y"]==65.0
assert len(cad["SERVO_MOUNT_HOLES"])==4
assert len(cad["PCB_STRAP_SLOTS"])==2
assert len(cad["LED_HOLDER_PINS"])==2
assert len(cad["pcb_side_clips"]) == 2
assert cad["CABLE_RISER_COVER_W"] == 7.9
assert len(cad["cable_riser_lips"]) == 0
assert "11_couvercle_goulotte_arriere" in cad["PRINTABLE"]
print("V15 revised attic: V14 internals preserved; door and mailbox white stripe, intercom removed")
orange_ref = next(s for n, s in refs.items() if "orange" in n)
assert orange_ref.BoundingBox().ymin > cad["WALL"]
for angle in range(0, 91, 5):
    door = cad["door"].rotate((0, cad["PIVOT_Y"], cad["PIVOT_Z"]),
                              (1, cad["PIVOT_Y"], cad["PIVOT_Z"]), angle)
    for name, solid in {**refs, "white_holder": cad["holder"], "attic_ceiling": cad["tray"],
                        "orange_holder": cad["orange_holder"]}.items():
        assert door.intersect(solid).Volume() < 1e-6, (angle, name)
print("LED envelopes clear shell, servo and sampled door sweep 0..90 by 5 degrees")
print("PASS — numerical prototype checks only; no hardware, printing, radio or full assembly qualification")
