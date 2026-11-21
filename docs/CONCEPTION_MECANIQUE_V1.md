# GarageStateClone — V1 retenue : mécanique et éclairage

**Décisions du 21/11/2026 — CAO de prototype (STL et STEP générés localement), sans validation par impression ni sur matériel physique.**

## Design extérieur retenu

Référence visuelle **exacte** : le garage miniature noir et blanc initialement avec un fin liseré bleu (désormais supprimé), posé sur une étagère en bois dans l'image explicitement sélectionnée par l'utilisateur.

- Garage bas, rectangulaire, sobre et discret, comme un objet de décoration.
- Murs **blancs**, toit mono-pente **noir**, porte **noire** à rainures horizontales, **aucun bandeau bleu** ; retours de mur intérieurs dans les montants de l'ouverture.
- Un **minuscule point orange en haut à droite de la façade**, LED **L7113NC 5 mm cachée en retrait** derrière une petite ouverture optique ; pas besoin de montrer tout le diamètre. Pas d'autre décoration voyante.
- Toit noir **amovible** pour accéder aux composants.
- Fabrication Bambu Lab **P1S + AMS** ; filaments disponibles : blanc, noir, bleu, rouge. Privilégier des pièces imprimées séparément par couleur.
- Les dimensions indicatives du rendu (~115 × 75 × 45 mm) représentent l'intention visuelle, **pas des cotes mécaniques confirmées**. Conserver les proportions mais dimensionner la coque après mesure de la carte radio, du servo et de la porte.

## Mouvement mécanique — choix définitif pour la V1

**Porte monobloc basculante vers l'intérieur** ; aspect « sectionnel » uniquement décoratif (rainures parallèles). Aucun panneau articulé, rail courbe, ficelle, poulie ou crémaillère.

- **Fermée** : panneau vertical devant l'ouverture.
- **Ouverte** : panneau relevé à ~90°, rangé **sous le plafond à l'intérieur**.
- **Intermédiaire** : panneau partiellement relevé.
- **Conséquence acceptée** : la porte balaie une partie du volume intérieur. Ne pas placer de fausse voiture, de LED, de fil ou d'électronique dans ce volume.

### Schéma de profil, non à l'échelle

~~~text
   FERMÉ                            OUVERT
   toit noir                        toit noir
   ┌───────────────────┐            ┌───────────────────┐
   ● axe               │            ●━━━━━━━━ porte    │
   ┃ porte             │            │                   │
   ┃                   │            │                   │
   ┃                   │            │                   │
   └───────────────────┘            └───────────────────┘
  façade       arrière             façade       arrière

  ● axe horizontal en haut de la façade ; rotation vers l'intérieur
~~~

**Garde au débattement :** pour une porte de hauteur H, réserver au moins H + marge vers l'arrière à partir de l'axe. Vérifier toute la trajectoire réelle en 3D, y compris épaisseur du panneau et pièces d'accouplement.

## Servo et charnière

Actionneur : **DFRobot DMS-MG90**, positionnel à pignons métalliques, Gotronic réf. 36923.

- **Boîtier du servo fixe**, monté sur support imprimé à l'intérieur, **en haut à droite** de l'ouverture.
- **Arbre de sortie du servo aligné sur l'axe supérieur horizontal de la porte**.
- Liaison mécanique directe par **palonnier du servo vissé et adaptateur imprimé** ; pas de bielle.
- **À gauche**, une petite portée / un tourillon dans un **palier imprimé** porte la porte et réduit l'effort latéral sur le servo.
- Panneau léger et rigide, départ ~2 mm d'épaisseur à ajuster. Butées et jeux mécaniques pour éviter le frottement.
- Ne **jamais** immobiliser le servo en butée sous tension : régler les angles pour arrêter avant toute butée physique.
- Le servo et son palonnier doivent être démontables en retirant le toit.

Les valeurs actuelles du firmware (**15° fermé, 55° intermédiaire, 95° ouvert**) sont *provisoires*. Calibrer d'abord le servo sans porte, puis vérifier la cinématique réelle avant d'arrêter les angles.

## Emplacement des éléments électroniques

