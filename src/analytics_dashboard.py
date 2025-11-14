import streamlit as st
import pandas as pd
from db_connection import get_postgres_engine, get_mongo_db

engine = get_postgres_engine()
df_pg = pd.read_sql("SELECT * FROM events", engine)

mongo_db = get_mongo_db()
df_mongo = pd.DataFrame(list(mongo_db.events.find()))

df_pg['timestamp'] = pd.to_datetime(df_pg['timestamp'])
df_mongo['timestamp'] = pd.to_datetime(df_mongo['timestamp'])

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

if success_filter == "True":
    filtered_df = filtered_df[filtered_df['succes'] == True]
elif success_filter == "False":
    filtered_df = filtered_df[filtered_df['succes'] == False]

# Events over time
st.header("Events over time")
filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'])
filtered_df['day_month'] = filtered_df['timestamp'].dt.strftime('%d %b')  # e.g. 03 Nov
filtered_df['date_only'] = filtered_df['timestamp'].dt.date  # we need it to sort the date

events_by_time = filtered_df.groupby(['date_only', 'day_month']).size().reset_index(name='count')
events_by_time = events_by_time.sort_values('date_only')

st.line_chart(events_by_time.set_index('day_month')['count'])


# Avg latency / feature
st.header("Average latency by feature")
average_latency_by_feature = filtered_df.groupby('feature')['latency_ms'].mean().reset_index()
st.bar_chart(average_latency_by_feature.set_index('feature')['latency_ms'])
st.write(average_latency_by_feature)

# Latency over time