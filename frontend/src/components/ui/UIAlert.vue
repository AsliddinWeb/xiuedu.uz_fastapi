<script setup>
/**
 * @prop {'info'|'success'|'warning'|'error'} variant
 * @prop {string} title
 * @prop {boolean} dismissible
 */
import { ref, computed } from 'vue'
import { CheckCircle2, AlertCircle, AlertTriangle, Info, X } from 'lucide-vue-next'

const props = defineProps({
  variant: { type: String, default: 'info' },
  title: String,
  dismissible: Boolean
})

const visible = ref(true)

const config = {
  info:    { cls: 'bg-sky-50 text-sky-900 border-sky-200 dark:bg-sky-950/40 dark:text-sky-200 dark:border-sky-900', icon: Info },
  success: { cls: 'bg-green-50 text-green-900 border-green-200 dark:bg-green-950/40 dark:text-green-200 dark:border-green-900', icon: CheckCircle2 },
  warning: { cls: 'bg-amber-50 text-amber-900 border-amber-200 dark:bg-amber-950/40 dark:text-amber-200 dark:border-amber-900', icon: AlertTriangle },
  error:   { cls: 'bg-red-50 text-red-900 border-red-200 dark:bg-red-950/40 dark:text-red-200 dark:border-red-900', icon: AlertCircle }
}

const cfg = computed(() => config[props.variant] || config.info)
</script>

<template>
  <div v-if="visible" :class="['flex gap-3 rounded-xl border p-4', cfg.cls]" role="alert">
    <component :is="cfg.icon" class="w-5 h-5 flex-shrink-0 mt-0.5" />
    <div class="flex-1 text-sm">
      <p v-if="title" class="font-semibold mb-0.5">{{ title }}</p>
      <slot />
    </div>
    <button v-if="dismissible" type="button" class="text-current opacity-60 hover:opacity-100" @click="visible = false" aria-label="Close">
      <X class="w-4 h-4" />
    </button>
  </div>
</template>
