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
        <h2 class="text-lg font-display font-bold text-ink-dark dark:text-white">Aloqa CTA</h2>
        <p class="text-xs text-ink-faint mt-0.5">Sahifa pastidagi xalqaro bo'lim aloqa kartochkasi</p>
      </div>
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>Saqlash
      </UIButton>
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Matn</p>
      <MultilingualInput v-model="form" base="cta_title" label="Sarlavha" placeholder="Xalqaro bo'lim" />
      <MultilingualInput v-model="form" base="cta_text"  label="Tavsif" textarea :rows="2" />
    </div>

    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint mb-3">Aloqa</p>
      <div class="space-y-3">
        <div>
          <label class="block text-sm font-medium text-ink-medium mb-1.5">Email</label>
          <input type="email" v-model="form.cta_email" placeholder="international@xiuedu.uz"
                 class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
        </div>
        <div class="grid sm:grid-cols-2 gap-3">
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">Telefon (label)</label>
            <input type="text" v-model="form.cta_phone_label" placeholder="+998 55 406-15-15"
                   class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">tel: URL</label>
            <input type="text" v-model="form.cta_phone_url" placeholder="+998554061515"
                   class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
        </div>
      </div>
    </div>

    <div class="flex justify-end">
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>Saqlash
      </UIButton>
    </div>
  </div>
</template>
