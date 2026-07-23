import sqlite3
from pathlib import Path

import pandas as pd
from scipy.stats import zscore

# ---------------------------------------
# Output folder
# ---------------------------------------

Path("output").mkdir(exist_ok=True)

# ---------------------------------------
# Database
# ---------------------------------------

conn = sqlite3.connect("database/nifty100.db")

companies = pd.read_sql(
    """
    SELECT id AS company_id,
           company_name
    FROM companies
    """,
    conn
)

sector = pd.read_sql(
    """
    SELECT
        company_id,
        broad_sector
    FROM sector
    """,
    conn
)

ratios = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    """,
    conn
)

conn.close()

# ---------------------------------------
# Latest year only
# ---------------------------------------

ratios = (
    ratios
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

# ---------------------------------------
# Merge
# ---------------------------------------

df = companies.merge(
    sector,
    on="company_id",
    how="left"
)

df = df.merge(
    ratios,
    on="company_id",
    how="left"
)

# ---------------------------------------
# Metrics
# ---------------------------------------

metrics = [

    "return_on_equity_pct",

    "debt_to_equity",

    "revenue_cagr_5yr",

    "operating_profit_margin_pct",

    "net_profit_margin_pct",

    "interest_coverage",

    "asset_turnover"

]

# Keep only columns that exist
metrics = [m for m in metrics if m in df.columns]

# ---------------------------------------
# Fill missing values
# ---------------------------------------

for col in metrics:

    df[col] = df.groupby("broad_sector")[col].transform(
        lambda x: x.fillna(x.median())
    )

    df[col] = df[col].fillna(df[col].median())

# ---------------------------------------
# Calculate Z-score by sector
# ---------------------------------------

for col in metrics:

    df[col + "_zscore"] = (
        df.groupby("broad_sector")[col]
        .transform(lambda x: zscore(x, nan_policy="omit"))
    )

# ---------------------------------------
# Flag Outliers
# ---------------------------------------

z_cols = [c + "_zscore" for c in metrics]

df["is_outlier"] = (
    df[z_cols]
    .abs()
    .max(axis=1)
    > 3
)

# ---------------------------------------
# Save only outliers
# ---------------------------------------

outliers = df[df["is_outlier"]].copy()

outliers.to_csv(
    "output/outlier_report.csv",
    index=False
)

# ---------------------------------------
# Print
# ---------------------------------------

print("=" * 50)
print("Outlier Detection Complete")
print("=" * 50)
print("Total Companies :", len(df))
print("Outliers Found  :", len(outliers))
print("Saved -> output/outlier_report.csv")