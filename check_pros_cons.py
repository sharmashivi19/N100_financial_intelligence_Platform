import pandas as pd

df = pd.read_csv("output/pros_cons_generated.csv")

summary = (
    df.groupby(["company_id", "type"])
      .size()
      .unstack(fill_value=0)
)

summary["has_pro"] = summary["pro"] > 0
summary["has_con"] = summary["con"] > 0

print(summary.head())

print("\nCompanies missing Pro:")
print((~summary["has_pro"]).sum())

print("\nCompanies missing Con:")
print((~summary["has_con"]).sum())