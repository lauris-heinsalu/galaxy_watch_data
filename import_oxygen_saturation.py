import csv
import json
import os
import sys
from datetime import datetime

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# --- InfluxDB Configuration ---
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "your-token" # <--- UPDATE THIS
INFLUXDB_ORG = "your-org"     # <--- UPDATE THIS
INFLUXDB_BUCKET = "samsung_health"

def import_oxygen_saturation_data(data_directory):
    """
    Extracts oxygen saturation data from a specified directory and writes it to InfluxDB.
    """
    # --- File Paths ---
    csv_filename = 'com.samsung.health.oxygen_saturation.raw.csv'
    # Find the specific CSV file by walking the directory
    csv_file_path = None
    for root, _, files in os.walk(data_directory):
        for file in files:
            if file.startswith('com.samsung.health.oxygen_saturation.raw') and file.endswith('.csv'):
                csv_file_path = os.path.join(root, file)
                break
        if csv_file_path:
            break

    if not csv_file_path or not os.path.exists(csv_file_path):
        print(f"Error: Could not find the oxygen saturation CSV file in {data_directory}")
        return

    json_dir = os.path.join(data_directory, 'jsons/com.samsung.health.oxygen_saturation.raw')

    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        with open(csv_file_path, 'r') as csvfile:
            # Skip header lines until the actual header is found
            for i, line in enumerate(csvfile):
                if not line.strip().startswith('com.samsung') and not line.strip().startswith('#') and line.strip():
                    header_line_index = i
                    break
            else:
                print("Could not find header row in CSV.")
                return
            
            csvfile.seek(0)
            for _ in range(header_line_index):
                next(csvfile)

            reader = csv.DictReader(csvfile)
            for row in reader:
                datauuid = row.get('datauuid')
                deviceuuid = row.get('deviceuuid')
                time_offset = row.get('time_offset')
                json_filename = row.get('binning_data')

                if not all([datauuid, json_filename]):
                    continue

                # The JSON files are in subdirectories named after the first character of the datauuid
                json_path = os.path.join(json_dir, datauuid[0], json_filename)

                if os.path.exists(json_path):
                    with open(json_path, 'r') as jsonfile:
                        try:
                            json_data = json.load(jsonfile)
                            points = []
                            for item in json_data:
                                point = Point("oxygen_saturation") \
                                    .tag("deviceuuid", deviceuuid) \
                                    .tag("datauuid", datauuid) \
                                    .tag("time_offset", time_offset) \
                                    .field("channel", item['channel']) \
                                    .time(datetime.fromtimestamp(item['time'] / 1000))
                                points.append(point)

                            if points:
                                write_api.write(bucket=INFLUXDB_BUCKET, record=points)
                                print(f"Successfully wrote {len(points)} points from {json_filename} to InfluxDB.")

                        except json.JSONDecodeError:
                            print(f"Error decoding JSON from {json_filename}")
                else:
                    print(f"JSON file not found: {json_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 import_oxygen_saturation.py <path_to_data_subdirectory>")
        sys.exit(1)
    
    data_dir = sys.argv[1]
    if not os.path.isdir(data_dir):
        print(f"Error: Directory not found at {data_dir}")
        sys.exit(1)

    import_oxygen_saturation_data(data_dir)