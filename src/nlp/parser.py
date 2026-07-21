import re
import sqlite3
import pandas as pd
from pathlib import Path

# ------------------------------------
# Create output folder
# ------------------------------------
Path("output").mkdir(exist_ok=True)

# ------------------------------------
# Connect Database
# ------------------------------------
conn = sqlite3.connect("database/nifty100.db")

companies = pd.read_sql(
    "SELECT id, company_name FROM companies",
    conn
)

ratios = pd.read_sql(
    """
    SELECT
        company_id,
        revenue_cagr_5yr,
        pat_cagr_5yr,
        return_on_equity_pct
    FROM financial_ratios
    """,
    conn
)

conn.close()

# ------------------------------------
# Load analysis.xlsx
# ------------------------------------
# ------------------------------------
# Load analysis.xlsx
# ------------------------------------

analysis = pd.read_excel(
    "data/source_files/analysis.xlsx",
    header=1
)

analysis.columns = [
    "id",
    "company_id",
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

print(analysis.head())
# ------------------------------------
# Regex Pattern
# ------------------------------------

pattern = re.compile(r"(\d+)\s*Years?:?\s*([\-\d.]+)%")

parsed_rows = []
failed_rows = []

metrics = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

# ------------------------------------
# Parse Analysis Text
# ------------------------------------

for _, row in analysis.iterrows():

    company = row["company_id"]

    for metric in metrics:

        value = str(row[metric]).strip()

        match = pattern.search(value)

        if match:

            period = int(match.group(1))
            pct = float(match.group(2))

            parsed_rows.append({
                "company_id": company,
                "metric_type": metric,
                "period_years": period,
                "value_pct": pct
            })

        else:

            failed_rows.append({
                "company_id": company,
                "metric_type": metric,
                "text": value
            })

# ------------------------------------
# Create DataFrames
# ------------------------------------

parsed_df = pd.DataFrame(parsed_rows)

failed_df = pd.DataFrame(failed_rows)

# ------------------------------------
# Save Outputs
# ------------------------------------

parsed_df.to_csv(
    "output/analysis_parsed.csv",
    index=False
)

failed_df.to_csv(
    "output/parse_failures.csv",
    index=False
)

print("=" * 50)
print("Parsing Complete")
print("=" * 50)
print("Parsed Records :", len(parsed_df))
print("Failed Records :", len(failed_df))
# ============================================
# Cross Validation with Ratio Engine
# ============================================

conn = sqlite3.connect("database/nifty100.db")

ratio_df = pd.read_sql("""
SELECT
company_id,
revenue_cagr_5yr,
pat_cagr_5yr
FROM financial_ratios
""", conn)

conn.close()

review_rows = []

for _, row in parsed_df.iterrows():

    company = row["company_id"]
    metric = row["metric_type"]
    parsed_value = row["value_pct"]

    ratio = ratio_df[
        ratio_df["company_id"] == company
    ]

    if ratio.empty:
        continue

    computed = None

    if metric == "compounded_sales_growth":
        computed = ratio.iloc[0]["revenue_cagr_5yr"]

    elif metric == "compounded_profit_growth":
        computed = ratio.iloc[0]["pat_cagr_5yr"]

    if pd.isna(computed):
        continue

    difference = abs(parsed_value - computed)

    if difference > 5:

        review_rows.append({

            "company_id": company,

            "metric": metric,

            "parsed_value": parsed_value,

            "computed_value": computed,

            "difference": difference

        })

review_df = pd.DataFrame(review_rows)

review_df.to_csv(
    "output/manual_review.csv",
    index=False
)

print()
print("Manual Review Records :", len(review_df))