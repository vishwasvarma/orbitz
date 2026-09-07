import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import { useAuth } from '../context/AuthContext'
import ThemeToggle from '../components/ThemeToggle'

const GOALS = [
  { id: 'muscle_gain', title: 'Muscle Gain', desc: 'Build muscle and strength' },
  { id: 'weight_gain', title: 'Weight Gain', desc: 'Gain weight in a healthy way' },
  { id: 'weight_loss', title: 'Weight Loss', desc: 'Become more active and leaner' },
  { id: 'cardio', title: 'Cardio & Endurance', desc: 'Improve stamina' },
  { id: 'general', title: 'General Fitness', desc: 'Stay active and healthy' },
]

const LEVELS = ['beginner', 'intermediate', 'advanced']

export default function Onboarding() {
  const navigate = useNavigate()
  const { refreshUser } = useAuth()
  const [step, setStep] = useState(1)
  const [goal, setGoal] = useState('muscle_gain')
  const [level, setLevel] = useState('beginner')
  const [form, setForm] = useState({
    name: '',
    age: '',
    gender: 'male',
    height: '',
    weight: '',
  })
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const update = (key, value) => setForm((f) => ({ ...f, [key]: value }))

  const submit = async (e) => {
    e.preventDefault()
    setBusy(true)
    setError('')
    try {
      await api.post('/auth/onboarding', {
        name: form.name,
        age: Number(form.age),
        gender: form.gender,
        height: Number(form.height),
        weight: Number(form.weight),
        fitness_goal: goal,
        fitness_level: level,
      })
      await refreshUser()
      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="auth-shell onboarding">
      <div className="onboarding-theme">
        <ThemeToggle />
      </div>
      <div className="auth-card wide">
        <p className="eyebrow">Step {step} of 3</p>
        <h1>Set up Orbitz</h1>

        {step === 1 && (
          <>
            <p className="tagline">What is your main goal?</p>
            <div className="goal-grid">
              {GOALS.map((g) => (
                <button
                  key={g.id}
                  type="button"
                  className={`goal-card ${goal === g.id ? 'active' : ''}`}
                  onClick={() => setGoal(g.id)}
                >
                  <strong>{g.title}</strong>
                  <span>{g.desc}</span>
                </button>
              ))}
            </div>
            <button className="btn primary" onClick={() => setStep(2)}>
              Continue
            </button>
          </>
        )}

        {step === 2 && (
          <>
            <p className="tagline">What&apos;s your current fitness level?</p>
            <div className="level-row">
              {LEVELS.map((l) => (
                <button
                  key={l}
                  type="button"
                  className={`goal-card ${level === l ? 'active' : ''}`}
                  onClick={() => setLevel(l)}
                >
                  <strong>{l[0].toUpperCase() + l.slice(1)}</strong>
                </button>
              ))}
            </div>
            <div className="row-actions">
              <button className="btn ghost" onClick={() => setStep(1)}>
                Back
              </button>
              <button className="btn primary" onClick={() => setStep(3)}>
                Continue
              </button>
            </div>
          </>
        )}

        {step === 3 && (
          <form onSubmit={submit}>
            <p className="tagline">Personal details</p>
            <label>
              Name
              <input value={form.name} onChange={(e) => update('name', e.target.value)} required />
            </label>
            <div className="form-row">
              <label>
                Age
                <input
                  type="number"
                  value={form.age}
                  onChange={(e) => update('age', e.target.value)}
                  required
                />
              </label>
              <label>
                Gender
                <select value={form.gender} onChange={(e) => update('gender', e.target.value)}>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </label>
            </div>
            <div className="form-row">
              <label>
                Height (cm)
                <input
                  type="number"
                  step="0.1"
                  value={form.height}
                  onChange={(e) => update('height', e.target.value)}
                  required
                />
              </label>
              <label>
                Weight (kg)
                <input
                  type="number"
                  step="0.1"
                  value={form.weight}
                  onChange={(e) => update('weight', e.target.value)}
                  required
                />
              </label>
            </div>
            {error ? <p className="error">{error}</p> : null}
            <div className="row-actions">
              <button type="button" className="btn ghost" onClick={() => setStep(2)}>
                Back
              </button>
              <button className="btn primary" disabled={busy}>
                {busy ? 'Saving…' : 'Go to Dashboard'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}
