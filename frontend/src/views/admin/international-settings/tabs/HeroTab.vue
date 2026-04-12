<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Save } from 'lucide-vue-next'
import { AdminIntlAPI } from '@/api/admin'
import UIButton from '@/components/ui/UIButton.vue'
import MultilingualInput from '@/components/admin/MultilingualInput.vue'
import { useToast } from '@/composables/useToast'

const toast = useToast()
const loading = ref(true)
const saving = ref(false)
const form = reactive({})

async function load() {
  loading.value = true
  try { Object.assign(form, await AdminIntlAPI.page.get()) }
  finally { loading.value = false }
}
onMounted(load)

async function save() {
  saving.value = true
  try {
    const { id, updated_at, ...payload } = form
    Object.assign(form, await AdminIntlAPI.page.update(payload))
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
        <h2 class="text-lg font-display font-bold text-ink-dark dark:text-white">Hero, statistika va sarlavhalar</h2>
        <p class="text-xs text-ink-faint mt-0.5">Barcha section eyebrow + title override + 4 ta katta raqam</p>
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

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint mb-4">4 ta statistika</p>
      <div class="grid sm:grid-cols-2 gap-5">
        <div v-for="n in 4" :key="n" class="rounded-lg p-4 bg-surface-soft dark:bg-slate-900/30 space-y-3">
          <p class="text-[11px] font-bold uppercase tracking-wider text-accent-600">Stat {{ n }}</p>
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">Qiymat</label>
            <input type="text" v-model="form[`stat${n}_value`]" placeholder="50+"
                   class="w-full h-9 px-3 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
          <MultilingualInput v-model="form" :base="`stat${n}_label`" label="Label" />
        </div>
      </div>
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Programs section</p>
      <MultilingualInput v-model="form" base="programs_eyebrow" label="Eyebrow" />
      <MultilingualInput v-model="form" base="programs_title"   label="Sarlavha" />
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Partners section</p>
      <MultilingualInput v-model="form" base="partners_eyebrow" label="Eyebrow" />
      <MultilingualInput v-model="form" base="partners_title"   label="Sarlavha" />
    </div>

    <div class="flex justify-end">
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>Saqlash
      </UIButton>
    </div>
  </div>
</template>
