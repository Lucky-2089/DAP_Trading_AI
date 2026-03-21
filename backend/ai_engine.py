import pandas as pd
import joblib
import os
from typing import Dict
from backend.api_mock import fetch_archax_mmfs, fetch_marketdata_mmfs


class RecommenderAPI:
    def __init__(self):
        # 1. Resolve the path to the serialized model
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'rf_model.joblib'))

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Serialized model not found at {model_path}. Please run 'python scripts/train_model.py' first.")

        # 2. Load the model and metrics into memory instantly
        saved_data = joblib.load(model_path)
        self.ml_model = saved_data['model']
        self.model_metrics = saved_data['metrics']

    def get_recommendations(self, wallet: Dict) -> pd.DataFrame:
        raw_data = fetch_archax_mmfs() + fetch_marketdata_mmfs()
        df = pd.DataFrame(raw_data)
        df = df[df['currency'] == wallet['currency']].copy()

        if df.empty:
            return df

        # Normalize Features
        max_yield = df['yield'].max()
        df['norm_yield'] = df['yield'] / max_yield if max_yield > 0 else 0
        df['risk_match'] = df['risk_level'].apply(lambda x: 1.0 if x == wallet['risk_profile'] else 0.5)
        df['wallet_fit'] = df['minimum_investment'].apply(lambda x: 1.0 if x <= wallet['wallet_balance'] else 0.0)
        df['liquidity_score'] = 1.0 / df['liquidity']

        # ML Prediction using the pre-trained, loaded model
        ml_features = df[['yield', 'risk_match', 'wallet_fit']]
        df['ml_boost'] = self.ml_model.predict_proba(ml_features)[:, 1]

        # Quant Base Score
        df['quant_score'] = (0.4 * df['norm_yield']) + (0.3 * df['risk_match']) + (0.1 * df['liquidity_score']) + (
                    0.2 * df['wallet_fit'])

        # Blended Final Score
        df['final_score'] = (df['quant_score'] * 0.4) + (df['ml_boost'] * 0.6)

        df = df[df['wallet_fit'] == 1.0].sort_values(by='final_score', ascending=False)
        return df

    def get_reasoning(self, row: pd.Series, wallet: Dict) -> str:
        return (f"Based on your {wallet['currency']} balance and {wallet['risk_profile']}-risk preference, "
                f"**{row['fund_name']}** is ideal. The AI predicts a high likelihood of fit based on its yield of {row['yield']}% "
                f"and strict adherence to your investment minimums.")