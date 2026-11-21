# Références de géométrie et licences

Quatre modèles STEP fournis par l'utilisateur (un servo MG90-A, une carte XIAO nRF52840, une carte Wio-SX1262 et un BC547B). Ce répertoire donne les noms, mesures et sommes SHA256. Pour les géométries complètes, copier les fichiers **dans `cad/refs/`** depuis le ZIP CAO V2 livré dans la conversation ou exécuter `cad/import_vendor_archives.py` sur les ZIP originaux. Des géométries de tiers sont maintenant versionnées en BREP; vérifier les droits/licences de redistribution des sources.

L'assemblage local STEP V2 contient ces modèles intégrés en solides de référence (NON imprimables). Le générateur peut être lancé sans ces références mais avertit qu'elles manquent, et l'assemblage exporté n'est alors pas complet.

**Bilan :** `servo` 33,4 × 32,5 × 12,22 mm hors tout dans le STEP ; `xiao` 22,482 × 4,46 × 17,78 ; `wio` 17,78 × 22,316 × 7,642 ; `BC547B` 4,08 × 3,05 × 12,8. Des mesures de lot réelles restent indispensables pour les vis, palonnier, connecteurs et antennes.
