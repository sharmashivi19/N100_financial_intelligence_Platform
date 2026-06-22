import pandas as pd
from pathlib import Path


def load_excel(file_path):
    """
    Load Excel file into DataFrame
    """

    file = Path(file_path)

    if not file.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    return pd.read_excel(file)



def normalize_year(year):
    """
    Convert year values into YYYY format
    """

    if year is None:
        return None

    year = str(year).strip()

    if year == "":
        return None

    if len(year) == 2:
        year = "20" + year

    return int(year)


def normalize_ticker(ticker):
    """
    Normalize stock ticker symbols
    """

    if pd.isna(ticker):
        return None


    ticker = str(ticker)

    ticker = ticker.strip()

    ticker = ticker.upper()

    ticker = ticker.replace(
        " ",
        ""
    )
    return ticker
import sqlite3


def get_connection():

    conn = sqlite3.connect(
        "database/nifty100.db"
    )


    conn.execute(
        "PRAGMA foreign_keys = ON"
    )


    return conn