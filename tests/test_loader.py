import pytest

from src.ingestion.loader import (
    normalize_year,
    normalize_ticker,
    load_excel
)


# -------------------
# YEAR TESTS
# -------------------

def test_year_two_digit():
    assert normalize_year("24")==2024


def test_year_four_digit():
    assert normalize_year("2025")==2025


def test_year_spaces():
    assert normalize_year(" 24 ")==2024


def test_year_integer():
    assert normalize_year(2024)==2024


def test_year_none():
    assert normalize_year(None)==None


def test_year_empty():
    assert normalize_year("") is None


# -------------------
# TICKER TESTS
# -------------------

def test_lowercase_ticker():
    assert normalize_ticker("tcs")=="TCS"


def test_uppercase_ticker():
    assert normalize_ticker("INFY")=="INFY"


def test_ticker_spaces():
    assert normalize_ticker(" infy ")=="INFY"


def test_ticker_none():
    assert normalize_ticker(None)==None


def test_remove_internal_space():
    assert normalize_ticker("RE LIANCE")=="RELIANCE"


def test_numeric_ticker():
    assert normalize_ticker(123)=="123"