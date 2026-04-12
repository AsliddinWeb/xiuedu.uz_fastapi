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
  try { Object.assign(form, await AdminAboutAPI.page.get()) }
  finally { loading.value = false }
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
  } finally { saving.value = false }
}
</script>

<template>
  <div v-if="loading" class="text-center py-12 text-ink-faint text-sm">Yuklanmoqda...</div>
  <div v-else>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-lg font-display font-bold text-ink-dark dark:text-white">Missiya, vizyon, qadriyatlar</h2>
        <p class="text-xs text-ink-faint mt-0.5">3 ta card matni</p>
      </div>
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>
        Saqlash
      </UIButton>
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Section sarlavhasi</p>
      <MultilingualInput v-model="form" base="mvv_eyebrow" label="Eyebrow" />
      <MultilingualInput v-model="form" base="mvv_title"   label="Sarlavha" />
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Card matnlari</p>
      <MultilingualInput v-model="form" base="mission" label="Missiya"      textarea :rows="3" />
      <MultilingualInput v-model="form" base="vision"  label="Vizyon"       textarea :rows="3" />
      <MultilingualInput v-model="form" base="values"  label="Qadriyatlar"  textarea :rows="3" />
    </div>

    <div class="flex justify-end">
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>
        Saqlash
      </UIButton>
    </div>
  </div>
</template>
