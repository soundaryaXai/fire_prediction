from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from .model import predict_fire

from fastapi import APIRouter
from datetime import datetime, timedelta
from .model import train_linear_model
import os
from fastapi.responses import FileResponse

app = FastAPI(title="Fire Prediction API")

# Enable CORS so the React dev server (vite) can reach the API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Features(BaseModel):
    model_config = ConfigDict(extra='allow')
    features: dict


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: Features):
    """Accepts a JSON object with a `features` dict and returns prediction result.

    Example request body:
    {"features": {"temperature": 30, "humidity": 20, "wind": 10}}
    """
    preds = predict_fire(data.features)
    return {"prediction": preds, "status": "ok"}


@app.get("/history")
def history(days: int = 7):
    """Return sample historical predictions for the last `days` days.

    This is a placeholder endpoint that returns synthetic data suitable for
    showing line, bar and pie charts on the frontend dashboard. Replace with
    real storage/DB retrieval when available.
    """
    now = datetime.utcnow()
    items = []
    for i in range(days):
        ts = (now - timedelta(days=(days - 1 - i))).isoformat() + 'Z'
        # synthetic feature values that vary over time
        temp = 20 + i * 0.8
        humidity = max(5, 80 - i * 3)
        wind = 5 + (i % 5)
        pred = predict_fire({"temperature": temp, "humidity": humidity, "wind": wind})
    items.append({"ts": ts, "temperature": temp, "humidity": humidity, "wind": wind, "prediction": pred, "eta_minutes": pred.get("eta_minutes")})
    return {"history": items}


@app.post("/train")
def train(days: int = 30):
    """Train a linear regression on synthetic history (or replace to use stored data).

    Returns training summary.
    """
    # reuse the history generator to create synthetic training data
    now = datetime.utcnow()
    items = []
    for i in range(days):
        ts = (now - timedelta(days=(days - 1 - i))).isoformat() + 'Z'
        temp = 20 + (i % 10) * 0.9
        humidity = max(5, 80 - i * 2)
        wind = 3 + (i % 6)
        pred = predict_fire({"temperature": temp, "humidity": humidity, "wind": wind})
        items.append({"ts": ts, "temperature": temp, "humidity": humidity, "wind": wind, "prediction": pred})
    result = train_linear_model(items)
    return {"status": "ok", "result": result}


@app.get("/model/status")
def model_status():
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    path = os.path.join(models_dir, 'linreg.joblib')
    exists = os.path.exists(path)
    return {"exists": exists, "path": path if exists else None}


@app.get("/model/download")
def model_download():
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    path = os.path.join(models_dir, 'linreg.joblib')
    if not os.path.exists(path):
        return {"error": "model not found"}
    return FileResponse(path, filename='linreg.joblib')
