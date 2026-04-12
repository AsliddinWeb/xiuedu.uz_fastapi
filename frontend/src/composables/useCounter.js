import { ref, watch } from 'vue'

/**
 * Animate a number from 0 to target over duration ms.
 * @param {import('vue').Ref<boolean>} startRef
 */
export function useCounter(target, startRef, duration = 1500) {
  const value = ref(0)
  watch(
    startRef,
    (start) => {
      if (!start) return
      const t0 = performance.now()
      const tick = (now) => {
        const p = Math.min((now - t0) / duration, 1)
        value.value = Math.floor(target * (1 - Math.pow(1 - p, 3)))
        if (p < 1) requestAnimationFrame(tick)
      }
      requestAnimationFrame(tick)
    },
    { immediate: true }
  )
  return value
}
