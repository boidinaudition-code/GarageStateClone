# CAO paramétrique GarageStateClone — V10 (bandeau nervuré, façade et câblage intérieur)

**Source de vérité : [generate_cad.py](generate_cad.py)** (CadQuery 2.8, unités mm). La V6 est un **prototype mécanique**, pas un assemblage validé avec le vrai DMS-MG90 ou avec le palonnier livré.

**Cotes fournisseurs et fixations V7 :** [audit fiches cotées](../docs/FICHES_COTEES_COMPOSANTS_V7.md), [plan des fixations](../docs/FIXATIONS_SERVO_V7.md) et [catalogue JSON](component_dimensions_sources_v7.json). Le constructeur **DMS-MG90** cote **29 mm entre les deux encoches Ø2** ; le berceau ajoute **deux pilotes Ø1,7** pour ces encoches en plus des **4 vis du socle**. Le crochet V6 a été retiré au profit d'une colonne arrière plus robuste. **Erratum :** les 33 mm constructeur (axe Z du garage) ne se comparent pas aux 32,5 mm STEP (axe X du garage) ; la réserve antérieure de 0,05 mm était un calcul sur axes différents et ne s'applique pas. Comparaison correcte du volume constructeur **X30 / Y12 / Z33** au STEP **X32,5 / Y12,221 / Z33,4**. L'alignement axial des oreilles et le palonnier restent à essayer sur pièces réelles.

**Positionnement longitudinal du support servo pour Onshape :** `SERVO_LUG_UNDERSIDE_FROM_BASE = 16.00` est la **cote fabricant** du dessous des oreilles depuis le fond. Dans le repère X orienté vers le fond : `X_dessous_oreilles = X_bout_arbre + (30.00 - 16.00) = 127.70 mm`. La face imprimée des deux bossages est à `X = 128.00 mm`, soit **+0,30 mm de jeu**, indépendamment des approximations d'épaisseur. Cotes **≈2,5** (épaisseur oreille), **≈4** (haut du boîtier) et **≈8 mm** (bossage arbre) documentées mais **jamais utilisées comme contraintes serrées**. Palonnier et têtes/longueur des vis = inconnus. Les STEP de tiers restent des références, pas la géométrie fabriquée du DMS-MG90.

**Entrée USB-C V8 :** platine Gotronic **49067** (enveloppe vendeur **21 × 15 × 4,5 mm**), orientée provisoirement **X15 / Y21 / Z4,5** au bas du garage, juste devant le mur arrière. La pièce **02_socle_noir** comporte un berceau **X63,9..86,1 / Y72,4..96,6 / dessus Z9,0**, deux guides latéraux et **2 tunnels horizontaux de 3,2 × 2,7 mm** pour colliers isolés. La coque V10 a une **ouverture USB-C arrière 10 × 4,2 mm**, entre **Z9,45 et Z13,65**, qui remplace l'ancienne découpe 13 × 8. L'empreinte et la position exactes de la prise sur la 49067 **ne sont pas vérifiées** : essayer la platine réelle avant impression finale. Référence simplifiée dans l'assemblage : `REF_USB_C_49067_GABARIT_NON_CONTRACTUEL_NE_PAS_IMPRIMER`. **Aucun perçage, nez de connecteur ni position CC prétendu exact**. Essai obligatoire avec carte et fiche réelles.

L'alimentation 5 V du XIAO et du servo est réalisée **en parallèle depuis la platine**, avec un petit bus soudé à part (borniers 48930, résistances CC1/CC2 5,1 kΩ uniquement si absentes). Voir [le guide V8](../docs/ALIMENTATION_USB_C_V8.md). Le support USB-C reste **intégré au socle** ; la V9 ajoute une pièce imprimable distincte pour la boîte aux lettres.

**Toit bac acier V9 :** la pièce `03_toit_noir_pente` comporte désormais **13 nervures trapézoïdales**, axes **Y** dans la direction de la pente, premier centre X=5,5 mm, pas X=11,5 mm, base **2,5 mm**, sommet **1,1 mm**, saillie **0,95 mm**. Les nervures sont fusionnées au dessus du toit (pénétration de fusion 0,18 mm), **sans diminuer ses 3 mm d'épaisseur sous le relief**, ni altérer le bord inférieur et la jupe amovible. Paramètres `ROOF_RIB_*`.

