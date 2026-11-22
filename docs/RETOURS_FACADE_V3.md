# Historique V3 — retours intérieurs de façade et suppression du liseré bleu

> **ARCHIVE V3 (190 mm), remplacée par V6 compacte 150 mm avec toit 62/78 et nouveaux supports.** Plan actuel : [ASSEMBLAGE_V6.md](ASSEMBLAGE_V6.md).


> **Version historique (190 mm). La version actuelle est la [V4 compacte 150 mm](IMPLANTATION_COMPACTE_V4.md)** ; ces cotes sont conservées pour comprendre les changements, pas pour fabriquer la dernière version.

## Demande et aspect attendu

- Supprimer le jour visible entre les **murs extérieurs** et la **porte noire** sur le rendu Onshape.
- **Ramener les deux montants de l'ouverture vers l'intérieur**, au lieu de faire avancer la porte.
- **Retirer entièrement le bandeau bleu au-dessus de la porte**. Le garage reste blanc, avec toit noir mono-pente, porte noire rainurée et **petit voyant orange**.
- Conserver le volet monobloc pivotant vers l'intérieur, le servo à l'avant haut droit, les cartes à l'arrière, le toit amovible et les fils hors débattement.

## Géométrie paramétrique actuelle

| Paramètre | Valeur V3 |
|---|---:|
| Coque extérieure (L × P) | **190 × 100 mm** ; +6 mm en largeur par rapport à V2 |
| Toit mono-pente (avant / arrière) | **62 / 65 mm** |
| Baie de porte | **110 × 42 mm** |
| Porte imprimée | **109,4 × 41,4 × 2,4 mm** |
| Épaisseur des murs | **2,4 mm**, minimum demandé ≥2 mm |
| Deux retours verticaux latéraux | **10,0 mm vers l'intérieur** derrière la façade |
| Épaisseur de chaque retour | **2,4 mm** |
| Jeu latéral avec le panneau mobile | **0,30 mm de chaque côté** |
| Trou dans le retour gauche pour tourillon | **Ø3,8 mm** pour **tourillon Ø3,2 mm** |
| Palier gauche | Recul latéral **1,6 mm** pour libérer le retour |
| Entrefer porte ↔ axe de sortie servo | **3 mm**, provisoire, sans accouplement modélisé |
| Servo | Déplacé **1,5 mm latéralement** afin d'éviter le retour droit |
| Bandeau bleu | **Supprimé**, y compris des STEP/STL, assemblages et schéma lumineux |

Les retours sont **fusionnés à la coque** et commencent au dos de la paroi avant. Le retour gauche est échancré pour le passage du tourillon supérieur. Aucun retour au-dessus de la baie : la porte pivote sous le toit sans contrainte. Les pièces ne doivent **pas** être déplacées dans l'ouverture elle-même, sinon le panneau entrerait en collision pendant sa course.

### Pourquoi la coque s'élargit de 6 mm ?

Avec la V2 à **184 mm**, placer une joue de **2,4 mm** juste à droite de la baie traverserait la géométrie du servo MG90 (entre ses pattes et son arbre). La largeur V3 **190 mm**, en conservant la baie centrée de 110 mm, permet de décaler le servo de **1,5 mm** vers la droite. La face du nouveau retour arrive à **0,30 mm du début de l'enveloppe STEP** du servo. Un jeu de couplage de **3 mm** remplace l'ancien 1,5 mm ; il devra être occupé par une liaison mécanique dimensionnée après mesure du palonnier réel.

L'ancienne position du palier gauche croisait le retour gauche. Son décalage de **1,6 mm** et le trou Ø3,8 mm libèrent l'axe de la porte.

## Tests CAO et impression

Les tests `cad/test_step_exports.py` vérifient :
- **8 pièces imprimables** (au lieu de 9), sans `08_liseret_bleu` ;
- **11 STEP générés** (8 pièces + 1 assemblage + 2 STEP Onshape alternatifs), **8 STL** ;
- intégrité des 4 BREP source inchangés et réimportation des 8 STEP des pièces ;
- géométrie des joues, collision du servo avec la joue droite, collision du palier gauche et du support servo avec leurs joues respectives ;
- parcours de la porte de **0 à 90° par pas de 5°** sans intersection avec coque, joues ou servo ;
- épaisseurs minimales des murs et jeu paramétrique.

**Ces tests ne remplacent pas une impression/mesure physique.** Le servo fourni en STEP est un MG90-A, pas une garantie dimensionnelle pour le DMS-MG90 réellement acheté ; son support et son palonnier ne sont pas encore validés.

## Regénération et import dans Onshape

Les STEP/STL sont **des sorties générées**, non des fichiers à fusionner manuellement dans Git.

```sh
python cad/generate_cad.py
python cad/qa_geometry.py
python cad/verify_gotronic.py
python cad/test_step_exports.py
```

Pour Onshape, utiliser le nouveau fichier `GarageStateClone_V2_assemblage_STEP_references.step` depuis l'artefact GitHub Actions. Son nom de fichier reste V2 pour compatibilité avec les outils existants, mais sa **géométrie est V3**.

Si des modèles électroniques tiers déclenchent `contains faults`, importer `GarageStateClone_V2_STRUCTURE_SANS_REFERENCES_ONSHAPE.step`, qui ne contient que les **8 pièces imprimables** ; la référence simplifiée du XIAO reste disponible séparément.

**L'import précédent ne se met pas à jour automatiquement.** Il faut réimporter le STEP modifié ou remplacer les pièces dans le document Onshape.
