import json
import os
import joblib

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve, average_precision_score, precision_score, recall_score
from xgboost import XGBClassifier


def main() -> None:
    df = pd.read_csv("data/raw/creditcard.csv")
    X = df.drop(columns=["Class", "Time"])
    y = df["Class"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        random_state=42,
    )
    model.fit(X_train, y_train)
    proba = model.predict_proba(X_test)[:, 1]

    pr_auc = average_precision_score(y_test, proba)
    precisions, recalls, thresholds = precision_recall_curve(y_test, proba)

    chosen = None
    for p, r, t in zip(precisions[:-1], recalls[:-1], thresholds):
        if p >= 0.20:
            chosen = (t, p, r)
            break

    threshold = float(chosen[0]) if chosen is not None else 0.5
    pred = (proba >= threshold).astype(int)

    print(f"PR-AUC: {pr_auc:.4f}")
    print(f"Threshold used: {threshold:.4f}")
    print(f"Precision: {precision_score(y_test, pred, zero_division=0):.4f}")
    print(f"Recall:    {recall_score(y_test, pred, zero_division=0):.4f}")

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/fraud_model.joblib")

    with open("models/threshold.json", "w") as f:
        json.dump({"threshold": threshold},f)
    
    metrics = {
        "pr_auc": round(pr_auc, 4),
        "threshold": round(threshold, 4),
        "precision": round(float(precision_score(y_test, pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, pred, zero_division=0)), 4),
    }

    with open("models/metrics.json", "w") as f:
        json.dump(metrics, f)
    
    print("Model saved to models/fraud_model.joblib")



if __name__ == "__main__":
    main()
