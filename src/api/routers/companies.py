from fastapi import APIRouter, HTTPException, Query
import sqlite3
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
import sqlite3
import pandas as pd

router = APIRouter(tags=["Companies"])


def get_db():
    return sqlite3.connect("database/nifty100.db")


@router.get("/companies")
def get_companies(
    sector: str = None,
    market_cap_category: str = None,
    search: str = None,
):

    conn = get_db()

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,
        s.sub_sector,
        s.market_cap_category,
        c.roe_percentage,
        c.roce_percentage
    FROM companies c
    LEFT JOIN sector s
        ON c.id = s.company_id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    # ----------------------------
    # Filter by sector
    # ----------------------------

    if sector:

        df = df[
            df["broad_sector"].str.contains(
                sector,
                case=False,
                na=False
            )
        ]

    # ----------------------------
    # Filter by market cap
    # ----------------------------

    if market_cap_category:

        df = df[
            df["market_cap_category"].str.contains(
                market_cap_category,
                case=False,
                na=False
            )
        ]

    # ----------------------------
    # Search company or ticker
    # ----------------------------

    if search:

        df = df[
            df["company_name"].str.contains(
                search,
                case=False,
                na=False
            )
            |
            df["id"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    return df.to_dict(
        orient="records"
    )
@router.get("/companies/{ticker}")
def get_company(ticker: str):

    conn = sqlite3.connect("database/nifty100.db")
    conn.row_factory = sqlite3.Row

    # -----------------------------
    # Company
    # -----------------------------

    company = conn.execute(
        """
        SELECT *
        FROM companies
        WHERE id = ?
        """,
        (ticker,)
    ).fetchone()

    if company is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    # -----------------------------
    # Sector
    # -----------------------------

    sector = conn.execute(
        """
        SELECT *
        FROM sector
        WHERE company_id = ?
        """,
        (ticker,)
    ).fetchone()

    # -----------------------------
    # Latest Financials
    # -----------------------------

    financials = conn.execute(
        """
        SELECT *
        FROM financials
        WHERE company_id = ?
        ORDER BY year DESC
        LIMIT 1
        """,
        (ticker,)
    ).fetchone()

    # -----------------------------
    # Latest Ratios
    # -----------------------------

    ratios = conn.execute(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year DESC
        LIMIT 1
        """,
        (ticker,)
    ).fetchone()

    conn.close()

    return {

        "company": dict(company),

        "sector": dict(sector) if sector else None,

        "latest_financials":
            dict(financials) if financials else None,

        "latest_ratios":
            dict(ratios) if ratios else None
    }
@router.get("/companies/{ticker}/pl")
def get_profit_loss(
    ticker: str,
    from_year: str | None = Query(None),
    to_year: str | None = Query(None)
):

    conn = sqlite3.connect("database/nifty100.db")
    conn.row_factory = sqlite3.Row

    query = """
        SELECT *
        FROM financials
        WHERE company_id = ?
    """

    params = [ticker]

    if from_year:
        query += " AND year >= ?"
        params.append(from_year)

    if to_year:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year"

    rows = conn.execute(query, params).fetchall()

    conn.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="No P&L data found"
        )

    return [dict(row) for row in rows]
@router.get("/companies/{ticker}/bs")
def get_balance_sheet(
    ticker: str,
    from_year: str | None = Query(None),
    to_year: str | None = Query(None),
):
    conn = sqlite3.connect("database/nifty100.db")
    conn.row_factory = sqlite3.Row

    query = """
        SELECT *
        FROM balance_sheet
        WHERE company_id = ?
    """

    params = [ticker.upper()]

    if from_year:
        query += " AND year >= ?"
        params.append(from_year)

    if to_year:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year"

    rows = conn.execute(query, params).fetchall()

    conn.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Balance Sheet not found"
        )

    return [dict(r) for r in rows]
@router.get("/companies/{ticker}/cashflow")
def get_cashflow(
    ticker: str,
    from_year: str | None = Query(None),
    to_year: str | None = Query(None),
):
    conn = sqlite3.connect("database/nifty100.db")
    conn.row_factory = sqlite3.Row

    query = """
        SELECT *
        FROM cash_flow
        WHERE company_id = ?
    """

    params = [ticker.upper()]

    if from_year:
        query += " AND year >= ?"
        params.append(from_year)

    if to_year:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year"

    rows = conn.execute(query, params).fetchall()

    conn.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Cash Flow data not found"
        )

    return [dict(row) for row in rows]
@router.get("/companies/{ticker}/ratios")
def get_ratios(
    ticker: str,
    year: str | None = Query(None)
):
    conn = sqlite3.connect("database/nifty100.db")
    conn.row_factory = sqlite3.Row

    query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
    """

    params = [ticker.upper()]

    if year:
        query += " AND year = ?"
        params.append(year)

    query += " ORDER BY year"

    rows = conn.execute(query, params).fetchall()

    conn.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Financial ratios not found"
        )

    return [dict(row) for row in rows]
@router.get("/companies/{ticker}/tearsheet")
def company_tearsheet(ticker: str):

    pdf_path = Path(f"reports/tearsheets/{ticker}.pdf")

    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Tearsheet PDF not found"
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"{ticker}.pdf"
    )
