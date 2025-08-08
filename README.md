# Intégration des données Galaxy Watch dans un bucket InfluxDB

## Créer un environnement virtuel
```bash
python -m venv .venv
source .venv/bin/activate
```

## Installer les dépendances

```bash
pip install -r requirements.txt
```

## Exporter les données de la montre

Cf. le [Dictionnaire de données](data_dictionary.md).

- Exporter les données de la montre en utilisant l'app Samsung Health
- recopier les fichiers dans un sous-dossier du répertoire `samsung_watch_data`
- Vérifier la config du serveur dans le fichier `servers.py`
- Vérifier l'existence du bucket `watch_data`
- Exécuter le script

```bash
python3 import_all_data.py <path_to_data_subdirectory>
````


[Références](references.md)