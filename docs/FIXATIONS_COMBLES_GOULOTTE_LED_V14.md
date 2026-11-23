# V14 — Clips XIAO/Wio, goulotte fermée et LED blanche

**23 novembre 2026 — unités : millimètres.** Le garage conserve la coque **105,6 × 85**, le vantail **55**, le faux plafond **100,2 × 25** et le toit **62 / 78**. Cette page décrit exclusivement les nouvelles interfaces de fixation V14 et les réserves de montage réel.

## 1. Deux clips pression latéraux sur le faux plafond

L'ensemble **XIAO nRF52840 + Wio SX1262** doit rester démontable, sans vis de PCB inventées. La carte Wio inférieure sert de retenue ; les deux anciens emplacements de sangle sont conservés.

| Repère CAO V14 | Valeur |
|---|---|
| Wio de référence, enveloppe STEP après rotation | X40,56..62,87 ; Y58,61..76,39 ; Z53,43..58,31 |
| XIAO de référence | X41,56..64,04 ; Y58,61..76,39 ; Z59,54..64,002 |
| Centre des clips | Y64,2..68,0 |
| Montant latéral gauche | X38,45..39,85 |
| Montant latéral droit | X63,75..65,15 |
| Section des montants | 1,4 mm selon X × 3,8 mm selon Y |
| Sommet des montants | Z59,20 |
| Lèvres intérieures | Z58,65..59,05 |
| Retenue prévue | environ 0,30 mm par côté |
| Clips / fentes anciennes | 2 clips ; 2 fentes de collier de secours ; 4 patins Wio |

La lèvre passe théoriquement **0,34 mm au-dessus de la face la plus haute de l'enveloppe Wio** et **0,49 mm en dessous de la face la plus basse de l'enveloppe XIAO** : pas de pression sur les composants du XIAO dans la modélisation. Les montants verticaux se déforment latéralement de manière contrôlée lors de l'insertion du module, selon un principe de **clip pression souple**.

**Impression : PETG recommandé**, assez de périmètres, ébarber sans affaiblir les montants. Enfoncer progressivement les côtés du Wio et confirmer que les languettes ne prennent appui ni sur une antenne, ni sur un composant SMD, ni sur le connecteur USB. La simulation avec BREP/STEP de référence n'est **pas un essai physique ni une certification de fatigue**. En cas de doute, utiliser les **deux passages de collier** avec une protection isolante souple et ne pas forcer les clips.

## 2. Goulotte arrière verticale fermée, sans virages

L'ancienne goulotte avait **trois retenues alternées**. La version actuelle les **supprime complètement** : le passage des fils est rectiligne, du bas vers le haut. L'arrière extérieur reste intact, hormis le petit trou USB-C bas.

**Corps solidaire de la coque :**
- deux rails X90..91,8 et X99..100,8, sur le mur intérieur arrière, **Y78,6..82,72**, **Z14..43**, séparés par **7,2 mm** ;
- sur leurs faces intérieures, deux petites **feuillures de 0,55 mm selon X** commencent à Y79,25 et s'étendent sur 1,50 mm de profondeur, depuis Z15 jusqu'au sommet Z43 ;
- chaque rail conserve **1,25 mm de matière en X** au niveau du logement, avec l'appui du mur arrière derrière.

**Couvercle indépendant :** `11_couvercle_goulotte_arriere`, **7,9 × 1,1 × 27,8 mm**, passe dans les feuillures avec **0,20 mm de jeu de chaque côté**. Il s'insère **par le haut (Z)**, toit démonté, et s'arrête contre la fin des rainures en bas, à **Z15**. Une petite prise en partie haute permet de le retirer sans colle. La bande recouvre les fils sur presque toute la longueur ; les entrées/sorties restent ouvertes pour le câblage, la ventilation et l'entretien.

La profondeur réellement utilisable entre le dos du couvercle et le mur blanc est **environ 2 mm**. Utiliser des fils souples suffisamment fins ; ne pas y contraindre une grosse fiche, une prise USB, une antenne coaxiale ou une courbure trop courte. Si le faisceau est plus épais, prévoir une variante de goulotte plus profonde **après mesure**. Ajuster les jeux de coulissement à l'imprimante ; ne pas poncer la façade extérieure.

