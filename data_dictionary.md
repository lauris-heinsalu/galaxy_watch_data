# Samsung Galaxy Watch Data Dictionary

## Table of Contents

1. [Overview](#overview)
2. [Data Structure](#data-structure)
   - [File Organization](#file-organization)
   - [Field Reference Types](#field-reference-types)
3. [Common Field Types](#common-field-types)
   - [Timestamp Fields](#timestamp-fields)
   - [Identifier Fields](#identifier-fields)
   - [Common Fields](#common-fields)
4. [Measurement Types](#measurement-types)
   - [1. Heart Rate Monitoring](#1-heart-rate-monitoring)
     - [com.samsung.shealth.tracker.heart_rate](#comsamsungshealthtrackerheart_rate)
   - [2. Heart Rate Variability (HRV)](#2-heart-rate-variability-hrv)
     - [com.samsung.health.hrv](#comsamsunghealthhrv)
   - [3. Sleep Monitoring](#3-sleep-monitoring)
     - [com.samsung.shealth.sleep](#comsamsungshealthsleep)
     - [com.samsung.health.sleep_stage](#comsamsunghealthsleep_stage)
     - [com.samsung.shealth.sleep_snoring](#comsamsungshealthsleep_snoring)
   - [4. Physical Activity Tracking](#4-physical-activity-tracking)
     - [com.samsung.shealth.tracker.pedometer_step_count](#comsamsungshealthtrackerpedometer_step_count)
     - [com.samsung.shealth.activity.day_summary](#comsamsungshealthactivityday_summary)
   - [5. Exercise Tracking](#5-exercise-tracking)
     - [com.samsung.shealth.exercise](#comsamsungshealthexercise)
   - [6. Stress Monitoring](#6-stress-monitoring)
     - [com.samsung.shealth.stress](#comsamsungshealthstress)
   - [7. Advanced Health Metrics](#7-advanced-health-metrics)
     - [com.samsung.health.oxygen_saturation.raw](#comsamsunghealthoxygen_saturationraw)
     - [com.samsung.health.skin_temperature](#comsamsunghealthskin_temperature)
     - [com.samsung.health.respiratory_rate](#comsamsunghealthrespiratory_rate)
   - [8. Movement and Activity Detection](#8-movement-and-activity-detection)
     - [com.samsung.health.movement](#comsamsunghealthmovement)
     - [com.samsung.health.floors_climbed](#comsamsunghealthfloors_climbed)
   - [9. Calories and Metabolism](#9-calories-and-metabolism)
     - [com.samsung.shealth.calories_burned.details](#comsamsungshealthcalories_burneddetails)
   - [10. Device and Configuration Data](#10-device-and-configuration-data)
     - [com.samsung.health.device_profile](#comsamsunghealthdevice_profile)
     - [com.samsung.health.user_profile](#comsamsunghealthuser_profile)
   - [11. Wellness and Scoring](#11-wellness-and-scoring)
     - [com.samsung.shealth.vitality_score](#comsamsungshealthvitality_score)
     - [com.samsung.health.advanced_glycation_endproduct](#comsamsunghealthadvanced_glycation_endproduct)
   - [12. Food and Nutrition](#12-food-and-nutrition)
     - [com.samsung.health.food_info](#comsamsunghealthfood_info)
   - [13. Women's Health](#13-womens-health)
     - [com.samsung.shealth.cycle.daily_temperature.raw](#comsamsungshealthcycledaily_temperatureraw)
5. [Data Quality and Validation](#data-quality-and-validation)
   - [Missing Data Patterns](#missing-data-patterns)
   - [Data Validation Rules](#data-validation-rules)
   - [File Naming Conventions](#file-naming-conventions)
6. [Usage Guidelines](#usage-guidelines)
   - [Data Processing](#data-processing)
   - [Analysis Considerations](#analysis-considerations)
   - [Common Use Cases](#common-use-cases)
7. [Version Information](#version-information)

## Overview

This comprehensive data dictionary documents all measurements, fields, and data structures found in Samsung Galaxy Watch data exports. The data is organized into CSV files with associated JSON files containing detailed time-series data and metadata.

## Data Structure

### File Organization
- **CSV Files**: Primary data files with summary information and metadata
- **JSON Files**: Detailed time-series data referenced by CSV files via UUID
- **Directory Structure**: `jsons/{measurement_type}/{uuid_first_char}/{uuid}.{data_type}.json`

### Field Reference Types
- **raw_data**: Raw sensor readings at original sampling rate
- **binning_data**: Time-aggregated sensor data with statistical summaries
- **extra_data**: Additional metadata and context information
- **live_data**: Real-time data streams during activities
- **sensing_status**: Sensor configuration and status information
- **level_boundary**: Threshold definitions for scores/levels

## Common Field Types

### Timestamp Fields
- **Format**: `YYYY-MM-DD HH:MM:SS.sss`
- **Precision**: Milliseconds
- **Example**: `2024-07-03 08:50:58.525`
- **JSON Format**: Unix timestamp in milliseconds
- **Example**: `1720017355119`

### Identifier Fields
- **deviceuuid**: 10-character alphanumeric string (e.g., `ooOmDJ1LSk`)
- **datauuid**: Standard UUID format (e.g., `852fd3e2-4927-4e46-8d1f-d307a8c32bfa`)
- **pkg_name**: Package identifier (typically `com.sec.android.app.shealth`)

### Common Fields
- **start_time**: Measurement start timestamp
- **end_time**: Measurement end timestamp
- **create_time**: Record creation timestamp
- **update_time**: Record update timestamp
- **time_offset**: Timezone offset (e.g., `UTC+0200`)

## Measurement Types

### 1. Heart Rate Monitoring

#### com.samsung.shealth.tracker.heart_rate
**Purpose**: Continuous heart rate monitoring from wearable device

**CSV Fields**:
- `heart_rate` (FLOAT): Heart rate in beats per minute
  - **Range**: 52.0 - 126.0 BPM
  - **Typical**: 57.0 - 116.0 BPM
- `heart_beat_count` (INTEGER): Number of heartbeats in interval
- `start_time` (TIMESTAMP): Measurement start time
- `end_time` (TIMESTAMP): Measurement end time
- `deviceuuid` (STRING): Device identifier
- `datauuid` (STRING): Data record identifier
- `pkg_name` (STRING): Package name
- `tag_id` (INTEGER): Measurement tag identifier
- `time_offset` (STRING): Timezone offset

**JSON Reference** (binning_data.json):
```json
[
  {
    "heart_rate": 68.5,
    "heart_rate_max": 72.0,
    "heart_rate_min": 65.0,
    "start_time": 1720017355119,
    "end_time": 1720017415119
  }
]
```

### 2. Heart Rate Variability (HRV)

#### com.samsung.health.hrv
**Purpose**: Heart rate variability analysis for stress and wellness monitoring

**CSV Fields**:
- `start_time` (TIMESTAMP): Analysis period start
- `end_time` (TIMESTAMP): Analysis period end
- `deviceuuid` (STRING): Device identifier
- `datauuid` (STRING): Data record identifier
- `binning_data` (STRING): Reference to detailed JSON data
- `time_offset` (STRING): Timezone offset

**JSON Reference** (binning_data.json):
```json
[
  {
    "start_time": 1720017355119,
    "end_time": 1720017715119,
    "sdnn": 35.90,
    "rmssd": 31.21
  }
]
```

**HRV Metrics**:
- `sdnn` (FLOAT): Standard deviation of NN intervals (20-100ms)
- `rmssd` (FLOAT): Root mean square of successive differences (20-80ms)

### 3. Sleep Monitoring

#### com.samsung.shealth.sleep
**Purpose**: Comprehensive sleep analysis and quality assessment

**CSV Fields**:
- `start_time` (TIMESTAMP): Sleep start time
- `end_time` (TIMESTAMP): Sleep end time
- `sleep_score` (FLOAT): Overall sleep quality score (0-100)
- `efficiency` (FLOAT): Sleep efficiency percentage (0-100)
- `sleep_duration` (INTEGER): Total sleep duration in minutes
- `total_light_duration` (INTEGER): Light sleep duration in minutes
- `total_deep_duration` (INTEGER): Deep sleep duration in minutes
- `total_rem_duration` (INTEGER): REM sleep duration in minutes
- `total_awake_duration` (INTEGER): Awake time during sleep in minutes
- `factor_01` through `factor_10` (INTEGER): Sleep quality factors (0-68)
- `extra_data` (STRING): Reference to additional sleep data

**JSON Reference** (extra_data.json):
```json
{
  "sleep_result_type": "STAGE"
}
```

#### com.samsung.health.sleep_stage
**Purpose**: Detailed sleep stage classification

**CSV Fields**:
- `start_time` (TIMESTAMP): Stage start time
- `end_time` (TIMESTAMP): Stage end time
- `sleep_id` (STRING): Associated sleep session ID
- `stage` (INTEGER): Sleep stage code
- `time_offset` (STRING): Timezone offset

**Sleep Stage Codes**:
- `40001`: Light sleep
- `40002`: Deep sleep
- `40003`: REM sleep
- `40004`: Awake

#### com.samsung.shealth.sleep_snoring
**Purpose**: Snoring detection and analysis

**CSV Fields**:
- `start_time` (TIMESTAMP): Snoring event start
- `end_time` (TIMESTAMP): Snoring event end
- `duration` (INTEGER): Snoring duration in milliseconds

### 4. Physical Activity Tracking

#### com.samsung.shealth.tracker.pedometer_step_count
**Purpose**: Step counting and movement analysis

**CSV Fields**:
- `count` (INTEGER): Step count for interval (0-6022)
- `distance` (FLOAT): Distance covered in meters (0.0-42.79)
- `speed` (FLOAT): Average speed in m/s (0.93-1.69)
- `calorie` (FLOAT): Calories burned (0.43-2.46)
- `run_step` (INTEGER): Running steps
- `walk_step` (INTEGER): Walking steps
- `duration` (INTEGER): Duration in milliseconds
- `start_time` (TIMESTAMP): Measurement start
- `end_time` (TIMESTAMP): Measurement end

#### com.samsung.shealth.activity.day_summary
**Purpose**: Daily activity aggregation and goal tracking

**CSV Fields**:
- `step_count` (INTEGER): Total daily steps
- `distance` (FLOAT): Total distance in meters
- `calorie` (FLOAT): Total calories burned
- `active_time` (INTEGER): Active time in milliseconds
- `exercise_time` (INTEGER): Exercise time in milliseconds
- `extra_data` (STRING): Reference to detailed activity data

**JSON Reference** (extra_data.json):
```json
{
  "mAdaptiveGoal": 8000,
  "mIsGoalAchieved": true,
  "mIsMostActiveAchieved": false,
  "mMostActiveMinutes": 45,
  "mStreakDayCount": 3,
  "version": 1
}
```

### 5. Exercise Tracking

#### com.samsung.shealth.exercise
**Purpose**: Detailed exercise session tracking

**CSV Fields**:
- `exercise_type` (INTEGER): Exercise type code
- `start_time` (TIMESTAMP): Exercise start time
- `end_time` (TIMESTAMP): Exercise end time
- `duration` (INTEGER): Exercise duration in milliseconds
- `distance` (FLOAT): Distance covered (0.68-3.64 km)
- `calorie` (FLOAT): Calories burned (57.0-294.6 kcal)
- `max_speed` (FLOAT): Maximum speed achieved
- `mean_speed` (FLOAT): Average speed (0.73-1.49 m/s)
- `max_heart_rate` (FLOAT): Maximum heart rate during exercise
- `mean_heart_rate` (FLOAT): Average heart rate during exercise
- `live_data` (STRING): Reference to real-time exercise data

**Exercise Type Codes**:
- `1001`: Walking
- `0`: Other activities

**JSON Reference** (live_data.json):
```json
[
  {
    "cadence": 45.5,
    "speed": 1.2,
    "start_time": 1720017355119
  },
  {
    "heart_rate": 85.0,
    "start_time": 1720017356119
  }
]
```

### 6. Stress Monitoring

#### com.samsung.shealth.stress
**Purpose**: Stress level monitoring and analysis

**CSV Fields**:
- `start_time` (TIMESTAMP): Measurement start
- `end_time` (TIMESTAMP): Measurement end
- `score` (FLOAT): Primary stress score (0.0-6.0)
- `max` (FLOAT): Maximum stress level (16.0-93.0)
- `min` (FLOAT): Minimum stress level (typically 0.0)
- `binning_data` (STRING): Reference to detailed stress data
- `tag_id` (INTEGER): Measurement tag

**JSON Reference** (binning_data.json):
```json
[
  {
    "score": 25,
    "score_max": 30,
    "score_min": 20,
    "flag": 1,
    "level": 2,
    "start_time": 1720017355119,
    "end_time": 1720017415119
  }
]
```

**Stress Levels**:
- `1`: Low stress
- `2`: Moderate stress
- `3`: High stress
- `4`: Very high stress

### 7. Advanced Health Metrics

#### com.samsung.health.oxygen_saturation.raw
**Purpose**: Blood oxygen saturation monitoring

**CSV Fields**:
- `start_time` (TIMESTAMP): Measurement start
- `end_time` (TIMESTAMP): Measurement end
- `binning_data` (STRING): Reference to raw SpO2 data
- `is_integrated` (INTEGER): Integration flag (0 or 1)
- `time_offset` (STRING): Timezone offset

**JSON Reference** (binning_data.json):
```json
[
  {
    "time": 1720017355119,
    "channel": 2.6469862E-23
  }
]
```

#### com.samsung.health.skin_temperature
**Purpose**: Continuous skin temperature monitoring

**CSV Fields**:
- `start_time` (TIMESTAMP): Measurement start
- `end_time` (TIMESTAMP): Measurement end
- `temperature` (FLOAT): Skin temperature in Celsius
- `baseline` (FLOAT): Baseline temperature
- `stat_sum` (FLOAT): Statistical sum
- `stat_count` (INTEGER): Statistical count
- `stat_min` (FLOAT): Minimum temperature
- `stat_max` (FLOAT): Maximum temperature
- `binning_data` (STRING): Reference to detailed temperature data

#### com.samsung.health.respiratory_rate
**Purpose**: Respiratory rate measurement

**CSV Fields**:
- `start_time` (TIMESTAMP): Measurement start
- `end_time` (TIMESTAMP): Measurement end
- `average` (FLOAT): Average respiratory rate
- `lower_limit` (FLOAT): Lower confidence limit
- `upper_limit` (FLOAT): Upper confidence limit
- `binning_data` (STRING): Reference to detailed respiratory data

### 8. Movement and Activity Detection

#### com.samsung.health.movement
**Purpose**: Movement and activity pattern detection

**CSV Fields**:
- `start_time` (TIMESTAMP): Movement period start
- `end_time` (TIMESTAMP): Movement period end
- `binning_data` (STRING): Reference to movement data
- `time_offset` (STRING): Timezone offset

**JSON Reference** (binning_data.json):
```json
[
  {
    "start_time": 1720017355119,
    "end_time": 1720017415119,
    "activity_level": 1.07192995E-4
  }
]
```

#### com.samsung.health.floors_climbed
**Purpose**: Floor climbing activity tracking

**CSV Fields**:
- `start_time` (TIMESTAMP): Climbing period start
- `end_time` (TIMESTAMP): Climbing period end
- `floor` (FLOAT): Number of floors climbed
- `raw_data` (STRING): Reference to raw climbing data
- `time_offset` (STRING): Timezone offset

**JSON Reference** (raw_data.json):
```json
[
  {
    "end_time": 1720017355119,
    "floor": 1.0
  }
]
```

### 9. Calories and Metabolism

#### com.samsung.shealth.calories_burned.details
**Purpose**: Detailed calorie expenditure analysis

**CSV Fields**:
- `start_time` (TIMESTAMP): Measurement start
- `end_time` (TIMESTAMP): Measurement end
- `active_calorie` (FLOAT): Active calories burned
- `rest_calorie` (FLOAT): Resting calories burned
- `exercise_calorie` (FLOAT): Exercise calories burned
- `extra_data` (STRING): Reference to additional calorie data

**JSON Reference** (extra_data.json):
```json
{
  "activityLevel": 2,
  "age": 35,
  "gender": "M",
  "height": 175.5,
  "stepCount": 8500,
  "weight": 72.3
}
```

### 10. Device and Configuration Data

#### com.samsung.health.device_profile
**Purpose**: Device capabilities and configuration

**CSV Fields**:
- `manufacturer` (STRING): Device manufacturer
- `model` (STRING): Device model
- `device_type` (INTEGER): Device type code
- `capability` (STRING): Reference to device capabilities
- `connectivity_type` (INTEGER): Connectivity type

**JSON Reference** (capability.json):
```json
{
  "supported_features": [...],
  "sensor_capabilities": {...},
  "sync_protocols": [...]
}
```

#### com.samsung.health.user_profile
**Purpose**: User profile and preferences

**CSV Fields**:
- `key` (STRING): Profile key
- `text_value` (STRING): Text value
- `int_value` (INTEGER): Integer value
- `float_value` (FLOAT): Float value
- `double_value` (DOUBLE): Double precision value
- `blob_value` (BLOB): Binary data value

### 11. Wellness and Scoring

#### com.samsung.shealth.vitality_score
**Purpose**: Overall vitality and wellness assessment

**CSV Fields**:
- Various vitality metrics and composite scores
- Wellness indicators and trend analysis

#### com.samsung.health.advanced_glycation_endproduct
**Purpose**: Advanced glycation end-product health scoring

**CSV Fields**:
- `measurement_result` (INTEGER): AGE measurement result
- `percent` (FLOAT): Percentage score
- `score` (INTEGER): Overall AGE score
- `level_boundary` (STRING): Reference to level definitions

### 12. Food and Nutrition

#### com.samsung.health.food_info
**Purpose**: Food database and nutritional information

**CSV Fields**:
- `name` (STRING): Food name
- `calorie` (FLOAT): Calories per serving
- `protein` (FLOAT): Protein content in grams
- `carbohydrate` (FLOAT): Carbohydrate content in grams
- `total_fat` (FLOAT): Total fat content in grams
- Additional vitamin and mineral content fields

### 13. Women's Health

#### com.samsung.shealth.cycle.daily_temperature.raw
**Purpose**: Menstrual cycle temperature tracking

**CSV Fields**:
- `start_time` (TIMESTAMP): Measurement start
- `end_time` (TIMESTAMP): Measurement end
- `temperature` (STRING): Reference to temperature data
- `hr_rri` (STRING): Reference to heart rate interval data

## Data Quality and Validation

### Missing Data Patterns
- **Empty Strings**: Most null values represented as empty strings
- **Default Values**: `-1` often represents null for integer fields
- **Boolean Representation**: `0` (false) and `1` (true) as integers

### Data Validation Rules
- **Timestamps**: Must be valid ISO 8601 format with timezone
- **UUIDs**: Must follow standard UUID format
- **Numeric Ranges**: Values should fall within documented ranges
- **Required Fields**: `start_time`, `deviceuuid`, `datauuid` are typically required

### File Naming Conventions
- **CSV Files**: `{measurement_type}.{export_date}.csv`
- **JSON Files**: `{uuid}.{data_type}.json`
- **Directory Structure**: UUID-based hierarchical organization

## Usage Guidelines

### Data Processing
1. Parse CSV files for summary data and references
2. Follow JSON references for detailed time-series data
3. Handle missing data gracefully
4. Validate data types and ranges
5. Consider timezone offsets for timestamp processing

### Analysis Considerations
- **Temporal Resolution**: Varies by measurement type
- **Data Volume**: JSON files can be very large (especially raw sensor data)
- **Completeness**: Not all measurements available for all users
- **Quality Indicators**: Use flags and statistical measures when available

### Common Use Cases
- **Health Monitoring**: Long-term trend analysis
- **Research**: Population health studies
- **Fitness Tracking**: Activity and exercise analysis
- **Sleep Studies**: Sleep pattern and quality research
- **Wellness Programs**: Comprehensive health assessment

## Version Information

This data dictionary is based on Samsung Galaxy Watch exports from 2024-2025, covering multiple device models and software versions. Field availability may vary based on device capabilities and software versions.

---

*Last Updated: July 2025*
*Data Sources: Samsung Galaxy Watch6/7, Samsung Health App Exports*