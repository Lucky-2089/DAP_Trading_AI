import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score


def generate_synthetic_data(num_samples=10000) -> pd.DataFrame:
    print("[Training Pipeline] Generating 10,000 synthetic trading records...")
    np.random.seed(42)

    yields = np.clip(np.random.normal(loc=4.5, scale=0.8, size=num_samples), 1.0, 8.0)
    risk_matches = np.random.choice([1.0, 0.5, 0.0], size=num_samples, p=[0.4, 0.4, 0.2])
    wallet_fits = np.random.choice([1.0, 0.0], size=num_samples, p=[0.8, 0.2])

    df = pd.DataFrame({'yield': yields, 'risk_match': risk_matches, 'wallet_fit': wallet_fits})

    # Adjusted weights for a stronger, clearer signal
    buy_probability = ((df['yield'] / 8.0 * 0.5) + (df['risk_match'] * 0.35) + (df['wallet_fit'] * 0.15))

    # CRITICAL FIX: Reduced the noise standard deviation from 0.1 to 0.02
    # This makes the synthetic customer's behavior highly predictable
    noise = np.random.normal(0, 0.02, num_samples)
    buy_probability = np.clip(buy_probability + noise, 0, 1)

    # Crisper decision boundary
    df['target_bought'] = (buy_probability > 0.55).astype(int)
    return df


def run_training_pipeline():
    # 1. Generate Data
    df = generate_synthetic_data()
    X = df[['yield', 'risk_match', 'wallet_fit']]
    y = df['target_bought']

    # 2. Train Model
    print("[Training Pipeline] Training Random Forest Classifier...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # CRITICAL FIX: Increased n_estimators to 200 and max_depth to 10
    # This gives the AI more capacity to learn tight decision boundaries
    model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    # 3. Calculate Metrics
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
        "precision": round(precision_score(y_test, y_pred) * 100, 2)
    }
    print(f"[Training Pipeline] Success. Accuracy: {metrics['accuracy']}%, Precision: {metrics['precision']}%")

    # 4. Serialize and Save with Joblib
    os.makedirs('models', exist_ok=True)
    model_path = os.path.join('models', 'rf_model.joblib')

    joblib.dump({'model': model, 'metrics': metrics}, model_path)
    print(f"[Training Pipeline] Model serialized and saved to: {model_path}")


if __name__ == "__main__":
    run_training_pipeline()