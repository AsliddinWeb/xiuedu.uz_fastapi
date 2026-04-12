import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import i18n, { loadLocale } from '@/i18n'

const STORAGE_KEY = 'xiuedu_locale'

export const LANGUAGES = [
  { code: 'uz', label: "O'zbekcha", short: 'UZ', flag: '🇺🇿' },
  { code: 'ru', label: 'Русский',   short: 'RU', flag: '🇷🇺' },
  { code: 'en', label: 'English',   short: 'EN', flag: '🇬🇧' }
]

const SUPPORTED = LANGUAGES.map(l => l.code)

export const useLanguageStore = defineStore('language', () => {
  const current = ref('uz')

  const currentLang = computed(() =>
    LANGUAGES.find(l => l.code === current.value) || LANGUAGES[0]
  )

  async function setLanguage(code) {
    if (!SUPPORTED.includes(code)) return
    await loadLocale(code)
    current.value = code
    i18n.global.locale.value = code
    localStorage.setItem(STORAGE_KEY, code)
    document.documentElement.setAttribute('lang', code)
  }

  function init() {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved && SUPPORTED.includes(saved)) {
      setLanguage(saved)
      return
    }
    const nav = (navigator.language || 'uz').slice(0, 2).toLowerCase()
    setLanguage(SUPPORTED.includes(nav) ? nav : 'uz')
  }

  return { current, currentLang, languages: LANGUAGES, setLanguage, init }
})
