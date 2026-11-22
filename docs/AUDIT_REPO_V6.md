# Audit intégral de cohérence — GarageStateClone V6

**Date : 22 novembre 2026.** Périmètre : **l’ensemble du dépôt public**, notamment firmware, PlatformIO, radio, BOM, câblage, géométries BREP tierces, générateur CadQuery, STEP/STL, visserie et documentation.

Les affirmations ci-dessous distinguent les **faits constatés sur les fichiers**, les **calculs sur modèles STEP**, et les **inconnues liées aux pièces physiques**. Les références STEP d’origine du MG90-A, XIAO, Wio et BC547B sont des modèles tiers fournis ; l’intégrité est contrôlée par empreinte SHA256. Le modèle XIAO simplifié évite un échec d’import Onshape, mais ne représente pas ses composants ou trous.

## 1. Décisions cohérentes et conservées

- V6 mécanique : **150 mm** largeur, **100 mm** profondeur, **62/78 mm** avant/arrière, 2,4 mm murs, 3 mm toit/socle ; pente **16/100 ≈ 9,1°**, toit noir amovible. Porte noire monobloc 99,4×41,4×2,4 mm dans baie 100×42 mm **décentrée de 14 mm à gauche**, sans bandeau bleu.
- Axe haut horizontal à **Y=9,5 / Z=45,4**, volet basculant vers l’intérieur, servo en haut à droite (MG90 à arbre coaxial), palier côté gauche. **Course mécanique CAO échantillonnée sur 0–90°** ; firmware actuellement **15°→95° = 80° d’angle servo**, à calibrer après montage. Ne pas confondre course en degrés du servo et angle physique du volet ; dépend de l’accouplement.
- XIAO nRF52840 + Wio-SX1262 à l’arrière sous toiture sur **faux plafond amovible 144,6×40×2,4 mm**, LED blanche sous plafond ; LED orange en façade.
- Un seul SAS308 réel (fermeture **confirmée**), ouverture **estimée** après 40 s sans aimant ; ce montage ne commande ni ne sécurise le moteur réel.
- Deux antennes LoRa 868 MHz, 5 V externe du servo et GND commun, BC547B + 330/4700/100k et LED orange +680 Ω à D0. **Le XIAO ne fournit pas le courant servo depuis 3V3.**
- Prix électronique de référence **23,43 € TTC** hors quincaillerie, alimentation, câble et transport. Les accessoires déjà livrés avec le servo ne sont pas achetés deux fois.

## 2. Incohérences trouvées et réparations V6

| Sujet | Avant | Correction V6 | Limite résiduelle |
|---|---|---|---|
| Fixation berceau servo | Colonnettes sans vis réelles | **4 pieds de 6×6×5,5**, pilotes **Ø1,7** ; **4 traversées Ø2,3** et fraisures nominales **Ø4,2** dans base, accès dessous | M2×8 fraisée et serrage à tester sur vrai plastique ; boîtier MG90-A seulement en STEP |
| Retenue supérieure servo | Moteur simplement posé dans berceau | **Crochet/lèvre de retenue** intégré à la pièce servo | Élasticité et résistance aux déposes à éprouver |
| Palier gauche | Pièce séparée sans véritable assise | **Petite tablette d’appui** imprimée dans la coque, sous le palier | Liaison positive/collage à confirmer physiquement |
| Porte/servo | **Vide axial de 3 mm**, pas d’interface de porte | Disque intégré Ø12, face X111,5 ; passage Ø12,6 au retour droit ; écart nominal **2,2 mm** avec sortie du servo STEP | **Entraxe du vrai palonnier et sa liaison au disque restent INCONNUS** : disque vierge, percer après mesure |
| Voyant orange / interface porte | Voyant proche du passage d’accouplement | LED orange déplacée vers **X=96**, même Z53,3 | Collerette LED réelle inconnue |
| LED blanche / nervure plafond | **Pénétration CAD intentionnellement tolérée mais non montable**, support dans nervure | Support repositionné **Y=65**, deux ergots **Ø2** dans **Ø2,6** ; surfaces jointives **sans chevauchement** | Précision FDM et collerette LED 5 mm inconnues |
| Cartes sous toiture | Modèles STEP posés au-dessus plafond sans maintien | **4 plots** sous Wio (garde verticale0,3), **2 fentes 3,2×4,2** pour petit lien isolant | Ne pas serrer sur SMD/USB/antenne ; dimensions réelles à vérifier |
| Faisceau câbles | Schéma seulement, aucun guide imprimé | **4 anneaux de paroi** Ø8/Ø3,4, épaisseur radiale2,3 | Décharge de traction externe et conducteurs à réaliser |
| Tolérances | Jeu de conception 0,3 par face, sans calibration | **3 éprouvettes** : axes et alésages Ø3,6/3,8/4,0 ; pilotes M2 Ø1,6/1,7/1,8 ; disque palonnier Ø12 vierge | Tolérances réelles à qualifier sur P1S dans matériau final |
| Build firmware | Bibliothèque Arduino Servo supplémentaire compilée pour chaque rôle, port nRF52 exigeant g_APinDescription incompatible | Supprimer dépendance externe et utiliser la bibliothèque **Servo fournie par le cœur Adafruit nRF52** ; CI compile les deux rôles | Compilation CI obligatoire ; essais physiques toujours non réalisés |
| CI et documentation | Pas de build firmware ni de coupons ; README empilant V1/V5 | Ajouter jobs de build, coupons et tests ; **README canonique V6**, détails dans documents historiques distincts | Les validations ne remplacent pas la qualification terrain |

