from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

# Paramètres de connexion
url = "http://localhost:8086"
token = "SO-wMqIzfS9wMn4Gyu94GKteCcaklwnSS1UOxZ_dRfo73r8A8OTA3-vEn6484fe3vOOSLDoS_0MI6tsRj9jvcQ=="
org = "pemesa"
bucket = "galaxy-watch-data"

# Connexion au client InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

import datetime

sdnn_values = [32.96, 37.36, 43.24]
rmssd_values = [27.96, 29.97, 31.94]

# Timestamp de départ
start_time = datetime.datetime(2025, 6, 2, 21, 0)

# Génération automatique
timestamps = [
    (start_time + datetime.timedelta(minutes=i)).isoformat() + "Z"
    for i in range(len(sdnn_values))
]


# Envoi des données
try:
    for t, sdnn, rmssd in zip(timestamps, sdnn_values, rmssd_values):
        point = (
            Point("hrv")
            .tag("user", "AS3")
            .field("sdnn", sdnn)
            .field("rmssd", rmssd)
            .time(t)
        )
        write_api.write(bucket=bucket, org=org, record=point)

    print("Données envoyées avec succès")

except Exception as e:
    print("Erreur lors de l'envoi des données :", e)
