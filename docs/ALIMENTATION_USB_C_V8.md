# Alimentation USB-C 5 V et platine Gotronic 49067 — V8

**22 novembre 2026 · GarageStateClone, version mécanique CAO V8** (socle et sortie arrière seulement ; servo V7 et firmware inchangés). **Prototype : les interfaces sont contrôlées en CAO, pas sur le composant réel.**

> **Version courante V10 (22/11/2026) :** ce document conserve l'historique et la nomenclature électriques V8, qui restent valables. La **coque** a changé : **ouverture USB-C réduite et provisoire 10 × 4,2 mm à Z9,45**, suppression complète de la **sortie haute 16 × 9 mm**, ajout d'une **goulotte interne arrière** de Z14 à Z43 pour les câbles montant vers les combles. Consulter [la révision mécanique V10](EVOLUTION_FACADE_CABLAGE_V10.md) plutôt que les anciens chiffres de découpe ci-dessous. Le vrai connecteur 49067 doit toujours être mesuré.

## 1. Architecture électrique

**Une seule alimentation secteur USB 5 V régulée, 2 A minimum**, raccordée à une **platine USB-C femelle Gotronic 49067**, alimente **en parallèle** le récepteur XIAO/Wio et le servo DMS-MG90. L'émetteur LoRa placé dans le vrai garage conserve son alimentation USB indépendante.

```text
     Chargeur USB 5 V / >= 2 A (source fixe 5 V ; pas de PD 9/12/20 V)
                  |
               USB-C
                  |
       Gotronic 49067 (femelle)
          VBUS / GND
             |  |
       +-----+--+---------+  distribution 5 V / masse sur pastilles soudées
       |                  |
   5 V / GND          5 V / GND
       |                  |
  XIAO nRF52840       SERVO DMS-MG90
  + Wio-SX1262        + condensateur 470 µF/16 V près du moteur
       |
  D6 (signal PWM 3,3 V) ------------------------> servo signal
  D7 -> R2 -> BC547B -> LED blanche alimentée par le 5 V du bus
  D0 -> LED orange (schéma existant, alimentée en 3,3 V)
```

- **VBUS +5 V 49067** → piste/bus +5 V → sortie A vers **5V/VBUS** du XIAO + sortie B vers **fil rouge** du servo ; +5 V vers **R1 330 Ω** pour la LED blanche.
- **GND 49067** → bus commun GND → sortie A vers **GND XIAO** + sortie B vers **fil marron/noir** du servo + émetteur du BC547B et condensateur C1.
- **D6** XIAO → **fil de commande** servo (ne pas lui fournir 5 V).
- **470 µF / 16 V** : borne **+** sur +5 V, bande négative **−** sur GND, **au plus près du servo**.
- **Interdit :** servo sur le 3V3 XIAO, buck 3,3→5 V, pontage de deux chargeurs différents sur la même ligne +5 V, +5 V sur GPIO.
- Préférer du **fil souple d'environ 0,25 mm²** sur le faisceau de puissance court, une connexion soudée et isolée, sans faire passer le courant du servo dans les pistes de la carte XIAO. Ces sections sont des **préconisations de montage**, pas une cote fabricant.
- Le circuit de commande et les niveaux logiques du firmware demeurent inchangés (D6 servo, D7 LED blanche, D0 orange).

### Mise en garde : programmation USB et double source

Sur XIAO nRF52840, la broche **5V est VBUS**. Si le XIAO reçoit déjà le 5 V de la distribution, **ne pas brancher simultanément son USB-C à un PC alimentant VBUS** sans vérifier/isoler le chemin d'alimentation, sous peine de rétroalimenter les ports ou les deux sources. Pour flasher : **débrancher la distribution 5 V extérieure** et alimenter uniquement le XIAO par l'USB-C de programmation. Le câble de programmation ne doit jamais être le chemin d'alimentation du servo.

