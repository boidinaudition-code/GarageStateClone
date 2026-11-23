# V12 — Profondeur 85 mm et LED orange sous le palier gauche

**Révision géométrique courante du 23 novembre 2026**, axes CAO : X largeur de gauche à droite, Y profondeur de la façade vers l'arrière, Z hauteur. Toutes les cotes sont en millimètres.

## Réduction de profondeur sans toucher au vantail

| Interface | Valeur V12 |
|---|---:|
| Coque et socle | **105,6 × 85** |
| Hauteur du toit à l'avant / arrière | **62 / 78** |
| Montée sur la profondeur | **16 / 85**, pente ≈10,66° |
| Ouverture / porte | **55,6 × 42** / **55 × 41,4 × 2,4** |
| Montant droit / gauche | **39 / 11** |
| Écart ouverture – boîte noire | **10,00** |
| Boîte noire | **7 × 7** |
| Palier gauche | **4,6 × 12 × 12**, trou Ø3,8, tourillon Ø3,2 |
| Faux plafond | **100,2 × 25 × 2,4**, `Y=55..80`, dessous `Z46` |
| Filets du toit bac acier | **9 pan + 9 façade descendante**, pas X11,5 |
| Câblage interne | 4 clips du plafond au servo + goulotte arrière ; aucun œillet bas |

La modification retire **15 mm du dos** du socle, de la coque et du toit. Elle retire en parallèle **15 mm du fond du faux plafond**, sans avancer son bord avant (**Y55**), qui se trouve derrière le volume balayé par la porte. Les 9 nervures restent solidaires du toit amovible, avec une hauteur de faîtage arrière nominale Z78. La **porte conserve exactement 55 mm de largeur** et sa cinématique, ses dégagements et son disque Ø12 vierge.

### Position des composants après raccourcissement

- **Radio XIAO/Wio :** référence déplacée de **−11,5 mm selon Y** pour faire rentrer le module entre `Y55..80` ; sur l'assemblage V11, le corps de la radio avait une enveloppe **Y70,11..87,89**, l'estimation après déplacement donne **Y58,61..76,39**. L'enveloppe doit être **contrôlée par STEP** en CI (ce n'est pas une certification du câble antenne).
- **Faux plafond :** les deux anciennes longues glissières de PCB sont supprimées pour ne pas immobiliser/écraser le module dans seulement 25 mm de profondeur. Les **4 plots de support** sont déplacés en Y59 et Y72,5 ; **2 passages de collier** sont repositionnés en Y65,5. Aucun perçage inconnu de PCB n'est inventé.
- **Entrée USB-C :** carte Gotronic 49067 déplacée **Y74,4 → Y59,4**, son support intégré au socle **Y72,4 → Y57,4** ; les colliers sont en Y64 et Y74,5. La découpe arrière **10 × 4,2** à Z9,45 est conservée, mais **sa correspondance avec la véritable prise est toujours à mesurer**.
- **Goulotte arrière :** conservée à X90..100,8, déplacée avec le mur arrière sur **Y78,6..82,72**, sur la plage Z14..43. Sa face inférieure de sommet reste juste sous le faux plafond.
- **LED blanche sous plafond :** position X52,8 / Y65, support amovible inchangé.
- **Servo :** toujours dans le montant droit de 39 mm, son berceau et la fixation du palonnier restent inchangés en X/Y et leurs dimensions physiques encore à vérifier.

## LED orange : dessin coté fourni le 23/11/2026

Ce dessin concerne **la LED orange**, pas la LED blanche WCS101. Les cotes lisibles sont les suivantes :

| Dimension | Dessin reçu | Exploitation |
|---|---:|---|
| Diamètre corps | **Ø5,0** | Alésage imprimé Ø5,6, soit jeu radial 0,30 |
| Diamètre collerette | **Ø5,9** | Lamage arrière Ø6,5, soit jeu radial 0,30 |
| De l'extrémité de la lentille à l'arrière de collerette | **8,6** | Profondeur optique corporelle, **pas** la longueur des pattes |
| Épaisseur collerette | **1,0 MAX** | Épaulement d'appui, éviter un ajustement serré |
| Écartement des deux pattes | **2,54** | Câblage ; pas de trou de pattes imposé |
| Longueur des pattes | **27 MIN** | Recouper/plier seulement après contrôle et isolation |
| Section carrée des pattes | **0,5 ± 0,05** | N'intervient pas dans le maintien |

### Support choisi : petite douille intégrée dans la coque

Sur la façade, le **palier gauche** occupe approximativement X3,2..8,0, Y2,7..14,7, Z39,4..51,4. Sa **tablette intégrée** descend jusqu'à **Z37,0**.

La LED orange vient **juste en dessous**, au **centre X5,3 / Z32,0**, sur le **montant blanc gauche de 11 mm**. Elle reste bien **sous la tablette** : la douille intégrée d'un diamètre de **9,0 mm** atteint Z36,5, soit **0,5 mm de jeu vertical théorique** par rapport à la tablette (Z37,0). Le logement est intégré à **`01_coque_blanche`** : **aucune pièce de fixation supplémentaire à imprimer**. Il ne gêne ni le palier démontable, ni la porte, ni les 4 clips du mur droit.

La lentille regarde la façade au travers d'un **trou optique Ø2 mm**. Son extrémité est à **Y3,4** derrière le mur : zone blanche non transparente autour de l'orifice, lumière discrète. Le corps traverse un trou **Ø5,6** ; la collerette se loge dans un contre-alésage **Ø6,5** démarrant à **Y10,8**, accessible depuis l'intérieur. La douille commence à Y2,2 et finit vers Y13,1.

**Montage proposé :** faire un essai d'insertion **par l'intérieur**, vérifier que le dôme repose sur l'épaulement du trou optique, souder/isoler les deux pattes (respecter la cathode), tester l'allumage puis fixer la collerette avec **une minuscule goutte de silicone neutre compatible composants électroniques**. Ne pas faire de clips fins, de joint press-fit ou de collage sur la lentille. Les **27 mm minimum de pattes** doivent être arrangés sans toucher la porte ou le palier et protégés électriquement.

**Réserve :** ce support utilise un plan coté **fourni dans le chat**, pas une inspection physique de la LED réellement achetée. Le profil blanc WCS101 reste non coté avec la même précision. Les cotes de ses supports ne sont pas modifiées.

## Instructions d'impression et contrôles

La version V12 produit toujours **9 STL**, **12 STEP** et **3 coupons**. Pièces concernées : coque, socle, toit, faux plafond et (par déplacement du câblage) position des références USB-C / XIAO / Wio. **Pas de nouvelle pièce de LED orange à imprimer**.

Contrôles automatisés : dimensions globales, 25 mm de faux plafond, passage des vrais volumes proxy XIAO/Wio, absence de collisions avec le toit/socle/coque/porte, trou Ø5,6/Ø6,5 de la LED et l'absence de matière bloquante dans ces alésages, support sous le palier gauche, angles de porte 0–90°, validité des neuf maillages et réimportation des fichiers STEP.

À réception, contrôler **l'orientation du port USB-C sur la 49067**, les dimensions du **palonnier DMS-MG90**, les **vis**, le **rayon de courbure des câbles** et l'insertion réelle de la **LED orange** avant une impression définitive.

[README V12](../README.md) · [Code CAO](../cad/generate_cad.py) · [Nomenclature des dimensions](../cad/bom_dimensions_v1.json).
