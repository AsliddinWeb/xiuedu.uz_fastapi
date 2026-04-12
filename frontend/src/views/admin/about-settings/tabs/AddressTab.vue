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
        <h2 class="text-lg font-display font-bold text-ink-dark dark:text-white">Manzil va xarita</h2>
        <p class="text-xs text-ink-faint mt-0.5">Yandex/Google xarita embed URL va kontakt ma'lumotlari</p>
      </div>
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>
        Saqlash
      </UIButton>
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <MultilingualInput v-model="form" base="address" label="Manzil (matn)" placeholder="Toshkent shahar, Mirzo Ulug'bek tumani" />

      <div>
        <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Aloqa email</label>
        <input
          type="email"
          v-model="form.contact_email"
          placeholder="info@xiuedu.uz"
          class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:border-primary-500"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Xarita embed URL</label>
        <input
          type="text"
          v-model="form.map_embed_url"
          placeholder="https://yandex.com/map-widget/v1/?ll=..."
          class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-mono focus:outline-none focus:border-primary-500"
        />
        <p class="mt-1 text-[11px] text-ink-faint">
          Yandex Maps yoki Google Maps embed URL. iframe ichida ko'rsatiladi.
        </p>
      </div>

      <!-- Live preview -->
      <div v-if="form.map_embed_url" class="rounded-lg overflow-hidden border border-surface-muted dark:border-slate-700">
        <iframe
          :src="form.map_embed_url"
          class="w-full h-64"
          loading="lazy"
          frameborder="0"
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
