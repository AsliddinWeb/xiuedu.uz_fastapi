import { ref, onMounted, onBeforeUnmount } from 'vue'

/**
 * useCountUp — IntersectionObserver-triggered number counter.
 *
 * Usage:
 *   <template>
 *     <span ref="el">{{ displayValue.toLocaleString() }}{{ suffix }}</span>
 *   </template>
 *
 *   <script setup>
 *   import { useCountUp } from '@/composables/useCountUp'
 *   const { el, displayValue, suffix } = useCountUp(5000, { suffix: '+', duration: 2000 })
 *   </script>
 *
 * Honors prefers-reduced-motion (jumps straight to target).
 */
export function useCountUp(target, { duration = 2000, suffix = '' } = {}) {
  const el = ref(null)
  const displayValue = ref(0)
  let observer = null
  let rafId = null
  let fired = false

  function animate() {
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (reduce) {
      displayValue.value = target
      return
    }
    const start = performance.now()
    const step = (now) => {
      const p = Math.min((now - start) / duration, 1)
      const eased = 1 - Math.pow(1 - p, 3) // ease-out cubic
      displayValue.value = Math.round(eased * target)
      if (p < 1) rafId = requestAnimationFrame(step)
      else displayValue.value = target
    }
    rafId = requestAnimationFrame(step)
  }

  onMounted(() => {
    if (!el.value || typeof IntersectionObserver === 'undefined') {
      displayValue.value = target
      return
    }
    observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !fired) {
          fired = true
          animate()
          observer.disconnect()
        }
      },
      { threshold: 0.4 }
    )
    observer.observe(el.value)
  })

  onBeforeUnmount(() => {
    observer?.disconnect()
    if (rafId) cancelAnimationFrame(rafId)
  })

  return { el, displayValue, suffix }
}
