from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json().get('status') == 'ok'


def test_predict():
    payload = {"features": {"temperature": 30, "humidity": 20, "wind": 10}}
    r = client.post('/predict', json=payload)
    assert r.status_code == 200
    data = r.json()
    assert 'prediction' in data
    pred = data['prediction']
    assert 'risk_score' in pred
    assert 0.0 <= pred['risk_score'] <= 1.0


def test_history():
    r = client.get('/history?days=5')
    assert r.status_code == 200
    data = r.json()
    assert 'history' in data
    assert len(data['history']) == 5