**Conception** : le crochet servo et les tirants PCB sont des interfaces de prototype. Le disque n’a **volontairement aucun trou de vis “universel” inventé**, et l’utilisateur devra proposer le vrai palonnier devant le gabarit pour fixer la porte de façon démontable.

## 3. Contrôles reproductibles

Depuis la racine du dépôt avec Python **3.11**, CadQuery **2.8** et trimesh **4.11** :

~~~sh
python cad/generate_cad.py
python cad/generate_fit_coupons.py
python cad/qa_geometry.py
python cad/verify_gotronic.py
python cad/test_step_exports.py
python cad/test_hardware_bom.py
python cad/test_fit_coupons.py
~~~

Pour le firmware, installer PlatformIO puis :

~~~sh
pio run -e emetteur
pio run -e recepteur
~~~

GitHub Actions exécute ces vérifications sur PR et push vers main. Les **8 STL, 11 STEP et 3 coupons de contrôle** sont exportés comme artefact, et les firmwares compilés (lorsque la toolchain réussit) sont archivés séparément. Les STL/STEP **générés** ne sont pas versionnés manuellement dans Git pour éviter les merges corrompus.

## 4. Limitations non masquées

1. **Le vrai palonnier MG90 et son entraxe** (la CAO représente un Ø12 vierge et l’espace axial initial). À mesurer puis concevoir une fixation positive, sans colle sur l’axe cannelé.
2. **Le vrai servo DMS-MG90** peut différer du STEP MG90-A fourni ; le clip et les points de vis M2 nécessitent une impression d’essai.
3. **Cartes en combles** : ~6,2 mm sous toit dans le modèle, hors antenne, USB, épaisseur de mousse isolante, fil et courbure ; tester avant fermeture.
4. **SAS308/aimant** : fixation dans le garage réel à concevoir sans percer ni gêner ressorts, rails, galets, motorisation ou dispositifs de sécurité.
5. **Boîtier émetteur isolant** : toujours non modélisé dans les huit STL du garage miniature.
6. **Fils et alimentation** : protection/anti-traction et masse commune à câbler, capacité servo à mesurer, deux antennes 868 MHz avant transmission.
7. **Protocole** : pas de télémétrie sécuritaire ni de confirmation d’ouverture réelle. Le réseau n’est pas authentifié et ne doit pas piloter le vrai moteur.

## 5. Critères de réussite physique

Voir la [checklist d’assemblage](ASSEMBLAGE_V6.md). Le projet n'est pas « prêt à imprimer en version définitive » tant que le vrai palonnier, les fixations du MG90, le maintien non conducteur du Wio et le cheminement des fils n’ont pas été essayés.

**CI / code source :** le statut du dernier workflow GitHub Actions est la source de vérité pour les compilations et les tests géométriques, car ce document est rédigé avant l’exécution finale post-merge. Ne jamais interpréter une PR ouverte ou un fichier STEP présent comme une preuve d’import réussi dans Onshape ou de montage matériel réussi.
