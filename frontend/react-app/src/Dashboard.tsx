import React, { useEffect, useState } from 'react'
import axios from 'axios'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line, Bar, Pie, Scatter, Radar, Doughnut, PolarArea } from 'react-chartjs-2'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function Dashboard() {
  const [history, setHistory] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    setLoading(true)
    axios.get(apiBase + '/history?days=14')
      .then(r => setHistory(r.data.history || []))
      .catch(() => setHistory([]))
      .finally(() => setLoading(false))
  }, [])

  const labels = history.map(h => new Date(h.ts).toLocaleDateString())
  const scores = history.map(h => h.prediction?.risk_score ?? 0)
  const temps = history.map(h => h.temperature)
  const humidity = history.map(h => h.humidity)

  const lineData = {
    labels,
    datasets: [
      {
        label: 'Risk score',
        data: scores,
        borderColor: 'rgb(255,99,132)',
        backgroundColor: 'rgba(255,99,132,0.2)'
      }
    ]
  }

  const barData = {
    labels,
    datasets: [
      {
        label: 'Temperature (°C)',
        data: temps,
        backgroundColor: 'rgba(54,162,235,0.6)'
      },
      {
        label: 'Humidity (%)',
        data: humidity,
        backgroundColor: 'rgba(75,192,192,0.6)'
      }
    ]
  }

  // pie chart aggregating risk levels counts
  const levelsCount: Record<string, number> = {}
  history.forEach(h => {
    const lvl = h.prediction?.risk_level || 'unknown'
    levelsCount[lvl] = (levelsCount[lvl] || 0) + 1
  })
  const pieData = {
    labels: Object.keys(levelsCount),
    datasets: [
      {
        data: Object.values(levelsCount),
        backgroundColor: ['#2a8f2a', '#d47a00', '#b30']
      }
    ]
  }

  // scatter: temperature vs humidity
  const scatterData = {
    datasets: [
      {
        label: 'Temp vs Humidity',
        data: history.map(h => ({ x: h.temperature, y: h.humidity })),
        backgroundColor: 'rgba(153,102,255,0.6)'
      }
    ]
  }

  // doughnut: same as pie but visual variant
  const doughnutData = pieData

  // radar: normalized features (avg values)
  const avgTemp = temps.length ? temps.reduce((a, b) => a + b, 0) / temps.length : 0
  const avgHumidity = humidity.length ? humidity.reduce((a, b) => a + b, 0) / humidity.length : 0
  const avgWind = history.map(h => h.wind).reduce((a, b) => a + b, 0) / (history.length || 1)
  const radarData = {
    labels: ['Temperature', 'Humidity', 'Wind'],
    datasets: [
      {
        label: 'Averages',
        data: [avgTemp, avgHumidity, avgWind],
        backgroundColor: 'rgba(255,159,64,0.2)',
        borderColor: 'rgba(255,159,64,1)'
      }
    ]
  }

  // polar area: distribution of temperature buckets
  const buckets: Record<string, number> = {}
  history.forEach(h => {
    const b = `${Math.floor(h.temperature / 5) * 5}-${Math.floor(h.temperature / 5) * 5 + 4}`
    buckets[b] = (buckets[b] || 0) + 1
  })
  const polarData = {
    labels: Object.keys(buckets),
    datasets: [
      {
        data: Object.values(buckets),
        backgroundColor: ['#ff6384', '#36a2eb', '#ffcd56', '#4bc0c0', '#9966ff']
      }
    ]
  }

  // bubble: x=temp, y=humidity, r=wind (scaled)
  const bubbleData = {
    datasets: [
      {
        label: 'Temp/Humidity/Wind (bubble r ~ wind)',
        data: history.map(h => ({ x: h.temperature, y: h.humidity, r: Math.max(2, (h.wind || 1)) })),
        backgroundColor: 'rgba(75,192,192,0.6)'
      }
    ]
  }

  return (
    <div style={{ padding: 24 }}>
      <h2>Dashboard</h2>
      {loading && <div>Loading...</div>}

      <div style={{ width: '800px', marginTop: 12 }}>
        <h3>Risk score over time (Line)</h3>
        <Line data={lineData} />
      </div>

      <div style={{ width: '800px', marginTop: 24 }}>
        <h3>Temperature and Humidity (Bar)</h3>
        <Bar data={barData} />
      </div>

      <div style={{ width: '400px', marginTop: 24 }}>
        <h3>Risk level distribution (Pie)</h3>
        <Pie data={pieData} />
      </div>

      <div style={{ width: '600px', marginTop: 24 }}>
        <h3>Temperature vs Humidity (Scatter)</h3>
        <Scatter data={scatterData} />
      </div>

      <div style={{ width: '400px', marginTop: 24 }}>
        <h3>Risk level distribution (Doughnut)</h3>
        <Doughnut data={doughnutData} />
      </div>

      <div style={{ width: '500px', marginTop: 24 }}>
        <h3>Feature averages (Radar)</h3>
        <Radar data={radarData} />
      </div>

      <div style={{ width: '500px', marginTop: 24 }}>
        <h3>Temperature buckets (Polar Area)</h3>
        <PolarArea data={polarData} />
      </div>

      <div style={{ width: '600px', marginTop: 24 }}>
        <h3>Bubble: temp/humidity/wind</h3>
        {/* Bubble chart uses the same component as Scatter in react-chartjs-2; ChartJS will pick dataset type by data shape */}
        <Scatter data={bubbleData as any} />
      </div>
    </div>
  )
}
