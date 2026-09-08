function resolveApiBase() {
  const host = typeof window !== 'undefined' ? window.location.hostname : '127.0.0.1'
  return `http://${host}:8020`
}

const API_BASE = resolveApiBase()

export function getToken() {
  return localStorage.getItem('orbitz_token')
}

export function setToken(token) {
  localStorage.setItem('orbitz_token', token)
}

export function clearToken() {
  localStorage.removeItem('orbitz_token')
}

async function request(path, options = {}) {
  const headers = { ...(options.headers || {}) }
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`
  if (options.json) {
    headers['Content-Type'] = 'application/json'
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
    body: options.json ? JSON.stringify(options.json) : options.body,
  })

  if (!res.ok) {
    let detail = 'Request failed'
    try {
      const err = await res.json()
      detail = err.detail || detail
      if (Array.isArray(detail)) detail = detail.map((d) => d.msg).join(', ')
    } catch {
      /* ignore */
    }
    throw new Error(detail)
  }

  if (res.status === 204) return null
  return res.json()
}

async function download(path, filename) {
  const headers = {}
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`
  const res = await fetch(`${API_BASE}${path}`, { headers })
  if (!res.ok) {
    let detail = 'Download failed'
    try {
      const err = await res.json()
      detail = err.detail || detail
    } catch {
      /* ignore */
    }
    throw new Error(detail)
  }
  const blob = await res.blob()
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  link.remove()
  URL.revokeObjectURL(url)
}

export const api = {
  get: (path) => request(path),
  post: (path, json) => request(path, { method: 'POST', json }),
  put: (path, json) => request(path, { method: 'PUT', json }),
  download,
  postForm: (path, form) =>
    request(path, {
      method: 'POST',
      body: form,
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
}
