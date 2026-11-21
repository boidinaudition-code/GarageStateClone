# GarageStateClone — maquette CAO V2 avec STEP de composants fournis

## Statut et limites

**V2 de conception**, modèle CAD paramétrique CadQuery, non validé sur matériel réel.

- Les 4 modèles 3D fournis par l'utilisateur ont été importés comme **solides STEP originaux** (servo DMS-MG90-A, XIAO nRF52840, Wio-SX1262 for XIAO, BC547B). Ils sont dans `refs/*.step` et **également incorporés dans `step/GarageStateClone_V2_assemblage_STEP_references.step`**.
- Le servo, le Wio/XIAO et le BC547B sont des **références non imprimables** ; seuls les STL du dossier `stl/` sont destinés à l'impression.
- Le modèle 3D du servo **MG90-A** fourni n'est pas une attestation de conformité dimensionnelle avec le produit **DMS-MG90** acheté. Vérifier physiquement avant de percer ou visser.
- La **liaison palonnier/axe de porte**, les **trous de vis servo**, la fixation exacte des cartes par connecteurs et l'antenne demandent encore une prise de cotes sur le matériel réel.
- Onshape : importer l'**assemblage STEP** pour inspecter les références ; `generate_cad.py` reste la source paramétrique des pièces imprimées (pas de FeatureScript natif).

## Changements par rapport à V1

Le servo complet (pattes comprises) montre une enveloppe hors tout de **33,40 × 32,50 × 12,22 mm** dans le repère de son STEP. La coque est élargie à **184 × 100 mm** pour garder le moteur **dans le montant avant droit**, coaxial à la charnière haute de la porte. Le servo est orienté de côté pour réduire l'emprise devant la façade, et le volet continue de **se rabattre à l'intérieur**.

Le XIAO et le Wio sont représentés avec leurs géométries 3D sur le plateau arrière, sans intersection avec coque, toit ou plateau. Leur empilage est **aligné approximativement** selon les trous de fixation des deux STEP et reste à contrôler après montage.

## Paramètres CAO

| Paramètre | V2 |
|---|---:|
| Largeur × profondeur | **184 × 100 mm** |
| Hauteur avant / arrière | **62 / 65 mm** |
| Pente de toit | **3 mm** sur 100 mm (1,72°) |
| Parois principales | **2,4 mm** |
| Toit / socle | **3 mm** |
| Largeur baie / hauteur | **110 × 42 mm** |
| Vantail | **109,4 × 41,4 × 2,4 mm** |
| Jeu d'emboîtement | **0,30 mm par face**, donc +0,60 mm sur largeur/diamètre intérieur |
| Axe porte / alésage palier | **Ø 3,2 / Ø 3,8 mm** |
| Centre axe porte (repère CAO) | Y = **9,5 mm**, Z = **45,4 mm** |
| Servo STEP, gabarit dans l'assemblage | X **148,2–180,7**, Y **3,4–15,62**, Z **23,3–56,7 mm** |
| Éclairage blanc sous toit, arrière | Y = **69 mm** |
| LED orange en façade, perçage | **Ø 3,6 mm** |

### Modules STEP relevés (avant mise en place, hors antennes/câbles)

| Objet | Enveloppe de son STEP | Corps réels / accessoires |
|---|---|---|
| Servo **Mg90.STEP** | **33,40 × 32,50 × 12,22 mm** | Pattes et axe présents ; palonnier non garanti |
| **XIAO-nRF52840 v3.step** | **22,482 × 4,46 × 17,78 mm** dans le repère d'origine | Carte et USB inclus, hors fils |
| **Wio-SX1262 ... V2.step** | **17,78 × 22,316 × 7,642 mm** | Modules et connecteurs, hors antenne externe |
| **BC547-B.step** | **4,08 × 3,05 × 12,8 mm** | Pattes incluses dans le modèle |

Consulter `qa_report.json` : les géométries de servo et de supports n'ont **pas d'intersection** dans le modèle, les neuf STL sont des volumes fermés. Le contact numérique XIAO/Wio comporte une très petite intersection d'environ **0,013 mm³**, compatible avec une approximation de placement mais **à valider avec l'empilage physique**.

## Imprimer et assembler

- Couleurs : **blanc** coque, **noir** toit/socle/porte, **bleu** liseré ; LED orange discrète.
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

Les STEP d'origine sont disponibles dans ce ZIP, sous `refs/`, et les 4 ZIP de téléchargement originaux peuvent aussi être convertis via `import_vendor_archives.py`. Les fichiers sources `generate_cad.py`, `qa_geometry.py`, `import_vendor_archives.py` et `reference_measurements.json` sont conçus pour être versionnés dans GitHub.

**Sur le vrai garage :** un **seul SAS308** (non inclus dans la miniature) détecte la **fermeture confirmée**. L'ouverture demeure une **estimation décorative** après 40 secondes sans aimant, selon la configuration actuelle du firmware, et ne doit pas être utilisée pour la sécurité du bâtiment.