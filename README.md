# Garage miniature LoRa — prototype V1

Projet personnel pour deux kits **Seeed Studio XIAO nRF52840 + Wio-SX1262** (carte Wio sur deux connecteurs 7 broches, **pas** le modèle B2B ESP32-S3).

## Démarrage rapide (projet GitHub)

Ce dépôt contient les **deux firmwares** dans un seul projet PlatformIO.

- `pio run -e emetteur` : compile la carte à installer dans le vrai garage.
- `pio run -e recepteur` : compile la carte intégrée au garage miniature.
- `pio run -e emetteur -t upload` / `pio run -e recepteur -t upload` : flashe chaque carte séparément.
- [Importer les fichiers dans un nouveau dépôt GitHub](docs/GITHUB.md).
- [Protocole LoRa](docs/PROTOCOLE.md).

> **Prototype à valider** : ne pas connecter la carte aux bornes secteur/moteur du garage ; seuls des contacts secs isolés sont utilisés pour la détection. La maquette n'actionne jamais la vraie porte.

## Fonction

- Emetteur dans le garage : deux contacts magnétiques miniatures **SAS308** avec aimants ; contacts **fermés en présence de l'aimant** à chaque fin de course.
- Récepteur dans la maison : servomoteur qui imite la porte, **LED blanche chaude intérieure** et **LED orange de signalisation en façade**.
- Radio LoRa directe 868,125 MHz, sans passerelle / réseau maillé / Internet.
- Etat ferme, ouvert, intermediaire, defaut des capteurs ; un état est dit « intermediaire » même si la porte est immobilisée en cours de trajet.
- Acquittement radio, jusqu'a 3 transmissions par rapport, synchronisation toutes les 60 secondes, invalidation de la liaison après 150 secondes sans message.
- **Aucune commande de la vraie porte de garage**.
- LED orange : 2 Hz durant le déplacement du servo, 1 Hz durant 40 secondes en état intermédiaire, puis fixe ; 5 Hz sur défaut capteurs, double flash sur perte radio. Les fins de course ne mesurent pas le mouvement réel.

## 1 — Matériel

- Deux kits XIAO nRF52840 + Wio-SX1262 avec leurs **antennes 868 MHz** adaptées.
- Deux contacts magnétiques miniatures **SAS308**, Gotronic réf. **26449** (24 × 15 × 6 mm, écart aimant/capteur **15 mm max.**, **25 cm de câble par capteur**, aimants inclus). Tester leur continuité ; un seul capteur reste possible en mode dégradé, voir plus bas.
- Un servomoteur SG90 ou MG90S, une **alimentation 5 V/2 A** pour la miniature, répartie **avant** le XIAO entre USB-C et servo + LED blanche.
- Une **LED blanche chaude** avec **Q1 BC547B**, R1 = **330 Ω** sur +5 V, R2 = **4,7 kΩ** sur D7/base et R3 = **100 kΩ** base/GND ; une **LED orange** 3 mm avec R4 = **680 Ω** sur 3V3.
- Un condensateur électrolytique 470 µF, tension nominale au moins 10 V, près du servo.
- Câblage, dominos ou bornes, support 3D.
- Une alimentation USB-C 5 V dans le garage pour le XIAO émetteur.

## 2 — Connexions

**Les modules LoRa sont déjà connectés à leurs XIAO par la carte Wio.** Pas de câblage SPI supplémentaire.

