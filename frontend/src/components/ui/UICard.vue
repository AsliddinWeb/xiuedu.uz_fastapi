<script setup>
/**
 * UICard — flexible card container.
 *
 * @prop {'default'|'soft'|'outline'|'colored'|'shadow'} variant
 * @prop {'none'|'sm'|'md'|'lg'} padding
 * @prop {boolean} hover  — lift on hover
 */
import { computed } from 'vue'

const props = defineProps({
  variant: { type: String, default: 'default' },
  padding: { type: String, default: 'md' },
  hover:   { type: Boolean, default: false }
})

const variants = {
  default: 'bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 shadow-card',
  soft:    'bg-surface-soft dark:bg-slate-800/60 border border-transparent',
  outline: 'bg-transparent border border-surface-muted dark:border-slate-700',
  colored: 'bg-primary-50 dark:bg-primary-900/30 border border-primary-100 dark:border-primary-800',
  shadow:  'bg-white dark:bg-slate-800 shadow-card'
}
const paddings = { none: '', sm: 'p-4', md: 'p-6', lg: 'p-8' }

const cls = computed(() => [
  'rounded-xl transition-all duration-300',
  variants[props.variant] || variants.default,
  props.hover && 'hover:-translate-y-0.5 hover:shadow-card-hover cursor-pointer'
])
</script>

<template>
  <div :class="cls">
    <header
      v-if="$slots.header"
      :class="['border-b border-surface-muted dark:border-slate-700', paddings[padding]]"
    >
      <slot name="header" />
    </header>
    <div :class="paddings[padding]"><slot /></div>
    <footer
      v-if="$slots.footer"
      :class="['border-t border-surface-muted dark:border-slate-700', paddings[padding]]"
    >
      <slot name="footer" />
    </footer>
  </div>
</template>
