<script setup>
/**
 * SEO + CWV friendly <img> wrapper.
 *
 * - Required: src, alt, width, height (prevents CLS)
 * - Native lazy loading by default; eager for LCP/hero images
 * - Optional WebP fallback via <picture> when `webp` is set
 * - Optional LQIP blur-up: pass `placeholder` (data:image/...) for blur effect
 * - Sets `decoding="async"` and `fetchpriority` for hero
 */
import { ref, computed } from 'vue'

const props = defineProps({
  src:    { type: String, required: true },
  alt:    { type: String, required: true },
  width:  { type: [Number, String], required: true },
  height: { type: [Number, String], required: true },
  webp:   { type: String, default: null },
  placeholder: { type: String, default: null }, // data URL or tiny URL
  eager:  { type: Boolean, default: false },    // for LCP / hero
  rounded: { type: String, default: '' },       // tailwind class, e.g. 'rounded-xl'
  cover:  { type: Boolean, default: false },
  alwaysShowSrc: { type: Boolean, default: false }
})

const loaded = ref(false)
function onLoad() { loaded.value = true }

const ratio = computed(() => `${props.width} / ${props.height}`)
const objectFit = computed(() => (props.cover ? 'object-cover' : 'object-contain'))
const loadingAttr = computed(() => (props.eager ? 'eager' : 'lazy'))
const fetchPriority = computed(() => (props.eager ? 'high' : 'auto'))
</script>

<template>
  <div
    :class="['relative overflow-hidden bg-neutral-100 dark:bg-primary-900', rounded]"
    :style="{ aspectRatio: ratio }"
  >
    <!-- LQIP blur-up -->
    <img
      v-if="placeholder"
      :src="placeholder"
      :alt="alt"
      aria-hidden="true"
      :class="['absolute inset-0 w-full h-full transition-opacity duration-500 blur-xl scale-110', objectFit, loaded && !alwaysShowSrc ? 'opacity-0' : 'opacity-100']"
    />

    <picture>
      <source v-if="webp" :srcset="webp" type="image/webp" />
      <img
        :src="src"
        :alt="alt"
        :width="width"
        :height="height"
        :loading="loadingAttr"
        :fetchpriority="fetchPriority"
        decoding="async"
        :class="['relative w-full h-full transition-opacity duration-500', objectFit, loaded ? 'opacity-100' : 'opacity-0']"
        @load="onLoad"
      />
    </picture>
  </div>
</template>
