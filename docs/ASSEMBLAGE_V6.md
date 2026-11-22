# Assemblage V6 — GarageStateClone : fixation, jeux et ordre de montage

**Version mécanique courante : V6, 22 novembre 2026.** Miniature à imprimer sur Bambu P1S. Le modèle est **contrôlé géométriquement**, mais le DMS-MG90 réellement livré, son palonnier, les connecteurs et les antennes n'ont pas encore été mesurés ni montés physiquement.

**Fichiers de référence :** [générateur paramétrique](../cad/generate_cad.py) · [BOM](BOM_V1_VERIFIEE.md) · [quincaillerie](QUINCAILLERIE_MONTAGE_V5.md) · [câblage](CABLAGE_V1_VERIFIE.md) · [tests](../cad/test_step_exports.py) · [audit](AUDIT_REPO_V6.md).

## Avis V8 (22 novembre 2026) : modifications à appliquer avant de suivre l'assemblage V6

Ce guide V6 décrit l'assemblage historique et conserve son contenu, **mais deux éléments sont remplacés par des versions plus récentes** :

- **Servo** : le crochet du berceau V6 a été supprimé en V7 ; deux vis au pas de **29 mm** et un positionnement constructeur **16,00 mm fond→dessous oreille avec jeu 0,30 mm** sont décrits dans [FIXATIONS_SERVO_V7.md](FIXATIONS_SERVO_V7.md). **Ne pas essayer de remonter un clip V6 absent du STEP actuel.**
- **USB-C V8** : l'ancienne fente arrière basse 12 × 8 mm de passage de câble est remplacée par une fenêtre **13 × 8 mm** ; la platine **Gotronic 49067** repose sur un **support monobloc du socle noir** avec deux tunnels de colliers. Une seule alimentation **USB 5 V / 2 A** arrive à la 49067, se distribue en parallèle vers XIAO et servo. La carte USB et le profil exact de son connecteur ne sont qu'une enveloppe CAO approximative. Voir [ALIMENTATION_USB_C_V8.md](ALIMENTATION_USB_C_V8.md) avant impression.

Les **8 pièces STL** restent au même nombre, les STEP historiques `GarageStateClone_V2_...` étant régénérés à partir de l'**état V8 actuel**. Réimporter les STEP dans Onshape pour voir le support arrière. Les anciennes instructions V6 de câblage du servo et du crochet ne remplacent pas les documents V7/V8.

## 1. Implantation V6 et huit pièces imprimables

Axes : X gauche→droite, Y façade→arrière, Z bas→haut, unités en millimètres. Les STL sont **dans le repère d'assemblage** : les orienter sur le plateau de la P1S avant impression.

| Pièce | Interface dessinée | Montage |
|---|---|---|
| 01 coque blanche | **150 × 100 mm**, toiture avant/arrière **62 / 78 mm** ; murs 2,4 mm | Se place sur les rails du socle, jeu nominal 0,30 mm par face ; 4 anneaux de guidage de câbles ajoutés aux parois |
| 02 socle noir | Solide de 3 mm, 4 trous traversants **Ø2,3 mm** avec fraisures nominales **Ø4,2 mm** | Fixer **par-dessous** les pieds du berceau à l'aide de quatre vis M2 adaptées, testées sur coupon |
| 03 toit noir | Mono-pente **16 mm sur 100 mm** (≈9,1°), épaisseur 3 mm | Jupe démontable, sans vis imposée |
| 04 porte noire | Baie décentrée 100 × 42 ; panneau **99,4 × 41,4 × 2,4 mm** ; axe gauche imprimé Ø3,2 | Dans palier gauche Ø3,8 ; disque Ø12 à droite servant de **face vierge** pour le vrai palonnier servo |
| 05 palier gauche | Largeur 5 ; assise Z34,4 ajoutée dans la coque | Prend appui sur une petite tablette imprimée ; coller seulement après essai d'alignement. **Pas encore vissé** |
| 06 berceau servo | Quatre **pieds 6 × 6 × 5,5**, pilotes **Ø1,7**, crochet supérieur intégré | **Quatre M2 à tête fraisée candidates**, depuis le dessous. Crochet de retenue à tester sur le vrai servo |
| 07 faux plafond | **144,6 × 40 × 2,4**, Y55–95 et Z46–48,4 | Appuis intégrés ; **4 plots 4 × 3 × 3,2** sous le Wio ; **2 fentes 3,2 × 4,2** pour un lien isolé |
| 09 support LED blanche | LED désormais **X75 / Y65**, dégagée de la nervure qui la traversait en V5 | Deux **ergots Ø2** dans **deux trous Ø2,6**, faces affleurantes, zéro pénétration solide ; point de colle facultatif |

