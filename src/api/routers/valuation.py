from fastapi import APIRouter
import sqlite3

router = APIRouter()

DATABASE = "database/nifty100.db"


@router.get("/valuation/{company_id}")
def get_valuation(company_id: str):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    query = """
    SELECT
        c.id AS company_id,
        c.company_name,
        c.face_value,
        c.book_value,
        c.roce_percentage,
        c.roe_percentage,
        fr.earnings_per_share,
        fr.book_value_per_share
    FROM companies c
    LEFT JOIN financial_ratios fr
        ON c.id = fr.company_id
    WHERE c.id = ?
    ORDER BY fr.year DESC
    LIMIT 1
    """

    cursor.execute(query, (company_id,))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return {
            "status": "error",
            "message": "Company not found"
        }

    return dict(row)


@router.get("/valuation")
def valuation_summary():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    query = """
    SELECT
        c.id AS company_id,
        c.company_name,
        c.face_value,
        c.book_value,
        c.roce_percentage,
        c.roe_percentage
    FROM companies c
    ORDER BY c.company_name
    """

    rows = cursor.execute(query).fetchall()

    conn.close()

    return {
        "count": len(rows),
        "companies": [dict(r) for r in rows]
    }