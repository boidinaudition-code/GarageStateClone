# Encombrement composants – V1 (21 novembre 2026)

**Statuts :** C = publié fabricant/vendeur pour la référence ; V = enveloppe de famille/variante, non garantie pour le lot ; P = valeur proposée dans la CAO ; M = à mesurer. Un nombre connu du vendeur n'est pas une mesure au pied à coulisse de votre exemplaire.

| Qté V1 | Composant | Dimension publiée (mm) | Statut / ce qui manque | Source |
|---:|---|---|---|---|
| **1** | SAS308, Gotronic 26449 | Boîtier **24 × 15 × 6**, câble **250**, écart avec aimant **15 maxi** | **C** ; aimant et trous de vis : **M** | [Gotronic](https://www.gotronic.fr/art-contact-magnetique-miniature-sas308-12751.htm) |
| **1** | DMS-MG90, Gotronic 36923, DFRobot SER0039 | Corps **22,3 × 11,8 × 26,3**, cordon **180** | **C** ; pattes, entraxe vis, arbre, palonnier : **M** ; [plan officiel](https://www.gotronic.fr/pj2-dms-mg90-servo-dimension-2320.pdf) à exploiter/mesurer avant fixation définitive | [Gotronic](https://www.gotronic.fr/art-servomoteur-dms-mg90-32266.htm) |
| **1** | C1 470 µF / 16 V, Gotronic 04947 | Corps **Ø10 × 13**, écart entre fils **5,0** | **C** ; fournisseur précise variation selon approvisionnement | [Gotronic](https://www.gotronic.fr/art-condensateur-radial-470uf-16v-3386.htm) |
| **1** | BC547B, Gotronic 02173 | Boîtier **TO-92** ; référence onsemi : enveloppe **5,20 × 5,33 × 4,19** selon axes du plan | **V** ; fabricant/lot exact, C-B-E et fil de sortie : **M** | [onsemi](https://www.onsemi.com/pub/Collateral/BC546-D.PDF), [Gotronic](https://www.gotronic.fr/art-transistor-bc547b-1336.htm) |
| **1** | R1 330 Ω Gotronic 04130 | Corps **longueur 6,5 × Ø2,5** | **C**, les fils/entraxe montage ne sont pas définis | [Gotronic](https://www.gotronic.fr/art-5-resistances-1-2w-330-8486-2653.htm) |
| **1** | R2 4,7 kΩ Gotronic 04144 | Corps **6,5 × Ø2,5** | **C**, fils non définis | [Série 1/2 W](https://www.gotronic.fr/cat-resistances-metal-1-2-w-267.htm) |
| **1** | R3 100 kΩ Gotronic 04160 | Corps **6,5 × Ø2,5** | **C**, fils non définis | [Série 1/2 W](https://www.gotronic.fr/cat-resistances-metal-1-2-w-267.htm) |
| **1** | R4 680 Ω Gotronic 04134 | Corps **6,5 × Ø2,5** | **C**, fils non définis | [Série 1/2 W](https://www.gotronic.fr/cat-resistances-metal-1-2-w-267.htm) |
| **1 utilisée** | Blanche chaude Whadda WCS101, Gotronic 03989 | **Ø5 nominal**, lot de 130 dont 20 blanches chaudes | **C** uniquement pour diamètre nominal ; longueur, collerette, pas/section pattes **M** ; aucune cote de l'ancienne Luckylight conservée | [Gotronic WCS101](https://www.gotronic.fr/art-assortiment-de-130-leds-wcs101-39775.htm) |
| **1** | Orange L7113NC, Gotronic 03051 | **Ø5 nominal** | **C** pour diamètre ; hauteur, collerette et pas fils **M** ; PDF lié L7113EC non transposé | [Gotronic L7113NC](https://www.gotronic.fr/art-led-5-mm-l7113nc-2086.htm) |
| **2 en stock** | XIAO nRF52840 | Carte seule **21 × 17,8** | **C**, hauteur du connecteur USB/soudures non publiée | [Seeed](https://wiki.seeedstudio.com/XIAO_BLE/) |
| **2 en stock** | XIAO + Wio-SX1262 en pile | Seeed annonce environ **8 × 22 × 23** pour le kit ; **21 × 17,8** pour PCB XIAO seul | **C nominal**, orientation et éléments annexes antenne/USB à **mesurer** | [Seeed kit](https://wiki.seeedstudio.com/xiao_nrf52840%26_wio_SX1262_kit_for_meshtastic/) |
| **2 en stock, vérifier** | Antennes 868 MHz | **Indéterminé** sans référence exacte | **M**, y compris câble RF et rayon de courbure | Référence réelle à relever |
| **2 ou 3** | Alimentation USB-A HNP18-USBV2 14749 | **56 × 27 × 73**, 5 V / 3 A | **C** fiche ; chargeur secteur externe, pas dans la coque | [Gotronic](https://www.gotronic.fr/art-alimentation-hnp18-usbv2-38701.htm) |
| **1 si variante servo séparée** | Bornier DC PCM10F 48214 + cordon 49101 | **40 × 15 × 11** ; cordon **900** | **C** ; place, sortie fils et polarité **M** | [Gotronic](https://www.gotronic.fr/art-adaptateur-pcm10f-17984.htm) |
| **1 à découper** | Perfboard BCS050 12470 | **50 × 100 × 1,5**, pas **2,54** | **C** ; découpe/implantation **P/M**, ne rentre pas entière dans le plateau | [Gotronic](https://www.gotronic.fr/art-plaque-d-essais-bcs050-6931.htm) |
| Selon montage | USB-A/C, fil, gaine, vis et éventuel répartiteur | Longueurs et montage final **à déterminer** | **M**, références et limites dans la BOM ; répartiteur non confirmé | [Fournitures Gotronic](BOM_V1_VERIFIEE.md#fournitures-indispensables-si-absentes) |

## Jeux et pièces imprimées

| Paramètre CAO | Cote (mm) | Statut |
|---|---:|---|
| Coque extérieure W × D | **190 × 100** | **P — CAO V3 actuelle**, largeur initiale 168 et ancienne V2 184 obsolètes |
| Hauteurs avant/arrière | **62 / 65** | **P** ; mono-pente +3 mm sur 100 mm (≈1,72°) |
| Parois structurelles | **2,4** | **P**, minimum exigé ≥2 |
| Toit et socle | **3,0** | **P** |
| Ouverture porte | **110 × 42** | **P — CAO V2 actuelle** |
| Panneau de porte | **103,4 × 41,4 × 2,4** | **P** |
| Jeu d'emboîtement | **0,30 par face**, donc +0,60 sur largeur de trou | **P** ; coupon d'essai PLA nécessaire |
| Axe / palier | **Ø3,2 / Ø3,8** | **P**, jeu radial 0,30 |
| Corps servo, volume nominal | **22,3 × 11,8 × 26,3** | **C**, sans palonnier ni pattes |
| Plateau électronique | **60 × 31**, compartiment arrière | **P** |
| Réserve de service pour les cartes et leurs fils | **52 × 23 × 12** | **P** ; ce n'est **pas** la taille de la carte |
| C1 : logement cylindrique minimal de départ | **Ø10,6** pour Ø10 de corps | **P** ; à ajuster après mesure |
| Orange façade : ouverture optique | **Ø2,0** | **P**, petit point visible, pas un trou de montage Ø5 |
| Poches des deux LED / enveloppes réservées | **Ø6,6 / Ø6 × 9** | **P**, enveloppes provisoires incluant réserve de collerette, **pas des cotes fabricant** |
| Orange : début de poche derrière façade | **3,4** depuis face avant | **P**, LED entièrement cachée ; fils au-delà de la réserve, maintien à définir |

## Implantation mécanique

- **Servo à l'avant, côté droit**, axe moteur coaxial avec l'axe horizontal **supérieur de la porte**, palier côté gauche ; la porte rigide rainurée **bascule vers l'intérieur** et se range sous le toit en pente.
- XIAO+Wio sur plateau arrière hors trajectoire ; condensateur proche du servo ; LED blanche à l'arrière sous le toit hors zone balayée ; LED orange en haut à droite de façade.
- Design esthétique V3 : **murs blancs, toit noir légèrement en pente, porte noire, aucun liseré bleu** ; toit amovible. Imprimante **Bambu Lab P1S + AMS**.
- Les pièces de la V1 **ne sont pas prêtes pour l'assemblage final** : centre réel de l'arbre et entraxes de fixations MG90, sortie USB, antenne, aimant du SAS308 et collerette LED orange à mesurer.

## Capteur unique de fermeture

**Dernière décision : un seul SAS308.** Le contact est fermé quand l'aimant est en face et que la **vraie porte est fermée**. Lorsque l'aimant s'éloigne, cela signifie uniquement **non fermée**, et non forcément complètement ouverte.

La simulation décorative peut faire **FERMÉ confirmé → INTERMÉDIAIRE → OUVERT estimé après 40 s sans aimant** (paramètre de firmware à adapter à la durée réelle). Attention : une vraie porte arrêtée à mi-course pendant plus de 40 s serait représentée ouverte **à tort**. Ne pas utiliser ce modèle comme indicateur de sécurité ni preuve d'ouverture.

## Liens du projet

- [CAO CadQuery paramétrique](../cad/generate_cad.py)
- [Notice des solides CAO](../cad/README.md)
- [Nomenclature et liens](BOM_V1_VERIFIEE.md)
- [Câblage et alimentation](CABLAGE_V1_VERIFIE.md)
## Mesure directe des 4 fichiers STEP fournis — révision V2

Ces cotes sont des **boîtes englobantes mesurées dans les STEP de l'utilisateur** avec CadQuery/OCP ; elles ne garantissent pas à elles seules les dimensions des composants réels du lot acheté.

| Modèle source | Taille de la boîte englobante mesurée (mm) | Solides | Particularité |
|---|---:|---:|---|
| `Mg90.STEP` | **33,400 × 32,500 × 12,221** | 2 | Boîtier **plus pattes de fixation et arbre** ; l'axe de sortie du modèle est // à Y local |
| `XIAO-nRF52840  v3.step` | **22,482 × 4,460 × 17,780** | 77 | Orientation d'origine dans le plan XZ ; USB et composants inclus |
| `Wio-SX1262_for_XIAO_3D_file V2.step` | **17,780 × 22,316 × 7,642** | 39 | Carte Wio et connecteurs, **hors antenne** |
| `BC547-B.step` | **4,080 × 3,050 × 12,800** | 1 | Corps et broches représentés |

La dimension **22,3 × 11,8 × 26,3 mm** du DMS-MG90 figurant ailleurs correspond à une cote de fiche pour le corps et **ne doit plus servir de volume hors tout de montage**. Le STEP utilisateur est nommé **MG90-A** : la correspondance exacte avec le servo DMS-MG90 reçu devra être vérifiée au pied à coulisse.

**Nouvelle coque CAO : 184 × 100 mm, hauteur avant/arrière 62/65 mm**, ouverture **110 × 42 mm**, panneau **109,4 × 41,4 × 2,4 mm**, jeu **0,30 mm de chaque côté**, toit/socle **3 mm** et parois **2,4 mm**. Le support MG90 est une selle imprimable avec garde de 0,30 mm autour de l'enveloppe STEP, **mais il faut encore concevoir les trous de vis et l'accouplement exact**. Pas de collision mesurée entre servo et coque/toit/support/porte ; voir [rapport V2](../cad/qa_report_v2.json).

L'assemblage Wio **sous** XIAO est une proposition de placement avec très faible intersection numérique entre leurs STEP (≈0,013 mm³) : les connexions mécaniques réelles n'ont pas été montées ni éprouvées. Antennes/câbles/vis non fournis dans ces STEP sont hors du contrôle d'encombrement.

[Source paramétrique V2](../cad/generate_cad.py) — [Notice CAO V2](../cad/README.md) — [Manifestes et références](../cad/vendor_models/README.md).

**Contrôle post-fusion :** le générateur et le JSON paramétrique ont été réconciliés sur la largeur **190 mm** et la baie **110 mm**. Les 4 BREP ont des empreintes SHA256 fixées dans le [manifeste](../cad/vendor_models/manifest.json), contrôlées avant export. Voir [rapport de validation automatisée](../cad/test_step_exports.py).

**Nouvel habillage de baie :** deux retours verticaux à épaisseur **2,4 mm**, profondeur **10 mm**, entièrement à l'extérieur de la baie (0,30 mm de jeu latéral au panneau). Passage Ø3,8 mm pour tourillon Ø3,2 mm à gauche. Coque **190 × 100 mm**, servo décalé de 1,5 mm latéralement, accouplement à concevoir sur un entrefer nominal de **3 mm**. Le bandeau bleu et son STL/STEP ont été retirés. [Notes de validation V3](RETOURS_FACADE_V3.md).
