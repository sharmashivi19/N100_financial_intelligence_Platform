import pandas as pd


def create_failure(
        rule_id,
        severity,
        table,
        column,
        message
):

    return {
        "rule_id": rule_id,
        "severity": severity,
        "table": table,
        "column": column,
        "message": message
    }
def check_missing_primary_key(df, table, column):

    failures=[]

    rows = df[df[column].isna()]

    for index in rows.index:

        failures.append(
            create_failure(
                "DQ-01",
                "CRITICAL",
                table,
                column,
                "Primary key missing"
            )
        )

    return failures
def check_duplicate_primary_key(
        df,
        table,
        column
):

    failures=[]


    rows=df[
        df[column].duplicated()
    ]


    for index in rows.index:

        failures.append(
            create_failure(
                "DQ-02",
                "CRITICAL",
                table,
                column,
                "Duplicate primary key"
            )
        )


    return failures
def check_required_columns(
        df,
        table,
        columns
):

    failures=[]


    for col in columns:

        if col not in df.columns:

            failures.append(
                create_failure(
                    "DQ-03",
                    "CRITICAL",
                    table,
                    col,
                    "Required column missing"
                )
            )


    return failures
def check_foreign_key(
        child_df,
        parent_df,
        column,
        table
):

    failures=[]


    valid_ids=set(
        parent_df[column]
    )


    invalid=child_df[
        ~child_df[column].isin(valid_ids)
    ]


    for index in invalid.index:

        failures.append(
            create_failure(
                "DQ-04",
                "CRITICAL",
                table,
                column,
                "Invalid foreign key"
            )
        )


    return failures
def check_negative_sales(df):

    failures=[]


    rows=df[
        df["sales"] < 0
    ]


    for index in rows.index:

        failures.append(
            create_failure(
                "DQ-10",
                "WARNING",
                "financials",
                "sales",
                "Negative sales value"
            )
        )


    return failures
def check_opm(df):

    failures=[]


    for index,row in df.iterrows():

        calculated = (
            row["operating_profit"]
            /
            row["sales"]
        )*100


        if abs(calculated-row["opm"]) > 1:

            failures.append(
                create_failure(
                    "DQ-11",
                    "WARNING",
                    "financials",
                    "opm",
                    "Incorrect OPM"
                )
            )


    return failures
def check_balance(df):

    failures=[]


    for index,row in df.iterrows():

        if row["assets"] != (
            row["liabilities"]
            +
            row["equity"]
        ):

            failures.append(
                create_failure(
                    "DQ-12",
                    "WARNING",
                    "balance_sheet",
                    "balance",
                    "Balance mismatch"
                )
            )


    return failures
def check_datatype(
        df,
        column,
        expected_type,
        table
):

    failures=[]

    for index,value in df[column].items():

        if not isinstance(value, expected_type):

            failures.append(
                create_failure(
                    "DQ-05",
                    "CRITICAL",
                    table,
                    column,
                    "Invalid data type"
                )
            )

    return failures
def check_duplicate_records(
        df,
        table
):

    failures=[]


    duplicates=df[
        df.duplicated()
    ]


    for index in duplicates.index:

        failures.append(
            create_failure(
                "DQ-06",
                "WARNING",
                table,
                "",
                "Duplicate record found"
            )
        )


    return failures
import re


def check_ticker(
        df,
        column,
        table
):

    failures=[]


    for index,value in df[column].items():

        if not re.match(
            "^[A-Z]+$",
            str(value)
        ):

            failures.append(
                create_failure(
                    "DQ-07",
                    "WARNING",
                    table,
                    column,
                    "Invalid ticker"
                )
            )


    return failures
def check_year(df, column, table):

    failures = []

    for value in df[column]:

        # Check empty year
        if pd.isna(value):

            failures.append(
                create_failure(
                    "DQ-08",
                    "WARNING",
                    table,
                    column,
                    "Year missing"
                )
            )

            continue


        # Convert safely
        year = int(value)


        if year < 2000 or year > 2100:

            failures.append(
                create_failure(
                    "DQ-08",
                    "WARNING",
                    table,
                    column,
                    "Invalid year"
                )
            )


    return failures
def check_company_name(
        df,
        column,
        table
):

    failures=[]


    rows=df[
        df[column].isna()
    ]


    for index in rows.index:

        failures.append(
            create_failure(
                "DQ-09",
                "CRITICAL",
                table,
                column,
                "Company data missing"
            )
        )


    return failures
def check_profit(
        df,
        table
):

    failures=[]


    for index,row in df.iterrows():

        calculated = (
            row["revenue"]
            -
            row["expense"]
        )


        if calculated != row["profit"]:

            failures.append(
                create_failure(
                    "DQ-13",
                    "WARNING",
                    table,
                    "profit",
                    "Profit calculation mismatch"
                )
            )


    return failures
def check_period(
        df,
        column,
        table
):

    failures=[]


    rows=df[
        df[column].isna()
    ]


    for index in rows.index:

        failures.append(
            create_failure(
                "DQ-14",
                "WARNING",
                table,
                column,
                "Financial period missing"
            )
        )


    return failures
def check_currency(
        df,
        column,
        table
):

    failures=[]

    allowed=[
        "INR",
        "USD",
        "EUR"
    ]


    for index,value in df[column].items():

        if value not in allowed:

            failures.append(
                create_failure(
                    "DQ-15",
                    "WARNING",
                    table,
                    column,
                    "Invalid currency"
                )
            )


    return failures
def check_outlier(
        df,
        column,
        table
):

    failures=[]


    mean=df[column].mean()

    limit=mean*5


    rows=df[
        df[column] > limit
    ]


    for index in rows.index:

        failures.append(
            create_failure(
                "DQ-16",
                "WARNING",
                table,
                column,
                "Outlier value detected"
            )
        )


    return failures
def save_failures(failures):

    df=pd.DataFrame(failures)

    df.to_csv(
        "data/validation_failures.csv",
        index=False
    )