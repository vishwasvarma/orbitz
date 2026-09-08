import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import { api } from '../services/api'
import { useAuth } from '../context/AuthContext'

const TYPES = ['Walking', 'Running', 'Gym', 'Cycling', 'Sports', 'Yoga', 'Other']

const MEDICAL = [
  { id: 'knee_pain', label: 'Knee pain' },
  { id: 'back_pain', label: 'Lower back pain' },
  { id: 'shoulder_pain', label: 'Shoulder pain' },
  { id: 'wrist_pain', label: 'Wrist pain' },
  { id: 'ankle_pain', label: 'Ankle / foot pain' },
  { id: 'hip_pain', label: 'Hip pain' },
  { id: 'neck_pain', label: 'Neck pain' },
  { id: 'heart_condition', label: 'Heart condition' },
  { id: 'asthma', label: 'Asthma / breathing' },
  { id: 'high_blood_pressure', label: 'High blood pressure' },
  { id: 'recent_surgery', label: 'Recent injury / surgery' },
  { id: 'dizziness', label: 'Dizziness' },
]

const ALLERGY_CHIPS = ['Peanuts', 'Nuts', 'Dairy', 'Eggs', 'Gluten', 'Soy', 'Fish', 'Chicken', 'Shellfish']

export default function DailyCheckIn() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [allergyDraft, setAllergyDraft] = useState('')
  const [form, setForm] = useState({
    weight: user?.weight || '',
    steps: '',
    exercise_minutes: '',
    exercise_intensity: 'moderate',
    exercise_types: [],
    exercise_breakdown: {},
    sleep_hours: '',
    water_liters: '',
    sitting_hours: '',
    feeling: 'normal',
    medical_constraints: [],
    diet_preference: '',
    food_allergies: [],
  })

  useEffect(() => {
    api
      .get('/activity/today')
      .then((today) => {
        if (!today) return
        setForm((f) => ({
          ...f,
          weight: today.weight ?? f.weight,
          steps: today.steps ?? '',
          exercise_minutes: today.exercise_minutes ?? '',
          exercise_intensity: today.exercise_intensity || 'moderate',
          exercise_types: today.exercise_types || [],
          exercise_breakdown: today.exercise_breakdown || {},
          sleep_hours: today.sleep_hours ?? '',
          water_liters: today.water_liters ?? '',
          sitting_hours: today.sitting_hours ?? '',
          feeling: today.feeling || 'normal',
          medical_constraints: today.medical_constraints || [],
          diet_preference: today.diet_preference || '',
          food_allergies: today.food_allergies || [],
        }))
      })
      .catch(() => {})
  }, [])

  const update = (key, value) => setForm((f) => ({ ...f, [key]: value }))

  const toggleType = (t) => {
    setForm((f) => {
      const has = f.exercise_types.includes(t)
      const nextTypes = has ? f.exercise_types.filter((x) => x !== t) : [...f.exercise_types, t]
      const nextBreakdown = { ...f.exercise_breakdown }
      if (has) delete nextBreakdown[t]
      else if (nextBreakdown[t] == null) nextBreakdown[t] = ''
      return { ...f, exercise_types: nextTypes, exercise_breakdown: nextBreakdown }
    })
  }

  const toggleChip = (key, value) => {
    setForm((f) => {
      const list = f[key]
      const has = list.includes(value)
      return { ...f, [key]: has ? list.filter((x) => x !== value) : [...list, value] }
    })
  }

  const addAllergy = () => {
    const value = allergyDraft.trim()
    if (!value) return
    setForm((f) => ({
      ...f,
      food_allergies: f.food_allergies.includes(value) ? f.food_allergies : [...f.food_allergies, value],
    }))
    setAllergyDraft('')
  }

  const breakdownTotal = useMemo(() => {
    return Object.values(form.exercise_breakdown).reduce((sum, mins) => sum + (Number(mins) || 0), 0)
  }, [form.exercise_breakdown])

  const onSubmit = async (e) => {
    e.preventDefault()
    if (!form.diet_preference) {
      setError('Choose whether tomorrow is veg or non-veg')
      return
    }
    setBusy(true)
    setError('')
    const breakdown = {}
    for (const [name, mins] of Object.entries(form.exercise_breakdown)) {
      const n = Number(mins)
      if (n > 0) breakdown[name] = n
    }
    try {
      await api.post('/activity', {
        weight: Number(form.weight),
        steps: Number(form.steps),
        exercise_minutes: breakdownTotal || Number(form.exercise_minutes || 0),
        exercise_intensity: form.exercise_intensity,
        exercise_types: form.exercise_types,
        exercise_breakdown: breakdown,
        sleep_hours: Number(form.sleep_hours),
        water_liters: Number(form.water_liters),
        sitting_hours: Number(form.sitting_hours || 0),
        feeling: form.feeling,
        medical_constraints: form.medical_constraints,
        diet_preference: form.diet_preference,
        food_allergies: form.food_allergies,
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

          <fieldset>
            <legend>Exercise you did today</legend>
            <p className="hint">Pick each activity and enter the minutes for it. Total is calculated for you.</p>
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
            {form.exercise_types.length ? (
              <div className="activity-mins">
                {form.exercise_types.map((t) => (
                  <label key={t}>
                    {t} (minutes)
                    <input
                      type="number"
                      min="0"
                      value={form.exercise_breakdown[t] ?? ''}
                      onChange={(e) =>
                        setForm((f) => ({
                          ...f,
                          exercise_breakdown: { ...f.exercise_breakdown, [t]: e.target.value },
                        }))
                      }
                    />
                  </label>
                ))}
                <p className="total-mins">Total exercise: {breakdownTotal} min</p>
              </div>
            ) : (
              <label>
                Total exercise minutes
                <input
                  type="number"
                  value={form.exercise_minutes}
                  onChange={(e) => update('exercise_minutes', e.target.value)}
                />
              </label>
            )}
          </fieldset>

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

          <fieldset>
            <legend>Medical constraints</legend>
            <p className="hint">These exercises will be left out of tomorrow&apos;s plan.</p>
            <div className="chip-grid">
              {MEDICAL.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  className={`chip-btn ${form.medical_constraints.includes(item.id) ? 'active' : ''}`}
                  onClick={() => toggleChip('medical_constraints', item.id)}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </fieldset>

          <fieldset>
            <legend>Tomorrow, will you eat veg or non-veg?</legend>
            <p className="hint">Your diet plan is built from this choice every day.</p>
            {['veg', 'non_veg'].map((v) => (
              <label key={v} className="radio">
                <input
                  type="radio"
                  name="diet"
                  checked={form.diet_preference === v}
                  onChange={() => update('diet_preference', v)}
                  required
                />
                {v === 'veg' ? 'Vegetarian' : 'Non-vegetarian'}
              </label>
            ))}
          </fieldset>

          <fieldset>
            <legend>Food allergies to exclude</legend>
            <div className="chip-grid">
              {ALLERGY_CHIPS.map((item) => (
                <button
                  key={item}
                  type="button"
                  className={`chip-btn ${form.food_allergies.includes(item) ? 'active' : ''}`}
                  onClick={() => toggleChip('food_allergies', item)}
                >
                  {item}
                </button>
              ))}
              {form.food_allergies
                .filter((item) => !ALLERGY_CHIPS.includes(item))
                .map((item) => (
                  <button
                    key={item}
                    type="button"
                    className="chip-btn active"
                    onClick={() => toggleChip('food_allergies', item)}
                  >
                    {item} ×
                  </button>
                ))}
            </div>
            <div className="allergy-add">
              <input
                type="text"
                placeholder="Other allergy"
                value={allergyDraft}
                onChange={(e) => setAllergyDraft(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault()
                    addAllergy()
                  }
                }}
              />
              <button type="button" className="btn ghost" onClick={addAllergy}>
                Add
              </button>
            </div>
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
