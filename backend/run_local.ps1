# PowerShell helper to create venv, install and run uvicorn
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
