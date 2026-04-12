// Vitest global setup — runs once before all tests.
import { config } from '@vue/test-utils'
import { createI18n } from 'vue-i18n'
import { createPinia } from 'pinia'
import uz from '../src/i18n/uz.js'

const i18n = createI18n({
  legacy: false,
  locale: 'uz',
  fallbackLocale: 'uz',
  messages: { uz }
})

config.global.plugins = [i18n, createPinia()]
config.global.stubs = {
  RouterLink: { template: '<a><slot /></a>' },
  RouterView: true,
  Teleport: true,
  Transition: false,
  TransitionGroup: false
}

// localStorage is provided by happy-dom but ensure clean state
beforeEach(() => {
  localStorage.clear()
  document.documentElement.classList.remove('dark')
})