| Zone | Implantation prévue |
|---|---|
| **Avant en haut à droite** | Servo + support, axe coaxial sur le bord supérieur de la porte |
| **Avant en haut à gauche** | Palier imprimé du côté opposé |
| **Sous le toit vers l'arrière sur longueur H** | **Volume balayé : laisser intégralement libre** |
| **Zone arrière / compartiment technique** | XIAO nRF52840 + Wio-SX1262, connecteurs, résistances et câbles ; vérifier que cette zone n'empiète pas dans le balayage |
| **Dessous du toit à l'arrière** | Une LED blanche chaude de faible courant, tournée vers le plancher, **hors du balayage** |
| **Façade haute droite** | Une L7113NC 5 mm cachée en retrait derrière un petit point lumineux, résistance dédiée, câbles longeant la paroi latérale hors débattement |
| **Face arrière** | Passage discret des alimentations USB / des fils et accès de maintenance |

Placer l'antenne 868 MHz sans contact avec des pièces métalliques et, si possible, loin du servo et des fils 5 V. Tester la liaison dans la coque fermée.

**Alimentation :** le servo reçoit une alimentation **5 V régulée**, source capable de supporter ses appels de courant (alimentation USB 5 V/2 A envisagée). **Ne jamais alimenter le servo depuis 3V3 du XIAO ni un GPIO.** Relier les GND. Condensateur **470 µF / 16 V** sur le 5 V/GND près du servo, en respectant la polarité.

## Éclairage et signalisation — deux LED, sans ruban

**Choix V1 :**
1. **LED blanche chaude 5 mm du lot Whadda WCS101**, Gotronic **03989**, dissimulée **sous le toit vers l'arrière**, tournée vers l'intérieur. **+5 V via 330 Ω et BC547B**, jamais une LED de puissance : D7 ne fournit qu'un courant de commande. Ne jamais l'installer dans le volume balayé. Allumée après état **OUVERT estimé** et fin du déplacement logiciel du servo, sans confirmation physique d'ouverture.
2. **Orange L7113NC 5 mm**, Gotronic **03051**, en façade haute droite mais **cachée derrière un petit point lumineux** (ouverture CAO proposée Ø2 mm). Elle reproduit le clignotement logiciel et sert aussi d'alerte ; luminosité et discrétion à tester.

Les deux poches CAO Ø6,6 et les enveloppes Ø6 × 9 sont **provisoires**, pas des dimensions constructeur. Mesurer longueur, collerette et pattes avant impression définitive ; ne pas reprendre les cotes de l'ancienne LED 3 mm. [Achats et fournitures Gotronic](BOM_V1_VERIFIEE.md).

### Câblage retenu — voir le schéma à jour

- [Schéma complet récepteur SVG](../assets/schemas/cablage-recepteur-v1.svg)
- [Schéma émetteur SVG](../assets/schemas/cablage-emetteur-v1.svg)
- [Netlist précise, alimentation et test](CABLAGE_V1_VERIFIE.md)
- [Nomenclature révisée](BOM_V1_VERIFIEE.md)

| Broche / alimentation | Branchements |
|---|---|
| **D6** | Signal du servo DMS-MG90 (servo alimenté directement en **5 V externe**, jamais en 3V3) |
| **D7** | **4,7 kΩ** vers la base B d'un **BC547B** ; base B → **100 kΩ** → GND ; émetteur E → GND ; collecteur C → cathode de la LED blanche ; **+5 V externe → 330 Ω → anode LED blanche** |
| **D0** | Cathode LED orange ; **3V3 → 680 Ω → anode LED orange** ; LOW = ON, INPUT = OFF ; D0 partagé avec bouton/pull-up 10 kΩ du Wio |
| **GND** | Commun entre alimentation servo, transistor et XIAO |
| **+5 V externe** | Servo + R1 LED blanche ; condensateur **470 µF / 16 V** entre +5 V et GND près du servo |

**Correction :** l'ancienne suggestion D7 → 330 Ω → LED blanche → GND n'est pas garantie avec des LED annoncées Vf 3,5 V. Le BC547B ne change **ni le nombre de LED ni la logique du firmware** (D7 HIGH = intérieur éclairé) ; il ajoute une commande basse consommation et permet d'alimenter la LED en 5 V. **Vérifier les broches C/B/E du transistor livré.**

