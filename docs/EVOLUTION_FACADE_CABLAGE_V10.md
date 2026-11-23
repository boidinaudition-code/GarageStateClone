# Révision V10 (historique) — Fronton nervuré, LED, boîte aux lettres et raccordement USB-C

> **V11 courante :** largeur de coque **105,6 mm**, porte **55 mm**, boîte aux lettres repositionnée à **10 mm** du bord de l'ouverture, passage des fils vers le servo par **4 clips sur le mur droit**, anciens 4 œillets supprimés. Les cotes latérales X du présent document sont historiques. Voir [COMPACTAGE_GARAGE_V11.md](COMPACTAGE_GARAGE_V11.md).

**GarageStateClone — 22 novembre 2026 — source géométrique [`cad/generate_cad.py`](../cad/generate_cad.py).**

À partir de la photographie de référence, l'habillage **métallique anthracite qui descend devant le mur blanc** doit montrer le même nervurage que le toit supérieur. Les dimensions ci-dessous sont des **choix CAO esthétiques**, pas un relevé sur le garage réel. Le socle noir avec le support **Gotronic USB-C 49067**, le servo DMS-MG90, le faux plafond et les firmwares ne changent pas.

## Toiture noire, bac acier sur le pan et sur la façade descendante

- **Pan supérieur existant V9 :** 13 nervures trapézoïdales **selon Y**, espacées de **11,5 mm sur X** (premier centre X5,5, dernier X143,5), base 2,5 mm, couronne 1,1 mm et relief supérieur 0,95 mm.
- **Bandeau avant descendant V10 :** 13 nervures correspondantes, orientées **verticalement (selon Z)**, aux **mêmes centres X** que celles du toit ; relief vers la rue **0,85 mm (−Y)**, bande visible de **Z≈54,37 à Z≈62,47**, débord de toit à **Y≈−3 mm**. Les nervures supérieures ont été prolongées à l'arête avant pour raccorder les deux textures.
- La pente du pan reste **62 mm à l'avant / 78 mm à l'arrière**, l'épaisseur sous la peau du toit **3 mm**, le toit **amovible**, la jupe interne et les jeux de montage **inchangés**. Aucune pièce supplémentaire à coller sur le toit : le fronton est fusionné au **`03_toit_noir_pente`**.
- Les nervures sont cosmétiques ; leur relief extérieur fait désormais dépasser localement le toit d'environ **0,85 mm** devant le débord ancien. Vérifier les coutures et supports en aperçu Bambu Studio avant une impression définitive.

## LED orange : très légère descente

- Position V9 : **X96 / Z53,3 mm**.
- Position V10 : **X96 / Z52,8 mm**, soit **−0,5 mm**.
- Le support interne et le conduit optique sont modifiés ensemble. Le firmware reste sur **D0**, avec la même logique électrique.

## Boîte aux lettres noire : réduction de 30 %

L'ancienne plaque noire V9 mesurait **10 × 10 mm**. La nouvelle plaque mesure **7 × 7 mm**, soit **−30 % sur chacune des deux dimensions linéaires** (surface 51 % de l'ancienne). Le centre reste en **X129,8 / Z29,3** sur le montant blanc droit.

| Détail | V10 |
|---|---|
| Logement dans la coque | **7,6 × 7,6 × 1,05 mm**, X126..133,6, Z25,5..33,1 |
| Pièce noire indépendante | **7 × 7 × 0,75 mm** (fente décorative en léger creux) |
| Jeu en largeur/hauteur | **0,30 mm** de chaque côté |
| Face externe visible | **Y=0,10 mm**, donc petit retrait |
| Mur restant derrière la niche | **1,35 mm** sur les 2,4 mm de façade |

Imprimer **`10_boite_aux_lettres_noire.stl`** séparément en noir ; l'ajuster à blanc puis coller sans débordement sur le mur blanc. Le carré et son logement sont uniquement cosmétiques.

## USB-C 49067 : seule la prise doit apparaître

La V8 prévoyait un **grand trou de service 13 × 8 mm**. La V10 remplace ce trou par un passage compact **10,0 × 4,2 mm**, au dos de la coque, de **X70 à X80** et de **Z9,45 à Z13,65** ; il traverse toujours le mur arrière. Le **support imprimé sur le socle noir** demeure inchangé.

**Réserve essentielle :** Gotronic ne donne que l'encombrement externe de la platine **21 × 15 × 4,5 mm** et **ne cote ni le contour exact du nez femelle, ni sa position sur le PCB**. Le trou de 10 × 4,2 est donc une **approximation volontairement minimale**, pas un ajustement garanti. Après réception, présenter la 49067 sur son support, essayer un câble USB-C mâle et relever le centre X/Z du port, la saillie et le contour effectif. **Corriger la CAO localement avant impression définitive de la coque si nécessaire** ; ne pas limer ou forcer la platine pour la faire correspondre à un trou estimé.

L'alimentation reste **USB 5 V vers un bus parallèle** XIAO/servo, GND commun et condensateur de 470 µF près du servo ; ne jamais charger le 3V3 du XIAO avec le servo. Voir [le guide d'alimentation](ALIMENTATION_USB_C_V8.md).

## Aucune sortie haute arrière : goulotte passe-câbles interne

L'ancienne ouverture de service **16 × 9 mm**, à hauteur du faux plafond sur le **mur arrière blanc**, est **supprimée**. L'arrière présente ainsi **une seule découpe basse, pour le port USB-C**.

La coque reçoit à l'intérieur **deux rails de guidage de câbles** le long du mur arrière :
- position approximative **X90..100,8 / Y93,6..97,72 / Z14..43** ;
- **2 rails de 1,8 mm**, encadrant un passage libre **7,2 mm**, ouverts vers l'intérieur ;
- **3 petites lèvres alternées** en Z19, Z29 et Z39 pour retenir une nappe de fils souples, sans créer un conduit fermé et inaccessible ;
- la goulotte reste **au-delà du support USB-C (X≈64..86)**, sous le faux plafond (Z46), sans dépasser à l'extérieur.

Câbler de la distribution 5 V au bas vers le récepteur dans les combles par le volume intérieur. Le cheminement ne doit pas gêner la porte en rotation, le servo, les pattes de fixation, l'antenne ou la fermeture du toit. **Il reste 3 mm entre le haut de la goulotte et le fond nominal du faux plafond**, donc contrôler le rayon de courbure et la sortie des fils lors du montage réel.

## Éléments impactés et fichiers livrés

Le nombre d'éléments à imprimer reste **9 STL** et **12 STEP**. Changements uniquement sur :
- **`01_coque_blanche`** : niche réduite, LED déplacée, prise arrière minimale, trou haut fermé et goulotte interne ;
- **`03_toit_noir_pente`** : les nervures du dessus se prolongent sur le bandeau descendant ;
- **`10_boite_aux_lettres_noire`** : plaque noire réduite.

Les six autres STL, dont le socle USB-C, gardent leurs interfaces. Les 3 coupons d'ajustement restent disponibles. Les tests CI contrôlent la validité STEP/STL, les intersections, la fermeture du mur arrière, la goulotte ouverte, la boîte aux lettres, la continuité des nervures et la porte de 0° à 90°. **La validation numérique ne garantit pas le jeu réel USB-C ni les fils souples.**

[README général](../README.md) · [README CAO](../cad/README.md) · [Guide historique du toit V9](TOIT_BAC_ACIER_BOITE_LETTRES_V9.md) · [Documentation USB-C V8](ALIMENTATION_USB_C_V8.md).
