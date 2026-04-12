<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Save } from 'lucide-vue-next'
import { AdminAboutAPI } from '@/api/admin'
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
    const data = await AdminAboutAPI.page.get()
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
        <h2 class="text-lg font-display font-bold text-ink-dark dark:text-white">Hero (sarlavha)</h2>
        <p class="text-xs text-ink-faint mt-0.5">PageHero komponentidagi matnlar. Bo'sh qoldirilsa default i18n ishlatiladi.</p>
      </div>
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>
        Saqlash
      </UIButton>
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 space-y-4">
      <MultilingualInput v-model="form" base="hero_eyebrow"  label="Eyebrow (kichik label)" />
      <MultilingualInput v-model="form" base="hero_title"    label="Sarlavha" />
      <MultilingualInput v-model="form" base="hero_subtitle" label="Subtitle" textarea :rows="3" />
    </div>

    <div class="flex justify-end mt-5">
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>
        Saqlash
      </UIButton>
    </div>
  </div>
</template>
