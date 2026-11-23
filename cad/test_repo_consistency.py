#!/usr/bin/env python3
"""V14: cross-check firmware, CAD, BOM, user white LED drawing and current README.

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
assert b["cad"]["shell_width_mm"] == m["design"]["shell_mm"][0] == 105.6
assert b["cad"]["printed_door_exact_width_mm"] == m["design"]["door_panel_mm"][0] == 55.0
assert b["cad"]["servo_cable_clip_count"] == m["design"]["servo_cable_clips_count"] == 4
assert b["cad"]["cable_eyes_qty"] == m["design"]["cable_eye_qty"] == 0
assert b["cad"]["compact_left_bearing_width_mm"] == m["design"]["compact_left_bearing_width_mm"] == 4.6
assert b["cad"]["roof_bac_acier_rib_count"] == m["design"]["roof_bac_acier_rib_count"] == 9
assert b["cad"]["roof_front_fascia_bac_acier_rib_count"] == m["design"]["roof_front_fascia_standing_seams_count"] == 9
assert b["cad"]["mailbox_opening_to_black_left_gap_mm"] == m["design"]["mailbox_visible_gap_to_opening_mm"] == 10.0
assert b["cad"]["shell_depth_mm"] == m["design"]["shell_mm"][1] == 85
assert b["cad"]["attic_ceiling_depth_mm"] == m["design"]["attic_false_ceiling_mm"][1] == 25
assert b["cad"]["service_tray_mm"] == [100.2,25]
assert b["cad"]["garage_depth_reduction_from_v11_mm"] == 15.0
assert b["cad"]["usb_c_board_nominal_xyz_min_mm"] == m["design"]["usb_c_reference_board_nominal_xyz_min_mm"] == [45.3,59.4,9.3]
assert b["cad"]["usb_c_carrier_nominal_xyz_min_mm"] == m["design"]["usb_c_carrier_min_xyz_mm"] == [41.7,57.4,3]
assert b["cad"]["usb_c_strap_tunnel_ys_mm"] == m["design"]["usb_c_carrier_strap_tunnel_ys_mm"] == [64,74.5]
assert b["cad"]["internal_cable_riser_x0_y0_z0_mm"] == m["design"]["cable_riser_wall_position_xyz_mm"] == [90,78.6,14]
assert [b["cad"]["front_height_mm"],b["cad"]["back_height_mm"]] == m["design"]["roof_z_front_back_mm"] == [62,78]
assert b["cad"]["door_opening_mm"] == [55.6,42]
assert b["cad"]["door_panel_mm"] == [55,41.4,2.4]
assert b["cad"]["fit_per_face_mm"] == 0.3
assert b["cad"]["wall_mm"] >= 2.0
assert b["cad"]["orange_led_center_x_mm"] == m["design"]["led_orange_center_xz_mm"][0] == 5.3
assert b["cad"]["attic_internal_light_holder_xy_mm"] == m["design"]["attic_led_holder_xy_mm"] == [52.8,65]
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
assert b["cad"]["servo_dms_mg90_drawing_exact_ear_case_y_width_mm"] == m["design"]["servo_dms_mg90_drawing_exact_ear_case_width_mm"] == [33,23,12]
assert b["cad"]["servo_dms_mg90_drawing_output_axis_case_end_offset_mm"] == m["design"]["servo_dms_mg90_shaft_from_case_end_mm"] == 6
assert b["cad"]["servo_dms_mg90_drawing_output_axis_near_ear_end_offset_mm"] == m["design"]["servo_dms_mg90_shaft_from_near_ear_end_mm"] == 11
assert b["cad"]["servo_lug_centres_z_from_drawing_mm"] == m["design"]["servo_ear_centres_z_from_drawing_mm"] == [25.4,54.4]
assert b["cad"]["servo_pilot_entrance_d_depth_mm"] == m["design"]["servo_ear_pilot_leadin_d_depth_mm"] == [2.3,0.45]
assert b["cad"]["servo_spine_gussets_count"] == m["design"]["servo_rear_spine_gussets_count"] == 2
assert b["cad"]["servo_cable_exit_notch_upper_width_x_mm"] == m["design"]["servo_cable_exit_notch_x_width_mm"] == 5
assert b["cad"]["optional_print_calibration_coupons_count"] == m["design"]["calibration_coupons_count"] == 4
assert "D_DMS_MG90_oreilles_entraxe29" in (root/"cad/generate_fit_coupons.py").read_text()
assert b["cad"]["usb_c_breakout_vendor_code"] == m["design"]["usb_c_breakout_code"] == "Gotronic 49067"
# V9 photo-derived roof/letterbox geometry: no electrical or hardware change.
assert b["cad"]["roof_bac_acier_rib_count"] == m["design"]["roof_bac_acier_rib_count"] == 9
assert b["cad"]["roof_bac_acier_rib_pitch_mm"] == m["design"]["roof_bac_acier_rib_pitch_mm"] == 11.5
assert b["cad"]["roof_bac_acier_rib_rise_above_original_surface_mm"] == m["design"]["roof_bac_acier_rib_rise_mm"] == 0.95
assert b["cad"]["mailbox_pocket_width_height_depth_mm"] == m["design"]["mailbox_pocket_width_height_depth_mm"] == [7.6,7.6,1.05]
assert b["cad"]["mailbox_insert_width_height_thickness_mm"] == m["design"]["mailbox_insert_width_height_thickness_mm"] == [7,7,0.75]
assert b["cad"]["mailbox_insert_linear_reduction_from_v9_percent"] == m["design"]["mailbox_insert_reduction_linear_percent_vs_v9"] == 30
assert b["cad"]["roof_front_fascia_bac_acier_rib_count"] == m["design"]["roof_front_fascia_standing_seams_count"] == 9
assert b["cad"]["orange_led_center_z_mm"] == m["design"]["led_orange_center_xz_mm"][1] == 32.0
assert b["cad"]["orange_led_body_flange_d_mm"] == m["design"]["orange_led_drawing_body_flange_d_mm"] == [5,5.9]
assert b["cad"]["orange_led_body_total_length_mm"] == m["design"]["orange_led_drawing_front_to_flange_back_mm"] == 8.6
assert b["cad"]["orange_led_body_flange_socket_d_mm"] == m["design"]["orange_led_body_flange_bores_mm"] == [5.6,6.5]
assert b["cad"]["orange_led_lead_pitch_mm"] == m["design"]["orange_led_drawing_pins_pitch_mm"] == 2.54
assert b["cad"]["orange_led_mount_location"].startswith("front left white pier")
assert m["design"]["orange_led_at_bearing_left"] is True
assert b["cad"]["mailbox_separate_black_part"] is True
assert m["design"]["mailbox_insert_separate_stl"] is True
assert b["cad"]["mailbox_print_part"] == "10_boite_aux_lettres_noire"
assert b["cad"]["cad_printable_part_count"] == m["design"]["cad_printable_count"] == 10
assert b["cad"]["cad_step_export_count"] == m["design"]["cad_step_count"] == 13
assert b["cad"]["internal_cable_riser_lips_z_mm"] == []
assert b["cad"]["internal_cable_riser_lips_count"] == m["design"]["cable_riser_lip_count"] == 0
assert b["cad"]["internal_cable_riser_cap_part_name"] == m["design"]["cable_riser_cover_part_name"] == "11_couvercle_goulotte_arriere"
assert b["cad"]["internal_cable_riser_cover_nominal_xyz_mm"] == m["design"]["cable_riser_cover_nominal_xyz_mm"] == [7.9,1.1,27.8]
assert b["cad"]["internal_cable_riser_cover_fit_each_side_mm"] == m["design"]["cable_riser_cover_fit_per_edge_mm"] == 0.2
assert b["cad"]["pcb_side_clip_count"] == m["design"]["attic_wio_side_clip_count"] == 2
assert b["cad"]["pcb_side_clip_post_x_mm"] == m["design"]["attic_wio_side_clip_x_posts_mm"] == [38.45,63.75]
assert b["cad"]["white_led_drawing_body_flange_d_mm"] == m["design"]["white_led_drawing_body_flange_d_mm"] == [5,5.9]
assert b["cad"]["white_led_drawing_head_length_mm"] == m["design"]["white_led_drawing_head_length_mm"] == 8.6
assert b["cad"]["white_led_drawing_lead_length_nominal_tolerance_mm"] == m["design"]["white_led_drawing_lead_length_nominal_tolerance_mm"] == [29,0.5]
assert b["cad"]["white_led_lower_insertion_flange_cavity_d_mm"] == m["design"]["white_led_holder_bore_d_mm"] == 6.5
assert b["cad"]["white_led_upper_lead_exit_d_mm"] == m["design"]["white_led_lead_exit_hole_d_mm"] == 4.4
assert b["cad"]["white_led_retention_stop_z_mm"] == m["design"]["white_led_holder_stop_z_mm"] == 45.2
assert b["cad"]["white_led_source_match_actual_BOM_part_confirmed"] is False
assert m["design"]["white_led_drawing_not_guaranteed_same_as_WCS101"] is True
assert "bac acier" in read.lower() and "boîte aux lettres" in read.lower()
assert "docs/PROFONDEUR_LED_V12.md" not in read, "main README only current V14"
assert "docs/FIXATIONS_COMBLES_GOULOTTE_LED_V14.md" in read
assert (root/"docs/FIXATIONS_COMBLES_GOULOTTE_LED_V14.md").is_file()
assert (root/"docs/SERVO_DMS_MG90_PALONNIERS_V13.md").is_file()
assert (root/"docs/PROFONDEUR_LED_V12.md").is_file()
assert "4 clips" in read and "aucun œillet" in read.lower()
assert "2 clips" in read and "PETG" in read and "couvercle" in read
assert "10 mm" in read and "Ø5,9" in read
# Single-version README: no old version sections or old garage depth.
assert "V13" not in read and "V12" not in read and "V11" not in read and "V10" not in read and "V9" not in read
assert "105,6 × 100" not in read
assert "100 × 42" not in read
assert "10 STL" in cadread and "13 STEP" in cadread
assert b["cad"]["usb_c_breakout_published_lwh_mm"] == m["design"]["usb_c_breakout_vendor_lwh_mm"] == [21,15,4.5]
assert b["cad"]["usb_c_carrier_integrated_into"] == "02_socle_noir"
assert b["cad"]["usb_c_rear_aperture_wh_mm"] == m["design"]["usb_c_rear_slot_wh_mm"] == [10,4.2]
assert b["cad"]["usb_c_rear_aperture_z0_mm"] == m["design"]["usb_c_rear_slot_z0_mm"] == 9.45
assert b["cad"]["usb_c_port_only_reduced_aperture_provisional"] is True
assert m["design"]["usb_c_port_only_provisional_cut"] is True
assert b["cad"]["attic_rear_upper_wall_cutout_removed"] is True
assert m["design"]["upper_rear_attic_external_hole_removed"] is True
assert b["cad"]["internal_cable_riser_lips_z_mm"] == []
assert m["design"]["cable_riser_lip_count"] == 0
assert m["design"]["cable_riser_internal_rear_covered_straight_channel"] is True
assert "bandeau" in read.lower() and "goulotte" in read.lower()
assert "10 × 4,2" in read
assert "7 × 7" in read
assert b["cad"]["usb_c_49067_socket_face_position_confirmed"] is False
assert b["cad"]["usb_c_49067_CC_populated_confirmed"] is None
assert b["cad"]["usb_c_old_low_power_exit_replaced"] is True
assert "49067" in read and "5,1 kΩ" in read
assert "docs/ALIMENTATION_USB_C_V8.md" not in read, "README must only show current V14"
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
for marker in ("V14", "105,6 × 85", "55 mm", "62 / 78", "2,4", "0,30",
               "PETG", "GTG502WWC", "couvercle", "2 clips", "4 coupons",
               "goussets", "6 mm", "29 mm", "4 coupons",
               "Ø12", "Ø2,3", "Ø1,7", "0 à 90°", "LoRa", "25 × 2,4",
               "Ø5,9", "2,54", "29 ± 0,5", "49067", "SAS308"):
    assert marker in read, ("README missing",marker)
assert "V14" in cadread and "4 coupons" in cadread
assert "105,6 × 85" in cadread
assert "V13" not in cadread and "V12" not in cadread and "V11" not in cadread and "V10" not in cadread and "V9" not in cadread
assert "Ø3,2" in read and "Ø3,8" in read
# Old docs remain archived in the repo, but README must present only V13.
assert "docs/FIXATIONS_COMBLES_GOULOTTE_LED_V14.md" in cadread
assert (root/"docs/PROFONDEUR_LED_V12.md").is_file()
assert len(list((root/"cad/refs").glob("*.brep.z.b64"))) == 4
# Explicit non-certified assembly claims in canonical docs
for token in ("palonnier", "non", "tester"):
    assert token in read.lower()
assert "boîtier" in read.lower() and "SAS308" in read
print("PASS cross-check V14: PETG Wio side clips, straight slide-covered chase, user GTG502WWC LED, 10 STL/13 STEP, firmware")
