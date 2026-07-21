import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path

# -----------------------------------------
# Create Output Folder
# -----------------------------------------

Path("output").mkdir(exist_ok=True)

# -----------------------------------------
# Connect Database
# -----------------------------------------

conn = sqlite3.connect("database/nifty100.db")

cashflow = pd.read_sql("SELECT * FROM cash_flow", conn)
financials = pd.read_sql("SELECT * FROM financials", conn)
sector = pd.read_sql("SELECT * FROM sector", conn)
companies = pd.read_sql("SELECT * FROM companies", conn)

conn.close()

# -----------------------------------------
# Latest Year Only
# -----------------------------------------

cashflow = (
    cashflow
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

financials = (
    financials
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

# Remove duplicate ID columns

cashflow = cashflow.drop(columns=["id"], errors="ignore")
financials = financials.drop(columns=["id"], errors="ignore")

companies = companies.rename(columns={"id": "company_id"})

# -----------------------------------------
# Merge Tables
# -----------------------------------------

df = companies.merge(
    sector,
    on="company_id",
    how="left"
)

df = df.merge(
    financials,
    on="company_id",
    how="left"
)

df = df.merge(
    cashflow,
    on="company_id",
    how="left"
)

# -----------------------------------------
# CFO / PAT Ratio
# -----------------------------------------

df["cfo_quality_score"] = (
    df["operating_activity"] /
    df["net_profit"].replace(0, np.nan)
)

# -----------------------------------------
# CFO Quality Label
# -----------------------------------------

def quality(score):

    if pd.isna(score):
        return "Unknown"

    if score > 1:
        return "High Quality"

    if score >= 0.5:
        return "Moderate"

    return "Accrual Risk"


df["cfo_quality_label"] = df["cfo_quality_score"].apply(quality)

# -----------------------------------------
# CapEx Intensity
# -----------------------------------------

df["capex_intensity_pct"] = (
    abs(df["investing_activity"]) /
    df["sales"].replace(0, np.nan)
) * 100

# -----------------------------------------
# CapEx Label
# -----------------------------------------

def capex_label(x):

    if pd.isna(x):
        return "Unknown"

    if x < 3:
        return "Asset Light"

    if x <= 8:
        return "Moderate"

    return "Capital Intensive"


df["capex_label"] = df["capex_intensity_pct"].apply(capex_label)

# -----------------------------------------
# FCF CAGR (Placeholder)
# -----------------------------------------

df["fcf_cagr_5yr"] = np.nan

# -----------------------------------------
# FCF Conversion
# -----------------------------------------

df["fcf_conversion_pct"] = (
    df["operating_activity"] /
    df["net_profit"].replace(0, np.nan)
) * 100

# -----------------------------------------
# Distress Flag
# CFO < 0 and Financing > 0
# -----------------------------------------

df["distress_flag"] = np.where(
    (df["operating_activity"] < 0) &
    (df["financing_activity"] > 0),
    "Yes",
    "No"
)

# -----------------------------------------
# Deleveraging Flag
# -----------------------------------------

df["deleveraging_flag"] = np.where(
    df["financing_activity"] < 0,
    "Yes",
    "No"
)

# -----------------------------------------
# Capital Allocation Label
# -----------------------------------------

def capital_label(row):

    if row["distress_flag"] == "Yes":
        return "Distress"

    if row["deleveraging_flag"] == "Yes":
        return "Deleveraging"

    return "Stable"


df["capital_allocation_label"] = df.apply(
    capital_label,
    axis=1
)

# -----------------------------------------
# Final Output
# -----------------------------------------

final = df[
    [
        "company_id",
        "company_name",
        "broad_sector",
        "cfo_quality_score",
        "cfo_quality_label",
        "capex_intensity_pct",
        "capex_label",
        "fcf_cagr_5yr",
        "fcf_conversion_pct",
        "distress_flag",
        "deleveraging_flag",
        "capital_allocation_label"
    ]
]

final = final.rename(
    columns={
        "broad_sector": "sector"
    }
)

# -----------------------------------------
# Save Excel
# -----------------------------------------

final.to_excel(
    "output/cashflow_intelligence.xlsx",
    index=False
)

# -----------------------------------------
# Distress Alerts
# -----------------------------------------

alerts = df[
    df["distress_flag"] == "Yes"
][
    [
        "company_id",
        "company_name",
        "operating_activity",
        "financing_activity",
        "net_profit"
    ]
]

alerts.to_csv(
    "output/distress_alerts.csv",
    index=False
)

# -----------------------------------------
# Done
# -----------------------------------------

print("=" * 50)
print("Cash Flow Intelligence Complete")
print("=" * 50)
print("Companies :", len(final))
print("Distress Alerts :", len(alerts))
print("Output saved to output/")