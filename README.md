# GarageStateClone — V15, façade fidèle au rendu et mécanique V14 préservée

**Révision 24 novembre 2026.** Miniature de garage imprimée en 3D, **105,6 × 85 mm**, porte basculante noire **55 mm**, affichage d'état LoRa du garage réel sans commande du moteur réel. Le projet ne constitue pas un dispositif de sécurité.

## Géométrie actuelle et fonctionnalités

| Élément | Conception V15 |
|---|---|
| Coque/socle | **105,6 × 85 mm**, blanche/noire, murs **2,4 mm** |
| Toit | Noir amovible, **62 / 78 mm**, 9 nervures bac acier sur pan et bandeau avant ; **2 rives surélevées et larmier frontal** |
| Porte | Ouverture **55,6 × 42 mm**, vantail imprimé **55 × 41,4 × 2,4 mm**, jeu **0,30 mm** de chaque côté |
| Montants | Gauche **11 mm**, droit servo **39 mm** |
| Boîte aux lettres | Carré noir **7 × 7 mm**, niche **7,6 × 7,6 mm**, **5 mm** après la porte de garage et **5 mm** avant la porte piétonne ; **rectangle blanc de 5,1 × 0,8 mm** séparé |
| Porte piétonne décorative | À droite, largeur **17 mm** (panneau **17 × 37,8 mm**), niche **17,6 × 38,4 × 1 mm** ; **5 rainures**, cadre, traverse basse et poignée intégrée ; **fixe, non fonctionnelle** |
| Interphone | **Supprimé** : aucun composant ni logement dans la façade |
| Palier de gauche | Bloc **4,6 × 12 × 12 mm**, tourillon Ø3,2 et alésage Ø3,8 |
| Moteur | DFRobot DMS-MG90, 2 fixations d'oreilles Ø2/entraxe 29 mm, berceau à 2 goussets, 4 fixations au socle (dégagement Ø2,3 mm) |
| Faux plafond | **100,2 × 25 × 2,4 mm**, de Y55 à Y80, démontable sous les combles |
| LED orange | Sous le palier gauche, centrée X5,3 / Z32, boîtier Ø9 intégré et trou de façade Ø2 |
| LED blanche chaude | Sous le faux plafond, nouveau logement à collerette pour LED de type **GTG502WWC**, insertion par dessous |
| Réception radio | XIAO nRF52840 + Wio-SX1262, **2 clips latéraux imprimés** sur le plateau, plus 4 plots et 2 fentes de collier de secours |
| Câbles | **4 clips** le long du mur droit pour les fils du servo ; **goulotte arrière droite et fermée par couvercle coulissant**, aucun œillet bas |
| Alimentation | Platine USB-C Gotronic 49067 sur socle noir, trou arrière **10 × 4,2 mm provisoire** |

### Finition V15 révisée : 5 mm / 7 mm / 5 mm / 17 mm

Sur le montant droit blanc de **39 mm**, le bord de la baie motorisée est **X66,6**. Les espaces sont mesurés **entre les faces noires visibles**, et non entre les logements de collage : **5 mm** avant la boîte aux lettres noire (**X71,6..78,6**, largeur 7 mm), puis **5 mm** jusqu'à la porte piétonne noire (**X83,6..100,6**, largeur **17 mm**). Il reste **5 mm de marge blanche** jusqu'au bord droit de la façade (**X105,6**).

La porte piétonne garde sa poignée, ses cinq rainures verticales, son panneau bas et sa fixation collée dans une niche peu profonde (**17,6 × 38,4 × 1 mm**). Le petit **rectangle blanc** sur la boîte aux lettres est conservé comme pièce indépendante. **Interphone supprimé : plus aucune platine ni aucun renfoncement prévu à cet emplacement.**

Les deux rives et le larmier frontal restent **fusionnés au toit noir amovible**, avec **9 nervures** sur le pan et leur retour sur le bandeau. La porte basculante de 55 mm, la LED orange à gauche, le servo DMS-MG90, la radio et l'alimentation USB-C sont inchangés. Les détails de la porte piétonne ne sont pas fonctionnels ; vérifier la finesse du rectangle blanc en impression.

