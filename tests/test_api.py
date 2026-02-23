from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}

def test_score_transaction_decline():
    res = client.post("/score_transaction", json={"model_score": 0.92, "high_risk_rule_hit": False})
    assert res.status_code == 200
    assert res.json()["decision"] == "decline"

def test_score_transaction_step_up():
    res = client.post("/score_transaction", json={"model_score": 0.50, "high_risk_rule_hit": False})
    assert res.status_code == 200
    assert res.json()["decision"] == "step_up"

def test_score_transaction_approve():
    res = client.post("/score_transaction", json={"model_score": 0.10, "high_risk_rule_hit": False})
    assert res.status_code == 200
    assert res.json()["decision"] == "approve"
