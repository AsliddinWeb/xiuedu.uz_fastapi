<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Save } from 'lucide-vue-next'
import { AdminContactPageAPI } from '@/api/admin'
import UIButton from '@/components/ui/UIButton.vue'
import MultilingualInput from '@/components/admin/MultilingualInput.vue'
import { useToast } from '@/composables/useToast'

const toast = useToast()
const loading = ref(true)
const saving = ref(false)
const form = reactive({})

async function load() {
  loading.value = true
  try { Object.assign(form, await AdminContactPageAPI.get()) }
  finally { loading.value = false }
}
onMounted(load)

async function save() {
  saving.value = true
  try {
    const { id, updated_at, ...payload } = form
    Object.assign(form, await AdminContactPageAPI.update(payload))
    toast.success('Saqlandi')
  } catch (e) { toast.error(e?.response?.data?.detail || 'Xatolik') }
  finally { saving.value = false }
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-xl font-display font-bold text-ink-dark dark:text-white">Aloqa sahifasi</h1>
        <p class="text-sm text-ink-faint mt-0.5">Hero, kontakt ma'lumotlari, forma matnlari va xarita</p>
      </div>
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>
        Saqlash
      </UIButton>
    </div>

    <div v-if="loading" class="text-center py-12 text-ink-faint text-sm">Yuklanmoqda...</div>

    <div v-else class="space-y-5 max-w-4xl">
      <!-- Hero -->
      <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 space-y-4">
        <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Hero (PageHero)</p>
        <MultilingualInput v-model="form" base="hero_eyebrow"  label="Eyebrow" />
        <MultilingualInput v-model="form" base="hero_title"    label="Sarlavha" />
        <MultilingualInput v-model="form" base="hero_subtitle" label="Subtitle" textarea :rows="2" />
      </div>

      <!-- Contact info -->
      <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 space-y-4">
        <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Kontakt ma'lumotlari</p>
        <MultilingualInput v-model="form" base="address" label="Manzil" />
        <div class="grid sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Telefon</label>
            <input type="text" v-model="form.phone" placeholder="+998 55 406-15-15"
                   class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Email</label>
            <input type="email" v-model="form.email" placeholder="info@xiuedu.uz"
                   class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
        </div>
        <MultilingualInput v-model="form" base="working_hours" label="Ish vaqti" placeholder="Du-Ju: 09:00 — 18:00" />
      </div>

      <!-- Form section -->
      <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 space-y-4">
        <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Forma sarlavhasi</p>
        <MultilingualInput v-model="form" base="form_title"    label="Sarlavha" placeholder="Bizga yozing" />
        <MultilingualInput v-model="form" base="form_subtitle" label="Subtitle" textarea :rows="2" />
      </div>

      <!-- Map -->
      <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 space-y-4">
        <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Xarita</p>
        <div>
          <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Embed URL</label>
          <input type="text" v-model="form.map_embed_url" placeholder="https://yandex.com/map-widget/v1/?ll=..."
                 class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-mono" />
        </div>
        <div v-if="form.map_embed_url" class="rounded-lg overflow-hidden border border-surface-muted dark:border-slate-700">
          <iframe :src="form.map_embed_url" class="w-full h-56" loading="lazy" frameborder="0" />
        </div>
      </div>

      <div class="flex justify-end">
        <UIButton variant="accent" :loading="saving" @click="save">
          <template #icon-left><Save class="w-4 h-4" /></template>
          Saqlash
        </UIButton>
      </div>
    </div>
  </div>
</template>