**Les 8 STL du garage** sont inchangés en nombre. Trois STL *éprouvettes* supplémentaires sont produits dans le dossier **cad/coupons**, et ne sont pas des pièces de l'assemblage.

## 2. Jeux calculés, pas tolérances garanties par l'imprimante

| Emboîtement | Mâle / femelle | Jeu ciblé |
|---|---|---|
| Porte / ouverture | 99,4 / 100 | **0,30 mm de chaque côté** |
| Tourillon gauche / palier | Ø3,2 / Ø3,8 | **0,30 mm radial** |
| Disque porte dans retour droit | Ø12 / Ø12,6 | **0,30 mm radial** |
| Ergots LED / trous plafond | Ø2 / Ø2,6 | **0,30 mm radial** |
| Faux plafond entre murs | 144,6 / 145,2 | **0,30 mm par côté** |
| Pieds du berceau | Pilotes Ø1,7 / trous de passage Ø2,3 | **Filetage dans plastique à tester sur coupon**, pas un ajustement glissant |
| Wio sur quatre supports | Plots jusqu'à Z51,6 / bas Wio STEP à Z51,9 | **0,30 mm avant sanglage** |
| Corps servo / support imprimé | Enveloppe modèle STEP + marge | **0,30 mm nominal** ; crochet destiné à retenir après montage |
| Lentilles des deux LED | Poche de service imprimée Ø6,6 | **Cote provisoire**, collerette réelle inconnue |

Les parois structurelles font **2,4 mm**, au-dessus des **2 mm** demandés. Les passe-câbles imprimés font **Ø8 extérieur / Ø3,4 intérieur**, soit **2,3 mm d'épaisseur radiale**. Les ergots et les rainures sont des détails locaux, pas des parois porteuses.

**Imprimer et essayer d'abord les éprouvettes** A (axe Ø3,2 contre trous Ø3,6 / Ø3,8 / Ø4,0), B (pilotes M2 Ø1,6 / Ø1,7 / Ø1,8) et C (disque palonnier vierge Ø12). Même sur la P1S, le retrait, l'orientation, le matériau et le premier cordon peuvent modifier les jeux.

## 3. Charnière et liaison servo/porte

La porte est un vantail monobloc rigide, dont les rainures *imitent* une porte sectionnelle. Elle pivote vers l'intérieur autour de X, sur **Y=9,5 / Z=45,4**. Le servo est à l'**avant droit** sur le même axe.

