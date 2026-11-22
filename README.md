# GarageStateClone — miniature de porte de garage connectée (LoRa)

**Statut : prototype mécanique V10 (fronton bac acier / façade / câblage intérieur), novembre 2026.** Une miniature décorative posée sur une étagère suit *approximativement* l’état d’une vraie porte de garage, sans jamais commander son moteur. Deux kits **Seeed XIAO nRF52840 + Wio-SX1262**, lien LoRa 868 MHz point à point. La miniature est imprimable en plusieurs pièces sur une **Bambu Lab P1S**.

**Version courante : V10, nervures continues du toit vers le bandeau avant, LED orange abaissée, boîte aux lettres réduite, USB-C compact et câblage interne. Le servo V7, le support USB-C V8, la cinématique et le firmware sont conservés.** Les documents V1–V6 décrivant des géométries de supports antérieures sont des archives.

> **Supports V7 :** [plan de fixation des vis du DMS-MG90](docs/FIXATIONS_SERVO_V7.md) et [fiches cotées](docs/FICHES_COTEES_COMPOSANTS_V7.md). Le servo a **deux encoches Ø2 à entraxe 29 mm (Z du garage)**, maintenant représentées par **deux pilotes imprimés** ; le berceau dispose toujours de **quatre vis indépendantes** pour son ancrage au socle. Le crochet supérieur V6 a été remplacé. L'ancienne alerte « 0,05 mm de jeu par bout » comparait deux axes différents : **elle était erronée**. Le palonnier, la longueur réelle des vis et l'antenne sont à vérifier avant montage final.

**Mise à jour du 22/11 — repère servo pour Onshape :** le plan donne **16,00 mm** du fond du DMS-MG90 au dessous des oreilles de fixation. Le berceau positionne ses deux points de vissage avec cette cote et **0,30 mm de jeu** (enveloppe nominale X30, plan sous oreille à X bout arbre +14,00). Les valeurs **≈2,5 mm** (épaisseur d'oreille), **≈4,0 mm** (vers dessus du boîtier) et **≈8,0 mm** (vers bossage d'arbre) sont **provisoires et uniquement documentaires**. Les dimensions du palonnier monté et des vis fournies restent inconnues. [Détails et schéma des plans](docs/FIXATIONS_SERVO_V7.md).

## Nouveauté V8 : une entrée USB-C et une seule alimentation 5 V

