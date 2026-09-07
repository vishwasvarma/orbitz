import { useEffect, useState } from 'react'
import Navbar from '../components/Navbar'
import ProgressChart from '../components/ProgressChart'
import Loading from '../components/Loading'
import { api } from '../services/api'

export default function Progress() {
  const [weekly, setWeekly] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .get('/progress/weekly')
      .then(setWeekly)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <Loading />

  const days = weekly?.days || []
  const avg = weekly?.averages || {}

  return (
    <div className="page">
      <Navbar />
      <main className="form-page">
        <h1>My Progress</h1>
        <p className="tagline">Track how your activity and fitness score evolve.</p>
        {error ? <p className="error">{error}</p> : null}

        <div className="summary-grid">
          <article>
            <p className="stat-label">Avg Steps</p>
            <p className="stat-value">{avg.steps?.toLocaleString?.() ?? 0}</p>
          </article>
          <article>
            <p className="stat-label">Exercise / day</p>
            <p className="stat-value">
              {avg.exercise_minutes ?? 0}
              <span className="stat-unit"> min</span>
            </p>
          </article>
          <article>
            <p className="stat-label">Avg Sleep</p>
            <p className="stat-value">
              {avg.sleep_hours ?? 0}
              <span className="stat-unit"> hrs</span>
            </p>
          </article>
          <article>
            <p className="stat-label">Consistency</p>
            <p className="stat-value">{weekly?.consistency || '0/7'}</p>
          </article>
          <article>
            <p className="stat-label">Fitness Score</p>
            <p className="stat-value">{avg.fitness_score ?? 0}</p>
          </article>
        </div>

        <ProgressChart data={days} dataKey="fitness_score" label="Fitness Score" />
        <ProgressChart data={days} dataKey="steps" label="Steps" />
        <ProgressChart data={days} dataKey="exercise_minutes" label="Exercise (min)" />
        <ProgressChart data={days} dataKey="weight" label="Weight (kg)" />
      </main>
    </div>
  )
}
