<script setup>
/**
 * Lightweight contenteditable rich text editor.
 * No external deps. Sanitizes on paste.
 *
 * v-model is bound to HTML string.
 */
import { ref, watch, onMounted } from 'vue'
import {
  Bold, Italic, Underline, List, ListOrdered, Heading2, Heading3,
  Link as LinkIcon, Quote, Code, Undo, Redo, RemoveFormatting
} from 'lucide-vue-next'

const props = defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: '' },
  minHeight: { type: String, default: '20rem' }
})
const emit = defineEmits(['update:modelValue'])

const editor = ref(null)

function exec(cmd, value = null) {
  document.execCommand(cmd, false, value)
  syncOut()
  editor.value?.focus()
}

function setLink() {
  const url = prompt('URL kiriting:', 'https://')
  if (url) exec('createLink', url)
}

function syncOut() {
  if (!editor.value) return
  emit('update:modelValue', editor.value.innerHTML)
}

function onPaste(e) {
  e.preventDefault()
  const text = (e.clipboardData || window.clipboardData).getData('text/plain')
  document.execCommand('insertText', false, text)
}

watch(() => props.modelValue, (v) => {
  if (editor.value && editor.value.innerHTML !== v) {
    editor.value.innerHTML = v || ''
  }
})

onMounted(() => {
  if (editor.value) editor.value.innerHTML = props.modelValue || ''
})

const tools = [
  { icon: Heading2,    cmd: 'formatBlock', val: 'h2',         title: 'H2' },
  { icon: Heading3,    cmd: 'formatBlock', val: 'h3',         title: 'H3' },
  { icon: Bold,        cmd: 'bold',        title: 'Bold'        },
  { icon: Italic,      cmd: 'italic',      title: 'Italic'      },
  { icon: Underline,   cmd: 'underline',   title: 'Underline'   },
  { icon: List,        cmd: 'insertUnorderedList', title: 'List' },
  { icon: ListOrdered, cmd: 'insertOrderedList',   title: 'Ordered list' },
  { icon: Quote,       cmd: 'formatBlock', val: 'blockquote', title: 'Quote' },
  { icon: Code,        cmd: 'formatBlock', val: 'pre',        title: 'Code' },
  { icon: RemoveFormatting, cmd: 'removeFormat', title: 'Clear formatting' }
]
</script>

<template>
  <div class="rounded-xl border border-neutral-200 dark:border-primary-700 bg-white dark:bg-primary-800 overflow-hidden">
    <!-- Toolbar -->
    <div class="flex flex-wrap items-center gap-0.5 px-2 py-1.5 border-b border-neutral-200 dark:border-primary-700 bg-neutral-50 dark:bg-primary-900">
      <button
        v-for="t in tools"
        :key="t.title"
        type="button"
        :title="t.title"
        class="w-8 h-8 grid place-items-center rounded text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-primary-700 transition"
        @click="exec(t.cmd, t.val)"
      >
        <component :is="t.icon" class="w-4 h-4" />
      </button>
      <button type="button" title="Link" class="w-8 h-8 grid place-items-center rounded text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-primary-700 transition" @click="setLink">
        <LinkIcon class="w-4 h-4" />
      </button>
      <span class="mx-1 h-5 w-px bg-neutral-300 dark:bg-primary-700" />
      <button type="button" title="Undo" class="w-8 h-8 grid place-items-center rounded text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-primary-700 transition" @click="exec('undo')"><Undo class="w-4 h-4" /></button>
      <button type="button" title="Redo" class="w-8 h-8 grid place-items-center rounded text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-primary-700 transition" @click="exec('redo')"><Redo class="w-4 h-4" /></button>
    </div>

    <div
      ref="editor"
      contenteditable="true"
      role="textbox"
      class="prose prose-sm dark:prose-invert max-w-none p-4 focus:outline-none"
      :data-placeholder="placeholder"
      :style="{ minHeight }"
      @input="syncOut"
      @paste="onPaste"
    />
  </div>
</template>

<style scoped>
[contenteditable="true"]:empty::before {
  content: attr(data-placeholder);
  color: #94A3B8;
  pointer-events: none;
}
</style>
