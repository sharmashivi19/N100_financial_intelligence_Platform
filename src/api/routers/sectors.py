from fastapi import APIRouter
import sqlite3

router = APIRouter()

DATABASE = "database/nifty100.db"


@router.get("/sectors")
def get_sectors():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    query = """
    SELECT
        broad_sector,
        COUNT(company_id) AS total_companies
    FROM sector
    GROUP BY broad_sector
    ORDER BY broad_sector
    """

    rows = conn.execute(query).fetchall()

    conn.close()

    return {
        "count": len(rows),
        "sectors": [dict(row) for row in rows]
    }


@router.get("/sectors/{sector_name}")
def sector_companies(sector_name: str):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    query = """
    SELECT
        c.id AS company_id,
        c.company_name,
        s.broad_sector
    FROM companies c
    JOIN sector s
        ON c.id = s.company_id
    WHERE s.broad_sector = ?
    ORDER BY c.company_name
    """

    rows = conn.execute(query, (sector_name,)).fetchall()

    conn.close()

    return {
        "sector": sector_name,
        "count": len(rows),
        "companies": [dict(row) for row in rows]
    }