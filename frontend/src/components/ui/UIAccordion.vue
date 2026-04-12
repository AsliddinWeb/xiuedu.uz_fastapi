<script setup>
/**
 * @prop {Array<{key:string, title:string}>} items
 * @prop {boolean} multiple - allow multiple panels open
 * @prop {Array<string>} modelValue - open keys
 */
import { computed } from 'vue'
import { ChevronDown } from 'lucide-vue-next'

const props = defineProps({
  items: { type: Array, required: true },
  multiple: Boolean,
  modelValue: { type: Array, default: () => [] }
})
const emit = defineEmits(['update:modelValue'])

const open = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v)
})

function toggle(key) {
  const isOpen = open.value.includes(key)
  if (props.multiple) {
    open.value = isOpen ? open.value.filter(k => k !== key) : [...open.value, key]
  } else {
    open.value = isOpen ? [] : [key]
  }
}
</script>

<template>
  <div class="divide-y divide-neutral-200 dark:divide-primary-700 border border-neutral-200 dark:border-primary-700 rounded-xl overflow-hidden">
    <div v-for="item in items" :key="item.key">
      <button
        type="button"
        :aria-expanded="open.includes(item.key)"
        class="w-full flex items-center justify-between gap-3 px-5 py-4 text-left bg-white dark:bg-primary-800 hover:bg-neutral-50 dark:hover:bg-primary-900/40 transition"
        @click="toggle(item.key)"
      >
        <span class="font-medium text-neutral-900 dark:text-white">
          <slot :name="`title-${item.key}`">{{ item.title }}</slot>
        </span>
        <ChevronDown
          :class="['w-4 h-4 flex-shrink-0 transition-transform', open.includes(item.key) && 'rotate-180']"
        />
      </button>
      <div v-if="open.includes(item.key)" class="px-5 py-4 bg-neutral-50 dark:bg-primary-900/30 text-sm text-neutral-700 dark:text-neutral-200 animate-fade-in">
        <slot :name="item.key">
          <slot :item="item" />
        </slot>
      </div>
    </div>
  </div>
</template>
