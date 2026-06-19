import pandas as pd


df = pd.read_csv(
    "data/validation_failures.csv"
)


critical = df[
    df["severity"]=="CRITICAL"
]


if len(critical)==0:
    print("PASS: No CRITICAL failures")
else:
    print("CRITICAL failures found:")
    print(critical)