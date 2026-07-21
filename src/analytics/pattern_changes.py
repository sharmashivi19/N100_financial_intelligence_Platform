import pandas as pd

capital = pd.read_csv("output/capital_allocation.csv")

capital = capital.sort_values(
    ["company_id", "year"]
)

changes = []

for company, grp in capital.groupby("company_id"):

    grp = grp.reset_index(drop=True)

    for i in range(1, len(grp)):

        old = grp.loc[i-1, "pattern_label"]
        new = grp.loc[i, "pattern_label"]

        if old != new:

            changes.append({

                "company_id": company,

                "from_pattern": old,

                "to_pattern": new,

                "year": grp.loc[i, "year"]

            })

changes = pd.DataFrame(changes)

changes.to_csv(
    "output/pattern_changes.csv",
    index=False
)

print("Pattern Changes:", len(changes))