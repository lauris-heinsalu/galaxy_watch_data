import csv
import json
import os
import glob
import sys
import logging
from datetime import datetime

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from servers import INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET

# Configuration du logging
def setup_logging():
    logger = logging.getLogger('samsung_health_import')
    logger.setLevel(logging.WARNING)
    
    # Handler pour la console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Handler pour le fichier
    file_handler = logging.FileHandler('samsung_health_import.log')
    file_handler.setLevel(logging.INFO)
    
    # Format du log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Ajout des handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Initialisation du logger
logger = setup_logging()


def get_measurement_name(filename):
    """Extracts the measurement name from the CSV filename."""
    parts = os.path.basename(filename).split('.')
    if len(parts) > 2:
        return ".".join(parts[:-2])
    return parts[0]

def process_field(points, point, key, value):
    """Processes a field for the InfluxDB point."""
    if key is None or value is None or value == '':
        return
    if key in ['mStartTime', 'start_time', 'end_time', 'timestamp', 'time']:
        date_value = datetime.fromtimestamp(int(value / 1000))
        point.field(key, date_value.isoformat())
    else:
        if not isinstance(value, list):
            try:
                point.field(key, float(value))
            except (ValueError, TypeError):
                point.field(key, value)
        else:
            # If the value is a list, one measurement for each value
            for record in value:
                sub_point = Point(point._name + "_" + key)
                sub_point.tag("deviceuuid", point._tags.get("deviceuuid", ""))
                sub_point.tag("datauuid", point._tags.get("datauuid", ""))
                sub_point.time(point._time)
                for sub_key, sub_value in record.items():
                    if sub_key is None or sub_value is None or sub_value == '':
                        continue
                    try:
                        sub_point.field(sub_key, float(sub_value))
                    except (ValueError, TypeError):
                        sub_point.field(sub_key, sub_value)
                points.append(sub_point)

def find_candidate_time_in_dict(item):
    """Finds a suitable time key in the item dictionary."""
    for key in ['mStartTime', 'start_time', 'create_time', 'update_time', 'end_time']:
        if key in item:
            return item[key]
    return None

def process_binned_data(csv_row_time, json_filename, write_api, measurement_name, csv_row, json_dir_root):
    """Processes data where details are in a separate JSON file."""
    datauuid = csv_row.get('datauuid')
    deviceuuid = csv_row.get('deviceuuid')
    #json_filename = csv_row.get('binning_data')

    if not all([datauuid, json_filename]):
        return

    json_dir = os.path.join(json_dir_root, measurement_name)
    json_path = os.path.join(json_dir, datauuid[0], json_filename)

    if os.path.exists(json_path):
        logger.info("Loading detailed data from {}".format(json_path))
        with open(json_path, 'r') as jsonfile:
            try:
                json_data = json.load(jsonfile)
                # Some json files are lists, some are dicts, we should handle both cases
                if not isinstance(json_data, list):
                     json_data = [json_data]  # Wrap in a list if it's a single dict
                points = []

                for item in json_data:
                    # remove the "com.samsung" prefix from the measurement name
                    point = Point(measurement_name.replace("com.samsung.", "") + "_binned")
                    if deviceuuid:
                        point.tag("deviceuuid", deviceuuid)
                    if datauuid:
                        point.tag("datauuid", datauuid)
                    timestamp = find_candidate_time_in_dict(item)
                    if timestamp is None:
                        logger.info(f"No suitable timestamp found in {json_filename} for {measurement_name}, using csv row time")
                        point.time(csv_row_time)
                    else:
                        try:
                            date_value = datetime.fromtimestamp(int(timestamp / 1000))
                            point.time(date_value, write_precision='ms')
                        except (ValueError, TypeError):
                            logger.warning(f"Invalid timestamp {timestamp} in {json_filename} for {measurement_name}")
                            continue

                    for key, value in item.items():
                        process_field(points, point, key, value)

                    points.append(point)
                
                if points:
                    logger.debug(f"Writing {len(points)} points for {measurement_name} from {json_filename}")
                    try:
                        write_api.write(bucket=INFLUXDB_BUCKET, record=points)
                    except Exception as e:
                        logger.critical(f"Error writing points for {measurement_name} from {json_filename}: {e}")
                else:
                    logger.error(f"No valid data found in {json_filename} for {measurement_name}")

            except json.JSONDecodeError:
                print(f"Error decoding JSON from {json_filename}")

