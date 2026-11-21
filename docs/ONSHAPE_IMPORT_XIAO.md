# Onshape — erreur « REF_XIAO_NRF52840_STEP_NE_PAS_IMPRIMER contains faults »

## Origine probable

La référence XIAO nRF52840 d'origine provient d'un modèle 3D tiers avec **77 solides**, dont des détails électroniques extrêmement petits. Sa topologie est valide dans **CadQuery / OpenCascade**, mais Onshape utilise un autre validateur à l'import et peut afficher **« contains faults (Preview) »**.

**Ce diagnostic est probable, pas certain sans un nouvel import Onshape.** Les références détaillées originales n'ont pas été supprimées ni modifiées : `cad/refs/xiao.brep.z.b64` est toujours la source complète.

## Solution proposée

Le générateur exporte maintenant deux alternatives :

| Fichier généré | Contenu | Usage |
|---|---|---|
| `cad/step/REF_XIAO_NRF52840_SIMPLIFIE_POUR_ONSHAPE.step` | **Un solide analytique** reproduisant l'enveloppe de la carte + connecteur USB du STEP d'origine | Remplacer uniquement la pièce XIAO en erreur |
| `cad/step/GarageStateClone_V2_assemblage_STEP_references.step` | Garage V2 + servo + Wio + composants + **XIAO simplifié** | Réimporter l'ensemble avec cette correction |
| `cad/step/GarageStateClone_V2_STRUCTURE_SANS_REFERENCES_ONSHAPE.step` | **8 pièces imprimables uniquement**, aucune géométrie tierce | Alternative la plus simple si une autre référence pose problème |

**Attention :** la référence XIAO simplifiée conserve **exactement l'enveloppe hors-tout** de l'ancien fichier dans le même repère et le même emplacement de l'assemblage, mais ne reproduit **ni les pastilles, ni les trous de fixation, ni les connecteurs de carte à carte détaillés**. Ne pas utiliser les surfaces de cette référence pour usiner un support de précision. Les BREP originales restent dans `cad/refs/` pour les études géométriques détaillées.

## Dans Onshape

1. Télécharger l'artefact `garage-state-clone-cad-step-stl` dans l'onglet **Actions** du dépôt, ou générer les STEP localement.
2. Importer **le nouveau STEP simplifié du XIAO**, ou réimporter **l'assemblage actualisé** dans un *nouveau* document / nouveau Part Studio.
3. L'ancienne pièce marquée **contains faults** ne se répare pas automatiquement parce qu'un fichier GitHub a changé : supprimer/remplacer l'ancien import dans Onshape, ou mettre à jour le document d'import en pointant sur le nouveau STEP.
4. Si le nouvel assemblage affiche encore des erreurs provenant d'autres composants, importer **STRUCTURE_SANS_REFERENCES_ONSHAPE.step**. La coque, le toit, la porte et les autres pièces imprimables seront disponibles sans les modèles tiers ; importer ensuite seulement les références souhaitées.
5. Pour identifier précisément une pièce invalide : consulter la liste des pièces dans le Part Studio, l'indicateur rouge d'import et les commandes de réparation d'Onshape.

Onshape documente le réglage **Allow import of parts with faults** et ses outils de réparation des modèles importés : [Importing Files](https://cad.onshape.com/help/Content/Document/importing_files.htm), [Tech Tip: How to Repair Imported Models](https://www.onshape.com/en/resource-center/tech-tips/tech-tip-how-to-repair-imported-models-in-onshape).

## Validation automatisée

`python cad/generate_cad.py` crée désormais **11 STEP** (8 pièces, 1 assemblage détaillé simplifiant le XIAO, 1 structure sans références, 1 XIAO simplifié) et **8 STL**.

Le test `cad/test_step_exports.py` vérifie notamment que :
- les **4 BREP tierces** ont leurs empreintes SHA256 intactes ;
- le XIAO simplifié est un **unique solide avec une seule coque** ;
- les six bornes de sa boîte englobante concordent à **0,005 mm** près avec le modèle source ;
- le STEP du XIAO simplifié se **réimporte dans CadQuery** sans erreur ;
- le STEP structure seule contient exactement **9 solides** ;
- les 8 STEP de pièces restent valides et les 8 STL sont fermés.

**Cette validation est locale et sur GitHub Actions, pas une certification d'import par Onshape.**

## Pourquoi les STEP ne sont pas commités dans Git

Les STEP et STL sont des **exports générés** : modifier ou fusionner manuellement leur contenu, même si un outil affiche des lignes de texte STEP, peut les rendre incohérents. GitHub ne versionne donc que le générateur et les **BREP compressées originales**. Les STEP à jour sont dans les artefacts Actions (et peuvent être produits en local).

**Révision V3 :** les retours de tableau sont intégrés à la coque, la pièce de liseré bleu a été supprimée. Réimporter les nouveaux STEP depuis GitHub Actions pour voir les changements. La structure de secours contient désormais **8 pièces**. Voir [V3 — retours de façade](RETOURS_FACADE_V3.md).
