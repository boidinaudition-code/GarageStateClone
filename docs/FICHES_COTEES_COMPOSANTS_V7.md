# Fiches techniques et plans cotés des composants — audit mécanique V7

**22 novembre 2026 · Unités mm · cible CAD V6 : coque 150 × 100 mm, toit 62/78 mm.**

Cette note est la **référence documentaire des cotes à utiliser pour la prochaine révision mécanique**, sans déclarer l'assemblage physique validé. Les dimensions exploitables par script sont dans [`cad/component_dimensions_sources_v7.json`](../cad/component_dimensions_sources_v7.json). Le [jeu actuel](../cad/generate_cad.py) et les STEP de tiers ne sont **pas automatiquement corrigés** par cette collecte.

## Méthode et confiance

- **A — Plan constructeur exact** : plan dimensionné explicitement lié à la référence achetée.
- **B — Cote vendeur/fabricant** : encombrement décrit dans la fiche, parfois avec avertissement de variation des lots.
- **C — Famille ou STEP tiers** : utile pour l'espace de service mais **pas interchangeable** avec une mesure du composant exact.
- **D — Inconnu** : aucun plan attribuable avec confiance ; ne jamais remplir avec des mesures d'un autre produit.
- **P — Projet** : valeur libre dessinée dans CadQuery, **pas** cote de la pièce commerciale.

## 1. Références critiques mécaniques