Source de brochage : [Seeed XIAO nRF52840](https://wiki.seeedstudio.com/XIAO_BLE/).

### Broches CC1/CC2 de l'USB-C

Gotronic **ne confirme pas** que la 49067 possède déjà les résistances de configuration **Rd**. Pour une source **USB-C vers USB-C**, un appareil récepteur 5 V standard doit généralement présenter **une résistance de 5,1 kΩ entre CC1 et GND et une seconde indépendamment entre CC2 et GND**. Ne les ajouter **que si elles sont absentes**, après examen de la platine et éventuellement du schéma; ne pas relier CC1 à CC2. **Ni la présence de résistances ni un profil USB-PD supérieur à 5 V ne sont attestés.**

La cote 20 V / 5 A mentionnée par Gotronic est une **limite du composant**, pas une autorisation à appliquer 20 V au XIAO ou au servo. Seule la tension **5 V** est prévue ici.

## 2. BOM Gotronic supplémentaire — distincte du noyau à 23,43 €

| Référence | Qté à commander si manquante | Coût indicatif TTC | Montage |
|---|---:|---:|---|
| [Platine USB-C 2.0 **49067**](https://www.gotronic.fr/art-platine-a-connecteur-usb-type-c-2-0-31137.htm) | **1** | **4,95 €** | Entrée 5 V / GND, intégrée dans le socle imprimé |
| [Bornier SC02/2.54 **48930**](https://www.gotronic.fr/art-bornier-sc02-2-54-15468.htm) | **2** | **1,60 €** | Deux sorties 5 V + GND sur **plaque à pastilles séparée** ; la platine 49067 n'est pas une barrette à vis |
| [Résistances **5,1 kΩ 15944** (lot de 5)](https://www.gotronic.fr/art-5-resistances-1-2w-5-1-k-8486-8829.htm) | **1 lot si les Rd sont absentes** | **0,30 €** | Une sur CC1 et une sur CC2, côté récepteur USB-C |
| [Plaque à pastilles **BCS050 12470**](https://www.gotronic.fr/art-plaque-d-essais-bcs050-6931.htm) | **1 si pas déjà achetée** | **1,40 €** | Déjà prévue pour l'électronique ; en découper un morceau pour la distribution |

**Surcoût indispensable si les 2 borniers sont achetés : 6,55 €** (4,95 + 2 × 0,80). Jusqu'à **8,25 €** pour les quatre lignes si aucune n'est déjà en stock et si les résistances Rd sont nécessaires. Le total indicatif du noyau électronique historique **23,43 €** n'a pas été discrètement modifié : avec tous les accessoires ci-dessus, il devient **31,68 €**, hors alimentation secteur, câble, soudure, gaines, quincaillerie et livraison. Vérifier les prix au panier.

**Attention** : les borniers SC02/2.54 mesurent environ **8,5 mm de haut**, doivent être soudés sur un circuit à pastilles, et leur position 3D exacte **n'est pas encore modélisée**. Deux borniers sont suffisants pour les deux branches à deux conducteurs; les autres départs 5 V (R1, C1) sont des dérivations soudées.

## 3. Implantation CAO du support USB-C

D'après la fiche officielle Gotronic : **21 × 15 × 4,5 mm** hors tout, **10 pastilles au pas de 2,54 mm**, sans position de la prise ni entraxe des éventuels perçages publiés. On prend une **enveloppe simplifiée** et non un STEP fabricant.

**Repères de la miniature :** X gauche→droite, Y avant→arrière, Z bas→haut, millimètres.

| Élément CAO V8 | Position / dimension | Statut |
|---|---|---|
| **Carte 49067 fictive** | X **67,50..82,50**, Y **74,40..95,40**, Z **9,30..13,80** | Enveloppe **15 × 21 × 4,5**, USB supposé orienté vers l'arrière +Y ; connecteur réellement non mesuré |
| **Support sur le socle noir** | X **63,90..86,10**, Y **72,40..96,60**, face haute **Z9,00** | **Intégré à la pièce `02_socle_noir`**, maintien indépendant du perçage de la carte |
| Guides latéraux | **2,4 mm** largeur × **3,4 mm** hauteur | Réserve latérale ; aucun clipsage forcé sur les composants de la platine |
| Deux tunnels sous le support | Y **79,00..82,20** et **89,50..92,70**, largeur libre **3,2 mm**, hauteur **2,7 mm** | Deux colliers nylon **2,5 mm**, boucle par-dessous puis par-dessus carte avec isolant mou, sans serrer la prise ni les CMS |
| **Ouverture arrière USB-C** | X **68,50..81,50** ; Z **8,50..16,50** ; traverse le mur arrière Y≈97,6..100 | **HISTORIQUE V8 13 × 8 mm, remplacée par 10 × 4,2 mm en V10**, *pas encore* le contour exact du nez USB-C |
| Ancienne sortie basse des fils | Ancienne fente **12 × 8 mm**, désormais **supprimée** | Une seule ouverture basse visible à l'arrière |
| Sortie haute en combles | **16 × 9 mm**, vers Z49..58 | **SUPPRIMÉE en V10** : fils dans goulotte intérieure, la carte radio reste en combles |

La carte est fixée **sans inventer les trous de vis** : deux guides + deux colliers dans le support bas. Ajouter une fine isolation souple entre bande et carte ; contrôler que rien ne touche le connecteur. La façade blanche et le toit amovible sont conservés ; la version courante V10 a **150 × 100 mm** au sol et **9 pièces imprimables**, avec **12 STEP** (la boîte noire est indépendante).

Le gabarit `REF_USB_C_49067_GABARIT_NON_CONTRACTUEL_NE_PAS_IMPRIMER` apparaît dans l'assemblage STEP **avec références** ; le STEP structure seule comporte le support mais pas le gabarit. Fichiers de sortie générés, non versionnés dans Git : `cad/stl/02_socle_noir.stl`, `cad/step/02_socle_noir.step` et les deux STEP d'assemblage (noms historiques V2 maintenus).

### À mesurer à réception pour obtenir une vraie prise affleurante

1. Distance **nez USB-C femelle → extrémité PCB** le long des **21 mm**.
2. Position **gauche/droite et hauteur Z du connecteur** par rapport au PCB, éventuelles pattes de fixation, tête des composants.
3. Longueur d'insertion du **câble USB-C mâle**, passage de son corps plastique dans l'ouverture, effort d'arrachement.
4. Présence des **2 résistances Rd** sur CC1 et CC2, pas seulement la continuité apparente de VBUS/GND.
5. La carte réellement livrée correspond-elle à **21 × 15 × 4,5 mm** ? Débattement des guides et hauteur des soudures sans la barrette de pins fournie.

**Ne pas imprimer le socle définitif avant ce montage à blanc si une prise totalement affleurante est requise.** Ne pas recourir au perçage ou à la lime près d'une carte branchée.

## 4. Séquence de montage et mise sous tension

1. Imprimer le **socle** et présenter la **49067 hors tension**, avec un câble USB-C mâle dans son embase. Vérifier ouverture et assise (avec un modèle plat en carton au besoin). **Pas de faux entraxe de vis**.
2. Souder deux fils +5 V et GND sur les pastilles identifiées de la platine **sans installer une barrette de pins** qui augmenterait la hauteur au-delà des 4,5 mm publiés. Isoler les points de soudure.
3. Créer un **petit bus à deux pistes séparées +5 V / GND** sur la plaque BCS050, avec départs à deux borniers 48930 pour XIAO et servo, dérivations vers R1 et C1. Contrôler au multimètre **qu'il n'y a pas de court-circuit** entre + et −.
4. Arrimer la platine aux **2 canaux de colliers**, en prévoyant une isolation entre la bande et les CMS, un mou de service vers le bus et une **retenue du câble** indépendamment des soudures.
5. Vérifier CC1/CC2 et la polarité sur le câble choisi, puis mesurer **5 V à vide** sur le bus, **avant** de brancher XIAO et servo.
6. Brancher XIAO + Wio et tester ses **3,3 V** internes, puis brancher le servo sans palonnier ni porte, surveiller baisses de tension et échauffements. Monter le mécanisme seulement après vérification de ses vis et de son palonnier.
7. Pour tout flash : **retirer l'alimentation externe 5 V** du XIAO avant de brancher un PC en USB-C.

## 5. Vérifications automatisées et limite

Les tests garantissent la validité du **socle imprimable**, des deux **tunnels ouverts**, de la **découpe arrière**, de l'enveloppe 49067 **sans interférence** avec coque, porte, base, servo, de l'intégrité STL/STEP et des états de documentation. Le modèle ne **certifie pas** le nez de connecteur, l'assemblage réel, les résistances CC intégrées, les valeurs de courant, la fixation de la perfboard ni la programmation USB simultanée.

Sources : [Gotronic 49067](https://www.gotronic.fr/art-platine-a-connecteur-usb-type-c-2-0-31137.htm) · [Gotronic 48930](https://www.gotronic.fr/art-bornier-sc02-2-54-15468.htm) · [Gotronic 15944](https://www.gotronic.fr/art-5-resistances-1-2w-5-1-k-8486-8829.htm) · [Gotronic 12470](https://www.gotronic.fr/art-plaque-d-essais-bcs050-6931.htm) · [Seeed XIAO pinout](https://wiki.seeedstudio.com/XIAO_BLE/).
