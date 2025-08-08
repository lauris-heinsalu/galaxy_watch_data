# Créer un environnement virtuel
```bash
python -m venv .venv
source .venv/bin/activate
```

# Installer les dépendances

```bash
pip install -r requirements.txt
```

# Exporter les données de la montre
- Exporter les données de la montre en utilisant l'app Samsung Health
- recopier les fichiers dans un sous-dossier du répertoire `samsung_watch_data`
- Véridier la config du serveur dans le fichier `servers.py`
- Exécuter le script

```bash
python3 import_all_data.py <path_to_data_subdirectory>
````

# Utilisation de InfluxDB CLI(exemples

## Créér une config pour InfluxDB CLI (exemple)

```bash
influx config create --config-name localV2 --host-url http://localhost:8086 -org "ISIS - Université Champollion" -token "CIZXVSzp12IPM_-uiZGfF6qdjRE2nDkZLWw20pdbhVAMca1Em-4zA3OwkftLhZvsa7tEwag4_N7_Zs0Y-o0v_Q=="
influx config list
influx config use localV2
```

## Lister les buckets

```bash
influx bucket list
```

## Backup d'un bucket en format line protocol (exemple)

```bash
influxd inspect export-lp --bucket-id 9fb9f425a8a731e0 --engine-path /usr/local/var/lib/influxdb2/engine --output-path test3.lp
```
> [!NOTE]
> --engine-path est le chemin vers le dossier de stockage d'InfluxDB, par défaut c'est `/usr/local/var/lib/influxdb2/engine` sur macOS et Linux.
> autre possibilité : `~/.influxdbv2/engine`



[Références](references.md)