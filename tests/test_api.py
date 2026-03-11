from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

BASE = {f"V{i}": 0.0 for i in range(1, 29)}

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}

def test_metrics():
    res = client.get("/metrics")
    assert res.status_code == 200
    assert "pr_auc" in res.json()

def test_score_transaction_approve():
    res = client.post("/score_transaction", json={**BASE, "Amount": 150.0})
    assert res.status_code == 200
    assert res.json()["decision"] in ["approve", "step_up", "decline"]

def test_score_transaction_high_risk_rule():
    res = client.post("/score_transaction", json={**BASE, "Amount": 6000.0})
    assert res.status_code == 200
    assert res.json()["high_risk_rule_hit"] == True
