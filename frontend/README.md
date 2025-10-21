Open `index.html` in your browser. It expects the API at http://localhost:8000/predict
If you prefer to serve the frontend via a small static server, you can use Python's http.server:

# from repo root (PowerShell)
python -m http.server -d frontend 5500; # then open http://localhost:5500
