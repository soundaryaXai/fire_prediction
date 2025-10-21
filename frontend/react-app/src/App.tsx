import React, { useState } from 'react'
import axios from 'axios'
import Dashboard from './Dashboard'

const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function App() {
  const [temperature, setTemperature] = useState(30)
  const [humidity, setHumidity] = useState(20)
  const [wind, setWind] = useState(10)
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  async function handlePredict() {
    setLoading(true)
    setResult(null)
    try {
      const r = await axios.post(apiBase + '/predict', { features: { temperature, humidity, wind } })
      setResult(r.data.prediction)
    } catch (err) {
      setResult({ error: (err as any).message })
    } finally {
      setLoading(false)
    }
  }

  const [view, setView] = useState<'form' | 'dashboard'>('form')

  return (
    <div style={{ padding: 24, fontFamily: 'Arial, Helvetica, sans-serif' }}>
      <h1>Fire Risk Prediction</h1>
      <div style={{ marginBottom: 12 }}>
        <button onClick={() => setView('form')} style={{ marginRight: 8 }}>Predict</button>
        <button onClick={() => setView('dashboard')}>Dashboard</button>
      </div>
      {view === 'dashboard' ? (
        <Dashboard />
      ) : (
      <div>
        <label>
          Temperature (°C)
          <input type="number" value={temperature} onChange={e => setTemperature(parseFloat(e.target.value))} />
        </label>
      </div>
      <div>
        <label>
          Humidity (%)
          <input type="number" value={humidity} onChange={e => setHumidity(parseFloat(e.target.value))} />
        </label>
      </div>
      <div>
        <label>
          Wind (km/h)
          <input type="number" value={wind} onChange={e => setWind(parseFloat(e.target.value))} />
        </label>
      </div>

      <button onClick={handlePredict} disabled={loading} style={{ marginTop: 12 }}>
        {loading ? 'Predicting...' : 'Predict'}
      </button>

      <div style={{ marginTop: 16, border: '1px solid #ddd', padding: 12, width: 420 }}>
        {result ? (
          result.error ? (
            <div style={{ color: 'red' }}>Error: {result.error}</div>
          ) : (
            <div>
              <div>Risk score: <strong>{result.risk_score}</strong></div>
              <div>Level: <strong>{result.risk_level}</strong></div>
              <div>ETA (min): <strong>{result.eta_minutes}</strong></div>
            </div>
          )
        ) : (
          <div>No prediction yet.</div>
        )}
      </div>
    </div>
  )
}
