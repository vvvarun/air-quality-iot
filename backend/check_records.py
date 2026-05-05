from backend.config import load_config
from backend.db import AirQualityDatabase

config = load_config()

db = AirQualityDatabase(config["database"]["path"])
print("Total records:", db.get_total_records())