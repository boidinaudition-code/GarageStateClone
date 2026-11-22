#!/usr/bin/env python3
"""Validate the purchase classification / core arithmetic against the V5 CAD BOM.

Tests facts that are represented in repository source; does NOT validate
unmeasured mounting hole sizes, actual stock, shipping or hardware assembly.
"""
from decimal import Decimal
import json
from pathlib import Path

root=Path(__file__).resolve().parent
p=json.loads((root/"hardware_bom_v5.json").read_text(encoding="utf-8"))
b=json.loads((root/"bom_dimensions_v1.json").read_text(encoding="utf-8"))
docs=(root.parent/"docs/BOM_V1_VERIFIEE.md").read_text(encoding="utf-8")
hard=(root.parent/"docs/QUINCAILLERIE_MONTAGE_V5.md").read_text(encoding="utf-8")
assert p["schema"]=="GarageStateClone-hardware-BOM-v5.1"
assert p["currency"]=="EUR"
core=p["core_electronics"]
assert len(core)==len({r["id"] for r in core})==10
total=sum((Decimal(x["pack_price_eur"]) for x in core),Decimal("0"))
assert total==Decimal(p["core_total_eur"])==Decimal("23.43"),total
assert "23,43 €" in docs and "3,90 €" in docs
assert "25,48" not in docs and "5,95" not in docs
assert b["system_state"]["sensor_count"]==1
assert {r["id"]:r["quantity_mounted"] for r in core}["SAS308"]==1
assert b["cad"]["shell_width_mm"]==150
assert b["cad"]["back_height_mm"]==78
assert b["cad"]["attic_ceiling_thickness_mm"]==2.4
assert b["cad"]["hinge_pin_diameter_mm"]==3.2
assert b["cad"]["hinge_bore_diameter_mm"]==3.8
assert b["cad"]["attic_min_xiao_clearance_to_roof_mm_approx"]<10
ids={x["id"] for x in p["hardware_candidates"]}
assert len(ids)==len(p["hardware_candidates"])
required={"TAP_2_2x6_5","M2x8","M2_NUTS","M2_WASHERS","CABLE_TIES_BLACK",
          "ADHESIVE_CLIPS","SERVO_JR_ADAPTER","SIGNAL_WIRE_BLACK","ADHESIVE_HEAT_SHRINK",
          "SENSOR_MAGNET_MOUNT","TRANSMITTER_HOUSING","XIAO_NONCONDUCTIVE_HOLDER","SERVO_DOOR_COUPLER"}
assert required.issubset(ids)
statuses=set(p["status_convention"])
for row in p["hardware_candidates"]:
    assert row["status"] in statuses
    if row["ref"]:
        assert row["url"] and row["url"].startswith("https://www.gotronic.fr/")
        assert Decimal(row["pack_price_eur"])>0
    else:
        assert row["status"]=="measure" and row["pack_price_eur"] is None
assert "boîtier émetteur" in hard
assert "3,90 €" in hard
assert "tourillon" in hard.lower()
servo=next(x for x in core if x["id"]=="DMS-MG90")
assert "servo fastening hardware" in servo["includes"]
assert "LEFT_HINGE_PIN" in {x["id"] for x in p["existing_not_rebuy"]}
assert next(x for x in p["hardware_candidates"] if x["id"]=="SERVO_DOOR_COUPLER")["status"]=="measure"
print(f"PASS BOM V5: {len(core)} articles electroniques = {total} EUR,"
      f" {len(p['hardware_candidates'])} lots/besoins montage classes,"
      " aucune dimension de vis finale pretendue validee")
