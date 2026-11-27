# Récupération automatique du récepteur

Retour terrain : ouverture/fermeture correctes, blocage après inactivité, plus de signal de liaison perdue. Cause physique non établie. Correctif limité au récepteur et à l'initialisation radio commune (émetteur et protocole inchangés fonctionnellement).

- WDT matériel nRF52840 8 s, alimenté uniquement à la fin de loop. Si une opération SPI/radio/USB/servo bloque le CPU, le WDT redémarre le XIAO. Après reset, la première trame valide réactive le servo (position initiale supposée fermée comme auparavant). Une coupure électrique ou une chute durable de tension n'est pas corrigée par logiciel.
- Reprise de réception si DIO1 reste haut malgré une interruption manquée. RX continu réarmé après chaque paquet, erreurs radio suivies d'une réinitialisation après 5 s. Silence de 80 s : réinitialisation du SX1262 avant expiration de 150 s. Si le silence persiste, essais espacés d'au moins 30 s (80 s au démarrage sans aucun état). La dernière consigne est conservée lors d'une réinit radio, pas d'animation supplémentaire. Pas de reset périodique du XIAO.
- CDC facultatif : DTR et place disponible vérifiés, une ligne courte au maximum, pas d'attente de connexion USB. Diagnostics perdus si le tampon est plein. RESETREAS bit 1 = watchdog si encore présent après bootloader.
- Servo maintenu sous PWM à l'arrêt : ne pas relâcher sans vérifier que la porte tient seule. Course 90° inversée, 5 s dans les deux sens inchangées.

## Validation physique à effectuer

1. Flasher uniquement recepteur. Alimenter sur le bus 5 V / 2 A minimum, condensateur 470 µF près du servo. Ne pas alimenter simultanément par USB PC et alimentation externe.
2. Laisser 30 à 60 min immobile en position fermée, puis ouverte, vérifier la réponse à chaque action. Répéter les cycles et laisser une nuit.
3. Couper l'émetteur au moins 3 min : LED orange double flash toutes les 2 s, blanche éteinte. Rebrancher : retour à l'état courant dès trame valide (heartbeat 60 s si nécessaire). Répéter en position ouverte et fermée.
4. Pour isoler une cause électrique, répéter avec servo déconnecté (alimentation coupée avant déconnexion), puis mesurer 5 V et 3V3 pendant l'inactivité et les ACK LoRa, idéalement à l'oscilloscope. Une alimentation insuffisante ou un servo en butée peut causer des perturbations.
5. Les tests logiciels ne reproduisent pas un gel matériel réel. Le code n'est pas un dispositif de sécurité.
