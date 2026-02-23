# FraudShield

Real-time credit card fraud detection project for interview prep.

## Day 1 Findings
- Dataset: synthetic credit card transactions (`data/raw/creditcard.csv`)
- Class imbalance: fraud rate is ~0.96% (`Class=1`)
- Baseline model: Logistic Regression with `class_weight="balanced"`
- Metrics:
  - Precision: 0.0164
  - Recall: 0.5584
  - PR-AUC: 0.0732
- Notes:
  - Accuracy is misleading for fraud because non-fraud dominates the dataset.
  - Baseline prioritizes recall but creates too many false positives.

## Day 2 Findings
- Model: XGBoost baseline (`src/models/train_xgb_baseline.py`)
- PR-AUC: 0.3987 (up from 0.0732 on Day 1)
- Threshold tuning target: precision >= 0.20
- Chosen threshold: 0.0274
- Precision: 0.2000
- Recall: 0.4632
- Notes:
  - XGBoost significantly improved fraud ranking quality.
  - Threshold tuning gave a more practical precision/recall tradeoff than default 0.5.

## Next Steps
- Build rule-based decisioning (`approve`, `step_up`, `decline`)
- Add tests for decision logic
- Expose scoring through a FastAPI endpoint
- Add a simple monitoring view (precision, recall, PR-AUC)
