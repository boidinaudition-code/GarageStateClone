# Protocole radio du prototype

Trame 8 octets (nRF52840 little-endian), identique sur les deux cartes :

| Octets | Champ | Valeur |
|--|--|--|
| 0..1 | network_id (uint16) | 0x6A93 |
| 2 | version | 1 |
| 3 | kind | 0x53 pour état ; 0x41 pour ACK |
| 4..5 | sequence (uint16) | compteur émetteur, repris dans ACK |
| 6 | value | 0 fermé / 1 ouvert / 2 intermédiaire / 3 défaut |
| 7 | reserved | 0 |

Radio : 868,125 MHz ; BW125 kHz ; SF8 ; CR 4/5 ; sync privé 0x12 ; préambule 8 ; +10 dBm ; TCXO 1,8 V.

* Emetteur : nouvelle lecture stabilisée après 150 ms, rapport immédiat ; sans changement, rapport toutes les 60 s.
* Trois essais maximum, chaque essai passe en écoute 600 ms pour l'ACK correspondant au numéro de séquence.
* Le récepteur accuse réception de chaque trame valide et revient en réception continue.
* Le récepteur invalide la fraîcheur après 150 secondes sans état valide. La position physique reste où elle était et la LED clignote.
* Sur une trame « défaut capteurs », ne pas faire bouger le servo.
* Les trames ne sont PAS authentifiées : usage indicatif, ne pas les utiliser pour sécuriser le bâtiment.

Limites connues : aucun journal persistant, aucun chiffrement, capteurs NO non supervisés (fil coupé pouvant apparaître comme non fermé), pas de détection de mouvement continu, aucune protection contre brouillage volontaire, aucun mécanisme de contrôle du rapport cyclique en cas d'utilisation hors scénario normal. Utiliser ce code pour des essais fonctionnels et renforcer avant une installation pérenne.

## Profil V1 à un seul capteur SAS308 (2026-11-21)

La **trame reste identique**. L'émetteur est configuré avec **OPEN_SENSOR_PRESENT=0**. SAS308 câblé **D6 → GND**, aimant présent seulement en position FERMÉE ; **D7 libre**.

- Valeur **0 FERMÉ** : fermeture physiquement constatée par le contact aimanté.
- Valeur **2 INTERMÉDIAIRE** : absence d'aimant, l'ouverture réelle n'est pas encore connue.
- Valeur **1 OUVERT** : **estimation décorative** émise après **40 s** d'absence continue d'aimant, délai configurable dans la compilation via SINGLE_SENSOR_OPEN_ESTIMATE_MS. **Ce n'est PAS une mesure de fin de course ouverte.**
- Valeur **3 DÉFAUT CAPTEURS** : non émise par le montage à un seul SAS308 en fonctionnement normal.

Une porte arrêtée à mi-course plus longtemps que le délai sera **faussement affichée ouverte**. Les LED et le servo du récepteur reproduisent donc une **simulation**. Ne pas utiliser pour sécuriser ou vérifier l'ouverture/fermeture réelle.
