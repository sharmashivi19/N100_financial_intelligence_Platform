from src.analytics.ratios import *


# -------------------------
# Net Profit Margin
# -------------------------

def test_npm_normal():

    assert net_profit_margin(
        100,
        1000
    ) == 10



def test_npm_zero_sales():

    assert net_profit_margin(
        100,
        0
    ) is None



# -------------------------
# OPM
# -------------------------

def test_opm_normal():

    assert operating_profit_margin(
        200,
        1000
    ) == 20



def test_opm_mismatch():

    value = operating_profit_margin(
        200,
        1000,
        30
    )

    assert value == 20



# -------------------------
# ROE
# -------------------------

def test_roe_normal():

    assert return_on_equity(
        100,
        500,
        500
    ) == 10



def test_negative_equity():

    assert return_on_equity(
        100,
        -500,
        0
    ) is None



# -------------------------
# ROA
# -------------------------

def test_roa_zero_assets():

    assert return_on_assets(
        100,
        0
    ) is None
def test_roa_normal():

    assert return_on_assets(
        200,
        1000
    ) == 20