import requests
import random
import time
from datetime import datetime, timedelta

API = "http://localhost:8000"
EMAIL = "simuser@example.com"
PASSWORD = "simtestpass"

# Register user (ignore if already exists)
requests.post(f"{API}/auth/register", json={"email": EMAIL, "password": PASSWORD})
# Login
resp = requests.post(f"{API}/auth/login", data={"username": EMAIL, "password": PASSWORD})
token = resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Create 5 devices for the user (assume /device endpoint exists, else use direct DB or adjust as needed)
device_ids = []
for i in range(5):
    name = f"SimDevice-{i+1}"
    # If you have a device creation API, use it. Otherwise, set device_ids manually if seeded.
    resp = requests.post(f"{API}/device", json={"name": name}, headers=headers)
    if resp.status_code == 200:
        device_ids.append(resp.json()["id"])
    else:
        # fallback: assume device IDs 1-5
        device_ids = [1,2,3,4,5]
        break

start_of_today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

for t in range(0, 24*60*60, 60):  # one reading per minute for 24h
    ts = (start_of_today + timedelta(seconds=t)).isoformat() + "Z"
    for dev in device_ids:
        payload = {
            "deviceId": dev,
            "timestamp": ts,
            "usage": random.uniform(5, 250)
        }
        r = requests.post(f"{API}/telemetry/", json=payload, headers=headers)
        if r.status_code not in (200, 201):
            print(f"Failed for device {dev} at {ts}: {r.status_code} {r.text}")
    time.sleep(0.05)  # reduce if you want faster

print("Simulation complete.")
