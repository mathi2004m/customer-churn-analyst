import pandas as pd
import numpy as np
import json
import os

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("Telco-Customer-Churn.csv")

print("=" * 60)
print("CUSTOMER CHURN ANALYTICS PROJECT")
print("=" * 60)

print("\nOriginal data shape:", df.shape)


# ============================================================
# 2. CLEAN DATA
# ============================================================

df.columns = df.columns.str.strip()

# Clean text columns
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype(str).str.strip()

# Convert TotalCharges
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

# Fill missing TotalCharges
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# Remove duplicate rows
df = df.drop_duplicates()

# Remove duplicate customers
df = df.drop_duplicates(
    subset="customerID"
)

print("\nAfter cleaning:", df.shape)
print(
    "Missing values:",
    df.isnull().sum().sum()
)


# ============================================================
# 3. BUSINESS METRICS
# ============================================================

total_customers = len(df)

churned_customers = int(
    (df["Churn"] == "Yes").sum()
)

retained_customers = int(
    (df["Churn"] == "No").sum()
)

churn_rate = (
    churned_customers /
    total_customers *
    100
)

avg_monthly_charge = float(
    df["MonthlyCharges"].mean()
)

avg_tenure = float(
    df["tenure"].mean()
)

print("\nBUSINESS METRICS")
print("-" * 40)

print(
    "Total customers:",
    total_customers
)

print(
    "Churned customers:",
    churned_customers
)

print(
    "Retained customers:",
    retained_customers
)

print(
    "Churn rate:",
    round(churn_rate, 2),
    "%"
)

print(
    "Average monthly charge:",
    round(avg_monthly_charge, 2)
)

print(
    "Average tenure:",
    round(avg_tenure, 2),
    "months"
)


# ============================================================
# 4. CONTRACT CHURN
# ============================================================

contract_table = pd.crosstab(
    df["Contract"],
    df["Churn"],
    normalize="index"
) * 100

contract_churn = {}

for contract in contract_table.index:

    contract_churn[contract] = round(
        float(
            contract_table.loc[
                contract,
                "Yes"
            ]
        ),
        2
    )

print("\nCHURN BY CONTRACT")
print(contract_table.round(2))


# ============================================================
# 5. INTERNET SERVICE CHURN
# ============================================================

internet_table = pd.crosstab(
    df["InternetService"],
    df["Churn"],
    normalize="index"
) * 100

internet_churn = {}

for service in internet_table.index:

    internet_churn[service] = round(
        float(
            internet_table.loc[
                service,
                "Yes"
            ]
        ),
        2
    )

print("\nCHURN BY INTERNET SERVICE")
print(internet_table.round(2))


# ============================================================
# 6. PAYMENT METHOD CHURN
# ============================================================

payment_table = pd.crosstab(
    df["PaymentMethod"],
    df["Churn"],
    normalize="index"
) * 100

payment_churn = {}

for payment in payment_table.index:

    payment_churn[payment] = round(
        float(
            payment_table.loc[
                payment,
                "Yes"
            ]
        ),
        2
    )

print("\nCHURN BY PAYMENT METHOD")
print(payment_table.round(2))


# ============================================================
# 7. MACHINE LEARNING DATA
# ============================================================

X = df.drop(
    columns=[
        "Churn",
        "customerID"
    ]
)

y = (
    df["Churn"] == "Yes"
).astype(int)


# ============================================================
# 8. IDENTIFY COLUMN TYPES
# ============================================================

categorical_cols = (
    X.select_dtypes(
        include=["object"]
    ).columns.tolist()
)

numeric_cols = (
    X.select_dtypes(
        exclude=["object"]
    ).columns.tolist()
)


print("\nNumeric columns:")
print(numeric_cols)

print("\nCategorical columns:")
print(categorical_cols)


# ============================================================
# 9. PREPROCESSING
# ============================================================

numeric_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(
            strategy="median"
        )
    ),
    (
        "scaler",
        StandardScaler()
    )
])

categorical_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(
            strategy="most_frequent"
        )
    ),
    (
        "encoder",
        OneHotEncoder(
            handle_unknown="ignore"
        )
    )
])

preprocessor = ColumnTransformer([
    (
        "numeric",
        numeric_pipeline,
        numeric_cols
    ),
    (
        "categorical",
        categorical_pipeline,
        categorical_cols
    )
])


# ============================================================
# 10. MODEL
# ============================================================

model = Pipeline([
    (
        "preprocessor",
        preprocessor
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=42
        )
    )
])


# ============================================================
# 11. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))


# ============================================================
# 12. TRAIN MODEL
# ============================================================

model.fit(
    X_train,
    y_train
)

print("\nModel training completed.")


# ============================================================
# 13. PREDICTIONS
# ============================================================

y_pred = model.predict(
    X_test
)

y_probability = model.predict_proba(
    X_test
)[:, 1]


# ============================================================
# 14. MODEL METRICS
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred
)

recall = recall_score(
    y_test,
    y_pred
)

f1 = f1_score(
    y_test,
    y_pred
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)

