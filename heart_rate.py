import csv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime

# Configuration
url = "http://localhost:8086"
token = "SO-wMqIzfS9wMn4Gyu94GKteCcaklwnSS1UOxZ_dRfo73r8A8OTA3-vEn6484fe3vOOSLDoS_0MI6tsRj9jvcQ=="
org = "pemesa"
bucket = "galaxy-watch-data"
csv_file_path = "C:\Users\lopez\PycharmProjects\galaxy_watch_data\samsung_watch_data\samsunghealth_pemesa01.champollion_20250604141272"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

with open(csv_file_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            # Exemple : timestamp ISO ou timestamp brut (à adapter selon ton fichier)
            ts = row.get("timestamp")  # ou "date", ou "_time", etc.
            value = float(row.get("heart_rate", 0))

            # Si timestamp est en millisecondes :
            if ts.isdigit():
                ts = datetime.datetime.fromtimestamp(int(ts) / 1000).isoformat() + "Z"

            point = (
                Point("heart_rate")
                .tag("source", "csv")
                .field("value", value)
                .time(ts)
            )
            write_api.write(bucket=bucket, org=org, record=point)
        except Exception as e:
            print(f"Erreur dans la ligne {row}: {e}")

print("Import CSV terminé.")
client.close()