1. Insérer le tourillon gauche **Ø3,2** dans le palier **Ø3,8** ; vérifier que le palier repose sur la nouvelle tablette, sans frottement de la porte contre la coque.
2. Vérifier à la main le débattement **0° → 90°** sans brancher le servo. Le disque imprimé de la porte côté droit est **Ø12**, et la partie supérieure du retour droit comporte un passage **Ø12,6** ; le mur extérieur n'est pas évidé.
3. Le disque vierge se termine à **X111,5**. Dans le STEP du MG90-A fourni, la pointe de sortie du servo est à **X113,7**, soit **2,2 mm d'espace axial théorique**. Cela n'inclut **pas** le palonnier réellement monté.
4. Monter sur le moteur le **palonnier d'origine livré**, le fixer avec **sa vis centrale**, mesurer **son épaisseur en saillie et son entraxe**. Utiliser l'éprouvette C pour reporter les perçages et la position réellement compatibles, puis adapter le disque de la porte si besoin.
5. **Ne pas forcer si le palonnier déborde dans le retour droit.** Modéliser son empreinte et ses fixations avant de percer la porte définitive. Ne jamais employer une simple liaison par frottement ou un collage direct sur l'axe cannelé.
6. Après une fixation positive démontrée, calibrer les consignes logicielles. Le firmware actuel commande **15° fermé → 95° ouvert estimé**, soit **80° de déplacement servo**, pas 90°. La CAO a été vérifiée sur un débattement de réserve de 90°, sans prétendre que le vrai servo atteindra cette butée.

**État réel :** la V6 modélise le **côté porte et un gabarit Ø12**, mais le **côté palonnier demeure volontairement NON percé**. Le modèle MG90-A n'est pas une preuve de compatibilité avec le DMS-MG90 réel. Ce point reste une étape obligatoire avant de pouvoir annoncer « prêt à assembler ».

## 4. Fixer le berceau et retenir le servo

La V5 utilisait quatre colonnes posées. En V6, le berceau possède quatre **pieds de 6 × 6 × 5,5 mm**, en continuité avec les colonnes, avec des pilotes **Ø1,7**. Les quatre passages du socle **Ø2,3** sont coaxiaux ; une fraisure conique Ø4,2 permet d'essayer une tête fraisée M2 sans dépasser sous le socle.

1. Tester la vraie vis **M2×8** sur l'éprouvette B, idéalement avec un tournevis manuel. Ne pas forcer si elle fend le pilote ou si la tête dépasse ; changer le pilote ou le type de vis.
2. Fixer les **quatre pieds depuis le dessous** du socle, en serrant progressivement. Ce montage n'exige pas d'insert métallique M3.
3. Insérer le vrai servo sous le **crochet arrière supérieur intégré**. Ce crochet a un petit recouvrement d'environ **0,8 mm** et reste un **prototype de clip élastique** à tester en PLA/PETG : il doit pouvoir se déformer sans blanchiment ni rupture.
4. Vérifier le dégagement entre crochet, moteur et toit fermé avant de fixer le palonnier. Retirer le moteur en soulevant doucement la languette sans appuyer sur l'axe.

La CAO ne prouve ni résistance à la fatigue du crochet, ni force de maintien, ni compatibilité des vraies oreilles de servo. Une fixation mécanique supplémentaire peut être nécessaire si la retenue est insuffisante.

## 5. Maintien de l'électronique dans les combles

Le Wio/XIAO est situé autour de **Z51,9–64,0**. À l'avant de son enveloppe, la pente du toit donne environ **6,2 mm de garde**, **hors USB, antenne, câble coaxial et rayon de courbure**. **Ne pas acheter d'entretoise universelle de 10 mm.**

- Les **quatre plots bas** (haut Z51,6) servent de support d'essai, avec 0,30 mm de marge sous l'enveloppe Wio du STEP. Les trous exacts du PCB n'étant pas certifiés, aucune vis n'est prévue directement dans la carte.
- Les **deux fentes de 3,2 × 4,2 mm** permettent de passer **un lien nylon 2,5 mm** ou une petite sangle isolante par le dessous du faux plafond et sur la carte, **avec protection souple non conductrice**. Ne jamais serrer sur un composant SMD, un bouton, l'antenne, la prise USB ou les broches.
- Le **faux plafond lui-même est amovible** et repose sur ses deux consoles moulées ; il ne nécessite pas de vis par défaut.
- La LED blanche, déplacée à **Y65** pour éviter la nervure avant, possède **deux petits ergots Ø2** s'insérant dans **deux trous Ø2,6** de part et d'autre du passage central des fils Ø2,4. Les surfaces d'appui sont affleurantes. Un point de colle isolante peut assurer la retenue.
- Faire un essai **toit fermé et alimentation branchée** : le gabarit CAO ne tient pas compte de l'antenne 868 MHz ni du câble USB-C réel.

