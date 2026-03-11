import json
import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(page_title="FraudShield", page_icon="🛡️", layout="wide")
st.title("🛡️ FraudShield — Fraud Detection Dashboard")

# - Sidebar: Model Metrics -
st.sidebar.header("Model Performance")

try:
    metrics = requests.get(f"{API_URL}/metrics", timeout=2).json()
    st.sidebar.metric("PR-AUC", metrics["pr_auc"])
    st.sidebar.metric("Precision", metrics["precision"])
    st.sidebar.metric("Recall", metrics["recall"])
    st.sidebar.metric("Threshold", metrics["threshold"])
except Exception:
    st.sidebar.warning("API offline - start uvicorn first")

# Main: Score a Transaction

st.header("Score a transaction")

FRAUD_SAMPLE = {
    "V1": -2.3122, "V2": 1.9520, "V3": -1.6099, "V4": 3.9979,
    "V5": -0.5222, "V6": -1.4265, "V7": -2.5374, "V8": 1.3917,
    "V9": -2.7701, "V10": -2.7723, "V11": 3.2020, "V12": -2.8999,
    "V13": -0.5952, "V14": -4.2893, "V15": 0.3897, "V16": -1.1407,
    "V17": -2.8301, "V18": -0.0168, "V19": 0.4170, "V20": 0.1269,
    "V21": 0.5172, "V22": -0.0350, "V23": -0.4652, "V24": 0.3202,
    "V25": 0.0445, "V26": 0.1778, "V27": 0.2611, "V28": -0.1433,
    "Amount": 0.0
}

if st.button("Load Fraud Sample"):
    for k, v in FRAUD_SAMPLE.items():
        if k != "Amount":
            st.session_state[k] = v
    st.rerun()


col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("Transaction Amount ($)", min_value=0.01, value=150.0, step=0.01)
with col2:
    st.markdown("**V1–V28** are anonymized PCA features from the raw transaction data.")


st.markdown("#### Feature Inputs (V1–V28)")

cols = st.columns(6)
features = {}
for i in range(1, 29):
    col = cols[(i-1) % 6]
    # features[f"V{i}"] = col.number_input(f"V{i}", value=0.0, step = 0.1, key=f"V{i}")
    features[f"V{i}"] = col.number_input(f"V{i}", value=st.session_state.get(f"V{i}", 0.0), step=0.1, key=f"V{i}")

if st.button("Score Transactions", type="primary"):
    payload = {**features, "Amount": amount}

    try:
        response = requests.post(f"{API_URL}/score_transaction", json=payload, timeout=5)
        result = response.json()
        decision = result["decision"]
        score = result["model_score"]
        high_risk = result["high_risk_rule_hit"]

        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric("Decision", decision.upper())
        col2.metric("Fraud Score", f"{score:.4f}")
        col3.metric("High Risk Rule", "YES" if high_risk else "NO")

        if decision == "decline":
            st.error("❌ Transaction DECLINED")
            reasons = []
            if score >= 0.85:
                reasons.append(f"Model score {score:.4f} exceeds high-risk threshold (0.85)")
            if high_risk:
                reasons.append(f"Amount ${amount:,.2f} exceeds $5,000 limit")
            for r in reasons:
                st.write(f"• {r}")

        elif decision == "step_up":
            st.warning("⚠️ Transaction flagged for STEP-UP review")
            st.write(f"• Model score {score:.4f} is in the review range (0.40–0.85)")

        else:
            st.success("✅ Transaction APPROVED")
            st.write(f"• Model score {score:.4f} is below risk threshold")

    except Exception as e:
        st.error(f"API error: {e}")