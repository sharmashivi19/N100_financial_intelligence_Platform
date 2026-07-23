import sqlite3
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------
# Output folder
# ---------------------------------------

Path("reports").mkdir(exist_ok=True)

# ---------------------------------------
# Database
# ---------------------------------------

conn = sqlite3.connect("database/nifty100.db")

financials = pd.read_sql(
    """
    SELECT *
    FROM financials
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
# Latest record for each company
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
# Select 10 KPIs
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
kpis = [c for c in kpis if c in df.columns]

corr = df[kpis].corr(method="pearson")

# ---------------------------------------
# Heatmap
# ---------------------------------------

plt.figure(figsize=(10,8))

sns.heatmap(

    corr,

    annot=True,

    cmap="RdYlBu",

    center=0,

    fmt=".2f"

)

plt.title("Correlation Matrix")

plt.tight_layout()

plt.savefig(

    "reports/correlation_heatmap.png",

    dpi=300

)

plt.close()

print("="*50)
print("Correlation Heatmap Generated")
print("="*50)
print("Saved -> reports/correlation_heatmap.png")