from fastapi import APIRouter
import sqlite3

router = APIRouter()

DATABASE = "database/nifty100.db"


@router.get("/companies")
def get_companies():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            company_name
        FROM companies
        ORDER BY company_name
    """)

    companies = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        "count": len(companies),
        "companies": companies
    }


@router.get("/companies/{company_id}")
def get_company(company_id: str):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM companies
        WHERE id = ?
    """, (company_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return {
            "status": "error",
            "message": "Company not found"
        }

    return dict(row)