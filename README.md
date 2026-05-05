# Air Quality Monitoring System

## Overview

This project is an end-to-end IoT-based Air Quality Monitoring System that collects environmental data using sensors, transmits it via MQTT, processes and stores it in a database, and visualizes it using an interactive dashboard.

The system supports both real-time monitoring and historical data analysis.

## System Architecture

```text
ESP32 and Sensors
      |
      v
WiFi Communication
      |
      v
MQTT Broker
      |
      v
Python Backend (Processing Layer)
      |
      v
SQLite Database (Storage Layer)
      |
      v
Streamlit Dashboard (Output Layer)
```

## Components Used

### Hardware

* ESP32 Development Board
* DHT22 Temperature & Humidity Sensor
* MQ135 Air Quality Sensor
* Breadboard & Jumper Wires

### Software

* Arduino IDE (ESP32 programming)
* Python 3
* Mosquitto MQTT Broker
* SQLite Database
* Streamlit (Dashboard)

## Project Structure

```text
air-quality-iot/
|-- backend/
|   |-- config.py
|   |-- db.py
|   |-- logger.py
|   |-- processor.py
|   |-- mqtt_reader.py
|   |-- check_records.py
|   `-- view_data.py
|-- config/
|   `-- config.json
|-- dashboard/
|   `-- app.py
|-- data/
|   `-- air_quality.db
|-- esp32/
|   |-- final_code/
|   |   `-- mqtt_final.ino
|   |-- sensor_test/
|   |   `-- sensor_test.ino
|   `-- wifi_test/
|       `-- wifi_test.ino
`-- README.md
```

## Features

* Real-time sensor data collection
* MQTT-based communication
* Data validation and error handling
* Storage of 10,000+ records
* Modular Python backend
* Interactive dashboard with live updates
* Configurable system via JSON file
* Logging for debugging and monitoring

## Data Processing

The backend performs:

* Validation of sensor data
* Categorization of air quality:
  * Good
  * Moderate
  * Unhealthy
* Timestamping of records
* Storage into SQLite database

## Database

* Type: SQLite
* File: `data/air_quality.db`
* Table: `air_quality`

Fields:

* id
* timestamp
* location
* temperature (C)
* humidity (%)
* air_raw (ADC value)
* category

## Dashboard (Streamlit)

Visualizations:

1. Air Quality Trend
   * Shows air quality changes over time
2. Temperature & Humidity Trend
   * Compares environmental conditions
3. Air Quality Category Distribution
   * Shows distribution of Good / Moderate / Unhealthy

Modes:

* Real-Time Mode
  * Uses latest 1000 records
  * Fast and responsive
* Full Data Analysis Mode
  * Uses all records (10,000+)
  * Suitable for deep analysis

## Real-Time Capability

The system supports real-time monitoring:

* ESP32 continuously sends data
* Python backend stores new records
* Dashboard auto-refreshes every few seconds

## How to Run

1. Start MQTT Broker

```bash
net start mosquitto
```

2. Run Backend

```bash
py -m backend.mqtt_reader
```

3. Run Dashboard

```bash
py -m streamlit run dashboard/app.py
```

4. Open Browser

```text
http://localhost:8501
```

## Testing

* Sensor validation handled (NaN checks)
* Error handling implemented in backend

## Screenshots

![Dashboard screenshot](Screenshot%202026-05-04%20174051.png)

![Dashboard screenshot](Screenshot%202026-05-04%20174230.png)

![Dashboard screenshot](Screenshot%202026-05-04%20174243.png)

## Conclusion

This project demonstrates a complete IoT pipeline integrating hardware, communication protocols, data engineering, and visualization, with support for both real-time monitoring and large-scale data analysis.