Les cotes et l'ordre de collage sont dans [**la fiche de façade V15 révisée**](docs/FACADE_REFERENCE_PORTE_INTERPHONE_V15.md).

### Maintien du XIAO + LoRa par deux clips latéraux

La pile des deux cartes repose au-dessus du faux plafond. Deux languettes verticales souples sont **imprimées sur le plateau**, de part et d'autre de la carte **Wio-SX1262**, au niveau Y64,2–68 mm. Les lèvres, à Z58,65–59,05, retiennent délicatement la carte du bas sans appuyer sur les composants du XIAO au-dessus. Les points d'appui sont calculés à partir des volumes des **STEP de référence** et prévoient une retenue latérale nominale d'environ **0,30 mm de chaque côté**.

**Imprimer le faux plafond en PETG** pour la souplesse des languettes et engager le module sans forcer. La géométrie reste un **prototype : les contours réels, les composants saillants, l'antenne et la résistance à la fatigue doivent être vérifiés à blanc**. Les deux trous de sangle originaux sont conservés comme fixation alternative sans serrer les composants.

### Goulotte fermée, fils droits

La **goulotte intérieure du mur arrière** va de **Z14 à Z43**, avec un canal de **7,2 mm de largeur**. Ses trois retenues précédentes disposées en quinconce sont supprimées : plus besoin de contourner des obstacles. Les fils montent **verticalement** derrière un **couvercle indépendant de 7,9 × 1,1 × 27,8 mm**, glissé depuis le haut dans deux petites rainures latérales, **toit retiré**. Une prise en haut permet de retirer le couvercle ; les extrémités du canal restent libres pour faire entrer et sortir les fils. Le mur extérieur arrière reste plein, sauf le port USB-C.

La paroi n'est pas percée pour accéder aux combles. **Aucun collage du couvercle** : monter les fils, présenter la pièce, coulisser sans forcer. Vérifier que l'épaisseur cumulée des fils reste compatible avec la profondeur utile d'environ **2 mm derrière le couvercle**.

### LED blanche chaude : dimensions du PDF fourni

La fiche jointe porte la référence **GTG502WWC** et indique un **corps Ø5,0 mm**, une **collerette Ø5,9 mm**, une **tête de 8,6 mm**, une collerette d'épaisseur **1 mm maximum**, des pattes espacées de **2,54 mm**, de **29 ± 0,5 mm**. Électriquement, la fiche donne **3,0–3,4 V (3,2 V typique) à 20 mA** et **30 mA maximum en continu**.

L'ancien support LED sous plafond, toujours indépendant avec **2 ergots Ø2 / logements Ø2,6**, reçoit maintenant un **alésage Ø6,5 mm par dessous**. On insère la LED dôme vers le garage, **collerette contre une butée à Z45,2**, avec la pointe de la lentille vers Z36,6 ; les deux pattes traversent un **passage Ø4,4 mm** jusqu'au faux plafond. Une goutte de **silicone neutre compatible électronique au bord inférieur** immobilise la LED après essai, sans second élément imprimé ni appui sur la lentille.

**Attention à la référence :** la LED blanche initialement listée dans la nomenclature provient d'un assortiment **Whadda WCS101**. Le document fourni cote une **GTG502WWC** ; il n'est pas établi que les deux références soient strictement identiques. **Confirmer les cotes de la LED effectivement montée** avant d'imprimer le support définitif. Utiliser une résistance de limitation de courant adaptée au branchement réel, jamais la LED directement sur 5 V.

### Bornier SC02/2.54

Le schéma fourni donne un pas **2,54 mm**, une emprise de **6,5 mm en profondeur**, une hauteur de boîtier **8,5 mm**, des broches dépassant de **3,5 mm** et, pour la version **2 contacts**, une largeur calculée **5,48 mm** (formule `B = 2 × 2,54 + 0,4`). Il sera fixé au **petit circuit de distribution**, dont l'emplacement réel n'est pas défini : **aucun support de bornier fictif n'a été créé**.

## Servo et porte

