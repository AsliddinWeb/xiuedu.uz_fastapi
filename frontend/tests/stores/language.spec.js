import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useLanguageStore } from '@/stores/language'

describe('language store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  it('has 3 supported languages', () => {
    const store = useLanguageStore()
    expect(store.languages.map(l => l.code)).toEqual(['uz', 'ru', 'en'])
  })

  it('setLanguage updates current and html lang', async () => {
    const store = useLanguageStore()
    await store.setLanguage('en')
    expect(store.current).toBe('en')
    expect(document.documentElement.getAttribute('lang')).toBe('en')
    expect(localStorage.getItem('xiuedu_locale')).toBe('en')
  })

  it('rejects unsupported language', async () => {
    const store = useLanguageStore()
    store.current = 'uz'
    await store.setLanguage('fr')
    expect(store.current).toBe('uz')
  })
})
