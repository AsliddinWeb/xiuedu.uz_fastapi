import { ref } from 'vue'
import { useIntersectionObserver } from '@vueuse/core'

/**
 * Reveal-on-scroll composable.
 * Returns: { target, visible }
 * Usage:
 *   const { target, visible } = useReveal()
 *   <div ref="target" :class="visible && 'animate-slide-up'">
 */
export function useReveal(options = {}) {
  const target = ref(null)
  const visible = ref(false)
  const { stop } = useIntersectionObserver(
    target,
    ([entry]) => {
      if (entry?.isIntersecting) {
        visible.value = true
        stop()
      }
    },
    { threshold: 0.15, ...options }
  )
  return { target, visible }
}
