import streamlit as st
import pandas as pd
import sqlite3

st.title("🔎 Stock Screener")

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

min_roe = st.sidebar.slider(
    "Minimum ROE",
    0,
    50,
    15
)

max_de = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    5.0,
    1.0
)

filtered = df[
    (df["return_on_equity_pct"] >= min_roe) &
    (df["debt_to_equity"] <= max_de)
]

st.write(f"Companies Found: {len(filtered)}")

st.dataframe(filtered)