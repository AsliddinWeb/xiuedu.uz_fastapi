<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Save } from 'lucide-vue-next'
import { AdminHomeAPI } from '@/api/admin'
import UIButton from '@/components/ui/UIButton.vue'
import MultilingualInput from '@/components/admin/MultilingualInput.vue'
import { useToast } from '@/composables/useToast'

const toast = useToast()
const loading = ref(true)
const saving = ref(false)
const form = reactive({})

async function load() {
  loading.value = true
  try {
    const data = await AdminHomeAPI.finalCta.get()
    Object.assign(form, data)
  } finally {
    loading.value = false
  }
}
onMounted(load)

async function save() {
  saving.value = true
  try {
    const { id, updated_at, ...payload } = form
    const updated = await AdminHomeAPI.finalCta.update(payload)
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
        <h2 class="text-lg font-display font-bold text-ink-dark dark:text-white">Yakuniy CTA</h2>
        <p class="text-xs text-ink-faint mt-0.5">Bosh sahifaning eng pastidagi qora gradient banner</p>
      </div>
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>
        Saqlash
      </UIButton>
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5">
      <label class="flex items-center justify-between gap-3 cursor-pointer">
        <span class="text-sm font-bold text-ink-dark dark:text-white">Banner ko'rsatilsin</span>
        <input type="checkbox" v-model="form.enabled" class="w-5 h-5 accent-accent-500" />
      </label>
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Matn</p>
      <MultilingualInput v-model="form" base="eyebrow" label="Eyebrow" placeholder="2026 / 2027 qabul" />
      <MultilingualInput v-model="form" base="title"   label="Sarlavha" />
      <MultilingualInput v-model="form" base="text"    label="Tavsif" textarea :rows="2" />
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">CTA tugma</p>
      <MultilingualInput v-model="form" base="cta_label" label="Tugma matni" />
      <div class="grid sm:grid-cols-[1fr_auto] gap-3 items-end">
        <div>
          <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">URL</label>
          <input
            type="text"
            v-model="form.cta_url"
            class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:border-primary-500"
          />
        </div>
        <label class="flex items-center gap-2 h-10">
          <input type="checkbox" v-model="form.cta_external" class="w-4 h-4 accent-accent-500" />
          <span class="text-sm">Tashqi link</span>
        </label>
      </div>
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint mb-3">Telefon raqami</p>
      <div class="grid sm:grid-cols-2 gap-3">
        <div>
          <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Ko'rinadigan label</label>
          <input
            type="text"
            v-model="form.phone_label"
            placeholder="+998 55 406-15-15"
            class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:border-primary-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">tel: URL</label>
          <input
            type="text"
            v-model="form.phone_url"
            placeholder="+998554061515"
            class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:border-primary-500"
          />
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
