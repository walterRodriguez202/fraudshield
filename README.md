# FraudShield

Real-time credit card fraud detection API with a rule-based decisioning engine and interactive dashboard.

## What it does

FraudShield scores incoming credit card transactions using an XGBoost model trained on the [Kaggle Credit Card Fraud dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) (284,807 real transactions, 0.17% fraud rate). Each transaction gets an approve, step_up, or decline decision based on model score and risk rules.

## Model Performance

| Metric | Value |
|--------|-------|
| PR-AUC | 0.8712 |
| Precision | 0.20 |
| Recall | 0.8980 |
| Threshold | 0.0021 |

Baseline logistic regression achieved PR-AUC of 0.07. XGBoost with threshold tuning improved this to **0.87**.

## Decision Logic

| Score Range | Rule Hit | Decision |
|-------------|----------|----------|
| >= 0.85 | any | decline |
| any | Amount > $5,000 | decline |
| 0.40 – 0.85 | false | step_up |
| < 0.40 | false | approve |

## Stack

- **Model**: XGBoost + scikit-learn
- **API**: FastAPI + Uvicorn
- **Dashboard**: Streamlit
- **Tests**: Pytest

## Setup

```bash
git clone https://github.com/walterRodriguez202/fraudshield.git
cd fraudshield
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Download the dataset from [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) and place it at `data/raw/creditcard.csv`, then train:

```bash
python -m src.models.train_xgb_baseline
```

## Run

```bash
# Terminal 1 - API
uvicorn src.api.main:app --reload

# Terminal 2 - Dashboard
streamlit run src/dashboard.py
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /health | GET | Health check |
| /metrics | GET | Model performance metrics |
| /score_transaction | POST | Score a transaction |

## Tests

```bash
pytest tests/ -v
```
