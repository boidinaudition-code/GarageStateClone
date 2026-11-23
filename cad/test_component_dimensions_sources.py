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
assert actual_drawing["lug_underside_height_from_base"] == 16.0
assert servo["visual_estimates_from_drawing_mm"]["lug_thickness"] == 2.5
assert servo["visual_estimates_from_drawing_mm"]["lug_top_to_flat_case_top"] == 4.0
assert servo["visual_estimates_from_drawing_mm"]["lug_top_to_shaft_boss_top_excluding_shaft"] == 8.0
assert all(v is None for v in servo["pending_physical_measurements_mm"].values())
assert actual_drawing["lug_open_notch_diameter"] == 2
assert actual_drawing["shaft_offset_from_near_case_end_in_lug_span"] == 6
assert actual_drawing["case_length_on_drawing"] == 23
assert actual_drawing["lug_span_with_open_notches"] == 33
assert actual_drawing["shaft_offset_from_near_lug_end_derived"] == 11
assert actual_drawing["shaft_feature_circular_diameters"] == [3,5]
assert actual_drawing["upper_shoulder_levels_from_base"] == [22.5,26.5,30]
assert actual_drawing["lug_notch_end_margin_each_side"] == 2
assert "2026-11-23" in servo["secondary_confirmed_source"]
assert "round" in servo["horn_photo_observation"]
assert bom["cad"]["servo_actual_horn_hole_pitch_measured_mm"] is None
assert bom["cad"]["servo_actual_horn_thickness_measured_mm"] is None
assert not bom["cad"]["servo_horn_physical_verified"]
assert servo["source"].lower().endswith(".pdf")
assert servo["dimensions"]["lug_centres_pitch"] == bom["components"][1]["manufacturer_drawing_mm"]["lug_center_pitch"]

design = catalog["critical_design"]
assert design["shell_lw"] == [bom["cad"]["shell_width_mm"], bom["cad"]["shell_depth_mm"]]
# Compare matching axes; old 0.05mm-per-end claim compared wrong axes.
assert design["servo_vendor_step_oriented_xyz"] == [32.5, 12.221, 33.4]
assert design["servo_official_oriented_xyz"] == [30, 12, 33]
assert all(a>b for a,b in zip(design["servo_vendor_step_oriented_xyz"], design["servo_official_oriented_xyz"]))
assert design["servo_ear_pitch_z"] == actual_drawing["lug_centres_pitch"] == bom["cad"]["servo_lug_pitch_mm"] == 29
assert design["servo_shaft_offset_from_case_end_mm"] == 6
assert design["servo_shaft_offset_from_near_ear_end_mm"] == 11
assert design["servo_ear_z_centres_mm"] == [25.4,54.4]
assert design["servo_cradle_gussets_count"] == 2
assert design["servo_mount_trial_coupons_count"] == 4
assert design["servo_ear_notch_nominal_d"] == 2
assert design["servo_ear_3d_printed_pilot_d"] == 1.7
assert design["servo_mounting_screw_count"] == 2
assert design["servo_base_mounting_screw_count"] == 4
assert design["servo_ear_screw_axis"] == "X"
assert design["servo_lug_underside_height_from_base_confirmed_mm"] == 16.0
assert design["servo_manufacturer_height_shaft_tip_from_base_mm"] == 30.0
assert design["servo_lug_underside_x_from_shaft_tip_nominal_mm"] == 30.0-16.0
assert abs(design["servo_lug_support_face_x_from_shaft_tip_nominal_mm"]-(30.0-16.0+0.30)) < 1e-8
assert design["servo_estimate_values_used_as_tight_fit"] is False
assert bom["cad"]["servo_lug_mount_axial_clearance_mm"] == 0.30
assert bom["cad"]["servo_mount_screw_head_diameter_mm"] is None
assert bom["cad"]["servo_mount_screw_under_head_length_mm"] is None
assert bom["cad"]["servo_horn_mounted_face_to_outer_face_mm"] is None
assert "16,00" in docs and "provisoire" in docs.lower()
assert not bom["cad"]["servo_horn_physical_verified"]

assert by_id["LED1"]["dimensions"]["flange_diameter"] is None, "white LED remains unmeasured"
orange = by_id["LED2"]
assert orange["dimensions"]["nominal_body_diameter"] == 5.0
assert orange["dimensions"]["flange_diameter"] == 5.9
assert orange["dimensions"]["body_length"] == 8.6
assert orange["dimensions"]["lead_pitch"] == 2.54
assert orange["dimensions"]["flange_thickness_max"] == 1.0
assert orange["dimensions"]["lead_length_min"] == 27.0
assert orange["dimensions"]["lead_square_width_nominal"] == 0.5
assert orange["dimensions"]["lead_square_width_tolerance"] == 0.05
assert orange["supplemental_drawing_source"].startswith("dimensioned engineering drawing supplied by user")
assert bom["cad"]["orange_led_body_flange_d_mm"] == [5.0,5.9]
assert bom["cad"]["orange_led_body_total_length_mm"] == 8.6
assert bom["cad"]["orange_led_body_flange_socket_d_mm"] == [5.6,6.5]
assert "27mm minimum" in orange["notes"]
assert by_id["LED1"]["dimensions"]["body_length"] is None
assert by_id["S1"]["dimensions"]["magnet_lwh"] is None
assert by_id["ANT"]["dimensions"]["antenna_body"] is None
assert by_id["MCU"]["manufacturer_2d_dxf_archive"].endswith(".zip")
assert "non décodé" in docs
usb=by_id["USB_C_BREAKOUT"]
assert usb["dimensions"]["overall_length"] == 21
assert usb["dimensions"]["overall_width"] == 15
assert usb["dimensions"]["overall_height"] == 4.5
assert usb["dimensions"]["exact_socket_position"] is None
assert usb["dimensions"]["mounting_hole_centres"] is None
assert usb["dimensions"]["cc1_cc2_rds_factory_fitted"] is None
assert bom["cad"]["usb_c_breakout_published_lwh_mm"] == [21,15,4.5]
assert by_id["SC02_254"]["dimensions"]["pin_pitch"] == 2.54
assert by_id["USB_C_CC_RDS"]["dimensions"]["resistance_ohms"] == 5100
assert "49067" in docs
print(f"PASS: {len(parts)} composants catalogués, plans sourcés, dimensions absentes explicites.")
print("PITCH DMS-MG90: 2 encoches ouvertes Ø2, entraxe 29mm (Z du garage), pilotes Ø1.7mm suivant X")
print("Aucune validation physique de palonnier, vis fournies, antenne et passages USB.")
