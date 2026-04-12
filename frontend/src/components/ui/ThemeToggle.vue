<script setup>
/**
 * Sun/Moon toggle with smooth icon crossfade.
 *
 * Props:
 *   compact — small variant for dark utility bars
 */
import { Sun, Moon } from 'lucide-vue-next'
import { useThemeStore } from '@/stores/theme'
import { useI18n } from 'vue-i18n'

defineProps({
  compact: { type: Boolean, default: false }
})

const theme = useThemeStore()
const { t } = useI18n()
</script>

<template>
  <button
    type="button"
    :aria-label="theme.isDark ? t('ui.theme_light') : t('ui.theme_dark')"
    :aria-pressed="theme.isDark"
    :class="[
      'relative grid place-items-center rounded-md transition focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-500',
      compact
        ? 'w-6 h-6 text-white/80 hover:text-white hover:bg-white/10'
        : 'w-9 h-9 text-ink-medium dark:text-slate-300 hover:bg-surface-soft dark:hover:bg-slate-800'
    ]"
    @click="theme.toggle"
  >
    <Transition
      enter-active-class="transition duration-300"
      enter-from-class="opacity-0 rotate-90 scale-50"
      leave-active-class="transition duration-200 absolute"
      leave-to-class="opacity-0 -rotate-90 scale-50"
      mode="out-in"
    >
      <Sun v-if="theme.isDark" key="sun" :class="compact ? 'w-3.5 h-3.5 text-accent-400' : 'w-4 h-4 text-accent-500'" />
      <Moon v-else key="moon" :class="compact ? 'w-3.5 h-3.5' : 'w-4 h-4'" />
    </Transition>
  </button>
</template>
