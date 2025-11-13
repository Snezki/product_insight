from db_connection import get_postgres_engine, get_mongo_db
import pandas as pd
import os

events_file = "data/events.json"
if not os.path.exists(events_file):
    raise FileNotFoundError(f"{events_file} not found. Run simulate_events first")

df = pd.read_json(events_file)

# Insert events in postgres for structured analytics
engine = get_postgres_engine()

df.to_sql("events", engine, if_exists="replace", index=False)
print("Events saved into PostgreSQL")

# Insert events in MongoDB for raw/flexible storage
db = get_mongo_db()
db.events.insert_many(df.to_dict("records"))
print("Events saved into MongoDB")
