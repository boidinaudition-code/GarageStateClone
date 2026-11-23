# V11 — Garage compact 105,6 mm, porte de 55 mm et chemins de câbles vers le servo

**Révision de la CAO GarageStateClone — 23 novembre 2026.** Source de vérité : [`cad/generate_cad.py`](../cad/generate_cad.py), en millimètres. Cette page remplace les dimensions globales V6–V10, sans rendre exactes les pièces électroniques non mesurées.

## Nouvelle implantation : largeur réduite sans affaiblir le montant servo

| Cote et interface | V10 | **V11 courante** |
|---|---:|---:|
| Largeur extérieure de la coque et du socle | 150 | **105,6** |
| Profondeur | 100 | **100** |
| **Largeur du vantail noir réellement imprimé** | 99,4 | **55,0** |
| Ouverture dans la coque (largeur × hauteur) | 100 × 42 | **55,6 × 42** |
| Porte imprimée (L × H × ép.) | 99,4 × 41,4 × 2,4 | **55,0 × 41,4 × 2,4** |
| Jeu horizontal de la porte | 0,30 par côté | **0,30 par côté** |
| Montant gauche | 11 | **11** |
| Montant droit, avec servo | 39 | **39** |
| Écart ouverture → bord **visible noir** de boîte aux lettres | non imposé | **10,00** |
| Boîte aux lettres noire | 7 × 7 | **7 × 7** |
| Toit bac acier, nervures dessus + bandeau descendant | 13 + 13 | **9 + 9** |

**Calcul :** 11 mm de montant gauche + (55,0 + 2 × 0,30) mm d'ouverture + 39 mm de montant servo = **105,6 mm de largeur totale**. Ce n'est **pas** un rétrécissement uniforme des pièces : le servo conserve le même volume utile, son entretoise, ses quatre vis de fixation au socle et ses deux points d'oreilles constructeur espacés de 29 mm.

**Coordonnées de référence V11 (X depuis la gauche)** :
- Ouverture noire : **X11,00 → X66,60** ; vantail **X11,30 → X66,30** ;
- Bord visible gauche de la boîte aux lettres : **X76,60**, soit **10,00 mm** après l'ouverture X66,60. Niche pour collage : **X76,30 → X83,90**, largeur 7,6 ; plaque noire : **X76,60 → X83,60**, largeur 7,0 ;
- Le logement de boîte aux lettres garde sa cote verticale **Z25,50 → Z33,10**, sa profondeur 1,05 et une paroi résiduelle de 1,35 ;
- LED orange : **X51,60 / Z52,80** ; position recalculée en X pour suivre l'ouverture plus courte ;
- Face du disque de porte Ø12 : **X67,10** ; bout d'arbre nominal du servo **X69,30** ; jeu axial théorique **2,20** *hors palonnier physique* ;
- Dessous nominal des oreilles du servo : **X83,30**, face des bossages imprimés **X83,60** (cote constructeur 16,00 depuis le fond + jeu 0,30). Ne pas garder les anciens X113,70 / X128,00 de la maquette large.

## Palier gauche : réduction raisonnée

La pièce `05_palier_gauche` passe de son corps principal **5,0 × 14,6 × 19,0 mm** à **4,6 × 12,0 × 12,0 mm**, avec bride de collage adaptée. Son trou **Ø3,8** est inchangé pour le tourillon imprimé **Ø3,2**, soit 0,30 de jeu radial. La tablette de support **solidaire de la coque** est remontée à **Z39,4** pour recevoir la face inférieure du palier réduit, avec contact nominal sans empiétement ; vérifier l'adhérence après essai à blanc. La pièce est plus petite, **mais pas allégée au détriment des parois autour du trou**.

## Quatre œillets bas supprimés ; quatre supports du faux plafond vers le servo

Les **quatre anciens anneaux Ø8/Ø3,4 situés vers Z12** ont été **retirés de la coque blanche**. Ils étaient destinés à l'ancien cheminement et occupaient inutilement les parties basses.

