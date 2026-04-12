<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Save } from 'lucide-vue-next'
import { AdminApplicantsAPI } from '@/api/admin'
import UIButton from '@/components/ui/UIButton.vue'
import MultilingualInput from '@/components/admin/MultilingualInput.vue'
import { useToast } from '@/composables/useToast'

const toast = useToast()
const loading = ref(true)
const saving = ref(false)
const form = reactive({})

async function load() {
  loading.value = true
  try { Object.assign(form, await AdminApplicantsAPI.page.get()) }
  finally { loading.value = false }
}
onMounted(load)

async function save() {
  saving.value = true
  try {
    const { id, updated_at, ...payload } = form
    Object.assign(form, await AdminApplicantsAPI.page.update(payload))
    toast.success('Saqlandi')
  } catch (e) { toast.error(e?.response?.data?.detail || 'Xatolik') }
  finally { saving.value = false }
}
</script>

<template>
  <div v-if="loading" class="text-center py-12 text-ink-faint text-sm">Yuklanmoqda...</div>
  <div v-else>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-lg font-display font-bold text-ink-dark dark:text-white">Sarlavhalar (override)</h2>
        <p class="text-xs text-ink-faint mt-0.5">Hero va har bir section'ning eyebrow + title matnlari. Bo'sh = default i18n.</p>
      </div>
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>Saqlash
      </UIButton>
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Hero (PageHero)</p>
      <MultilingualInput v-model="form" base="hero_eyebrow"  label="Eyebrow" />
      <MultilingualInput v-model="form" base="hero_title"    label="Sarlavha" />
      <MultilingualInput v-model="form" base="hero_subtitle" label="Subtitle" textarea :rows="2" />
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Steps section</p>
      <MultilingualInput v-model="form" base="steps_eyebrow" label="Eyebrow" />
      <MultilingualInput v-model="form" base="steps_title"   label="Sarlavha" />
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Forms section</p>
      <MultilingualInput v-model="form" base="forms_eyebrow" label="Eyebrow" />
      <MultilingualInput v-model="form" base="forms_title"   label="Sarlavha" />
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Timeline section</p>
      <MultilingualInput v-model="form" base="timeline_eyebrow" label="Eyebrow" />
      <MultilingualInput v-model="form" base="timeline_title"   label="Sarlavha" />
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Documents section</p>
      <MultilingualInput v-model="form" base="docs_eyebrow" label="Eyebrow" />
      <MultilingualInput v-model="form" base="docs_title"   label="Sarlavha" />
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">FAQ section</p>
      <MultilingualInput v-model="form" base="faq_eyebrow" label="Eyebrow" />
      <MultilingualInput v-model="form" base="faq_title"   label="Sarlavha" />
    </div>

    <div class="flex justify-end">
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>Saqlash
      </UIButton>
    </div>
  </div>
</template>
