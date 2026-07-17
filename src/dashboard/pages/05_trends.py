import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go

st.set_page_config(
    page_title="Trend Analysis",
    layout="wide"
)

st.title("📈 Trend Analysis")

# -------------------------------------------------------
# Connect Database
# -------------------------------------------------------

conn = sqlite3.connect("database/nifty100.db")

financials = pd.read_sql(
    "SELECT * FROM financials",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

conn.close()

# -------------------------------------------------------
# Merge Tables
# -------------------------------------------------------

df = financials.merge(
    ratios,
    on=["company_id", "year"],
    how="inner"
)

df = df.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

# -------------------------------------------------------
# Keep only Annual (Mar) data
# -------------------------------------------------------

df = df[
    df["year"].str.contains("Mar", na=False)
].copy()

df["year_num"] = (
    df["year"]
    .str.extract(r"(\d{4})")
    .astype(int)
)

# -------------------------------------------------------
# Company Search
# -------------------------------------------------------

company = st.selectbox(
    "Select Company",
    sorted(df["company_name"].dropna().unique())
)

company_df = df[
    df["company_name"] == company
].copy()

company_df = company_df.sort_values("year_num")

company_df = company_df.tail(10)

# -------------------------------------------------------
# Metrics
# -------------------------------------------------------

metric_options = {
    "Revenue":"sales",
    "Operating Profit":"operating_profit",
    "Net Profit":"net_profit",
    "ROE":"return_on_equity_pct",
    "OPM":"operating_profit_margin_pct",
    "Net Margin":"net_profit_margin_pct",
    "Debt/Equity":"debt_to_equity",
    "Interest Coverage":"interest_coverage",
    "Asset Turnover":"asset_turnover",
    "Free Cash Flow":"free_cash_flow_cr",
    "Revenue CAGR":"revenue_cagr_5yr",
    "PAT CAGR":"pat_cagr_5yr",
    "EPS CAGR":"eps_cagr_5yr"
}

selected = st.multiselect(
    "Select up to 3 Metrics",
    list(metric_options.keys()),
    default=["Revenue","ROE"]
)

if len(selected) > 3:
    st.error("Maximum 3 metrics allowed.")
    st.stop()

# -------------------------------------------------------
# Plot Chart
# -------------------------------------------------------

fig = go.Figure()

for metric in selected:

    col = metric_options[metric]

    fig.add_trace(
        go.Scatter(
            x=company_df["year_num"],
            y=company_df[col],
            mode="lines+markers",
            name=metric
        )
    )

    yoy = company_df[col].pct_change()*100

    for x, y, p in zip(
        company_df["year_num"],
        company_df[col],
        yoy
    ):

        if pd.notna(p):

            fig.add_annotation(
                x=x,
                y=y,
                text=f"{p:.1f}%",
                showarrow=False,
                font=dict(size=9)
            )

fig.update_layout(

    title=f"{company} Financial Trends",

    xaxis_title="Year",

    yaxis_title="Value",

    hovermode="x unified",

    height=600

)

st.plotly_chart(
    fig,
    width="stretch"
)

# -------------------------------------------------------
# Trend Table
# -------------------------------------------------------

st.subheader("Trend Data")

columns = [
    "year",
    "sales",
    "operating_profit",
    "net_profit",
    "return_on_equity_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "interest_coverage",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "eps_cagr_5yr"
]

st.dataframe(
    company_df[columns],
    width="stretch"
)