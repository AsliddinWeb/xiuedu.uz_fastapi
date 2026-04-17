<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Save } from 'lucide-vue-next'
import UIButton from '@/components/ui/UIButton.vue'
import MultilingualInput from '@/components/admin/MultilingualInput.vue'
import MediaPicker from '@/components/admin/MediaPicker.vue'
import api from '@/api/client'

const loading = ref(true)
const saving = ref(false)
const form = reactive({})
const msg = ref('')

async function load() {
  loading.value = true
  try {
    const { data } = await api.get('/admin/site-settings/')
    Object.assign(form, data)
  } finally { loading.value = false }
}
onMounted(load)

async function save() {
  saving.value = true
  try {
    const { id, updated_at, ...payload } = form
    const { data } = await api.put('/admin/site-settings/', payload)
    Object.assign(form, data)
    msg.value = 'Saqlandi!'
    setTimeout(() => { msg.value = '' }, 3000)
  } catch (e) {
    msg.value = e?.response?.data?.detail || 'Xatolik'
  } finally { saving.value = false }
}
</script>

<template>
  <div class="max-w-4xl">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-xl font-display font-bold text-ink-dark dark:text-white">Sayt sozlamalari</h1>
        <p class="text-sm text-ink-faint mt-0.5">Logo, nom, ijtimoiy tarmoqlar, footer va analytics</p>
      </div>
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>
        Saqlash
      </UIButton>
    </div>

    <Transition enter-active-class="transition duration-300" enter-from-class="opacity-0 -translate-y-2"
                leave-active-class="transition duration-200" leave-to-class="opacity-0">
      <div v-if="msg" class="fixed top-4 right-4 z-50 px-5 py-3 rounded-xl shadow-lg text-sm font-semibold bg-success text-white">
        {{ msg }}
      </div>
    </Transition>

    <div v-if="loading" class="text-center py-12 text-ink-faint">Yuklanmoqda...</div>

    <div v-else class="space-y-5">
      <!-- Branding -->
      <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 space-y-4">
        <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Branding</p>
        <MultilingualInput v-model="form" base="site_name" label="Sayt nomi" placeholder="Xalqaro Innovatsion Universiteti" />
        <div>
          <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Qisqa nom</label>
          <input type="text" v-model="form.site_short_name" placeholder="XIU Edu"
                 class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
        </div>
        <div class="grid sm:grid-cols-2 gap-4">
          <MediaPicker v-model="form.logo_url" label="Logo (light bg)" />
          <MediaPicker v-model="form.logo_dark_url" label="Logo (dark bg)" />
        </div>
        <div class="grid sm:grid-cols-2 gap-4">
          <MediaPicker v-model="form.favicon_url" label="Favicon" />
          <MediaPicker v-model="form.og_image_url" label="OG Image (default)" />
        </div>
      </div>

      <!-- Contact -->
      <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 space-y-4">
        <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Kontakt (global)</p>
        <div class="grid sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">Telefon</label>
            <input type="text" v-model="form.phone" placeholder="+998 55 406-15-15"
                   class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">Email</label>
            <input type="email" v-model="form.email" placeholder="info@xiuedu.uz"
                   class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
        </div>
        <MultilingualInput v-model="form" base="address" label="Manzil" />
      </div>

      <!-- External links -->
      <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 space-y-4">
        <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Tashqi havolalar</p>
        <div class="grid sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">Qabul URL</label>
            <input type="text" v-model="form.admission_url" placeholder="https://qabul.xiuedu.uz"
                   class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">HEMIS URL</label>
            <input type="text" v-model="form.hemis_url" placeholder="https://student.xiuedu.uz"
                   class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
        </div>
      </div>

      <!-- Social -->
      <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 space-y-4">
        <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Ijtimoiy tarmoqlar</p>
        <div class="grid sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">Telegram</label>
            <input type="text" v-model="form.telegram_url" placeholder="https://t.me/..."
                   class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">Instagram</label>
            <input type="text" v-model="form.instagram_url" placeholder="https://instagram.com/..."
                   class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">Facebook</label>
            <input type="text" v-model="form.facebook_url" placeholder="https://facebook.com/..."
                   class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">YouTube</label>
            <input type="text" v-model="form.youtube_url" placeholder="https://youtube.com/..."
                   class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 space-y-4">
        <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Footer</p>
        <MultilingualInput v-model="form" base="footer_desc" label="Footer tavsif" textarea :rows="3" />
      </div>

      <!-- Analytics -->
      <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 space-y-4">
        <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Analytics</p>
        <div class="grid sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">Google Analytics ID</label>
            <input type="text" v-model="form.google_analytics_id" placeholder="G-XXXXXXXXXX"
                   class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm font-mono" />
          </div>
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">Yandex Metrica ID</label>
            <input type="text" v-model="form.yandex_metrica_id" placeholder="12345678"
                   class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm font-mono" />
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
  </div>
</template>