def process_direct_data(write_api, measurement_name, csv_row):
    """Processes data contained directly within the CSV row."""
    point = Point(measurement_name.replace("com.samsung.", ""))
    
    timestamp = csv_row.get('start_time') or csv_row.get('create_time')
    if not timestamp:
        logger.warning(f"No timestamp found in {measurement_name} for row: {csv_row}")
        return None
    try:
        dt_object = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        point.time(dt_object)
    except ValueError:
        logger.error(f"Could not parse timestamp: {timestamp} in {measurement_name}")
        return None

    for key, value in csv_row.items():

        if key is None or value is None or value == '':
            continue
        if key in ['deviceuuid', 'datauuid', 'pkg_name', 'time_offset']:
            point.tag(key, value)
        #elif key in ['start_time', 'end_time', 'create_time', 'update_time']:
        #    # TODO : pourquoi ?
        #    continue
        else:
            try:
                point.field(key, float(value))
            except (ValueError, TypeError):
                point.field(key, value)
    #print(f"Writing point for {measurement_name} at {dt_object} with fields: {list(csv_row.keys())}")
    write_api.write(bucket=INFLUXDB_BUCKET, record=point)
    return point._time


def normalize_row(headers, row):
    """Normalizes the row by keeping only the last word of each header."""
    normalized_row = {}
    for header in headers:
        normalized_key = header.split('.')[-1]
        normalized_row[normalized_key] = row[header]
    return normalized_row

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
            # Définir ici la liste des measurement_names à traiter
            measurement_names_to_process = [
                'com.samsung.health.advanced_glycation_endproduct.raw',
                'com.samsung.health.floors_climbed',
                'com.samsung.health.movement',
                'com.samsung.health.respiratory_rate',
                'com.samsung.health.oxygen_saturation.raw',
                'com.samsung.health.respiratory_rate',
                'com.samsung.health.skin_temperature',
                'com.samsung.shealth.activity.day_summary', # TODO : bug sur extra_data
                'com.samsung.shealth.activity_level',
                'com.samsung.shealth.calories_burned.details',
                'com.samsung.shealth.exercise',
                'com.samsung.shealth.step_daily_trend'
                'com.samsung.shealth.stress',
                'com.samsung.shealth.tracker.floors_day_summary'
                "com.samsung.shealth.tracker.heart_rate",
                'com.samsung.shealth.tracker.oxygen_saturation'
                "com.samsung.shealth.tracker.pedometer_day_summary",
                "com.samsung.shealth.tracker.pedometer_step_count",
                'com.samsung.shealth.vitality_score',
            ]  # À adapter selon vos besoins
            #measurement_names_to_process = ["com.samsung.shealth.tracker.heart_rate"]  # À adapter selon vos besoins
            #measurement_names_to_process = ['com.samsung.shealth.tracker.floors_day_summary']
            if measurement_name not in measurement_names_to_process:
                logger.info(f"Skipping {measurement_name} (not in filter list)")
                continue

            logger.info(f"Processing {measurement_name} from {os.path.basename(csv_file)}...")
            
            try:
                with open(csv_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) < 2:
                        debug.error(f"Skipping empty file: {os.path.basename(csv_file)}")
                        continue

                    header_line_index = -1
                    for i, line in enumerate(lines):
                        if not line.strip().startswith('com.samsung') and not line.strip().startswith('#') and line.strip():
                            header_line_index = i + 1
                            break
                    
                    if header_line_index == -1:
                        logger.error(f"Could not find header in {os.path.basename(csv_file)}")
                        continue

                    reader = csv.DictReader(lines[header_line_index:])
                    headers = reader.fieldnames
                    # construct a dictionary from reader where keys are normalized keeping only the last word of header

                    for row in reader:
                        # Normalize the row to use the last word of each header
                        normalized_row = normalize_row(headers, row)
                        row_time = process_direct_data(write_api, measurement_name, normalized_row)
                        # Allow other names for binning data
                        #take the value of 'binning_data' or else 'raw_data'
                        binned_file = normalized_row.get('binning_data',
                            normalized_row.get('raw_data', # TODO pour health.exercise trois fichiers json
                            normalized_row.get('live_data_internal',
                            normalized_row.get('extra_data', None)))) # TODO com.samsung.shealth.activity.day_summary

                        if binned_file is not None and binned_file != '':
                            process_binned_data(row_time, binned_file, write_api, measurement_name, normalized_row, json_dir_root)

                logger.info(f"Finished processing {measurement_name}.")
            except Exception as e:
                print(f"An error occurred processing {os.path.basename(csv_file)}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 import_all_data.py <path_to_data_subdirectory>")

    data_dir = sys.argv[1] if len(sys.argv) > 1 else "samsung_watch_data/samsunghealth_pemesa01.champollion_20250604141272/"
    if not os.path.isdir(data_dir):
        logger.error(f"Directory not found at {data_dir}")
        sys.exit(1)

    import_all_data(data_dir)