import pandas as pd


def calculate_percentile(df, metric, ascending=True):
    """
    Calculate percentile rank for one metric.
    """

    rank = df[metric].rank(
        pct=True,
        ascending=ascending
    )

    return rank * 100