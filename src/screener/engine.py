import yaml
import pandas as pd


def load_config():
    with open("config/screener_config.yaml", "r") as file:
        return yaml.safe_load(file)


def apply_filters(df):
    config = load_config()

    result = df.copy()
    print("Initial rows:", len(result))

    # ROE filter
    result = result[
        result["return_on_equity_pct"] >= config["roe_min"]
    ]
    print("After ROE filter:", len(result))

    # Debt to Equity filter
    result = result[
        result["debt_to_equity"] <= config["de_max"]
    ]
    print("After D/E filter:", len(result))

    # Free Cash Flow filter
    result = result[
        result["free_cash_flow_cr"] >= config["fcf_min"]
    ]
    print("After FCF filter:", len(result))

    # Revenue CAGR filter
    result = result[
        result["revenue_cagr_5yr"] >= config["revenue_cagr_5yr_min"]
    ]
    print("After Revenue CAGR filter:", len(result))

    # PAT CAGR filter
    result = result[
        result["pat_cagr_5yr"] >= config["pat_cagr_5yr_min"]
    ]
    print("After PAT CAGR filter:", len(result))

    # Operating Profit Margin filter
    result = result[
        result["operating_profit_margin_pct"] >= config["opm_min"]
    ]
    print("After OPM filter:", len(result))

    # Asset Turnover filter
    result = result[
        result["asset_turnover"] >= config["asset_turnover_min"]
    ]
    print("After Asset Turnover filter:", len(result))

    # Interest Coverage filter
    result = result[
        result["interest_coverage"].fillna(float("inf")) >= config["icr_min"]
    ]
    print("After ICR filter:", len(result))

    result = result.sort_values(
        by="composite_quality_score",
        ascending=False
    )

    return result