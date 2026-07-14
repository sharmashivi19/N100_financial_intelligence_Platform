import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.title("📈 Financial Trends")

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

company = st.selectbox(
    "Company",
    sorted(df["company_id"].unique())
)

company_df = df[
    df["company_id"] == company
]

fig = px.line(
    company_df,
    x="year",
    y="return_on_equity_pct",
    title="ROE Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)