# Fixations et interface servo — V7 (22 novembre 2026)

**Statut : CAO prototype documentée, pas montage physique qualifié.** Cotes en millimètres.

## 1. Deux ensembles de vis distincts

| Liaison | Quantité | Entraxe | Axe des vis | Cotes dans le modèle | Statut |
|---|---:|---:|---|---|---|
| **Servo DMS-MG90 → son berceau** | **2** | **29,0 mm sur l'axe Z de la miniature** | Selon **X** (parallèle à la sortie du servo) | Encoches **ouvertes Ø2,0 mm** fabricant ; pilotes imprimés **Ø1,7**, bosses **Ø5,8** (paroi radiale nominale **2,05**) | Entraxe/encoches : **plan constructeur** ; pilotes/position axiale : **essai CAO** |
| **Berceau imprimé → socle noir** | **4** | Plan d'implantation *CAD*, **aucun lien avec les 29 mm** | Selon **Z**, vissage par dessous | 4 passages socle Ø2,3, fraisures d'essai Ø4,2, pieds 6×6×5,5 à pilotes Ø1,7, candidat M2×8 | **Imprimable à calibrer** |
| **Axe servo → porte** | Palonnier fourni | **Inconnu** | Selon **X** | Disque porte Ø12 **sans trou de palonnier**, passage Ø12,6 ; écart de 2,2 mm avec pointe d'axe du STEP | **À mesurer avant entraînement** |
| **XIAO + Wio → faux plafond** | Une bride souple | **Aucun entraxe de vis constructeur garanti** | Bride, pas de perçage PCB | Deux fentes de bride 3,2×4,2 et quatre plots bas isolés | Montage à blanc indispensable |
| **LED blanche → faux plafond** | 2 ergots imprimés | **13,0 mm de projet** | Selon Z | Deux ergots Ø2 dans deux trous Ø2,6 | **Cotes de conception**, pas fabricant |
| **SAS308 / aimant → vraie porte** | Selon support | **Non documenté pour les deux éléments** | Dépend du lieu | **Ne pas choisir arbitrairement un entraxe de capteur** | Relevé sur les pièces obligatoires |

**Plan constructeur servo :** [Gotronic DMS-MG90 SER0039, 3 vues](https://www.gotronic.fr/pj2-dimensions-dms-mg90-36923-2320.pdf). Les 2 lumières en « C » sont cotées **Ø2** et leur distance entre centres est **29 mm**. Leur entrée est ouverte vers l'extérieur de chaque oreille : ce **ne sont pas des trous traversants fermés**. La force de maintien et la taille de la tête/éventuelle rondelle de la vis doivent être vérifiées.

## 2. Erreur d'axes V6 corrigée

**Erratum important** : la note de collecte V7 antérieure avançait 0,05 mm de jeu en comparant **33 mm constructeur** à **32,5 mm STEP** : cette comparaison mélangeait deux axes.

Une fois le STEP générique **MG90-A** orienté avec l'axe moteur parallèle à **X**, le rapprochement correct est :

| Direction miniature | Plan DMS-MG90 | Ancien STEP générique | Commentaire |
|---|---:|---:|---|
| **X** — sortie d'arbre (hauteur fabricant) | **30,0** | **32,5** | STEP déborde de 2,5 mm, utile comme réserve conservative |
| **Y** — épaisseur | **12,0** | **12,221** | STEP déborde de 0,221 mm |
| **Z** — longueur avec oreilles | **33,0** | **33,4** | STEP déborde de 0,4 mm |

Le berceau conserve l'enveloppe conservatrice du STEP en attendant le relevé réel, mais les **deux pilotes de fixation sont maintenant espacés de 29 mm** sur Z, indépendamment des quatre pieds vissés au socle. Le crochet haut élastique fragile de V6 est remplacé par une **colonne extérieure et deux points de fixation vissés** près des oreilles.

La **profondeur de retenue dans l'axe X**, la géométrie des oreilles et le type exact de vis restent à valider physiquement ; le modèle source MG90-A ne prouve pas l'emboîtement du vrai SER0039. Les nouvelles vis ne doivent pas forcer dans les encoches et ne doivent pas contraindre la sortie cannelée.

## 3. Ordre de montage recommandé

1. Imprimer seulement le **support servo V7** et le **coupon de vis M2** de `cad/generate_fit_coupons.py`. Vérifier que les deux encoches du **vrai SER0039** se présentent face aux deux pilotes à 29 mm. Si la hauteur axiale des oreilles/les têtes de vis diffèrent, modifier uniquement `SERVO_LUG_BOSS_X_FROM_SHAFT_TIP` et/ou la longueur/filetage des pilotes, puis relancer les tests.
2. Fixer le **berceau au socle** par **quatre vis distinctes**, après test de la prise dans les quatre pieds imprimés. Les quatre positions ne constituent **pas** un entraxe constructeur.
3. Présenter la porte et son palier Ø3,8 face au tourillon Ø3,2. Vérifier le balayage sans collision, toit en place.
4. **Ne pas motoriser** avant d'avoir mesuré le palonnier du lot, choisi une liaison mécanique positive démontable entre palonnier et disque Ø12, et calibré les deux angles firmware à vide puis en charge. Éviter toute fixation par collage de l'arbre.
5. Dans les combles, conserver la sangle isolante de l'ensemble XIAO/Wio : la carte XIAO n'a **pas de trous de vis de montage identifiés** qui justifient un entraxe inventé. Contrôler USB, IPEX, coaxial, décharge de traction, faux plafond et toit réel.
6. Pour le **SAS308**, mesurer séparément les points de fixation du contact et de l'aimant avant de concevoir les attaches sur la vraie porte. Ne pas percer les rails, ressorts, galets, ni les éléments de sécurité.

## 4. Tests automatisés et limites

`cad/test_step_exports.py` vérifie la distance de **29 mm**, l'absence de matière dans les deux pilotes, le volume de référence tiers, les collisions avec les 8 pièces, les jeux charnières et le balayage de porte. `cad/test_component_dimensions_sources.py` contrôle les correspondances entre le plan, la BOM, et les axes géométriques. La CI contrôle en outre l'étanchéité des STL et la réimportation des STEP.

**Ni les tests numériques ni ce plan constructeur ne permettent de garantir le type/longueur des vis fournies, la flexion du support imprimé ou la compatibilité du palonnier.** Ces mesures sont explicitement ouvertes avant production finale.

[Source CadQuery](../cad/generate_cad.py) · [Catalogue source des cotes](../cad/component_dimensions_sources_v7.json) · [Plans cotés](FICHES_COTEES_COMPOSANTS_V7.md) · [BOM V6 historique](BOM_V6.md).
