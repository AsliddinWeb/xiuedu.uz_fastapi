<script setup>
/**
 * Input / textarea with label, error, hint and prefix/suffix slots.
 * Supports v-model.
 */
import { computed, useSlots } from 'vue'

const props = defineProps({
  modelValue: { type: [String, Number], default: '' },
  label: String,
  hint: String,
  error: String,
  type: { type: String, default: 'text' },
  placeholder: String,
  disabled: Boolean,
  required: Boolean,
  textarea: Boolean,
  rows: { type: Number, default: 4 },
  id: String
})

const emit = defineEmits(['update:modelValue', 'blur', 'focus'])
const slots = useSlots()

const inputId = computed(() => props.id || `inp-${Math.random().toString(36).slice(2, 9)}`)

const baseCls = computed(() => [
  'w-full rounded-lg border bg-white dark:bg-primary-800',
  'text-neutral-900 dark:text-neutral-100 placeholder:text-neutral-400',
  'transition-colors focus:outline-none focus:ring-2 focus:ring-offset-0',
  props.error
    ? 'border-danger focus:ring-red-200 dark:focus:ring-red-900'
    : 'border-neutral-300 dark:border-primary-700 focus:border-primary-500 focus:ring-primary-100 dark:focus:ring-primary-800',
  props.disabled && 'opacity-60 cursor-not-allowed',
  slots.prefix ? 'pl-10' : 'pl-3.5',
  slots.suffix ? 'pr-10' : 'pr-3.5',
  props.textarea ? 'py-2.5' : 'py-2.5 h-10'
])

function onInput(e) {
  emit('update:modelValue', e.target.value)
}
</script>

<template>
  <div class="w-full">
    <label v-if="label" :for="inputId" class="block text-sm font-medium text-neutral-700 dark:text-neutral-200 mb-1.5">
      {{ label }}
      <span v-if="required" class="text-danger ml-0.5">*</span>
    </label>

    <div class="relative">
      <span v-if="$slots.prefix" class="absolute inset-y-0 left-0 flex items-center pl-3 text-neutral-400">
        <slot name="prefix" />
      </span>

      <textarea
        v-if="textarea"
        :id="inputId"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        :rows="rows"
        :class="baseCls"
        :aria-invalid="!!error"
        @input="onInput"
        @blur="$emit('blur', $event)"
        @focus="$emit('focus', $event)"
      />
      <input
        v-else
        :id="inputId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        :class="baseCls"
        :aria-invalid="!!error"
        @input="onInput"
        @blur="$emit('blur', $event)"
        @focus="$emit('focus', $event)"
      />

      <span v-if="$slots.suffix" class="absolute inset-y-0 right-0 flex items-center pr-3 text-neutral-400">
        <slot name="suffix" />
      </span>
    </div>

    <p v-if="error" class="mt-1.5 text-xs text-danger">{{ error }}</p>
    <p v-else-if="hint" class="mt-1.5 text-xs text-neutral-500 dark:text-neutral-400">{{ hint }}</p>
  </div>
</template>
