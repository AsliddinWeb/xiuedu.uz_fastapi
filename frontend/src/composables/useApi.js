import { ref, shallowRef } from 'vue'
import api from '@/api/client'

/**
 * Lightweight fetch wrapper with reactive loading/error/data state.
 *
 * @example
 * const { data, loading, error, run } = useApi(() => api.get('/news/'))
 * onMounted(run)
 */
export function useApi(fetcher, { immediate = false } = {}) {
  const data = shallowRef(null)
  const error = shallowRef(null)
  const loading = ref(false)

  async function run(...args) {
    loading.value = true
    error.value = null
    try {
      const res = await fetcher(...args)
      data.value = res?.data ?? res
      return data.value
    } catch (e) {
      error.value = e
      throw e
    } finally {
      loading.value = false
    }
  }

  if (immediate) run()

  return { data, error, loading, run }
}

export { api }
