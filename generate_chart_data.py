
import json
import pandas as pd

# Read your dataset from the same folder
df = pd.read_csv("Telco-Customer-Churn.csv")

df = df.drop_duplicates(subset="customerID").copy()
df["tenure"] = pd.to_numeric(df["tenure"], errors="coerce")
df["MonthlyCharges"] = pd.to_numeric(
    df["MonthlyCharges"], errors="coerce"
)
df["Churn"] = df["Churn"].astype(str).str.strip()
df = df.dropna(
    subset=["Contract", "tenure", "MonthlyCharges", "Churn"]
)
df = df[df["Churn"].isin(["Yes", "No"])].copy()

# Group customers by duration
df["TenureGroup"] = "Long-term"
df.loc[df["tenure"] <= 12, "TenureGroup"] = "New"
df.loc[
    (df["tenure"] >= 13) & (df["tenure"] <= 36),
    "TenureGroup"
] = "Existing"

# Group customers by monthly bill
df["ChargeGroup"] = "High"
df.loc[df["MonthlyCharges"] < 35, "ChargeGroup"] = "Low"
df.loc[
    (df["MonthlyCharges"] >= 35)
    & (df["MonthlyCharges"] < 70),
    "ChargeGroup"
] = "Medium"


def summarize(column, groups):
    result = []

    for group_name in groups:
        subset = df[df[column] == group_name]
        total = len(subset)
        churned = int((subset["Churn"] == "Yes").sum())
        retained = int((subset["Churn"] == "No").sum())

        result.append({
            "key": group_name,
            "label": group_name,
            "customers": total,
            "churned": churned,
            "retained": retained,
            "churnRate": round(
                churned / total * 100, 2
            ) if total else 0
        })

    return result


total = len(df)
churned = int((df["Churn"] == "Yes").sum())
retained = int((df["Churn"] == "No").sum())

data = {
    "totalCustomers": total,
    "churnedCustomers": churned,
    "retainedCustomers": retained,
    "overallChurnRate": round(
        churned / total * 100, 2
    ) if total else 0,

    "contract": summarize(
        "Contract", ["Month-to-month", "One year", "Two year"]
    ),
    "tenure": summarize(
        "TenureGroup", ["New", "Existing", "Long-term"]
    ),
    "charges": summarize(
        "ChargeGroup", ["Low", "Medium", "High"]
    ),
    "monthlyChargesByChurn": {
        "No": df.loc[
            df["Churn"] == "No", "MonthlyCharges"
        ].round(2).tolist(),
        "Yes": df.loc[
            df["Churn"] == "Yes", "MonthlyCharges"
        ].round(2).tolist()
    }
}

# Save JSON beside this Python file
with open("chart_data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False)

print("SUCCESS: chart_data.json created!")
print(f"Total customers: {total}")
print(f"Churned customers: {churned}")
print(f"Overall churn rate: {data['overallChurnRate']}%")
