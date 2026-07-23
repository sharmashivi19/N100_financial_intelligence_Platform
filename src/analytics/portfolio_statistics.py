import sqlite3
from pathlib import Path

import pandas as pd

# ---------------------------------------
# Output Folder
# ---------------------------------------

Path("output").mkdir(exist_ok=True)

# ---------------------------------------
# Database
# ---------------------------------------

conn = sqlite3.connect("database/nifty100.db")

financials = pd.read_sql(
    "SELECT * FROM financials",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

# ---------------------------------------
# Latest record of each company
# ---------------------------------------

financials = (
    financials
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

ratios = (
    ratios
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

# ---------------------------------------
# Merge
# ---------------------------------------

df = financials.merge(
    ratios,
    on="company_id",
    how="left"
)

# ---------------------------------------
# KPIs
# ---------------------------------------

kpis = [

    "sales",

    "operating_profit",

    "net_profit",

    "eps",

    "return_on_equity_pct",

    "debt_to_equity",

    "net_profit_margin_pct",

    "operating_profit_margin_pct",

    "interest_coverage",

    "asset_turnover"

]

# Keep only existing columns

kpis = [k for k in kpis if k in df.columns]

# ---------------------------------------
# Statistics
# ---------------------------------------

rows = []

for col in kpis:

    rows.append({

        "KPI": col,

        "P10": df[col].quantile(0.10),

        "P25": df[col].quantile(0.25),

        "P50": df[col].quantile(0.50),

        "P75": df[col].quantile(0.75),

        "P90": df[col].quantile(0.90),

        "Mean": df[col].mean(),

        "Std": df[col].std()

    })

stats = pd.DataFrame(rows)

# ---------------------------------------
# Round values
# ---------------------------------------

stats = stats.round(2)

# ---------------------------------------
# Save
# ---------------------------------------

stats.to_csv(

    "output/portfolio_stats.csv",

    index=False

)

# ---------------------------------------
# Print
# ---------------------------------------

print("=" * 50)
print("Portfolio Statistics Generated")
print("=" * 50)
print(stats)
print()
print("Saved -> output/portfolio_stats.csv")