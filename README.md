# GarageStateClone — Miniature de garage connectée (V12)

**Version en cours : V12 — 23 novembre 2026.** Miniature imprimable de porte de garage, sur une base **105,6 × 85 mm**, dont la porte noire **55 mm** bascule vers l'intérieur. L'objet reflète approximativement l'état d'une vraie porte à travers une liaison **LoRa 868 MHz** entre deux kits Seeed XIAO nRF52840 / Wio-SX1262. **Il ne commande pas le moteur réel** et ne doit pas être utilisé comme dispositif de sécurité.

## Géométrie actuelle

| Élément | Cote ou principe V12 |
|---|---|
| Encombrement de la coque / du socle | **105,6 × 85 mm** |
| Toit avant / arrière | **62 / 78 mm** de hauteur totale, 16 mm de montée sur 85 mm de profondeur |
| Toit noir bac acier amovible | **9 nervures trapézoïdales** sur le pan et 9 alignées sur le bandeau descendant, pas de 11,5 mm |
| Coque / toit / fond | Épaisseurs **2,4 / 3 / 3 mm** |
| Ouverture en façade | **55,6 × 42 mm** |
| **Porte noire imprimée** | **55 × 41,4 × 2,4 mm**, rainures décoratives, bascule rigide 0–90° en CAO |
| Montants gauche / droit | **11 / 39 mm** ; servo placé dans le montant droit |
| Boîte aux lettres | Pièce noire indépendante **7 × 7 mm**, dans une niche 7,6 × 7,6 mm ; **10 mm** entre le bord droit de l'ouverture et le bord noir visible |
| Palier gauche | Bloc compact **4,6 × 12 × 12 mm**, tourillon **Ø3,2** dans alésage **Ø3,8** |
| Faux plafond arrière amovible | **100,2 × 25 × 2,4 mm**, de Y55 à Y80 et à Z46 |
| LED blanche | Sous le faux plafond, centrée en X52,8 / Y65, support indépendant à deux ergots |
| LED orange | **Sous le palier gauche**, centre X5,3 / Z32,0, logement intégré au mur blanc |
| USB-C arrière | Platine Gotronic **49067**, support intégré au socle, ouverture provisoire **10 × 4,2 mm** |
| Câbles | **Aucun œillet bas** ; 4 clips en C sur mur droit vers le servo, plus goulotte verticale interne arrière |

Le **boîtier** blanc conserve **0,30 mm de jeu de conception par face** aux emboîtements concernés. Les mesures de l'imprimante doivent confirmer ce jeu après les coupons.

### LED orange : montage compact basé sur le plan fourni

Le dessin de la LED orange transmis le 23/11/2026 indique : **corps Ø5 mm**, **collerette Ø5,9 mm**, **longueur optique jusqu'à l'arrière de la collerette 8,6 mm**, épaisseur de collerette **1,0 mm maximum**, pas des deux pattes **2,54 mm**, et pattes **27 mm minimum**.

La coque comporte un **petit fourreau imprimé d'un seul tenant, Ø9 mm extérieur**, placé **juste sous la tablette du palier gauche**. L'arrière est accessible : passage **Ø5,6 mm** pour le corps et lamage **Ø6,5 mm** pour la collerette (jeu radial nominal de 0,30 mm). Un **orifice optique discret Ø2 mm** subsiste côté façade, avec une LED reculée de 3,4 mm. La LED s'insère **par l'intérieur** et se retient, après essai, par une **petite goutte de silicone neutre compatible électronique** sur la collerette. **Aucun clip fragile ni pièce supplémentaire à imprimer**. Éviter la colle sur le dôme et isoler les pattes soudées ; ne pas confondre la longueur du corps avec les pattes de 27 mm, à adapter au câblage.

Ce plan fourni par l'utilisateur est la référence dimensionnelle de la LED **orange** ; la géométrie de la LED **blanche WCS101** demeure une enveloppe provisoire distincte. La correspondance du plan avec le composant livré est à vérifier avant montage.

### Électronique et servo

Le DFRobot **DMS-MG90** est placé derrière le montant droit : deux encoches de fixation **Ø2 à entraxe 29 mm** (selon Z) et **2 pilotes de retenue Ø1,7 mm** sur le berceau ; le berceau se fixe au socle par **4 autres pilotes Ø1,7 / dégagements Ø2,3 mm**, indépendants. Le plan du fabricant situe le dessous des oreilles à **16,00 mm du fond du servo** et le support imprimé prévoit **0,30 mm de jeu axial**. La pièce côté porte porte un **disque Ø12 mm sans perçage de palonnier**, car l'entraxe réel des vis et la longueur sous tête ne sont pas connus.

