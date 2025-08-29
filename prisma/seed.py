import os
import psycopg2
from datetime import datetime, timedelta

conn = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB', 'energy_db'),
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', 5432)
)
cur = conn.cursor()

# Create demo users and devices
cur.execute("INSERT INTO "user" (email, password, role) VALUES ('demo@user.com', 'hashed_pw', 'user') ON CONFLICT DO NOTHING;")
cur.execute("INSERT INTO device (name, userId) VALUES ('Living Room Plug', 1) ON CONFLICT DO NOTHING;")

# Insert demo telemetry
now = datetime.utcnow()
for i in range(7):
    cur.execute("INSERT INTO telemetry (timestamp, usage, deviceId) VALUES (%s, %s, %s)", (now - timedelta(days=i), 1.5 + i, 1))

conn.commit()
cur.close()
conn.close()
