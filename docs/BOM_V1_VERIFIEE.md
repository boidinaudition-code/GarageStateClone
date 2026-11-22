# BOM vérifiée — GarageStateClone V5 (électronique et quincaillerie)

**Révision 22 novembre 2026** à partir des références Gotronic et de la CAO V5. Prix TTC indicatifs, disponibilités à revérifier, aucun achat ni essai physique. Pour la visserie et les fournitures de montage, voir **[quincaillerie V5 et liste des pièces manquantes](QUINCAILLERIE_MONTAGE_V5.md)**. Les fixations du servo et du XIAO restent à concevoir : la liste n'est donc pas une nomenclature de montage totalement figée.

- [Schéma émetteur](../assets/schemas/cablage-emetteur-v1.svg)
- [Schéma récepteur](../assets/schemas/cablage-recepteur-v1.svg)
- [Guide de câblage précis](CABLAGE_V1_VERIFIE.md)

## Déjà disponible — ne pas racheter

| Qté | Matériel | À vérifier |
|---:|---|---|
| 2 | Seeed **XIAO nRF52840 + Wio-SX1262**, à **deux barrettes 7 broches** | Antennes adaptées **868 MHz**, accès physique aux GPIO D6 et D7 sous le Wio |
| 1 | **Bambu Lab P1S + AMS** | Filaments blanc, noir, bleu, rouge |
| 1 | Prise secteur dans le vrai garage | Réservée à un **chargeur USB isolé** ; aucune liaison avec la motorisation |

## Pièces électroniques de la V1