La miniature reçoit une **platine USB-C femelle Gotronic 49067** ([fiche fabricant](https://www.gotronic.fr/art-platine-a-connecteur-usb-type-c-2-0-31137.htm)), **21 × 15 × 4,5 mm**, installée sur un **support imprimé solidaire du socle noir**. La coque V10 possède une **petite ouverture arrière de 10 × 4,2 mm** pour ne voir que le port, **provisoirement centrée** : la position exacte du connecteur sur la platine reste à mesurer. Deux guides et **deux tunnels de 3,2 mm pour des colliers de 2,5 mm** maintiennent la platine sans inventer un entraxe de trous. La prise est modélisée par une simple enveloppe, pas par un STEP exact du fabricant.

**Alimentation côté miniature :** un **chargeur USB 5 V / 2 A minimum** → **VBUS +5 V / GND de la 49067** → une petite distribution sur plaque à pastilles, **en parallèle** vers (**A**) 5V/VBUS + GND du **XIAO/Wio récepteur** et (**B**) +5 V + GND du **servo DMS-MG90**. D6 reste uniquement le signal du servo ; le **470 µF / 16 V** reste près du moteur (+ au 5 V). **Aucun buck ni boost**, **aucune puissance servo depuis 3V3**, et **masse commune**.

**Important avant soudure et impression finale :** vérifier sur la 49067 si les résistances **5,1 kΩ de CC1→GND et CC2→GND** sont présentes ; les ajouter **seulement si elles manquent**, sans relier CC1 et CC2. La **position exacte du connecteur USB-C**, ses trous et le dégagement du câble ne sont **pas documentés** par Gotronic et restent à mesurer. Le XIAO reçoit le 5 V externe sur sa broche VBUS : **débrancher cette alimentation avant de le brancher à un PC pour flasher**, ou ajouter une isolation d'alimentation vérifiée.

**Détails, repères CAO, schéma, liste d'achats et montage : [ALIMENTATION_USB_C_V8.md](docs/ALIMENTATION_USB_C_V8.md).**

## Nouveauté V9 : toiture bac acier et boîte aux lettres d'après photo

Sur le **toit noir amovible**, **13 nervures trapézoïdales** régulièrement espacées de **11,5 mm** suivent l'axe **avant → arrière de la pente**, avec un relief de **0,95 mm** et une base de **2,5 mm** (sommet **1,1 mm**). Elles sont **solidaires du toit imprimé**. La pente reste **62 / 78 mm**, l'épaisseur structurelle sous le relief **3 mm**, la jupe et les dégagements mécaniques inchangés. C'est une **interprétation esthétique** de la couverture sur la photo, pas un profil industriel exact mesuré.

Dans l'ancienne version V9, sur le **montant blanc droit de la façade**, un **renfoncement de 10,6 × 10,6 × 1,05 mm** était réservé à une **plaque noire carrée 10 × 10 × 0,75 mm**, imprimer séparément comme pièce **`10_boite_aux_lettres_noire`**, à coller après peinture/essai à blanc. Plaque légèrement rentrante (0,1 mm), jeu nominal 0,30 mm par côté et une petite fente gravée décorative. L'emplacement de la boîte noire est repris **visuellement** des photos fournies, à droite de la porte ; il n'est pas une cote de relevé sur le vrai bâtiment.

**Les fichiers CAO comptent désormais 9 pièces STL et 12 STEP** (9 pièces, 2 assemblages, 1 XIAO simplifié). Le support d'USB-C **49067 reste solidaire du socle**. Le dessin V9 historique est détaillé dans [le guide toiture et boîte aux lettres](docs/TOIT_BAC_ACIER_BOITE_LETTRES_V9.md).

## Révision V10 : fronton nervuré, goulotte intérieure et prises discrètes

La photo montre un **bandeau métallique descendant en façade** avec des lignes verticales. Les **13 nervures trapézoïdales du toit** se prolongent désormais sur **la façade avant descendante du toit noir amovible**, au même pas de **11,5 mm** et avec un relief extérieur de **0,85 mm**. La pente **62 / 78 mm** et le maintien intérieur du toit restent identiques.

La **LED orange est abaissée de 0,5 mm** : X96 conservé, **Z52,8** au lieu de Z53,3. La **boîte aux lettres est 30 % plus petite en largeur et en hauteur** : plaque noire **7 × 7 × 0,75 mm** dans un logement **7,6 × 7,6 × 1,05 mm** ; centre inchangé à X129,8/Z29,3, jeu 0,30 mm par côté.

La **seule ouverture arrière extérieure** devient une découpe USB-C d'essai **10 × 4,2 mm** (Z9,45..13,65). La position du port réel de la **Gotronic 49067** n'étant pas publiée, cette découpe reste **à contrôler avec la platine et la fiche réelles avant impression finale**. L'ancien **trou haut arrière 16 × 9 mm est supprimé**. Les fils passent du bas vers le haut **à l'intérieur**, dans une **goulotte ouverte** à l'arrière, séparée du support USB-C, entre Z14 et Z43 (largeur libre 7,2 mm, trois petites lèvres de retenue). Aucun câble n'a besoin de traverser le mur arrière en hauteur.

Voir le [**dossier technique V10 et les réserves d'assemblage**](docs/EVOLUTION_FACADE_CABLAGE_V10.md). La CAO conserve **9 STL et 12 STEP**.

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
| Toit avant / arrière | **62 / 78 mm** (pente **16/100 ≈ 9,1°**), 13 nervures bac acier +0,95 mm |
| Mur / toit / socle | **2,4 / 3 / 3 mm** ; parois structurelles ≥2 mm |
| Ouverture de porte | **100 × 42 mm**, décentrée de **14 mm vers la gauche** |
| Montants gauche / droit | **11 / 39 mm** ; servo dans le montant droit |
| Vantail | **99,4 × 41,4 × 2,4 mm**, noir avec rainures décoratives |
| Charnière haute | Axe imprimé **Ø3,2 mm**, palier **Ø3,8 mm** |
| Jeu d’emboîtement | **0,30 mm par face** en CAO, à calibrer sur la P1S |
| Faux plafond des combles | **144,6 × 40 × 2,4 mm**, amovible |
| Éclairage intérieur | Une LED blanche sous le faux plafond, **X75 / Y65 mm** |
| Façade | Blanche, porte noire, orange discret, **boîte aux lettres noire 7 × 7 mm** sur montant droit ; **aucun bandeau bleu** |
| Bandeau V10 | Même nervurage bac acier sur toit et façade descendante |
| Alimentation V10 | Platine **USB-C 49067** sur socle arrière intégré, sortie **10 × 4,2 mm** ; 5 V / 2 A minimum |

La porte est **rigide et monobloc**. Ses rainures *imitent* une porte sectionnelle, mais elle **bascule vers l’intérieur** sous le toit autour d’un axe horizontal supérieur. On ne peut pas placer une voiture décorative dans son volume balayé.

Les cartes **XIAO nRF52840 + Wio-SX1262** sont **dans les combles**, au-dessus du faux plafond arrière. Le toit noir reste démontable. La garde théorique sous la pente est d’environ **6,2 mm au-dessus du modèle XIAO**, **sans antenne, câble USB ni rayon de courbure** : mesurer le kit réel avant impression définitive.

## Mécanisme, supports et fixations

La V6 concrétise plusieurs interfaces qui étaient seulement illustrées en V5 :

| Sous-ensemble | Interface modélisée | Ce qui reste à valider |
|---|---|---|
| **Servo DMS-MG90** à l’avant droit | Berceau imprimé, **4 pieds à pilotes Ø1,7** vissés au socle à travers les **passages Ø2,3** et **2 pilotes Ø1,7** pour les **2 encoches Ø2, entraxe 29 mm** du servo ; colonne de retenue à la place du crochet | Face support calée sur cote constructeur 16,00 mm avec 0,30 mm de jeu ; tester vis, épaisseur d'oreille et alignement réel en X avant mise sous tension |
| **Porte/servo** | Disque **Ø12 mm** intégré côté porte, passage Ø12,6 dans retour droit, **2,2 mm d’écart axial nominal** entre disque et bout d’arbre du modèle servo | **Palonnier livré non mesuré. Disque laissé volontairement sans trous.** Mesurer l’épaisseur et les trous du vrai palonnier, dessiner/percer une liaison positive avant essai motorisé |
| **Palier gauche** | Tourillon Ø3,2 / alésage Ø3,8, **tablette d’appui** dans la coque | Vérifier rotation et maintien sur support, collage ponctuel après essai |
| **XIAO/Wio** | 4 plots bas non conducteurs (3,2 mm haut), **2 fentes 3,2×4,2** pour lien nylon 2,5 mm avec protection isolante | Ne pas écraser les SMD ; contrôler USB-C, antenne et accès |
| **LED blanche** | Support amovible à **2 ergots Ø2 dans trous Ø2,6**, fixé au-dessous du faux plafond ; LED orange en façade | Dimensions réelles des collerettes LED et retenue définitive |
| **Entrée USB-C 49067** | Support intégré au socle noir (2 guides, 2 tunnels de collier Ø fonctionnel 3,2) et **ouverture USB-C arrière 10 × 4,2 mm (essai)** ; l'ancienne fente basse 12 × 8 est supprimée | Placer la vraie prise dans l'ouverture après mesure ; sans trou de PCB inventé, hauteur et nez USB inconnus |
| **Câbles** | 4 œillets de guidage muraux **Ø8 extérieur / Ø3,4 intérieur** ; **goulotte intérieure sans sortie haute arrière** | Protéger fils et soudure de la 49067 contre les tractions et la porte mobile |
| **Émetteur réel** | Un seul SAS308 et son aimant | **Boîtier émetteur et supports capteur/aimant non modélisés** dans les 9 STL de la maquette ; pose sans toucher rails, ressorts, galets ou sécurités |

Le vrai DMS-MG90 pourrait différer du **MG90-A** des références 3D fournies. Les modèles tiers conservent leurs géométries originales en **BREP compressées avec SHA256 contrôlé** ; le modèle XIAO simplifié en un seul solide est réservé à l’importation Onshape et aux dégagements, **pas à la conception exacte de ses trous ou composants**.

**Lire avant fabrication :** [fixations servo V7](docs/FIXATIONS_SERVO_V7.md) puis [guide d'assemblage V6](docs/ASSEMBLAGE_V6.md) pour les autres sous-ensembles (les instructions du crochet V6 sont remplacées).

## Liste de pièces et coûts

Les **deux kits XIAO/Wio, l’imprimante et les filaments** sont déjà disponibles. Le **noyau électronique complémentaire indicatif** est de **23,43 € TTC** hors livraison, alimentation, vis, fils et consommables : un SAS308, un servo DMS-MG90, un condensateur 470 µF, un BC547B, quatre valeurs de résistances, une LED orange et le **lot entier de 130 LEDs WCS101** dont une blanche chaude est utilisée.

**Le palonnier et des vis sont annoncés fournis avec le DMS-MG90**, mais il faut contrôler leur nombre, leur tête, leur longueur et leur aptitude aux deux pilotes Ø1,7. **Pas d’axe métallique** à acheter pour la charnière gauche imprimée.

Le montage nécessite aussi selon votre stock : **2 antennes 868 MHz compatibles**, 2 câbles USB-C, **2 ou 3 alimentations 5 V selon l’architecture**, un adaptateur servo JR facultatif, petite plaque à souder, gaine isolante, fil souple pour D6/D7/D0, colliers de câbles, protection des jonctions du SAS308, et **quatre vis M2 expérimentales** pour le socle. Le besoin et les tailles définitives sont détaillés sans inventer de compatibilité :

- [**BOM canonique V6 : quantités, composants et fixations réellement dessinées**](docs/BOM_V6.md)
- [Nomenclature structurée des achats et quincaillerie](cad/hardware_bom_v5.json)
- [Historique vérifié des prix Gotronic et options de fourniture](docs/BOM_V1_VERIFIEE.md)

**Accessoires V8 à ajouter au noyau historique :** 1× platine USB-C [49067](https://www.gotronic.fr/art-platine-a-connecteur-usb-type-c-2-0-31137.htm) (**4,95 €**), 2× bornier SC02/2.54 [48930](https://www.gotronic.fr/art-bornier-sc02-2-54-15468.htm) (**1,60 €** les deux), éventuellement 1 lot de résistances [5,1 kΩ 15944](https://www.gotronic.fr/art-5-resistances-1-2w-5-1-k-8486-8829.htm) (**0,30 € si absentes de la 49067**), et une plaque à pastilles [BCS050 12470](https://www.gotronic.fr/art-plaque-d-essais-bcs050-6931.htm) (**1,40 € si non achetée**, déjà prévue pour la LED). Soit **6,55 €** d'éléments minimaux + **1,70 €** conditionnels, **8,25 € au maximum** si tout manque. Noyau 23,43 € + 8,25 € = **31,68 €** hors alimentation, câble, fils, vis et livraison. Les résistances CC dépendent de la platine reçue.

**Total complet non déterminé** tant que l’alimentation, les fils, le support capteur et les fixations réelles ne sont pas mesurés.

## Câblage et alimentation

| Signal XIAO | Émetteur sur vraie porte | Récepteur miniature |
|---|---|---|
| **D6** | Contact sec SAS308 → **GND** | Signal du servo positionnel |
| **D7** | Non connecté | Base du BC547B via **4,7 kΩ** ; **100 kΩ** rappel base→GND |
| **D0** | Non utilisé | LED orange câblée **3V3 → 680 Ω → anode LED → cathode D0**, donc LOW = allumée ; **ne jamais piloter D0 HIGH** |
| **5 V** | Chargeur USB isolé vers XIAO | **Chargeur USB-C 5 V / 2 A** → 49067 / bus parallèle → **5V/VBUS XIAO** et **servo** ; C1 et R1 sur le même bus |
| **GND** | Référence du SAS308 | **Commun à XIAO, servo, LED blanche et alimentation** |

La LED blanche est sur la branche **+5 V → 330 Ω → anode LED → cathode LED → collecteur BC547B → émetteur GND**, commandée par D7 via 4,7 kΩ et 100 kΩ de rappel.

**Ne pas alimenter le servo sur 3V3 ou directement via un GPIO.** En V8, un seul 5 V distribué à deux branches séparées ; GND commun. Si une variante avec deux chargeurs est utilisée, ne jamais réunir leurs +5 V. Lors d'une programmation USB du XIAO, isoler d'abord le 5 V externe pour éviter tout retour de courant. Monter l'antenne LoRa avant toute émission.

[**Schéma d'alimentation USB-C V8 et instructions**](docs/ALIMENTATION_USB_C_V8.md) · [Netlist de contrôle des GPIO V1](docs/CABLAGE_V1_VERIFIE.md) · [Protocole LoRa et limites](docs/PROTOCOLE.md).

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
python cad/test_component_dimensions_sources.py
python cad/test_fit_coupons.py
~~~

Cela produit :
- **9 STL imprimables** dans **cad/stl/** et **12 STEP** dans **cad/step/** (9 pièces dont le toit nervuré, une nouvelle plaque noire de boîte aux lettres, le socle V8 avec support USB ; 1 assemblage avec enveloppe 49067, 1 structure sans références tierces et 1 XIAO simplifié).
- **3 STL d’éprouvettes** dans **cad/coupons/** pour jeu de charnière, pilote M2 et gabarit vierge de palonnier. Imprimer les éprouvettes avant les grandes pièces.
- Des rapports de métriques et de vérification. Les tests mesurent les géométries et des échantillons de rotation, **pas la résistance du maintien imprimé ni la fiabilité réelle des vis**.

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

Les firmwares compilés et les exports CAO sont automatiquement contrôlés par [GitHub Actions](.github/workflows/cad-validation.yml). **Une compilation verte n'est pas un essai de servomoteur, de portée LoRa ni de précision des angles**.

## Tests, documentation et limites

Consulter d'abord le [**montage USB-C V8**](docs/ALIMENTATION_USB_C_V8.md), puis le [**montage servo V7**](docs/FIXATIONS_SERVO_V7.md), puis l'[audit historique V6](docs/AUDIT_REPO_V6.md) et la [checklist d'assemblage](docs/ASSEMBLAGE_V6.md) pour les autres sous-ensembles.

**Avant de considérer la miniature prête à offrir :** imprimer les coupons, mesurer le **vrai palonnier**, vérifier les quatre fixations du berceau ET les deux pilotes du servo (29 mm), assurer une retenue non conductrice de la radio, contrôler la position réelle de l'embase 49067 et ses résistances CC1/CC2, isoler le bus de puissance et les soudures, installer les antennes et l’alimentation sans conflit sous le toit, tester le capteur/aimant sur la vraie porte en toute sécurité, puis répéter plusieurs cycles et les scénarios coupure radio/secteur.

Autres documents utiles : [implantation des combles V5](docs/TOIT_COMBLES_V5.md) *(implantation historique du faux plafond, certaines positions LED remplacées par V6)*, [cotes V4](docs/IMPLANTATION_COMPACTE_V4.md) *(historique)*, [dimensions publiées et inconnues des composants](docs/ENCOMBREMENT_BOM_V1.md) et [dépannage STEP Onshape](docs/ONSHAPE_IMPORT_XIAO.md).

**Aucun câble du montage ne se raccorde aux bornes de motorisation de la vraie porte.** GarageStateClone est un **objet décoratif à états estimés**, pas un dispositif de sécurité.
