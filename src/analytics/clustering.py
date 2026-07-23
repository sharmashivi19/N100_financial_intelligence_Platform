import sqlite3
from pathlib import Path

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
Path("output").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)
conn = sqlite3.connect("database/nifty100.db")
ratios = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        return_on_equity_pct,
        debt_to_equity,
        revenue_cagr_5yr,
        operating_profit_margin_pct
    FROM financial_ratios
    """,
    conn
)

# Keep only the latest record for each company
ratios = (
    ratios
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)
cashflow = pd.read_excel(
    "output/cashflow_intelligence.xlsx"
)
cashflow = cashflow[
    [
        "company_id",
        "fcf_cagr_5yr"
    ]
]
sector = pd.read_sql(
    """
    SELECT
        company_id,
        broad_sector
    FROM sector
    """,
    conn
)

conn.close()
df = ratios.merge(
    cashflow,
    on="company_id",
    how="left"
)

df = df.merge(
    sector,
    on="company_id",
    how="left"
)
features = [

    "return_on_equity_pct",

    "debt_to_equity",

    "revenue_cagr_5yr",

    "fcf_cagr_5yr",

    "operating_profit_margin_pct"

]
# --------------------------------------------------
# Fill missing values with sector median
# --------------------------------------------------

for col in features:

    df[col] = df.groupby("broad_sector")[col].transform(
        lambda x: x.fillna(x.median())
    )

# --------------------------------------------------
# Fill remaining missing values with overall median
# --------------------------------------------------

for col in features:

    median = df[col].median()

    if pd.isna(median):
        median = 0

    df[col] = df[col].fillna(median)

# --------------------------------------------------
# Final safety check
# --------------------------------------------------

df[features] = df[features].fillna(0)

print("\nMissing values after imputation:")
print(df[features].isna().sum())
scaler = StandardScaler()
print("\nFeature Summary")
print(df[features].describe())
X = scaler.fit_transform(
    df[features]
)
inertia = []

for k in range(2,11):

    model = KMeans(

        n_clusters=k,

        random_state=42,

        n_init=10

    )

    model.fit(X)

    inertia.append(model.inertia_)
plt.figure(figsize=(6,4))

plt.plot(

    range(2,11),

    inertia,

    marker="o"

)

plt.xlabel("Number of Clusters")

plt.ylabel("Inertia")

plt.title("Elbow Plot")

plt.tight_layout()

plt.savefig(
    "reports/elbow_plot.png"
)

plt.close()
kmeans = KMeans(

    n_clusters=5,

    random_state=42,

    n_init=10

)

df["cluster_id"] = kmeans.fit_predict(X)
distance = kmeans.transform(X)

df["distance_from_centroid"] = [

    distance[i][cluster]

    for i, cluster in enumerate(df["cluster_id"])

]
names = {

    0:"Cluster A",

    1:"Cluster B",

    2:"Cluster C",

    3:"Cluster D",

    4:"Cluster E"

}

df["cluster_name"] = df["cluster_id"].map(names)
output = df[

    [

        "company_id",

        "cluster_id",

        "cluster_name",

        "distance_from_centroid"

    ]

]

output.to_csv(

    "output/cluster_labels.csv",

    index=False

)
print("="*50)
print("KMeans Clustering Complete")
print("="*50)
print("Companies :", len(output))
print("Clusters :", output["cluster_id"].nunique())
print("Output : output/cluster_labels.csv")
print("Elbow Plot : reports/elbow_plot.png")
