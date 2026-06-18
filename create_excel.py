import pandas as pd


data = {
    "ticker":[
        "tcs",
        " infy ",
        "reliance"
    ],

    "year":[
        "24",
        "2023",
        "25"
    ]
}


df = pd.DataFrame(data)


df.to_excel(
    "data/raw/sample.xlsx",
    index=False
)


print("Excel created")