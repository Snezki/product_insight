# Provides reusable connections to PostgreSQL and MongoDB
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from pymongo import MongoClient

load_dotenv()

# PostgreSQL credentials
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# MongoDB credentials
MONGO_PORT = os.getenv("MONGO_PORT")


# PostgreSQL connection
def get_postgres_engine():
    url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}"
    engine = create_engine(url)
    return engine


# MongoDB connection
def get_mongo_client():
    url = f"mongodb://localhost:{MONGO_PORT}"
    client = MongoClient(url)
    return client


# Return a MongoDB db obj
def get_mongo_db(db_name="product_insight"):
    client = get_mongo_client()
    db = client[db_name]
    return db
