import yaml
import pandas as pd


def load_config():

    with open("config/presets.yaml", "r") as f:
        return yaml.safe_load(f)


def apply_filters(df, config):

    result = df.copy()

    print("Initial rows:", len(result))

    if "roe_min" in config:
        result = result[
            result["return_on_equity_pct"] >= config["roe_min"]
        ]
        print("After ROE:", len(result))

    if "de_max" in config:
        result = result[
            result["debt_to_equity"] <= config["de_max"]
        ]
        print("After D/E:", len(result))

    if "fcf_min" in config:
        result = result[
            result["free_cash_flow_cr"] >= config["fcf_min"]
        ]
        print("After FCF:", len(result))

    if "revenue_cagr_5yr_min" in config:
        result = result[
            result["revenue_cagr_5yr"] >= config["revenue_cagr_5yr_min"]
        ]
        print("After Revenue CAGR:", len(result))

    if "pat_cagr_5yr_min" in config:
        result = result[
            result["pat_cagr_5yr"] >= config["pat_cagr_5yr_min"]
        ]
        print("After PAT CAGR:", len(result))

    if "opm_min" in config:
        result = result[
            result["operating_profit_margin_pct"] >= config["opm_min"]
        ]
        print("After OPM:", len(result))

    if "asset_turnover_min" in config:
        result = result[
            result["asset_turnover"] >= config["asset_turnover_min"]
        ]
        print("After Asset Turnover:", len(result))

    if "icr_min" in config:
        result = result[
            result["interest_coverage"].fillna(float("inf"))
            >= config["icr_min"]
        ]
        print("After ICR:", len(result))

    if "dividend_payout_ratio_pct_max" in config:
        result = result[
            result["dividend_payout_ratio_pct"]
            <= config["dividend_payout_ratio_pct_max"]
        ]
        print("After Dividend Payout:", len(result))

    result = result.sort_values(
        "composite_quality_score",
        ascending=False
    )

    return result