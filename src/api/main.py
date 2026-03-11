import json
import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from src.decisioning.decision_engine import decide_transaction

app = FastAPI(title="FraudShield API")

# Load model and metadata at startup
model = joblib.load("models/fraud_model.joblib")
with open("models/threshold.json") as f:
    THRESHOLD = json.load(f)["threshold"]
with open("models/metrics.json") as f:
    METRICS = json.load(f)

FEATURE_COLS = [f"V{i}" for i in range(1, 29)] + ["Amount"]

class TransactionRequest(BaseModel):
    V1: float; V2: float; V3: float; V4: float; V5: float
    V6: float; V7: float; V8: float; V9: float; V10: float
    V11: float; V12: float; V13: float; V14: float; V15: float
    V16: float; V17: float; V18: float; V19: float; V20: float
    V21: float; V22: float; V23: float; V24: float; V25: float
    V26: float; V27: float; V28: float
    Amount: float


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.get("/metrics")
def metrics() -> dict:
    return METRICS

@app.post("/score_transaction")
def score_transaction(payload: TransactionRequest) -> dict:
    features = np.array([[getattr(payload, col) for col in FEATURE_COLS]])
    model_score = float(model.predict_proba(features)[0, 1])
    high_risk_rule_hit = payload.Amount > 5000
    decision = decide_transaction(
        model_score=model_score,
        high_risk_rule_hit=high_risk_rule_hit,
    )
    return {
        "decision": decision,
        "model_score": round(model_score, 4),
        "high_risk_rule_hit": high_risk_rule_hit,
    }
