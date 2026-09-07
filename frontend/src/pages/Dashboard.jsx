import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'
import StatCard from '../components/StatCard'
import FitnessPlanCard from '../components/FitnessPlanCard'
import Loading from '../components/Loading'
import { api } from '../services/api'
import { useAuth } from '../context/AuthContext'

export default function Dashboard() {
  const { user } = useAuth()
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api
      .get('/progress/dashboard')
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <Loading text="Loading dashboard…" />

  const name = data?.user?.name || user?.username || 'there'
  const score = data?.analysis?.fitness_score
  const hour = new Date().getHours()
  const greet = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening'

  return (
    <div className="page">
      <Navbar />
      <main className="dashboard">
        <header className="dash-hero">
          <p className="eyebrow">{greet}</p>
          <h1>{name}</h1>
          <p className="tagline">Here&apos;s your fitness overview</p>
        </header>

        {error ? <p className="error">{error}</p> : null}

        <div className="dash-grid">
          <article className="score-card">
            <p className="stat-label">Fitness Score</p>
            <p className="score-number">{score != null ? Math.round(score) : '—'}</p>
            <p className="muted">/ 100</p>
            {data?.analysis?.activity_level ? (
              <p className="chip">{data.analysis.activity_level} activity</p>
            ) : null}
          </article>

          <FitnessPlanCard plan={data?.tomorrow_plan} compact />

          <StatCard
            className="span-sm"
            label="Weight"
            value={data?.today?.weight}
            unit=" kg"
          />
          <StatCard
            className="span-md"
            label="Steps"
            value={data?.today?.steps?.toLocaleString?.() ?? data?.today?.steps}
          />
          <StatCard
            className="span-md"
            label="Exercise"
            value={data?.today?.exercise_minutes}
            unit=" min"
          />
          <StatCard
            className="span-sm"
            label="Sleep"
            value={data?.today?.sleep_hours}
            unit=" hrs"
          />
        </div>

        <div className="dash-cta">
          <Link className="btn primary" to="/daily-checkin">
            Daily Check-in →
          </Link>
          <Link className="btn ghost" to="/tomorrow-plan">
            View full plan
          </Link>
        </div>
      </main>
    </div>
  )
}
