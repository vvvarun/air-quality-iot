import sqlite3

class AirQualityDatabase:
    def __init__(self, db_path):
        self.db_path = db_path

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS air_quality (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                location TEXT NOT NULL,
                temperature REAL,
                humidity REAL,
                air_raw INTEGER,
                category TEXT
            )
        """)

        conn.commit()
        conn.close()

    def save_record(self, record):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO air_quality 
            (timestamp, location, temperature, humidity, air_raw, category)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            record["timestamp"],
            record["location"],
            record["temperature"],
            record["humidity"],
            record["air_raw"],
            record["category"]
        ))

        conn.commit()
        conn.close()

    def get_total_records(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM air_quality")
        total = cursor.fetchone()[0]

        conn.close()
        return total