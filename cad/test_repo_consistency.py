#!/usr/bin/env python3
"""V6: cross-check firmware, CAD, BOM and canonical README.

This test checks repository claims and source constants, NOT actual hardware fit.
"""
import json
import re
from pathlib import Path
root=Path(__file__).resolve().parent.parent
s=(root/"cad/generate_cad.py").read_text(encoding="utf-8")
read=(root/"README.md").read_text(encoding="utf-8")
cadread=(root/"cad/README.md").read_text(encoding="utf-8")
platform=(root/"platformio.ini").read_text(encoding="utf-8")
firm=(root/"src/main.cpp").read_text(encoding="utf-8")
b=json.loads((root/"cad/bom_dimensions_v1.json").read_text(encoding="utf-8"))
m=json.loads((root/"cad/vendor_models/manifest.json").read_text(encoding="utf-8"))
hardware=json.loads((root/"cad/hardware_bom_v5.json").read_text(encoding="utf-8"))
assert b["cad"]["shell_width_mm"] == m["design"]["shell_mm"][0] == 150
assert b["cad"]["shell_depth_mm"] == 100
assert [b["cad"]["front_height_mm"],b["cad"]["back_height_mm"]] == m["design"]["roof_z_front_back_mm"] == [62,78]
assert b["cad"]["door_opening_mm"] == [100,42]
assert b["cad"]["door_panel_mm"] == [99.4,41.4,2.4]
assert b["cad"]["fit_per_face_mm"] == 0.3
assert b["cad"]["wall_mm"] >= 2.0
assert b["cad"]["orange_led_center_x_mm"] == m["design"]["led_orange_center_xz_mm"][0] == 96
assert b["cad"]["attic_internal_light_holder_xy_mm"] == m["design"]["attic_led_holder_xy_mm"] == [75,65]
assert b["cad"]["led_holder_pin_diameter_mm"] == 2
assert b["cad"]["led_holder_hole_diameter_mm"] == 2.6
assert b["cad"]["servo_base_mount_count"] == m["design"]["servo_mounting_pilot_count"] == 4
assert b["cad"]["servo_lug_pitch_mm"] == m["design"]["servo_ear_screws_pitch_z_mm"] == 29
assert b["cad"]["servo_lug_notch_nominal_d_mm"] == m["design"]["servo_ear_open_notches_d_mm"] == 2
assert b["cad"]["servo_lug_screw_count"] == m["design"]["servo_ear_mount_count"] == 2
assert b["cad"]["servo_lug_underside_from_base_confirmed_mm"] == m["design"]["servo_lug_underside_from_base_manufacturer_mm"] == 16.0
assert b["cad"]["servo_lug_support_face_from_shaft_tip_nominal_mm"] == m["design"]["servo_lug_printed_boss_face_x_from_shaft_tip_mm"] == 14.3
assert b["cad"]["servo_lug_mount_axial_clearance_mm"] == m["design"]["servo_lug_printed_boss_axial_fit_mm"] == 0.3
assert m["design"]["servo_mount_visual_estimates_drive_geometry"] is False
assert b["cad"]["servo_lug_boss_d_mm"] == 5.8
assert b["cad"]["usb_c_breakout_vendor_code"] == m["design"]["usb_c_breakout_code"] == "Gotronic 49067"
# V9 photo-derived roof/letterbox geometry: no electrical or hardware change.
assert b["cad"]["roof_bac_acier_rib_count"] == m["design"]["roof_bac_acier_rib_count"] == 13
assert b["cad"]["roof_bac_acier_rib_pitch_mm"] == m["design"]["roof_bac_acier_rib_pitch_mm"] == 11.5
assert b["cad"]["roof_bac_acier_rib_rise_above_original_surface_mm"] == m["design"]["roof_bac_acier_rib_rise_mm"] == 0.95
assert b["cad"]["mailbox_pocket_width_height_depth_mm"] == m["design"]["mailbox_pocket_width_height_depth_mm"] == [7.6,7.6,1.05]
assert b["cad"]["mailbox_insert_width_height_thickness_mm"] == m["design"]["mailbox_insert_width_height_thickness_mm"] == [7,7,0.75]
assert b["cad"]["mailbox_insert_linear_reduction_from_v9_percent"] == m["design"]["mailbox_insert_reduction_linear_percent_vs_v9"] == 30
assert b["cad"]["roof_front_fascia_bac_acier_rib_count"] == m["design"]["roof_front_fascia_standing_seams_count"] == 13
assert b["cad"]["orange_led_center_z_mm"] == m["design"]["led_orange_center_xz_mm"][1] == 52.1
assert b["cad"]["mailbox_separate_black_part"] is True
assert m["design"]["mailbox_insert_separate_stl"] is True
assert b["cad"]["mailbox_print_part"] == "10_boite_aux_lettres_noire"
assert b["cad"]["cad_printable_part_count"] == 9
assert b["cad"]["cad_step_export_count"] == 12
assert "bac acier" in read and "boîte aux lettres" in read
assert "docs/TOIT_BAC_ACIER_BOITE_LETTRES_V9.md" in read
assert (root/"docs/TOIT_BAC_ACIER_BOITE_LETTRES_V9.md").is_file()
assert "9 STL" in cadread and "12 STEP" in cadread
assert b["cad"]["usb_c_breakout_published_lwh_mm"] == m["design"]["usb_c_breakout_vendor_lwh_mm"] == [21,15,4.5]
assert b["cad"]["usb_c_carrier_integrated_into"] == "02_socle_noir"
assert b["cad"]["usb_c_rear_aperture_wh_mm"] == m["design"]["usb_c_rear_slot_wh_mm"] == [10,4.2]
assert b["cad"]["usb_c_rear_aperture_z0_mm"] == m["design"]["usb_c_rear_slot_z0_mm"] == 9.45
assert b["cad"]["usb_c_port_only_reduced_aperture_provisional"] is True
assert m["design"]["usb_c_port_only_provisional_cut"] is True
assert b["cad"]["attic_rear_upper_wall_cutout_removed"] is True
assert m["design"]["upper_rear_attic_external_hole_removed"] is True
assert b["cad"]["internal_cable_riser_lips_z_mm"] == [19,29,39]
assert m["design"]["cable_riser_lip_count"] == 3
assert "bandeau" in read.lower() and "goulotte" in read.lower()
assert "10 × 4,2" in read
assert "7 × 7" in read
assert b["cad"]["usb_c_49067_socket_face_position_confirmed"] is False
assert b["cad"]["usb_c_49067_CC_populated_confirmed"] is None
assert b["cad"]["usb_c_old_low_power_exit_replaced"] is True
assert "49067" in read and "5,1 kΩ" in read
assert "docs/ALIMENTATION_USB_C_V8.md" in read
assert (root/"docs/ALIMENTATION_USB_C_V8.md").is_file()
assert "USB-C" in (root/"docs/ALIMENTATION_USB_C_V8.md").read_text(encoding="utf-8")
assert b["cad"]["servo_mount_screw_head_diameter_mm"] is None
assert b["cad"]["servo_mount_screw_under_head_length_mm"] is None
assert b["cad"]["servo_official_oriented_xyz_mm"] == m["design"]["servo_official_oriented_xyz_mm"]
assert b["cad"]["servo_vendor_step_oriented_xyz_mm"] == m["design"]["servo_generic_step_oriented_xyz_mm"]
assert b["cad"]["servo_foot_pilot_hole_mm"] == 1.7
assert b["cad"]["servo_base_clearance_hole_mm"] == 2.3
assert b["cad"]["door_drive_disc_outer_diameter_mm"] == 12
assert b["cad"]["door_drive_disc_face_to_shaft_tip_gap_mm"] == 2.2
assert not m["design"]["horn_bolt_pattern_validated"]
assert hardware["core_total_eur"] == "23.43"
assert b["system_state"]["sensor_count"] == 1
assert "OPEN_SENSOR_PRESENT=0" in platform
assert "SINGLE_SENSOR_OPEN_ESTIMATE_MS=40000UL" in platform
assert "arduino-libraries/Servo" not in platform
assert "Servo.h" in firm and "#include <Servo.h>" in firm
assert "static constexpr uint8_t PIN_SERVO = D6" in firm
assert "static constexpr uint8_t PIN_INTERIOR_LED = D7" in firm
assert "static constexpr uint8_t PIN_AMBER_LED = D0" in firm
assert "ANGLE_CLOSED = 15" in firm and "ANGLE_OPEN = 95" in firm
for marker in ("V6", "150 × 100", "62 / 78", "2,4", "0,30",
               "23,43", "Ø12", "Ø2,3", "Ø1,7", "0–90", "LoRa"):
    assert marker in read, ("README missing",marker)
assert "V6" in cadread and "3 coupons" in cadread
assert "Ø3,2" in read and "Ø3,8" in read
assert "docs/ASSEMBLAGE_V6.md" in read and "docs/AUDIT_REPO_V6.md" in read
assert "BOM_V6.md" in read
for name in ("ASSEMBLAGE_V6.md","AUDIT_REPO_V6.md","BOM_V6.md"):
    assert (root/"docs"/name).is_file()
assert "V6" in (root/"docs/BOM_V6.md").read_text()
assert "V6" in (root/"docs/ASSEMBLAGE_V6.md").read_text()
assert len(list((root/"cad/refs").glob("*.brep.z.b64"))) == 4
# Explicit non-certified assembly claims in canonical docs
for token in ("palonnier", "non", "tester"):
    assert token in read.lower()
assert "boîtier" in read.lower() and "SAS308" in read
print("PASS cross-check V6: firmware roles/pins, CAD/BOM/LED positions, README, unknowns")
