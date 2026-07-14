import sqlite3
import pandas as pd
import streamlit as st

DATABASE = "database/nifty100.db"


def get_connection():
    return sqlite3.connect(DATABASE)


# ---------------------------------------------------
# Companies
# ---------------------------------------------------

@st.cache_data(ttl=600)
def get_companies():
    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    conn.close()
    return df


# ---------------------------------------------------
# Financial Ratios
# ---------------------------------------------------

@st.cache_data(ttl=600)
def get_ratios(ticker=None, year=None):

    conn = get_connection()

    query = "SELECT * FROM financial_ratios"

    conditions = []

    if ticker is not None:
        conditions.append(f"company_id='{ticker}'")

    if year is not None:
        conditions.append(f"year='{year}'")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# ---------------------------------------------------
# Profit & Loss
# ---------------------------------------------------

@st.cache_data(ttl=600)
def get_pl(ticker):

    conn = get_connection()

    df = pd.read_sql(
        f"""
        SELECT *
        FROM financials
        WHERE company_id='{ticker}'
        """,
        conn
    )

    conn.close()

    return df


# ---------------------------------------------------
# Balance Sheet
# ---------------------------------------------------

@st.cache_data(ttl=600)
def get_bs(ticker):

    conn = get_connection()

    df = pd.read_sql(
        f"""
        SELECT *
        FROM balance_sheet
        WHERE company_id='{ticker}'
        """,
        conn
    )

    conn.close()

    return df


# ---------------------------------------------------
# Cash Flow
# ---------------------------------------------------

@st.cache_data(ttl=600)
def get_cf(ticker):

    conn = get_connection()

    df = pd.read_sql(
        f"""
        SELECT *
        FROM cash_flow
        WHERE company_id='{ticker}'
        """,
        conn
    )

    conn.close()

    return df


# ---------------------------------------------------
# Financials (All Companies)
# ---------------------------------------------------

@st.cache_data(ttl=600)
def get_financials():

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM financials",
        conn
    )

    conn.close()

    return df


# ---------------------------------------------------
# Peer Groups
# ---------------------------------------------------

@st.cache_data(ttl=600)
def get_sectors():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT DISTINCT peer_group_name
        FROM peer_percentiles
        """,
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_peers(group_name):

    conn = get_connection()

    df = pd.read_sql(
        f"""
        SELECT *
        FROM peer_percentiles
        WHERE peer_group_name='{group_name}'
        """,
        conn
    )

    conn.close()

    return df


# ---------------------------------------------------
# Valuation
# ---------------------------------------------------

@st.cache_data(ttl=600)
def get_valuation(ticker):

    conn = get_connection()

    df = pd.read_sql(
        f"""
        SELECT *
        FROM financial_ratios
        WHERE company_id='{ticker}'
        """,
        conn
    )

    conn.close()

    return df