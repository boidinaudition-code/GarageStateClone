# Vérification de la révision Gotronic

## Périmètre

Reprise du diff existant sur `docs/gotronic-only`, sans modification du firmware. Le montage conserve un seul SAS308 de fermeture ; aucune commande de la vraie porte.

Les prix et stocks sont les relevés des fiches directes Gotronic au navigateur transmis par le chef de projet : WCS101 03989 9,90 € (69), L7113NC 03051 0,18 € (250+), SAS308 26449 5,95 € (23), C1 0,20 € (500+), quatre lots de cinq résistances à 0,30 € chacun (stock confirmé). Servo 7,90 € et BC547B 0,15 € déjà contrôlés. Sous-total actuel du noyau : **25,48 € TTC**. Aucun achat ; prix et stocks peuvent évoluer. Total complet non déterminé : fournitures, quantités finales, fixation, alimentations manquantes et port restent à chiffrer.

## Reproduction des contrôles

Interpréteur retrouvé : `/opt/data/profiles/github-manager/cache/scratch/garage-cad-venv/bin/python` (CadQuery et trimesh).

**Sur un clone neuf, les STL, STEP et métriques ne sont pas présents : générer les artefacts avant de les vérifier.** Depuis la racine du dépôt, avec un environnement Python contenant CadQuery et trimesh :

```sh
PYTHON=/chemin/vers/venv/bin/python
# Sous Linux, fournir les bibliothèques système requises par CadQuery (dont libGL).
# Ajouter leur chemin à LD_LIBRARY_PATH seulement si elles sont hors des chemins système.
timeout 120 "$PYTHON" cad/generate_cad.py
timeout 120 "$PYTHON" cad/verify_gotronic.py
git diff --check
```

Les chemins ci-dessous décrivent uniquement l'environnement du worker utilisé pour les contrôles ; ils ne font pas partie du dépôt et sont à adapter sur une autre machine :

```sh
export LD_LIBRARY_PATH=/opt/data/profiles/github-manager/cache/scratch/garage-cad-libs/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
PYTHON=/opt/data/profiles/github-manager/cache/scratch/garage-cad-venv/bin/python
timeout 120 "$PYTHON" cad/generate_cad.py
timeout 120 "$PYTHON" cad/verify_gotronic.py
```

## Résultats réellement exécutés

- Premier lancement : échec d'import CadQuery (`libGL.so.1` absent du chemin dynamique). Relance avec les bibliothèques locales existantes via `LD_LIBRARY_PATH` ci-dessus : **code de sortie 0, PASS**.
- JSON/générateur : capteur unique, LED nominales 5 mm, cotes inconnues et poches cohérentes.
- **44 chemins de liens Markdown locaux valides** ; SVG XML et syntaxe Python valides.
- **9 STL étanches à volumes positifs**, **9 solides uniques valides** ; **10 fichiers STEP présents et non vides** (pas une réimportation STEP).
- Enveloppes LED sans intersection avec coque, servo et support ; blanche dégagée du toit, recouvrement volontaire support/toit confirmé. Zones LED dégagées de la porte de 0 à 90° par pas de 5°.
- `git diff --check` : aucune erreur. Sous-total vérifié avec `decimal.Decimal` : **25,48 €**.
- Liste des fichiers modifiés contrôlée : aucun fichier firmware ; `sensor_count` et quantité S1 vérifiés à 1 par le test.

Les contrôles portent sur les chemins des liens Markdown locaux (pas la disponibilité HTTP ni les ancres), la syntaxe JSON et sa cohérence avec le générateur, les SVG XML, la syntaxe Python, les solides et les artefacts locaux existants. Les STL, STEP et métriques générés restent hors commit.

## Limites géométriques

Les LED sont nominalement de diamètre 5 mm ; longueur, collerette et pattes ne sont pas validées par une cote fabricant. Les enveloppes Ø6 × 9 mm, poches Ø6,6 mm, ouverture optique orange Ø2 mm et retrait 3,4 mm sont des **choix CAO provisoires**, pas des dimensions fabricants. Le support blanc recouvre volontairement le toit pour collage ; maintien et montage restent à définir après mesure.

Le balayage échantillonné de la porte ne qualifie ni toute la cinématique continue ni l'assemblage complet. Aucun essai physique, impression, test radio ou qualification électrique n'est effectué par ce script.

## Vérification additionnelle après réparation du merge

Le générateur CAO et le manifeste BREP sont maintenant testés à chaque PR et push `main` via [GitHub Actions](../.github/workflows/cad-validation.yml). En complément des contrôles documentaires ci-dessus, `cad/test_step_exports.py` vérifie les quatre SHA256 BREP, réimporte **9 STEP** pour comparer les volumes CadQuery, teste **9 STL** fermés et contrôle les collisions servo / LED et porte / LED de 0 à 90°. L'assemblage STEP est exporté et contrôlé au niveau structure et présence. Les sorties sont accessibles comme artefact GitHub Actions : **`garage-state-clone-cad-step-stl`**. Les résultats historiques de cette page ne constituent pas une validation physique.

## Dernière validation CAO V3 — retour de mur et retrait du bandeau

Le contrôle historique « 9 STL / 10 STEP » ci-dessus correspond à une version plus ancienne. **La V3 génère maintenant 8 STL et 11 STEP** : 8 pièces, assemblage avec références, structure seule pour Onshape et XIAO simplifié. Les tests CI vérifient les deux retours internes (épaisseur 2,4 mm, profondeur 10 mm), l'absence de liseré bleu, et la trajectoire 0–90° sans collision avec les joues et le servo. [Détails V3](RETOURS_FACADE_V3.md).
