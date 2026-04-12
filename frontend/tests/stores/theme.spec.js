import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useThemeStore } from '@/stores/theme'

describe('theme store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    document.documentElement.classList.remove('dark')
  })

  it('toggles isDark and applies dark class', () => {
    const store = useThemeStore()
    store.set(false)
    expect(store.isDark).toBe(false)
    store.toggle()
    expect(store.isDark).toBe(true)
    expect(document.documentElement.classList.contains('dark')).toBe(true)
  })

  it('persists choice to localStorage', () => {
    const store = useThemeStore()
    store.set(true)
    expect(localStorage.getItem('xiuedu_theme')).toBe('dark')
    store.set(false)
    expect(localStorage.getItem('xiuedu_theme')).toBe('light')
  })

  it('init() restores from localStorage', () => {
    localStorage.setItem('xiuedu_theme', 'dark')
    const store = useThemeStore()
    store.init()
    expect(store.isDark).toBe(true)
  })
})
