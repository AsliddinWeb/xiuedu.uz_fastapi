<script setup>
/**
 * Global confirm dialog. Mount once in AdminLayout / AppLayout.
 * Controlled via useConfirm() composable.
 */
import { onMounted, onBeforeUnmount } from 'vue'
import { AlertTriangle, Info, X } from 'lucide-vue-next'
import { _confirmState, _resolveConfirm } from '@/composables/useConfirm'

const state = _confirmState()

function confirm() { _resolveConfirm(true) }
function cancel()  { _resolveConfirm(false) }

function onKey(e) {
  if (!state.open) return
  if (e.key === 'Escape') cancel()
  if (e.key === 'Enter')  confirm()
}
onMounted(() => document.addEventListener('keydown', onKey))
onBeforeUnmount(() => document.removeEventListener('keydown', onKey))
</script>

<template>
  <Teleport to="body">
    <Transition enter-active-class="transition duration-200" enter-from-class="opacity-0" leave-active-class="transition duration-150" leave-to-class="opacity-0">
      <div
        v-if="state.open"
        class="fixed inset-0 z-[150] grid place-items-center p-4 bg-black/40 backdrop-blur-sm"
        role="alertdialog"
        aria-modal="true"
        @click.self="cancel"
      >
        <Transition
          enter-active-class="transition duration-200"
          enter-from-class="opacity-0 scale-95"
          leave-active-class="transition duration-150"
          leave-to-class="opacity-0 scale-95"
          appear
        >
          <div class="w-full max-w-sm bg-white dark:bg-slate-900 rounded-2xl shadow-modal overflow-hidden">
            <div class="p-5">
              <div class="flex items-start gap-3">
                <div
                  :class="[
                    'w-10 h-10 rounded-xl grid place-items-center flex-shrink-0',
                    state.danger
                      ? 'bg-danger-light text-danger-dark'
                      : 'bg-info-light text-info-dark'
                  ]"
                >
                  <AlertTriangle v-if="state.danger" class="w-5 h-5" />
                  <Info v-else class="w-5 h-5" />
                </div>
                <div class="flex-1 min-w-0">
                  <h3 class="font-display font-semibold text-ink-dark dark:text-white text-base">{{ state.title }}</h3>
                  <p v-if="state.message" class="text-sm text-ink-light dark:text-slate-400 mt-1.5">{{ state.message }}</p>
                </div>
                <button
                  type="button"
                  class="text-ink-faint hover:text-ink-dark dark:hover:text-white -m-1 p-1"
                  @click="cancel"
                  aria-label="Close"
                >
                  <X class="w-4 h-4" />
                </button>
              </div>
            </div>
            <div class="px-5 py-4 bg-surface-light dark:bg-slate-800 flex items-center justify-end gap-2">
              <button type="button" class="btn-ghost btn-sm" @click="cancel">{{ state.cancelLabel }}</button>
              <button
                type="button"
                :class="state.danger ? 'btn-danger btn-sm' : 'btn-primary btn-sm'"
                @click="confirm"
              >
                {{ state.confirmLabel }}
              </button>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>
