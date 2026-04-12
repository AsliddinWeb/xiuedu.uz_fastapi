<script setup>
/**
 * Compact image / video / file picker.
 * Uploads via AdminMediaAPI and stores the returned URL in v-model.
 */
import { ref } from 'vue'
import { Upload, Trash2, ExternalLink } from 'lucide-vue-next'
import { AdminMediaAPI } from '@/api/admin'
import { useToast } from '@/composables/useToast'

const props = defineProps({
  modelValue: { type: String, default: null },
  label: String,
  hint: String,
  accept: { type: String, default: 'image/*' },
  preview: { type: String, default: 'image' }  // 'image' | 'video' | 'file'
})
const emit = defineEmits(['update:modelValue'])
const toast = useToast()
const uploading = ref(false)

async function onPick(e) {
  const file = e.target.files[0]
  if (!file) return
  uploading.value = true
  try {
    const res = await AdminMediaAPI.upload(file)
    emit('update:modelValue', res.url)
    toast.success('Yuklandi')
  } catch (_) {
    toast.error('Yuklashda xatolik')
  } finally {
    uploading.value = false
    e.target.value = ''
  }
}
function clear() { emit('update:modelValue', null) }
</script>

<template>
  <div>
    <label v-if="label" class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">
      {{ label }}
    </label>

    <div v-if="modelValue" class="rounded-lg border border-surface-muted dark:border-slate-700 overflow-hidden bg-surface-soft dark:bg-slate-900 mb-2">
      <video
        v-if="preview === 'video'"
        :src="modelValue"
        controls
        class="w-full max-h-48 bg-black"
      />
      <img
        v-else-if="preview === 'image'"
        :src="modelValue"
        alt=""
        class="w-full max-h-48 object-contain bg-black/5"
      />
      <a
        v-else
        :href="modelValue"
        target="_blank"
        rel="noopener"
        class="flex items-center gap-2 px-4 py-3 text-sm text-primary-700 hover:underline"
      >
        <ExternalLink class="w-4 h-4" /> {{ modelValue.split('/').pop() }}
      </a>
    </div>

    <div class="flex items-center gap-2">
      <label class="flex-1 cursor-pointer">
        <input type="file" :accept="accept" class="hidden" @change="onPick" />
        <span class="block text-center px-4 py-2 rounded-lg border-2 border-dashed border-surface-muted dark:border-slate-700 text-xs text-ink-faint hover:border-accent-500 transition-colors">
          <Upload class="w-3.5 h-3.5 inline mr-1" />
          {{ uploading ? 'Yuklanmoqda...' : (modelValue ? 'Boshqasini tanlash' : 'Fayl tanlash') }}
        </span>
      </label>
      <button
        v-if="modelValue"
        type="button"
        class="w-9 h-9 grid place-items-center rounded-lg border border-surface-muted dark:border-slate-700 text-ink-faint hover:text-danger hover:border-danger"
        @click="clear"
      >
        <Trash2 class="w-3.5 h-3.5" />
      </button>
    </div>

    <p v-if="hint" class="mt-1 text-[11px] text-ink-faint">{{ hint }}</p>
  </div>
</template>
