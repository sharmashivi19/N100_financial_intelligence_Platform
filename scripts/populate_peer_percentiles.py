import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)
peer_groups = pd.read_excel(
    "data/source_files/peer_groups.xlsx"
)
# print(peer_groups.columns.tolist())
df = ratios.merge(
    peer_groups,
    on="company_id",
    how="left"
)
df["peer_group_name"] = df["peer_group_name"].fillna(
    "No peer group assigned"
)
# print(df[[
#     "company_id",
#     "peer_group_name"
# ]].head())

# print(df["peer_group_name"].value_counts())
metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "eps_cagr_5yr",
    "interest_coverage",
    "asset_turnover"
]
results = []

for group in df["peer_group_name"].unique():

    # Skip companies without a peer group
    if group == "No peer group assigned":
        continue

    group_df = df[
        df["peer_group_name"] == group
    ].copy()

    for metric in metrics:

        if metric not in group_df.columns:
            continue

        if metric == "debt_to_equity":

            group_df["percentile_rank"] = (
                1 - group_df[metric].rank(pct=True)
            )

        else:

            group_df["percentile_rank"] = (
                group_df[metric].rank(pct=True)
            )

        for _, row in group_df.iterrows():

            results.append({

                "company_id": row["company_id"],
                "peer_group_name": row["peer_group_name"],
                "metric": metric,
                "value": row[metric],
                "percentile_rank": row["percentile_rank"],
                "year": row["year"]

            })
# for group in df["peer_group_name"].unique():

#     group_df = df[
#         df["peer_group_name"] == group
#     ].copy()

    for metric in metrics:

        if metric not in group_df.columns:
            continue
        if metric == "debt_to_equity":

            group_df["percentile_rank"] = (
                1 - group_df[metric].rank(pct=True)
            )

        else:

            group_df["percentile_rank"] = (
                group_df[metric].rank(pct=True)
            )
        for _, row in group_df.iterrows():

            results.append({

                "company_id": row["company_id"],

                "peer_group_name": row["peer_group_name"],

                "metric": metric,

                "value": row[metric],

                "percentile_rank": row["percentile_rank"],

                "year": row["year"]

            })
peer_percentiles = pd.DataFrame(results)
# print(peer_percentiles.head())
# print(len(peer_percentiles))
peer_percentiles.to_sql(
    "peer_percentiles",
    conn,
    if_exists="replace",
    index=False
)
conn.close()

print("Peer percentile table created successfully!")