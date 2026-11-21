# Nomenclature vérifiée — GarageStateClone V1

Vérification du **21 novembre 2026** : comparaison des références constructeur, du firmware et du nouveau schéma électrique. Les prix sont des **prix produits indicatifs TTC**, hors frais de livraison ; vérifier le panier avant paiement.

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
| **1** | Contact magnétique miniature **SAS308**, réf. Gotronic **26449** | **3,90 €** (1 capteur) (prix fiche article vérifié) | [Gotronic — SAS308](https://www.gotronic.fr/art-contact-magnetique-miniature-sas308-12751.htm) ; **aimants inclus**, vis non fournies ; écart maxi **15 mm**, boîtier **24 × 15 × 6 mm**, **25 cm de câble moulé** par capteur ; contact fermé aimant en face (tester avant pose) |
| **1** | Microservo **DFRobot DMS-MG90**, réf. Gotronic **36923** | **7,90 €** | [Gotronic — servo](https://www.gotronic.fr/art-servomoteur-dms-mg90-32266.htm) ; **4,8–6 V**, course **2 × 90°**, pignons métal, palonnier et visserie inclus |
| **1** | Condensateur **470 µF / 16 V**, réf. Gotronic **04947** | **0,20 €** | [Gotronic — condensateur](https://www.gotronic.fr/art-condensateur-radial-470uf-16v-3386.htm) ; **polarisé**, +5 V / GND à proximité du servo |
| **1** | Transistor **BC547B NPN** TO-92, réf. Gotronic **02173** | **0,15 €** | [Gotronic — BC547B](https://www.gotronic.fr/art-transistor-bc547b-1336.htm) ; **ajout important** : LED blanche 5 V pilotée depuis D7 sans la faire passer directement par le GPIO |
| **1 utilisée** | **330 Ω** — lot de 5, réf. Gotronic **04130** | **0,30 € le lot** | [Gotronic — résistances 330 Ω](https://www.gotronic.fr/art-5-resistances-1-2w-330-8486-2653.htm) ; série **+5 V → LED blanche** |
| **1 utilisée** | **680 Ω** — lot de 5, réf. Gotronic **04134** | **0,30 € le lot** | [Gotronic — résistances 680 Ω](https://www.gotronic.fr/art-5-resistances-1-2w-680-8486-2657.htm) ; série **3V3 → LED orange → D0** |
| **1 utilisée** | **4,7 kΩ** — lot de 5, réf. Gotronic **04144** | **0,30 € le lot** | [Gotronic — résistances 4,7 kΩ](https://www.gotronic.fr/art-5-resistances-1-2w-4-7-k-8486-2667.htm) ; série **D7 → base BC547B** |
| **1 utilisée** | **100 kΩ** — lot de 5, réf. Gotronic **04160** | **0,30 € le lot** | [Gotronic — résistances 100 kΩ](https://www.gotronic.fr/art-5-resistances-1-2w-100-k-8486-2681.htm) ; **base BC547B → GND**, évite l'allumage au démarrage |
| **1** | LED **blanche chaude** THT 3 mm 3000 K, ex. **304WC2J-W6-3PD** | **0,19 € pièce**, vendue par **10 min.**, soit **1,90 €** avant port | [RPtronics — 304WC2J-W6-3PD](https://rptronics.fr/led-blanche-chaude-ronde-3mm-5000-8500mcd-304wc2j-w6-3pd%2C179414.html) ; Vf annoncé **2,6–3,6 V** ; prévue **sur +5 V via BC547B** |
| **1** | LED orange THT **3 mm non clignotante**, ex. **LED3OLN** | **0,40 €** | [Lextronic — LED orange diffusante 3 mm](https://www.lextronic.fr/leds-18-mm-a-3-mm-10919) ; le clignotement est réalisé par le firmware. Variante plus lumineuse sur la même page : **L-7104SEC-H**, 0,80 € |

**Sous-total des références chiffrées : environ 15,65 € TTC**, comprenant les quatre lots de résistances et le lot minimum de dix LED blanches, **hors livraisons, câbles, alimentation, borniers et fixation**. Ne pas confondre sous-total et budget complet.

**Livraison rapide :** Gotronic annonce généralement Colissimo en **24/48 h + préparation** pour la France selon l'article et le transporteur ; les autres marchands facturent chacun leur port. **Deux boutiques supplémentaires ne sont pas indispensables** : si tu as déjà les LED dans ton stock, ne commande pas chez RPtronics et Lextronic. Pour une seule commande, on peut rechercher une LED compatible équivalente chez le vendeur principal, mais **une LED blanche marquée Vf 3,5 V doit être raccordée à +5 V avec le transistor**, pas directement à 3V3.

## Fournitures indispensables si absentes

- **Deux alimentations USB 5 V au total minimum** : une près de la vraie porte (XIAO émetteur), une dans la maison pour la miniature (**5 V / 2 A recommandé**).
- Côté miniature : **répartiteur d'alimentation 5 V** avec branche USB-C vers le XIAO **et sortie 5 V / GND distincte** vers le servo et la LED blanche, **OU** un second chargeur USB 5 V pour le servo/LED avec **GND commun** à celui du XIAO. Ne pas mettre les deux +5 V de deux chargeurs en parallèle.
- **2 câbles USB-C** vers les XIAO (plus un câble d'alimentation permettant la distribution vers le servo selon montage retenu).
- **Fils souples**, borniers ou connecteurs, petit morceau de **plaque à souder/perfboard**, gaine thermorétractable et isolants.
- **Vis de fixation du SAS308** (non fournies), **fil 2 conducteurs et raccordements protégés pour rallonger leurs câbles moulés de 25 cm**, support imprimé pour LED orange en façade et LED blanche sous le toit, axe/palier et support servo imprimés.
- Multimètre pour tester la polarité, les résistances, le contact magnétique et les masses.

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
