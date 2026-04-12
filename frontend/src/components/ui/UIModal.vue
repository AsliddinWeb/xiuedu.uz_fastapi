<script setup>
/**
 * Accessible modal with backdrop, ESC close, focus trap-friendly.
 * @prop {boolean} modelValue - open state (v-model)
 * @prop {'sm'|'md'|'lg'|'xl'|'full'} size
 * @prop {boolean} closeOnBackdrop
 * @prop {boolean} closeOnEsc
 */
import { computed, watch, onBeforeUnmount } from 'vue'
import { X } from 'lucide-vue-next'

const props = defineProps({
  modelValue: Boolean,
  title: String,
  size: { type: String, default: 'md' },
  closeOnBackdrop: { type: Boolean, default: true },
  closeOnEsc: { type: Boolean, default: true }
})
const emit = defineEmits(['update:modelValue', 'close'])

const sizes = {
  sm: 'max-w-sm',
  md: 'max-w-md',
  lg: 'max-w-2xl',
  xl: 'max-w-4xl',
  full: 'max-w-[95vw] h-[90vh]'
}

const dialogCls = computed(() => [
  'relative w-full bg-white dark:bg-primary-800 rounded-2xl shadow-2xl',
  'animate-scale-in flex flex-col max-h-[90vh] overflow-hidden',
  sizes[props.size] || sizes.md
])

function close() {
  emit('update:modelValue', false)
  emit('close')
}

function onKey(e) {
  if (e.key === 'Escape' && props.closeOnEsc && props.modelValue) close()
}

watch(
  () => props.modelValue,
  (open) => {
    if (open) {
      document.addEventListener('keydown', onKey)
      document.body.style.overflow = 'hidden'
    } else {
      document.removeEventListener('keydown', onKey)
      document.body.style.overflow = ''
    }
  }
)
onBeforeUnmount(() => {
  document.removeEventListener('keydown', onKey)
  document.body.style.overflow = ''
})
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-200"
      enter-from-class="opacity-0"
      leave-active-class="transition duration-150"
      leave-to-class="opacity-0"
    >
      <div
        v-if="modelValue"
        class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
        role="dialog"
        aria-modal="true"
        @click.self="closeOnBackdrop && close()"
      >
        <div :class="dialogCls">
          <header
            v-if="title || $slots.header"
            class="flex items-center justify-between px-6 py-4 border-b border-neutral-200 dark:border-primary-700"
          >
            <slot name="header">
              <h3 class="font-display font-semibold text-lg text-primary-700 dark:text-white">
                {{ title }}
              </h3>
            </slot>
            <button
              type="button"
              class="text-neutral-400 hover:text-neutral-700 dark:hover:text-white transition"
              :aria-label="$t('common.close')"
              @click="close"
            >
              <X class="w-5 h-5" />
            </button>
          </header>

          <div class="overflow-y-auto p-6 flex-1">
            <slot />
          </div>

          <footer
            v-if="$slots.footer"
            class="flex items-center justify-end gap-3 px-6 py-4 border-t border-neutral-200 dark:border-primary-700 bg-neutral-50 dark:bg-primary-900"
          >
            <slot name="footer" />
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
