# Support du DMS-MG90 et palonniers : révision CAO V13

**23 novembre 2026 — fondé sur** le fichier `DMS-MG90 Servo Dimension.pdf` et la photographie des accessoires fournis dans la conversation. Axes de la miniature : X dans l'axe de l'arbre du servo, Y vers l'arrière du garage, Z vertical.

## Cotes du plan fabricant reçues

| Cote du dessin | Valeur | Usage V13 |
|---|---:|---|
| Envergure totale **des oreilles** | **33 mm** | Enveloppe longitudinale selon Z |
| Entraxe des deux encoches ouvertes | **29 mm** | Position des 2 vis d'oreilles |
| Ouverture des encoches | **Ø2 mm** | 2 vis de fixation à vérifier |
| Longueur du boîtier proprement dit | **23 mm** | Centre du boîtier dans les oreilles |
| Largeur du servo | **12 mm** | Encombrement suivant Y |
| Axe du moteur depuis le bord proche du boîtier | **6 mm** | Référence de l'axe réel, et non centre de la bbox STEP |
| Fonctions circulaires autour de l'arbre | **Ø3 et Ø5 mm** | Formes du dessin, pas les cannelures du palonnier |
| Bas du servo → dessous des oreilles | **16 mm** | Plan de contact des deux bossages |
| Bas → marche supérieure | **22,5 mm** | Enveloppe haute constructeur |
| Bas → niveau capot | **26,5 mm** | Enveloppe haute constructeur |
| Bas → sommet de l'arbre | **30 mm** | Repère longitudinal X de l'arbre |

Le boîtier étant représenté centré entre les deux oreilles, sa marge à chaque bout est `(33 − 23)/2 = 5 mm`. La distance entre l'extrémité de l'oreille **proche** et l'arbre devient `5 + 6 = 11 mm`. Chaque centre d'encoche est distant de **2 mm** de l'extrémité de l'envergure 33 mm. Avec le centre de pivot CAO **Z45,4**, les vis doivent être situées à **Z25,4 et Z54,4** : **29,0 mm d'entraxe**. Le plan sous les oreilles est nominalement à `X = bout d'arbre + 14,0 mm`, la face imprimée de retenue à **X + 14,3 mm** laissant **0,30 mm de montage**.

## Nouvelle géométrie du berceau imprimé

La pièce imprimable reste **`06_support_servo_step_0p3mm_PROTOTYPE`**. Aucune cote du palonnier ou vis non mesurée ne devient un perçage supposé exact.

1. **Deux bossages de fixation d'oreilles**, Ø5,8 mm autour de pilotes Ø1,7 mm, repositionnés par les cotes officielles à **Z25,4 et Z54,4** (et non par le centre de la STEP générique MG90-A). L'entrée de chaque pilote reçoit un petit **chanfrein conique de Ø2,3 mm sur 0,45 mm** pour faciliter le départ de vis. Le corps du trou reste Ø1,7 sur le reste du bossage ; l'entraxe reste 29 mm.
2. **Colonne extérieure rigidifiée par deux goussets triangulaires** (épaisseur 1,8 mm dans X) du côté extérieur du servo. Ces renforts reprennent les efforts des oreilles sans clip fragile sur le corps du moteur. Ils restent à l'arrière du plan de contact et préservent l'accès aux deux vis.
3. **Fenêtre de sortie des trois fils de servo**, ouverte sur le dessus de la bordure arrière du berceau, de **5 mm de largeur selon X**. La base de cette bordure garde **2,4 mm de matière** ; la fenêtre est un espace de service, car le départ du câble n'est pas coté sur le PDF fabricant.
4. **Quatre pieds au socle**, pilotes Ø1,7 / traversées Ø2,3 et fraisages prévus au socle, **inchangés** ; les deux vis aux oreilles sont distinctes des quatre vis au socle. Aucun diamètre réel de tête ou longueur sous tête n'est revendiqué.

Le gabarit électronique du servo qui apparaît dans le STEP d'assemblage est une **référence générique MG90-A** plus volumineuse que le modèle officiellement coté. Ses BREP restent inchangés : ils servent seulement de contrôle conservateur des enveloppes, pas de substitut au vrai fabricant.

## Palonniers photographiés et liaison de porte

La photo montre les palonniers **disque circulaire**, **croix quatre branches**, **bras double** et **bras simple**, plus **trois petites vis**. Pour la porte monobloc de **55 mm**, le **disque rond** est la meilleure hypothèse de liaison symétrique, puisque son périmètre et plusieurs trous pourraient répartir le couple. Ce n'est encore **pas une fixation dimensionnée**.

**Manquent pour fixer la porte de façon sûre :** diamètre réel du disque rond, épaisseur totale une fois monté sur les cannelures, entraxe exact de deux trous opposés, diamètre des trous, hauteur du moyeu, diamètre et longueur sous tête de la vis centrale et longueur des petites vis fournies. Le dessin constructeur indique Ø3/Ø5 pour des fonctions circulaires de l'axe, **pas une denture ou des filetages certifiés**.

En attendant, la porte conserve son **disque Ø12 mm vierge**, le passage de montant **Ø12,6 mm** et le jeu nominal d'accouplement. **Ne pas imprimer un palonnier prétendu compatible, percer à l'aveugle ou coller le disque plastique sur l'arbre cranté.** Pré-monter le palonnier sur le vrai servo, puis mesurer sa face utile et prévoir la fixation de la porte, de préférence avec deux petites vis dans un adaptateur mesuré.

## Coupon supplémentaire avant impression du berceau

Le dossier `cad/coupons/` contient désormais **4 coupons** (3 existants + **`D_DMS_MG90_oreilles_entraxe29_pilotes_D1p7.stl`**). Le quatrième est un échantillon mince à **deux pilotes Ø1,7 mm espacés de 29 mm**, avec une entrée de guidage conique Ø2,3 sur 0,45 mm.

Essai : poser les oreilles du vrai DMS-MG90 sur le coupon, vérifier la position des encoches, essayer **sans forcer** deux des vis fournies et vérifier qu'elles prennent les pilotes sans fissuration. Les tolérances FDM et l'épaisseur des oreilles restent à mesurer physiquement. Le coupon ne remplace ni la fixation finale au socle ni un essai de force de l'ensemble.

## Assemblage et vérifications

Version courante **V13** : largeur/profondeur coque **105,6 × 85 mm** ; porte **55 mm** ; profondeur du faux plafond **25 mm**, LED orange sous palier gauche, USB-C 49067 derrière à travers un trou provisoire. Toutes les pièces du garage restent au nombre de **9 STL et 12 STEP** ; seuls les coupons passent de 3 à **4**.

Les tests CAO contrôlent l'écart des vis, la source du repère X/Z, la géométrie des goussets, la fenêtre de câblage, les pilotes et leur entrée conique, les interférences avec le modèle de référence, la coque, la porte 0–90°, les exports maillés et la nomenclature.

Il faut toujours faire un **montage à blanc** du servo, du palonnier et de ses vis avant de considérer le berceau imprimable comme définitif.

[README actuel](../README.md) · [README CAO](../cad/README.md) · [Code source CadQuery](../cad/generate_cad.py) · [BOM dimensionnelle](../cad/bom_dimensions_v1.json).
