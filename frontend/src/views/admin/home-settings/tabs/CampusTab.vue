<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Save, Plus, Trash2 } from 'lucide-vue-next'
import { AdminHomeAPI } from '@/api/admin'
import UIButton from '@/components/ui/UIButton.vue'
import MultilingualInput from '@/components/admin/MultilingualInput.vue'
import MediaPicker from '@/components/admin/MediaPicker.vue'
import { useToast } from '@/composables/useToast'

const toast = useToast()
const loading = ref(true)
const saving = ref(false)
const form = reactive({ bullets: [] })

async function load() {
  loading.value = true
  try {
    const data = await AdminHomeAPI.campus.get()
    Object.assign(form, data)
    if (!Array.isArray(form.bullets)) form.bullets = []
  } finally {
    loading.value = false
  }
}
onMounted(load)

function addBullet() {
  form.bullets.push({ uz: '', ru: '', en: '' })
}
function removeBullet(i) {
  form.bullets.splice(i, 1)
}

async function save() {
  saving.value = true
  try {
    const { id, updated_at, ...payload } = form
    const updated = await AdminHomeAPI.campus.update(payload)
    Object.assign(form, updated)
    toast.success('Saqlandi')
  } catch (e) {
    toast.error(e?.response?.data?.detail || 'Saqlashda xatolik')
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
        <h2 class="text-lg font-display font-bold text-ink-dark dark:text-white">Kampus section</h2>
        <p class="text-xs text-ink-faint mt-0.5">3 ta rasm + matn + bullet ro'yxat + video link</p>
      </div>
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>
        Saqlash
      </UIButton>
    </div>

    <!-- Images -->
    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Rasmlar</p>
      <MediaPicker v-model="form.main_image" label="Asosiy rasm (katta)" hint="Katta col-span-2 hujayradagi rasm" />
      <div class="grid sm:grid-cols-2 gap-4">
        <MediaPicker v-model="form.image_2" label="Rasm 2" />
        <MediaPicker v-model="form.image_3" label="Rasm 3" />
      </div>
      <div>
        <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Video URL (ixtiyoriy)</label>
        <input
          type="text"
          v-model="form.video_url"
          placeholder="https://youtube.com/..."
          class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:border-primary-500"
        />
      </div>
    </div>

    <!-- Text -->
    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Matn</p>
      <MultilingualInput v-model="form" base="eyebrow" label="Eyebrow" placeholder="Talabalar hayoti" />
      <MultilingualInput v-model="form" base="title"   label="Sarlavha" placeholder="Bizning kampus" />
      <MultilingualInput v-model="form" base="text"    label="Matn" textarea :rows="3" />
    </div>

    <!-- Bullets -->
    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5">
      <div class="flex items-center justify-between mb-4">
        <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Bullets ro'yxat</p>
        <UIButton variant="ghost" size="sm" @click="addBullet">
          <template #icon-left><Plus class="w-4 h-4" /></template>
          Qo'shish
        </UIButton>
      </div>
      <div v-if="!form.bullets.length" class="text-xs text-ink-faint text-center py-6">
        Hozircha bullet yo'q
      </div>
      <div v-else class="space-y-3">
        <div
          v-for="(b, i) in form.bullets"
          :key="i"
          class="grid sm:grid-cols-[1fr_1fr_1fr_auto] gap-2 items-end p-3 rounded-lg bg-surface-soft dark:bg-slate-900/30"
        >
          <div>
            <label class="block text-[10px] uppercase tracking-wider text-ink-faint mb-1">UZ</label>
            <input type="text" v-model="b.uz" class="w-full h-9 px-3 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
          <div>
            <label class="block text-[10px] uppercase tracking-wider text-ink-faint mb-1">RU</label>
            <input type="text" v-model="b.ru" class="w-full h-9 px-3 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
          <div>
            <label class="block text-[10px] uppercase tracking-wider text-ink-faint mb-1">EN</label>
            <input type="text" v-model="b.en" class="w-full h-9 px-3 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
          <button
            type="button"
            class="w-9 h-9 grid place-items-center rounded-lg text-ink-faint hover:text-danger hover:bg-danger-light"
            @click="removeBullet(i)"
          ><Trash2 class="w-3.5 h-3.5" /></button>
        </div>
      </div>
    </div>

    <!-- CTA -->
    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">CTA tugma</p>
      <MultilingualInput v-model="form" base="cta_label" label="Tugma matni" placeholder="Galereyani ko'rish" />
      <div>
        <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">URL</label>
        <input
          type="text"
          v-model="form.cta_url"
          placeholder="/gallery"
          class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:border-primary-500"
        />
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
