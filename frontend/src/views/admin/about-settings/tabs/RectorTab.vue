<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Save, Plus, Trash2 } from 'lucide-vue-next'
import { AdminAboutAPI } from '@/api/admin'
import UIButton from '@/components/ui/UIButton.vue'
import MultilingualInput from '@/components/admin/MultilingualInput.vue'
import MediaPicker from '@/components/admin/MediaPicker.vue'
import { useToast } from '@/composables/useToast'

const toast = useToast()
const loading = ref(true)
const saving = ref(false)
const form = reactive({ rector_letter_paragraphs: [] })

async function load() {
  loading.value = true
  try {
    const data = await AdminAboutAPI.page.get()
    Object.assign(form, data)
    if (!Array.isArray(form.rector_letter_paragraphs)) form.rector_letter_paragraphs = []
  } finally {
    loading.value = false
  }
}
onMounted(load)

function addParagraph() {
  form.rector_letter_paragraphs.push({ uz: '', ru: '', en: '' })
}
function removeParagraph(i) {
  form.rector_letter_paragraphs.splice(i, 1)
}

async function save() {
  saving.value = true
  try {
    const { id, updated_at, ...payload } = form
    Object.assign(form, await AdminAboutAPI.page.update(payload))
    toast.success('Saqlandi')
  } catch (e) {
    toast.error(e?.response?.data?.detail || 'Xatolik')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div v-if="loading" class="text-center py-12 text-ink-faint text-sm">Yuklanmoqda...</div>

  <div v-else>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-lg font-display font-bold text-ink-dark dark:text-white">Rektor murojaati</h2>
        <p class="text-xs text-ink-faint mt-0.5">Foto, ism-lavozim va xat matni paragraflari</p>
      </div>
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>
        Saqlash
      </UIButton>
    </div>

    <!-- Photo + identity -->
    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Identity</p>
      <MediaPicker v-model="form.rector_image" label="Rektor fotosi" hint="4:5 portret eng yaxshi" />
      <MultilingualInput v-model="form" base="rector_name"   label="Ism-familiya" />
      <MultilingualInput v-model="form" base="rector_role"   label="Lavozim" placeholder="Rektor" />
      <MultilingualInput v-model="form" base="rector_degree" label="Daraja" placeholder="Pedagogika fanlari doktori, professor" />
    </div>

    <!-- Letter title -->
    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Xat sarlavhasi</p>
      <MultilingualInput v-model="form" base="rector_letter_eyebrow" label="Eyebrow" placeholder="Rektor murojaati" />
      <MultilingualInput v-model="form" base="rector_letter_title"   label="Asosiy sarlavha" placeholder="Bilim — eng kuchli sarmoya" />
    </div>

    <!-- Paragraphs -->
    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5">
      <div class="flex items-center justify-between mb-4">
        <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">
          Xat matni — paragraflar ({{ form.rector_letter_paragraphs.length }} ta)
        </p>
        <UIButton variant="ghost" size="sm" @click="addParagraph">
          <template #icon-left><Plus class="w-4 h-4" /></template>
          Paragraf qo'shish
        </UIButton>
      </div>
      <div v-if="!form.rector_letter_paragraphs.length" class="text-xs text-ink-faint text-center py-6">
        Hozircha paragraf yo'q
      </div>
      <div v-else class="space-y-4">
        <div
          v-for="(p, i) in form.rector_letter_paragraphs"
          :key="i"
          class="rounded-lg border border-surface-muted dark:border-slate-700 p-4 bg-surface-soft/50 dark:bg-slate-900/30"
        >
          <div class="flex items-center justify-between mb-2">
            <span class="text-[11px] font-bold uppercase tracking-wider text-ink-faint">Paragraf {{ i + 1 }}</span>
            <button type="button"
              class="w-7 h-7 grid place-items-center rounded text-ink-faint hover:text-danger hover:bg-danger-light"
              @click="removeParagraph(i)">
              <Trash2 class="w-3.5 h-3.5" />
            </button>
          </div>
          <div class="grid sm:grid-cols-3 gap-2">
            <div>
              <label class="block text-[10px] uppercase tracking-wider text-ink-faint mb-1">UZ</label>
              <textarea v-model="p.uz" rows="3"
                class="w-full px-2 py-1.5 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs" />
            </div>
            <div>
              <label class="block text-[10px] uppercase tracking-wider text-ink-faint mb-1">RU</label>
              <textarea v-model="p.ru" rows="3"
                class="w-full px-2 py-1.5 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs" />
            </div>
            <div>
              <label class="block text-[10px] uppercase tracking-wider text-ink-faint mb-1">EN</label>
              <textarea v-model="p.en" rows="3"
                class="w-full px-2 py-1.5 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="flex justify-end">
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>
        Saqlash
      </UIButton>
    </div>
  </div>
</template>
