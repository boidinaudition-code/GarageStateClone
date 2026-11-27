# Façade V15 révisée — porte piétonne 17 mm, boîte aux lettres, sans interphone

**Version de la branche `cad/v15-facade-porte-interphone-rendu-reference` — 24 novembre 2026.**
Le nom historique du présent fichier mentionne encore l'interphone, mais celui-ci a été **entièrement supprimé** de la géométrie CAO et des exports imprimables. Ces dimensions sont issues des instructions utilisateur pour une maquette esthétique, pas d'un relevé réel.

## Implantation en façade (X depuis la gauche, millimètres)

L'ensemble de la coque garde sa largeur de **105,6 mm**. La porte de garage motorisée reste à **X11..66,6** (ouverture de **55,6 mm**, panneau noir de 55 mm). Le montant droit conserve **39 mm**, de X66,6 à 105,6.

| Élément visible noir | Bord gauche | Bord droit | Largeur |
|---|---:|---:|---:|
| Fin de l'ouverture de garage | — | **66,6** | 55,6 pour l'ouverture entière |
| **Espace blanc après garage** | **66,6** | **71,6** | **5,0** |
| **Boîte aux lettres noire** | **71,6** | **78,6** | **7,0** |
| **Espace blanc avant porte piétonne** | **78,6** | **83,6** | **5,0** |
| **Porte piétonne noire fixe** | **83,6** | **100,6** | **17,0** |
| **Bord blanc droit** | **100,6** | **105,6** | **5,0** |

Les cotes de **5 mm** sont mesurées entre les faces visibles, **et non entre les niches**. Avec un jeu FDM nominal de **0,30 mm de chaque côté**, les découpes sont légèrement plus grandes.

## Boîte aux lettres et rectangle blanc

- Logement blanc peu profond : **7,6 × 7,6 × 1,05 mm**, origine **X71,3 / Z25,5**.
- Pièce noire : **7 × 7 × 0,75 mm**, face extérieure très légèrement en retrait ; centre X75,1/Z29,3.
- Pièce blanche séparée : `14_insert_blanc_boite_lettres`, rectangle **5,1 × 0,8 × 0,35 mm** dans un logement local **5,5 × 1,2 mm** du carré noir.
- Jeu nominal **0,30 mm** par côté dans la façade, et environ 0,20 mm autour de la pièce blanche. Essai à blanc et collage léger.

## Porte piétonne noire de 17 mm

- Logement blanc : origine **X83,3 / Z3,25**, **17,6 × 38,4 × 1,0 mm**.
- Pièce `12_porte_pietonne_noire` : panneau visible de **17,0 × 37,8 × 0,76 mm**, origine **X83,6 / Z3,55**.
- La partie visible présente **5 rainures verticales en creux**, un panneau central encadré, une traverse basse et **une poignée noire en relief** fusionnée à la porte.
- Le fond de mur blanc reste **1,4 mm d'épaisseur** au minimum derrière le logement. La porte est décorative, **non ouvrante**.
- Il subsiste **5 mm** entre son bord droit et le bord extérieur du bâtiment.

## Interphone supprimé

La précédente V15 avait un interphone gris entre la boîte et la porte. Cette proposition est **abandonnée** : ni `13_interphone_gris`, ni cavité de fixation, ni perçage, ni composant associé ne figurent dans la CAO révisée. Le mur blanc est continu entre le carré noir et la porte, avec le jeu visible de 5 mm demandé.

Le numéro de pièce 13 est volontairement laissé inoccupé pour éviter de réaffecter le nom historique à une pièce différente. Les nouvelles pièces imprimables restent numérotées **12** (porte piétonne) et **14** (rectangle blanc).

## Toit et parties non modifiées

Le toit noir amovible conserve **9 nervures trapézoïdales** sur le dessus et **9 retours nervurés** en façade, ainsi que les deux rives latérales de **0,55 mm** et le larmier frontal de **0,70 mm**. La pente **62/78 mm**, le socle, les supports du DMS-MG90, la porte de garage, les clips XIAO/Wio, les LED, la goulotte couverte et l'USB-C restent inchangés.

## Export et validation

La branche révisée doit livrer **12 fichiers STL** imprimables, **15 fichiers STEP** (12 pièces, un assemblage avec références, un assemblage structure seule pour Onshape, un XIAO simplifié) et **4 coupons de contrôle**.

Les contrôles CI vérifient l'intervalle exact entre les faces noires et leurs positions X, l'absence de solide d'interphone et de niche correspondante, l'intégrité de la coque, les intersections des inserts, la structure mécanique, le débattement motorisé 0–90°, les maillages et la cohérence BOM/manifeste/README.

**Limites physiques :** la porte piétonne reste une pièce de décoration à coller, non une vraie ouverture ; les jeux de collage et la finition du rectangle blanc demandent un essai d'impression. Le palonnier du servo et la géométrie exacte du port USB-C Gotronic 49067 doivent encore être validés sur les pièces reçues.

[README général](../README.md) · [README CAO](../cad/README.md) · [générateur paramétrique](../cad/generate_cad.py).
