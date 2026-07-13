import sqlite3
import pandas as pd
import streamlit as st

DATABASE = "database/nifty100.db"


@st.cache_data(ttl=600)
def get_companies():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql("SELECT * FROM companies", conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):
    conn = sqlite3.connect(DATABASE)

    if year is None:
        query = f"""
        SELECT *
        FROM financial_ratios
        WHERE company_id='{ticker}'
        """
    else:
        query = f"""
        SELECT *
        FROM financial_ratios
        WHERE company_id='{ticker}'
        AND year='{year}'
        """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_pl(ticker):
    conn = sqlite3.connect(DATABASE)

    df = pd.read_sql(
        f"SELECT * FROM financials WHERE company_id='{ticker}'",
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_bs(ticker):

    conn = sqlite3.connect(DATABASE)

    df = pd.read_sql(
        f"SELECT * FROM balance_sheet WHERE company_id='{ticker}'",
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_cf(ticker):

    conn = sqlite3.connect(DATABASE)

    df = pd.read_sql(
        f"SELECT * FROM cash_flow WHERE company_id='{ticker}'",
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_sectors():

    conn = sqlite3.connect(DATABASE)

    try:
        df = pd.read_sql(
            "SELECT DISTINCT peer_group_name FROM peer_percentiles",
            conn
        )
    finally:
        conn.close()

    return df


@st.cache_data(ttl=600)
def get_peers(group_name):

    conn = sqlite3.connect(DATABASE)

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


@st.cache_data(ttl=600)
def get_valuation(ticker):

    conn = sqlite3.connect(DATABASE)

    try:
        df = pd.read_sql(
            f"""
            SELECT *
            FROM financial_ratios
            WHERE company_id='{ticker}'
            """,
            conn
        )
    finally:
        conn.close()

    return df