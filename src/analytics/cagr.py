def calculate_cagr(start, end, years):
    """
    CAGR calculator with edge case handling

    Returns:
    {
        "value": CAGR percentage,
        "flag": status
    }
    """

    # insufficient years
    if years <= 0:
        return {
            "value": None,
            "flag": "INSUFFICIENT"
        }


    # zero starting value
    if start == 0:
        return {
            "value": None,
            "flag": "ZERO_BASE"
        }


    # positive to positive
    if start > 0 and end > 0:

        cagr = (
            (end / start) ** (1 / years)
            - 1
        ) * 100


        return {
            "value": round(cagr,2),
            "flag": None
        }


    # positive to negative
    if start > 0 and end < 0:

        return {
            "value": None,
            "flag": "DECLINE_TO_LOSS"
        }


    # negative to positive
    if start < 0 and end > 0:

        return {
            "value": None,
            "flag": "TURNAROUND"
        }


    # negative to negative
    if start < 0 and end < 0:

        return {
            "value": None,
            "flag": "BOTH_NEGATIVE"
        }


    return {
        "value": None,
        "flag": "INSUFFICIENT"
    }
def revenue_cagr(start, end, years):

    return calculate_cagr(
        start,
        end,
        years
    )



def pat_cagr(start, end, years):

    return calculate_cagr(
        start,
        end,
        years
    )



def eps_cagr(start, end, years):

    return calculate_cagr(
        start,
        end,
        years
    )