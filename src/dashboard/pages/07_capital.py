import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
    page_title="Capital Allocation",
    layout="wide"
)

st.title("💰 Capital Allocation Analysis")

# ---------------------------------------------------
# Load Database
# ---------------------------------------------------

conn = sqlite3.connect("database/nifty100.db")

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

financials = pd.read_sql(
    "SELECT * FROM financials",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

cashflow = pd.read_sql(
    "SELECT * FROM cash_flow",
    conn
)

market = pd.read_sql(
    "SELECT * FROM market_cap",
    conn
)

conn.close()

# ---------------------------------------------------
# Company Dropdown
# ---------------------------------------------------

company = st.selectbox(
    "Select Company",
    sorted(companies["company_name"])
)

company_id = companies.loc[
    companies["company_name"] == company,
    "id"
].iloc[0]

# ---------------------------------------------------
# Filter Data
# ---------------------------------------------------

fin = financials[
    financials["company_id"] == company_id
].copy()

rat = ratios[
    ratios["company_id"] == company_id
].copy()

cf = cashflow[
    cashflow["company_id"] == company_id
].copy()

mc = market[
    market["company_id"] == company_id
].copy()

# ---------------------------------------------------
# Clean Years
# ---------------------------------------------------

fin = fin[
    fin["year"].astype(str).str.contains("TTM")==False
]

rat = rat[
    rat["year"].astype(str).str.contains("TTM")==False
]

# ---------------------------------------------------
# KPIs
# ---------------------------------------------------

st.subheader("Capital Allocation Scorecard")

c1,c2,c3,c4 = st.columns(4)

try:
    roe = rat.iloc[-1]["return_on_equity_pct"]
except:
    roe = None

try:
    debt = rat.iloc[-1]["total_debt_cr"]
except:
    debt = None

try:
    dividend = fin.iloc[-1]["dividend_payout"]
except:
    dividend = None

try:
    fcf = rat.iloc[-1]["free_cash_flow_cr"]
except:
    fcf = None

c1.metric("ROE %", f"{roe:.2f}" if pd.notna(roe) else "-")

c2.metric("Total Debt", f"{debt:,.0f}" if pd.notna(debt) else "-")

c3.metric("Dividend Payout", f"{dividend:.2f}" if pd.notna(dividend) else "-")

c4.metric("Free Cash Flow", f"{fcf:,.0f}" if pd.notna(fcf) else "-")

st.divider()

# ---------------------------------------------------
# Market Cap Trend
# ---------------------------------------------------

if not mc.empty:

    fig = px.line(
        mc,
        x="year",
        y="market_cap_crore",
        markers=True,
        title="Market Capitalization"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# ---------------------------------------------------
# Free Cash Flow Trend
# ---------------------------------------------------

if not rat.empty:

    fig = px.line(
        rat,
        x="year",
        y="free_cash_flow_cr",
        markers=True,
        title="Free Cash Flow"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# ---------------------------------------------------
# ROE Trend
# ---------------------------------------------------

if not rat.empty:

    fig = px.line(
        rat,
        x="year",
        y="return_on_equity_pct",
        markers=True,
        title="Return on Equity"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# ---------------------------------------------------
# Dividend Trend
# ---------------------------------------------------

if not fin.empty:

    fig = px.bar(
        fin,
        x="year",
        y="dividend_payout",
        title="Dividend Payout"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# ---------------------------------------------------
# Debt Trend
# ---------------------------------------------------

if not rat.empty:

    fig = px.bar(
        rat,
        x="year",
        y="total_debt_cr",
        title="Total Debt"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# ---------------------------------------------------
# Financial Data
# ---------------------------------------------------

st.subheader("Financial Data")

display = rat[
    [
        "year",
        "return_on_equity_pct",
        "free_cash_flow_cr",
        "total_debt_cr",
        "cash_from_operations_cr",
        "dividend_payout_ratio_pct"
    ]
]

st.dataframe(
    display,
    width="stretch"
)