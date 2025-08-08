
# Utilisation de InfluxDB CLI (exemples)

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

## Références
[Plot your health with Samsung Health and Pandas](https://www.technowizardry.net/2022/02/plot-your-health-with-samsung-health-and-pandas/)

[Analyzing Samsung Health Data](https://www.kaggle.com/code/kmader/analyzing-samsung-health-data/notebook)

[Sensor SDK](https://developer.samsung.com/health/sensor/overview.html)

[Samsung Health Connect](https://developer.android.com/health-and-fitness/guides/health-connect/develop/get-started)

[Exemple Heart Rate](https://developer.samsung.com/codelab/health/blood-oxygen-heart-rate.html)

[Référence des données](https://developer.samsung.com/health/android/data/guide/health-data-type.html)

[Wear OS Module](https://developer.android.com/health-and-fitness/guides/basic-fitness-app/integrate-wear-os)

[Wear OS sensors with counterpart](https://github.com/GeoTecINIT/WearOSSensors)