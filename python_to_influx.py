import os
import json
import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
from pathlib import Path

# ⚙Config InfluxDB
url = "http://localhost:8086"
token = "SO-wMqIzfS9wMn4Gyu94GKteCcaklwnSS1UOxZ_dRfo73r8A8OTA3-vEn6484fe3vOOSLDoS_0MI6tsRj9jvcQ=="
org = "pemesa"
bucket = "galaxy-watch-data"

# Dossier racine contenant les fichiers
data_dir = "C:\\Users\\lopez\\PycharmProjects\\galaxy_watch_data\\samsung_watch_data"


# Connexion InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)


# Fonction d’envoi
def write_point(measurement: str, fields: dict, timestamp: datetime):
    point = Point(measurement).time(timestamp, WritePrecision.NS)
    for key, value in fields.items():
        point.field(key, value)
    write_api.write(bucket=bucket, org=org, record=point)


# Parcours des fichiers
for root, dirs, files in os.walk(data_dir):
    for file in files:
        path = os.path.join(root, file)

        if file.endswith(".json"):
            with open(path, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print(f"Erreur JSON : {path}")
                    continue

                for entry in data:
                    if isinstance(entry, dict) and "start_time" in entry:
                        ts = pd.to_datetime(entry["start_time"], unit='ms')
                        fields = {
                            "heart_rate": entry.get("heart_rate"),
                            "heart_rate_max": entry.get("heart_rate_max"),
                            "heart_rate_min": entry.get("heart_rate_min"),
                        }
                        write_point("heart_rate", fields, ts)
                    else:
                        print(f"Entrée JSON ignorée (non conforme) dans {file} : {entry}")


        elif file.endswith(".csv"):
            try:
                df = pd.read_csv(path)
            except Exception as e:
                print(f"Erreur lecture CSV {path} : {e}")
                continue

            for _, row in df.iterrows():
                try:
                    ts_str = f"{row['date']} {row['time']}"
                    ts = pd.to_datetime(ts_str)
                    fields = {"heart_rate": float(row["heart_rate"])}
                    write_point("heart_rate", fields, ts)
                except Exception as e:
                    print(f"Erreur ligne CSV : {row} → {e}")

client.close()
print("Importation terminée.")
