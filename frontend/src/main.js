import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import i18n from './i18n'
import { useThemeStore } from './stores/theme'
import { useLanguageStore } from './stores/language'
import { initAnalytics } from './plugins/analytics'
import './assets/main.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(i18n)

// ===== Global directives =====

/**
 * v-click-outside — calls the bound handler when a click occurs
 * outside the element. Useful for dropdowns, popovers, drawers.
 *
 * Usage:  <div v-click-outside="close">...</div>
 */
app.directive('click-outside', {
  beforeMount(el, binding) {
    el._clickOutsideHandler = (e) => {
      if (!el.contains(e.target)) binding.value(e)
    }
    document.addEventListener('click', el._clickOutsideHandler, true)
  },
  unmounted(el) {
    document.removeEventListener('click', el._clickOutsideHandler, true)
  }
})

/**
 * v-tooltip — simple native title tooltip on hover.
 * Usage: <button v-tooltip="'Label'">...</button>
 * Passing empty string disables it.
 */
app.directive('tooltip', {
  mounted(el, binding) {
    if (binding.value) el.setAttribute('title', binding.value)
  },
  updated(el, binding) {
    if (binding.value) el.setAttribute('title', binding.value)
    else el.removeAttribute('title')
  }
})

// Initialize theme and language from persisted storage
useThemeStore().init()
useLanguageStore().init()

// Analytics: load only if user has previously granted consent
initAnalytics(router)

app.mount('#app')
