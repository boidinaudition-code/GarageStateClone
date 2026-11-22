# BOM V6 — nomenclature de référence et quincaillerie à approvisionner

**Révision : 22 novembre 2026.** Document de référence courant pour la coque **150 × 100**, toit **62 / 78**, mécanique V6. La [BOM de 2026-11-21/V5](BOM_V1_VERIFIEE.md) et le [détail historique de la quincaillerie V5](QUINCAILLERIE_MONTAGE_V5.md) sont conservés comme traces d'audit mais **ne définissent pas les fixations V6 actuelles**. La vraie compatibilité des vis servo/horn et de l'antenne demande une mesure avant montage définitif.

**Sources dimensionnelles mises à jour** : voir [l'audit V7 de toutes les fiches cotées](FICHES_COTEES_COMPOSANTS_V7.md) et [son inventaire JSON](../cad/component_dimensions_sources_v7.json). **Erratum et géométrie V7 :** les **33 mm** constructeur (oreilles, suivant Z) et les **32,5 mm** du STEP (sortie d'arbre, suivant X) avaient été comparés par erreur : la réserve de 0,05 mm n'est pas valable. Deux **encoches Ø2 à entraxe 29 mm** sont désormais alignées sur **2 pilotes imprimés** du berceau V7. **4 vis supplémentaires, indépendantes**, fixent le berceau au socle. [Détails de conception V7](FIXATIONS_SERVO_V7.md). Longueur et tête des vis, épaisseur réelle des oreilles et palonnier à vérifier.

## A. Déjà disponible — ne pas acheter deux fois

| Quantité | Élément | Vérification requise |
|---:|---|---|
| **2 kits** | **Seeed XIAO nRF52840 + Wio-SX1262** (émetteur et récepteur) | Broches D6/D7 réellement accessibles, compatibilité de leurs **2 antennes 868 MHz** et de leurs raccords |
| **1** | Bambu Lab P1S + AMS | Filaments disponibles blanc/noir/bleu/rouge (bleu non utilisé dans le garage V6) |
| **1** | MG90 palonnier, vis centrale, visserie et prise JR | Ces accessoires **sont fournis avec le DMS-MG90** ; mesurer le palonnier fourni plutôt que racheter un axe ou un kit d'entraxe supposé |
| **1** | Tourillon de porte Ø3,2 et palier Ø3,8 | **Imprimés dans les pièces 04/05**, aucun axe métallique à commander |
| **1** | Base, toit et faux plafond | Emboîtements imprimés ; aucune vis d'assemblage générale imposée |

## B. Électronique supplémentaire : total indicatif 23,43 € TTC

