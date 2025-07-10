import csv
import json
import os
import glob
import sys
from datetime import datetime

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# --- InfluxDB Configuration ---
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "your-token"  # <--- UPDATE THIS
INFLUXDB_ORG = "your-org"      # <--- UPDATE THIS
INFLUXDB_BUCKET = "samsung_health"

def get_measurement_name(filename):
    """Extracts the measurement name from the CSV filename."""
    parts = os.path.basename(filename).split('.')
    if len(parts) > 2:
        return ".".join(parts[:-2])
    return parts[0]

def process_binned_data(write_api, measurement_name, csv_row, json_dir_root):
    """Processes data where details are in a separate JSON file."""
    datauuid = csv_row.get('datauuid')
    deviceuuid = csv_row.get('deviceuuid')
    json_filename = csv_row.get('binning_data')

    if not all([datauuid, json_filename]):
        return

    json_dir = os.path.join(json_dir_root, measurement_name)
    json_path = os.path.join(json_dir, datauuid[0], json_filename)

    if os.path.exists(json_path):
        with open(json_path, 'r') as jsonfile:
            try:
                json_data = json.load(jsonfile)
                points = []
                for item in json_data:
                    point = Point(measurement_name)
                    if deviceuuid:
                        point.tag("deviceuuid", deviceuuid)
                    if datauuid:
                        point.tag("datauuid", datauuid)
                    
                    for key, value in item.items():
                        if key == 'time':
                            point.time(datetime.fromtimestamp(int(value) / 1000))
                        else:
                            try:
                                point.field(key, float(value))
                            except (ValueError, TypeError):
                                point.field(key, value)
                    points.append(point)
                
                if points:
                    write_api.write(bucket=INFLUXDB_BUCKET, record=points)

            except json.JSONDecodeError:
                print(f"Error decoding JSON from {json_filename}")

def process_direct_data(write_api, measurement_name, csv_row):
    """Processes data contained directly within the CSV row."""
    point = Point(measurement_name)
    
    timestamp = csv_row.get('start_time') or csv_row.get('create_time')
    if not timestamp:
        return

    try:
        dt_object = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        point.time(dt_object)
    except ValueError:
        print(f"Could not parse timestamp: {timestamp} in {measurement_name}")
        return

    for key, value in csv_row.items():
        if value is None or value == '':
            continue
        if key in ['deviceuuid', 'datauuid', 'pkg_name', 'time_offset']:
            point.tag(key, value)
        elif key in ['start_time', 'end_time', 'create_time', 'update_time']:
            continue
        else:
            try:
                point.field(key, float(value))
            except (ValueError, TypeError):
                point.field(key, value)

    write_api.write(bucket=INFLUXDB_BUCKET, record=point)

def import_all_data(data_directory):
    """
    Extracts data from all Samsung Health CSV files in a directory and writes it to InfluxDB.
    """
    json_dir_root = os.path.join(data_directory, 'jsons')
    
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        csv_files = glob.glob(os.path.join(data_directory, '*.csv'))

        for csv_file in csv_files:
            measurement_name = get_measurement_name(csv_file)
            print(f"Processing {measurement_name} from {os.path.basename(csv_file)}...")
            
            try:
                with open(csv_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) < 2:
                        print(f"Skipping empty file: {os.path.basename(csv_file)}")
                        continue

                    header_line_index = -1
                    for i, line in enumerate(lines):
                        if not line.strip().startswith('com.samsung') and not line.strip().startswith('#') and line.strip():
                            header_line_index = i
                            break
                    
                    if header_line_index == -1:
                        print(f"Could not find header in {os.path.basename(csv_file)}")
                        continue

                    reader = csv.DictReader(lines[header_line_index:])
                    headers = reader.fieldnames

                    for row in reader:
                        if 'binning_data' in headers and row.get('binning_data'):
                            process_binned_data(write_api, measurement_name, row, json_dir_root)
                        else:
                            process_direct_data(write_api, measurement_name, row)
                print(f"Finished processing {measurement_name}.")
            except Exception as e:
                print(f"An error occurred processing {os.path.basename(csv_file)}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 import_all_data.py <path_to_data_subdirectory>")
        sys.exit(1)

    data_dir = sys.argv[1]
    if not os.path.isdir(data_dir):
        print(f"Error: Directory not found at {data_dir}")
        sys.exit(1)

    import_all_data(data_dir)