#!/usr/bin/env python3
"""Check manufacturer dimension traceability without claiming physical fit.

This test verifies documented sources and CAD warnings. It intentionally does
NOT assert that the current STL cradle fits the actual DMS-MG90 or antenna.
"""
import json
from pathlib import Path

base = Path(__file__).resolve().parent
catalog = json.loads((base / "component_dimensions_sources_v7.json").read_text(encoding="utf-8"))
bom = json.loads((base / "bom_dimensions_v1.json").read_text(encoding="utf-8"))
docs = (base.parent / "docs" / "FICHES_COTEES_COMPOSANTS_V7.md").read_text(encoding="utf-8")

assert catalog["units"] == bom["units"] == "mm"
parts = catalog["parts"]
identifiers = [p["id"] for p in parts]
assert len(identifiers) == len(set(identifiers))
assert len(parts) >= 19
statuses = set(catalog["status_codes"])
assert all(p["status"] in statuses for p in parts)
for part in parts:
    source = part.get("source")
    if part["status"] != "unknown":
        assert source and source.startswith("https://"), part["id"]
    elif source:
        assert source.startswith("https://")

by_id = {part["id"]: part for part in parts}
for item in bom["components"]:
    if item["id"] in ("S1", "M1", "C1", "Q1", "R1", "R2", "R3", "R4", "LED1", "LED2", "MCU", "RF_STACK", "ANT"):
        assert item["id"] in by_id

servo = by_id["M1"]
actual_drawing = servo["dimensions"]
assert servo["status"] == "manufacturer_drawing"
assert actual_drawing["overall_lug_length"] == 33
assert actual_drawing["overall_width"] == 12
assert actual_drawing["overall_height_excluding_horn"] == 30
assert actual_drawing["lug_centres_pitch"] == 29
assert actual_drawing["lug_open_notch_diameter"] == 2
assert servo["source"].lower().endswith(".pdf")
assert servo["dimensions"]["lug_centres_pitch"] == bom["components"][1]["manufacturer_drawing_mm"]["lug_center_pitch"]

design = catalog["critical_design"]
assert design["shell_lw"] == [bom["cad"]["shell_width_mm"], bom["cad"]["shell_depth_mm"]]
# Compare matching axes; old 0.05mm-per-end claim compared wrong axes.
assert design["servo_vendor_step_oriented_xyz"] == [32.5, 12.221, 33.4]
assert design["servo_official_oriented_xyz"] == [30, 12, 33]
assert all(a>b for a,b in zip(design["servo_vendor_step_oriented_xyz"], design["servo_official_oriented_xyz"]))
assert design["servo_ear_pitch_z"] == actual_drawing["lug_centres_pitch"] == bom["cad"]["servo_lug_pitch_mm"] == 29
assert design["servo_ear_notch_nominal_d"] == 2
assert design["servo_ear_3d_printed_pilot_d"] == 1.7
assert design["servo_mounting_screw_count"] == 2
assert design["servo_base_mounting_screw_count"] == 4
assert design["servo_ear_screw_axis"] == "X"
assert not bom["cad"]["servo_horn_physical_verified"]

assert by_id["LED1"]["dimensions"]["flange_diameter"] is None
assert by_id["LED2"]["dimensions"]["flange_diameter"] is None
assert "L7113EC" in by_id["LED2"]["notes"] and "L7113NC" in by_id["LED2"]["notes"]
assert by_id["S1"]["dimensions"]["magnet_lwh"] is None
assert by_id["ANT"]["dimensions"]["antenna_body"] is None
assert by_id["MCU"]["manufacturer_2d_dxf_archive"].endswith(".zip")
assert "non décodé" in docs
print(f"PASS: {len(parts)} composants catalogués, plans sourcés, dimensions absentes explicites.")
print("PITCH DMS-MG90: 2 encoches ouvertes Ø2, entraxe 29mm (Z du garage), pilotes Ø1.7mm suivant X")
print("Aucune validation physique de palonnier, vis fournies, antenne et passages USB.")
