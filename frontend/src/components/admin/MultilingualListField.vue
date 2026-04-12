<script setup>
/**
 * Editable list of multilingual items.
 * Each item is { uz, ru, en }. v-model is the array.
 */
import { Plus, Trash2 } from 'lucide-vue-next'

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
  label: String,
  hint: String
})
const emit = defineEmits(['update:modelValue'])

function add() {
  emit('update:modelValue', [...(props.modelValue || []), { uz: '', ru: '', en: '' }])
}
function remove(i) {
  const next = [...props.modelValue]
  next.splice(i, 1)
  emit('update:modelValue', next)
}
function update(i, code, val) {
  const next = props.modelValue.map((it, idx) => idx === i ? { ...it, [code]: val } : it)
  emit('update:modelValue', next)
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-2">
      <label v-if="label" class="text-sm font-medium text-ink-medium dark:text-slate-300">{{ label }}</label>
      <button type="button" class="inline-flex items-center gap-1 px-2.5 py-1 rounded text-[11px] font-bold text-primary-700 hover:bg-primary-50 dark:hover:bg-slate-700/40" @click="add">
        <Plus class="w-3 h-3" /> Qo'shish
      </button>
    </div>
    <div v-if="!(modelValue || []).length" class="text-[11px] text-ink-faint italic py-2">Hozircha yo'q</div>
    <div v-else class="space-y-2">
      <div
        v-for="(it, i) in modelValue"
        :key="i"
        class="grid sm:grid-cols-[1fr_1fr_1fr_auto] gap-2 items-center p-2 rounded-lg bg-surface-soft dark:bg-slate-900/30"
      >
        <input type="text" :value="it.uz" placeholder="UZ"
               @input="update(i, 'uz', $event.target.value)"
               class="h-9 px-2 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs" />
        <input type="text" :value="it.ru" placeholder="RU"
               @input="update(i, 'ru', $event.target.value)"
               class="h-9 px-2 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs" />
        <input type="text" :value="it.en" placeholder="EN"
               @input="update(i, 'en', $event.target.value)"
               class="h-9 px-2 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs" />
        <button type="button" class="w-8 h-8 grid place-items-center rounded text-ink-faint hover:text-danger" @click="remove(i)">
          <Trash2 class="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
    <p v-if="hint" class="mt-1 text-[11px] text-ink-faint">{{ hint }}</p>
  </div>
</template>
