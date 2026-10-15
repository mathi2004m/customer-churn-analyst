
import json
import pandas as pd

df = pd.read_csv("Telco-Customer-Churn.csv")

# Clean and validate the data
required = {"customerID", "Contract", "tenure", "MonthlyCharges", "Churn"}
missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing CSV columns: {missing}")

df = df.drop_duplicates(subset="customerID").copy()
df["tenure"] = pd.to_numeric(df["tenure"], errors="coerce")
df["MonthlyCharges"] = pd.to_numeric(df["MonthlyCharges"], errors="coerce")
df["Churn"] = df["Churn"].astype(str).str.strip()
df["Contract"] = df["Contract"].astype(str).str.strip()

df = df.dropna(subset=["tenure", "MonthlyCharges", "Churn", "Contract"])
df = df[df["Churn"].isin(["Yes", "No"])].copy()

# Create the three customer groups
df["TenureGroup"] = "Long-term"
df.loc[df["tenure"] <= 12, "TenureGroup"] = "New"
df.loc[(df["tenure"] >= 13) & (df["tenure"] <= 36), "TenureGroup"] = "Existing"

df["ChargeGroup"] = "High"
df.loc[df["MonthlyCharges"] < 35, "ChargeGroup"] = "Low"
df.loc[
    (df["MonthlyCharges"] >= 35) & (df["MonthlyCharges"] < 70),
    "ChargeGroup"
] = "Medium"


def summarize(column, order):
    results = []

    for key in order:
        group = df[df[column] == key]
        total = len(group)
        churned = int((group["Churn"] == "Yes").sum())
        retained = int((group["Churn"] == "No").sum())

        results.append({
            "key": key,
            "label": key,
            "customers": total,
            "churned": churned,
            "retained": retained,
            "churnRate": round(churned / total * 100, 2) if total else 0
        })

    return results


total = len(df)
churned = int((df["Churn"] == "Yes").sum())
retained = int((df["Churn"] == "No").sum())

data = {
    "totalCustomers": total,
    "churnedCustomers": churned,
    "retainedCustomers": retained,
    "overallChurnRate": round(churned / total * 100, 2) if total else 0,

    "contract": summarize(
        "Contract", ["Month-to-month", "One year", "Two year"]
    ),
    "tenure": summarize(
        "TenureGroup", ["New", "Existing", "Long-term"]
    ),
    "charges": summarize(
        "ChargeGroup", ["Low", "Medium", "High"]
    ),

    # Actual monthly charges for the box plot
    "monthlyChargesByChurn": {
        "No": df.loc[df["Churn"] == "No", "MonthlyCharges"].round(2).tolist(),
        "Yes": df.loc[df["Churn"] == "Yes", "MonthlyCharges"].round(2).tolist()
    }
}

with open("chart_data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False)

print("chart_data.json created successfully!")
print(f"Total customers: {total:,}")
print(f"Churned customers: {churned:,}")
print(f"Overall churn rate: {data['overallChurnRate']}%")

print("\nChurn rate by contract:")
for row in data["contract"]:
    print(f"{row['label']}: {row['churnRate']}%")
