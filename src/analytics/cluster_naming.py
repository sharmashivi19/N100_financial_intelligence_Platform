import pandas as pd

df = pd.read_csv("output/cluster_labels.csv")

cluster_names = {
    0: "High Quality Compounders",
    1: "Emerging Growth",
    2: "Value Cyclicals",
    3: "Defensive Dividend Payers",
    4: "Turnaround Opportunities"
}

df["cluster_name"] = df["cluster_id"].map(cluster_names)

df.to_csv(
    "output/cluster_labels.csv",
    index=False
)

print("=" * 50)
print("Cluster Names Updated")
print("=" * 50)
print(df.head())