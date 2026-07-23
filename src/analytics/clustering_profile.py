import sqlite3
from pathlib import Path

import pandas as pd

# -----------------------------------------
# Create output folder
# -----------------------------------------

Path("output").mkdir(exist_ok=True)

# -----------------------------------------
# Database
# -----------------------------------------

conn = sqlite3.connect("database/nifty100.db")

# -----------------------------------------
# Latest financial ratios
# -----------------------------------------

ratios = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        return_on_equity_pct,
        debt_to_equity,
        revenue_cagr_5yr,
        operating_profit_margin_pct
    FROM financial_ratios
    """,
    conn
)

conn.close()

# Keep latest record for each company
ratios = (
    ratios
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

# -----------------------------------------
# Read cluster labels
# -----------------------------------------

clusters = pd.read_csv(
    "output/cluster_labels.csv"
)

# -----------------------------------------
# Read cashflow CAGR
# -----------------------------------------

cashflow = pd.read_excel(
    "output/cashflow_intelligence.xlsx"
)

cashflow = cashflow[
    [
        "company_id",
        "fcf_cagr_5yr"
    ]
]

# -----------------------------------------
# Merge everything
# -----------------------------------------

df = ratios.merge(
    cashflow,
    on="company_id",
    how="left"
)

df = df.merge(
    clusters,
    on="company_id",
    how="left"
)

# -----------------------------------------
# Features
# -----------------------------------------

features = [

    "return_on_equity_pct",

    "debt_to_equity",

    "revenue_cagr_5yr",

    "fcf_cagr_5yr",

    "operating_profit_margin_pct"

]

# -----------------------------------------
# Mean
# -----------------------------------------

mean_profile = (
    df
    .groupby("cluster_id")[features]
    .mean()
)

mean_profile.columns = [
    col + "_mean"
    for col in mean_profile.columns
]

# -----------------------------------------
# Median
# -----------------------------------------

median_profile = (
    df
    .groupby("cluster_id")[features]
    .median()
)

median_profile.columns = [
    col + "_median"
    for col in median_profile.columns
]

# -----------------------------------------
# Combine
# -----------------------------------------

profile = pd.concat(
    [mean_profile, median_profile],
    axis=1
).reset_index()

# -----------------------------------------
# Save
# -----------------------------------------

profile.to_csv(
    "output/cluster_profiles.csv",
    index=False
)

print("="*50)
print("Cluster Profiling Complete")
print("="*50)
print(profile)

print()
print("Saved -> output/cluster_profiles.csv")