### Comportements logiciels V1

| État détecté | LED blanche intérieure | LED orange de façade |
|---|---|---|
| **Fermée** et servo à l'arrêt | Éteinte | Éteinte |
| **Servo miniature en déplacement** | Éteinte | **Clignote 2 Hz** |
| **Intermédiaire**, moins de 40 secondes depuis le changement d'état | Éteinte | **Clignote 1 Hz** (mouvement *supposé*) |
| **Intermédiaire prolongé** au-delà de 40 secondes | Éteinte | **Fixe** |
| **Ouverte** et servo arrivé à sa position | **Allumée fixe** | **Fixe** |
| **Défaut de capteurs** | Éteinte | **Clignote rapidement, 5 Hz** |
| **Liaison perdue**, plus de 150 secondes sans trame valide | Éteinte | **Double flash toutes les 2 secondes** |

Le délai de 40 secondes **ne prouve pas que la vraie porte bouge** : le SAS308 unique confirme la fermeture uniquement, pas des capteurs de vitesse. Une porte volontairement arrêtée à mi-course provoquera le même clignotement temporaire. Un heartbeat radio de 60 secondes ne doit pas relancer le minuteur.

**Implémentation :** le firmware de la branche de cette évolution affecte D7 à la lumière blanche et D0 au témoin orange ; les différents clignotements sont non bloquants, basés sur `millis()`. **À valider sur table** avec le bouton utilisateur, la puissance LED, l'assemblage complet et la liaison LoRa. La compilation PlatformIO sur matériel réel reste nécessaire.

### Visuels du projet

- [État des deux LED et implantation en façade — schéma SVG](../assets/visuels/leds-garage-v1.svg).
- **Référence esthétique actualisée :** garage blanc/noir posé sur l'étagère, **sans filet bleu**, encadrement de porte propre grâce aux retours intérieurs.
- Le **rendu actualisé** réalisé dans la conversation illustre l'éclairage intérieur et le point orange en façade. Sa porte visible en train de basculer est **un visuel d'ambiance, pas un dessin technique** : dans la V1 mécanique réelle, la porte doit pivoter **vers l'intérieur** et se ranger sous le toit.

## Matériel prévu et références

