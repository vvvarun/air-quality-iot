import sqlite3
import time

import pandas as pd
import streamlit as st

DB_PATH = "data/air_quality.db"

st.set_page_config(
    page_title="Air Quality Monitoring Dashboard",
    layout="wide"
)

st.title("Air Quality Monitoring System")

mode = st.radio(
    "Select Dashboard Mode",
    ["Real-Time (Fast)", "Full Data Analysis"],
    horizontal=True
)

refresh = st.checkbox(
    "Enable live refresh",
    value=True if mode == "Real-Time (Fast)" else False
)

conn = sqlite3.connect(DB_PATH)

total_records = pd.read_sql_query(
    "SELECT COUNT(*) AS total FROM air_quality",
    conn
)["total"][0]

if mode == "Real-Time (Fast)":
    query = """
        SELECT *
        FROM air_quality
        ORDER BY id DESC
        LIMIT 1000
    """
else:
    query = """
        SELECT *
        FROM air_quality
        ORDER BY id ASC
    """

df = pd.read_sql_query(query, conn)
conn.close()

df["timestamp"] = pd.to_datetime(df["timestamp"])

if mode == "Real-Time (Fast)":
    df = df.sort_values("timestamp")
else:
    df = df.sort_values("timestamp")

latest = df.iloc[-1]

st.caption(f"Records loaded in dashboard: {len(df):,}")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Records", f"{total_records:,}")
col2.metric("Temperature", f"{latest['temperature']:.2f} °C")
col3.metric("Humidity", f"{latest['humidity']:.2f} %")
col4.metric("Air Raw Value", f"{latest['air_raw']} ADC")
col5.metric("Air Category", latest["category"])

st.subheader("Air Quality Trend")
st.line_chart(df.set_index("timestamp")["air_raw"])

st.subheader("Temperature and Humidity Trend")
st.line_chart(df.set_index("timestamp")[["temperature", "humidity"]])

st.subheader("Air Category Distribution")
category_counts = df["category"].value_counts()
st.bar_chart(category_counts)

st.subheader("Latest 20 Records")
st.dataframe(df.tail(20))

if refresh:
    time.sleep(5)
    st.rerun()