L'assemblage XIAO + Wio-SX1262 est dans les combles, sur quatre patins et deux emplacements de sangles, recentrés pour le faux plafond de **25 mm**. Le câblage monte de la prise USB-C par la **goulotte intérieure arrière** et rejoint le servo par les **quatre clips du mur droit**. Les deux anciennes longues glissières de PCB ont été retirées pour préserver la place autour du module de 22 mm environ. Les câbles d'antenne et USB-C doivent être présentés avec leurs rayons de courbure réels.

## Alimentation et branchements

Une **alimentation USB-C 5 V / 2 A minimum** arrive sur la platine femelle Gotronic 49067. Distribuer **5 V et GND en parallèle** vers le XIAO récepteur et le servo ; ajouter **470 µF / 16 V** entre +5 V et GND près du servo. **Ne pas alimenter le servo depuis la broche 3V3 du XIAO**. La commande du servo utilise **D6**, la LED blanche **D7** et la LED orange **D0** (pilotage actif à l'état bas selon le firmware).

Vérifier si la platine 49067 intègre déjà les deux résistances USB-C **5,1 kΩ entre CC1/GND et CC2/GND** ; les ajouter uniquement si absentes. Ne pas relier CC1 et CC2 ensemble. **Débrancher l'alimentation externe 5 V avant de relier le XIAO à un ordinateur pour le programmer**, sauf montage avec isolation validée.

Le contour **10 × 4,2 mm** et la position du nez USB-C sont **provisoires** : Gotronic donne l'encombrement de carte **21 × 15 × 4,5 mm**, mais pas la position exacte du connecteur. Tester la carte et une fiche USB-C avant l'impression définitive de la coque.

## Comportement du système

Un **SAS308** à contact magnétique au garage réel confirme uniquement l'état **complètement fermé**. Le récepteur fait évoluer l'affichage de la miniature :

| Contact / communication | Interprétation | Miniature |
|---|---|---|
| Contact fermé | Porte réellement fermée (détection du capteur) | Fermée |
| Contact ouvert, délai inférieur à 40 s | Non fermée | Position intermédiaire estimée, LED orange clignotante |
| Contact ouvert au-delà de 40 s | Ouverte **présumée** | Ouverte estimée, LED blanche allumée |
| Trames radio absentes depuis plus de 150 s | Liaison périmée | Dernière consigne retenue, signal LED de défaut |

Les angles servo configurés restent **15° fermé / 95° ouvert** ; la CAO vérifie un mouvement de porte **0–90°**, mais le montage réel nécessitera un réglage mécanique du palonnier. Une vraie porte bloquée à mi-course peut être annoncée ouverte : il s'agit d'un **affichage décoratif d'état estimé, pas d'une alarme**.

## Fabriquer, tester, importer dans Onshape

Le script `cad/generate_cad.py` produit dans `cad/stl/` **9 STL imprimables**, dans `cad/step/` **12 STEP** (9 pièces, 1 assemblage avec références électroniques, 1 structure sans références tierces, 1 XIAO simplifié), et **3 coupons** pour l'axe Ø3,2, les pilotes M2 et le disque de palonnier. Le fichier d'assemblage conserve un nom historique contenant « V2 » : **la géométrie générée est V12**.

```bash
python cad/generate_cad.py
python cad/test_step_exports.py
python cad/test_repo_consistency.py
python cad/test_hardware_bom.py
python cad/test_component_dimensions_sources.py
```

La CI GitHub Actions valide la génération, les maillages et BREP, les exports STEP, la cohérence JSON/README, la compilation des firmwares, les jeux et la porte en rotation. Cela **ne remplace pas un essai mécanique imprimé**.

**À contrôler à réception :** gabarit du vrai palonnier et vis DMS-MG90, position réelle du connecteur USB-C de la 49067, dégagement du câble d'antenne, et présentation de la LED orange dans son siège. Pour la première impression, faire les coupons, présenter les composants sans collage puis seulement finaliser la coque.

## Documentation et fichiers

- [Plan mécanique V12 : profondeur, implantation radio et fixation LED](docs/PROFONDEUR_LED_V12.md)
- [Sources CadQuery et README technique](cad/README.md)
- [Catalogue des dimensions constructeur et du dessin LED orange](cad/component_dimensions_sources_v7.json)
- [Nomenclature dimensionnelle courante](cad/bom_dimensions_v1.json)
- [Nomenclature d'approvisionnement](cad/hardware_bom_v5.json)
- [Actions CI / fichiers STEP et STL générés](.github/workflows/cad-validation.yml)

**Ne jamais raccorder ce dispositif au secteur 230 V, à la commande du moteur de garage ni à une entrée de sécurité du portail.**
