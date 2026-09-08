import { useEffect, useState } from 'react'
import Navbar from '../components/Navbar'
import ProgressChart from '../components/ProgressChart'
import Loading from '../components/Loading'
import { api } from '../services/api'

export default function Progress() {
  const [weekly, setWeekly] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [downloading, setDownloading] = useState('')

  useEffect(() => {
    api
      .get('/progress/weekly')
      .then(setWeekly)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  const downloadReport = async (path, filename, key) => {
    setDownloading(key)
    setError('')
    try {
      await api.download(path, filename)
    } catch (e) {
      setError(e.message)
    } finally {
      setDownloading('')
    }
  }

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

        <div className="dash-cta report-actions">
          <button
            type="button"
            className="btn primary"
            disabled={Boolean(downloading)}
            onClick={() => downloadReport('/progress/weekly.pdf', 'orbitz-weekly-report.pdf', 'weekly')}
          >
            {downloading === 'weekly' ? 'Preparing…' : 'Download weekly PDF'}
          </button>
          <button
            type="button"
            className="btn ghost"
            disabled={Boolean(downloading)}
            onClick={() => downloadReport('/progress/three-day.pdf', 'orbitz-3-day-report.pdf', 'three')}
          >
            {downloading === 'three' ? 'Preparing…' : 'Download 3-day PDF'}
          </button>
        </div>

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

        <ProgressChart data={days} dataKey="fitness_score" label="Fitness Score" color="#3ea6ff" />
        <ProgressChart data={days} dataKey="steps" label="Steps" color="#3ecf8e" />
        <ProgressChart data={days} dataKey="exercise_minutes" label="Exercise (min)" color="#ffae00" />
        <ProgressChart data={days} dataKey="weight" label="Weight (kg)" color="#ff4e45" />
      </main>
    </div>
  )
}
