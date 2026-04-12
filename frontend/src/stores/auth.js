import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/client'

const TOKEN_KEY = 'xiuedu_token'
const REFRESH_KEY = 'xiuedu_refresh'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem(TOKEN_KEY) || null)
  const refreshToken = ref(localStorage.getItem(REFRESH_KEY) || null)
  const user = ref(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value)
  const role = computed(() => user.value?.role || null)

  function hasRole(...allowed) {
    if (!user.value) return false
    if (user.value.role === 'superadmin') return true
    return allowed.includes(user.value.role)
  }

  function setToken(t, r) {
    token.value = t
    if (t) localStorage.setItem(TOKEN_KEY, t)
    else localStorage.removeItem(TOKEN_KEY)
    if (r !== undefined) {
      refreshToken.value = r
      if (r) localStorage.setItem(REFRESH_KEY, r)
      else localStorage.removeItem(REFRESH_KEY)
    }
  }

  function setUser(u) { user.value = u }

  async function login(email, password) {
    loading.value = true
    try {
      const res = await api.post('/auth/login', { email, password }, { _silent: true })
      setToken(res.data.access_token, res.data.refresh_token)
      setUser(res.data.user)
      return res.data.user
    } finally {
      loading.value = false
    }
  }

  async function loadMe() {
    if (!token.value) return null
    try {
      const res = await api.get('/auth/me', { _silent: true })
      setUser(res.data)
      return res.data
    } catch (_) {
      logout()
      return null
    }
  }

  async function logout() {
    try { await api.post('/auth/logout', null, { _silent: true }) } catch (_) {}
    setToken(null, null)
    setUser(null)
  }

  return { token, refreshToken, user, loading, isAuthenticated, role, hasRole, setToken, setUser, login, loadMe, logout }
})
