from fastapi import APIRouter
import sqlite3

router = APIRouter()

DATABASE = "database/nifty100.db"


@router.get("/peers/{company_id}")
def get_peers(company_id: str):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    # ----------------------------------------
    # Find company's sector
    # ----------------------------------------

    cursor.execute("""
        SELECT broad_sector
        FROM sector
        WHERE company_id = ?
    """, (company_id,))

    sector = cursor.fetchone()

    if sector is None:
        conn.close()
        return {
            "status": "error",
            "message": "Company not found"
        }

    sector_name = sector["broad_sector"]

    # ----------------------------------------
    # Get peer companies
    # ----------------------------------------

    cursor.execute("""
        SELECT
            c.id AS company_id,
            c.company_name,
            s.broad_sector
        FROM companies c
        JOIN sector s
            ON c.id = s.company_id
        WHERE s.broad_sector = ?
          AND c.id != ?
        ORDER BY c.company_name
    """, (sector_name, company_id))

    peers = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        "company": company_id,
        "sector": sector_name,
        "peer_count": len(peers),
        "peers": peers
    }