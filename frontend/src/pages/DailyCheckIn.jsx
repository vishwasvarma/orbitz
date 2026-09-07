import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import { api } from '../services/api'
import { useAuth } from '../context/AuthContext'

const TYPES = ['Walking', 'Running', 'Gym', 'Cycling', 'Sports', 'Yoga', 'Other']

export default function DailyCheckIn() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    weight: user?.weight || '',
    steps: '',
    exercise_minutes: '',
    exercise_intensity: 'moderate',
    exercise_types: [],
    sleep_hours: '',
    water_liters: '',
    sitting_hours: '',
    feeling: 'normal',
  })

  const update = (key, value) => setForm((f) => ({ ...f, [key]: value }))

  const toggleType = (t) => {
    setForm((f) => {
      const has = f.exercise_types.includes(t)
      return {
        ...f,
        exercise_types: has
          ? f.exercise_types.filter((x) => x !== t)
          : [...f.exercise_types, t],
      }
    })
  }

  const onSubmit = async (e) => {
    e.preventDefault()
    setBusy(true)
    setError('')
    try {
      await api.post('/activity', {
        weight: Number(form.weight),
        steps: Number(form.steps),
        exercise_minutes: Number(form.exercise_minutes),
        exercise_intensity: form.exercise_intensity,
        exercise_types: form.exercise_types,
        sleep_hours: Number(form.sleep_hours),
        water_liters: Number(form.water_liters),
        sitting_hours: Number(form.sitting_hours || 0),
        feeling: form.feeling,
      })
      navigate('/tomorrow-plan')
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="page">
      <Navbar />
      <main className="form-page">
        <h1>Daily Check-in</h1>
        <p className="tagline">Tell Orbitz how today went — we&apos;ll build tomorrow&apos;s plan.</p>

        <form className="checkin-form" onSubmit={onSubmit}>
          <label>
            Today&apos;s weight (kg)
            <input
              type="number"
              step="0.1"
              value={form.weight}
              onChange={(e) => update('weight', e.target.value)}
              required
            />
          </label>
          <label>
            Steps
            <input
              type="number"
              value={form.steps}
              onChange={(e) => update('steps', e.target.value)}
              required
            />
          </label>
          <label>
            Exercise minutes
            <input
              type="number"
              value={form.exercise_minutes}
              onChange={(e) => update('exercise_minutes', e.target.value)}
              required
            />
          </label>

          <fieldset>
            <legend>Exercise intensity</legend>
            {['light', 'moderate', 'high'].map((v) => (
              <label key={v} className="radio">
                <input
                  type="radio"
                  name="intensity"
                  checked={form.exercise_intensity === v}
                  onChange={() => update('exercise_intensity', v)}
                />
                {v}
              </label>
            ))}
          </fieldset>

          <fieldset>
            <legend>Exercise type</legend>
            <div className="chip-grid">
              {TYPES.map((t) => (
                <button
                  key={t}
                  type="button"
                  className={`chip-btn ${form.exercise_types.includes(t) ? 'active' : ''}`}
                  onClick={() => toggleType(t)}
                >
                  {t}
                </button>
              ))}
            </div>
          </fieldset>

          <label>
            Sleep hours
            <input
              type="number"
              step="0.1"
              value={form.sleep_hours}
              onChange={(e) => update('sleep_hours', e.target.value)}
              required
            />
          </label>
          <label>
            Water (litres)
            <input
              type="number"
              step="0.1"
              value={form.water_liters}
              onChange={(e) => update('water_liters', e.target.value)}
              required
            />
          </label>
          <label>
            Sitting hours
            <input
              type="number"
              step="0.1"
              value={form.sitting_hours}
              onChange={(e) => update('sitting_hours', e.target.value)}
            />
          </label>

          <fieldset>
            <legend>How do you feel today?</legend>
            {['tired', 'normal', 'energetic'].map((v) => (
              <label key={v} className="radio">
                <input
                  type="radio"
                  name="feeling"
                  checked={form.feeling === v}
                  onChange={() => update('feeling', v)}
                />
                {v}
              </label>
            ))}
          </fieldset>

          {error ? <p className="error">{error}</p> : null}
          <button className="btn primary" disabled={busy}>
            {busy ? 'Generating plan…' : "Generate Tomorrow's Plan →"}
          </button>
        </form>
      </main>
    </div>
  )
}
