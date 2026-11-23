# CAO paramétrique — GarageStateClone V13

**Dimensions courantes en millimètres.** Le script `generate_cad.py` exporte **9 STL imprimables et 12 STEP** à partir des paramètres ci-dessous. Les quatre références BREP fournisseurs sont importées sans les modifier. Les anciennes cotes de construction ne sont pas applicables à cette version.

## Géométrie, implantation et matériaux

| Sous-ensemble | Paramètre V13 |
|---|---|
| Coque et socle | **105,6 × 85 mm**, blanc / noir |
| Haut de la toiture | **62 / 78 mm** avant / arrière |
| Parois / toit / socle | **2,4 / 3 / 3 mm** |
| Ouverture | **55,6 × 42 mm**, origine X11 |
| Porte imprimée | **55 × 41,4 × 2,4 mm**, axe Ø3,2, disque d'accouplement **Ø12** non percé |
| Montants | **11 mm gauche**, **39 mm droit** pour le servo |
| Palier gauche | Corps 4,6 × 12 × 12 ; trou Ø3,8 et tablette d'appui intégrée |
| Boîte aux lettres | Carré noir 7 × 7, niche 7,6 × 7,6, **10,00 mm** du bord droit de l'ouverture au noir visible |
| Toit bac acier noir | 9 nervures trapézoïdales sur le pan, 9 sur la retombée avant, pas 11,5 |
| Faux plafond XIAO/Wio | **100,2 × 25 × 2,4**, plage Y55..80, dessous Z46 |
| LED blanche | X52,8 / Y65, sous la tablette, support séparé à 2 ergots Ø2 |
| LED orange | X5,3 / Z32,0 **sous le palier gauche**, douille intégrée au mur |
| Électricité arrière | Carte USB-C Gotronic 49067, arrivée 5 V et GND ; trou compact 10 × 4,2 **provisoire** |
| Cheminement | 4 clips C du faux plafond au servo + guide arrière bas/haut, **0 œillet au fond** |

Le toit noir est **amovible** ; la porte reste monobloc et bascule vers l'intérieur. Les jeux CAO de base sont **0,30 mm par face** quand cela est indiqué. Une validation CAO n'est pas un contrôle de l'impression ni de la visserie réelle.

## Douille de LED orange

Le **dessin fourni le 23 novembre 2026** (LED orange) cote :
- Corps **Ø5,0 mm**, collerette **Ø5,9 mm**, longueur lentille/face arrière de collerette **8,6 mm**.
- Épaisseur de collerette **1,0 mm MAX**, entre-axes de pattes **2,54 mm**, longueur des pattes **27 mm MIN**.
- Une **douille monobloc Ø9,0 mm extérieur**, imprimée avec `01_coque_blanche`, est intégrée au montant blanc gauche à **X5,3/Z32,0**, **sous la tablette du palier**, dont le bas est Z37,0 ; dessus de douille Z36,5.
- Trou optique avant **Ø2 mm**, corps alésé **Ø5,6 mm** depuis Y3,4, lamage collerette **Ø6,5 mm** depuis Y10,8, accessibles par l'intérieur.
- Installation par l'arrière ; **petite goutte de silicone neutre adapté à l'électronique sur la collerette**, seulement après contrôle de polarité, de lumière et de dégagement des pattes. Pas de clip ni de second STL.

Le support de LED **blanche** reste basé sur une enveloppe de service provisoire `LED_ENVELOPE=(6,9)` : **ne pas réutiliser le dessin orange pour la LED blanche**.

## Faux plafond raccourci et radio

La face avant du faux plafond reste à **Y55** ; l'arrière est à **Y80** et non plus plus loin. La fixation des cartes conserve **4 plots** en Y59 et Y72,5 et **2 passages de sangles** en Y65,5. Les deux longues glissières parallèles au PCB ont été retirées : elles auraient encombré la plage réduite à 25 mm. XIAO et Wio sont décalés d'environ **11,5 mm vers l'avant**, en gardant leurs dimensions BREP. Le câble et l'antenne peuvent demander un coude qui **n'est pas intégré dans les gabarits théoriques**.

La platine USB-C (enveloppe constructeur **21 × 15 × 4,5 mm**) est translatée au dos du socle : référence carte à **X45,3 / Y59,4 / Z9,3** et berceau à **X41,7 / Y57,4 / Z3** ; deux passages de collier en Y64 / Y74,5. Ne pas inventer de trous PCB ou d'offset de la prise : **vérifier la position réelle du connecteur sur la platine et sur la coque avant l'impression définitive**.

