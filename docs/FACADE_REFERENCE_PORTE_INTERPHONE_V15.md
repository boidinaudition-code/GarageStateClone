# Façade V15 — porte piétonne, interphone et boîte aux lettres du rendu

**Référence visuelle :** image photoréaliste fournie par l'utilisateur le 23 novembre 2026, présentant une miniature de garage blanc à toit noir nervuré, porte sectionnelle centrale noire, petite boîte noire à rectangle blanc, interphone gris, porte piétonne noire à rainures verticales et poignée. Le rendu n'est pas un dessin industriel coté. Toutes les nouvelles dimensions sont des **choix de maquettisme**, à différencier des cotes attestées du servo et des cartes.

## 1. Contraintes conservées

- Modèle mécanique **105,6 × 85 mm** au sol, toit **Z62 / Z78**, murs **2,4 mm**.
- Porte **motorisée de garage** de **55 × 41,4 mm**, ouverture 55,6 mm et débattement de 0 à 90°, gauche X11, droite X66,6.
- Montant droit de **39 mm**, avec support servo, palonnier non finalisé, câble et interphone **décoratif seulement**.
- Boîte aux lettres actuelle **7 × 7 mm**, exactement **10 mm de décalage visuel** à droite de l'ouverture de la porte de garage.
- Toit noir amovible, **9 nervures bac acier sur le pan supérieur et 9 nervures alignées sur la retombée frontale**, sans réduire l'épaisseur de 3 mm du pan ou modifier la jupe démontable.
- LED orange réelle sur le montant gauche (X5,3/Z32), USB-C à l'arrière, XIAO/Wio dans les combles et goulotte intérieure V14, sans modifications fonctionnelles.

## 2. Nouvelle porte piétonne noire, fixe

| Caractéristique | Géométrie V15 |
|---|---|
| Niche dans le mur blanc | X **89,4..104,0**, Z **3,25..41,65** ; profondeur **1 mm** |
| Panneau noir indépendant | **14 × 37,8 × 0,76 mm**, X **89,7..103,7**, Z **3,55..41,35** |
| Face de l'insert | Y **0,12..0,88**, noyé dans le mur, encadrement blanc très fin |
| Détails de panneau | Rebord noir, panneau intérieur en léger creux, **5 rainures verticales** de 0,42 mm, traverse basse à Z ≈14,75 |
| Poignée | Écusson/support noir d'environ **0,95 × 2,25 mm** et levier **2,85 × 0,55 mm**, fusionnés à la pièce, en saillie sur la face |
| Mur blanc derrière la niche | **1,4 mm** minimum |

**Ne fonctionne pas comme une vraie porte** : pas de charnières, de fermeture ou d'ouverture traversante. L'emplacement et la largeur sont contraints par le moteur dans le montant droit : c'est une approximation de la porte du rendu, plus étroite qu'une porte à l'échelle 1.

## 3. Interphone gris, également décoratif

- Niche blanche : X **84,8..88,4**, Z **27,9..35,1**, profondeur **0,95 mm**.
- Corps extérieur imprimé gris : **3 × 6,6 × 0,73 mm** avec jeu de 0,3 mm par côté.
- En haut : trou de caméra **Ø1,12 mm** en léger creux, pouvant être peint en noir. En bas : bouton **Ø0,90 mm** en creux. Trois reliefs horizontaux de grille **1,5 × 0,28 mm** à mi-hauteur.
- Ne pas percer le fond : le mur porteur reste fermé ; **pas de fil, buzzer, caméra, moteur ni carte électronique**. Les gravures fines peuvent s'atténuer à la buse FDM 0,4 mm ; un point de peinture noire améliore les contrastes.

## 4. Boîte noire et rectangle blanc

La pièce **`10_boite_aux_lettres_noire`** reste un carré **7 × 7 mm** encastré sur le montant droit. Sa rainure supérieure V14 a été transformée en un petit logement de **5,5 × 1,2 mm**, d'une profondeur de **0,43 mm**.

La nouvelle pièce **`14_insert_blanc_boite_lettres`** mesure **5,1 × 0,8 × 0,35 mm**, avec un jeu d'environ 0,2 mm autour. À imprimer en filament blanc, ou à remplacer au besoin par une petite découpe de vinyle blanc. **Coller seulement après un essai à blanc**. Le liseré n'a pas vocation à recevoir une lettre réelle.

## 5. Finition du toit

- Neuf bandes noires en relief **0,95 mm** sur la pente et neuf profils correspondants sur le bandeau vertical descendant (**0,85 mm vers l'avant**).
- **Deux rives latérales** fusionnées au toit, largeur **1,2 mm**, surélévation **0,55 mm** ; elles suivent la même pente et restent dans les débords existants.
- **Petit larmier frontal** noir continu, hauteur **0,70 mm**, profondeur **0,55 mm**, fusionné au rebord supérieur du bandeau.
- Ne jamais modifier la partie intérieure de la jupe / de l'emboîtement pour réaliser ces détails purement extérieurs.

## 6. Impression et couleur

| Pièce | Couleur recommandée | Assemblage |
|---|---|---|
| `01_coque_blanche` | Blanc mat | Poches moulées dans la façade |
| `03_toit_noir_pente` | Noir / anthracite mat | Toit amovible, **nervures et larmier intégrés** |
| `10_boite_aux_lettres_noire` | Noir | Collage dans le logement de façade |
| `12_porte_pietonne_noire` | Noir | Collage léger dans la niche, poignée sur la face extérieure |
| `13_interphone_gris` | Gris argenté / gris | Collage ; peinture noire dans caméra et bouton si désiré |
| `14_insert_blanc_boite_lettres` | Blanc | Collage du trait blanc dans la boîte noire |

**Architecture des fichiers : 13 pièces imprimables et 16 STEP** (13 pièces, assemblage avec références tierces, assemblage structure Onshape et proxy XIAO). La génération doit être contrôlée par l'Action GitHub CAO, la stabilité des BREP, les maillages watertight, les jeux et la rotation de porte 0–90°. La mécanique et le firmware demeurent ceux de V14.

**Réserve d'atelier :** les dimensions de l'USB-C Gotronic et du palonnier réel ne sont toujours pas définitivement connues ; la porte et l'interphone de façade ne changent pas ce statut. Une validation des trois petits collages, en particulier du rectangle blanc de 0,8 mm de haut, reste indispensable sur impression réelle.

[README du projet](../README.md) · [README CAO](../cad/README.md) · [générateur CadQuery](../cad/generate_cad.py).
