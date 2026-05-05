from datetime import datetime
import math

class AirQualityProcessor:
    def __init__(self, location, good_threshold, moderate_threshold):
        self.location = location
        self.good_threshold = good_threshold
        self.moderate_threshold = moderate_threshold

    def get_category(self, air_value):
        if air_value < self.good_threshold:
            return "Good"
        elif air_value < self.moderate_threshold:
            return "Moderate"
        else:
            return "Unhealthy"

    def process(self, data):
        temp = float(data["temp"])
        hum = float(data["hum"])
        air = int(data["air"])

        if math.isnan(temp) or math.isnan(hum):
            raise ValueError("Temperature or humidity is NaN")

        if air < 0:
            raise ValueError("Air value cannot be negative")

        return {
            "timestamp": datetime.now().isoformat(),
            "location": self.location,
            "temperature": temp,
            "humidity": hum,
            "air_raw": air,
            "category": self.get_category(air)
        }