## 3. LED blanche chaude GTG502WWC : montage par dessous

La fiche **Warm white LED.pdf** fournie par l'utilisateur décrit une **GTG502WWC**, pas explicitement la **Whadda WCS101** mentionnée dans l'ancienne nomenclature d'approvisionnement. Les dimensions ci-dessous viennent **de la fiche fournie** et ne prouvent pas que l'ampoule finalement reçue est identique.

| Cote source | Valeur |
|---|---|
| Corps | Ø5,0 |
| Collerette | Ø5,9 |
| Longueur lentille jusqu'à l'arrière de la collerette | 8,6 |
| Épaisseur collerette | 1,0 MAX |
| Entre-axes pattes | 2,54 |
| Longueur pattes | 29,0 ± 0,5 |
| Tension directe, sous 20 mA | 3,0–3,4 V (type 3,2 V) |
| Intensité directe maximale continue | 30 mA |

**Support imprimé 09 :** l'ancienne pièce `09_support_led_blanche` est conservée avec ses deux ergots Ø2 dans deux logements Ø2,6 sous le faux plafond. Elle reçoit une **cavité traversante Ø6,5 mm**, ouverte **par dessous**, permettant de présenter d'abord le dôme puis la collerette, jusqu'à une **butée Z45,2 mm**. La pointe du dôme doit se retrouver environ à **Z36,6 mm**. Au-dessus, l'épaulement autour d'un **passage de pattes Ø4,4 mm** arrête la collerette et laisse passer les deux connexions vers le plafond, dont le trou central est également Ø4,4.

Une **très petite goutte de silicone neutre compatible électronique**, appliquée près du bord inférieur du support, immobilise la diode après vérification de la polarité et de l'allumage. Ne pas coller la lentille, ni laisser les pattes non isolées toucher le support du Wio. Pas de nouvel objet à imprimer pour la LED.

La référence GTG502WWC est donnée pour **3,2 V typiques à 20 mA** : utiliser une **résistance adaptée et le circuit de commande prévu**, jamais un raccordement direct à 5 V.

## 4. Bornier SC02/2.54 : plan de référence joint

Le dessin de bornier permet de compléter les informations dimensionnelles du bornier **deux contacts** destiné à une carte de distribution séparée :

- pas des bornes **2,54 mm** ;
- hauteur de boîtier **8,5 mm**, pattes de soudure supplémentaires **3,5 mm** ;
- profondeur **6,5 mm** ;
- longueur générique **B=N×2,54+0,4 mm**, soit **5,48 mm pour N=2** ;
- entraxe de broches extrêmes **A=(N−1)×2,54 mm**, soit **2,54 mm pour N=2** ;
- fenêtre d'entrée du conducteur indiquée **1,4 × 1,5 mm**.

**Pas de fixation imprimée pour le bornier dans V14** : il reste prévu sur une plaquette de distribution dont les dimensions et la position ne sont pas définies ; un support précis serait inventé.

## 5. Pièces et méthode de vérification

Le générateur CadQuery produit **10 pièces STL**, **13 STEP** (10 pièces + 2 assemblages + référence XIAO simplifiée) et **4 coupons**. Le couvercle est la seule pièce imprimable supplémentaire ; le support LED blanc et le faux plafond sont modifiés, la coque comporte les rails sans chicanes. Le toit, la porte de 55 mm et les mécanismes du servo restent aux dimensions V13 mais le projet courant porte le nom **V14**.

Tests CI : contrôle des 4 BREP fournisseurs, maillages étanches et volumes positifs, pas de collision des deux clips avec le Wio/XIAO importés, marge LED réelle, jeu entre le couvercle et la coque, maintien d'un canal continu, contrôles servo/porte de 0° à 90° et compilation des deux firmwares.

**Toujours non mesurés :** palonnier du DMS-MG90, vraie taille/position du nez USB-C 49067, trajet de l'antenne/coaxial, géométrie effective des cartes reçues, matériau et tolérances de l'impression. Les deux languettes et le couvercle sont des **prototypes numériques** à essayer sans forcer.

[README V14](../README.md) · [README CAO](../cad/README.md) · [Source du générateur](../cad/generate_cad.py) · [BOM dimensionnelle](../cad/bom_dimensions_v1.json).
