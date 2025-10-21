import math
import os
from typing import Optional
import pickle
import numpy as np

"""
Placeholder model functions extracted from the notebook later.
Replace the contents of `predict_fire` with the real preprocessing and model code
from your `fire_prediction.ipynb` once it's available in the workspace.
"""

def risk_to_level(r: float) -> str:
    if r > 0.66:
        return "high"
    if r > 0.33:
        return "medium"
    return "low"


def predict_fire(features: dict) -> dict:
    """Simple deterministic placeholder to simulate a risk score in [0,1] and ETA (minutes).

    ETA is a fake value: if risk is high, ETA=0; if medium, ETA=30; if low, ETA=60.
    Replace with real logic as needed.
    """
    try:
        temp = float(features.get("temperature", 25.0))
    except Exception:
        temp = 25.0
    try:
        humidity = float(features.get("humidity", 50.0))
    except Exception:
        humidity = 50.0
    try:
        wind = float(features.get("wind", 5.0))
    except Exception:
        wind = 5.0

    # basic heuristic: higher temp, lower humidity, higher wind -> higher risk
    score = (max(0.0, min(1.0, (temp - 10) / 40.0))) * (1.0 - humidity / 100.0) * (1.0 + wind / 20.0)
    score = max(0.0, min(1.0, score))
    level = risk_to_level(score)

    # If a trained linear regression model exists, use it to predict a numeric
    # 'risk_score' as a fallback/adjustment. The model expects [temp, humidity, wind].
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'linreg.pkl')
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                m = pickle.load(f)
            x = np.array([[temp, humidity, wind]])
            # m is dict with 'coef' and 'intercept' saved by train_linear_model
            coef = np.array(m.get('coef', [0, 0, 0]))
            intercept = float(m.get('intercept', 0.0))
            model_score = float(np.dot(x, coef) + intercept)
            # blend heuristic and model (simple average)
            score = float((score + model_score) / 2.0)
            score = max(0.0, min(1.0, score))
            level = risk_to_level(score)
        except Exception:
            pass

    if level == "high":
        eta = 0
    elif level == "medium":
        eta = 30
    else:
        eta = 60
    return {"risk_score": round(score, 4), "risk_level": level, "eta_minutes": eta}


def train_linear_model(history: list, save_path: Optional[str] = None) -> dict:
    """Train a simple LinearRegression to predict risk_score from features.

    `history` should be a list of items with keys: temperature, humidity, wind, prediction.risk_score
    """
    rows = []
    y = []
    for h in history:
        try:
            t = float(h.get('temperature', 0))
            hu = float(h.get('humidity', 0))
            w = float(h.get('wind', 0))
            rs = float(h.get('prediction', {}).get('risk_score', 0))
            rows.append([t, hu, w])
            y.append(rs)
        except Exception:
            continue
    if not rows:
        return {"trained": False, "reason": "no valid data"}

    X = np.array(rows)
    y = np.array(y)

    # closed-form linear regression (ordinary least squares): w = (X^T X)^{-1} X^T y
    X_design = np.hstack([X, np.ones((X.shape[0], 1))])  # add intercept
    try:
        params = np.linalg.lstsq(X_design, y, rcond=None)[0]
    except Exception:
        return {"trained": False, "reason": "lstsq failed"}
    coef = params[:3]
    intercept = float(params[3]) if len(params) > 3 else 0.0

    # ensure models directory
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    if save_path is None:
        save_path = os.path.join(models_dir, 'linreg.pkl')
    model_obj = {'coef': coef.tolist(), 'intercept': intercept}
    with open(save_path, 'wb') as f:
        pickle.dump(model_obj, f)
    return {"trained": True, "n_samples": len(y), "path": save_path}
