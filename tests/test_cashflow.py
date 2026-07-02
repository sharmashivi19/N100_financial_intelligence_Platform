from src.analytics.cashflow import *


def test_fcf():
    assert free_cash_flow(500, -100) == 400


def test_cfo_quality():
    assert cfo_quality_score(120, 100) == "High Quality"


def test_pat_zero():
    assert cfo_quality_score(100, 0) is None


def test_capex_asset_light():
    ratio, label = capex_intensity(-20, 1000)
    assert label == "Asset Light"


def test_capex_capital_intensive():
    ratio, label = capex_intensity(-200, 1000)
    assert label == "Capital Intensive"


def test_fcf_conversion():
    assert fcf_conversion_rate(300, 600) == 50


def test_reinvestor():
    assert capital_allocation_pattern(100, -50, -20) == "Reinvestor"


def test_distress():
    assert capital_allocation_pattern(-100, 50, 50) == "Distress Signal"


def test_cash_accumulator():
    assert capital_allocation_pattern(100, 20, 30) == "Cash Accumulator"


def test_mixed():
    assert capital_allocation_pattern(100, -30, 50) == "Mixed"