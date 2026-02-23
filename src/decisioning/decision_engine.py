def decide_transaction(model_score: float, high_risk_rule_hit: bool) -> str:
    if high_risk_rule_hit or model_score >= 0.85:
        return "decline"
    if model_score >= 0.40:
        return "step_up"
    return "approve"
