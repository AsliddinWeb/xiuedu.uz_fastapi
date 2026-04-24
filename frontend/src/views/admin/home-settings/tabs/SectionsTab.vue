<script setup>
/**
 * Section list — fixed keys (from seed), each row has:
 *  - on/off toggle
 *  - up/down reorder
 *  - "Edit overrides" modal (eyebrow/title/subtitle override + settings JSON)
 */
import { ref, reactive, onMounted } from 'vue'
import {
  ChevronUp, ChevronDown, Edit3, Save, Check, X
} from 'lucide-vue-next'
import { AdminHomeAPI } from '@/api/admin'
import UIModal from '@/components/ui/UIModal.vue'
import UIButton from '@/components/ui/UIButton.vue'
import MultilingualInput from '@/components/admin/MultilingualInput.vue'
import { useToast } from '@/composables/useToast'

const toast = useToast()
const sections = ref([])
const loading = ref(true)
const modalOpen = ref(false)
const form = reactive({})
const editing = ref(null)
const saving = ref(false)

// Friendly labels for the 12 known section keys
const SECTION_LABELS = {
  intro:        'Intro — universitet kirish',
  news:         'Yangiliklar',
  campus:       'Kampus editorial',
  why_xiu:      'Why XIU — afzalliklar',
  academic:     'Akademik (fakultetlar)',
  admission:    'Qabul jarayoni',
  numbers:      'Raqamlar (Numbers)',
  events:       'Tadbirlar',
  testimonials: 'Sharhlar',
  partners:     'Hamkorlar',
  licenses:     'Litsenziyalar',
  faq:          'FAQ'
}

async function load() {
  loading.value = true
  try {
    sections.value = (await AdminHomeAPI.sections.list()) || []
  } finally {
    loading.value = false
  }
}
onMounted(load)

async function toggle(s) {
  await AdminHomeAPI.sections.update(s.key, { enabled: !s.enabled })
  await load()
}

async function move(s, dir) {
  const idx = sections.value.findIndex(x => x.key === s.key)
  const swap = sections.value[idx + dir]
  if (!swap) return
  await Promise.all([
    AdminHomeAPI.sections.update(s.key,    { sort_order: swap.sort_order }),
    AdminHomeAPI.sections.update(swap.key, { sort_order: s.sort_order })
  ])
  await load()
}

function openEdit(s) {
  editing.value = s
  Object.keys(form).forEach(k => delete form[k])
  Object.assign(form, JSON.parse(JSON.stringify(s)))
  if (typeof form.settings !== 'object' || form.settings === null) form.settings = {}
  form._settingsJson = JSON.stringify(form.settings, null, 2)
  modalOpen.value = true
}

