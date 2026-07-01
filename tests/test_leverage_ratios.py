from src.analytics.ratios import *



def test_debt_equity_normal():

    assert debt_to_equity(
        500,
        500,
        500
    ) == 0.5



def test_debt_free_returns_zero():

    assert debt_to_equity(
        0,
        500,
        500
    ) == 0



def test_negative_equity():

    assert debt_to_equity(
        500,
        -100,
        0
    ) is None



def test_high_debt_flag():

    assert high_leverage_flag(
        6,
        "Technology"
    ) is True



def test_financial_sector_no_flag():

    assert high_leverage_flag(
        6,
        "Financials"
    ) is False



def test_icr_interest_zero():

    assert interest_coverage_ratio(
        100,
        20,
        0
    ) is None



def test_icr_debt_free_label():

    assert icr_label(None) == "Debt Free"



def test_asset_turnover_zero_assets():

    assert asset_turnover(
        1000,
        0
    ) is None