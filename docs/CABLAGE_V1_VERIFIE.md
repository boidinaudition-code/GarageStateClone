# Câblage V1 — schémas vérifiés et connexions point à point

Révision : 21/11/2026. Ces plans correspondent au projet **GarageStateClone** et au firmware des deux XIAO nRF52840 + Wio-SX1262. Les schémas SVG sont des **vues électriques de principe**, et non des plans de routage PCB ou des dessins de la position physique des broches.

- [Schéma SVG ÉMETTEUR : contacts de la vraie porte](../assets/schemas/cablage-emetteur-v1.svg)
- [Schéma SVG RÉCEPTEUR : servo, deux LED et alimentations](../assets/schemas/cablage-recepteur-v1.svg)
- [Liste d'achats vérifiée et liens vendeurs](BOM_V1_VERIFIEE.md)

## Mise à jour V8 — alimentation USB-C intégrée (22 novembre 2026)

**Référence courante pour le 5 V du récepteur : [ALIMENTATION_USB_C_V8.md](ALIMENTATION_USB_C_V8.md).** Le câblage des D6/D7/D0 et le schéma de principe des LED ci-dessous restent valides, mais l'ancienne option « deux alimentations 5 V côté miniature » **n'est plus l'architecture privilégiée**.

Une seule alimentation **5 V USB-C / 2 A minimum** alimente la **platine Gotronic 49067** intégrée au socle de la miniature : **VBUS et GND** → petit bus sur plaque à pastilles → deux départs séparés, (**A**) broches **5V/VBUS et GND du XIAO nRF52840 récepteur**, (**B**) fils **rouge +5 V et marron/noir GND du DMS-MG90**. Le **condensateur 470 µF / 16 V** reste en parallèle du servo (polarité respectée) ; **D6 reste le signal 3,3 V** ; R1 de LED blanche reçoit le même bus 5 V. **Ne pas puiser le courant du servo dans le XIAO ou son 3V3.**

Deux borniers **Gotronic 48930** peuvent fournir les deux sorties démontables, **sur un morceau distinct de BCS050 12470**. Il faut vérifier si la platine USB-C 49067 intègre déjà les **deux résistances Rd de 5,1 kΩ** (CC1 et CC2 vers GND) ; à installer uniquement si absentes pour fonctionner correctement avec une source USB-C. **Pendant la programmation du XIAO par USB-C relié au PC, retirer l'alimentation 5 V externe** ou prévoir une isolation de sources réellement vérifiée. Ne pas confondre les limites constructeur USB-C jusqu'à 20 V avec la tension acceptable du servo : **l'ensemble est conçu pour 5 V, sans USB-PD supérieur**.

Le support USB-C V8 est **intégré au socle**, ouverture arrière de **13 × 8 mm** et deux tunnels de collier ; la **position précise du connecteur femelle** reste **à mesurer**, le contour de service n'étant pas validé comme trou affleurant. Voir la [notice CAO et montage](ALIMENTATION_USB_C_V8.md).

## 1. Variante de matériel : impératif

Les plans concernent le **Seeed XIAO nRF52840**, associé au **Wio-SX1262 à deux barrettes 7 broches** (et NON au Wio-SX1262 B2B destiné à l'ESP32-S3).

Sources :
- [Schéma Seeed du Wio-SX1262 pour XIAO V1.0 (PDF)](https://files.seeedstudio.com/products/113010003/Wio-SX1262%20for%20XIAO%20V1.0.pdf)
- [XIAO nRF52840 : brochage et niveau logique 3,3 V](https://wiki.seeedstudio.com/XIAO_BLE/)

Correspondance logique confirmée :

| Signal | XIAO nRF52840 | Affectation firmware |
|---|---|---|
| D0 | P0.02 | Récepteur : LED orange, **partagé avec bouton Wio** |
| D1 | P0.03 | LoRa DIO1 |
| D2 | P0.28 | LoRa RESET |
| D3 | P0.29 | LoRa BUSY |
| D4 | P0.04 | LoRa NSS |
| D5 | P0.05 | LoRa RF switch |
| D6 | P1.11 | Émetteur : capteur fermé / Récepteur : SIG servo |
| D7 | P1.12 | Émetteur : **libre, un seul SAS308 sur D6** / Récepteur : commande transistor LED blanche |
| D8 / D9 / D10 | P1.13 / P1.14 / P1.15 | SPI radio SCK / MISO / MOSI |

Sur le schéma du Wio V1.0, **D0 va à un bouton relié à GND et un pull-up de 10 kΩ à +3V3**. D6/D7 ne sont **pas câblées au module Wio** : elles restent utilisables sur les **pastilles du XIAO**, à condition de pouvoir y accéder avec le module enfiché. Prévoir des fils soudés et isolés à la bonne position ; vérifier le câblage sur les cartes réellement reçues à l'ohmmètre.

## 2. Émetteur, installé à proximité de la vraie porte

| Départ | Arrivée | Explication |
|---|---|---|
| Chargeur USB secteur 5 V isolé | USB-C de XIAO émetteur | Alimentation de la carte uniquement |
| XIAO D6 | **Fil 1** du SAS308 « fermé » (prolongé si besoin) | Contact sec, entrée INPUT_PULLUP |
| XIAO D7 | **Libre / non raccordé côté émetteur V1** | L'ancien second contact a été supprimé |
| XIAO GND | **Fil 2 du seul SAS308** | Référence du contact sec |
| Module Wio SX1262 | Antenne 868 MHz prévue pour ce module | Antenne installée avant toute émission |

Logique attendue : **aimant présent en face = contact fermé = entrée à LOW** ; aimant absent = circuit ouvert = HIGH via pull-up interne. La fiche du SAS308 emploie le terme « NF » mais indique explicitement **fermé avec l'aimant en face** ; vérifier le comportement au multimètre. Mesurer la continuité aimant proche/éloigné avant pose. En mode un seul contact, l'état « défaut capteurs simultanés » ne peut pas être produit normalement. Après 40 s sans aimant, un état « ouvert » est **estimé** pour l'animation uniquement.

⚠️ Ce capteur n'est **pas raccordé au moteur** : jamais de 230 V, de sortie relais de motorisation ou de connecteur de sécurité sur un GPIO. Installer hors des pièces mobiles, des ressorts et des galets. Le **SAS308 est très plat (24 × 15 × 6 mm)** ; la distance **maximale** annoncée avec son aimant est de **15 mm** (prévoir une marge). Il comporte **25 cm de câble déjà moulé**, sans bornier à vis : prolonger sa paire de fils proprement et protéger les jonctions de l'humidité.

## 3. Récepteur, dans le garage miniature

### 3.1 Netlist des composants

| Signal ou nœud | Liaison physique **à réaliser** |
|---|---|
| **D6 XIAO** | Signal de commande du servo DMS-MG90 seulement |
| **+5V_EXT** | +5 V du répartiteur USB vers + alimentation servo, **borne + du condensateur 470 µF**, et une extrémité de R1 330 Ω |
| **GND_COMMUN** | GND du XIAO, GND alimentation servo, GND servo, **borne − condensateur**, **émetteur E de Q1** et bas de R3 100 kΩ |
| **LED blanche** | +5V_EXT → **R1 330 Ω** → **anode A** de la LED blanche → **cathode K** vers **collecteur C de Q1** |
| **Q1 BC547B** | **Collecteur C** ← cathode LED blanche ; **émetteur E → GND** ; **base B** raccordée à R2 et R3 |
| **D7 XIAO** | D7 → **R2 4,7 kΩ** → **base B de Q1** |
| **R3** | **Base B de Q1 → R3 100 kΩ → GND** (maintien à l'arrêt au démarrage) |
| **LED orange façade** | **3V3 XIAO → R4 680 Ω → anode A** LED orange → **cathode K → D0 XIAO** |
| **USB-C XIAO** | Branche 5 V dédiée aux circuits du XIAO/Wio ; ne pas faire passer la puissance du servo dans le 3V3 |

Un **BC547B NPN TO-92** a trois broches, collecteur (C), base (B), émetteur (E) : **vérifier son brochage dans la notice du lot livré**, ne pas inférer l'ordre uniquement du nom « TO-92 ».

### 3.2 Pourquoi un transistor pour la LED blanche ?

La version initiale prévoyait D7 → 330 Ω → LED blanche → GND. Ce câblage **n'est pas une garantie de luminosité** : une LED blanche Gotronic classique est spécifiée à **Vf ≈ 3,5 V**, alors que D7 ne sort que **3,3 V**.

**V1 Gotronic :** le XIAO commande la **base du BC547B**, tandis qu'une **blanche chaude 5 mm du lot Whadda WCS101 (03989)** reçoit le 5 V externe via **330 Ω**. La fiche du lot confirme 20 blanches chaudes mais ne précise pas leur Vf/courant admissible : **mesurer le courant et tester l'éclairage**, ne pas lui attribuer les valeurs de l'ancienne LED. Ne choisir ni RGB ni LED de puissance **1 W/3 W**. Aucun changement de logique firmware.

Le code **ne change pas de logique** : D7 HIGH → Q1 conducteur → LED allumée. D7 LOW → LED éteinte. R3 100 kΩ évite l'allumage intempestif lorsque la sortie est flottante.

### 3.3 Voyant orange D0 : bouton partagé

Le schéma Seeed du Wio confirme **D0 → bouton vers GND** et **résistance de rappel 10 kΩ à +3V3**. La LED orange ne doit donc pas être câblée entre D0 et GND en sortie HIGH.

Câblage confirmé : **+3V3 → R4 680 Ω → anode de LED orange → cathode sur D0**. Le firmware met D0 en sortie **LOW pour allumer** (~2 mA pour Vf orange ≈ 2 V) et le remet en **INPUT haute impédance pour éteindre**. Un appui sur le bouton peut alors allumer la LED, sans intérêt pour le fonctionnement habituel.

Orange retenue : **L7113NC 5 mm, Gotronic 03051**, claire, non clignotante ; 80 mcd à 10 mA et angle 15° annoncés, pas une luminosité garantie avec **680 Ω**. Vf et courant réel à confirmer. La cacher en retrait derrière une petite ouverture façade : pas besoin d'exposer les 5 mm.

Attention : ne **jamais** mettre D0 en sortie HIGH dans cette topologie.

### 3.4 Alimentation sûre du servo et de la LED blanche

- **Émetteur** : son propre chargeur USB-C 5 V.
- **Récepteur** : **un chargeur USB 5 V / 2 A minimum** ; prévoir **un véritable répartiteur de puissance** externe, avant les cartes, pour séparer (A) l'USB-C du XIAO et (B) les conducteurs 5 V/GND dédiés au servo et à R1.
- Variante acceptable : deux chargeurs USB 5 V différents côté miniature, **un dédié au XIAO, l'autre au servo + LED blanche**. Dans ce cas **réunir les GND** ; **ne jamais réunir les deux bornes +5 V** des chargeurs.
- Le **condensateur 470 µF / 16 V est polarisé** : + au +5 V servo, bande négative sur GND, au plus près du connecteur servo. Il aide mais ne remplace pas une vraie alimentation adaptée aux appels de courant.
- Les modules émetteur et récepteur ne partagent **aucun fil** entre eux : radio uniquement.
- Les deux antennes doivent être installées avant usage.

Pour la variante séparée : [HNP18-USBV2 14749](https://www.gotronic.fr/art-alimentation-hnp18-usbv2-38701.htm) **5 V / 3 A**, puis [cordon USB-A → DC 49101](https://www.gotronic.fr/art-cordon-usb-alim-5-5-x-2-1-mm-34157.htm) (**2 A maxi**) et [bornier PCM10F 48214](https://www.gotronic.fr/art-adaptateur-pcm10f-17984.htm). Le + du bornier alimente servo/C1/R1 uniquement ; le − rejoint leur GND et celui du XIAO. **Le +5 V USB du chargeur XIAO reste séparé.** Vérifier les polarités et isoler les connexions avant branchement. Deux chargeurs côté miniature, donc **trois au total** avec l'émetteur. [Fournitures et limites des références](BOM_V1_VERIFIEE.md#fournitures-indispensables-si-absentes).

**Pas de 5 V appliqué directement aux GPIO.** Ne jamais alimenter le servo depuis le 3V3 de XIAO ou les petites pistes de son module.

## 4. Implantation physique retenue

Porte monobloc noire à rainures horizontales, **bascule vers l'intérieur** autour de son axe en haut de façade, actionnée directement par le **DMS-MG90 à droite**, palier à gauche.

- LED **orange** discrètement encastrée en haut à droite de façade (deux conducteurs longeant la paroi).
- LED **blanche chaude** sous le toit près de la paroi arrière, dirigée vers le sol et **en dehors du débattement** de la porte.
- BC547B, résistances, XIAO/Wio et connectique dans un compartiment arrière, **hors trajectoire** de la porte.
- C1 près des bornes servo, même si le reste du circuit est plus loin.
- Toit amovible ; port USB-C et antenne accessibles ; fils fixés et isolés.

## 5. Essai sur table avant installation

1. Couper l'alimentation. Installer les **deux antennes LoRa** et vérifier l'absence de court-circuit.
2. Contrôler le **SAS308 unique** au multimètre avec et sans son aimant.
3. Contrôler **C/B/E de Q1**, les résistances (330 / 680 / 4,7 k / 100 k) et **les polarités des 2 LED**.
4. Contrôler l'orientation du **470 µF** ; mesurer le 5 V du servo puis le 3,3 V du XIAO.
5. Alimenter le **récepteur avec le servo sans porte**. Tester les trois positions sans blocage ni surchauffe.
6. Simuler FERMÉ (aimant présent sur D6), puis NON FERMÉ (aimant retiré) ; dès réception LoRa, vérifier l'ouverture continue du servo de 90° à 0° en 5 s (course 90°, sens inversé), sans pause, puis LED blanche allumée et orange fixe. Le retour de l'aimant commande la fermeture en 2 s. La trame OPEN estimée après 40 s ne relance pas le mouvement.
7. Appuyer brièvement sur le bouton D0 **uniquement si le câblage est vérifié** : noter que la LED orange peut aussi s'allumer.
8. Tester la perte radio en arrêtant l'émetteur plus de 150 s. Le défaut « deux fins de course actives » n'est pas testable avec un seul contact.

## Références des vérifications

- [PDF schéma Wio-SX1262 pour XIAO V1.0](https://files.seeedstudio.com/products/113010003/Wio-SX1262%20for%20XIAO%20V1.0.pdf)
- [Seeed XIAO nRF52840 : pinout](https://wiki.seeedstudio.com/XIAO_BLE/)
- [Gotronic : SAS308](https://www.gotronic.fr/art-contact-magnetique-miniature-sas308-12751.htm)
- [Gotronic : DMS-MG90](https://www.gotronic.fr/art-servomoteur-dms-mg90-32266.htm)
- [Gotronic : LED blanche Vf 3,5 V](https://www.gotronic.fr/art-led-3-mm-l3fwc1-35813.htm)

## V1 — actualisation capteur unique

**Un seul SAS308 est monté** : D6→contact→GND, aimant en face **si la vraie porte est fermée**. D7 n'est pas raccordé côté émetteur. Le capteur est placé en position fixe hors des éléments mobiles, seul l'aimant suit la porte. [Cotes exactes et inconnues](ENCOMBREMENT_BOM_V1.md).

**Estimation décorative d'ouverture :** après 40 s sans aimant (configurable), l'émetteur annonce l'état OPEN *estimé* ; le récepteur anime désormais l'ouverture dès le premier état NON FERMÉ et allume la LED blanche en fin de mouvement. C'est inexact si la vraie porte reste arrêtée entre les fins de course. **Ce montage n'est pas une sécurité de fermeture.**

## Implantation V5 : alimentation et cartes dans les combles

Le **schéma électrique ne change pas** : XIAO/Wio en combles au-dessus d'un faux plafond amovible à l'arrière ; D6 vers le servo en façade, D7 vers la base du BC547B (LED blanche sous le faux plafond), D0 vers la LED orange en façade ; masses communes et alimentation **5 V externe distincte du 3V3**. Le condensateur de 470 µF reste proche du servo. Prévoir **un faisceau basse tension sécurisé** depuis la zone sous toiture vers le servo et les deux LED, arrimé à la paroi et sans passer par le volume balayé par la porte. La fente arrière haute 16 × 9 mm est une réserve provisoire pour câble, **pas une cote USB-C validée** ; éviter tout pincement lors de la repose du toit. [Implantation précise V5](TOIT_COMBLES_V5.md).
