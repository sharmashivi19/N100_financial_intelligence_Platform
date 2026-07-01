from src.analytics.cagr import *



def test_normal_cagr():

    result = calculate_cagr(
        100,
        200,
        5
    )

    assert result["flag"] is None



def test_decline_to_loss():

    result = calculate_cagr(
        100,
        -50,
        5
    )

    assert result["flag"] == "DECLINE_TO_LOSS"



def test_turnaround():

    result = calculate_cagr(
        -100,
        200,
        5
    )

    assert result["flag"] == "TURNAROUND"



def test_both_negative():

    result = calculate_cagr(
        -100,
        -200,
        5
    )

    assert result["flag"] == "BOTH_NEGATIVE"



def test_zero_base():

    result = calculate_cagr(
        0,
        200,
        5
    )

    assert result["flag"] == "ZERO_BASE"



def test_insufficient_years():

    result = calculate_cagr(
        100,
        200,
        0
    )

    assert result["flag"] == "INSUFFICIENT"



def test_revenue_cagr():

    result = revenue_cagr(
        100,
        150,
        5
    )

    assert result["value"] > 0



def test_pat_cagr():

    result = pat_cagr(
        200,
        400,
        5
    )

    assert result["value"] > 0



def test_eps_cagr():

    result = eps_cagr(
        10,
        20,
        5
    )

    assert result["value"] > 0



def test_negative_eps():

    result = eps_cagr(
        -10,
        20,
        5
    )

    assert result["flag"] == "TURNAROUND"