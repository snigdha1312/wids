#import and load model

import joblib
import hashlib
import json

model = joblib.load("best_fraud_detection_model.pkl")

#raw transaction input
raw_transaction = {
    "TxHash": "0xabc123",
    "BlockHeight": 5848095,
    "TimeStamp": 1529873859,
    "From": "0x16f209b5332a1b4fa5bf19497ca40154c5db2f85",
    "To": "0x002f0c8119c16d310342d869ca8bf6ace34d9c39",
    "Value": 0.5
}

#SHA-256 Hashing ( FUNCTION)
def sha256_hash_transaction(transaction_dict):
    transaction_str = json.dumps(transaction_dict, sort_keys=True)
    return hashlib.sha256(transaction_str.encode()).digest()

tx_hash = sha256_hash_transaction(raw_transaction)
print("Transaction Hash:", tx_hash.hex())

#FEATURE ENGINEERING SAME LOGIC AS TRAINING THE DATA
import pandas as pd
import numpy as np

df = pd.DataFrame([raw_transaction])

# Feature engineering (must match training)
df["hour"] = pd.to_datetime(df["TimeStamp"], unit="s").dt.hour
df["dayofweek"] = pd.to_datetime(df["TimeStamp"], unit="s").dt.dayofweek
df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)

# Dummy freq values (Week 5 you’ll compute real ones)
df["from_freq"] = 1
df["to_freq"] = 1

df["log_value"] = np.log1p(df["Value"])

X = df[[
    "BlockHeight",
    "hour",
    "dayofweek",
    "is_weekend",
    "from_freq",
    "to_freq",
    "log_value"
]]

#FRAUD DETECTION
prediction = model.predict(X)[0]
probability = model.predict_proba(X)[0][1]

print("Fraud Prediction:", prediction)
print("Fraud Probability:", probability)

