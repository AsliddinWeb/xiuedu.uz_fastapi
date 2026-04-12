import { onMounted, onUnmounted } from 'vue'

/**
 * Adds an `animate-in` class to elements matching `selector` when they
 * scroll into view. Pairs with the `[data-animate]` CSS rule in main.css.
 *
 * IMPORTANT: handles BOTH initial and dynamically-added elements via
 * MutationObserver — critical for async-loaded content (news cards) and
 * v-if/tab-switched lists (program cards) that would otherwise stay hidden.
 *
 * Usage:
 *   <script setup>
 *   import { useScrollAnimation } from '@/composables/useScrollAnimation'
 *   useScrollAnimation()
 *   </script>
 *
 *   <div data-animate>...</div>
 *   <div data-animate data-delay="200">...</div>
 */
export function useScrollAnimation(selector = '[data-animate]') {
  let intersectionObserver = null
  let mutationObserver = null

  onMounted(() => {
    if (typeof window === 'undefined' || !('IntersectionObserver' in window)) return

    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (reduce) {
      document.querySelectorAll(selector).forEach(el => el.classList.add('animate-in'))
      return
    }

    intersectionObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in')
            intersectionObserver.unobserve(entry.target)
          }
        })
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    )

    const observeAll = () => {
      document.querySelectorAll(selector).forEach((el) => {
        if (!el.dataset.animateObserved) {
          el.dataset.animateObserved = '1'
          intersectionObserver.observe(el)
        }
      })
    }

    requestAnimationFrame(observeAll)

    // Watch for dynamically-added elements (async API loads, tab switches, v-if/v-for changes)
    if ('MutationObserver' in window) {
      mutationObserver = new MutationObserver(() => observeAll())
      mutationObserver.observe(document.body, { childList: true, subtree: true })
    }
  })

  onUnmounted(() => {
    intersectionObserver?.disconnect()
    mutationObserver?.disconnect()
  })
}
