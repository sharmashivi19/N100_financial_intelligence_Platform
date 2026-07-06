import os
import sqlite3
import pandas as pd

from src.analytics.ratios import (
    return_on_equity,
    return_on_capital_employed
)

conn = sqlite3.connect("database/nifty100.db")

financials = pd.read_sql(
    "SELECT * FROM financials",
    conn
)

balance = pd.read_sql(
    "SELECT * FROM balance_sheet",
    conn
)

df = financials.merge(
    balance,
    on=["company_id", "year"]
)

df["calculated_roe"] = df.apply(
    lambda x: return_on_equity(
        x["net_profit"],
        x["equity_capital"],
        x["reserves"]
    ),
    axis=1
)

df["calculated_roce"] = df.apply(
    lambda x: return_on_capital_employed(
        x["operating_profit"],
        x["equity_capital"],
        x["reserves"],
        x["borrowings"]
    ),
    axis=1
)

os.makedirs("output", exist_ok=True)

with open("output/ratio_edge_cases.log", "w") as log:
    log.write("Day 13\n")
    log.write("------------------------\n")
    log.write("ROE/ROCE comparison skipped.\n")
    log.write("Reason: companies table does not contain company_id.\n")
    log.write("Financial sector carve-out cannot be implemented because broad_sector is missing.\n")

conn.close()

print("Ratio edge case log generated successfully!")