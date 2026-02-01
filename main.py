from fastapi import FastAPI
from pydantic import BaseModel
from app.ml_model import predict_fraud
from app.hashing import hash_transaction
from app.blockchain import store_on_chain

app = FastAPI()

class Transaction(BaseModel):
    amount: float
    sender: str
    receiver: str
    timestamp: int

@app.post("/analyze")
def analyze_transaction(tx: Transaction):
    # 1. ML Prediction
    prediction = predict_fraud(tx.dict())

    # 2. Hash the transaction
    tx_hash = hash_transaction(tx.dict())

    # 3. Store on blockchain
    tx_receipt = store_on_chain(tx_hash, prediction)

    return {
        "hash": tx_hash,
        "prediction": prediction,
        "tx_receipt": tx_receipt
    }
