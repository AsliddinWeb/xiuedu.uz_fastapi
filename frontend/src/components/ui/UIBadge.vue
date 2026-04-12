<script setup>
/**
 * @prop {'default'|'primary'|'success'|'warning'|'danger'|'info'|'accent'} variant
 * @prop {'sm'|'md'|'lg'} size
 * @prop {boolean} dot
 * @prop {boolean} pill
 */
import { computed } from 'vue'

const props = defineProps({
  variant: { type: String, default: 'default' },
  size: { type: String, default: 'md' },
  dot: Boolean,
  pill: { type: Boolean, default: true }
})

const variants = {
  default: 'bg-neutral-100 text-neutral-700 dark:bg-primary-700 dark:text-neutral-200',
  primary: 'bg-primary-100 text-primary-800 dark:bg-primary-800 dark:text-primary-100',
  success: 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300',
  warning: 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300',
  danger:  'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300',
  info:    'bg-sky-100 text-sky-800 dark:bg-sky-900/40 dark:text-sky-300',
  accent:  'bg-accent-100 text-accent-800 dark:bg-accent-900/40 dark:text-accent-300'
}
const sizes = {
  sm: 'text-[10px] px-1.5 py-0.5',
  md: 'text-xs px-2.5 py-1',
  lg: 'text-sm px-3 py-1.5'
}
const dotColor = {
  default: 'bg-neutral-500',
  primary: 'bg-primary-500',
  success: 'bg-success',
  warning: 'bg-warning',
  danger:  'bg-danger',
  info:    'bg-info',
  accent:  'bg-accent-500'
}
const cls = computed(() => [
  'inline-flex items-center gap-1.5 font-medium',
  props.pill ? 'rounded-full' : 'rounded',
  variants[props.variant] || variants.default,
  sizes[props.size] || sizes.md
])
</script>

<template>
  <span :class="cls">
    <span v-if="dot" :class="['w-1.5 h-1.5 rounded-full', dotColor[variant]]" />
    <slot />
  </span>
</template>
