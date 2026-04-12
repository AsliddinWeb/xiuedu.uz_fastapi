<script setup>
/**
 * Headless dropdown.
 * @prop {Array<{label:string, value?:any, icon?:any, onSelect?:Function, divider?:boolean}>} items
 * @prop {'left'|'right'} align
 */
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'

const props = defineProps({
  items: { type: Array, default: () => [] },
  align: { type: String, default: 'right' },
  width: { type: String, default: 'w-48' }
})
const emit = defineEmits(['select'])

const open = ref(false)
const root = ref(null)

function toggle() { open.value = !open.value }
function close() { open.value = false }

function pick(item) {
  if (item.divider || item.disabled) return
  if (item.onSelect) item.onSelect(item)
  emit('select', item)
  close()
}

function onClickOutside(e) {
  if (root.value && !root.value.contains(e.target)) close()
}
function onKey(e) {
  if (e.key === 'Escape') close()
}

onMounted(() => {
  document.addEventListener('mousedown', onClickOutside)
  document.addEventListener('keydown', onKey)
})
onBeforeUnmount(() => {
  document.removeEventListener('mousedown', onClickOutside)
  document.removeEventListener('keydown', onKey)
})

const menuCls = computed(() => [
  'absolute z-50 mt-2 py-1 rounded-xl border border-neutral-200 dark:border-primary-700 bg-white dark:bg-primary-800 shadow-soft animate-scale-in',
  props.width,
  props.align === 'right' ? 'right-0' : 'left-0'
])
</script>

<template>
  <div ref="root" class="relative inline-block">
    <div @click="toggle">
      <slot name="trigger" :open="open" :toggle="toggle" />
    </div>
    <div v-if="open" :class="menuCls" role="menu">
      <template v-for="(item, i) in items" :key="i">
        <div v-if="item.divider" class="my-1 border-t border-neutral-200 dark:border-primary-700" />
        <button
          v-else
          type="button"
          role="menuitem"
          :disabled="item.disabled"
          class="flex w-full items-center gap-2 px-3 py-2 text-sm text-left text-neutral-700 dark:text-neutral-200 hover:bg-neutral-100 dark:hover:bg-primary-700 disabled:opacity-50"
          @click="pick(item)"
        >
          <component :is="item.icon" v-if="item.icon" class="w-4 h-4" />
          {{ item.label }}
        </button>
      </template>
    </div>
  </div>
</template>
