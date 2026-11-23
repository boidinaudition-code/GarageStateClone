#!/usr/bin/env python3
"""Check four optional Bambu P1S calibration coupons separately from main STL."""
from pathlib import Path
import trimesh

dirpath=Path(__file__).resolve().parent/"coupons"
expected=[
"A_axe_D3p2_alesages_D3p6_D3p8_D4p0.stl",
"B_vis_M2_pilotes_D1p6_D1p7_D1p8.stl",
"C_gabarit_face_palonnier_D12_SANS_ENTRAXE_VALIDE.stl",
"D_DMS_MG90_oreilles_entraxe29_pilotes_D1p7.stl"
]
actual=sorted(p.name for p in dirpath.glob("*.stl"))
assert actual==sorted(expected),actual
for name in expected:
    p=dirpath/name
    mesh=trimesh.load_mesh(p)
    assert mesh.is_watertight and mesh.is_volume and mesh.volume>10,name
    print("PASS coupon",name,"volume",round(mesh.volume,1),"mm3")
