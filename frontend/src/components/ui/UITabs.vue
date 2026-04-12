<script setup>
/**
 * @prop {Array<{key:string, label:string, icon?:any}>} tabs
 * @prop {string} modelValue - active tab key (v-model)
 */
import { computed } from 'vue'

const props = defineProps({
  tabs: { type: Array, required: true },
  modelValue: { type: String, default: null }
})
const emit = defineEmits(['update:modelValue'])

const active = computed({
  get: () => props.modelValue ?? props.tabs[0]?.key,
  set: (v) => emit('update:modelValue', v)
})
</script>

<template>
  <div>
    <div class="flex items-center gap-1 border-b border-neutral-200 dark:border-primary-700 overflow-x-auto" role="tablist">
      <button
        v-for="t in tabs"
        :key="t.key"
        type="button"
        role="tab"
        :aria-selected="active === t.key"
        :class="[
          'inline-flex items-center gap-2 px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap',
          active === t.key
            ? 'border-accent-500 text-primary-700 dark:text-accent-500'
            : 'border-transparent text-neutral-500 hover:text-primary-700 dark:hover:text-white'
        ]"
        @click="active = t.key"
      >
        <component :is="t.icon" v-if="t.icon" class="w-4 h-4" />
        {{ t.label }}
      </button>
    </div>
    <div class="pt-5">
      <slot :active="active" />
    </div>
  </div>
</template>
