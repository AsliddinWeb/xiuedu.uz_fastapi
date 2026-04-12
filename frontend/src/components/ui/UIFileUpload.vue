<script setup>
/**
 * Drag & drop file upload zone with per-file progress.
 *
 * @prop {boolean} multiple
 * @prop {string}  accept   — e.g. 'image/*'
 * @prop {Function} upload  — async (file, onProgress(0..1)) => returns url or object
 * @emits uploaded — one arg: uploaded file descriptor
 */
import { ref } from 'vue'
import { UploadCloud, X, FileText, Loader2 } from 'lucide-vue-next'

const props = defineProps({
  multiple: { type: Boolean, default: true },
  accept:   { type: String,  default: 'image/*' },
  upload:   { type: Function, required: true }
})
const emit = defineEmits(['uploaded'])

const dragOver = ref(false)
const queue = ref([])   // { id, file, progress, error, done }

let qid = 0
function makeEntry(file) { return { id: ++qid, file, progress: 0, error: '', done: false } }

async function handleFiles(files) {
  for (const file of files) {
    const entry = makeEntry(file)
    queue.value.push(entry)
    try {
      const result = await props.upload(file, (p) => { entry.progress = p })
      entry.done = true
      emit('uploaded', result)
      // Remove after short delay so user sees the checkmark
      setTimeout(() => {
        queue.value = queue.value.filter(q => q.id !== entry.id)
      }, 1200)
    } catch (e) {
      entry.error = e?.message || 'Upload failed'
    }
  }
}

function onInput(e) {
  const files = [...e.target.files]
  if (files.length) handleFiles(files)
  e.target.value = ''
}
function onDrop(e) {
  e.preventDefault()
  dragOver.value = false
  if (e.dataTransfer?.files?.length) handleFiles([...e.dataTransfer.files])
}
function remove(id) { queue.value = queue.value.filter(q => q.id !== id) }

function fmtSize(b) {
  if (!b) return ''
  const u = ['B','KB','MB','GB']; let i = 0, v = b
  while (v >= 1024 && i < u.length - 1) { v /= 1024; i++ }
  return v.toFixed(1) + ' ' + u[i]
}
</script>

<template>
  <div>
    <label
      :class="[
        'block rounded-2xl border-2 border-dashed p-8 text-center cursor-pointer transition',
        dragOver
          ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
          : 'border-surface-muted dark:border-slate-700 hover:border-primary-400 dark:hover:border-primary-600 hover:bg-surface-soft dark:hover:bg-slate-800/30'
      ]"
      @dragover.prevent="dragOver = true"
      @dragleave.prevent="dragOver = false"
      @drop="onDrop"
    >
      <input type="file" :multiple="multiple" :accept="accept" class="hidden" @change="onInput" />
      <UploadCloud class="w-10 h-10 mx-auto text-primary-500 mb-3" stroke-width="1.4" />
      <p class="text-sm font-medium text-ink-dark dark:text-white">Faylni bu yerga tashlang yoki bosing</p>
      <p class="text-xs text-ink-faint mt-1">{{ accept === 'image/*' ? 'JPG, PNG, WebP • max 10MB' : 'JPG, PNG, WebP, PDF, DOC • max 50MB' }}</p>
    </label>

    <!-- Queue -->
    <div v-if="queue.length" class="mt-4 space-y-2">
      <div
        v-for="q in queue"
        :key="q.id"
        class="flex items-center gap-3 p-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-800"
      >
        <div class="w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/40 grid place-items-center text-primary-600 dark:text-primary-300 flex-shrink-0">
          <Loader2 v-if="!q.done && !q.error" class="w-5 h-5 animate-spin" />
          <FileText v-else class="w-5 h-5" />
        </div>
        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between gap-2">
            <p class="text-sm font-medium text-ink-dark dark:text-white truncate">{{ q.file.name }}</p>
            <p class="text-xs text-ink-faint flex-shrink-0">{{ fmtSize(q.file.size) }}</p>
          </div>
          <div class="mt-1.5 h-1 rounded-full bg-surface-soft dark:bg-slate-700 overflow-hidden">
            <div
              class="h-full rounded-full transition-[width] duration-300"
              :class="q.error ? 'bg-danger' : q.done ? 'bg-success' : 'bg-primary-500'"
              :style="{ width: ((q.error ? 100 : q.progress * 100) || (q.done ? 100 : 0)) + '%' }"
            />
          </div>
          <p v-if="q.error" class="mt-1 text-xs text-danger">{{ q.error }}</p>
        </div>
        <button class="text-ink-faint hover:text-danger p-1" @click.stop="remove(q.id)" aria-label="Remove">
          <X class="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
</template>
