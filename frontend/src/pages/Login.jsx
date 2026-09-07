import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const onSubmit = async (e) => {
    e.preventDefault()
    setBusy(true)
    setError('')
    try {
      const me = await login(username.trim(), password)
      if (!me?.onboarding_complete) navigate('/onboarding')
      else navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="auth-shell">
      <form className="auth-card" onSubmit={onSubmit}>
        <p className="eyebrow">Welcome back</p>
        <h1>Orbitz</h1>
        <p className="tagline">Your personal fitness AI</p>

        <label>
          Username
          <input value={username} onChange={(e) => setUsername(e.target.value)} required />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>

        {error ? <p className="error">{error}</p> : null}
        <button className="btn primary" disabled={busy}>
          {busy ? 'Signing in…' : 'Login'}
        </button>

        <p className="auth-foot">
          New to Orbitz? <Link to="/register">Let&apos;s Begin</Link>
        </p>
      </form>
    </div>
  )
}
