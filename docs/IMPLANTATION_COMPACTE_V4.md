# Implantation compacte V4 — coque 150 mm, porte décentrée

**Version courante après la V3 à 190 mm.** Modèle paramétrique : [`cad/generate_cad.py`](../cad/generate_cad.py). Les dimensions ci-dessous sont **des cotes de conception CAO**, pas des mesures du garage réel. Unités en millimètres.

## Objectif

Réduire la largeur du mini-garage sans sacrifier les volumes du moteur MG90 et des cartes. La porte devient **asymétrique** : un **montant gauche étroit** abrite seulement un petit palier, tandis que le **montant droit large** abrite le servo.

| Paramètre | V3 (historique) | V4 compacte |
|---|---:|---:|
| Largeur extérieure | 190 | **150** (−40, soit **−21,1 %**) |
| Profondeur | 100 | **100** |
| Hauteur avant / arrière | 62 / 65 | **62 / 65** |
| Baie (L × H) | 110 × 42 | **100 × 42** |
| Porte imprimée (L × H × E) | 109,4 × 41,4 × 2,4 | **99,4 × 41,4 × 2,4** |
| Épaisseur de coque | 2,4 | **2,4** |
| Toit et socle | 3 | **3** |
| Jeux latéraux dans la baie | 0,30 par face | **0,30 par face** |
| Retour de mur intérieur de chaque côté | 10 profond × 2,4 épais | **inchangé** |
| Montant gauche / montant droit | 40 / 40 | **11 / 39** |
| Largeur palier gauche | 6,5 | **5,0** |
| Entrefer provisoire arbre servo / porte | 3 | **3** |

### Vue de face : cotes le long de X

```text
X=0           11                            111                      150
 |-- 11 mm --|-------- 100 mm de baie -------|-------- 39 mm ----------|
 |   GAUCHE |       porte noire, 99,4 mm     |          DROITE         |
 |  palier  |          jeu 0,3 / côté        |        MG90 + LED       |
 |__________|_______________________________ |_________________________|

Centre de coque : X=75  |  centre de baie : X=61
Décalage de la baie : -14 mm (vers la gauche).
```

L'ouverture commence à **X=11**, se termine à **X=111**, et reste au même niveau vertical (base **Z=3**, hauteur **42**). Le toit à pente inchangée reste posé à **Z=62** à l'avant et **Z=65** à l'arrière.

## Implantation réelle des pièces CAO

- **MG90-A** (référence STEP fournie par l'utilisateur) : volume enveloppe en position **X≈113,7 à X≈146,2 mm** ; le servo reste **à l'avant, à droite, coaxial avec l'axe supérieur de la porte**. La paroi de droite occupe environ X=147,6..150. Le servo n'intersecte pas la coque dans le modèle.
- **Retour droit** de la baie : X=111..113,4 ; **0,30 mm** nominal de jeu avant l'enveloppe gauche du servo, dont Xmin≈113,7.
- **Palier gauche compact** : X=**3,2..8,2**, largeur **5,0 mm** ; Ymin=**2,7** pour laisser **0,30 mm** derrière la paroi frontale de 2,4 mm. Bride réduite à **5 × 2,4 × 18 mm** (liée au palier) entre X=3 et 8.
- **Retour gauche** de la baie : X=8,6..11 ; trou de dégagement **Ø3,8 mm** autour du tourillon de porte Ø3,2 mm (jeu 0,30 mm radial).
- **Porte** : X=11,3..110,7 ; panneau rainuré basculant **vers l'intérieur** de 0 à 90° autour de l'axe horizontal, Y=9,5 et Z=45,4.
- **Plateau arrière XIAO/Wio** : centré X=75, donc plateau X=45..105 ; profondeurs et hauteurs de service inchangées.
- **LED orange** au sommet droit de la baie : X=106, Z=53,3, ouverture optique Ø2 ; LED blanche sous toit vers l'arrière, déplacée avec le centre de coque.
- **Liseré bleu** : supprimé depuis V3, non réintroduit.

## Tests intégrés au dépôt

Le fichier [`cad/test_step_exports.py`](../cad/test_step_exports.py) vérifie en plus des contrôles historiques :
- largeur coque **150**, baie **100**, décentrage **−14** et montants **11/39** ;
- diamètre de palier et largeur réduite, jeu du servo derrière le retour droit ;
- absence de collision entre **palier / mur**, **palier / retour gauche**, **servo / coque**, **servo / retour droit**, **support servo / retour droit** ;
- absence de collision entre **porte / coque / retours / servo** de 0 à 90° par pas de 5° ;
- intégrité des quatre BREP tierces et réimportation des **8 STEP des pièces**, validité des **8 STL** fermés, existence des **11 STEP**.

## Limites et impression Bambu P1S

- L'**accouplement entre palonnier du vrai servo et porte**, les vis et la fixation des supports **ne sont pas encore validés**. Le modèle est un prototype CAO, pas un ensemble prêt à assembler sans essais.
- Le servo disponible dans les fichiers STEP est un **MG90-A générique**, qui peut différer du **DMS-MG90** commandé. Tester le logement et le mouvement avec le matériel réel avant la coque finale.
- Prévoir un **coupon de calibration d'emboîtement 0,30 mm/face** et contrôler la surface du palier après impression.
- Le code et les fichiers BREP sont les sources de vérité ; les sorties STEP et STL sont reconstruites par [GitHub Actions](../.github/workflows/cad-validation.yml), **non fusionnées manuellement**.
- Pour Onshape, **réimporter** `GarageStateClone_V2_assemblage_STEP_references.step` depuis l'artefact de la nouvelle exécution Actions. Son **nom conserve « V2 » pour compatibilité**, mais la géométrie est bien la **V4 compacte 150 mm**.

**Le firmware LoRa et son capteur SAS308 unique restent inchangés** : l'objet continue de suivre la fermeture confirmée et d'estimer l'ouverture à partir du délai configuré.
