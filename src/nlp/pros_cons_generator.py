import sqlite3
import pandas as pd
from pathlib import Path

Path("output").mkdir(exist_ok=True)

# -----------------------------
# Database
# -----------------------------

conn = sqlite3.connect("database/nifty100.db")

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

financials = pd.read_sql(
    "SELECT * FROM financials",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

market = pd.read_sql(
    "SELECT * FROM market_cap",
    conn
)
# ---------------------------------------------
# Historical Data
# ---------------------------------------------

financial_history = pd.read_sql(
    "SELECT * FROM financials",
    conn
)

ratio_history = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

sector = pd.read_sql(
    "SELECT * FROM sector",
    conn
)

conn.close()

# -----------------------------
# Latest record for each company
# -----------------------------

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

market = (
    market
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

financials = financials.drop(columns=["id"], errors="ignore")
market = market.drop(columns=["id"], errors="ignore")
df = companies.rename(columns={"id": "company_id"})

df = df.merge(
    ratios,
    on="company_id",
    how="left"
)

df = df.merge(
    financials,
    on="company_id",
    how="left",
    suffixes=("", "_fin")
)

df = df.merge(
    market,
    on="company_id",
    how="left",
    suffixes=("", "_market")
)

df = df.merge(
    sector,
    on="company_id",
    how="left"
)
results = []
def add_result(company, typ, rule, text, confidence):

    if confidence < 60:
        return

    results.append({

        "company_id": company,

        "type": typ,

        "rule_id": rule,

        "text": text,

        "confidence_pct": confidence

    })
for _, row in df.iterrows():

    company = row["company_id"]
    if pd.notna(row["return_on_equity_pct"]):

        if row["return_on_equity_pct"] > 20:

            add_result(

                company,

                "pro",

                "P1",

                "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",

                90

            )
    if pd.notna(row["free_cash_flow_cr"]):

        if row["free_cash_flow_cr"] > 0:

            add_result(

                company,

                "pro",

                "P2",

                "Strong free cash flow generation signals healthy business fundamentals.",

                85

            )
    if pd.notna(row["debt_to_equity"]):

        if row["debt_to_equity"] == 0:

            add_result(

                company,

                "pro",

                "P3",

                "Debt-free balance sheet provides financial flexibility.",

                95

            )
    if pd.notna(row["revenue_cagr_5yr"]):

        if row["revenue_cagr_5yr"] > 15:

            add_result(

                company,

                "pro",

                "P4",

                "Revenue growing above 15% CAGR reflects strong business momentum.",

                88

            )
    if pd.notna(row["pat_cagr_5yr"]):

        if row["pat_cagr_5yr"] > 20:

            add_result(

                company,

                "pro",

                "P6",

                "Profit compounding above 20% creates shareholder value.",

                90

            )
    # ------------------------------------
    # Pro Rule 7
    # ------------------------------------

    if (
        (pd.notna(row["interest_coverage"]) and row["interest_coverage"] > 10)
        or
        (pd.notna(row["debt_to_equity"]) and row["debt_to_equity"] == 0)
    ):

        add_result(

            company,

            "pro",

            "P7",

            "Very high interest coverage ratio reflects negligible financial stress from debt servicing.",

            88

        )
    # ------------------------------------
    # Pro Rule 8
    # ------------------------------------

    if (
        pd.notna(row["dividend_yield_pct"])
        and
        pd.notna(row["free_cash_flow_cr"])
    ):

        if (
            row["dividend_yield_pct"] > 2
            and
            row["free_cash_flow_cr"] > 0
        ):

            add_result(

                company,

                "pro",

                "P8",

                "Consistent dividend yield above 2% backed by positive free cash flow.",

                85

            )
    # ------------------------------------
    # Pro Rule 9
    # ------------------------------------

    if pd.notna(row["eps_cagr_5yr"]):

        if row["eps_cagr_5yr"] > 15:

            add_result(

                company,

                "pro",

                "P9",

                "Earnings per share growing above 15% CAGR indicates strong earnings quality and compounding.",

                90

            )
    # ------------------------------------
    # Pro Rule 11
    # ------------------------------------

    if (
        pd.notna(row["revenue_cagr_5yr"])
        and
        pd.notna(row["pat_cagr_5yr"])
    ):

        if row["revenue_cagr_5yr"] > row["pat_cagr_5yr"]:

            add_result(

                company,

                "pro",

                "P11",

                "Revenue growing slower than profits shows improving operating leverage and scale benefits.",

                82

            )
    # ------------------------------------
    # Pro Rule 10
    # ------------------------------------

    hist = ratio_history[
        ratio_history["company_id"] == company
    ].sort_values("year")

    if len(hist) >= 3:

        roe = hist["return_on_equity_pct"].dropna().tail(3).tolist()

        if len(roe) == 3:

            if roe[0] < roe[1] < roe[2]:

                add_result(

                    company,

                    "pro",

                    "P10",

                    "Return on equity improving for 3 consecutive years shows strengthening business quality.",

                    88

                )
    # ------------------------------------
    # Pro Rule 12
    # ------------------------------------

    fin = financial_history[
        financial_history["company_id"] == company
    ].sort_values("year")

    if (
        "total_assets" in fin.columns
        and
        "total_debt" in fin.columns
    ):

        assets = fin["total_assets"].dropna().tail(3).tolist()

        debt = fin["total_debt"].dropna().tail(3).tolist()

        if len(assets) == 3 and len(debt) == 3:

            if assets[0] < assets[1] < assets[2]:

                if debt[0] > debt[1] > debt[2]:

                    add_result(

                        company,

                        "pro",

                        "P12",

                        "Growing asset base funded by internal accruals reflects self-sustaining growth.",

                        90

                    )
    if pd.notna(row["debt_to_equity"]):

        if row["debt_to_equity"] > 2:

            add_result(

                company,

                "con",

                "C1",

                f"Debt-to-equity ratio of {row['debt_to_equity']:.2f} is elevated.",

                90

            )
    if pd.notna(row["free_cash_flow_cr"]):

        if row["free_cash_flow_cr"] < 0:

            add_result(

                company,

                "con",

                "C2",

                "Negative free cash flow raises concern about cash generation.",

                85

            )
    if pd.notna(row["operating_profit_margin_pct"]):

        if row["operating_profit_margin_pct"] < 10:

            add_result(

                company,

                "con",

                "C3",

                "Operating margin is weak.",

                80

            )
    if pd.notna(row["net_profit"]):

        if row["net_profit"] < 0:

            add_result(

                company,

                "con",

                "C4",

                "Company reported a net loss.",

                95

            )
    if pd.notna(row["revenue_cagr_5yr"]):

        if row["revenue_cagr_5yr"] < 5:

            add_result(

                company,

                "con",

                "C5",

                "Revenue growth below 5% suggests weak business momentum.",

                85

            )
    if pd.notna(row["interest_coverage"]):

        if row["interest_coverage"] < 1.5:

            add_result(

                company,

                "con",

                "C6",

                "Interest coverage below 1.5 indicates debt servicing risk.",

                90

            )
    # ------------------------------------
    # Con Rule 7
    # ------------------------------------

    if pd.notna(row["dividend_payout_ratio_pct"]):

        if row["dividend_payout_ratio_pct"] > 100:

            add_result(

                company,

                "con",

                "C7",

                "Dividend payout ratio above 100% may be unsustainable.",

                90

            )
    # ------------------------------------
    # Con Rule 10
    # ------------------------------------

    if pd.notna(row["roce_percentage"]):

        if row["roce_percentage"] < 10:

            add_result(

                company,

                "con",

                "C10",

                "Return on capital employed below 10% suggests weak capital efficiency.",

                82

            )
    # ------------------------------------
    # Con Rule 8
    # ------------------------------------

    de = hist["debt_to_equity"].dropna().tail(3).tolist()

    if len(de) == 3:

        if de[0] < de[1] < de[2]:

            add_result(

                company,

                "con",

                "C8",

                "Debt-to-equity ratio has increased for three consecutive years.",

                85

            )
    # ------------------------------------
    # Con Rule 9
    # ------------------------------------

    eps = hist["earnings_per_share"].dropna().tail(3).tolist()

    if len(eps) == 3:

        if eps[0] > eps[1] > eps[2]:

            add_result(

                company,

                "con",

                "C9",

                "EPS has declined for three consecutive years.",

                85

            )
    # ------------------------------------
    # Con Rule 11
    # ------------------------------------
    # Skipped because Net Debt / EBITDA data
    # is not available in the current database.
# ------------------------------------
# Ensure every company has one Pro & Con
# ------------------------------------

for company in df["company_id"]:

    company_results = [
        r for r in results
        if r["company_id"] == company
    ]

    pros = [r for r in company_results if r["type"] == "pro"]
    cons = [r for r in company_results if r["type"] == "con"]

    if len(pros) == 0:

        add_result(

            company,

            "pro",

            "DEFAULT",

            "Business shows stable long-term operating performance.",

            65

        )

    if len(cons) == 0:

        add_result(

            company,

            "con",

            "DEFAULT",

            "Business should continue to be monitored for future risks.",

            65

        )
output = pd.DataFrame(results)

output.to_csv(
    "output/pros_cons_generated.csv",
    index=False
)

print("=" * 50)
print("Pros / Cons Generator Complete")
print("=" * 50)
print("Companies :", df["company_id"].nunique())
print("Generated :", len(output))