from fastapi import APIRouter
import sqlite3
import pandas as pd

router = APIRouter()

DATABASE = "database/nifty100.db"


@router.get("/portfolio")
def portfolio_summary():

    conn = sqlite3.connect(DATABASE)

    companies = pd.read_sql("""
        SELECT
            id,
            company_name
        FROM companies
        ORDER BY company_name
    """, conn)

    sector = pd.read_sql("""
        SELECT
            company_id,
            broad_sector
        FROM sector
    """, conn)

    ratios = pd.read_sql("""
        SELECT
            company_id,
            year,
            return_on_equity_pct,
            debt_to_equity,
            operating_profit_margin_pct,
            revenue_cagr_5yr
        FROM financial_ratios
    """, conn)

    conn.close()

    # Latest ratios for each company
    ratios = (
        ratios
        .sort_values("year")
        .groupby("company_id", as_index=False)
        .last()
    )

    companies = companies.rename(columns={"id": "company_id"})

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

    return {
        "count": len(df),
        "portfolio": df.fillna("").to_dict(orient="records")
    }


@router.get("/portfolio/stats")
def portfolio_stats():

    conn = sqlite3.connect(DATABASE)

    ratios = pd.read_sql("""
        SELECT
            return_on_equity_pct,
            debt_to_equity,
            operating_profit_margin_pct,
            revenue_cagr_5yr
        FROM financial_ratios
    """, conn)

    conn.close()

    stats = {
        "roe_mean": float(ratios["return_on_equity_pct"].mean()),
        "roe_median": float(ratios["return_on_equity_pct"].median()),
        "debt_equity_mean": float(ratios["debt_to_equity"].mean()),
        "opm_mean": float(ratios["operating_profit_margin_pct"].mean()),
        "revenue_cagr_mean": float(ratios["revenue_cagr_5yr"].mean())
    }

    return stats