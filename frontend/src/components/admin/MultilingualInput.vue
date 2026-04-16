<script setup>
/**
 * Multilingual text/textarea field — manages 3 underlying values
 * (uz/ru/en) with a compact tab strip on top.
 *
 * Usage:
 *   <MultilingualInput v-model="form" base="title" label="Sarlavha" />
 *
 * Reads/writes form[`${base}_uz`], form[`${base}_ru`], form[`${base}_en`].
 */
import { ref } from 'vue'

const props = defineProps({
  modelValue: { type: Object, required: true },
  base:       { type: String, required: true },
  label:      String,
  hint:       String,
  textarea:   Boolean,
  rows:       { type: Number, default: 3 },
  required:   Boolean,
  placeholder: String
})
const lang = ref('uz')
const tabs = [
  { key: 'uz', label: 'UZ' },
  { key: 'ru', label: 'RU' },
  { key: 'en', label: 'EN' }
]

function update(code, val) {
  // Directly mutate the reactive object — no spread (keeps reactivity)
  props.modelValue[`${props.base}_${code}`] = val
}
</script>

<template>
  <div>
    <div v-if="label" class="flex items-center justify-between mb-1.5">
      <label class="text-sm font-medium text-ink-medium dark:text-slate-300">
        {{ label }}<span v-if="required" class="text-danger ml-0.5">*</span>
      </label>
      <div class="flex items-center gap-0.5 bg-surface-soft dark:bg-slate-900/40 rounded-md p-0.5">
        <button
          v-for="t in tabs"
          :key="t.key"
          type="button"
          @click="lang = t.key"
          :class="[
            'px-2 h-6 rounded text-[11px] font-bold uppercase tracking-wider transition',
            lang === t.key
              ? 'bg-primary-700 text-white'
              : 'text-ink-faint hover:text-primary-700'
          ]"
        >{{ t.label }}</button>
      </div>
    </div>

    <textarea
      v-if="textarea"
      :value="modelValue[`${base}_${lang}`] || ''"
      @input="update(lang, $event.target.value)"
      :rows="rows"
      :placeholder="placeholder"
      class="w-full px-3 py-2.5 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm text-ink-medium dark:text-slate-300 placeholder:text-ink-faint focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-100 dark:focus:ring-primary-900"
    />
    <input
      v-else
      type="text"
      :value="modelValue[`${base}_${lang}`] || ''"
      @input="update(lang, $event.target.value)"
      :placeholder="placeholder"
      class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm text-ink-medium dark:text-slate-300 placeholder:text-ink-faint focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-100 dark:focus:ring-primary-900"
    />

    <p v-if="hint" class="mt-1 text-[11px] text-ink-faint">{{ hint }}</p>
  </div>
</template>
