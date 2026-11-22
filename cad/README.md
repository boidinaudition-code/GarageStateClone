# GarageStateClone — maquette CAO V2 avec STEP de composants fournis

## Statut et limites

**V2 de conception**, modèle CAD paramétrique CadQuery, non validé sur matériel réel.

- Les 4 modèles 3D fournis par l'utilisateur ont été importés comme **solides STEP originaux** (servo DMS-MG90-A, XIAO nRF52840, Wio-SX1262 for XIAO, BC547B). Le dépôt contient désormais **les géométries BREP compressées sans perte** dans `refs/*.brep.z.b64`, que le générateur décompresse automatiquement. L'archive complète livrée dans la conversation contient en plus les `refs/*.step` d'origine et l'assemblage STEP.
- Le servo, le Wio/XIAO et le BC547B sont des **références non imprimables** ; seuls les STL du dossier `stl/` sont destinés à l'impression.
- Le modèle 3D du servo **MG90-A** fourni n'est pas une attestation de conformité dimensionnelle avec le produit **DMS-MG90** acheté. Vérifier physiquement avant de percer ou visser.
- La **liaison palonnier/axe de porte**, les **trous de vis servo**, la fixation exacte des cartes par connecteurs et l'antenne demandent encore une prise de cotes sur le matériel réel.
- Onshape : depuis l'erreur **« contains faults » sur le XIAO détaillé**, utiliser la nouvelle **référence XIAO simplifiée à un seul solide**. Elle conserve l'enveloppe totale sans les petits composants et **ne permet pas de concevoir des trous de fixation précis**. Voir [procédure d'import](../docs/ONSHAPE_IMPORT_XIAO.md). Le modèle BREP d'origine reste complet. `generate_cad.py` reste le source paramétrique des pièces imprimées (pas de FeatureScript natif).

## Changements par rapport à V1

Le servo complet (pattes comprises) montre une enveloppe hors tout de **33,40 × 32,50 × 12,22 mm** dans le repère de son STEP. La coque actuelle est **150 × 100 mm** avec porte décentrée vers la gauche pour garder le moteur **dans le montant avant droit**, coaxial à la charnière haute de la porte. Le servo est orienté de côté pour réduire l'emprise devant la façade, et le volet continue de **se rabattre à l'intérieur**.

Le XIAO et le Wio sont représentés avec leurs géométries 3D **dans les combles arrière, au-dessus du faux plafond amovible**, sans intersection avec coque, toit ou plateau. Leur empilage est **aligné approximativement** selon les trous de fixation des deux STEP et reste à contrôler après montage.

## Paramètres CAO

| Paramètre | V2 |
|---|---:|
| Largeur × profondeur | **150 × 100 mm** (inchangé en V5) |
| Hauteur avant / arrière | **62 / 78 mm** |
| Pente de toit | **16 mm** sur 100 mm (≈9,1°) |
| Parois principales | **2,4 mm** |
| Toit / socle | **3 mm** |
| Largeur baie / hauteur | **100 × 42 mm** |
| Vantail | **99,4 × 41,4 × 2,4 mm** |
| Jeu d'emboîtement | **0,30 mm par face**, donc +0,60 mm sur largeur/diamètre intérieur |
| Axe porte / alésage palier | **Ø 3,2 / Ø 3,8 mm** |
| Centre axe porte (repère CAO) | Y = **9,5 mm**, Z = **45,4 mm** |
| Servo STEP, gabarit dans l'assemblage | X **113,7–146,2**, Y **3,4–15,62**, Z **23,3–56,7 mm** |
| LED blanche sous faux plafond arrière | Y = **61,5 mm** (X=75, hauteur du support Z=36,2–46,2) |
| LED orange en façade | **Ouverture optique Ø 2,0 mm**, LED Ø5 mm masquée dans une poche Ø6,6 mm, retrait **3,4 mm** |

### Modules STEP relevés (avant mise en place, hors antennes/câbles)

| Objet | Enveloppe de son STEP | Corps réels / accessoires |
|---|---|---|
| Servo **Mg90.STEP** | **33,40 × 32,50 × 12,22 mm** | Pattes et axe présents ; palonnier non garanti |
| **XIAO-nRF52840 v3.step** | **22,482 × 4,46 × 17,78 mm** dans le repère d'origine | Carte et USB inclus, hors fils |
| **Wio-SX1262 ... V2.step** | **17,78 × 22,316 × 7,642 mm** | Modules et connecteurs, hors antenne externe |
| **BC547-B.step** | **4,08 × 3,05 × 12,8 mm** | Pattes incluses dans le modèle |

Consulter `qa_report_v2.json` (historique) puis `qa_report_runtime.json` généré : les géométries de servo et de supports n'ont **pas d'intersection** dans le modèle, les huit STL sont des volumes fermés. Le contact numérique XIAO/Wio comporte une très petite intersection d'environ **0,013 mm³**, compatible avec une approximation de placement mais **à valider avec l'empilage physique**.

## Imprimer et assembler

- Couleurs : **blanc** coque, **noir** toit/socle/porte ; **pas de liseré bleu**. LED orange discrète.
- Ne pas imprimer les pièces dont le nom commence par `REF_` ; **ne jamais imprimer l'assemblage STEP** comme s'il s'agissait d'une seule pièce.
- `06_support_servo_step_0p3mm_PROTOTYPE.stl` est une **première selle** avec garde de 0,30 mm autour de la boîte du servo, mais ses trous de fixation restent à concevoir et l'assemblage doit être sécurisé mécaniquement.
- Les pieds du support reposent au niveau du dessus du socle ; une liaison par vis ou collage est nécessaire après tests.
- Tester d'abord **à vide et sans porte** ; vérifier le palier et la course de 0 à 90° avec la porte avant de refermer le toit.

## Reproduction

```sh
python -m pip install cadquery trimesh
python import_vendor_archives.py chemin/vers/les-archives-zip
python generate_cad.py
python qa_geometry.py
```

Les STEP d'origine sont disponibles dans le ZIP complet, sous `refs/`. **Un clone GitHub du dépôt peut générer la même géométrie sans ces STEP**, grâce aux quatre `refs/*.brep.z.b64` versionnés. Les quatre ZIP de téléchargement originaux peuvent aussi être convertis via `import_vendor_archives.py`. Les fichiers sources `generate_cad.py`, `qa_geometry.py`, `import_vendor_archives.py` et `vendor_models/manifest.json` sont conçus pour être versionnés dans GitHub.

**Sur le vrai garage :** un **seul SAS308** (non inclus dans la miniature) détecte la **fermeture confirmée**. L'ouverture demeure une **estimation décorative** après 40 secondes sans aimant, selon la configuration actuelle du firmware, et ne doit pas être utilisée pour la sécurité du bâtiment.
## Depuis la réparation du générateur (2026-11-22)

Le merge précédent avait supprimé les définitions de certaines constantes LED et le registre `PRINTABLE`. Les quatre références BREP sont intactes ; **aucun STEP source utilisateur n'a dû être recréé de façon approximative**.

- Cotes V4 : coque **150 × 100**, baie **100 × 42** décentrée à gauche, toit en pente et **0,30 mm de jeu par face**.
- La **LED orange 5 mm** est reculée derrière une ouverture optique Ø2 mm. Son **logement est déplacé en haut à droite de l'ouverture (X = 142 mm, Z = 53,3 mm)**, pour ne pas traverser le servo, et son diamètre externe **10,8 mm** offre une paroi radiale de **2,1 mm** autour de la poche Ø6,6 mm. Ce sont des **cotes de conception, pas des mesures de collerette**.
- **[Test d'intégrité des exports](test_step_exports.py)** : compare la somme SHA256 des quatre BREP à [leur manifeste](vendor_models/manifest.json), réimporte les neuf STEP individuels et teste les collisions de la porte à 0–90°.
- Les **11 STEP et 8 STL générés** sont **exclus des commits** pour éviter les conflits de fusion ; [GitHub Actions](../.github/workflows/cad-validation.yml) les distribue en **artefact téléchargeable** après chaque validation.
- Pour générer : `python cad/generate_cad.py` depuis la racine du dépôt, puis `python cad/verify_gotronic.py` et `python cad/test_step_exports.py`. La CAO reste une **V2 d'étude**, sans validation de fixation réelle du servo.


### Export Onshape simplifié (XIAO)

Le BREP source du XIAO contient **77 solides** et peut produire un *contains faults* sous le moteur de traduction d'Onshape. Le générateur reconstruit une **enveloppe analytique d'un seul solide**, basée sur les boîtes englobantes de la carte et du connecteur USB, en gardant les six limites exactes du STEP source et la position du module dans le garage. Cette référence simplifiée n'est **PAS** adaptée aux dimensions des trous, des connecteurs 2,54 mm, des soudures ni à la conception finale du support PCB.

Deux fichiers supplémentaires sont désormais générés : `step/REF_XIAO_NRF52840_SIMPLIFIE_POUR_ONSHAPE.step` et `step/GarageStateClone_V2_STRUCTURE_SANS_REFERENCES_ONSHAPE.step`. L'assemblage habituel `GarageStateClone_V2_assemblage_STEP_references.step` utilise lui aussi l'enveloppe simplifiée, alors que **la géométrie 77-solides originale est toujours conservée** dans `refs/xiao.brep.z.b64`.

Voir [méthode de réimport Onshape](../docs/ONSHAPE_IMPORT_XIAO.md). Les STEP sont vérifiés par réimportation sous CadQuery/OpenCascade ; **seul un essai dans Onshape permet de confirmer l'absence de tout défaut d'import**.

## Historique V3 — habillage intérieur des montants, remplacé dimensionnellement par V4

Deux **retours de tableau** sont fusionnés à la coque au niveau de l'ouverture avant, sur **10 mm de profondeur intérieure**, **épaisseur 2,4 mm**. Aucun retour ne doit entrer dans le volume du panneau mobile. Un trou Ø3,8 mm dans le retour gauche libère la rotation du tourillon Ø3,2 mm, en conservant **0,30 mm de jeu radial**. Le palier gauche est décalé de **1,6 mm** vers l'extérieur de la baie.

Pour ménager le retour droit face au servo STEP, le servo est déplacé **1,5 mm vers la droite** par rapport à la porte et la coque est élargie de **6 mm**, soit **190 × 100 mm**, baie **110 × 42 mm** inchangée. L'espace de couplage passe à **3 mm**, qui **n'est pas encore un accouplement dimensionné**. La pièce `08_liseret_bleu` est supprimée et ne doit plus figurer dans les nouveaux exports.

La V3 génère **8 STL** et **11 STEP** (8 STEP de pièces, assemblage complet avec XIAO simplifié, structure seule, XIAO simplifié). **La géométrie doit encore être vérifiée après impression** et les vis et le palonnier du servo restent provisoires. [Notes et tests V3](../docs/RETOURS_FACADE_V3.md).

## V4 — coque compacte asymétrique, édition courante

La **coque 150 × 100 mm** conserve le toit mono-pente (62/65 mm), le montant intérieur/retrait de tableau de **10 mm** et la porte rigide noire. **Baie 100 × 42 mm**, centrée à X=61 mm dans une coque centrée à X=75 mm : **décentrage −14 mm**. Montants gauche/droit : **11 / 39 mm**.

Le **servo STEP complet** occupe désormais X ≈ **113,7–146,2 mm**, juste derrière le montant droit. La pièce palier gauche est **réduite à 5,0 mm de largeur** (alésage Ø3,8 mm) et commence à X ≈ **3,2 mm**, hors de la paroi extérieure X=0–2,4 mm ; sa bride compacte de 5 mm conserve un contact mécanique avec le palier et ne coupe pas le mur. Les deux retours intérieurs font encore **2,4 mm × 10 mm**.

L'assemblage se génère toujours en **8 STL et 11 STEP** : pas de bandeau bleu, et références originales BREP conservées. Les fichiers STEP doivent être réimportés dans Onshape. [Détails CAO et limites](../docs/IMPLANTATION_COMPACTE_V4.md).

## V5 actuelle — combles et toit accentué

Le **toit arrière passe à Z=78 mm**, le bord avant restant Z=62 mm. La pente est donc **16 mm sur 100 mm (≈9,1°)**, sans élargir la coque compacte 150 × 100 mm. La porte reste décentrée, baie 100 × 42 mm.

Le modèle imprime maintenant un **faux plafond de combles amovible** à la place de l'ancien plateau électronique : **144,6 × 40 × 2,4 mm**, de Y=55 à Y=95 mm, base Z=46 mm. Deux **appuis muraux** intégrés à la coque portent le plateau, avec **0,3 mm de jeu aux parois** ; de petites nervures sous le plateau limitent sa flexion. Les cartes sont sur la face supérieure, la LED blanche est fixée sous le plateau et son fil traverse un perçage de Ø2,4 mm.

Le modèle référence **Wio Z≈51,9..59,54 mm et XIAO Z≈59,54..64,00 mm**, Y≈70,1..87,9 mm. À Y≈70,1 mm, l'intrados du toit est Z≈70,2 mm : la marge théorique est **≈6,2 mm**, sans antenne/câble/prise USB modélisés. Le BC547B est lui aussi dans les combles ; **le condensateur reste près du servo à l'avant**. Une fente arrière haute **16 × 9 mm** a été prévue (à adapter au câble réellement choisi).

**Contrôles CAO :** 8 pièces imprimables, 11 fichiers STEP, STEP Wio/XIAO/transistor sans intersection avec le nouveau plafond ni le toit, et porte testée de 0 à 90°. Le couplage mécanique du servo, les véritables vis de PCB, la fixation du câble coaxial/USB et l'antenne ne sont toujours **pas validés physiquement**.

Voir le [plan de montage V5](../docs/TOIT_COMBLES_V5.md). Les sections V3/V4 plus haut documentent l'historique, pas les hauteurs actuelles.