La coque reçoit **quatre clips imprimés en forme de C**, intégrés à la **face intérieure du mur latéral droit**, sur un chemin du bord avant du faux plafond (**Y55**) vers le servo (**Y≈3..16**).

| Clip | Centre Y | Centre Z |
|---|---:|---:|
| Depuis les combles | 51 | 43,5 |
| Guide 2 | 41 | 43,0 |
| Guide 3 | 31 | 42,5 |
| Près du servo | 21 | 42,0 |

Chaque clip possède un logement **Ø3,4 mm**, diamètre extérieur **Ø7,4 mm**, épaisseur **2,4 mm** suivant Y, une fente d'introduction ouverte de **2,2 mm côté intérieur**, et une épaisseur radiale imprimée de **2,0 mm**. Les câbles souples peuvent être engagés par le côté dans ces clips : ne pas les imposer comme points de traction, ne pas comprimer un coaxial ou connecteur d'antenne et contrôler les courbures réelles.

La **goulotte arrière verticale V10** (X90..100,8 / Z14..43, rails 1,8, passage libre 7,2 mm) est conservée pour la montée des câbles d'alimentation depuis la prise USB-C. Les **clips latéraux** constituent une seconde route de la zone des combles vers le servo ; aucun trou supplémentaire ne traverse les parois.

## Autres pièces redimensionnées

- **`01_coque_blanche`** et **`02_socle_noir`** : largeur **105,6 mm**, trous USB-C bas conservés (profil 10 × 4,2, **encore provisoire**), aucune ouverture haute arrière ; la goulotte arrière reste située dans la coque.
- **`03_toit_noir_pente`** : largeur adaptée au nouveau châssis, **9 nervures** au lieu de 13 sur le pan supérieur et **9 en façade descendante**, toujours au pas 11,5, avec les mêmes reliefs 0,95 et 0,85.
- **`04_porte_noire`** : vantail 55 mm, rainures et tourillon intégrés préservés ; interface de palonnier **Ø12 vierge**.
- **`07_faux_plafond_combles_XIAO`** : largeur utile **100,2 mm** ; les quatre patins de Wio, deux fentes de sangle et la LED blanche sont recalés sur le centre X=52,8 au lieu de75. Les géométries BREP source des cartes sont conservées intactes.
- **`09_support_led_blanche`** : décalé avec le faux plafond, sans modifier son emboîtement.
- **`10_boite_aux_lettres_noire`** : reste noire, 7 × 7 × 0,75, repositionnée à 10 mm de l'ouverture.
- **`06_support_servo_step_0p3mm_PROTOTYPE`** : même interface mécanique fabricant et perçages, repositionné avec le montant droit.

**Nombre de fichiers :** toujours **9 STL**, **12 STEP** et **3 coupons d'essai**. Les noms des STEP d'assemblage conservent historiquement « V2 » mais leur **contenu est bien V11** si téléchargé depuis le dernier run.

## Contrôles et limites

La CI vérifie les enveloppes, les maillages étanches, l'import STEP, les 9+9 nervures, l'écartement boîte/porte 10 mm, les 4 clips avec passage libre et la disparition des 4 anciens œillets, le contact tablette/palier, le repositionnement des cartes et de la prise USB-C, et **les mouvements de porte de 0 à 90°**.

**Toujours à mesurer avant impression définitive et installation :** dimensions du palonnier et de ses vis, fixation exacte du vrai DMS-MG90, position réelle du connecteur USB-C de la 49067, coudes des câbles/antenne sous le toit, résistances CC1/CC2 de l'embase. Une CI verte ne garantit ni l'ajustement physique ni la résistance des pièces imprimées.

[README](../README.md) · [README CAO](../cad/README.md) · [Guide V10 historique](EVOLUTION_FACADE_CABLAGE_V10.md) · [Servo V7](FIXATIONS_SERVO_V7.md).
