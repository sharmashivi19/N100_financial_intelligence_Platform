import pandas as pd

from src.validation.validator import *


df=pd.read_csv(
    "data/test_financials.csv"
)


failures=[]


failures += check_missing_primary_key(
    df,
    "financials",
    "company_id"
)


failures += check_duplicate_primary_key(
    df,
    "financials",
    "company_id"
)


failures += check_required_columns(
    df,
    "financials",
    [
        "company_id",
        "ticker",
        "sales"
    ]
)


failures += check_duplicate_records(
    df,
    "financials"
)


failures += check_ticker(
    df,
    "ticker",
    "financials"
)


failures += check_year(
    df,
    "year",
    "financials"
)


failures += check_company_name(
    df,
    "company_id",
    "financials"
)


failures += check_negative_sales(df)

failures += check_opm(df)
failures += check_balance(
    df
)

failures += check_profit(
    df,
    "financials"
)

failures += check_period(
    df,
    "year",
    "financials"
)


failures += check_currency(
    df,
    "currency",
    "financials"
)


failures += check_outlier(
    df,
    "sales",
    "financials"
)


save_failures(
    failures
)


print(
    "Validation completed"
)