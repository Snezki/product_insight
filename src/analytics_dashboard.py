import streamlit as st
import pandas as pd
from db_connection import get_postgres_engine, get_mongo_db

engine = get_postgres_engine()
df_pg = pd.read_sql("SELECT * FROM events", engine)

mongo_db = get_mongo_db()
df_mongo = pd.DataFrame(list(mongo_db.events.find()))

# PRE PROCESS
df_pg['timestamp'] = pd.to_datetime(df_pg['timestamp'])
df_mongo['timestamp'] = pd.to_datetime(df_mongo['timestamp'])

# Streamlit dashboard
st.title("Product Analytics Dashboard")

# Now filters
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start date", df_pg['timestamp'].min())
end_date = st.sidebar.date_input("End date", df_pg['timestamp'].max())
selected_feature = st.sidebar.multiselect("Feature", df_pg['feature'].unique(), default=df_pg['feature'].unique())
success_filter = st.sidebar.selectbox("Success", ["All", "True", "False"])

filtered_df = df_pg[
    (df_pg['timestamp'].dt.date >= start_date) &
    (df_pg['timestamp'].dt.date <= end_date) &
    (df_pg['feature'].isin(selected_feature))
]

if success_filter != "ALL":
    filtered_df = filtered_df[filtered_df['succes'] == (success_filter == "True")]

# Feature adoption (bar chart)