| Qté à monter | Pièce et référence | Prix produit TTC | Achat / vérification |
|---:|---|---:|---|
| **1** | Contact magnétique miniature **SAS308**, réf. Gotronic **26449** | **3,90 €** | [Gotronic — SAS308](https://www.gotronic.fr/art-contact-magnetique-miniature-sas308-12751.htm) ; **aimant inclus**, vis non fournies ; écart maxi **15 mm**, boîtier **24 × 15 × 6 mm**, **25 cm de câble moulé** ; contact fermé aimant en face (tester avant pose) |
| **1** | Microservo **DFRobot DMS-MG90**, réf. Gotronic **36923** | **7,90 €** | [Gotronic — servo](https://www.gotronic.fr/art-servomoteur-dms-mg90-32266.htm) ; **4,8–6 V**, course **2 × 90°**, pignons métal, palonnier et visserie inclus |
| **1** | Condensateur **470 µF / 16 V**, réf. Gotronic **04947** | **0,20 €** | [Gotronic — condensateur](https://www.gotronic.fr/art-condensateur-radial-470uf-16v-3386.htm) ; **polarisé**, +5 V / GND à proximité du servo |
| **1** | Transistor **BC547B NPN** TO-92, réf. Gotronic **02173** | **0,15 €** | [Gotronic — BC547B](https://www.gotronic.fr/art-transistor-bc547b-1336.htm) ; **ajout important** : LED blanche 5 V pilotée depuis D7 sans la faire passer directement par le GPIO |
| **1 utilisée** | **330 Ω** — lot de 5, réf. Gotronic **04130** | **0,30 € le lot** | [Gotronic — résistances 330 Ω](https://www.gotronic.fr/art-5-resistances-1-2w-330-8486-2653.htm) ; série **+5 V → LED blanche** |
| **1 utilisée** | **680 Ω** — lot de 5, réf. Gotronic **04134** | **0,30 € le lot** | [Gotronic — résistances 680 Ω](https://www.gotronic.fr/art-5-resistances-1-2w-680-8486-2657.htm) ; série **3V3 → LED orange → D0** |
| **1 utilisée** | **4,7 kΩ** — lot de 5, réf. Gotronic **04144** | **0,30 € le lot** | [Gotronic — résistances 4,7 kΩ](https://www.gotronic.fr/art-5-resistances-1-2w-4-7-k-8486-2667.htm) ; série **D7 → base BC547B** |
| **1 utilisée** | **100 kΩ** — lot de 5, réf. Gotronic **04160** | **0,30 € le lot** | [Gotronic — résistances 100 kΩ](https://www.gotronic.fr/art-5-resistances-1-2w-100-k-8486-2681.htm) ; **base BC547B → GND**, évite l'allumage au démarrage |
| **1 utilisée** | LED **blanche chaude 5 mm** issue du lot **Whadda WCS101**, Gotronic **03989** | **9,90 € le lot** (relu) | [Gotronic — 130 LED WCS101](https://www.gotronic.fr/art-assortiment-de-130-leds-wcs101-39775.htm) ; contient **20 blanches chaudes**. Une seule montée, non RGB, **+5 V via 330 Ω et BC547B** ; ni puissance ni ruban. Vf, courant admissible, Kelvin, collerette, longueur et pas des pattes à confirmer pour cette LED du lot |
| **1** | LED orange THT **5 mm L7113NC**, Gotronic **03051** | **0,18 €** (relu) | [Gotronic — L7113NC](https://www.gotronic.fr/art-led-5-mm-l7113nc-2086.htm) ; boîtier clair, **15°**, **80 mcd à 10 mA** annoncés ; 680 Ω conservée, clignotement logiciel. Luminosité réelle à tester. LED cachée en retrait derrière un petit point façade |

**Sous-total électronique corrigé : 23,43 € TTC.** Comprend les quatre lots de résistances à 0,30 € chacun et le lot complet WCS101, pas seulement une LED. C1 est confirmé à 0,20 €, le servo à 7,90 € et le BC547B à 0,15 €.

**Prix et stocks non réservés.** Calcul mis à jour : **3,90 + 7,90 + 0,20 + 0,15 + 4 × 0,30 + 9,90 + 0,18 = 23,43 € TTC.** Le prix du lot de 130 LED WCS101 est inclus en entier même si une seule LED chaude est utilisée. Le SAS308 est bien affiché à **3,90 € TTC sur sa fiche directe** ; les stocks et délais restent à vérifier au panier. Alimentation, câbles, visserie, boîtier et port exclus.

## Fournitures indispensables si absentes

- **Deux alimentations USB 5 V au total minimum** : une près de la vraie porte (XIAO émetteur), une dans la maison pour la miniature (**5 V / 2 A recommandé**).
- Côté miniature : **répartiteur d'alimentation 5 V** avec branche USB-C vers le XIAO **et sortie 5 V / GND distincte** vers le servo et la LED blanche, **OU** un second chargeur USB 5 V pour le servo/LED avec **GND commun** à celui du XIAO. Ne pas mettre les deux +5 V de deux chargeurs en parallèle.
- **2 câbles USB-C** vers les XIAO (plus un câble d'alimentation permettant la distribution vers le servo selon montage retenu).
- **Fils souples**, borniers ou connecteurs, petit morceau de **plaque à souder/perfboard**, gaine thermorétractable et isolants.
- **Vis de fixation du SAS308** (non fournies), **fil 2 conducteurs et raccordements protégés pour prolonger son câble moulé de 25 cm**, support imprimé pour LED orange en façade et LED blanche **sous le faux plafond**, **tourillon de porte déjà imprimé Ø3,2 mm**, palier/support servo imprimés, **accouplement servo/porte et boîtier de l'émetteur encore à concevoir**.
- Multimètre pour tester la polarité, les résistances, le contact magnétique et les masses.

### Sélection Gotronic hors panier noyau

Quantités de départ **si rien n'est en stock**, non cumulables entre variantes d'alimentation. Références trouvées sur les pages Gotronic ; une référence identifiée ne garantit pas la compatibilité finale.

| Fourniture | Qté / référence Gotronic | Choix et réserves |
|---|---|---|
| Chargeurs secteur USB-A 5 V, ≥2 A | **2 minimum**, ou **3** pour la variante séparée ; [HNP18-USBV2 14749](https://www.gotronic.fr/art-alimentation-hnp18-usbv2-38701.htm) | **5 V / 3 A**, protection surcharge/court-circuit, 11,70 € relevés dans la recherche ; ne pas ouvrir le boîtier secteur. Vérifier le panier et réutiliser les alims possédées adaptées |
| Câbles USB-A mâle → USB-C mâle pour XIAO | **2** ; [cordons Type-C Gotronic](https://www.gotronic.fr/cat-cordons-usb-type-c-1829.htm), ex. GB45743 **49311** | Longueur 1 m extensible, 4,90 € repérés ; référence/prix/courant à confirmer sur fiche et au panier ; prévoir données pour flash |
| Sortie de puissance servo externe, variante à 3 chargeurs | **1** [cordon USB-A → DC 5,5/2,1 49101](https://www.gotronic.fr/art-cordon-usb-alim-5-5-x-2-1-mm-34157.htm) + **1** [PCM10F 48214](https://www.gotronic.fr/art-adaptateur-pcm10f-17984.htm) | Cordon 90 cm, **2 A maxi** ; bornier femelle **4 A maxi**, 40 × 15 × 11 mm. Contrôler +/− au multimètre ; fils vers servo, C1 et R1 ; relier GND au XIAO, **pas les +5 V de ses deux chargeurs** |
| Répartition avec une seule source côté miniature | À réaliser / **référence de répartiteur non confirmée** | En amont des cartes : source 5 V → deux branches USB-C XIAO et puissance servo. Pas de hub de données, pas de câble Y reliant deux sorties de chargeurs. La variante précédente est l'alternative documentée, pas un répartiteur acheté garanti |
| Fil souple puissance et prolongation SAS308 | Longueur à mesurer ; [FC50G **08941**](https://www.gotronic.fr/art-fil-de-cablage-fc50g-5200.htm) | **0,50 mm²**, Ø extérieur 1,8 mm, 0,40 €/m relevé ; repérer +/GND aux deux extrémités. Deux conducteurs séparés protégés pour le capteur ; fil fin pour GPIO à sélectionner selon soudure |
| Perfboard | **1** [BCS050 **12470**](https://www.gotronic.fr/art-plaque-d-essais-bcs050-6931.htm) | 50 × 100 × 1,5 mm, pas 2,54 mm ; **à découper et isoler**, ne rentre pas entière sur le plateau 60 × 31. Implantation finale à mesurer |
| Gaine thermorétractable | **1 pochette** [FTK01 **08918**](https://www.gotronic.fr/art-pochette-de-gaine-thermo-rouge-et-noire-ftk01-5179.htm) | 20 longueurs de 200 mm, Ø1,6 à 6,4 mm avant rétreint 2:1 ; 5,50 € repérés. La gaine seule ne qualifie pas l'étanchéité des jonctions garage |
| Visserie et quincaillerie V5 | [**11850** Ø2,2×6,5 autotaraudeuses, 0,65 €/10](https://www.gotronic.fr/art-10-vis-auto-taraudeuses-2-2x6-5mm-6681.htm) ; [**11636** M2×8, 0,65 €/10](https://www.gotronic.fr/cat-visserie-685.htm) ; M2 écrous **11592** 0,40 €/10 et rondelles **11593** 0,20 €/10 | **À confirmer après dessin des trous**. Ces vis sont du stock de prototype, **pas une taille prouvée pour le MG90/SAS308** ; palonniers et visserie servo **déjà fournis** ; aucun axe métal à acheter pour le tourillon imprimé. [Détails](QUINCAILLERIE_MONTAGE_V5.md) |

**Total complet : non déterminé.** Le noyau est désormais **23,43 € TTC** ; les fournitures réellement absentes, dimensions des fixations, longueurs de fils, variantes d'alimentation et port ne sont pas inclus. **Ne pas additionner toutes les options de quincaillerie ni les variantes d'alimentation.** Les alims déjà possédées sont exclues des achats, pas des besoins. Les outils, consommables de soudure et pièces imprimées restent à inventorier. Toutes les pistes d'achat ci-dessus sont chez Gotronic ; les liens constructeur servent de documentation, non de deuxième boutique.

Les fiches consultées ne donnent pas les cotes détaillées de la blanche chaude du WCS101. La fiche L7113NC renvoie un PDF **L7113EC (autre couleur/référence)** : ne pas lui attribuer ces cotes ou sa Vf sans confirmation. Aucune ancienne cote Luckylight n'est réutilisée.

## Analyse des risques / corrections

1. **LED blanche : ancienne erreur évitée.** Plusieurs LED blanches Gotronic sont données à **Vf 3,5 V** ; il serait trompeur de garantir un éclairage depuis GPIO D7 à 3,3 V. Le nouveau schéma utilise un **BC547B + 4,7 kΩ + 100 kΩ** et 330 Ω sur l'alimentation 5 V.
2. **D0 : déjà relié à un bouton et à une résistance de pull-up 10 kΩ sur le Wio-SX1262 nRF52840.** L'orange (680 Ω) est câblée **3V3 → résistance → anode LED → cathode D0**. Logiciel : **LOW = allumée ; INPUT = éteinte**. Ne jamais piloter D0 HIGH dans ce schéma.
3. **Servo : jamais sur 3V3.** 5 V externe, GND commun, condensateur polarisé en parallèle près du servo ; le servo peut demander des pics de courant.
4. **Capteur unique SAS308 : vérifier NF/NO.** La fiche les appelle « NF », mais précise que le contact est **fermé lorsque l'aimant est en face** : c'est la logique du firmware (**contact fermé → entrée LOW**). Vérifier chaque exemplaire à l'ohmmètre. **Distance maxi 15 mm**, viser moins pour garder une marge contre les vibrations. Les **25 cm de fils moulés** peuvent nécessiter une prolongation.
5. **Antennes 868 MHz :** branchées avant mise sous tension radio ; pas de connexion LoRa sans antenne.
6. **Broches réellement accessibles :** D6/D7 ne sont pas routées au Wio, mais accessibles sur le XIAO lui-même ; en montage empilé, prévoir une soudure et isolation soigneuses.

## Sources

- [Seeed : schéma du Wio-SX1262 pour XIAO V1.0](https://files.seeedstudio.com/products/113010003/Wio-SX1262%20for%20XIAO%20V1.0.pdf)
- [Seeed : brochage du XIAO nRF52840](https://wiki.seeedstudio.com/XIAO_BLE/)
- [Gotronic : page SAS308](https://www.gotronic.fr/art-contact-magnetique-miniature-sas308-12751.htm)
- [Gotronic : page servo DMS-MG90](https://www.gotronic.fr/art-servomoteur-dms-mg90-32266.htm)
- [Gotronic : exemple de LED blanche Vf 3,5 V](https://www.gotronic.fr/art-led-3-mm-l3fwc1-35813.htm)

## Dimensions constructeur et correction V1

- **Le BOM V1 utilise désormais 1 seul SAS308**, détecteur de **fermeture confirmée** sur D6. Le contact D7 côté émetteur est supprimé du montage. L'absence d'aimant n'est pas une preuve d'ouverture ; une **estimation temporisée à 40 s** alimente seulement la maquette décorative.
- **Dimensions détaillées, une ligne par composant : [ENCOMBREMENT_BOM_V1.md](ENCOMBREMENT_BOM_V1.md)**. Y figurent les cotes constructeur du servo, condensateur, résistances, transistor, LED, XIAO/Wio, mais aussi les cotes **non publiées à mesurer**.
- Pour la CAO, ne pas reprendre l'ancien gabarit servo approximatif : **corps DMS-MG90 22,3 × 11,8 × 26,3 mm** ; cap **Ø10 × 13 mm, pas 5 mm** ; les résistances métal 1/2 W font **6,5 × Ø2,5 mm**. Les emboîtements seront dimensionnés à **0,30 mm de jeu par face**, parois ≥2 mm.


## Quincaillerie de la V5 — audit final

**[Fiche complète de montage, quantité par emplacement, liens d'achat et statut de compatibilité](QUINCAILLERIE_MONTAGE_V5.md)**. La V5 reste **150 × 100 mm**, toit **62/78 mm**, XIAO/Wio au-dessus d'un faux plafond amovible et LED blanche en dessous.

| Accessoire ajouté / disponibilité | Budget de référence (catalogue, pas commande) | Statut |
|---|---:|---|
| [**11850**, 10 vis autotaraudeuses Ø2,2 × 6,5](https://www.gotronic.fr/art-10-vis-auto-taraudeuses-2-2x6-5mm-6681.htm) | **0,65 €** | **OPTION** : seulement après modélisation des bossages percés en plastique |
| [**11636**, 10 vis inox fraisées M2 × 8](https://www.gotronic.fr/cat-visserie-685.htm) + [**11592**, 10 écrous M2](https://www.gotronic.fr/cat-visserie-685.htm) + [**11593**, 10 rondelles M2](https://www.gotronic.fr/cat-visserie-685.htm) | **0,65 + 0,40 + 0,20 €** | **OPTION** : support servo/bras encore sans trous homologués |
| [**11845**, 100 colliers noirs 2,5 × 100 mm](https://www.gotronic.fr/cat-colliers-de-serrage-1330.htm) | **1,20 €** | **À PRÉVOIR SI ABSENTS** pour maintien des petits câbles |
| [**49463**, 12 clips adhésifs MMP108, câble Ø4 mm maxi](https://www.gotronic.fr/art-12-clips-support-de-cable-40452.htm) | **1,80 €** | **OPTION** pour support fixe du vrai garage, trop grand pour certains emplacements de maquette |
| [**37783**, adaptateur JR servo vers 3 contacts mâles, 170 mm](https://www.gotronic.fr/art-adaptateur-pour-servos-vers-contacts-males-35364.htm) | **2,35 €** | **RECOMMANDÉ SI ABSENT**, pour un servo démontable sans couper sa prise JR |
| [**49090**, fil multibrins 0,14 mm² noir (10 m)](https://www.gotronic.fr/cat-fil-de-cablage-souple-0-14-mm-1569.htm) | **2,30 €** | **À PRÉVOIR SI ABSENT**, ajouter autre couleur ou 2e longueur, notamment pour prolonger SAS308 |
| [**08906**, gaine thermorétractable adhésive FT3/1](https://www.gotronic.fr/cat-gaine-thermoretractable-823.htm) | **3,60 €** | **SI PROLONGATION du SAS308** en zone humide/poussiéreuse |
| **Supports de détecteur et d'aimant, boîtier émetteur, bride XIAO sur faux plafond, accouplement servo/porte** | **À réaliser/imprimer**, non chiffré | **MANQUENT encore de la CAO définitive**, aucune vis M3 arbitraire à acheter |

Les **vis/palonniers du DMS-MG90 sont livrés avec lui**. Le **tourillon gauche Ø3,2 mm est imprimé avec la porte**, le palier Ø3,8 mm est imprimé : **aucun axe métallique à ajouter**. Toit, socle et faux plafond sont des emboîtements, **aucune vis obligatoirement ajoutée** tant que les impressions d'essai le confirment.

**Points d'arrêt avant commande finale :** relever trous SAS308/aimant, pattes et palonnier du MG90 réellement livré, fixation non conductrice de XIAO/Wio, espace USB-C et antenne sous le toit (~6,2 mm théoriques), et longueur du câble jusqu'au capteur. Ne jamais percer les rails/éléments de sécurité du vrai garage, ni connecter un GPIO au moteur secteur. Alim servo 5 V externe et GND commun indispensables.

L'achat d'une visserie optionnelle **ne suffit pas** à résoudre la fixation mécanique tant que les perçages/supports ne sont pas modélisés.