| Réf. de BOM / qté | Fiche exacte / plan | Cotes vérifiables | Source et niveau | Mesures ou réserves avant validation |
|---|---|---|---|---|
| **M1 — 1× DMS-MG90 SER0039** | **Plan coté 3 vues Gotronic 36923** | **L totale 33, largeur 12, hauteur jusqu'au bout d'arbre 30**, longueur corps en vue de dessus **23**, **entraxe lumières 29**, ouverture en **Ø2**, axe à **6** de l'extrémité du corps ; niveaux verticaux **16 / 22,5 / 26,5 / 30** depuis la base | **A** · [plan PDF Gotronic](https://www.gotronic.fr/pj2-dimensions-dms-mg90-36923-2320.pdf) · [fiche DMS-MG90](https://www.gotronic.fr/art-servomoteur-dms-mg90-32266.htm) | Forme des palonniers fournis, entraxe de leurs **propres** trous, épaisseur, denture/vis centrale ; hauteur réelle des oreilles et tête/longueur des vis fournies |
| **S1 — 1× SAS308** | Contact magnétique Gotronic **26449** | Corps du contact **24 × 15 × 6**, câble moulé **250**, écart maxi de déclenchement indiqué **15** | **B** · [fiche SAS308](https://www.gotronic.fr/art-contact-magnetique-miniature-sas308-12751.htm) | **Aimant non coté**, perçages/entraxe des deux éléments non cotés, surface de fixation réelle non définie |
| **MCU — 2× Seeed XIAO nRF52840** | Dimension officielle **DXF** et empreintes Seeed | Carte seule **21 × 17,8** ; le STEP tiers du dépôt englobe env. **22,482 × 4,460 × 17,780** dans ses axes d'origine | **B** carte · [wiki Seeed](https://wiki.seeedstudio.com/XIAO_BLE/) · [DXF officiel (ZIP)](https://files.seeedstudio.com/wiki/XIAO-BLE/XIAO-nRF52840-DXF.zip) · [pads (ZIP)](https://files.seeedstudio.com/wiki/XIAO-BLE/Bottom-pad-positioning.zip) | Épaisseur PCB, position réelle USB-C, connecteur d'accouplement, hauteur des composants ; **le DXF est identifié mais non décodé dans cet audit**, éviter toute cote de trous prétendument mesurée |
| **WIO — 2× Wio-SX1262 for XIAO** | Modèle 3D de Seeed (archive) et STEP tiers déposé | Boîte du STEP tiers fourni : **17,780 × 22,316 × 7,642** (axes d'origine, **hors antenne**) | **C** · [ressources 3D Seeed Wio](https://wiki.seeedstudio.com/wio_sx1262_and_xiao_esp32s3_kit_with_3dprinted_enclosure_introduction_and_assembly_guide/) · [manifeste interne](../cad/vendor_models/manifest.json) | Emboîtement XIAO/Wio, hauteur et dégagement des connecteurs, prise IPEX, épaisseur/soudure : à contrôler **assemblés** |
| **RF_STACK — 2× kit XIAO+Wio** | Donnée de présentation du kit nRF52840 | Enveloppe annoncée par Seeed **8 × 22 × 23** (ordre non assimilable sans repère XYZ) | **B nominal** · [kit Seeed nRF52840](https://wiki.seeedstudio.com/xiao_nrf52840%26_wio_SX1262_kit_for_meshtastic/) | **Mesurer le montage complet**, antenne et câble branchés, le rayon de courbure du coaxial et la prise USB ; réserve au toit seulement ~6,2 mm dans V6 sans ces accessoires |
| **ANT — 2× antenne 868 MHz** | Référence non verrouillée | **Aucune cote exploitable** | **D** | Identifier modèle, type de connecteur RF, câble, diamètre du corps et rayon de courbure. Ne pas imprimer de trou fixé à une antenne imaginaire |

### Pourquoi le servomoteur est un point bloquant

Le fichier tiers conservé comme **MG90-A** dans le dépôt a, **une fois orienté dans la miniature**, une boîte de **L 32,5 × l 12,221 × h 33,4**. Le **plan officiel DMS-MG90** donne **L 33 × l 12 × h 30**, palonnier non inclus. Ce ne sont pas des tolérances de production, mais **deux géométries qui ne coïncident pas**.

Dans [`generate_cad.py`](../cad/generate_cad.py), le berceau V6 est dérivé d'une longueur STEP de 32,5 avec un jeu de **0,30 mm par bout**. Longueur interne résultante **33,10**. Avec **33,00 mm officiels**, il ne reste que **0,10 mm au total**, soit **0,05 mm par bout si le servo est centré** : **insuffisant pour une pièce FDM**, et la retenue supérieure basée sur un STEP **3,4 mm plus haut** risque de ne pas fonctionner.

**Décision de conception :** conserver la V6 comme *prototype non certifié*, mais **redimensionner le berceau et son clip d'après le DMS-MG90 physique**, puis recaler l'axe et vérifier les collisions. Le plan officiel autorise dès maintenant un **gabarit test à entraxe 29 et lumières Ø2**, pas un accouplement de porte définitif. Les symboles **Ø3 / Ø5** du dessin désignent les détails circulaires du haut du servo, **pas** une fiche de cannelure de palonnier.

## 2. Électronique passive et voyants

| Réf. / qté | Cote fiable et référence | Ce qui reste inconnu |
|---|---|---|
| **C1 470 µF/16 V — 1×** | **Ø10 × 13**, pattes au pas **5,0** · **B** [Gotronic 04947](https://www.gotronic.fr/art-condensateur-radial-470uf-16v-3386.htm) | Le fournisseur prévient que le lot peut varier : mesurer corps et longueur de fil avant support définitif |
| **Q1 BC547B TO-92 — 1×** | **A max 5,20, B max 5,33, C max 4,19**, fils ≥12,70 sur plan de famille **onsemi Case 29-11**, page 6 du PDF (page index 5) · **C** [onsemi BC546/547/548](https://www.onsemi.com/pdf/datasheet/bc546-d.pdf) | Le fabricant du BC547B Gotronic 02173 n'est pas garanti être onsemi ; le boîtier et les fils dépendent du lot |
| **R1 330 Ω — 1×** | Corps **6,5 × Ø2,5** · **B** [Gotronic 04130](https://www.gotronic.fr/art-5-resistances-1-2w-330-8486-2653.htm) | Encombrement des pattes pliées |
| **R2 4,7 kΩ — 1×** | Corps **6,5 × Ø2,5** · **B** [Gotronic 04144](https://www.gotronic.fr/art-5-resistances-1-2w-4-7-k-8486-2667.htm) | Idem |
| **R3 100 kΩ — 1×** | Corps **6,5 × Ø2,5** · **B** [Gotronic 04160](https://www.gotronic.fr/art-5-resistances-1-2w-100-k-8486-2681.htm) | Idem |
| **R4 680 Ω — 1×** | Corps **6,5 × Ø2,5** · **B** [Gotronic 04134](https://www.gotronic.fr/art-5-resistances-1-2w-680-8486-2657.htm) | Idem |
| **LED1 blanche chaude WCS101 — 1× dans lot** | **Ø5 nominal** seulement · **B** [Whadda WCS101 fabricant](https://www.velleman.eu/fr_BE/shop/wcs101-assortiment-de-led-1573) | Hauteur, collerette et pas de fils ; le lot couvre plusieurs LEDs distinctes sans plan individuel identifié |
| **LED2 orange L7113NC — 1×** | **Ø5 nominal** seulement · **B** [Gotronic 03051](https://www.gotronic.fr/art-led-5-mm-l7113nc-2086.htm) | Corps, collerette et pattes. **ATTENTION** : Gotronic renvoie vers le PDF **L7113EC (03050)**, **autre référence** ; ne pas l'importer comme plan exact L7113NC |

Le trou orange **Ø2 en façade**, la poche LED **Ø6,6**, l'enveloppe LED **Ø6 × 9** et les deux ergots du support blanc sont des **choix P de la CAO**, pas des dimensions constructeur. Mesurer avant de remplacer le gabarit provisoire.

## 3. Supports, connecteurs et accessoires de la BOM

| Élément | Dimensions connues | Réserve |
|---|---|---|
| **BCS050 perfboard / Gotronic 12470** | Plaque **50 × 100 × 1,5**, pas **2,54** · [Gotronic](https://www.gotronic.fr/art-plaque-d-essais-bcs050-6931.htm) | **25 × 30** de découpe dans la BOM est un choix P ; implantation filaire hors CAO |
| **4 vis M2×8 fraisées / 11636** | Vis nominales **M2, longueur 8** · [rubrique Gotronic](https://www.gotronic.fr/cat-visserie-685.htm) | Diamètre/angle/hauteur exacts de tête **non attestés** : Ø4,2 × profondeur fraisure 1,2 du socle = **P** |
| **Colliers nylon 11845** | **2,5 × 100** nominal · [Gotronic](https://www.gotronic.fr/cat-colliers-de-serrage-1330.htm) | Tête et épaisseur non cotées ; ne pas serrer contre SMD/prise IPEX |
| **Prises USB-C, câble, répartiteur 5 V** | **Aucune référence mécanique finale** | Choisir le cordon **avant** de finaliser la sortie arrière haute **16 × 9** ; passage inclut gaine et courbure, pas seulement métal USB-C |
| **SAS308 : vis/supports sur porte réelle** | **Aucun entraxe de fixation exploitable** | Mesure sur la porte/aimant réels, fixation non invasive hors rails/ressorts/galets ; ne jamais modifier les dispositifs de sécurité |
| **Émetteur LoRa externe** | Boîtier toujours à choisir/imprimer | Poussière, humidité, antenne et décharge de traction doivent être étudiées séparément ; ne dépend pas du volume intérieur de la miniature |

## 4. Check-list de métrologie à faire avant impression finale

1. **Servo** : mesurer L/l/h hors tout, face du corps, saillie d'arbre et entraxe des lumières Ø2 ; photographier le palonnier choisi sur papier millimétré avec pied à coulisse ; mesurer épaisseur et vis centrale. **Priorité absolue**.
2. **Radio** : mesurer kit XIAO+Wio réellement assemblé, connecteurs/soudures, câble antenne branché et une fiche USB-C en situation de pliage. Vérifier l'implantation sous la pente et la maintenance du toit.
3. **LEDs** : mesurer collerette, hauteur de lentille, pas des deux pattes et le volume des fils isolés. La mesure de LED1 ne se transpose pas automatiquement à LED2.
4. **SAS308** : relever les deux éléments séparément, diamètre et entraxe des points de vis, chemin fixe du câble sur vrai garage.
5. **C1 + visserie + petite plaque** : cote réelle du condensateur du lot, tête des M2×8, effort de serrage des pieds imprimés, protection de fils et dimensions du montage soudé.

**Politique de release :** aucun fichier STL ne doit être déclaré « prêt au montage définitif » tant que les mesures marquées **D** ou les interfaces de fixation **A non testées physiquement** n'ont pas été validées. Les contrôles de collision CadQuery et les STEP fournis n'établissent pas les tolérances de pièces commerciales.

[Catalogue JSON exploitable par CAO](../cad/component_dimensions_sources_v7.json) · [BOM V6](BOM_V6.md) · [Guide d'assemblage V6](ASSEMBLAGE_V6.md).
