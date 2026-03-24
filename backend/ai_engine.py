import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os


class RecommenderAPI:
    def __init__(self):
        self.model_path = "rf_model.joblib"
        self.train_and_test()
        self.model = joblib.load(self.model_path)

    def train_and_test(self):
        """Trains the RF Model and evaluates accuracy for the AI POC."""
        np.random.seed(42)
        # Features: [Risk_Score (0-2), Wallet_Balance, Liquidity_Need]
        X = np.random.rand(600, 3)
        X[:, 0] = np.random.randint(0, 3, 600)
        X[:, 1] = np.random.uniform(1000, 100000, 600)

        y = []  # Target: 0 (Conservative), 1 (Balanced), 2 (Aggressive)
        for row in X:
            if row[0] == 2 and row[1] > 40000:
                y.append(2)
            elif row[0] == 0:
                y.append(0)
            else:
                y.append(1)

        X_train, X_test, y_train, y_test = train_test_split(X, np.array(y), test_size=0.2)
        rf = RandomForestClassifier(n_estimators=100, max_depth=5)
        rf.fit(X_train, y_train)

        acc = accuracy_score(y_test, rf.predict(X_test))
        print(f"--- AI Model Initialized: Accuracy {acc * 100:.1f}% ---")
        joblib.dump(rf, self.model_path)

    def get_recommendations(self, user_risk, user_balance, funds):
        risk_map = {"low": 0, "medium": 1, "high": 2}
        user_input = [[risk_map.get(user_risk, 0), user_balance, 0.5]]
        probs = self.model.predict_proba(user_input)[0]

        scored = []
        for fund in funds:
            f_cat = 0 if fund['yield'] < 5.15 else (1 if fund['yield'] < 5.23 else 2)
            f = fund.copy()
            f['ai_score'] = round(probs[f_cat] * 100, 1) if f_cat < len(probs) else 50.0
            f['volatility'] = round(np.random.uniform(0.5, 2.0), 2)
            f['liquidity_score'] = round(np.random.uniform(85, 99), 1)
            scored.append(f)
        return pd.DataFrame(scored).sort_values(by='ai_score', ascending=False)

    def simulate_stress_test(self, funds, drop_percent):
        stressed = []
        for fund in funds:
            f = fund.copy()
            f['potential_loss'] = round(drop_percent * (1 + (f.get('volatility', 1.0) / 2)), 2)
            f['recovery_months'] = np.random.randint(4, 14)
            stressed.append(f)
        return pd.DataFrame(stressed)