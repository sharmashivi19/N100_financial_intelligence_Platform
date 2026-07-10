import os
import sqlite3
import pandas as pd

from src.visualization.radar import create_radar

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("database/nifty100.db")

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

peer = pd.read_excel(
    "data/source_files/peer_groups.xlsx"
)

# Rename id -> company_id for merge
companies = companies.rename(
    columns={"id": "company_id"}
)

# Merge all tables
df = ratios.merge(
    peer,
    on="company_id",
    how="left"
)

df = df.merge(
    companies,
    on="company_id",
    how="left"
)

df["peer_group_name"] = df["peer_group_name"].fillna(
    "No peer group assigned"
)

# Create output folder
os.makedirs(
    "reports/radar_charts",
    exist_ok=True
)

# Metrics
metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "composite_quality_score"
]

# Generate radar chart for every company
for company in df["company_id"].unique():

    company_df = df[
        df["company_id"] == company
    ].sort_values("year")

    latest = company_df.iloc[-1]

    company_values = []

    for metric in metrics:
        value = latest[metric]

        if pd.isna(value):
            value = 0

        company_values.append(value)

    # Determine comparison values
    if latest["peer_group_name"] == "No peer group assigned":

        peer_values = []

        for metric in metrics:
            peer_values.append(
                df[metric].fillna(0).mean()
            )

    else:

        peer_df = df[
            df["peer_group_name"] ==
            latest["peer_group_name"]
        ]

        peer_values = []

        for metric in metrics:
            peer_values.append(
                peer_df[metric].fillna(0).mean()
            )

    create_radar(
        latest["company_name"],
        company_values,
        peer_values,
        metrics,
        f"reports/radar_charts/{company}_radar.png"
    )

conn.close()

print("Radar charts generated successfully!")