import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.title("🏭 Sector Analysis")

conn = sqlite3.connect("database/nifty100.db")

peer = pd.read_sql(
    "SELECT peer_group_name FROM peer_percentiles",
    conn
)

conn.close()

sector = (
    peer.groupby("peer_group_name")
    .size()
    .reset_index(name="Companies")
)

fig = px.bar(
    sector,
    x="peer_group_name",
    y="Companies",
    title="Companies by Peer Group"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(sector)