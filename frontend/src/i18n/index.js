import { createI18n } from 'vue-i18n'
import uz from './uz'

/**
 * vue-i18n in Composition API mode.
 * - Uzbek loaded eagerly (default + fallback)
 * - Russian / English loaded on demand via loadLocale()
 */
const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: 'uz',
  fallbackLocale: 'uz',
  silentTranslationWarn: true,
  silentFallbackWarn: true,
  messages: { uz }
})

const loaders = {
  ru: () => import('./ru.js'),
  en: () => import('./en.js')
}

const loaded = new Set(['uz'])

export async function loadLocale(code) {
  if (loaded.has(code) || !loaders[code]) return
  const mod = await loaders[code]()
  i18n.global.setLocaleMessage(code, mod.default || mod)
  loaded.add(code)
}

// Restore saved locale on boot
const saved = (typeof localStorage !== 'undefined') && localStorage.getItem('xiuedu_locale')
if (saved && saved !== 'uz') {
  loadLocale(saved).then(() => { i18n.global.locale.value = saved })
}

export default i18n
