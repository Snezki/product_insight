from sqlalchemy import create_engine
import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# First we check that the data is saved in PostgreSQL
engine = create_engine(f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")
df_pg = pd.read_sql("SELECT * FROM events", engine)
print("Postgres rows:", len(df_pg))

# Then we do the same for MongoDB
client = MongoClient(f"mongodb://localhost:{os.getenv('MONGO_PORT')}")
db = client.product_insight
count_mongo = db.events.count_documents({})
print("MongoDB documents:", count_mongo)