## 6. Passe-câbles et alimentation

La coque possède maintenant **quatre petits œillets intégrés** à X≈5,4 / X≈144,6 et Y=35 / Y=73, à Z=12. Ils guident les fils **basse tension** le long des parois, **hors du volume balayé de la porte**. Deux ouvertures arrière sont prévues : **12 × 8 mm en bas et 16 × 9 mm en haut**. Ni l'une ni l'autre ne constitue un presse-étoupe certifié : prévoir isolation et **décharge de traction**.

L'émetteur de la vraie porte n'utilise qu'**un SAS308** confirmant **FERMÉ**. Le récepteur alimente le servo en **5 V externe**, avec **masse commune** au XIAO (jamais à partir de sa broche 3V3) ; condensateur **470 µF** près du servo, BC547B pour LED blanche. D6 commande le servo ; D7 la LED blanche via transistor ; D0 la LED orange en absorption de courant. Voir la [netlist](CABLAGE_V1_VERIFIE.md).

**Côté vraie porte**, pas de connexion à la motorisation ni de perçage de rails/galets ou dispositifs de sécurité. Un boîtier isolant pour l'émetteur et des supports sans danger pour le capteur/aimant restent à réaliser.

## 7. Ordre recommandé d'impression et de mise en service

1. Imprimer et mesurer les **3 éprouvettes**, dans le matériau et l'orientation envisagés. Pour la P1S, commencer par 0,20 mm de couche et **4 périmètres** pour les pièces mécaniques ; ajuster après inspection. Le matériau et les températures ne sont pas imposés par la CAO.
2. Orienter chaque STL dans le slicer **sur le plateau**. Les STL proviennent des coordonnées assemblées, pas d'un plan d'impression préorienté ; prévoir des supports si nécessaire pour la charnière et le crochet.
3. Assembler **socle / coque / palier / porte sans moteur**, tourner librement de 0 à 90° et mesurer les jeux ; coller le palier uniquement après validation.
4. Fixer le berceau et essayer le **servo sans porte**, vérifier la tenue du crochet, la polarité 5 V et l'absence d'effort contre le toit.
5. Mesurer puis adapter le **vrai palonnier**, fixer le disque de porte et recontrôler le mouvement à la main avant de commander le servo.
6. Installer sous toiture l'électronique retenue et isolée, la LED sur ses deux ergots, l'antenne 868 MHz. Fixer tous les fils dans les œillets et tester la fermeture du toit sans pincement.
7. Faire les tests radio/LED avec le vrai capteur : délai de 40 s **estimé** sans aimant, perte radio après >150 s et reprise après coupure.

## 8. Ce qui reste à valider sur le matériel réel

- [ ] **Palonnier réel** mesuré et fixé positivement au disque de porte ; vis centrale accessible ; aucun collage sur l'axe cannelé.
- [ ] Les **4 vis** ne fendent pas les pieds imprimés, affleurent sous le socle et résistent à plusieurs déposes.
- [ ] Le **crochet du berceau** maintient le vrai servo sans fatigue ni collision avec le toit.
- [ ] Le palier gauche reste retenu, libre et coaxial après collage.
- [ ] Le Wio/XIAO ne subit **aucune pression sur les composants ni les connecteurs**, l'antenne et l'USB n'entrent pas en conflit avec le toit.
- [ ] Les deux LED se fixent sans percer ni forcer les collerettes ; câbles isolés, anti-traction.
- [ ] Le capteur et l'aimant de la vraie porte ne gênent aucune pièce mobile ; boîtier protecteur XIAO émetteur réalisé.

**La V6 est un prototype mécanique nettement plus abouti, pas une validation « prêt à offrir » tant que ces points physiques ne sont pas cochés.**
