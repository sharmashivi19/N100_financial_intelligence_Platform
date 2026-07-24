from fastapi import APIRouter
import sqlite3

router = APIRouter()

DATABASE = "database/nifty100.db"


@router.get("/screener")
def stock_screener():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    query = """
    SELECT
        c.id AS company_id,
        c.company_name,
        s.broad_sector,
        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.operating_profit_margin_pct,
        fr.revenue_cagr_5yr
    FROM companies c
    LEFT JOIN sector s
        ON c.id = s.company_id
    LEFT JOIN financial_ratios fr
        ON c.id = fr.company_id
    """

    data = conn.execute(query).fetchall()

    conn.close()

    return {
        "count": len(data),
        "results": [dict(row) for row in data]
    }


@router.get("/screener/high-roe")
def high_roe():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    query = """
    SELECT
        c.id AS company_id,
        c.company_name,
        fr.return_on_equity_pct
    FROM companies c
    JOIN financial_ratios fr
        ON c.id = fr.company_id
    WHERE fr.return_on_equity_pct >= 20
    ORDER BY fr.return_on_equity_pct DESC
    """

    data = conn.execute(query).fetchall()

    conn.close()

    return {
        "count": len(data),
        "results": [dict(row) for row in data]
    }