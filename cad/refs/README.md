# Références géométriques exactes intégrées à GitHub

Les quatre fichiers **BREP compressés sans perte puis encodés en base64** sont désormais dans ce dossier :

| Fichier GitHub | Contenu |
|---|---|
| `servo.brep.z.b64` | Géométrie exacte de `Mg90.STEP`, pattes et axe inclus |
| `xiao.brep.z.b64` | Géométrie exacte du STEP `XIAO-nRF52840 v3` |
| `wio.brep.z.b64` | Géométrie exacte du STEP Wio-SX1262 pour XIAO V2 |
| `transistor.brep.z.b64` | Géométrie exacte du STEP BC547B |

Ces quatre fichiers ne sont **pas des STL** et ne sont pas à imprimer. `../generate_cad.py` effectue automatiquement `base64 → zlib → BREP → solide CadQuery`, sans dégradation géométrique. La reconstruction a été vérifiée en local : **4 solides de référence valides** avec les mêmes boîtes englobantes et le même nombre de solides que les STEP sources.

Les STEP d'origine sont également présents dans le **ZIP complet fourni dans la conversation**, pour import direct dans Onshape. Leur format peut contenir des noms/présentations supplémentaires que la BREP ne conserve pas ; le rendu géométrique reste identique.

**Attention licences** : ces modèles 3D ont été fournis par l'utilisateur mais leurs droits de redistribution publique ne sont pas documentés. Vérifier les conditions de réutilisation des fichiers tiers.

[Manifeste d'origine + SHA256](../vendor_models/manifest.json) · [Notice CAO V2](../README.md).
