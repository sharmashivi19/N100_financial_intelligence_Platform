import sqlite3
import pandas as pd

from src.analytics.ratios import *
from src.analytics.cashflow import *
from src.analytics.cagr import *
conn = sqlite3.connect("database/nifty100.db")
companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

pnl = pd.read_sql(
    "SELECT * FROM financials",
    conn
)

balance = pd.read_sql(
    "SELECT * FROM balance_sheet",
    conn
)

cashflow = pd.read_sql(
    "SELECT * FROM cash_flow",
    conn
)
df = pnl.merge(
    balance,
    on=["company_id", "year"],
    how="left"
)

df = df.merge(
    cashflow,
    on=["company_id", "year"],
    how="left"
)
df["net_profit_margin_pct"] = df.apply(
    lambda x: net_profit_margin(
        x["net_profit"],
        x["sales"]
    ),
    axis=1
)
# Operating Profit Margin
df["operating_profit_margin_pct"] = df.apply(
    lambda x: operating_profit_margin(
        x["operating_profit"],
        x["sales"],
        x["opm_percentage"]
    ),
    axis=1
)

# Return on Equity
df["return_on_equity_pct"] = df.apply(
    lambda x: return_on_equity(
        x["net_profit"],
        x["equity_capital"],
        x["reserves"]
    ),
    axis=1
)

# Debt to Equity
df["debt_to_equity"] = df.apply(
    lambda x: debt_to_equity(
        x["borrowings"],
        x["equity_capital"],
        x["reserves"]
    ),
    axis=1
)

# Interest Coverage
df["interest_coverage"] = df.apply(
    lambda x: interest_coverage_ratio(
        x["operating_profit"],
        x["other_income"],
        x["interest"]
    ),
    axis=1
)

# Asset Turnover
df["asset_turnover"] = df.apply(
    lambda x: asset_turnover(
        x["sales"],
        x["total_assets"]
    ),
    axis=1
)

# Free Cash Flow
df["free_cash_flow_cr"] = df.apply(
    lambda x: free_cash_flow(
        x["operating_activity"],
        x["investing_activity"]
    ),
    axis=1
)

# CapEx
def get_capex(row):
    result = capex_intensity(
        row["investing_activity"],
        row["sales"]
    )

    if result is None:
        return None

    return result[0]


df["capex_cr"] = df.apply(
    get_capex,
    axis=1
)
# -----------------------------
# -----------------------------
df = df.sort_values(
    ["company_id", "year"]
)

# -----------------------------
# -----------------------------
df["revenue_cagr_5yr"] = None
df["pat_cagr_5yr"] = None
df["eps_cagr_5yr"] = None

# -----------------------------
# -----------------------------
for company in df["company_id"].unique():

    company_df = df[
        df["company_id"] == company
    ].sort_values("year")

    years = company_df.index.tolist()

    for i in range(5, len(years)):

        current = years[i]
        previous = years[i-5]

        # Revenue CAGR
        rev = revenue_cagr(
            company_df.loc[previous, "sales"],
            company_df.loc[current, "sales"],
            5
        )

        df.loc[current, "revenue_cagr_5yr"] = rev["value"]

        # PAT CAGR
        pat = pat_cagr(
            company_df.loc[previous, "net_profit"],
            company_df.loc[current, "net_profit"],
            5
        )

        df.loc[current, "pat_cagr_5yr"] = pat["value"]

        # EPS CAGR
        eps = eps_cagr(
            company_df.loc[previous, "eps"],
            company_df.loc[current, "eps"],
            5
        )

        df.loc[current, "eps_cagr_5yr"] = eps["value"]
df["composite_quality_score"] = (

    df["return_on_equity_pct"].fillna(0)

    + df["net_profit_margin_pct"].fillna(0)

    + df["operating_profit_margin_pct"].fillna(0)

) / 3
df["book_value"] = (
    df["equity_capital"] + df["reserves"]
)
final_df = df[

    [

        "company_id",

        "year",

        "net_profit_margin_pct",

        "operating_profit_margin_pct",

        "return_on_equity_pct",

        "debt_to_equity",

        "interest_coverage",

        "asset_turnover",

        "free_cash_flow_cr",

        "capex_cr",

        "eps",

        "book_value",

        "dividend_payout",

        "borrowings",

        "operating_activity",

        "revenue_cagr_5yr",

        "pat_cagr_5yr",

        "eps_cagr_5yr",

        "composite_quality_score"

    ]

]
print(df.columns.tolist())
final_df = final_df.rename(columns={

    "eps": "earnings_per_share",

    "book_value": "book_value_per_share",

    "dividend_payout": "dividend_payout_ratio_pct",

    "borrowings": "total_debt_cr",

    "operating_activity": "cash_from_operations_cr"

})
final_df.to_sql(

    "financial_ratios",

    conn,

    if_exists="replace",

    index=False

)
conn.close()

print("Financial ratios populated successfully!")