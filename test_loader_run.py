import pytest

from src.ingestion.loader import (
    load_excel,
    normalize_year,
    normalize_ticker
)


# =====================================================
# Test File Configuration
# =====================================================

TEST_FILE = "data/source_files/sample.xlsx"
TEST_TABLE = "companies"


# =====================================================
# normalize_year Tests
# =====================================================

def test_year_with_spaces():
    assert normalize_year(" 24 ") == 2024


def test_year_integer():
    assert normalize_year(2024) == 2024


def test_year_none():
    assert normalize_year(None) is None


def test_year_string():
    assert normalize_year("2025") == 2025


def test_year_99():
    assert normalize_year("99") == 2099


def test_year_00():
    assert normalize_year("00") == 2000


def test_year_with_leading_zero():
    assert normalize_year("01") == 2001



# =====================================================
# normalize_ticker Tests
# =====================================================

def test_ticker_lowercase():
    assert normalize_ticker("tcs") == "TCS"


def test_ticker_uppercase():
    assert normalize_ticker("INFY") == "INFY"


def test_ticker_mixed_case():
    assert normalize_ticker("InFy") == "INFY"


def test_ticker_spaces_before():
    assert normalize_ticker("  TCS") == "TCS"


def test_ticker_spaces_after():
    assert normalize_ticker("TCS  ") == "TCS"


def test_ticker_internal_space():
    assert normalize_ticker("RE LIANCE") == "RELIANCE"


def test_ticker_none_value():
    assert normalize_ticker(None) is None


def test_ticker_number():
    assert normalize_ticker(123) == "123"


def test_ticker_special_character():
    assert normalize_ticker("tcs.") == "TCS."


def test_ticker_empty():
    assert normalize_ticker("") == ""



# =====================================================
# Excel Loader Tests
# =====================================================


def test_excel_file_load():

    import pandas as pd

    df = pd.read_excel(
        TEST_FILE
    )

    assert len(df) > 0



def test_missing_excel_file():

    import pandas as pd

    with pytest.raises(FileNotFoundError):

        pd.read_excel(
            "wrong_file.xlsx"
        )