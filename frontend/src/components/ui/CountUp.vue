<script setup>
/**
 * Animated number counter — counts from 0 → end when scrolled into view.
 *
 * Props:
 *   end      Number  — target value
 *   suffix   String  — appended after the number (e.g. '+', '%')
 *   duration Number  — animation duration in ms (default 2000)
 *
 * Honors prefers-reduced-motion (jumps straight to end).
 */
import { ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  end:      { type: Number, required: true },
  suffix:   { type: String, default: '' },
  duration: { type: Number, default: 2000 }
})

const root = ref(null)
const displayed = ref(0)
let observer = null
let triggered = false
let raf = null

function animateCount() {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduce) { displayed.value = props.end; return }

  const start = performance.now()
  function step(now) {
    const elapsed = now - start
    const progress = Math.min(elapsed / props.duration, 1)
    const eased = 1 - Math.pow(1 - progress, 3) // ease-out cubic
    displayed.value = Math.round(eased * props.end)
    if (progress < 1) raf = requestAnimationFrame(step)
    else displayed.value = props.end
  }
  raf = requestAnimationFrame(step)
}

onMounted(() => {
  if (!root.value || typeof IntersectionObserver === 'undefined') {
    displayed.value = props.end
    return
  }
  observer = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting && !triggered) {
      triggered = true
      animateCount()
      observer.disconnect()
    }
  }, { threshold: 0.5 })
  observer.observe(root.value)
})

onBeforeUnmount(() => {
  observer?.disconnect()
  if (raf) cancelAnimationFrame(raf)
})

function format(n) {
  return n.toLocaleString('en-US')
}
</script>

<template>
  <span ref="root" class="tabular-nums">{{ format(displayed) }}{{ suffix }}</span>
</template>
