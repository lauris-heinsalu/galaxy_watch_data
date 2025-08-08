# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Setup

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Data Import
```bash
# Import all data from a Samsung Health export directory
python import_all_data.py samsung_watch_data/samsunghealth_remi.bastide_20250510201044/

# Or use the default directory
python import_all_data.py
```

### InfluxDB Configuration
The application connects to InfluxDB for time-series data storage. Configuration is in `servers.py`:
- **Local InfluxDB**: `http://localhost:8086`
- **Organization**: "ISIS - Université Champollion"
- **Bucket**: "watch_data"

## Code Architecture

### Main Components

#### Data Processing Pipeline (`import_all_data.py`)
Core ETL pipeline with three main functions:
- `process_direct_data()`: Handles CSV row data directly
- `process_binned_data()`: Processes detailed JSON time-series data
- `import_all_data()`: Main orchestrator for the entire pipeline

#### Data Flow
1. **CSV Processing**: Reads Samsung Health export CSV files
2. **JSON Processing**: Loads detailed time-series data from associated JSON files
3. **Data Transformation**: Normalizes field names, handles timestamps, converts data types
4. **InfluxDB Writing**: Stores processed data as time-series measurements

### Samsung Health Data Structure

#### File Organization
- **CSV Files**: Main data files with metadata and summary information
- **JSON Directory**: `jsons/` contains detailed time-series data
- **File Naming**: `jsons/{measurement_name}/{uuid_first_char}/{uuid}.{data_type}.json`

#### Data Types Processed
The pipeline handles 18 measurement types including:
- Heart rate tracking (`com.samsung.shealth.tracker.heart_rate`)
- Sleep analysis (`com.samsung.shealth.sleep`)
- Step counting (`com.samsung.shealth.tracker.pedometer_step_count`)
- Movement patterns (`com.samsung.health.movement`)
- Physiological metrics (oxygen saturation, respiratory rate, stress)

#### Field Normalization
- CSV headers use full Samsung package names (e.g., `com.samsung.shealth.tracker.heart_rate`)
- Fields are normalized by keeping only the last component (e.g., `heart_rate`)
- Timestamps are converted from milliseconds to datetime objects

### Key Functions

#### `normalize_row(headers, row)` - import_all_data.py:177
Simplifies Samsung's verbose field names by extracting the last component.

#### `process_field(points, point, key, value)` - import_all_data.py:49
Handles different data types and converts timestamps. Recursively processes nested arrays.

#### `find_candidate_time_in_dict(item)` - import_all_data.py:78
Searches for suitable timestamp fields in JSON data using priority order.

### Data Storage Strategy

#### InfluxDB Schema
- **Measurements**: Named after Samsung data types (without `com.samsung.` prefix)
- **Tags**: `deviceuuid`, `datauuid`, `pkg_name`, `time_offset`
- **Fields**: All other data converted to appropriate types (float, string, timestamp)
- **Binned Data**: Suffixed with `_binned` for detailed time-series data

#### Time Handling
- Primary timestamps: `start_time`, `create_time`, `end_time`
- JSON timestamps: `mStartTime`, `start_time`, `create_time`, `update_time`
- Conversion: Milliseconds to datetime objects with proper timezone handling

### Configuration Files

#### `servers.py`
Contains database connection settings and MQTT broker configuration (legacy).

#### `requirements.txt`
Jupyter ecosystem, data analysis libraries (pandas, matplotlib, seaborn), and InfluxDB client.

## Development Notes

### Error Handling
- Comprehensive logging system with file and console output
- Graceful handling of missing JSON files and invalid timestamps
- Validation of required fields (datauuid, deviceuuid, timestamps)

### Performance Considerations
- Synchronous InfluxDB writes for data integrity
- Batch processing of JSON arrays for efficient storage
- Selective measurement processing via filter list

### Common Issues
- Missing JSON files: Logged as info, processing continues
- Invalid timestamps: Logged as warnings, records skipped
- Empty CSV files: Detected and skipped automatically
- Unicode handling: UTF-8 encoding specified for CSV reading