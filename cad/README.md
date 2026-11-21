# GarageStateClone — source CAO paramétrique V1

**Fichier source : [generate_cad.py](generate_cad.py)** (CadQuery). Unités **mm**. Ne pas confondre dimension d'un composant et *volume de service* proposé autour de lui.

## Statut

Cette CAO est un **prototype technique**, non un assemblage mécaniquement qualifié. Le script génère **9 pièces imprimables**, un **assemblage STEP** incluant des volumes de référence explicitement marqués **NE_PAS_IMPRIMER**, et les métriques de volume/coordonnées. Il ne fournit pas un Part Studio Onshape natif. Pour modifier les cotes, éditer les variables en tête du script puis régénérer.

L'assemblage comporte notamment la coque blanche, le toit noir mono-pente, le socle, la porte noire rainurée, le palier gauche, le support servo **provisoire**, le plateau électronique arrière, le liseré bleu et le support de LED blanche.

## Dimensions CAO de la version documentée

| Paramètre | Valeur (mm) | Nature |
|---|---:|---|
| Largeur extérieure de la coque | **168** | Choix design |
| Profondeur extérieure de la coque | **100** | Choix design |
| Hauteurs avant / arrière | **62 / 65** | Toit mono-pente montante de **+3 / 100** (~1,72°) |
| Parois | **2,4** | Structure, minimum utilisateur ≥2 |
| Toit / socle | **3 / 3** | Structure |
| Baie / vantail | **104 × 42** / **103,4 × 41,4 × 2,4** | Vantail avec 0,30 mm de jeu de chaque côté |
| Axe / palier | **Ø3,2 / Ø3,8** | Jeu radial 0,30 mm |
| Alésage LED orange | **Ø3,6** | Pour boîtier LED Ø3 |
| Volume de **corps** du DMS-MG90 | **22,3 × 11,8 × 26,3** | Taille du corps constructeur, **n'inclut pas fixation/arbre/palonnier** |
| Réserve technique radio | **52 × 23 × 12** | **Réserve de câblage choisie** ; XIAO seul = 21 × 17,8 |
| Plateau électronique | **60 × 31** | Largeur × profondeur proposées |
| C1 470 µF | **Ø10 × 13**, pas fils 5 | Référence dimensionnelle représentée en rouge « NE_PAS_IMPRIMER » |
| LED blanche 304WC2J-W6-3PD | **Ø3 × 5,1** | Valeur constructeur |
| Jeu d'emboîtement | **0,30 par face** | 0,60 mm au diamètre/largeur, essai de calibration conseillé |

## Cinématique et implantation

- La porte est **rigide et monobloc**, à rainures horizontales **décoratives** (pas une vraie sectionnelle).
- **Le servo est à l'avant, en haut à droite**, coaxial à l'axe horizontal **supérieur** de porte ; un palier imprimé est à gauche.
- La porte **bascule vers l'intérieur** jusqu'à ~90°, puis se range sous le toit en pente ; la trajectoire doit rester libre de tout fil, LED ou carte.
- Électronique XIAO/Wio et petite plaque à souder sur **plateau arrière**, hors débattement. **C1 proche du servo**, LED blanche sous le toit arrière, LED orange en haut à droite de la façade.
- Toit amovible. Imprimante **Bambu Lab P1S + AMS** ; filaments **noir, blanc, bleu, rouge**.

**À mesurer avant les fixations définitives :** pattes/vis, déport d'arbre et palonnier du DMS-MG90, épaisseur de la pile réelle XIAO/Wio, connecteur coaxial/antenne, USB-C, collerette de LED orange, taille de l'aimant SAS308.

## Génération (sur un PC disposant de CadQuery)

Depuis le dossier contenant ce script :

~~~sh
python -m pip install cadquery
python generate_cad.py
~~~

Le script crée les sous-dossiers **stl/** et **step/** et les fichiers de contrôle. L'importation de l'assemblage dans Onshape est possible par **Import → STEP** ; les références marquées « NE_PAS_IMPRIMER » ne doivent pas être envoyées à la Bambu P1S.

Les neuf STL ont été régénérés et vérifiés **watertight** dans la session de travail du 21/11/2026. **Ce contrôle géométrique n'est pas un test d'impression, de montage ni de cinématique matérielle.**

## Correspondance avec le BOM et le firmware

- [Dimensions des composants : vérifié / réservé / à mesurer](../docs/ENCOMBREMENT_BOM_V1.md)
- [BOM à 1 SAS308](../docs/BOM_V1_VERIFIEE.md)
- [Schéma de câblage récepteur et émetteur](../docs/CABLAGE_V1_VERIFIE.md)

**Émetteur : un seul SAS308** positionné pour détecter la **fermeture** (aimant en face lorsque la vraie porte est fermée). Sans aimant, la position est d'abord « intermédiaire/non fermée », puis **ouverte estimée** après un délai réglable (40 secondes par défaut). Ce n'est jamais une confirmation de la position réelle si la porte s'arrête en chemin.
