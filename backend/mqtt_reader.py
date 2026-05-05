import json
import paho.mqtt.client as mqtt

from backend.config import load_config
from backend.db import AirQualityDatabase
from backend.logger import setup_logger
from backend.processor import AirQualityProcessor

config = load_config()
logger = setup_logger()

db = AirQualityDatabase(config["database"]["path"])
db.init_db()

processor = AirQualityProcessor(
    location=config["device"]["location"],
    good_threshold=config["processing"]["good_threshold"],
    moderate_threshold=config["processing"]["moderate_threshold"]
)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        logger.info("Connected to MQTT broker")
        client.subscribe(config["mqtt"]["topic"])
    else:
        print("Connection failed:", rc)
        logger.error(f"MQTT connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)

        record = processor.process(data)
        db.save_record(record)

        total = db.get_total_records()
        print(f"Record #{total}: {record}")
        logger.info(f"Saved record #{total}: {record}")

    except json.JSONDecodeError as e:
        print("Bad JSON skipped")
        logger.warning(f"Bad JSON skipped: {e}")

    except Exception as e:
        print("Error processing message:", e)
        logger.error(f"Error processing message: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(
    config["mqtt"]["broker"],
    config["mqtt"]["port"],
    60
)

client.loop_forever()