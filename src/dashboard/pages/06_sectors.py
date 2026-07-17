import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
    page_title="Sector Analysis",
    layout="wide"
)

st.title("🏭 Sector Analysis")

# --------------------------------------------------
# Load Database
# --------------------------------------------------

conn = sqlite3.connect("database/nifty100.db")

sector = pd.read_sql(
    "SELECT * FROM sector",
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

market = pd.read_sql(
    "SELECT * FROM market_cap",
    conn
)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

conn.close()

# --------------------------------------------------
# Keep latest record for each company
# --------------------------------------------------

# --------------------------------------------------
# Keep latest Market Cap (2024)
# --------------------------------------------------

market = market[
    market["year"] == 2024
]

# --------------------------------------------------
# Financials
# --------------------------------------------------

financials["year_num"] = (
    financials["year"]
    .str.extract(r'(\d{4})')
    .astype(float)
)

financials = (
    financials
    .sort_values("year_num")
    .groupby("company_id", as_index=False)
    .last()
)

# --------------------------------------------------
# Ratios
# --------------------------------------------------

ratios["year_num"] = (
    ratios["year"]
    .str.extract(r'(\d{4})')
    .astype(float)
)

ratios = (
    ratios
    .sort_values("year_num")
    .groupby("company_id", as_index=False)
    .last()
)
# --------------------------------------------------
# Remove duplicate id columns
# --------------------------------------------------

financials = financials.drop(columns=["id"], errors="ignore")
ratios = ratios.drop(columns=["id"], errors="ignore")
market = market.drop(columns=["id"], errors="ignore")

# --------------------------------------------------
# Merge all tables
# --------------------------------------------------

df = sector.merge(
    financials,
    on="company_id",
    how="left"
)

df = df.merge(
    ratios,
    on="company_id",
    how="left",
    suffixes=("", "_ratio")
)

df = df.merge(
    market,
    on="company_id",
    how="left",
    suffixes=("", "_market")
)

df = df.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

# --------------------------------------------------
# Remove duplicated columns after merge
# --------------------------------------------------

df = df.loc[:, ~df.columns.duplicated()]
# st.write("Rows after merge:", len(df))

st.write(df[[
    "company_id",
    "company_name",
    "broad_sector"
]].head(20))
df = df.drop(
    columns=["year_num"],
    errors="ignore"
)
# --------------------------------------------------
# Sector Dropdown
# --------------------------------------------------
# st.write("Total companies after merge:", len(df))
sector_name = st.selectbox(
    "Select Sector",
    sorted(df["broad_sector"].dropna().unique())
)

sector_df = df[
    df["broad_sector"] == sector_name
]
# st.write("Selected Sector:", sector_name)

# st.write("Companies in this sector:")
# st.write(sector_df["company_id"].tolist())

# st.write("Number of companies:", len(sector_df))

# st.success(f"{len(sector_df)} companies found")

# --------------------------------------------------
# Bubble Chart
# --------------------------------------------------

fig = px.scatter(
    sector_df,
    x="sales",
    y="return_on_equity_pct",
    size="market_cap_crore",
    color="sub_sector",
    hover_name="company_name",
    title="Revenue vs ROE"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# --------------------------------------------------
# Sector KPIs
# --------------------------------------------------

median_df = pd.DataFrame({

    "Metric": [
        "ROE",
        "Revenue CAGR",
        "PAT CAGR",
        "Debt/Equity",
        "Net Margin"
    ],

    "Value": [

        sector_df["return_on_equity_pct"].median(),

        sector_df["revenue_cagr_5yr"].median(),

        sector_df["pat_cagr_5yr"].median(),

        sector_df["debt_to_equity"].median(),

        sector_df["net_profit_margin_pct"].median()

    ]

})

fig2 = px.bar(
    median_df,
    x="Metric",
    y="Value",
    text="Value",
    title="Sector Median KPIs"
)

st.plotly_chart(
    fig2,
    width="stretch"
)

# --------------------------------------------------
# Company Table
# --------------------------------------------------

st.subheader("Companies in Sector")

st.dataframe(

    sector_df[
        [
            "company_id",
            "company_name",
            "sub_sector",
            "sales",
            "return_on_equity_pct",
            "market_cap_crore"
        ]
    ],

    width="stretch"
)