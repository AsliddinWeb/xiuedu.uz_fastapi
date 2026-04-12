import { defineStore } from 'pinia'
import { ref } from 'vue'

let _id = 0

export const useToastStore = defineStore('toast', () => {
  const items = ref([])

  function show(message, { type = 'info', duration = 4000, title = '' } = {}) {
    const id = ++_id
    items.value.push({ id, type, message, title })
    if (duration > 0) setTimeout(() => dismiss(id), duration)
    return id
  }

  function dismiss(id) {
    items.value = items.value.filter(t => t.id !== id)
  }

  return { items, show, dismiss }
})
