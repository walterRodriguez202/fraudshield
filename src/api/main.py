from fastapi import FastAPI
from pydantic import BaseModel
from src.decisioning.decision_engine import decide_transaction

app = FastAPI(title="FraudShield API")

class TransactionRequest(BaseModel):
    model_score: float
    high_risk_rule_hit: bool = False

@app.get("/health")
def health() -> dict: 
    return {"status": "ok"}

@app.post("/score_transaction")
def score_transaction(payload: TransactionRequest) -> dict:
    decision = decide_transaction(
        model_score=payload.model_score,
        high_risk_rule_hit=payload.high_risk_rule_hit,
    )
    return {
        "decision": decision,
        "model_score": payload.model_score,
        "high_risk_rule_hit": payload.high_risk_rule_hit,
    }