| Qté montée / achat | Composant | Gotronic / prix par conditionnement | Usage |
|---|---|---|---|
| 1 | SAS308 détecteur + aimant | [26449 — **3,90 €**](https://www.gotronic.fr/art-contact-magnetique-miniature-sas308-12751.htm) | Détecte *fermé* uniquement, 25 cm de fil, pas de vis |
| 1 | DFRobot DMS-MG90 | [36923 — **7,90 €**](https://www.gotronic.fr/art-servomoteur-dms-mg90-32266.htm) | Entraînement miniature 5 V, 180° positionnel, palonniers/vis fournis |
| 1 | Condensateur 470 µF, 16 V | [04947 — **0,20 €**](https://www.gotronic.fr/art-condensateur-radial-470uf-16v-3386.htm) | Sur 5 V/GND servo près du moteur |
| 1 | BC547B TO-92 | [02173 — **0,15 €**](https://www.gotronic.fr/art-transistor-bc547b-1336.htm) | Commande LED blanche à partir de D7 |
| 1 de chaque, **4 lots de 5 achetés** | Résistances 330 Ω, 680 Ω, 4,7 kΩ, 100 kΩ | **04130 / 04134 / 04144 / 04160 : 4 × 0,30 € = 1,20 €** | LED blanche, LED orange, base et rappel transistor |
| 1 blanche chaude montée / **lot de 130 acheté** | Whadda WCS101 | [03989 — **9,90 €**](https://www.gotronic.fr/art-assortiment-de-130-leds-wcs101-39775.htm) | Le lot inclut 20 LEDs blanches chaudes ; une seule utilisée |
| 1 | L7113NC orange 5 mm | [03051 — **0,18 €**](https://www.gotronic.fr/art-led-5-mm-l7113nc-2086.htm) | Voyant façade D0, déjà masqué par trou optique |

**Total noyau : 3,90 + 7,90 + 0,20 + 0,15 + 1,20 + 9,90 + 0,18 = 23,43 € TTC**, si ces composants ne sont pas déjà en stock. **Ni livraison, ni alimentation, ni fils, ni fixation ne sont inclus**. Les prix et disponibilités restent variables, à confirmer au panier.

## C. Quincaillerie V6 réellement dessinée et fournitures à prévoir

| Besoin | Quantité *dans le montage* | Référence ou solution | Statut |
|---|---:|---|---|
| **Visser le berceau sous le socle** | **4 vis** | [Gotronic **11636** M2×8 tête fraisée, lot 10](https://www.gotronic.fr/cat-visserie-685.htm), à essayer avec **trou Ø2,3**, **fraisure Ø4,2** dans socle et **pilote Ø1,7** dans 4 pieds **6×6×5,5** | **DESSINÉ V6, MAIS À ESSAYER** sur coupon B : pas de preuve de filetage ou de hauteur de tête sur vrai plastique |
| **Accouplement vrai servo/porte** | 1 palonnier, montage positif avec ses vrais trous | Le **palonnier fourni** est retenu par sa vis centrale sur sortie cannelée ; **disque porte Ø12 sans trous** pour reporter ensuite l'entraxe | **À DIMENSIONNER** ; aucune taille M1.6/M2 arbitraire garantie pour fixer le disque au palonnier |
| **Retenir le vrai servo** | **2 vis** | **2 pilotes Ø1,7 espacés de 29 mm** suivant les **2 encoches ouvertes Ø2** du DMS-MG90, sur colonne imprimée V7 | **CAO V7**, type de vis, hauteur d'oreille et tenue physique à confirmer |
| **Retenir le palier gauche** | 1 fixation ponctuelle | **Assise imprimée** sous palier, colle compatible PLA/PETG ou fixation à redessiner | **DESSINÉ comme appui**, adhérence à valider ; pas de vis imposée |
| **Retenir XIAO/Wio dans les combles** | 1 lien **2,5 mm** + protection isolante | [Colliers nylon noir **11845**, 2,5×100 mm / lot 100](https://www.gotronic.fr/cat-colliers-de-serrage-1330.htm) ; passages **3,2×4,2** dessinés + 4 plots sous carte | **DESSINÉ V6**, serrer très doucement et vérifier que la sangle ne porte pas sur SMD/antenne/USB |
| **Fixer LED blanche sous faux plafond** | 2 ergots + adhésif facultatif | **Ø2 dans Ø2,6**, deux languettes imprimées, aucun vis nécessaire | **DESSINÉ V6**, 0,30 mm par face, vérifier collerette LED réelle |
| **Acheminer câbles de miniature** | **4 anneaux imprimés** + liens souples si besoin | Anneaux **Ø8/Ø3,4**, paroi 2,3 mm ; fil souple multibrins **0,14 mm²** (par ex. Gotronic **49090**) pour signaux | **DESSINÉ V6**, fils à arrimer loin de la porte, 5 V servo avec conducteur adapté au courant |
| **Prolonger le SAS308** | 2 conducteurs + 2 jonctions protégées, selon distance | Fil fin 2 conducteurs ; thermo adhésive **08906** ou boîte de jonction adaptée ; clips/attaches de câble si nécessaire | **SI FIL MOULÉ DE 25 CM TROP COURT**, trajet à mesurer dans vrai garage |
| **Brancher servo démontable** | 1 adaptateur optionnel | [**37783** JR femelle → 3 contacts mâles, 170 mm](https://www.gotronic.fr/art-adaptateur-pour-servos-vers-contacts-males-35364.htm) | **OPTION**, sauf connecteur JR installé sur une perfboard |
| **Petit circuit assemblé** | 1 | Morceau **env. 25×30 mm** de perfboard BCS050 (Gotronic **12470**), soudure, gaine isolante | **À PRÉVOIR** si absent ; la plaque complète 50×100 ne rentre pas telle quelle dans les combles |
| **Alimentation** | 2 chargeurs 5 V min. / 3 selon architecture | Deux XIAO en USB-C ; branche servo **5 V externe** d'au moins 2 A recommandés côté miniature, **masse commune**, aucune liaison des +5 V de chargeurs différents | **IMPÉRATIF**, choix de répartiteur/chargeurs encore ouvert ; voir [câblage](CABLAGE_V1_VERIFIE.md) |
| **Boîtier émetteur dans vrai garage** | 1 | Boîtier isolant imprimé ou acheté, fixation sur support immobile | **NON MODÉLISÉ**, vérifier poussière/humidité et passage câble/antenne |
| **Fixer SAS308 et aimant sur vraie porte** | 2 emplacements | Supports imprimés ou attaches non invasives adaptées, **sans percer rail, galets ou moteur** | **À CONCEVOIR après inspection**, entraxes des trous SAS308 et aimant non mesurés |
| **Protection USB/antenne** | 2 entrées/arrimage | Décharge de traction, protection anti-arête ; passages 12×8 et 16×9 présents | **À FINALISER**, connecteurs et rayon de courbure non fournis par les STEP |

**Non requis par défaut :** axe métallique, roulement, inserts M3, grosses entretoises 10 mm, vis toit/socle hors berceau, second SAS308, ruban LED, nouveau palonnier, vis de la sortie cannelée.

**À commander après essais uniquement :** vis spécifiques du palonnier *vers disque Ø12*, attaches de capteur/aimant du vrai garage et éventuels adaptateurs de fixation du servo si le crochet ne convient pas.

## D. Bons de contrôle avant le « prêt à monter »

1. Mesurer l'entraxe et l'épaisseur du **vrai palonnier** du servo ; le disque Ø12 est un **gabarit vierge**, avec un **espace axial nominal 2,2 mm** jusqu'à la sortie servo en STEP. Si la pièce réelle occupe davantage, **modifier la CAO**, pas forcer.
2. Imprimer **coupon B** : essayer les M2×8 fraisées dans les pilotes Ø1,6 / Ø1,7 / Ø1,8. La vis doit tenir sans casser le pied. Le lot 11636 est une *hypothèse de vis*, pas une validation imprimante.
3. Imprimer **coupon A** : tourillon Ø3,2 / alésages Ø3,6, 3,8 et 4,0 ; conserver la valeur qui tourne librement sans jeu visible excessif.
4. Tester le **crochet servo** sur le DMS-MG90, plusieurs insertions/déposes sans casse, toit fermé.
5. Utiliser une **fine protection souple isolante** sous le lien radio ; ne jamais écraser les SMD ni gêner prise USB/antenne (~6,2 mm de garde brute dans la CAO).
6. Poser et fixer à blanc l'émetteur réel hors mobile, protections de rallonge si besoin ; vérifier deux antennes 868 MHz.

**La nomenclature V6 est cohérente avec les composants/quantités et les formes modélisées, pas avec un assemblage physique déjà validé.** [Guide de montage détaillé](ASSEMBLAGE_V6.md).
