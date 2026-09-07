import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'
import Loading from './components/Loading'
import AuthLock from './components/AuthLock'
import Login from './pages/Login'
import Register from './pages/Register'
import Onboarding from './pages/Onboarding'
import Dashboard from './pages/Dashboard'
import DailyCheckIn from './pages/DailyCheckIn'
import TomorrowPlan from './pages/TomorrowPlan'
import Progress from './pages/Progress'

function Protected({ children, requireOnboarding = true }) {
  const { user, loading } = useAuth()
  if (loading) return <Loading />
  if (!user) return <Navigate to="/login" replace />
  if (requireOnboarding && !user.onboarding_complete) {
    return <Navigate to="/onboarding" replace />
  }
  if (!requireOnboarding && user.onboarding_complete) {
    return <Navigate to="/dashboard" replace />
  }
  return children
}

function PublicOnly({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <Loading />
  if (user) {
    return (
      <Navigate
        to={user.onboarding_complete ? '/dashboard' : '/onboarding'}
        replace
      />
    )
  }
  return children
}

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Navigate to="/login" replace />} />
            <Route
              path="/login"
              element={
                <AuthLock>
                  <PublicOnly>
                    <Login />
                  </PublicOnly>
                </AuthLock>
              }
            />
            <Route
              path="/register"
              element={
                <AuthLock>
                  <PublicOnly>
                    <Register />
                  </PublicOnly>
                </AuthLock>
              }
            />
            <Route
              path="/onboarding"
              element={
                <Protected requireOnboarding={false}>
                  <Onboarding />
                </Protected>
              }
            />
            <Route
              path="/dashboard"
              element={
                <Protected>
                  <Dashboard />
                </Protected>
              }
            />
            <Route
              path="/daily-checkin"
              element={
                <Protected>
                  <DailyCheckIn />
                </Protected>
              }
            />
            <Route
              path="/tomorrow-plan"
              element={
                <Protected>
                  <TomorrowPlan />
                </Protected>
              }
            />
            <Route
              path="/progress"
              element={
                <Protected>
                  <Progress />
                </Protected>
              }
            />
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  )
}
