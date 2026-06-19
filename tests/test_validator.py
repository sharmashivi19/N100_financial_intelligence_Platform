import pandas as pd

from src.validation.validator import *


def test_missing_primary_key():

    df = pd.DataFrame({
        "company_id":[1,None]
    })

    result = check_missing_primary_key(
        df,
        "financials",
        "company_id"
    )

    assert len(result) == 1



def test_duplicate_primary_key():

    df = pd.DataFrame({
        "company_id":[1,1]
    })

    result = check_duplicate_primary_key(
        df,
        "financials",
        "company_id"
    )

    assert len(result) == 1



def test_negative_sales():

    df = pd.DataFrame({
        "sales":[100,-50]
    })

    result = check_negative_sales(df)

    assert len(result)==1



def test_currency():

    df=pd.DataFrame({
        "currency":["INR","ABC"]
    })


    result=check_currency(
        df,
        "currency",
        "financials"
    )


    assert len(result)==1