from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .model import predict_fire

from fastapi import APIRouter
from datetime import datetime, timedelta

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
        items.append({"ts": ts, "temperature": temp, "humidity": humidity, "wind": wind, "prediction": pred})
    return {"history": items}
