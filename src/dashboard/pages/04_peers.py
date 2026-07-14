import streamlit as st
import pandas as pd
import sqlite3

st.title("👥 Peer Comparison")

conn = sqlite3.connect("database/nifty100.db")

groups = pd.read_sql(
    "SELECT * FROM peer_percentiles",
    conn
)

conn.close()

peer = st.selectbox(
    "Select Peer Group",
    sorted(groups["peer_group_name"].unique())
)

df = groups[
    groups["peer_group_name"] == peer
]

st.dataframe(df)