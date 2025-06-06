from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime

# Paramètres de connexion
url = "http://localhost:8086"
token = " "
org = " "
bucket = " "

# Connexion au client InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Exemple de données
timestamps = [
    "2024-06-05T10:00:00Z",
    "2024-06-05T10:01:00Z",
    "2024-06-05T10:02:00Z",
    # ... etc.
]
sdnn_values = [32.96, 37.36, 43.24]
rmssd_values = [27.96, 29.97, 31.94]

# Envoi des données
for t, sdnn, rmssd in zip(timestamps, sdnn_values, rmssd_values):
    point = (
        Point("hrv")
        .tag("user", "user123")
        .field("sdnn", sdnn)
        .field("rmssd", rmssd)
        .time(t)
    )
    write_api.write(bucket=bucket, org=org, record=point)

print("Données envoyées avec succès")