- Déjà disponible : **2 kits XIAO nRF52840 + Wio-SX1262**, Bambu Lab P1S et AMS, filaments blanc/noir/bleu/rouge ; alimentation secteur disponible dans le vrai garage.
- **1 × SAS308**, Gotronic réf. 26449 : [contact magnétique miniature](https://www.gotronic.fr/art-contact-magnetique-miniature-sas308-12751.htm), **24 × 15 × 6 mm**, écartement aimant **15 mm max.**, câble moulé **25 cm** à prolonger au besoin ; un seul capteur placé pour confirmer la **fermeture** (aimant en face de la porte fermée).
- **1 × DMS-MG90**, Gotronic réf. 36923 : [servomoteur](https://www.gotronic.fr/art-servomoteur-dms-mg90-32266.htm).
- **1 × 470 µF / 16 V**, Gotronic réf. 04947 : [condensateur](https://www.gotronic.fr/art-condensateur-radial-470uf-16v-3386.htm).
- **1 × blanche chaude WCS101 5 mm** + **330 Ω / +5 V** + **BC547B NPN** + **4,7 kΩ D7/base** + **100 kΩ base/GND**, **1 × orange L7113NC 5 mm** + **680 Ω / 3V3** ; [fournitures Gotronic hors noyau](BOM_V1_VERIFIEE.md#fournitures-indispensables-si-absentes), puissance servo distribuée hors cartes, jamais de +5 V de deux sources réunis.

À vérifier au multimètre : comportement des contacts SAS308 (la fiche mentionne « NF », mais décrit une fermeture quand l'aimant est présent). Ne relier **aucun GPIO** au 230 V ou aux bornes du moteur du vrai garage ; conserver toutes les sécurités de la porte.

## Prochaines étapes

1. Mesurer servo, kit radio, ports et antenne ; figer les **cotes réelles** sans dénaturer le rendu choisi.
2. Modéliser et imprimer en priorité **support servo, axe, palier gauche et porte d'essai**.
3. Tester le balayage complet et régler les angles du servo sans point dur.
4. Modéliser la coque finale avec toit amovible, électronique en compartiment arrière et passage de câble.
5. Tester les **deux LED** (blanche sur D7 via transistor BC547B alimenté en +5 V, orange sur D0 via 680 Ω) ; compiler et valider le nouveau firmware sur les cartes.
6. Poser le **SAS308 unique** sur le vrai garage, régler la durée d'ouverture estimée (40 s par défaut), puis tester LoRa, les LED et les cas de panne.

## Précisions dimensionnelles V1 (nouvelle CAO)

- **[Tableau dimensionnel des composants et des réserves](ENCOMBREMENT_BOM_V1.md)** ; [source CAO paramétrique](../cad/generate_cad.py).
- Gabarit décoratif CAO V4 **150 × 100 mm**, hauteur avant **62 mm** et arrière **65 mm** (pente de toit ≈ **1,72°**), parois structurelles **2,4 mm** et toit/socle **3 mm**.
- Jeu d'assemblage **0,30 mm par face** (soit +0,60 mm au diamètre ou à la largeur du logement).
- Servo **en haut à droite de la façade** ; son **boîtier** mesure **22,3 × 11,8 × 26,3 mm** selon DFRobot ; pattes, arbre et palonnier à mesurer. Réserve de service électronique arrière **52 × 23 × 12 mm**, qui **n'est pas la dimension physique** du XIAO/Wio.
- Porte : baie **100 × 42 mm**, vantail **99,4 × 41,4 × 2,4 mm** ; axe **Ø3,2 mm** avec palier **Ø3,8 mm** ; animation vers l'intérieur sous le toit.
- **Un seul capteur** dans le garage réel confirme l'état fermé. L'ouverture et le voyant intérieur sont estimés après un délai sans aimant : cette estimation n'est pas fiable si la porte reste immobilisée à mi-course.

**Correction d'implantation après contrôle STEP :** la LED orange Ø5 mm demeure en haut à droite du linteau, mais son logement est désormais centré à **X = 106,0 mm, Z = 53,3 mm**. Derrière le trou optique Ø2 mm, poche Ø6,6 mm et bosse Ø10,8 mm (paroi locale min. 2,1 mm). Son ancienne position heurtait le servo STEP. Le trajet réel de la porte a été vérifié sur 0–90° par pas de 5° sur la géométrie CAO seulement.

## Historique — correction de façade V3 (coque 190 mm remplacée par V4)

Les deux **joues/retours de tableau** font **2,4 mm d'épaisseur** et se prolongent de **10 mm vers l'intérieur**, à l'extérieur de la baie **110 × 42 mm**. Le **bandeau bleu supérieur est supprimé** des pièces imprimables et de l'assemblage. Le servo reste en haut à droite à l'avant ; l'élargissement de la coque à **190 mm** et la réserve de couplage **3 mm** permettent de dégager sa géométrie STEP du retour droit. Le palier gauche est décalé de **1,6 mm** et la joue gauche possède un passage Ø3,8 mm pour l'axe Ø3,2 mm. **Vérification numérique seulement**, à confirmer avec le vrai DMS-MG90 et le palonnier. Voir [plan de modification](RETOURS_FACADE_V3.md).

## V4 actuelle — réduction de largeur et décentrage

La coque actuelle mesure **150 × 100 mm**, soit **40 mm plus courte** que la V3 ; l'ouverture **100 × 42 mm** est décentrée de **14 mm vers la gauche**. Montant gauche **11 mm**, droit **39 mm**. Porte **99,4 × 41,4 × 2,4 mm**, jeux **0,30 mm par côté**. Le palier est ramené à **5 mm de largeur** et possède une bride de fixation compacte entièrement hors du mur ; le servo et ses pattes restent dans le montant droit. Les joues intérieures **10 mm de profondeur et 2,4 mm d'épaisseur** et le toit en pente sont conservés. Voir [plan V4](IMPLANTATION_COMPACTE_V4.md). Tests numériques de collisions uniquement, pas encore de validation du servo réel et de son palonnier.
