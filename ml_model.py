import pandas as pd

# Load dataset
df = pd.read_csv("first_order_df.csv")

# 1. Basic dataset info
print("\n--- Dataset Shape ---")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# 2. Preview first rows
print("\n--- Sample Rows ---")
print(df.head())

# 3. Column data types
print("\n--- Column Data Types ---")
print(df.dtypes)

# 4. Missing values check
print("\n--- Missing Values ---")
print(df.isnull().sum())

# 5. Duplicate rows check
print("\n--- Duplicate Rows ---")
print("Total Duplicates:", df.duplicated().sum())

# 6. Fraud label distribution (isError)
print("\n--- Fraud Label Distribution ---")
print(df["isError"].value_counts())
print("\nFraud Percentage:")
print(df["isError"].value_counts(normalize=True) * 100)

# 7. Unique counts for blockchain fields
print("\n--- Unique Blockchain Fields ---")
print("Unique TxHash:", df["TxHash"].nunique())
print("Unique From Addresses:", df["From"].nunique())
print("Unique To Addresses:", df["To"].nunique())

# 8. Transaction value statistics
print("\n--- Value Statistics ---")
print(df["Value"].describe())

import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("first_order_df.csv")

# 1. Drop useless index column
df.drop(columns=["Unnamed: 0"], inplace=True)

# 2. Handle missing 'To' address (contract creation txns)
df["To"] = df["To"].fillna("CONTRACT_CREATION")

# Drop rows missing critical blockchain fields (very few rows)
df.dropna(
    subset=["BlockHeight", "TimeStamp", "From", "Value", "isError"],
    inplace=True
)


# 3. Convert UNIX timestamp to useful features
df["datetime"] = pd.to_datetime(df["TimeStamp"], unit="s")
df["hour"] = df["datetime"].dt.hour
df["dayofweek"] = df["datetime"].dt.dayofweek
df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)

df.drop(columns=["TimeStamp", "datetime"], inplace=True)

# 4. Frequency encoding for addresses
from_freq = df["From"].value_counts()
to_freq = df["To"].value_counts()

df["from_freq"] = df["From"].map(from_freq)
df["to_freq"] = df["To"].map(to_freq)

df.drop(columns=["From", "To"], inplace=True)

# 5. Log transform transaction value
df["log_value"] = np.log1p(df["Value"])
df.drop(columns=["Value"], inplace=True)

# 6. Rename target column
df.rename(columns={"isError": "is_fraud"}, inplace=True)

# 7. Remove duplicate transactions
df.drop_duplicates(subset=["TxHash"], inplace=True)

# Final check
print(df.head())
print(df.info())

# 8. Save cleaned dataset (IMPORTANT)
df.to_csv("cleaned_transactions.csv", index=False)

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Load cleaned data
df = pd.read_csv("cleaned_transactions.csv")

# Features & target
X = df.drop(columns=["TxHash", "is_fraud"])
y = df["is_fraud"]

# Train-test split (stratified due to class imbalance)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================
# MODEL 1: Logistic Regression
# =========================
log_model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

log_model.fit(X_train, y_train)

log_preds = log_model.predict(X_test)
log_probs = log_model.predict_proba(X_test)[:, 1]

log_auc = roc_auc_score(y_test, log_probs)

print("\n--- Logistic Regression ---")
print(classification_report(y_test, log_preds))
print("ROC-AUC:", log_auc)

# =========================
# MODEL 2: Random Forest
# =========================
rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    min_samples_split=10,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)

rf_preds = rf_model.predict(X_test)
rf_probs = rf_model.predict_proba(X_test)[:, 1]

rf_auc = roc_auc_score(y_test, rf_probs)

print("\n--- Random Forest ---")
print(classification_report(y_test, rf_preds))
print("ROC-AUC:", rf_auc)

# =========================
# MODEL SELECTION
# =========================
print("\n--- Model Comparison ---")
print(f"Logistic Regression ROC-AUC: {log_auc:.4f}")
print(f"Random Forest ROC-AUC:     {rf_auc:.4f}")

if rf_auc > log_auc:
    best_model = rf_model
    best_model_name = "Random Forest"
else:
    best_model = log_model
    best_model_name = "Logistic Regression"

print(f"\n✅ Best Model Selected: {best_model_name}")

# =========================
# SAVE BEST MODEL
# =========================
joblib.dump(best_model, "best_fraud_detection_model.pkl")

print("✅ Best model saved as best_fraud_detection_model.pkl")
