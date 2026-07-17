import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Company Report",
    layout="wide"
)

st.title("📑 Company Report")

# -------------------------
# Load Database
# -------------------------

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

sector = pd.read_sql(
    "SELECT * FROM sector",
    conn
)

market = pd.read_sql(
    "SELECT * FROM market_cap",
    conn
)

documents = pd.read_sql(
    "SELECT * FROM documents",
    conn
)

conn.close()

# -------------------------
# Company Selector
# -------------------------

company = st.selectbox(
    "Select Company",
    sorted(companies["company_name"])
)

company_id = companies.loc[
    companies["company_name"] == company,
    "id"
].values[0]

# -------------------------
# Company Info
# -------------------------

info = companies[
    companies["id"] == company_id
].iloc[0]

st.header(company)

col1, col2 = st.columns(2)

with col1:

    st.write("**Website**")

    st.write(info["website"])

    st.write("**Face Value**")

    st.write(info["face_value"])

    st.write("**Book Value**")

    st.write(info["book_value"])

with col2:

    st.write("**ROE**")

    st.write(info["roe_percentage"])

    st.write("**ROCE**")

    st.write(info["roce_percentage"])

# -------------------------
# Sector
# -------------------------

sec = sector[
    sector["company_id"] == company_id
]

if not sec.empty:

    st.subheader("Sector")

    st.dataframe(sec, width="stretch")

# -------------------------
# Financials
# -------------------------

fin = financials[
    financials["company_id"] == company_id
]

st.subheader("Financial Statements")

st.dataframe(
    fin.sort_values("year", ascending=False),
    width="stretch"
)

# -------------------------
# Ratios
# -------------------------

ratio = ratios[
    ratios["company_id"] == company_id
]

st.subheader("Financial Ratios")

st.dataframe(
    ratio.sort_values("year", ascending=False),
    width="stretch"
)

# -------------------------
# Market Cap
# -------------------------

mkt = market[
    market["company_id"] == company_id
]

if not mkt.empty:

    st.subheader("Valuation")

    st.dataframe(
        mkt.sort_values("year", ascending=False),
        width="stretch"
    )

# -------------------------
# Annual Reports
# -------------------------

docs = documents[
    documents["company_id"] == company_id
]

if not docs.empty:

    st.subheader("Annual Reports")

    for _, row in docs.iterrows():

        st.markdown(
            f"- {row['Year']} : {row['Annual_Report']}"
        )