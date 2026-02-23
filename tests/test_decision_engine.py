from src.decisioning.decision_engine import decide_transaction

def test_decline_when_rule_hit():
    assert decide_transaction(0.10, True) == "decline"

def test_decline_when_score_very_high():
    assert decide_transaction(0.90, False) == "decline"

def test_step_up_when_score_mid():
    assert decide_transaction(0.50, False) == "step_up"

def test_approve_when_score_low():
    assert decide_transaction(0.10, False) == "approve"
