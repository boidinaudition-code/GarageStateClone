# Installer ce projet dans un nouveau dépôt GitHub

Ce ZIP contient **directement** `platformio.ini`, `src/`, `docs/`, `.gitignore`, etc. Il n'y a pas de sous-dossier parent à déplacer.

## Méthode A — Interface GitHub (sans Git installé)

1. Télécharger et **décompresser** le ZIP sur ton ordinateur. GitHub ne décompresse pas automatiquement les fichiers ZIP envoyés.
2. Sur GitHub : **New repository** → nom conseillé `garage-miniature-lora`.
3. Créer le dépôt vide (ne pas initialiser avec un README si tu souhaites mettre celui de ce projet).
4. Dans le dépôt : **Add file → Upload files**.
5. Glisser **tous les fichiers et dossiers extraits**, dont les fichiers cachés `.gitignore` et `.editorconfig`.
6. Vérifier que `platformio.ini` est bien **à la racine du dépôt**, puis **Commit changes**.

## Méthode B — Terminal (recommandée)

Créer un dépôt vide sur GitHub, puis, depuis le dossier extrait :

```bash
git init
git add .
git commit -m "Initial prototype: XIAO nRF52840 garage status over LoRa"
git branch -M main
git remote add origin https://github.com/VOTRE_COMPTE/garage-miniature-lora.git
git push -u origin main
```

Remplacer `VOTRE_COMPTE` par ton compte GitHub et le nom du dépôt si nécessaire. Pour `git push`, GitHub demandera une authentification compatible (navigateur, gestionnaire d'identifiants, token ou SSH), **pas** ton mot de passe de compte.

## Ouvrir dans PlatformIO

Ouvrir le dossier du dépôt dans VS Code avec l'extension PlatformIO puis :

```bash
pio run -e emetteur
pio run -e recepteur
```

Flasher chaque kit **un par un**, antenne adaptée connectée :

```bash
pio run -e emetteur -t upload
pio run -e recepteur -t upload
```

Le firmware remplace le logiciel MeshCore/Meshtastic présent sur la carte. Lis le README avant le premier branchement.

## État de validation

Prototype logiciel : contrôles statiques effectués, mais **pas de compilation complète PlatformIO ni de test électronique réel** dans cet environnement. Des ajustements peuvent être nécessaires selon les versions installées.
