#!/usr/bin/env python3
"""Régression CAO : BREP source, 9 STEP, 9 STL et assemblage V9.

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
assert manifest["design"]["shell_mm"][0] == g.W == bom["cad"]["shell_width_mm"] == 105.6
assert math.isclose(g.DOOR_W,55.0,abs_tol=1e-8)
assert math.isclose(g.OPEN_W,55.6,abs_tol=1e-8)
assert math.isclose(g.W, g.LEFT_PIER_W + g.OPEN_W + g.RIGHT_PIER_W, abs_tol=1e-8)
assert g.W==105.6 and bom["cad"]["printed_door_exact_width_mm"] == 55.0
assert manifest["design"]["door_opening_mm"][0] == g.OPEN_W == bom["cad"]["door_opening_mm"][0] == 55.6
assert g.WALL >= 2 and g.ROOF >= 2 and g.BASE >= 2 and g.FIT == 0.3
assert g.LED_ENVELOPE == (6.0, 9.0)
assert len(g.PRINTABLE) == 9
assert "10_boite_aux_lettres_noire" in g.PRINTABLE
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
assert math.isclose(bom["cad"]["attic_ceiling_width_mm"], g.ATTIC_W, abs_tol=1e-8)
assert math.isclose(g.ATTIC_W,100.2,abs_tol=1e-8)
assert g.ATTIC_PLATE_THICK == g.WALL == 2.4
assert "07_faux_plafond_combles_XIAO" in g.PRINTABLE
assert g.LEFT_PIER_W == g.OPEN_X == 11.0
assert g.RIGHT_PIER_W == 39.0
assert g.door_x1 < g.right_jamb_return.BoundingBox().xmin
# V9 user photo: roof standing seams on upper face; shallow glued black
# mailbox in the white FRONT right pier; no change below the roof.
assert g.ROOF_RIB_COUNT == 9
assert len(g.roof_front_fascia_seams) == 9
assert g.ROOF_FASCIA_RIB_PROJECTION == 0.85
assert g.ROOF_FASCIA_RIB_BOTTOM_Z > g.H_FRONT-g.ROOF-g.ROOF_SKIRT_DROP-1.0
assert g.ROOF_FASCIA_RIB_TOP_Z > g.H_FRONT-1.0
assert manifest["design"]["roof_front_fascia_standing_seams_count"] == 9
assert manifest["design"]["roof_front_fascia_seams_continuous_with_top"] is True
assert bom["cad"]["roof_front_fascia_bac_acier_rib_count"] == 9
assert all(seam.isValid() and len(seam.Solids())==1
           for seam in g.roof_front_fascia_seams)
assert len(g.ROOF_RIB_XS) == len(g.roof_standing_seams) == 9
assert math.isclose(g.ROOF_RIB_PITCH, 11.5)
assert math.isclose(g.ROOF_RIB_RISE, 0.95)
assert math.isclose(g.ROOF_RIB_BASE_W, 2.5)
assert math.isclose(g.ROOF_RIB_CROWN_W, 1.1)
assert all(math.isclose(b-a,g.ROOF_RIB_PITCH,abs_tol=1e-8)
           for a,b in zip(g.ROOF_RIB_XS,g.ROOF_RIB_XS[1:]))
assert g.ROOF_RIB_XS[0]-g.ROOF_RIB_BASE_W/2 > -g.ROOF_OVERHANG
assert g.ROOF_RIB_XS[-1]+g.ROOF_RIB_BASE_W/2 < g.W+g.ROOF_OVERHANG
assert g.ROOF_RIB_Y0 >= -g.ROOF_OVERHANG
assert g.ROOF_RIB_Y1 <= g.D+g.ROOF_OVERHANG
assert all(rib.isValid() and len(rib.Solids())==1
           for rib in g.roof_standing_seams)
assert g.MAILBOX_POCKET_X0 > g.OPEN_X+g.OPEN_W+5
assert g.MAILBOX_POCKET_X0+g.MAILBOX_POCKET_W < g.W-4
assert g.MAILBOX_POCKET_Z0 >= g.BASE+g.MAILBOX_POCKET_H
assert g.MAILBOX_POCKET_Z0+g.MAILBOX_POCKET_H < g.OPEN_Z+g.OPEN_H
assert math.isclose(g.WALL-g.MAILBOX_POCKET_DEPTH,1.35,abs_tol=1e-8)
assert math.isclose((g.MAILBOX_POCKET_W-g.MAILBOX_INSERT_W)/2,g.FIT,abs_tol=1e-8)
assert math.isclose((g.MAILBOX_POCKET_H-g.MAILBOX_INSERT_H)/2,g.FIT,abs_tol=1e-8)
assert g.MAILBOX_FACE_RELIEF_Y+g.MAILBOX_INSERT_THICK < g.MAILBOX_POCKET_DEPTH
assert g.mailbox_insert.isValid() and len(g.mailbox_insert.Solids())==1
assert bom["cad"]["roof_bac_acier_rib_count"] == manifest["design"]["roof_bac_acier_rib_count"] == 9
assert bom["cad"]["mailbox_separate_black_part"] is True
assert bom["cad"]["mailbox_pocket_width_height_depth_mm"] == [7.6,7.6,1.05]
assert bom["cad"]["mailbox_insert_width_height_thickness_mm"] == [7,7,0.75]
assert bom["cad"]["mailbox_insert_linear_reduction_from_v9_percent"] == 30
assert math.isclose(g.MAILBOX_INSERT_W / 10.0, 0.7, abs_tol=1e-8)
assert math.isclose(g.MAILBOX_INSERT_H / 10.0, 0.7, abs_tol=1e-8)
assert math.isclose(g.MAILBOX_POCKET_X0+g.MAILBOX_POCKET_W/2,80.1,abs_tol=1e-8)
assert math.isclose(g.MAILBOX_INSERT_X0 - (g.OPEN_X+g.OPEN_W),
                    10.0,abs_tol=1e-8)
assert bom["cad"]["mailbox_opening_to_black_left_gap_mm"] == 10.0
assert manifest["design"]["mailbox_visible_gap_to_opening_mm"] == 10.0
assert math.isclose(g.MAILBOX_POCKET_Z0+g.MAILBOX_POCKET_H/2,29.3,abs_tol=1e-8)
assert manifest["design"]["mailbox_insert_separate_stl"] is True
assert g.bearing_width == 4.6
assert g.bearing_depth == 12.0 and g.bearing_height == 12.0
assert bom["cad"]["compact_left_bearing_width_mm"] == 4.6
assert bom["cad"]["compact_left_bearing_depth_mm"] == 12
assert bom["cad"]["compact_left_bearing_height_mm"] == 12
assert math.isclose(g.BEARING_SEAT_Z,g.PIVOT_Z-6,abs_tol=1e-8)
assert bom["cad"]["left_pier_width_mm"] == 11
assert bom["cad"]["right_pier_width_mm"] == 39
assert bom["cad"]["door_offset_from_center_mm"] == -14.0
# USB-C 49067 manufacturer published outer envelope is NOT a connector STEP.
# Carrier is part of the black base, so printable count stays eight.
assert g.USB_C_BOARD_VENDOR_LWH_MM == (21.0,15.0,4.5)
assert g.USB_C_REAR_APERTURE_WH == (10.0,4.2)
assert g.USB_C_REAR_APERTURE_Z0 == 9.45
assert bom["cad"]["usb_c_port_only_reduced_aperture_provisional"] is True
assert manifest["design"]["usb_c_port_only_provisional_cut"] is True
# The 49067 vendor does not supply the actual nose offset; this is deliberately
# a tiny hole to adjust once a real breakout and mating plug are received.
assert manifest["design"]["usb_c_socket_position_known"] is False
assert g.CABLE_RISER_X0 > g.USB_C_CARRIER_X0+g.USB_C_CARRIER_W
assert g.CABLE_RISER_HEIGHT == 29
assert len(g.cable_riser_lips) == 3
assert manifest["design"]["upper_rear_attic_external_hole_removed"] is True
assert bom["cad"]["attic_rear_upper_wall_cutout_removed"] is True
assert g.USB_C_CARRIER_TOP_Z == 9.0
assert g.USB_C_STRAP_TUNNEL_YS == (79.0,89.5)
assert g.USB_C_STRAP_TUNNEL_W == 3.2
assert g.USB_C_BOARD_ORIENTATION_STATUS.startswith("provisional")
assert bom["cad"]["usb_c_breakout_published_lwh_mm"] == [21,15,4.5]
assert manifest["design"]["usb_c_carrier_integral_base"] is True
assert manifest["design"]["usb_c_socket_position_known"] is False
assert bom["cad"]["usb_c_49067_socket_face_position_confirmed"] is False
assert bom["cad"]["usb_c_49067_CC_populated_confirmed"] is None
assert "USB_C_BREAKOUT" in {p["id"] for p in bom["components"]}

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

# The published 49067 envelope rests ABOVE the integrated base without
# forcing the actual connector, which is not located on the published drawing.
usb_reference = g.REFERENCES["REF_USB_C_49067_GABARIT_NON_CONTRACTUEL_NE_PAS_IMPRIMER"]
assert len(usb_reference.Solids()) == 1
usb_bb = usb_reference.BoundingBox()
assert math.isclose(usb_bb.xlen,15,abs_tol=1e-8)
assert math.isclose(usb_bb.ylen,21,abs_tol=1e-8)
assert math.isclose(usb_bb.zlen,4.5,abs_tol=1e-8)
assert math.isclose(usb_bb.zmin-g.USB_C_CARRIER_TOP_Z,g.FIT,abs_tol=1e-8)
assert overlap(g.base_plate,usb_reference) < 1e-5, "USB board proxy / carrier"
assert overlap(g.shell,usb_reference) < 1e-5, "USB board proxy / shell"
assert overlap(g.roof_lid,usb_reference) < 1e-5
assert overlap(g.door,usb_reference) < 1e-5
assert g.USB_C_CARRIER_Y0+g.USB_C_CARRIER_D <= g.D-g.WALL-g.FIT, "USB carrier crosses rear wall"
# Two real channels to pass nylon ties UNDER the board; do not drill the PCB.
assert len(g.usb_c_strap_tunnels)==2
for passage in g.usb_c_strap_tunnels:
    assert overlap(g.base_plate,passage)<1e-5, "USB cable tie tunnel occluded"
    assert passage.BoundingBox().xlen > g.USB_C_CARRIER_W
    assert math.isclose(passage.BoundingBox().ylen, g.USB_C_STRAP_TUNNEL_W, abs_tol=1e-8)
    assert g.USB_C_CARRIER_TOP_Z-(g.USB_C_STRAP_TUNNEL_Z0+g.USB_C_STRAP_TUNNEL_H) >= 2.0-1e-8
# Rear USB-C cutout replaces ONLY the previous low rear opening.
usb_service=cq.Workplane("XY").box(g.USB_C_REAR_APERTURE_WH[0],
    g.WALL+0.20,g.USB_C_REAR_APERTURE_WH[1],centered=(False,False,False)).translate((
        g.W/2-g.USB_C_REAR_APERTURE_WH[0]/2,
        g.D-g.WALL-0.05,g.USB_C_REAR_APERTURE_Z0)).val()
assert overlap(g.shell,usb_service)<1e-5, "rear USB opening obstructed"
old_slot_lower=cq.Workplane("XY").box(1.0,0.4,0.8,
    centered=(False,False,False)).translate((g.W/2,98.2,6.0)).val()
assert overlap(g.shell,old_slot_lower)>0.1, "obsolete lower power slit still open"
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
# The dimensioned manufacturer datum from base to UNDER the mounting ear.
# Garage X runs from shaft tip toward base: 30 - 16 = 14 mm.
# Apply the 0.30mm printer clearance only, not the three estimated offsets.
assert g.SERVO_LUG_UNDERSIDE_FROM_BASE == 16.0
assert g.SERVO_OFFICIAL_ORIENTED_XYZ[0] == 30.0
assert math.isclose(g.SERVO_MANUFACTURER_BASE_X - g.SERVO_LUG_UNDERSIDE_DATUM_X,
                    16.0, abs_tol=1e-8)
assert math.isclose(g.SERVO_LUG_UNDERSIDE_DATUM_X - g.SERVO_SHAFT_TIP_X,
                    14.0, abs_tol=1e-8)
assert math.isclose(g.spine_x - g.SERVO_LUG_UNDERSIDE_DATUM_X,
                    g.FIT, abs_tol=1e-8)
assert math.isclose(g.spine_x - g.SERVO_SHAFT_TIP_X, 14.3, abs_tol=1e-8)
assert (g.SERVO_LUG_THICKNESS_EST_MM,
        g.SERVO_LUG_TOP_TO_CASE_TOP_EST_MM,
        g.SERVO_LUG_TOP_TO_SHAFT_BOSS_TOP_EST_MM) == (2.5,4.0,8.0)
assert g.SERVO_HORN_MOUNTED_THICKNESS_MM is None
assert g.SERVO_MOUNT_SCREW_HEAD_D_MM is None
assert g.SERVO_MOUNT_SCREW_UNDER_HEAD_LENGTH_MM is None
assert manifest["design"]["servo_mount_visual_estimates_drive_geometry"] is False
assert bom["cad"]["servo_lug_underside_from_base_confirmed_mm"] == 16.0
assert bom["cad"]["servo_lug_mount_axial_clearance_mm"] == g.FIT
assert bom["cad"]["servo_mount_screw_head_diameter_mm"] is None
assert bom["cad"]["servo_mount_screw_under_head_length_mm"] is None
assert bom["cad"]["servo_horn_mounted_face_to_outer_face_mm"] is None
assert (g.SERVO_LUG_BOSS_D - g.SERVO_LUG_PILOT_D)/2 >= 2.0, "lug pilot boss wall too thin"
assert len(g.SERVO_LUG_CENTERS_YZ) == 2
assert len(g.SERVO_LUG_CENTERS_Z) == 2
assert math.isclose(g.SERVO_LUG_CENTERS_Z[1] - g.SERVO_LUG_CENTERS_Z[0], 29, abs_tol=1e-6)
assert [*g.SERVO_OFFICIAL_ORIENTED_XYZ] == bom["cad"]["servo_official_oriented_xyz_mm"]
assert [*g.SERVO_VENDOR_ORIENTED_XYZ] == bom["cad"]["servo_vendor_step_oriented_xyz_mm"]
assert bom["cad"]["servo_lug_screw_count"] == manifest["design"]["servo_ear_mount_count"] == 2
assert bom["cad"]["servo_base_mount_count"] == 4
assert len(g.wire_eyes)==0, "old four lower wire rings still present"
assert bom["cad"]["cable_eyes_qty"] == manifest["design"]["cable_eye_qty"] == 0
assert len(g.servo_cable_clips)==4
assert len(g.SERVO_CABLE_CLIP_YZ)==4
assert (g.SERVO_CABLE_CLIP_OUTER_D-g.SERVO_CABLE_CLIP_INNER_D)/2>=2.0
assert g.SERVO_CABLE_CLIP_ENTRY_GAP_Z==2.2
assert bom["cad"]["servo_cable_clip_count"] == manifest["design"]["servo_cable_clips_count"] == 4
for (cy,cz),clip in zip(g.SERVO_CABLE_CLIP_YZ,g.servo_cable_clips):
    assert clip.isValid() and len(clip.Solids())==1
    assert not g.shell.isInside(cq.Vector(g.SERVO_CABLE_CLIP_X,cy,cz),1e-5), "clip bore blocked"
    assert g.shell.isInside(cq.Vector(g.SERVO_CABLE_CLIP_X,cy,cz+2.7),1e-5), "clip not fused to shell"
    assert not g.shell.isInside(cq.Vector(g.SERVO_CABLE_CLIP_X-3.0,cy,cz),1e-5), "clip entry closed"
    assert overlap(clip,g.cradle) < 1e-5
    assert overlap(clip,g.tray) < 1e-5
for x_old in (g.WALL+3.0,g.W-g.WALL-3.0):
    for y_old in (35.0,73.0):
        assert not g.shell.isInside(cq.Vector(x_old,y_old,12.0),1e-5), "old eyelet not removed"
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
assert g.SERVO_CABLE_CLIP_X<g.W-g.WALL
assert math.isclose(g.SERVO_CABLE_CLIP_X,g.W-g.WALL-2.1,abs_tol=1e-8)
assert g.DRIVE_DISC_R==6
assert math.isclose(g.DRIVE_JAMB_BORE_D-2*g.DRIVE_DISC_R,2*g.FIT)
assert math.isclose(g.DRIVE_DISC_END_X,67.1)
assert bom["cad"]["door_drive_disc_axial_bounds_mm"]==[63.6,67.1]
assert math.isclose(g.SERVO_SHAFT_TIP_X-g.DRIVE_DISC_END_X,2.2)
assert g.door.distance(g.shell)>=g.FIT-0.01
assert g.bearing.distance(g.shell)<0.01 # bearing rests on integral shelf
assert g.cradle.distance(g.base_plate)<0.01 # M2 feet rest on 3mm base
assert overlap(g.usb_c_carrier,g.cradle)<1e-5
# The closest extents of both mounting bosses have a nominal 0.30mm
# relief to the manufacturer 16.00mm ear datum in the garage X frame.
# Actual production case, fastening and horn are still not measured.
assert g.spine_x >= g.SERVO_LUG_UNDERSIDE_DATUM_X + g.FIT - 1e-8
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
assert math.isclose(g.ATTIC_LED_X,g.W/2,abs_tol=1e-8)
assert g.PCB_STRAP_SLOTS == [(g.W/2-18.2,77.0),(g.W/2+14.7,77.0)]
assert g.PCB_PADS == [(g.W/2-11.0,70.5),(g.W/2+6.0,70.5),
                       (g.W/2-11.0,84.0),(g.W/2+6.0,84.0)]
assert bom["cad"]["pcb_strap_slot_positions_xy_mm"] == [[34.6,77],[67.5,77]]
assert bom["cad"]["pcb_support_pads_xy_mm"] == [[41.8,70.5],[58.8,70.5],[41.8,84],[58.8,84]]
assert g.orange_x == g.OPEN_X+g.OPEN_W-15.0
assert math.isclose(g.orange_z,52.8,abs_tol=1e-8)
assert bom["cad"]["orange_led_center_z_mm"] == manifest["design"]["led_orange_center_xz_mm"][1] == 52.8
assert math.isclose(53.3-g.orange_z,0.5,abs_tol=1e-8)
servo = next(s for n, s in g.REFERENCES.items() if "MG90" in n)
assert overlap(g.usb_c_carrier,servo)<1e-5, "USB rear carrier vs servo"
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
# Mailbox insert occupies its local shallow cut without embedding in shell.
assert overlap(g.mailbox_insert, g.shell)<1e-5
assert g.mailbox_insert.distance(g.shell)<g.FIT+0.03
assert overlap(g.mailbox_insert, g.door)<1e-5
assert overlap(g.mailbox_insert, g.cradle)<1e-5
assert overlap(g.mailbox_insert, g.roof_lid)<1e-5
for xc in g.ROOF_RIB_XS:
    probe=cq.Vector(xc,45.0,g.H_FRONT+(g.H_BACK-g.H_FRONT)*0.45+0.4)
    assert g.roof_lid.isInside(probe,1e-5), ("raised steel rib missing",xc)
    # Second V10 corrugation segment is perpendicular to the roof sheet
    # and sits down on the visible FRONT FASCIA, same 11.5mm pitch.
    fold=cq.Vector(xc,-g.ROOF_OVERHANG-0.40,58.0)
    assert g.roof_lid.isInside(fold,1e-5), ("front fascia standing seam missing",xc)
# Old 16x9 rear wall service slot is physically filled again.
rear_top=cq.Vector(g.W/2,g.D-g.WALL/2,g.ATTIC_Z0+8)
assert g.shell.isInside(rear_top,1e-5), "upper rear wall cutout still present"
# Open internal U-channel lies close to rear wall but has continuous air
# at its centre and does NOT break the outside wall at any height.
assert math.isclose(g.CABLE_RISER_Y0,93.6,abs_tol=1e-8)
assert math.isclose(g.CABLE_RISER_Z0+g.CABLE_RISER_HEIGHT,43,abs_tol=1e-8)
for z in (15.0,23.0,35.0,42.0):
    air=cq.Vector(g.CABLE_RISER_X0+g.CABLE_RISER_RAIL_W+
                  g.CABLE_RISER_INNER_W/2,95.5,z)
    assert not g.shell.isInside(air,1e-5), ("cable chase blocked",z)
    back=cq.Vector(95.0,g.D-g.WALL/2,z)
    assert g.shell.isInside(back,1e-5), ("rear external wall perforated",z)
assert overlap(g.tray,g.cable_riser_left)<1e-5
assert overlap(g.tray,g.cable_riser_right)<1e-5
assert overlap(g.usb_c_carrier,g.cable_riser_left)<1e-5
assert overlap(g.usb_c_carrier,g.cable_riser_right)<1e-5
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
    assert overlap(door,g.usb_c_carrier) < 1e-5, ("door / rear USB-C carrier",angle)
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
print("PASS — V11: shell 105.6mm, door 55mm, 10mm black mailbox gap, 9 roof ribs, reduced bearing, 4 servo cable clips, 0 bottom eyes, 12 STEP/9 STL")
