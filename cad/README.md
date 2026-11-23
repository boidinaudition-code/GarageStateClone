# CAO GarageStateClone — V14

**CAO paramétrique courante — 23/11/2026.** Développer via `cad/generate_cad.py`. Une version antérieure du dessin peut exister dans l'historique Git, mais les spécifications ci-dessous décrivent **uniquement V14**.

| Élément | Cote V14 |
|---|---|
| Coque | **105,6 × 85 mm**, murs 2,4 mm |
| Toit | **62 / 78 mm**, 9 nervures en pan et 9 en retombée, 3 mm d'épaisseur |
| Porte | 55 × 41,4 × 2,4 mm, ouverture 55,6 × 42 mm, jeu 0,30 mm par côté |
| Servo DMS-MG90 | Montant droit 39 mm, entraxe d'oreilles 29 mm, 2 pilotes Ø1,7 et 4 pieds indépendants, goussets |
| Palier | 4,6 × 12 × 12 mm, axe Ø3,2 et alésage Ø3,8 |
| Boîte aux lettres | 7 × 7 mm noire, **10 mm** du bord de l'ouverture |
| Combles | Faux plafond **100,2 × 25 × 2,4**, origine Y55 / Z46 ; XIAO+Wio dessus |
| Fixation XIAO+Wio | **2 clips pression latéraux en PETG** autour du Wio ; 4 patins PCB + 2 passages de collier maintenus |
| Goulotte | U intérieur arrière, canal droit **7,2 mm**, de Z14 à Z43, **couvercle coulissant amovible** indépendant |
| LED blanche | GTG502WWC sur plan fourni : corps Ø5/ collerette Ø5,9/ hauteur 8,6 ; support n°09 à butée et passage fils |
| LED orange | Ø5 avec collerette Ø5,9, sous palier gauche, trou façade Ø2 |
| USB-C arrière | Platine Gotronic 49067, trou **10 × 4,2 mm provisoire** |

## Clips souples de radio

La pile XIAO/Wio utilise le volume des références STEP existantes : Wio **X40,56..62,87 / Y58,61..76,39 / Z53,43..58,31** ; XIAO **X41,56..64,04 / Y58,61..76,39 / Z59,54..64,002**. Deux supports verticaux sur le faux plafond, en X38,45..39,85 et X63,75..65,15, Y64,2..68,0, portent des lèvres à **Z58,65..59,05**. Elles retiennent la carte Wio inférieure à environ **0,30 mm d'engagement nominal latéral** en laissant libres les composants XIAO situés au-dessus. **PETG conseillé**, insertion douce uniquement ; tolérances et fatigue non vérifiées sur les composants réels. Les anciennes fentes de sangle restent en secours.

## Goulotte arrière droite et fermée

Le canal conserve deux rails imprimés contre la paroi intérieure arrière (X90..91,8 et X99..100,8, Y78,6..82,72), sans aucune lèvre alternée bloquant le cheminement. Chaque rail a une feuillure **0,55 mm de profondeur X**, ouverte par le haut, permettant d'insérer la **10e pièce STL**, `11_couvercle_goulotte_arriere`, **7,9 × 1,1 × 27,8 mm**. Les **0,20 mm de jeu** évitent un montage en force ; butée basse à Z15. Les fils souples montent droit derrière le couvercle, profondeur utile d'environ **2,05 mm**. Pour le retrait, saisir le petit talon au sommet avec le toit déposé. **Ni colle ni trou dans la façade arrière haute**.

## Support de LED blanche

La fiche fournie **Warm white LED.pdf** concerne la **GTG502WWC** (Ø5 corps, Ø5,9 collerette, tête 8,6, collerette 1 MAX, pas2,54, pattes29±0,5). L'ancienne BOM mentionne **Whadda WCS101**, sans preuve d'identité : la géométrie GTG502WWC est une **cote de référence conditionnelle**, à vérifier sur le produit effectivement employé.

Le support n°09, démontable avec ses deux tenons Ø2 dans Ø2,6, reçoit une cavité **Ø6,5** ouverte **depuis le bas** jusqu'à la butée **Z45,2**. Passage de fils **Ø4,4** dans la partie haute du support et à travers le plateau. La pointe de LED se situe nominalement à **Z36,6** ; ajouter un point de silicone neutre compatible électronique près de l'entrée après un essai à blanc. Aucune deuxième pièce de retenue. L'alimentation de LED requiert un courant limité (Vf 3,0–3,4 V à 20 mA selon le PDF).

Le schéma **Bornier SC02/2.54** donne le pas2,54, la profondeur6,5, la hauteur de logement8,5, les pattes3,5 et la largeur5,48 pour deux contacts. Ce bornier reste sur une plaquette externe **non modélisée**.

## Exports et contrôles

**10 STL**, **13 STEP** (10 pièces imprimables, 2 assemblages et 1 XIAO simplifié), **4 coupons**. Les anciens noms « V2 » des assemblages STEP sont historiques et leur **contenu est V14**.

```bash
python cad/generate_cad.py
python cad/qa_geometry.py
python cad/verify_gotronic.py
python cad/test_step_exports.py
python cad/test_component_dimensions_sources.py
python cad/test_fit_coupons.py
python cad/test_repo_consistency.py
```

Le contrôle STEP/maillages, les vérifications BREP source, le dégagement toit/porte/servo, les clips Wio et l'absence de collision du couvercle dans les glissières sont vérifiés par CI. Les **câbles, connecteurs, l'antenne et les composants réels** restent à présenter physiquement.

[README V14](../README.md) · [Plan d'assemblage V14](../docs/FIXATIONS_COMBLES_GOULOTTE_LED_V14.md) · [Nomenclature](bom_dimensions_v1.json).
