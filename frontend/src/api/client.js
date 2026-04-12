import axios from 'axios'
import { useLanguageStore } from '@/stores/language'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 15000
})

// ===== Request: lang + token =====
api.interceptors.request.use((config) => {
  try {
    const lang = useLanguageStore().current
    config.params = { ...(config.params || {}), lang }
    config.headers['Accept-Language'] = lang
  } catch (_) { /* store may not be ready */ }
  const token = localStorage.getItem('xiuedu_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// ===== Response: 401 → refresh & retry once; toast on errors =====
let refreshPromise = null

async function refreshToken() {
  const refresh = localStorage.getItem('xiuedu_refresh')
  if (!refresh) throw new Error('no refresh token')
  const res = await axios.post(
    (import.meta.env.VITE_API_BASE_URL || '/api') + '/auth/refresh',
    { refresh_token: refresh }
  )
  const newToken = res.data.access_token
  localStorage.setItem('xiuedu_token', newToken)
  try { useAuthStore().setToken(newToken) } catch (_) {}
  return newToken
}

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const cfg = error.config || {}
    const status = error.response?.status

    // Auto-refresh once
    if (status === 401 && !cfg._retry && !cfg.url?.includes('/auth/')) {
      cfg._retry = true
      try {
        if (!refreshPromise) refreshPromise = refreshToken().finally(() => { refreshPromise = null })
        const newToken = await refreshPromise
        cfg.headers.Authorization = `Bearer ${newToken}`
        return api(cfg)
      } catch (_) {
        try { useAuthStore().logout() } catch (_) {}
      }
    }

    // Toast
    if (!cfg._silent) {
      try {
        const toast = useToastStore()
        if (status === 401)      toast.show('Avtorizatsiya talab qilinadi', { type: 'warning' })
        else if (status === 403) toast.show('Sizda ruxsat yo\'q', { type: 'warning' })
        else if (status === 404) toast.show('Topilmadi', { type: 'info' })
        else if (status >= 500)  toast.show('Server xatoligi', { type: 'error' })
        else if (!error.response) toast.show('Tarmoq xatoligi', { type: 'error' })
      } catch (_) {}
    }

    return Promise.reject(error)
  }
)

export default api
