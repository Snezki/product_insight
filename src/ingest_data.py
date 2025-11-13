import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
MONGO_PORT = os.getenv("MONGO_PORT")

POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}"
MONGO_URL = f"mongodb://localhost:{MONGO_PORT}"

events_file = "data/events.json"
if not os.path.exists(events_file):
    raise FileNotFoundError(f"{events_file} not found. Run simulate_events first")

df = pd.read_json(events_file)

# Insert events in postgres for structured analytics
engine = create_engine(POSTGRES_URL)

df.to_sql("events", engine, if_exists="replace", index=False)
print("Events saved into PostgreSQL")

# Insert events in MongoDB for raw/flexible storage
client = MongoClient(MONGO_URL)

db = client.product_insight
db.events.insert_many(df.to_dict("records"))
print("Events saved into MongoDB")
