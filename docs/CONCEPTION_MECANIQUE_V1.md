# GarageStateClone — V1 retenue : mécanique et éclairage

**Décisions du 21/11/2026 — spécification de conception, pas encore STL ni firmware validé.**

## Design extérieur retenu

Référence visuelle **exacte** : le garage miniature noir et blanc avec un fin liseré bleu, posé sur une étagère en bois dans l'image explicitement sélectionnée par l'utilisateur.

- Garage bas, rectangulaire, sobre et discret, comme un objet de décoration.
- Murs **blancs**, toit plat **noir**, porte **noire** à rainures horizontales, **liseré bleu très fin** au-dessus de la porte.
- Pas de façade chargée ni de décoration rouge.
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
| **Face arrière** | Passage discret des alimentations USB / des fils et accès de maintenance |

Placer l'antenne 868 MHz sans contact avec des pièces métalliques et, si possible, loin du servo et des fils 5 V. Tester la liaison dans la coque fermée.

**Alimentation :** le servo reçoit une alimentation **5 V régulée**, source capable de supporter ses appels de courant (alimentation USB 5 V/2 A envisagée). **Ne jamais alimenter le servo depuis 3V3 du XIAO ni un GPIO.** Relier les GND. Condensateur **470 µF / 16 V** sur le 5 V/GND près du servo, en respectant la polarité.

## Éclairage V1 : une seule LED

**Décision : pas de ruban LED.** Installer **une LED blanche chaude à haut rendement**, de préférence diffusante, dans un support discret sous le plafond **près du fond du garage**, à distance de la zone où passe la porte.

### Branchement prévu sur le XIAO récepteur

~~~text
D6 --------------------------- fil signal du servo DMS-MG90
D7 --- résistance 330 ohms --- anode (+) de la LED blanche
GND -------------------------- cathode (-) de la LED
5 V externe ------------------ alimentation (+) du servo
GND commun ------------------- alimentation (-) servo et GND XIAO
~~~

La LED est commandée directement par la **sortie 3,3 V D7**, **à faible courant**, avec la résistance en série : **aucune tension 5 V sur D7**. Avec une LED blanche, la chute de tension peut être proche de 3,3 V : acheter une LED efficace à faible courant et vérifier la luminosité avant de figer le support.

### Règles fonctionnelles souhaitées

| État radio valide / porte réelle | Porte miniature | LED d'ambiance |
|---|---|---|
| FERMÉE | Fermée | Éteinte |
| INTERMÉDIAIRE | Mi-course | Éteinte |
| OUVERTE | Ouverte | **Allumée fixe** |
| Perte de liaison / défaut capteurs | Dernière position connue, non garantie | **Éteinte** |

**Important : mise à jour logicielle non effectuée.** Le firmware actuel utilise **D7 comme LED d'état** et la fait **clignoter** en cas d'anomalie. Avant utilisation comme éclairage intérieur, il faut modifier la fonction de mise à jour de cette sortie pour qu'elle ne s'allume que lorsque **OUVERTE** est confirmé et que la liaison est récente. Les défauts seront alors gérés par les journaux série ou un indicateur distinct.

## Matériel prévu et références

- Déjà disponible : **2 kits XIAO nRF52840 + Wio-SX1262**, Bambu Lab P1S et AMS, filaments blanc/noir/bleu/rouge ; alimentation secteur disponible dans le vrai garage.
- **2 × SAS301**, Gotronic réf. 26444 : [contact magnétique](https://www.gotronic.fr/art-contact-magnetique-1t-sas301-12746.htm) ; un en fin de course fermée, un en fin de course ouverte.
- **1 × DMS-MG90**, Gotronic réf. 36923 : [servomoteur](https://www.gotronic.fr/art-servomoteur-dms-mg90-32266.htm).
- **1 × 470 µF / 16 V**, Gotronic réf. 04947 : [condensateur](https://www.gotronic.fr/art-condensateur-radial-470uf-16v-3386.htm).
- **1 × LED blanche chaude faible courant**, **1 × résistance 330 Ω**, fil et petit bornier, vis, palonnier, alimentation USB 5 V/2 A et câbles.

À vérifier au multimètre : comportement des contacts SAS301 (la fiche mentionne « NF », mais décrit une fermeture quand l'aimant est présent). Ne relier **aucun GPIO** au 230 V ou aux bornes du moteur du vrai garage ; conserver toutes les sécurités de la porte.

## Prochaines étapes

1. Mesurer servo, kit radio, ports et antenne ; figer les **cotes réelles** sans dénaturer le rendu choisi.
2. Modéliser et imprimer en priorité **support servo, axe, palier gauche et porte d'essai**.
3. Tester le balayage complet et régler les angles du servo sans point dur.
4. Modéliser la coque finale avec toit amovible, électronique en compartiment arrière et passage de câble.
5. Tester la LED seule, puis **adapter le firmware D7** ; compiler et valider sur le matériel.
6. Poser les capteurs réels, tester la communication LoRa et les cas de panne.
