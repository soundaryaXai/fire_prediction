React frontend (development)
1. Change to the react app folder and install dependencies:

# PowerShell
cd frontend\react-app; npm install

2. Start the dev server:

# PowerShell
npm run dev

The Vite dev server runs on port 5173 by default and the backend CORS is pre-configured for that origin.

NOTE: If you're using Python 3.13, some older numpy versions (e.g. 1.27.x) are not available for that interpreter. The `backend/requirements.txt` pins a numpy version compatible with Python 3.13. If venv creation fails complaining about `numpy==1.27.5`, update the numpy pin to a 3.13-compatible release or use Python 3.11/3.12.
Fire Prediction — FastAPI backend + simple frontend

Overview
- FastAPI backend scaffold lives under `backend/app/`.
- A placeholder model is in `backend/app/model.py` — replace this with the code from your `fire_prediction.ipynb`.
- A simple static frontend is at `frontend/index.html` which talks to `http://localhost:8000/predict`.

Quick start (PowerShell)

# create a virtual env and install
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r backend\requirements.txt

# run the API server
# from repository root
(Activate the virtualenv first) then:
python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# open the frontend
# open frontend\index.html in a browser, or serve it with a static server.

Wiring in your notebook
1. Copy preprocessing, feature-engineering and model loading code from your `fire_prediction.ipynb` into `backend/app/model.py`.
2. Replace `predict_fire` with a function that accepts a dict of inputs and returns a JSON-serializable dict with at least `risk_score` (float 0..1) and `risk_level` (str).
3. Run tests: `pytest -q` from repo root.

Notes
- The current model is a placeholder heuristic so the app is runnable without the notebook. Replace it when you can move the notebook into the workspace.
