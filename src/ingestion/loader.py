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
import pandas as pd
import sqlite3
import os


def get_connection():

    conn = sqlite3.connect(
        "database/nifty100.db"
    )

    # Enable foreign key checking
    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn



def load_excel(file_path, table_name):

    print("\nOpening file:", file_path)


    # Check file exists
    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )


    # Check file size
    file_size = os.path.getsize(file_path)

    if file_size == 0:

        raise Exception(
            f"File is empty: {file_path}"
        )


    # Read CSV files
    if file_path.lower().endswith(".csv"):

        print("Reading CSV file")

        df = pd.read_csv(
            file_path
        )


    # Read Excel files
    elif file_path.lower().endswith(".xlsx"):

        print("Reading Excel file")

        try:

         df = pd.read_excel(
    file_path,
    engine="openpyxl",
    header=1
)

        except Exception as e:

            print(
                "Excel reading failed:",
                e
            )

            raise


    else:

        raise Exception(
            f"Unsupported file type: {file_path}"
        )


    print(
        "Rows loaded:",
        len(df)
    )


    # Connect database

    conn = get_connection()


    try:

        df.to_sql(
            table_name,
            conn,
            if_exists="append",
            index=False
        )


    except Exception as e:

        print(
            "Database insert failed:",
            e
        )

        raise


    finally:

        conn.close()


    return len(df)
