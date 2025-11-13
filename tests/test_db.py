import pytest
from src.db_connection import get_postgres_engine, get_mongo_db
import pandas as pd


def test_postgres_connection():
    engine = get_postgres_engine()
    df_pg = pd.read_sql("SELECT * FROM events", engine)
    assert len(df_pg) > 0, "No events found in PostgreSQL"
    print(f"PostgreSQL has {len(df_pg)} events")


def test_mongo_connection():
    db = get_mongo_db()
    count = db.events.count_documents({})
    assert count > 0, "No events found in MongoDB"
    print(f"MongoDB has {count} events")


if __name__ == "__main__":
    test_postgres_connection()
    test_mongo_connection()
