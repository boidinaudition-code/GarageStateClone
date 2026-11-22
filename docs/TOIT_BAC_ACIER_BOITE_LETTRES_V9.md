# V9 — Toit bac acier et boîte aux lettres sur façade

**Projet : GarageStateClone · 22 novembre 2026 · unités en millimètres.**

> **Archive V9 :** la version actuelle est **V10** : les mêmes 13 nervures sont prolongées sur le bandeau métallique descendant, LED orange abaissée 1,2 mm et boîte noire réduite à 7 × 7 mm. Voir [EVOLUTION_FACADE_CABLAGE_V10.md](EVOLUTION_FACADE_CABLAGE_V10.md) pour les cotes à imprimer ; les cotes V9 ci-dessous décrivent l'ancienne géométrie.


Les deux photos fournies par le propriétaire montrent une façade de garage blanche, une porte sectionnelle noire et une **petite boîte aux lettres noire à droite du portail**. La couverture métallique gris anthracite comporte des **lignes régulières verticales sur la bande en façade**. La maquette choisit une interprétation **bac acier à nervures sur le pan de toit** : cette géométrie est volontairement décorative et **n'est pas une reproduction cotée exacte du vrai profil métallique**.

## 1. Toit noir, plan incliné et nervures

- **Géométrie conservée :** coque **150 × 100**, haut du toit **Z=62 devant / Z=78 derrière**, soit une pente de **16 mm / 100 mm** (≈9,1°) ; épaisseur pleine du toit sous sa face initiale **3 mm**, jupe amovible, débord de 3 mm et lèvre verticale 4,5 mm.
- **Géométrie ajoutée :** **13 nervures trapézoïdales** au-dessus du plan, longitudinales **selon Y** (direction de pente), **pas 11,5 mm** selon X. Premier centre **X=5,5**, dernier centre **X=143,5**. Base **2,5 mm**, sommet **1,1 mm**, hauteur en relief **0,95 mm**. Longueur en Y **−2,5 à 102,5 mm**, à l'intérieur des bords de toiture **−3 à +103 mm**.
- Les nervures sont fusionnées au volume du toit sur **0,18 mm** de recouvrement numérique. Il n'y a ni plaque supplémentaire à coller, ni perçage au travers de la toiture, ni épaississement en dessous de son plan.
- **Impression :** `03_toit_noir_pente.stl` noir ; réorienter dans le slicer. Vérifier en aperçu tranche que les treize nervures sont imprimées sans disparaître au niveau du réglage de hauteur de couche/buse. Éviter de poncer le relief.

Le détail est basé sur les photographies, non sur un vrai relevé de tôle ou une gamme industrielle. Il est paramétré dans `cad/generate_cad.py` via `ROOF_RIB_*`.

## 2. Boîte aux lettres à droite de la porte

Le carré noir sur les photos est situé **juste à droite de la baie**, à mi-hauteur environ du mur. À l'échelle de la miniature, la façade a une **baie X11..111** et le montant droit mesure **39 mm** de largeur.

| Élément | Position et dimensions CAO | Finition |
|---|---|---|
| **Logement dans la coque blanche** | **X=124,5..135,1**, **Z=24..34,6**, **Y=0..1,05** depuis la face extérieure | Renfoncement peu profond, **10,6 × 10,6 × 1,05** |
| **Plaque noire séparée** | **10 × 10 × 0,75** ; face vue à Y=0,10 une fois assemblée | Collage léger uniquement après essayage |
| **Jeu de mise en place** | **0,30 mm tout autour** ; espace arrière nominal **0,20 mm** | Colle en très faible quantité |
| **Mur porteur restant** | Façade initiale **2,4 mm**, fond du logement résiduel **1,35 mm** | Exception locale cosmétique, aucune traversée du mur |
| **Fente sur plaque** | Trait gravé en léger creux, non débouchant | Détail décoratif facultatif |

**Nouvelle pièce imprimable :** `10_boite_aux_lettres_noire.stl` et `.step`. Les deux pièces `01_coque_blanche` et `10_boite_aux_lettres_noire` sont distinctes dans le STEP d'assemblage. Laisser le carré noir en place sans le coller pour la première présentation à blanc : le retrait de 0,10 mm et les jeux sont des cibles d'impression FDM non garanties par la machine.

**Attention** : la position choisie est une interprétation à l'échelle fondée sur l'apparence de la photo, pas une mesure dimensionnelle du bâtiment. Aucun impact sur l'ouverture rigide de la porte, les colonnes servo, la platine d'alimentation USB-C en bas à l'arrière, la radio dans les combles ou les LEDs.

## 3. Fichiers et validation

La CAO paramétrique V9 exporte **9 STL imprimables** et **12 STEP** :
- 9 STEP individuels pour les 9 éléments, dont le nouveau carré noir ;
- 1 STEP assemblage complet avec références électroniques ;
- 1 STEP structure seule, sans références tierces, adapté à Onshape ;
- 1 STEP XIAO simplifié à importer séparément si besoin.

Les 3 éprouvettes d'ajustement V6 sont toujours générées à part. Les tests CI contrôlent l'unicité des volumes, le maillage fermé, la réimportation STEP, les nervures, le jeu de la boîte aux lettres, les collisions, ainsi que le débattement porte 0–90°.

**Ne pas confondre validation numérique et validation réelle :** la finition est imprimable théoriquement mais les dimensions du servo/palonnier, des câbles de l'antenne et du nez USB-C Gotronic 49067 restent à vérifier. Ne pas commander de nouveau composant électrique pour cette seule modification.

[Source CadQuery](../cad/generate_cad.py) · [README général](../README.md) · [README CAO](../cad/README.md) · [alimentation USB-C V8](ALIMENTATION_USB_C_V8.md) · [fixation servo V7](FIXATIONS_SERVO_V7.md).
