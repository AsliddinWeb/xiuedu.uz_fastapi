<script setup>
/**
 * Premium button component.
 * @prop {'primary'|'secondary'|'outline'|'ghost'|'danger'|'accent'} variant
 * @prop {'sm'|'md'|'lg'} size
 * @prop {boolean} loading
 * @prop {boolean} disabled
 * @prop {boolean} block - full-width
 * @prop {string} type - button | submit | reset
 * @prop {string} to - if set, renders RouterLink
 * @prop {string} href - if set, renders <a>
 */
import { computed } from 'vue'
import { Loader2 } from 'lucide-vue-next'

const props = defineProps({
  variant: { type: String, default: 'primary' },
  size: { type: String, default: 'md' },
  loading: Boolean,
  disabled: Boolean,
  block: Boolean,
  type: { type: String, default: 'button' },
  to: { type: [String, Object], default: null },
  href: { type: String, default: null }
})

const variants = {
  primary:   'bg-primary-700 text-white hover:bg-primary-800 focus-visible:ring-primary-500 shadow-soft',
  secondary: 'bg-neutral-100 text-primary-700 hover:bg-neutral-200 dark:bg-primary-800 dark:text-white dark:hover:bg-primary-700',
  outline:   'border-2 border-primary-700 text-primary-700 hover:bg-primary-700 hover:text-white dark:border-accent-500 dark:text-accent-500 dark:hover:bg-accent-500 dark:hover:text-primary-900',
  ghost:     'text-primary-700 hover:bg-primary-50 dark:text-neutral-200 dark:hover:bg-primary-800',
  danger:    'bg-danger text-white hover:bg-red-700 focus-visible:ring-red-500',
  accent:    'bg-accent-500 text-primary-900 hover:bg-accent-600 focus-visible:ring-accent-400 shadow-glow font-semibold'
}
const sizes = {
  sm: 'text-xs px-3 py-1.5 gap-1.5 h-8',
  md: 'text-sm px-5 py-2.5 gap-2 h-10',
  lg: 'text-base px-7 py-3 gap-2.5 h-12'
}

const cls = computed(() => [
  'inline-flex items-center justify-center rounded-lg font-medium transition-all duration-150',
  'focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
  'disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none',
  variants[props.variant] || variants.primary,
  sizes[props.size] || sizes.md,
  props.block && 'w-full'
])

const tag = computed(() => (props.to ? 'router-link' : props.href ? 'a' : 'button'))
</script>

<template>
  <component
    :is="tag"
    :to="to"
    :href="href"
    :type="!to && !href ? type : undefined"
    :disabled="disabled || loading"
    :class="cls"
    :aria-busy="loading || undefined"
  >
    <Loader2 v-if="loading" class="w-4 h-4 animate-spin" />
    <slot v-else name="icon-left" />
    <slot />
    <slot name="icon-right" />
  </component>
</template>
