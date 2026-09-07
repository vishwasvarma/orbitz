import { NavLink, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import ThemeToggle from './ThemeToggle'

export default function Navbar() {
  const { logout, user } = useAuth()
  const navigate = useNavigate()
  const [open, setOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="nav">
      <div className="nav-inner">
        <NavLink to="/dashboard" className="brand">
          Orbitz
        </NavLink>
        <button className="nav-toggle" onClick={() => setOpen((v) => !v)} aria-label="Menu">
          ☰
        </button>
        <nav className={`nav-links ${open ? 'open' : ''}`}>
          <NavLink to="/dashboard" onClick={() => setOpen(false)}>
            Dashboard
          </NavLink>
          <NavLink to="/daily-checkin" onClick={() => setOpen(false)}>
            Daily Check-in
          </NavLink>
          <NavLink to="/progress" onClick={() => setOpen(false)}>
            Progress
          </NavLink>
          <ThemeToggle />
          <button className="linkish" onClick={handleLogout}>
            Logout{user?.username ? ` (${user.username})` : ''}
          </button>
        </nav>
      </div>
    </header>
  )
}
