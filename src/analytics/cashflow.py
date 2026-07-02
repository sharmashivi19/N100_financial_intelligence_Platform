def free_cash_flow(operating_activity, investing_activity):
    return operating_activity + investing_activity
def cfo_quality_score(cfo, pat):

    if pat == 0:
        return None

    ratio = cfo / pat

    if ratio > 1:
        return "High Quality"

    elif ratio >= 0.5:
        return "Moderate"

    else:
        return "Accrual Risk"
def capex_intensity(investing_activity, sales):

    if sales == 0:
        return None

    ratio = abs(investing_activity) / sales * 100

    if ratio < 3:
        label = "Asset Light"

    elif ratio <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return ratio, label
def fcf_conversion_rate(fcf, operating_profit):

    if operating_profit == 0:
        return None

    return (fcf / operating_profit) * 100
def sign(value):

    if value > 0:
        return "+"

    elif value < 0:
        return "-"

    return "0"
def capital_allocation_pattern(
        cfo,
        cfi,
        cff,
        cfo_pat_ratio=None
):

    s = (
        sign(cfo),
        sign(cfi),
        sign(cff)
    )


    if s == ("+", "-", "-"):

        if (
            cfo_pat_ratio is not None
            and cfo_pat_ratio > 1
        ):
            return "Shareholder Returns"

        return "Reinvestor"


    if s == ("+", "+", "-"):
        return "Liquidating Assets"


    if s == ("-", "+", "+"):
        return "Distress Signal"


    if s == ("-", "-", "+"):
        return "Growth Funded by Debt"


    if s == ("+", "+", "+"):
        return "Cash Accumulator"


    if s == ("-", "-", "-"):
        return "Pre-Revenue"


    if s == ("+", "-", "+"):
        return "Mixed"


    return "Unknown"