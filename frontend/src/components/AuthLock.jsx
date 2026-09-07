import { useEffect } from 'react'

export default function AuthLock({ children }) {
  useEffect(() => {
    document.documentElement.setAttribute('data-auth-page', 'true')
    return () => document.documentElement.removeAttribute('data-auth-page')
  }, [])

  return children
}
