from fastapi import APIRouter
from pathlib import Path

router = APIRouter()

# Folder locations
TEARSHEETS_DIR = Path("reports/tearsheets")
SECTOR_DIR = Path("reports/sector")
PORTFOLIO_DIR = Path("reports/portfolio")


@router.get("/documents")
def list_documents():

    tearsheets = []
    sector_reports = []
    portfolio_reports = []

    if TEARSHEETS_DIR.exists():
        tearsheets = sorted(
            [f.name for f in TEARSHEETS_DIR.glob("*.pdf")]
        )

    if SECTOR_DIR.exists():
        sector_reports = sorted(
            [f.name for f in SECTOR_DIR.glob("*.pdf")]
        )

    if PORTFOLIO_DIR.exists():
        portfolio_reports = sorted(
            [f.name for f in PORTFOLIO_DIR.glob("*.pdf")]
        )

    return {
        "tearsheets": tearsheets,
        "sector_reports": sector_reports,
        "portfolio_reports": portfolio_reports
    }


@router.get("/documents/summary")
def documents_summary():

    tearsheets = (
        len(list(TEARSHEETS_DIR.glob("*.pdf")))
        if TEARSHEETS_DIR.exists()
        else 0
    )

    sector_reports = (
        len(list(SECTOR_DIR.glob("*.pdf")))
        if SECTOR_DIR.exists()
        else 0
    )

    portfolio_reports = (
        len(list(PORTFOLIO_DIR.glob("*.pdf")))
        if PORTFOLIO_DIR.exists()
        else 0
    )

    return {
        "total_tearsheets": tearsheets,
        "total_sector_reports": sector_reports,
        "total_portfolio_reports": portfolio_reports,
        "total_documents":
            tearsheets
            + sector_reports
            + portfolio_reports
    }