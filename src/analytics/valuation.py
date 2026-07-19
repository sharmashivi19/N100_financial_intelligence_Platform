import sqlite3
import pandas as pd
import os

# ---------------------------------------
# Create Output Folder
# ---------------------------------------

os.makedirs("output", exist_ok=True)

# ---------------------------------------
# Database Connection
# ---------------------------------------

conn = sqlite3.connect("database/nifty100.db")

companies = pd.read_sql(
    "SELECT * FROM companies",
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

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

# ---------------------------------------
# Latest Market Year
# ---------------------------------------

latest_market_year = market["year"].max()

market = market[
    market["year"] == latest_market_year
].copy()

# ---------------------------------------
# Latest Financial Ratios
# ---------------------------------------

ratios = (
    ratios
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

# ---------------------------------------
# Merge Tables
# ---------------------------------------

df = market.merge(
    sector,
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
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

# ---------------------------------------
# FCF Yield
# ---------------------------------------

df["FCF_yield_pct"] = (
    df["free_cash_flow_cr"] /
    df["market_cap_crore"]
) * 100

# ---------------------------------------
# Sector Median PE
# ---------------------------------------

sector_median = (
    df.groupby("broad_sector")["pe_ratio"]
    .median()
    .reset_index()
)

sector_median.columns = [
    "broad_sector",
    "sector_median_pe"
]

df = df.merge(
    sector_median,
    on="broad_sector",
    how="left"
)

# ---------------------------------------
# PE Difference
# ---------------------------------------

df["PE_vs_sector_median_pct"] = (
    (
        df["pe_ratio"] -
        df["sector_median_pe"]
    )
    /
    df["sector_median_pe"]
) * 100

# ---------------------------------------
# Valuation Flag
# ---------------------------------------

def valuation_flag(row):

    if pd.isna(row["pe_ratio"]):
        return "Fair"

    if row["pe_ratio"] > row["sector_median_pe"] * 1.5:
        return "Caution"

    if row["pe_ratio"] < row["sector_median_pe"] * 0.7:
        return "Discount"

    return "Fair"

df["flag"] = df.apply(
    valuation_flag,
    axis=1
)

# ---------------------------------------
# Final Output
# ---------------------------------------

summary = df[
    [
        "company_id",
        "company_name",
        "broad_sector",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "FCF_yield_pct",
        "sector_median_pe",
        "PE_vs_sector_median_pct",
        "flag"
    ]
].copy()

summary.columns = [
    "company_id",
    "company_name",
    "sector",
    "P/E",
    "P/B",
    "EV/EBITDA",
    "FCF_yield_pct",
    "5yr_median_PE",
    "PE_vs_sector_median_pct",
    "flag"
]

summary.to_excel(
    "output/valuation_summary.xlsx",
    index=False
)

summary[
    summary["flag"] != "Fair"
].to_csv(
    "output/valuation_flags.csv",
    index=False
)

print("=" * 50)
print("Valuation Module Complete")
print("=" * 50)
print("Companies :", len(summary))
print("Flags :", len(summary[summary['flag']!='Fair']))
print("Output saved in output/")