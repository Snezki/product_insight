from faker import Faker
import random
import json
import os

fake = Faker()
events = []

for _ in range(1000):
    event = {
        "timestamp": fake.date_time_this_month().isoformat(),
        "user_id": random.randint(1, 100),
        "event": random.choice(["user_login", "model_interference", "feature_click", "apî_error"]),
        "latency_ms": random.randint(25, 2000),
        "succes": random.choice([True, True, True, False]),
        "feature": random.choice(["summarise", "translate", "chat", "image_gen"])
    }
    events.append(event)

os.makedirs("data", exist_ok=True)

with open("data/events.json", "w") as f:
    json.dump(events, f, indent=2)

print("All fake events generated in data/events.json")