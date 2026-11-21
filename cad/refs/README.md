# Modèles STEP utilisés par la CAO V2

Les quatre STEP sont fournis par l'utilisateur dans des archives ZIP. La géométrie a été inspectée, placée et contrôlée dans le générateur `../generate_cad.py`.

**Fichiers d'entrée requis :** `cad/refs/servo.step`, `cad/refs/xiao.step`, `cad/refs/wio.step`, `cad/refs/transistor.step`. Les STEP binaires complets se trouvent dans l'**archive CAO V2 téléchargeable dans la conversation**. La connexion GitHub ne sait pas transférer directement les gros fichiers de l'environnement local ; ce commit apporte le générateur, le manifeste, les mesures et les contrôles, mais **pas encore les quatre STEP originaux dans GitHub**.

Pour les reconstituer à partir des archives ZIP d'origine :

```bash
cd cad
python import_vendor_archives.py dossier_des_4_zips
python generate_cad.py
```

Le manifeste `manifest.json` contient les noms de fichiers originaux, les tailles et les SHA256 à contrôler. Les STEP fournis sont **des références non imprimables**, qui ne remplacent pas un contrôle au pied à coulisse des composants physiques. **Vérifier les droits de redistribution du modèle tiers avant de publier les STEP bruts dans un dépôt public.**
