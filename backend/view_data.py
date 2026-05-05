import sqlite3

conn = sqlite3.connect("data/air_quality.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM air_quality ORDER BY id DESC LIMIT 10")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()