async function save() {
  saving.value = true
  try {
    let settings = {}
    try { settings = JSON.parse(form._settingsJson || '{}') }
    catch { toast.error('settings JSON noto\'g\'ri'); saving.value = false; return }

    const payload = {
      enabled: form.enabled,
      sort_order: form.sort_order,
      eyebrow_uz: form.eyebrow_uz || null,
      eyebrow_ru: form.eyebrow_ru || null,
      eyebrow_en: form.eyebrow_en || null,
      title_uz: form.title_uz || null,
      title_ru: form.title_ru || null,
      title_en: form.title_en || null,
      subtitle_uz: form.subtitle_uz || null,
      subtitle_ru: form.subtitle_ru || null,
      subtitle_en: form.subtitle_en || null,
      body_p1_uz: form.body_p1_uz || null,
      body_p1_ru: form.body_p1_ru || null,
      body_p1_en: form.body_p1_en || null,
      body_p2_uz: form.body_p2_uz || null,
      body_p2_ru: form.body_p2_ru || null,
      body_p2_en: form.body_p2_en || null,
      link_label_uz: form.link_label_uz || null,
      link_label_ru: form.link_label_ru || null,
      link_label_en: form.link_label_en || null,
      link_url: form.link_url || null,
      settings
    }
    await AdminHomeAPI.sections.update(editing.value.key, payload)
    toast.success('Yangilandi')
    modalOpen.value = false
    await load()
  } catch (e) {
    toast.error(e?.response?.data?.detail || 'Saqlashda xatolik')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div>
    <div class="mb-5">
      <h2 class="text-lg font-display font-bold text-ink-dark dark:text-white">Bosh sahifa sectionlari</h2>
      <p class="text-xs text-ink-faint mt-0.5">Sectionlarni yoqib/o'chirish, tartibini o'zgartirish va matn/sozlamalarini override qilish</p>
    </div>

    <div v-if="loading" class="text-center py-12 text-ink-faint text-sm">Yuklanmoqda...</div>

    <div v-else class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 overflow-hidden">
      <table class="w-full">
        <thead class="bg-surface-soft dark:bg-slate-900/40">
          <tr>
            <th class="w-10 px-2 py-3"></th>
            <th class="text-left px-3 py-3 text-[10px] font-bold uppercase tracking-wider text-ink-faint">Section</th>
            <th class="text-left px-3 py-3 text-[10px] font-bold uppercase tracking-wider text-ink-faint">Override</th>
            <th class="w-32 px-3 py-3 text-[10px] font-bold uppercase tracking-wider text-ink-faint">Holat</th>
            <th class="w-20 px-3 py-3"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(s, i) in sections"
            :key="s.key"
            class="border-t border-surface-muted dark:border-slate-700 hover:bg-surface-soft/50 dark:hover:bg-slate-900/20"
          >
            <td class="px-2 py-2.5 align-middle">
              <div class="flex flex-col gap-0.5">
                <button
                  type="button"
                  :disabled="i === 0"
                  @click="move(s, -1)"
                  class="w-6 h-5 grid place-items-center rounded text-ink-faint hover:bg-surface-muted disabled:opacity-30"
                ><ChevronUp class="w-3 h-3" /></button>
                <button
                  type="button"
                  :disabled="i === sections.length - 1"
                  @click="move(s, 1)"
                  class="w-6 h-5 grid place-items-center rounded text-ink-faint hover:bg-surface-muted disabled:opacity-30"
                ><ChevronDown class="w-3 h-3" /></button>
              </div>
            </td>
            <td class="px-3 py-2.5">
              <p class="text-sm font-bold text-ink-dark dark:text-white">{{ SECTION_LABELS[s.key] || s.key }}</p>
              <p class="text-[11px] font-mono text-ink-faint">{{ s.key }}</p>
            </td>
            <td class="px-3 py-2.5 text-xs text-ink-light">
              <span v-if="s.title_uz">{{ s.title_uz }}</span>
              <span v-else class="italic">— default —</span>
            </td>
            <td class="px-3 py-2.5">
              <button
                type="button"
                @click="toggle(s)"
                :class="[
                  'inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-bold',
                  s.enabled ? 'bg-success-light text-success-dark' : 'bg-surface-muted text-ink-faint'
                ]"
              >
                <Check v-if="s.enabled" class="w-3 h-3" /><X v-else class="w-3 h-3" />
                {{ s.enabled ? 'Yoqilgan' : "O'chirilgan" }}
              </button>
            </td>
            <td class="px-3 py-2.5 text-right">
              <button
                type="button"
                class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-surface-soft hover:text-primary-600"
                @click="openEdit(s)"
              ><Edit3 class="w-3.5 h-3.5" /></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Edit modal -->
    <UIModal v-model="modalOpen" size="lg" :title="`Section: ${editing ? (SECTION_LABELS[editing.key] || editing.key) : ''}`">
      <div class="space-y-4 max-h-[70vh] overflow-y-auto pr-1">
        <p class="text-[11px] text-ink-faint">
          Quyidagi maydonlar bo'sh bo'lsa, frontenddagi standart i18n matnlar ishlatiladi.
          Override kiritilgan bo'lsa — admin matn ustunlik qiladi.
        </p>

        <MultilingualInput v-model="form" base="eyebrow"  label="Eyebrow override" />
        <MultilingualInput v-model="form" base="title"    label="Sarlavha override" />
        <MultilingualInput v-model="form" base="subtitle" label="Subtitle override" textarea :rows="2" />

        <div class="border-t border-surface-muted dark:border-slate-700 pt-4">
          <p class="text-[11px] font-semibold uppercase tracking-wider text-ink-faint mb-3">
            Body (intro va shunga o'xshash sectionlar uchun)
          </p>
          <div class="space-y-3">
            <MultilingualInput v-model="form" base="body_p1" label="1-paragraf" textarea :rows="3" />
            <MultilingualInput v-model="form" base="body_p2" label="2-paragraf" textarea :rows="3" />
            <MultilingualInput v-model="form" base="link_label" label="Havola matni" />
            <div>
              <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">
                Havola URL'i
              </label>
              <input
                v-model="form.link_url"
                type="text"
                placeholder="/about"
                class="w-full px-3 py-2 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:border-primary-500"
              />
            </div>
          </div>
        </div>

        <div class="border-t border-surface-muted dark:border-slate-700 pt-4">
          <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">
            Per-section sozlamalar (JSON)
          </label>
          <textarea
            v-model="form._settingsJson"
            rows="6"
            class="w-full px-3 py-2 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-mono focus:outline-none focus:border-primary-500"
          />
          <p class="mt-1 text-[11px] text-ink-faint">
            Masalan news section uchun: <code class="text-primary-600">{ "limit": 5 }</code>
          </p>
        </div>
      </div>

      <template #footer>
        <UIButton variant="ghost" @click="modalOpen = false">Bekor qilish</UIButton>
        <UIButton variant="accent" :loading="saving" @click="save">
          <template #icon-left><Save class="w-4 h-4" /></template>
          Saqlash
        </UIButton>
      </template>
    </UIModal>
  </div>
</template>
