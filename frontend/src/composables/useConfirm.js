import { ref, reactive } from 'vue'

/**
 * Imperative confirm dialog — single global instance.
 *
 * Usage:
 *   const confirm = useConfirm()
 *   if (await confirm({ title: 'Delete?', message: '...', danger: true })) { ... }
 *
 * Render <UIConfirmDialog /> once in your root layout.
 */
const state = reactive({
  open: false,
  title: '',
  message: '',
  confirmLabel: 'Tasdiqlash',
  cancelLabel: 'Bekor qilish',
  danger: false
})

let resolver = null

export function useConfirm() {
  return function confirm(opts = {}) {
    Object.assign(state, {
      open: true,
      title: opts.title || 'Tasdiqlang',
      message: opts.message || '',
      confirmLabel: opts.confirmLabel || 'Tasdiqlash',
      cancelLabel: opts.cancelLabel || 'Bekor qilish',
      danger: !!opts.danger
    })
    return new Promise((resolve) => { resolver = resolve })
  }
}

export function _confirmState() { return state }
export function _resolveConfirm(value) {
  state.open = false
  if (resolver) { resolver(value); resolver = null }
}
