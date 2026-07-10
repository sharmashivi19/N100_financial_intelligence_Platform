import pandas as pd


def normalize(series):

    p10 = series.quantile(0.10)
    p90 = series.quantile(0.90)

    clipped = series.clip(p10, p90)

    minimum = clipped.min()
    maximum = clipped.max()

    if maximum == minimum:
        return pd.Series(50, index=series.index)

    return ((clipped - minimum) /
            (maximum - minimum)) * 100
def profitability_score(df):

    roe = normalize(df["return_on_equity_pct"])

    npm = normalize(df["net_profit_margin_pct"])

    roce = normalize(df["operating_profit_margin_pct"])

    return (

        roe * 0.15 +

        roce * 0.10 +

        npm * 0.10

    )
def cash_quality_score(df):

    fcf = normalize(
        df["free_cash_flow_cr"].fillna(0)
    )

    return (
        fcf * 0.15
        + fcf * 0.10
        + fcf * 0.05
    )
def growth_score(df):

    revenue = normalize(
        df["revenue_cagr_5yr"].fillna(0)
    )

    pat = normalize(
        df["pat_cagr_5yr"].fillna(0)
    )

    return (
        revenue * 0.10
        + pat * 0.10
    )
def leverage_score(df):

    debt = normalize(
        -df["debt_to_equity"].fillna(0)
    )

    icr = normalize(
        df["interest_coverage"].fillna(0)
    )

    return (
        debt * 0.10
        + icr * 0.05
    )
def calculate_composite_score(df):

    df = df.copy()

    profit = profitability_score(df).fillna(0)

    cash = cash_quality_score(df).fillna(0)

    growth = growth_score(df).fillna(0)

    leverage = leverage_score(df).fillna(0)

    df["composite_score"] = (
        profit
        + cash
        + growth
        + leverage
    )

    return df