cm = confusion_matrix(
    y_test,
    y_pred
)


print("\nMODEL PERFORMANCE")
print("-" * 40)

print(
    "Accuracy :",
    round(accuracy, 4)
)

print(
    "Precision:",
    round(precision, 4)
)

print(
    "Recall   :",
    round(recall, 4)
)

print(
    "F1 Score :",
    round(f1, 4)
)

print(
    "ROC-AUC  :",
    round(roc_auc, 4)
)

print("\nConfusion Matrix:")
print(cm)


# ============================================================
# 15. GET MODEL PARAMETERS
# ============================================================

trained_preprocessor = (
    model.named_steps[
        "preprocessor"
    ]
)

classifier = (
    model.named_steps[
        "classifier"
    ]
)

feature_names = (
    trained_preprocessor
    .get_feature_names_out()
)

coefficients = (
    classifier.coef_[0]
)

intercept = float(
    classifier.intercept_[0]
)


# ============================================================
# 16. CREATE BROWSER MODEL
# ============================================================

numeric_transformer = (
    trained_preprocessor
    .named_transformers_[
        "numeric"
    ]
)

numeric_imputer = (
    numeric_transformer
    .named_steps[
        "imputer"
    ]
)

numeric_scaler = (
    numeric_transformer
    .named_steps[
        "scaler"
    ]
)

numeric_medians = (
    numeric_imputer.statistics_
)

numeric_means = (
    numeric_scaler.mean_
)

numeric_scales = (
    numeric_scaler.scale_
)


categorical_transformer = (
    trained_preprocessor
    .named_transformers_[
        "categorical"
    ]
)

encoder = (
    categorical_transformer
    .named_steps[
        "encoder"
    ]
)

categories = (
    encoder.categories_
)


browser_model = {
    "intercept": intercept,
    "numeric": {},
    "categorical": {}
}


# ============================================================
# 17. NUMERIC PARAMETERS
# ============================================================

for i, column in enumerate(
    numeric_cols
):

    transformed_name = (
        "numeric__" +
        column
    )

    feature_index = list(
        feature_names
    ).index(
        transformed_name
    )

    browser_model[
        "numeric"
    ][column] = {

        "mean":
            float(
                numeric_means[i]
            ),

        "scale":
            float(
                numeric_scales[i]
            ),

        "median":
            float(
                numeric_medians[i]
            ),

        "coefficient":
            float(
                coefficients[
                    feature_index
                ]
            )
    }


# ============================================================
# 18. CATEGORICAL PARAMETERS
# ============================================================

for col_index, column in enumerate(
    categorical_cols
):

    browser_model[
        "categorical"
    ][column] = {}

    for category in categories[
        col_index
    ]:

        transformed_name = (
            "categorical__" +
            column +
            "_" +
            str(category)
        )

        if transformed_name in feature_names:

            feature_index = list(
                feature_names
            ).index(
                transformed_name
            )

            browser_model[
                "categorical"
            ][column][
                str(category)
            ] = float(
                coefficients[
                    feature_index
                ]
            )


# ============================================================
# 19. SAVE MODEL PARAMETERS
# ============================================================

with open(
    "model.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        browser_model,
        file,
        indent=2
    )

print("\nSaved: model.json")


# ============================================================
# 20. SAVE METRICS
# ============================================================

metrics = {

    "total_customers":
        total_customers,

    "churned_customers":
        churned_customers,

    "retained_customers":
        retained_customers,

    "churn_rate":
        round(
            churn_rate,
            2
        ),

    "avg_monthly_charge":
        round(
            avg_monthly_charge,
            2
        ),

    "avg_tenure":
        round(
            avg_tenure,
            2
        ),

    "accuracy":
        round(
            accuracy,
            4
        ),

    "precision":
        round(
            precision,
            4
        ),

    "recall":
        round(
            recall,
            4
        ),

    "f1":
        round(
            f1,
            4
        ),

    "roc_auc":
        round(
            roc_auc,
            4
        ),

    "contract_churn":
        contract_churn,

    "internet_churn":
        internet_churn,

    "payment_churn":
        payment_churn
}


with open(
    "metrics.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        metrics,
        file,
        indent=2
    )

print("Saved: metrics.json")


# ============================================================
# 21. FINISH
# ============================================================

print("\n" + "=" * 60)
print("PROJECT MODEL BUILD COMPLETE")
print("=" * 60)

print("\nFiles created:")

print("✓ model.json")
print("✓ metrics.json")

print("\nFinal Model Results:")
print(
    "Accuracy :",
    round(
        accuracy * 100,
        2
    ),
    "%"
)

print(
    "Precision:",
    round(
        precision * 100,
        2
    ),
    "%"
)

print(
    "Recall   :",
    round(
        recall * 100,
        2
    ),
    "%"
)

print(
    "F1 Score :",
    round(
        f1 * 100,
        2
    ),
    "%"
)

print(
    "ROC-AUC  :",
    round(
        roc_auc,
        3
    )
)

print("\nNow open index.html.")