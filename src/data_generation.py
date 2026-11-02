import numpy as np
import pandas as pd
from pathlib import Path

rng = np.random.default_rng(42)
zones = ["Zone A", "Zone B", "Zone C", "Zone D", "Zone E", "Zone F"]
rows = []

for i in range(2400):
    zone = rng.choice(zones)
    hour = i % 24
    base_flow = rng.uniform(40, 120)
    base_pressure = rng.uniform(3.5, 6.5)
    consumption = base_flow * rng.uniform(0.65, 0.95)
    leak = rng.random() < 0.22

    if leak:
        flow = base_flow + rng.uniform(8, 35)
        pressure = base_pressure - rng.uniform(0.4, 2.0)
        night_flow = flow * rng.uniform(0.45, 0.8)
        leak_rate = max(2, flow - consumption + rng.uniform(2, 15))
    else:
        flow = base_flow + rng.normal(0, 4)
        pressure = base_pressure + rng.normal(0, 0.25)
        night_flow = max(5, flow * rng.uniform(0.08, 0.28))
        leak_rate = max(0, rng.normal(1.2, 1.0))

    rows.append({
        "timestamp_index": i,
        "hour": hour,
        "zone": zone,
        "flow_m3h": round(max(1, flow), 2),
        "pressure_bar": round(max(0.1, pressure), 2),
        "consumption_m3h": round(max(1, consumption), 2),
        "night_flow_m3h": round(night_flow, 2),
        "leak_rate_m3h": round(leak_rate, 2),
        "leak": int(leak)
    })

df = pd.DataFrame(rows)
Path("data").mkdir(exist_ok=True)
df.to_csv("data/water_sensor_data.csv", index=False)
print("Created data/water_sensor_data.csv with", len(df), "rows")