L'entraxe des deux encoches d'oreilles du DMS-MG90 est **29 mm**, avec des pilotes Ø1,7 à **Z25,4 et Z54,4** ; la sortie se situe à 6 mm du bord de son boîtier. Le berceau conserve ses **deux goussets**, son dégagement de câble de 5 mm et ses **quatre** points de fixation à la base. Pour la porte, **le palonnier circulaire** est à privilégier, mais son diamètre, son entraxe et son épaisseur réelle restent inconnus : le disque de liaison **Ø12** est conservé **sans perçages présumés**.

## Électricité et fonctionnement

Un seul capteur magnétique **SAS308** indique la fermeture complète du garage réel. Contact ouvert : le récepteur lance immédiatement une ouverture décorative continue de **5 s de 90° à 0° (servo inversé, course de 90°)** dès réception de NON FERMÉ (état 2), sans attendre l'état 1 estimé après 40 s. La fermeture complète est également commandée en **5 s**. La LED orange clignote pendant le mouvement et reste fixe à l'ouverture ; la blanche s'allume à la fin de l'ouverture. L'ouverture réelle n'est pas mesurée. Seul le récepteur doit être reflashé pour cette évolution. Sans nouvelles trames pendant 150 s, la liaison est considérée périmée.

Alimentation : **USB-C 5 V / 2 A minimum** vers un **bus 5 V et GND commun en parallèle**, XIAO et servo ; condensateur **470 µF / 16 V** près du servo. Ne jamais alimenter le servo par la broche **3V3 du XIAO**. Firmware : **D6 servo, D7 LED blanche, D0 LED orange** ; angles servo configurés **90° fermé et 0° ouvert** (porte physique verticale 0°, horizontale 90°). Vérifier les butées et indexer le palonnier sans charge. Vérifier les résistances **5,1 kΩ CC1/GND et CC2/GND** de la platine USB-C avant assemblage.

Le nez de prise de la carte Gotronic 49067 et son câble mâle n'étant pas correctement cotés, l'ouverture de coque **10 × 4,2 mm reste provisoire**. Débrancher l'alimentation externe avant de connecter le XIAO à un ordinateur, à moins d'utiliser une isolation contrôlée. La miniature ne pilote pas la motorisation réelle.

## Impression, fichiers et validations

La CAO paramétrique `cad/generate_cad.py` génère **12 STL imprimables**, **15 STEP** (12 pièces + deux assemblages + un XIAO simplifié) et **4 coupons de contrôle**. La V15 révisée conserve les pièces **12** (porte) et **14** (rectangle blanc), la pièce **13** (interphone) étant supprimée ; le couvercle `11_couvercle_goulotte_arriere` est conservé. Les noms historiques « V2 » des STEP d'assemblage restent les mêmes, mais leur **contenu est V15**.

```bash
python cad/generate_cad.py
python cad/test_step_exports.py
python cad/test_repo_consistency.py
python cad/test_component_dimensions_sources.py
python cad/test_hardware_bom.py
```

Tests prévus : intégrité BREP, 12 STL étanches, 15 STEP, clips Wio vs référence Wio et XIAO, rails/couvercle sans intersections, LED Ø5/Ø5,9, couverture/toit avec rives, façade et porte basculante de 0 à 90°, compilation des deux firmwares. **Ces tests numériques ne prouvent pas l'ajustement mécanique réel**. **Tester** le montage à blanc du module XIAO/Wio, du couvercle et de la LED avant de finaliser l'impression. Faire un montage à blanc en PETG du faux plafond et de la goulotte.

[Conception mécanique héritée de V14](docs/FIXATIONS_COMBLES_GOULOTTE_LED_V14.md) · [README CAO V15](cad/README.md) · [Sources des cotes](cad/component_dimensions_sources_v7.json) · [Nomenclature dimensionnelle](cad/bom_dimensions_v1.json) · [BOM composants](cad/hardware_bom_v5.json) · [GitHub Actions](.github/workflows/cad-validation.yml).

**Ne pas connecter cette maquette au secteur 230 V, aux commandes du moteur de garage ou à un circuit de sécurité.**