La goulotte verticale reste sur le mur arrière intérieur, à X90..100,8, Y78,6..82,72, Z14..43. Les 4 clips C latéraux droit (passage Ø3,4, fente de 2,2 mm) guident les fils depuis l'entrée du faux plafond jusqu'au servo. L'extérieur arrière est plein sauf **l'ouverture USB-C basse de 10 × 4,2 mm**.

## Berceau moteur renforcé et palonniers photographiés (V13)

Le plan coté exact du **DFRobot DMS-MG90** apporte des cotes supplémentaires : corps **23 × 12 mm**, oreilles **33 mm**, sortie **6 mm depuis le bord proche du boîtier**, deux encoches **Ø2 / entraxe 29 mm**, niveaux du capot **16 / 22,5 / 26,5 / 30 mm**, fonctions circulaires Ø3 et Ø5. Le servo reste orienté selon X et logé dans le montant droit de 39 mm.

Les axes des deux pilotes sont désormais calculés sans dépendre de la bbox du STEP tiers : un corps centré entre oreilles donne 5 mm de marge par côté, donc la sortie est à 11 mm de l'oreille proche ; pilotes **Z25,4 / Z54,4** pour la porte à Z45,4. Le plan de serrage reste à **+14,3 mm derrière le bout d'arbre** (cote constructeur 16 mm depuis le fond et 0,30 mm de jeu).

Le support `06_support_servo_step_0p3mm_PROTOTYPE` possède maintenant **2 goussets triangulaires** (épaisseur X1,8 mm), **2 pilotes Ø1,7** avec amorce conique **Ø2,3 sur 0,45**, et une **fenêtre de sortie du câble de 5 mm** dans sa bordure arrière. Les **4 vis au socle sont conservées**. Un **4ᵉ coupon** `D_DMS_MG90_oreilles_entraxe29_pilotes_D1p7` permet de vérifier les oreilles et les vis sur le véritable moteur.

Sur la photo des accessoires, le **palonnier circulaire** est le candidat logique pour entraîner le disque Ø12 de la porte, mais aucune échelle du diamètre, des trous ou des vis n'est fournie. **Le disque reste vierge** et la connexion ne sera pas qualifiée tant que le palonnier ne sera pas mesuré. Voir [les cotes et l'essai V13](../docs/SERVO_DMS_MG90_PALONNIERS_V13.md).

## Servo et limites physiques

Le DMS-MG90 a deux encoches **Ø2 mm, entraxe 29 mm**, représentées par 2 perçages pilotes **Ø1,7**, ainsi que **4 pilotes** du berceau vers le socle (**Ø1,7**, trous de dégagement **Ø2,3**). La position des bossages utilise la cote constructeur **16,00 mm du dessous des oreilles au fond**, avec **0,30 mm de jeu**.

La porte a un disque vierge **Ø12** ; les perçages du vrai **palonnier**, les têtes et longueurs de vis et les dégagements de l'antenne ne sont **pas mesurés**. Tester ces interfaces avant d'imprimer ou de fixer définitivement les pièces.

## Génération et validation

Depuis la racine du dépôt :

```bash
python cad/generate_cad.py
python cad/test_step_exports.py
python cad/test_repo_consistency.py
python cad/test_component_dimensions_sources.py
python cad/test_hardware_bom.py
```

Les fichiers imprimables vont dans `cad/stl/`, les pièces et les 2 assemblages STEP plus la représentation XIAO simplifiée dans `cad/step/`, les **4 coupons** dans `cad/coupons/`. Les STEP d'assemblage gardent un **nom historique avec « V2 »**, mais sont recalculés en V13. Pour **Onshape**, importer de préférence `GarageStateClone_V2_STRUCTURE_SANS_REFERENCES_ONSHAPE.step`, puis les références si nécessaires.

**Tests numériques obligatoires avant merge :** formes et maillages 9/12, vérification source BREP, collisions entre composants référencés et coque/toit/porte/servomoteur, jeu de l'axe Ø3,2, porte **0–90°**, dimensions de la douille orange, dégagement du palier, emplacement XIAO/Wio dans les combles Y55..80, et cohérence des valeurs de la nomenclature.

[README principal V13](../README.md) · [Cotes et justification de la profondeur/LED](../docs/PROFONDEUR_LED_V13.md) · [BOM JSON](bom_dimensions_v1.json) · [Plan d'orange fourni : dimensions consignées ici](component_dimensions_sources_v7.json).
