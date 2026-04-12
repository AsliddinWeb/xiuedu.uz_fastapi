<script setup>
/**
 * @prop {number} modelValue - current page (v-model)
 * @prop {number} total
 * @prop {number} perPage
 */
import { computed } from 'vue'
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'

const props = defineProps({
  modelValue: { type: Number, required: true },
  total: { type: Number, required: true },
  perPage: { type: Number, default: 12 }
})
const emit = defineEmits(['update:modelValue'])

const totalPages = computed(() => Math.max(1, Math.ceil(props.total / props.perPage)))

function go(p) {
  if (p < 1 || p > totalPages.value || p === props.modelValue) return
  emit('update:modelValue', p)
}

const pages = computed(() => {
  const cur = props.modelValue
  const last = totalPages.value
  const range = new Set([1, last, cur, cur - 1, cur + 1])
  const arr = [...range].filter(p => p >= 1 && p <= last).sort((a, b) => a - b)
  const result = []
  let prev = 0
  for (const p of arr) {
    if (p - prev > 1) result.push('...')
    result.push(p)
    prev = p
  }
  return result
})

const btnCls = (active) => [
  'min-w-[2.25rem] h-9 px-3 inline-flex items-center justify-center rounded-lg text-sm font-medium transition',
  active
    ? 'bg-primary-700 text-white'
    : 'text-neutral-600 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-primary-700'
]
</script>

<template>
  <nav class="flex items-center gap-1" :aria-label="$t('common.next')">
    <button :class="btnCls(false)" :disabled="modelValue === 1" @click="go(modelValue - 1)" aria-label="Previous">
      <ChevronLeft class="w-4 h-4" />
    </button>
    <template v-for="(p, i) in pages" :key="i">
      <span v-if="p === '...'" class="px-2 text-neutral-400">…</span>
      <button v-else :class="btnCls(p === modelValue)" @click="go(p)">{{ p }}</button>
    </template>
    <button :class="btnCls(false)" :disabled="modelValue === totalPages" @click="go(modelValue + 1)" aria-label="Next">
      <ChevronRight class="w-4 h-4" />
    </button>
  </nav>
</template>
