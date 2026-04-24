import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/client'

export const useSiteSettingsStore = defineStore('siteSettings', () => {
  const data = ref(null)
  const loading = ref(false)
  const loaded = ref(false)

  const logoUrl     = computed(() => data.value?.logo_url || null)
  const logoDarkUrl = computed(() => data.value?.logo_dark_url || data.value?.logo_url || null)
  const faviconUrl  = computed(() => data.value?.favicon_url || null)
  const siteName    = computed(() => data.value?.site_name || null)
  const shortName   = computed(() => data.value?.site_short_name || null)

  async function ensureLoaded(force = false) {
    if (loaded.value && !force) return data.value
    if (loading.value) return data.value
    loading.value = true
    try {
      const res = await api.get('/site-settings/')
      data.value = res.data
      loaded.value = true
    } catch {
      data.value = null
    } finally {
      loading.value = false
    }
    return data.value
  }

  return { data, loading, loaded, logoUrl, logoDarkUrl, faviconUrl, siteName, shortName, ensureLoaded }
})
