import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const STORAGE_KEY = 'xiuedu_theme'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(false)
  const mode = computed(() => (isDark.value ? 'dark' : 'light'))

  function apply() {
    const root = document.documentElement
    root.classList.toggle('dark', isDark.value)
    root.style.colorScheme = isDark.value ? 'dark' : 'light'
  }

  function set(dark) {
    isDark.value = !!dark
    localStorage.setItem(STORAGE_KEY, isDark.value ? 'dark' : 'light')
    apply()
  }

  function toggle() {
    set(!isDark.value)
  }

  function init() {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved === 'dark' || saved === 'light') {
      isDark.value = saved === 'dark'
    } else {
      isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    apply()

    // Watch system preference (only when user hasn't set explicitly)
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (!localStorage.getItem(STORAGE_KEY)) {
        isDark.value = e.matches
        apply()
      }
    })
  }

  return { isDark, mode, set, toggle, init }
})
