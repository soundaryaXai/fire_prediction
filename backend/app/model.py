import math

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
    """Simple deterministic placeholder to simulate a risk score in [0,1].

    Uses temperature, humidity, wind speed when present. This gives a
    repeatable, explainable output that the frontend and tests can use
    until the notebook logic is wired in.
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
    return {"risk_score": round(score, 4), "risk_level": risk_to_level(score)}
