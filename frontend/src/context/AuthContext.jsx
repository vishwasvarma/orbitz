import { createContext, useContext, useEffect, useState } from 'react'
import { api, setToken, clearToken, getToken } from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const refreshUser = async () => {
    if (!getToken()) {
      setUser(null)
      setLoading(false)
      return null
    }
    try {
      const me = await api.get('/auth/me')
      setUser(me)
      return me
    } catch {
      clearToken()
      setUser(null)
      return null
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    refreshUser()
  }, [])

  const login = async (username, password) => {
    const form = new URLSearchParams()
    form.set('username', username)
    form.set('password', password)
    const data = await api.postForm('/auth/login', form)
    setToken(data.access_token)
    const me = await refreshUser()
    return me
  }

  const register = async (username, password) => {
    const data = await api.post('/auth/register', { username, password })
    setToken(data.access_token)
    const me = await refreshUser()
    return me
  }

  const logout = () => {
    clearToken()
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refreshUser, setUser }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
