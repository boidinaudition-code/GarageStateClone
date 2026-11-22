# GarageStateClone — miniature de porte de garage connectée (LoRa)

**Statut : prototype mécanique V6, novembre 2026.** Une miniature décorative posée sur une étagère suit *approximativement* l’état d’une vraie porte de garage, sans jamais commander son moteur. Deux kits **Seeed XIAO nRF52840 + Wio-SX1262**, lien LoRa 868 MHz point à point. La miniature est imprimable en plusieurs pièces sur une **Bambu Lab P1S**.

**Version courante : V6.** Les anciennes mentions « V1–V5 » dans certains documents sont des **archives de conception**, pas des instructions dimensionnelles à utiliser pour fabriquer V6.

## Sommaire

1. [Ce que fait réellement le système](#ce-que-fait-réellement-le-système)
2. [Design et cotes V6](#design-et-cotes-v6)
3. [Mécanisme, supports et fixations](#mécanisme-supports-et-fixations)
4. [Liste de pièces et coûts](#liste-de-pièces-et-coûts)
5. [Câblage et alimentation](#câblage-et-alimentation)
6. [Générer et imprimer la CAO](#générer-et-imprimer-la-cao)
7. [Compiler les deux firmwares](#compiler-les-deux-firmwares)
8. [Tests, documentation et limites](#tests-documentation-et-limites)

## Ce que fait réellement le système

**Côté vrai garage** : un **seul contact magnétique SAS308** est disposé pour être fermé lorsque la porte réelle est complètement fermée. Un émetteur XIAO/Wio placé à proximité transmet son état via LoRa, sans Wi-Fi.

**Côté maison** : un second XIAO/Wio anime un **microservo MG90**, une **LED orange** en façade et une **LED blanche** à l’intérieur de la miniature. Les deux kits possèdent chacun leur antenne **868 MHz**.

| Situation | Observation réelle | Affichage miniature |
|---|---|---|
| SAS308 fermé, aimant devant | **Fermeture confirmée** | Porte miniature fermée, LEDs éteintes |
| SAS308 ouvert, moins de 40 s | Porte **non fermée** (position exacte inconnue) | Position intermédiaire, orange clignotante |
| SAS308 ouvert depuis 40 s | **Ouverture estimée**, non mesurée | Porte miniature ouverte, blanche allumée, orange fixe |
| Radio sans trame valide depuis >150 s | Statut périmé | Dernière consigne mécanique maintenue, blanche éteinte, orange en double flash |

**Important :** la porte réelle peut rester bloquée à mi-course et être affichée ouverte après 40 secondes. Ce n’est **pas** une télécommande, une alarme, une détection de personnes ni une sécurité de motorisation. Le réseau LoRa n’est **pas authentifié**. Aucune liaison au secteur 230 V ni au moteur réel ne doit être réalisée.

Le récepteur commande actuellement le servo entre **15° (fermé) et 95° (ouvert estimé)**, soit **80° de déplacement servo**. Le modèle mécanique est contrôlé sur un balayage **0–90°**, mais les angles finaux devront être calibrés après montage réel du palonnier.

## Design et cotes V6

| Élément | Valeur V6 actuelle |
|---|---:|
| Coque extérieure | **150 × 100 mm** au sol |
| Toit avant / arrière | **62 / 78 mm** (pente **16/100 ≈ 9,1°**) |
| Mur / toit / socle | **2,4 / 3 / 3 mm** ; parois structurelles ≥2 mm |
| Ouverture de porte | **100 × 42 mm**, décentrée de **14 mm vers la gauche** |
| Montants gauche / droit | **11 / 39 mm** ; servo dans le montant droit |
| Vantail | **99,4 × 41,4 × 2,4 mm**, noir avec rainures décoratives |
| Charnière haute | Axe imprimé **Ø3,2 mm**, palier **Ø3,8 mm** |
| Jeu d’emboîtement | **0,30 mm par face** en CAO, à calibrer sur la P1S |
| Faux plafond des combles | **144,6 × 40 × 2,4 mm**, amovible |
| Éclairage intérieur | Une LED blanche sous le faux plafond, **X75 / Y65 mm** |
| Façade | Blanche, porte noire, orange discret ; **aucun bandeau bleu** |

La porte est **rigide et monobloc**. Ses rainures *imitent* une porte sectionnelle, mais elle **bascule vers l’intérieur** sous le toit autour d’un axe horizontal supérieur. On ne peut pas placer une voiture décorative dans son volume balayé.

Les cartes **XIAO nRF52840 + Wio-SX1262** sont **dans les combles**, au-dessus du faux plafond arrière. Le toit noir reste démontable. La garde théorique sous la pente est d’environ **6,2 mm au-dessus du modèle XIAO**, **sans antenne, câble USB ni rayon de courbure** : mesurer le kit réel avant impression définitive.

## Mécanisme, supports et fixations

La V6 concrétise plusieurs interfaces qui étaient seulement illustrées en V5 :

| Sous-ensemble | Interface modélisée | Ce qui reste à valider |
|---|---|---|
| **Servo MG90** à l’avant droit | Berceau imprimé, **4 pieds avec pilotes Ø1,7**, trous socle Ø2,3 et fraisures Ø4,2, **lèvre de retenue** à l’arrière haut ; fixation par-dessous | **4 vis M2×8 fraisées** seulement comme essai, vraie dimension d’oreilles/boîtier et souplesse du crochet à vérifier |
| **Porte/servo** | Disque **Ø12 mm** intégré côté porte, passage Ø12,6 dans retour droit, **2,2 mm d’écart axial nominal** entre disque et bout d’arbre du modèle servo | **Palonnier livré non mesuré. Disque laissé volontairement sans trous.** Mesurer l’épaisseur et les trous du vrai palonnier, dessiner/percer une liaison positive avant essai motorisé |
| **Palier gauche** | Tourillon Ø3,2 / alésage Ø3,8, **tablette d’appui** dans la coque | Vérifier rotation et maintien sur support, collage ponctuel après essai |
| **XIAO/Wio** | 4 plots bas non conducteurs (3,2 mm haut), **2 fentes 3,2×4,2** pour lien nylon 2,5 mm avec protection isolante | Ne pas écraser les SMD ; contrôler USB-C, antenne et accès |
| **LED blanche** | Support amovible à **2 ergots Ø2 dans trous Ø2,6**, fixé au-dessous du faux plafond ; LED orange en façade | Dimensions réelles des collerettes LED et retenue définitive |
| **Câbles** | 4 œillets de guidage muraux **Ø8 extérieur / Ø3,4 intérieur** ; sortie arrière basse 12×8 et haute 16×9 | Protections anti-arête, anti-traction et trajet sans collision avec la porte |
| **Émetteur réel** | Un seul SAS308 et son aimant | **Boîtier émetteur et supports capteur/aimant non modélisés** dans les 8 STL de la maquette ; pose sans toucher rails, ressorts, galets ou sécurités |

Le vrai DMS-MG90 pourrait différer du **MG90-A** des références 3D fournies. Les modèles tiers conservent leurs géométries originales en **BREP compressées avec SHA256 contrôlé** ; le modèle XIAO simplifié en un seul solide est réservé à l’importation Onshape et aux dégagements, **pas à la conception exacte de ses trous ou composants**.

**Lire avant fabrication :** [guide d’assemblage V6 avec toutes les cotes, essais et limites](docs/ASSEMBLAGE_V6.md).

## Liste de pièces et coûts

Les **deux kits XIAO/Wio, l’imprimante et les filaments** sont déjà disponibles. Le **noyau électronique complémentaire indicatif** est de **23,43 € TTC** hors livraison, alimentation, vis, fils et consommables : un SAS308, un servo DMS-MG90, un condensateur 470 µF, un BC547B, quatre valeurs de résistances, une LED orange et le **lot entier de 130 LEDs WCS101** dont une blanche chaude est utilisée.

**Ne pas racheter le palonnier ni ses vis** : ils sont fournis avec le DMS-MG90. **Pas d’axe métallique** à acheter pour la charnière gauche imprimée.

Le montage nécessite aussi selon votre stock : **2 antennes 868 MHz compatibles**, 2 câbles USB-C, **2 ou 3 alimentations 5 V selon l’architecture**, un adaptateur servo JR facultatif, petite plaque à souder, gaine isolante, fil souple pour D6/D7/D0, colliers de câbles, protection des jonctions du SAS308, et **quatre vis M2 expérimentales** pour le socle. Le besoin et les tailles définitives sont détaillés sans inventer de compatibilité :

- [**BOM canonique V6 : quantités, composants et fixations réellement dessinées**](docs/BOM_V6.md)
- [Nomenclature structurée des achats et quincaillerie](cad/hardware_bom_v5.json)
- [Historique vérifié des prix Gotronic et options de fourniture](docs/BOM_V1_VERIFIEE.md)

**Total complet non déterminé** tant que l’alimentation, les fils, le support capteur et les fixations réelles ne sont pas mesurés.

## Câblage et alimentation

| Signal XIAO | Émetteur sur vraie porte | Récepteur miniature |
|---|---|---|
| **D6** | Contact sec SAS308 → **GND** | Signal du servo positionnel |
| **D7** | Non connecté | Base du BC547B via **4,7 kΩ** ; **100 kΩ** rappel base→GND |
| **D0** | Non utilisé | LED orange câblée **3V3 → 680 Ω → anode LED → cathode D0**, donc LOW = allumée ; **ne jamais piloter D0 HIGH** |
| **5 V** | Chargeur USB isolé vers XIAO | **5 V régulé séparé** vers servo, condensateur 470 µF/16 V et LED blanche (+330 Ω) |
| **GND** | Référence du SAS308 | **Commun à XIAO, servo, LED blanche et alimentation** |

La LED blanche est sur la branche **+5 V → 330 Ω → anode LED → cathode LED → collecteur BC547B → émetteur GND**, commandée par D7 via 4,7 kΩ et 100 kΩ de rappel.

**Ne pas alimenter le servo sur 3V3 ou directement via un GPIO.** Si deux chargeurs sont utilisés côté miniature, **relier seulement les GND**, jamais leurs **+5 V** ensemble. Monter l’antenne LoRa avant toute émission.

[**Netlist détaillée et deux schémas électriques**](docs/CABLAGE_V1_VERIFIE.md) · [Protocole LoRa et limites](docs/PROTOCOLE.md).

## Générer et imprimer la CAO

Le dossier **cad/** est la **source paramétrique**. Les fichiers STEP/STL générés ne sont volontairement pas commités à cause des conflits de fusion de fichiers CAO.

~~~sh
python -m pip install 'cadquery==2.8.0' 'trimesh==4.11.1'
python cad/generate_cad.py
python cad/generate_fit_coupons.py
python cad/qa_geometry.py
python cad/verify_gotronic.py
python cad/test_step_exports.py
python cad/test_hardware_bom.py
python cad/test_fit_coupons.py
~~~

Cela produit :
- **8 STL imprimables** dans **cad/stl/** et **11 STEP** dans **cad/step/** (8 pièces + assemblage V6, structure sans références tierces, XIAO simplifié).
- **3 STL d’éprouvettes** dans **cad/coupons/** pour jeu de charnière, pilote M2 et gabarit vierge de palonnier. Imprimer les éprouvettes avant les grandes pièces.
- Des rapports de métriques et de vérification. Les tests mesurent les géométries et des échantillons de rotation, **pas la résistance des crochets ni la fiabilité réelle des vis**.

Sur GitHub, ouvrir **[Actions — validations CAD et firmware](https://github.com/boidinaudition-code/GarageStateClone/actions/workflows/cad-validation.yml)**, choisir une exécution réussie puis télécharger l’artefact **garage-state-clone-cad-step-stl**. Pour Onshape, importer **GarageStateClone_V2_assemblage_STEP_references.step** (nom historique conservé), ou **GarageStateClone_V2_STRUCTURE_SANS_REFERENCES_ONSHAPE.step** si une référence électronique déclenche “contains faults”. **Réimporter** les STEP après chaque changement, Onshape ne les met pas à jour automatiquement.

**P1S :** commencer à **0,20 mm de couche**, envisager au moins **4 périmètres** pour les pièces mécaniques, calibrer sur les coupons ; orienter les STL dans Bambu Studio, car ils sont exportés **en position assemblée**, pas forcément à plat. Faire un essai mécanique à blanc avant tout collage définitif.

## Compiler les deux firmwares

Les deux rôles ont **le même code** mais des compilations différentes :

~~~sh
python -m pip install 'platformio>=6.1,<7'
pio run -e emetteur
pio run -e recepteur
pio run -e emetteur -t upload
pio run -e recepteur -t upload
pio device monitor -b 115200
~~~

Brancher un seul XIAO à la fois pour flasher, vérifier la bonne carte et l’antenne. **Ne jamais flasher l’émetteur sur la miniature ou inversement.** La configuration utilise **RadioLib** et la **Servo.h fournie par le cœur Adafruit nRF52** ; la bibliothèque Servo Arduino générique a été retirée car elle provoquait une erreur de compilation sur ce cœur.

Les firmware compilés et les exports CAO sont automatiquement contrôlés par [GitHub Actions](.github/workflows/cad-validation.yml). **Une compilation verte n'est pas un essai de servomoteur, de portée LoRa ni de précision des angles**.

## Tests, documentation et limites

Consulter le [**rapport d’audit complet V6**](docs/AUDIT_REPO_V6.md) et surtout la [**checklist d’assemblage et de mise en service**](docs/ASSEMBLAGE_V6.md).

**Avant de considérer la miniature prête à offrir :** imprimer les coupons, mesurer le **vrai palonnier**, vérifier les quatre fixations du berceau et le crochet, assurer une retenue non conductrice de la radio, installer les antennes et l’alimentation sans conflit sous le toit, tester le capteur/aimant sur la vraie porte en toute sécurité, puis répéter plusieurs cycles et les scénarios coupure radio/secteur.

Autres documents utiles : [implantation des combles V5](docs/TOIT_COMBLES_V5.md) *(implantation historique du faux plafond, certaines positions LED remplacées par V6)*, [cotes V4](docs/IMPLANTATION_COMPACTE_V4.md) *(historique)*, [dimensions publiées et inconnues des composants](docs/ENCOMBREMENT_BOM_V1.md) et [dépannage STEP Onshape](docs/ONSHAPE_IMPORT_XIAO.md).

**Aucun câble du montage ne se raccorde aux bornes de motorisation de la vraie porte.** GarageStateClone est un **objet décoratif à états estimés**, pas un dispositif de sécurité.
