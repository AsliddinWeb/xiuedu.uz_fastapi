import { useToastStore } from '@/stores/toast'

export function useToast() {
  const store = useToastStore()
  return {
    success: (msg, opts) => store.show(msg, { ...opts, type: 'success' }),
    error:   (msg, opts) => store.show(msg, { ...opts, type: 'error' }),
    warning: (msg, opts) => store.show(msg, { ...opts, type: 'warning' }),
    info:    (msg, opts) => store.show(msg, { ...opts, type: 'info' }),
    dismiss: store.dismiss
  }
}
