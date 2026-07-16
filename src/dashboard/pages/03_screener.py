import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Stock Screener",
    layout="wide"
)

st.title("🔎 Stock Screener")
st.subheader("Quick Presets")

c1, c2, c3, c4, c5, c6 = st.columns(6)

preset = None

if c1.button("Quality"):
    preset = "quality"

if c2.button("Value"):
    preset = "value"

if c3.button("Growth"):
    preset = "growth"

if c4.button("Dividend"):
    preset = "dividend"

if c5.button("Debt-Free"):
    preset = "debtfree"

if c6.button("Turnaround"):
    preset = "turnaround"

# -----------------------------
# Load Database
# -----------------------------
conn = sqlite3.connect("database/nifty100.db")

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

conn.close()

# -----------------------------
# Merge company names
# -----------------------------
df = ratios.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Screening Filters")

# -----------------------------
# Default Values
# -----------------------------
roe_default = 15
de_default = 1.0
fcf_default = 0.0
revenue_default = 5
pat_default = 5
opm_default = 10
icr_default = 2
asset_default = 0.5
eps_default = 5
dividend_default = 0

# -----------------------------
# Presets
# -----------------------------
if preset == "quality":
    roe_default = 20
    de_default = 1
    revenue_default = 10
    pat_default = 10
    opm_default = 15

elif preset == "growth":
    revenue_default = 20
    pat_default = 20
    eps_default = 20

elif preset == "value":
    roe_default = 12
    de_default = 1.5

elif preset == "dividend":
    dividend_default = 20

elif preset == "debtfree":
    de_default = 0

elif preset == "turnaround":
    revenue_default = 0
    pat_default = 0
    roe_default = 5

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

min_roe = st.sidebar.slider(
    "Minimum ROE (%)",
    0,
    50,
    roe_default
)

max_de = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    5.0,
    de_default
)

min_fcf = st.sidebar.number_input(
    "Minimum Free Cash Flow",
    value=fcf_default
)

min_revenue = st.sidebar.slider(
    "Minimum Revenue CAGR (%)",
    -20,
    50,
    revenue_default
)

min_pat = st.sidebar.slider(
    "Minimum PAT CAGR (%)",
    -20,
    50,
    pat_default
)

min_opm = st.sidebar.slider(
    "Minimum OPM (%)",
    0,
    60,
    opm_default
)

min_icr = st.sidebar.slider(
    "Minimum Interest Coverage",
    0,
    50,
    icr_default
)

min_asset = st.sidebar.slider(
    "Minimum Asset Turnover",
    0.0,
    5.0,
    asset_default
)

min_eps = st.sidebar.slider(
    "Minimum EPS CAGR (%)",
    -20,
    50,
    eps_default
)

min_dividend = st.sidebar.slider(
    "Minimum Dividend Payout (%)",
    0,
    100,
    dividend_default
)

# -----------------------------
# Apply Filters
# -----------------------------
filtered = df[
    (df["return_on_equity_pct"] >= min_roe) &
    (df["debt_to_equity"] <= max_de) &
    (df["free_cash_flow_cr"] >= min_fcf) &
    (df["revenue_cagr_5yr"] >= min_revenue) &
    (df["pat_cagr_5yr"] >= min_pat) &
    (df["operating_profit_margin_pct"] >= min_opm) &
    (df["interest_coverage"] >= min_icr) &
    (df["asset_turnover"] >= min_asset) &
    (df["eps_cagr_5yr"] >= min_eps) &
    (df["dividend_payout_ratio_pct"] >= min_dividend)
]

# -----------------------------
# Result Count
# -----------------------------
st.success(
    f"{len(filtered)} companies match your filters"
)

# -----------------------------
# Display Results
# -----------------------------
show = filtered[
    [
        "company_id",
        "company_name",
        "year",
        "return_on_equity_pct",
        "operating_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "interest_coverage",
        "asset_turnover",
        "dividend_payout_ratio_pct",
        "composite_quality_score"
    ]
]

st.dataframe(
    show,
    use_container_width=True
)

# -----------------------------
# Download CSV
# -----------------------------
csv = show.to_csv(index=False)

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="screener_output.csv",
    mime="text/csv"
)