| Usage | Connexion |
|---|---|
| Emetteur, capteur fermé | D6 vers GND via **SAS308** (contact fermé **lorsque l'aimant est en face**) |
| Emetteur, capteur ouvert | D7 vers GND via second **SAS308** (idem) |
| Récepteur, signal servo | D6 vers fil signal du SG90/MG90S |
| Récepteur, LED intérieure blanche | **D7 → 4,7 kΩ → base BC547B** ; **base → 100 kΩ → GND** ; émetteur → GND ; collecteur → cathode LED blanche ; **+5 V externe → 330 Ω → anode LED** |
| Récepteur, LED orange façade | 3V3 → résistance **680 Ω** → anode LED orange ; cathode → **D0** (allumée par LOW, éteinte en INPUT haute impédance) |
| Servo, fil rouge | 5 V de l'alimentation servo (PAS au 3V3 du XIAO) |
| Servo, fil brun/noir | GND de l'alimentation servo ET GND du XIAO |
| Condensateur | + sur 5 V servo, – sur GND ; attention à la polarité |
| XIAO (chacun) | USB-C 5 V |

Les D6/D7 du XIAO sont disponibles **mais ne sont pas routés sur la carte Wio**. Accéder aux pads/broches correspondants du XIAO monté sur la carte. Vérifier à l'ohmmètre, isoler contre les courts-circuits.

Le SAS308 est livré avec un **câble de 25 cm déjà fixé**, à prolonger au besoin en deux conducteurs correctement isolés ; pas de bornier intégré au capteur. Garder l'aimant idéalement nettement plus près que la limite de 15 mm. Ne jamais raccorder de 230 V ni les bornes du moteur de garage aux GPIO. Eviter tout élément de l'ouvrant qui pourrait accrocher les câbles/capteurs ou perturber les sécurités.

**Servomoteur :** alimenter depuis une source 5 V régulée pouvant fournir au moins ~1 A de pointe ; le XIAO peut être branché sur un second chargeur USB, les GND doivent être communs. Si alimentation unique, utiliser un câble répartiteur 5 V correctement dimensionné pour XIAO + servo. Ne PAS faire passer le courant servo par la sortie 3V3 ni un GPIO.

## 3 — Installer PlatformIO et flasher

1. Installer VS Code et l'extension PlatformIO.
2. Ouvrir le dossier contenant `platformio.ini`.
3. Brancher **un seul kit** en USB-C au PC, avec son antenne 868 MHz connectée.
4. Compiler/flasher l'émetteur : `pio run -e emetteur -t upload`.
5. Débrancher ce kit ; brancher le second et flasher : `pio run -e recepteur -t upload`.
6. Pour voir les logs : `pio device monitor -b 115200`.
7. Si l'upload ne trouve pas le kit : faire deux pressions rapides sur RESET (bootloader UF2) puis réessayer. Les firmwares Meshtastic fournis d'origine seront remplacés ; les sauvegarder au besoin.

Le projet utilise la plateforme PlatformIO personnalisée `maxgerhardt/platform-nordicnrf52`, le framework Arduino pour Seeed et `RadioLib`. Une connexion Internet est nécessaire au premier build.

**Environnement non testé sur ton matériel physique** : les fichiers sont un point de départ complet à compiler puis valider en conditions réelles, pas un firmware binaire garanti prêt à flasher.

## 4 — Premier essai sur table

1. Allumer le récepteur avec le servo **sans aucune porte accrochée** pour éviter les efforts mécaniques au premier mouvement.
2. Allumer l'émetteur sans aimants. Les deux contacts sont ouverts : état intermédiaire (2), servo au milieu.
3. Relier momentanément D6 à GND (ou approcher l'aimant) : état fermé (0), servo vers 15°.
4. Libérer D6 et relier D7 à GND : état ouvert (1), servo vers 95°.
5. Relier les deux simultanément : état défaut (3), le servo reste en place et la LED clignote vite.
6. Débrancher l'émetteur : après 150 secondes sans message, **la LED orange doit faire deux flashs brefs** et la LED blanche s'éteint ; la porte miniature garde sa dernière position mais elle n'est plus considérée fiable.
7. Réalimenter l'émetteur : il transmet immédiatement, la miniature se resynchronise.

Attendre la LED/les logs pour confirmer la bonne réception ; ne pas confondre « non fermé » avec « entièrement ouvert ».

## 5 — Adaptations

- `src/main.cpp` : `ANGLE_CLOSED`, `ANGLE_MIDDLE`, `ANGLE_OPEN` à adapter à l'articulation (15°, 55°, 95° par défaut). Faire les premiers essais servo détaché de la porte.
- `src/main.cpp` : `RADIO_SF` à modifier **sur les deux appareils** si la portée est faible. Tester d'abord en SF8 ; une valeur plus élevée allonge les émissions.
- Si la porte n'a qu'un capteur de fermeture, mettre `-D OPEN_SENSOR_PRESENT=0` dans l'environnement émetteur dans `platformio.ini`. Dans ce mode l'état 1 « ouvert complet » ne sera **jamais** émis : l'état sans fermeture sera 2 « non fermé/intermédiaire ».
- `NETWORK_ID` identique sur les deux appareils. Il filtre les trames accidentelles, sans chiffrement/authentification.

## 6 — Test radio en situation

Placer le premier kit dans le garage réel, second dans la maison. Vérifier les 4 états, puis déclencher au moins 100 changements (manuellement sur les GPIO pour éviter 100 cycles réels du moteur). Noter les ACK manqués et le RSSI. Déplacer les antennes, préférablement loin de la porte métallique, avant d'augmenter le facteur d'étalement.

N'émettre **jamais** sans antenne adaptée raccordée. Pour 868 MHz, respecter la puissance rayonnée autorisée et le temps d'occupation radio applicables en France. Configuration prévue : 868,125 MHz, 125 kHz, SF8, +10 dBm, messages courts. Dans le prototype, une synchronisation est envoyée chaque minute et l'émetteur ne boucle pas indéfiniment sur des retransmissions en cas de panne de liaison. Cela ne dispense pas d'une vérification de conformité pour un produit distribué/commercialisé.

## 7 — Mécanisme de la maquette (v1)

Un garage de 160 x 140 x 120 mm avec porte basculante 95 x 85 mm est la première étape raisonnable, même si la porte réelle est sectionnelle. Le mécanisme retenu place le servo DMS-MG90 **directement et coaxialement** sur l'axe supérieur de la porte, avec un palier imprimé à gauche ; ajouter des butées non forcées. Tester tout le débattement sans frottement et choisir les angles avant de fixer la porte. Un modèle à panneaux articulés sur rails pourra remplacer la façade en v2.


## Conception retenue — porte basculante et éclairage

La V1 conserve le design du **garage noir et blanc au fin liseré bleu posé sur une étagère**. Sa porte monobloc rainurée pivote vers **l'intérieur**, sous le toit, via un **DMS-MG90 monté coaxialement sur la charnière supérieure**, avec un palier côté opposé. Le XIAO + Wio-SX1262 est dissimulé dans une zone arrière hors débattement. Une **LED blanche chaude** sous le toit à l'arrière éclaire l'intérieur à l'état OUVERT ; une **LED orange** discrète en façade indique mouvement et erreurs.

**Lire la [spécification mécanique et électrique V1](docs/CONCEPTION_MECANIQUE_V1.md)** avant la modélisation 3D. Les anciennes cotes et le montage à bielle évoqués plus bas sont des hypothèses initiales, **supplantées par l'entraînement coaxial**. Le firmware **pilote maintenant deux LED** : D7 pour l'intérieur, D0 pour la façade (commande active à LOW). Voir le [schéma des états lumineux](assets/visuels/leds-garage-v1.svg). **Nouveau câblage et code à valider physiquement**.

## Câblage et références vérifiés — V1

- [**Schéma émetteur** : contacts magnétiques D6/D7 → GND](assets/schemas/cablage-emetteur-v1.svg)
- [**Schéma récepteur** : servo D6, LED blanche D7 via BC547B, orange D0](assets/schemas/cablage-recepteur-v1.svg)
- [**Guide technique de câblage** et netlist point à point](docs/CABLAGE_V1_VERIFIE.md)
- [**Liste d'achats / BOM vérifiée**](docs/BOM_V1_VERIFIEE.md)

**Correction importante :** une LED blanche annoncée Vf = 3,5 V peut ne pas être suffisamment éclairée directement par la sortie D7 du XIAO (3,3 V). La LED blanche est désormais alimentée depuis le **+5 V externe via une résistance 330 Ω et un BC547B**. D7 commande seulement la base via **4,7 kΩ**, avec **100 kΩ** de rappel vers GND. Le code D7 actif à HIGH reste compatible. Vérifier **C/B/E**, polarités, masses communes et alimentations avant mise sous tension.

## Sources matérielles

- Seeed XIAO nRF52840 + Wio-SX1262 : https://wiki.seeedstudio.com/xiao_nrf52840%26_wio_SX1262_kit_for_meshtastic/
- Schéma Wio pour XIAO : https://files.seeedstudio.com/products/113010003/Wio-SX1262%20for%20XIAO%20V1.0.pdf
- Meshtastic, brochage de ce kit : https://github.com/meshtastic/firmware/discussions/9424
- RadioLib : https://github.com/jgromes/RadioLib
- Référence PlatformIO (même hardware) : https://github.com/schustercp/TrapLineLoRa