**Boîte aux lettres V10 :** niche **X=126,0..133,6 mm, Z=25,5..33,1 mm, Y=0..1,05 mm** dans le **montant blanc droit** de `01_coque_blanche`. L'épaisseur locale résiduelle de façade est toujours **1,35 mm**. Pièce séparée `10_boite_aux_lettres_noire` : carré **7 × 7 × 0,75 mm** (30 % de réduction linéaire par rapport aux 10 × 10 de V9), à coller en léger retrait avec **0,30 mm de jeu sur chaque côté**. Fente superficielle imprimée (non fonctionnelle) ; finition cosmétique, photo non relevée au pied à coulisse. Voir [la révision V10](../docs/EVOLUTION_FACADE_CABLAGE_V10.md).

**Bandeau de toiture métallique V10 :** `roof_front_fascia_seams` ajoute **13 nervures trapézoïdales verticales** sur la partie **descendante en façade** du toit noir, exactement aux mêmes X que les nervures supérieures, espacement 11,5 mm, relief de **0,85 mm en direction −Y**. Environ Z54,37..62,47. La jupe interne, la pente et le système de toit amovible restent intacts.

**LED orange :** X96 inchangé et Z **53,3 → 52,1 mm**. Le boîtier de LED, le conduit optique et la référence STEP suivent cette descente de 1,2 mm.

**Goulotte intérieure V10 :** le **trou extérieur arrière haut 16 × 9 est supprimé**. Deux rails de **1,8 mm** et trois petites lèvres alternées constituent un guide de fils **ouvert** contre le mur arrière, **X90..100,8 / Y93,6..97,72 / Z14..43**, laissant **7,2 mm de largeur** entre les deux rails. Le câble part de la distribution 5 V en bas et monte sous le faux plafond ; aucun nouveau trou de façade n'est nécessaire. Ce passage est un prototype pour fils souples, pas un conduit garanti pour tout connecteur/coaxial.

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
| LED orange façade | X96 / Z52,1 |
| Emboîtements | **0,30 mm par face**, cible CAO à calibrer en FDM |

Les **9 STL** sont : coque avec logement de boîte aux lettres, **socle intégrant le berceau USB-C**, toit nervuré bac acier, porte, palier gauche, berceau servo, faux plafond, support LED blanche et **10_boite_aux_lettres_noire** indépendante. Le bandeau bleu est supprimé.

### Interfaces mécaniques nouvellement dessinées

- **Berceau servo** : quatre pieds **6 × 6 × 5,5 mm**, pilotes **Ø1,7** alignés sur quatre trous socle **Ø2,3** et fraisures **Ø4,2** ; **essai de quatre vis M2×8 à tête fraisée depuis dessous**, sans garantie de filet ni hauteur de tête.
- **Maintien moteur V7** : colonne extérieure et **2 vis pilotes Ø1,7 espacées de 29 mm** selon les encoches Ø2 du DMS-MG90. Les quatre M2 de fixation du berceau au socle sont distinctes. Longueur des vis et position axiale des oreilles à essayer sur le servo réel.
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

**Sorties** : **9 STL** dans le sous-dossier stl, **12 STEP** dans step (9 pièces, 1 assemblage avec références, 1 assemblage structure seule, 1 XIAO simplifié), et **3 coupons STL d'essai** dans coupons.

Les tests contrôlent intégrité SHA256 des quatre géométries BREP tierces, solides fermés, volumes réimportés, collisions et jeux échantillonnés de 0 à 90° par 5°. Ils ne testent ni adhérence des couches, ni résistance des bossages vissés, ni usure, ni véritable accouplement de servo. Les STEP sont des exports dérivés : ne pas les fusionner manuellement dans Git, les télécharger depuis **GitHub Actions**.

**Pour Onshape** : utiliser l'assemblage historique nommé GarageStateClone_V2_assemblage_STEP_references.step, mais sa **structure V7** inclut maintenant les deux pilotes de vis du servo (nom historique du fichier conservé). Alternative : GarageStateClone_V2_STRUCTURE_SANS_REFERENCES_ONSHAPE.step, huit pièces uniquement. Les anciens imports Onshape ne se réparent pas automatiquement.

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
