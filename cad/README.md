# CAO paramétrique GarageStateClone — V6

**Source de vérité : [generate_cad.py](generate_cad.py)** (CadQuery 2.8, unités mm). La V6 est un **prototype mécanique**, pas un assemblage validé avec le vrai DMS-MG90 ou avec le palonnier livré.

**Cotes fournisseurs V7 :** [catalogue JSON sourcé](component_dimensions_sources_v7.json) et [audit des fiches cotées](../docs/FICHES_COTEES_COMPOSANTS_V7.md). Le **plan constructeur DMS-MG90** donne **33 × 12 × 30 mm** et **entraxe 29 mm** ; l'ancien STEP de référence MG90-A est plus haut et plus court. Le berceau imprimé V6 de longueur intérieure 33,1 mm ne laisse qu'environ **0,05 mm de jeu à chaque extrémité** par rapport à la longueur nominale officielle ; **ne pas le déclarer compatible** avant recalage de l'axe, redimensionnement du berceau/clip et essais sur pièce réelle. Les palonniers ne sont pas cotés.

## Géométrie de référence V6

| Cote | Valeur |
|---|---:|
| Coque au sol | **150 × 100 mm** |
| Toit avant/arrière | **62 / 78 mm**, pente ≈**9,1°** |
| Parois / toit / socle | **2,4 / 3 / 3 mm** |
| Ouverture de porte | **100 × 42 mm**, X=11..111, décentrée de 14 mm vers la gauche |
| Porte imprimée | **99,4 × 41,4 × 2,4 mm**, noire rainurée |
| Tourillon gauche / palier | **Ø3,2 / Ø3,8 mm** (jeu radial 0,30 mm) |
| Disque de liaison côté droit | **Ø12 mm** vierge, alésage de passage **Ø12,6 mm**, jeu radial 0,30 mm |
| Écart disque / pointe d’axe servo STEP | **2,2 mm nominal**, **hors vrai palonnier** |
| Faux plafond | **144,6 × 40 × 2,4 mm**, Y55..95 et Z46..48,4 |
| Support de LED blanche | X75 / Y65, **2 ergots Ø2 dans Ø2,6** |
| LED orange façade | X96 / Z53,3 |
| Emboîtements | **0,30 mm par face**, cible CAO à calibrer en FDM |

Les huit STL restent : coque, socle, toit, porte, palier gauche, berceau servo, faux plafond, support de LED blanche. Le bandeau bleu est supprimé.

### Interfaces mécaniques nouvellement dessinées

- **Berceau servo** : quatre pieds **6 × 6 × 5,5 mm**, pilotes **Ø1,7** alignés sur quatre trous socle **Ø2,3** et fraisures **Ø4,2** ; **essai de quatre vis M2×8 à tête fraisée depuis dessous**, sans garantie de filet ni hauteur de tête.
- **Maintien moteur** : crochet supérieur arrière imprimé avec berceau ; résistance à la déformation et tenue du DMS-MG90 réel non validées.
- **Palier gauche** : tablette de support intégrée à la coque ; collage localisé après essai à blanc, pas de vis inventée.
- **Liaison servo/porte** : disque imprimé Ø12 avec face à X111,5, pointe d’axe MG90-A STEP à X113,7 ; **pas de trous du vrai palonnier**. Faire le gabarit C, mesurer l'entraxe sur le palonnier fourni et choisir une liaison positive démontable.
- **Radio en combles** : quatre plots de soutien sous Wio, deux fentes **3,2 × 4,2 mm** pour un petit lien isolant ; jamais de serrage direct sur SMD, prise USB ou antenne.
- **LED blanche** : fixation par deux ergots imprimés Ø2 et perçages de plafond Ø2,6, **sans intersection** de solides. Passage central fils Ø2,4.
- **Câbles** : quatre œillets imprimés Ø8/Ø3,4 (épaisseur radiale 2,3 mm), à utiliser uniquement en basse tension.

**Les trous et l'accouplement du vrai palonnier restent à finaliser.** Le STEP MG90-A de référence ne certifie pas les pattes du DMS-MG90 livré. Les pièces électroniques XIAO/Wio ont ≈6,2 mm de garde théorique au toit hors USB, antenne et câbles.

## Génération des fichiers et vérifications

Depuis la racine du dépôt avec Python 3.11 :

~~~sh
python -m pip install 'cadquery==2.8.0' 'trimesh==4.11.1'
python cad/generate_cad.py
python cad/generate_fit_coupons.py
python cad/qa_geometry.py
python cad/verify_gotronic.py
python cad/test_step_exports.py
python cad/test_hardware_bom.py
python cad/test_component_dimensions_sources.py
python cad/test_fit_coupons.py
python cad/test_repo_consistency.py
~~~

**Sorties** : 8 STL dans le sous-dossier stl, **11 STEP** dans step (8 pièces, 1 assemblage avec références, 1 assemblage structure seule, 1 XIAO simplifié), et **3 coupons STL d'essai** dans coupons.

Les tests contrôlent intégrité SHA256 des quatre géométries BREP tierces, solides fermés, volumes réimportés, collisions et jeux échantillonnés de 0 à 90° par 5°. Ils ne testent ni adhérence des couches, ni flexion du crochet, ni usure, ni véritable accouplement de servo. Les STEP sont des exports dérivés : ne pas les fusionner manuellement dans Git, les télécharger depuis **GitHub Actions**.

**Pour Onshape** : utiliser l'assemblage historique nommé GarageStateClone_V2_assemblage_STEP_references.step, mais son **contenu est V6**. Alternative : GarageStateClone_V2_STRUCTURE_SANS_REFERENCES_ONSHAPE.step, huit pièces uniquement. Les anciens imports Onshape ne se réparent pas automatiquement.

## Éprouvettes et impression P1S

- **Coupon A** : alésages Ø3,6 / Ø3,8 / Ø4,0 à essayer avec axe imprimé Ø3,2.
- **Coupon B** : pilotes Ø1,6 / Ø1,7 / Ø1,8 avec vraie vis M2 et sa tête.
- **Coupon C** : disque Ø12 **sans entraxe de palonnier**, pour reporter les mesures du vrai MG90.
- Commencer avec 0,20 mm de couche et ≈4 périmètres pour les pièces contraintes ; ajuster matériau, sens des couches, retrait et soutien du tourillon. Les STL sont dans le repère assemblé, **à réorienter dans Bambu Studio**.
- Mesurer au pied à coulisse chaque interface et modifier **localement** la cote, sans imposer un redimensionnement global.

## Sources de modèles et documents

Les BREP originales sans perte sont dans [refs/](refs/) : servo MG90-A, XIAO nRF52840, Wio-SX1262 et BC547B. Vérifier le [manifeste](vendor_models/manifest.json), les licences des modèles tiers et l'usage du **XIAO simplifié** (enveloppe de dégagement, **pas** les trous ou broches).

- [**Guide d’assemblage V6**](../docs/ASSEMBLAGE_V6.md)
- [**Audit complet du dépôt**](../docs/AUDIT_REPO_V6.md)
- [BOM V6 et quincaillerie](../docs/BOM_V6.md)
- [README principal](../README.md)

**Archives de design, cotes remplacées** : [toit V5](../docs/TOIT_COMBLES_V5.md), [coque V4](../docs/IMPLANTATION_COMPACTE_V4.md), [mur V3](../docs/RETOURS_FACADE_V3.md). Les positions LED/fixations de ces versions ne correspondent plus toutes à V6.
