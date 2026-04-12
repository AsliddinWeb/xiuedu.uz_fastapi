<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Save, Plus, Trash2, ExternalLink } from 'lucide-vue-next'
import { AdminSeoAPI } from '@/api/admin'
import UITabs from '@/components/ui/UITabs.vue'
import UIInput from '@/components/ui/UIInput.vue'
import UIButton from '@/components/ui/UIButton.vue'
import UIModal from '@/components/ui/UIModal.vue'
import UILoader from '@/components/ui/UILoader.vue'
import { useToast } from '@/composables/useToast'

const toast = useToast()
const tabs = [
  { key: 'globals',   label: 'Global sozlamalar' },
  { key: 'redirects', label: 'Redirectlar' }
]
const active = ref('globals')

// ===== Globals =====
const GLOBAL_KEYS = [
  { key: 'site_title_template', label: 'Site title template (%s | XIU Edu)', placeholder: '%s | XIU Edu' },
  { key: 'default_description_uz', label: 'Default description (UZ)', textarea: true },
  { key: 'default_description_ru', label: 'Default description (RU)', textarea: true },
  { key: 'default_description_en', label: 'Default description (EN)', textarea: true },
  { key: 'default_og_image',    label: 'Default og:image URL' },
  { key: 'google_analytics_id', label: 'Google Analytics ID', placeholder: 'G-XXXXXX' },
  { key: 'yandex_metrica_id',   label: 'Yandex Metrica ID',   placeholder: '12345678' }
]
const globals = reactive({})
const loadingGlobals = ref(true)

async function loadGlobals() {
  loadingGlobals.value = true
  try {
    const rows = await AdminSeoAPI.globals()
    for (const r of rows) globals[r.key] = r.value
  } finally { loadingGlobals.value = false }
}

async function saveGlobal(item) {
  try {
    await AdminSeoAPI.setGlobal(item.key, { value: globals[item.key] || '', description: item.label })
    toast.success("Saqlandi")
  } catch (_) {}
}

async function saveAllGlobals() {
  await Promise.all(GLOBAL_KEYS.map(k => AdminSeoAPI.setGlobal(k.key, { value: globals[k.key] || '', description: k.label })))
  toast.success("Barchasi saqlandi")
}

// ===== Redirects =====
const redirects = ref([])
const loadingRed = ref(false)
const editing = ref(null)
const form = reactive({ old_path: '', new_path: '', status_code: 301, is_active: true })

async function loadRedirects() {
  loadingRed.value = true
  try { redirects.value = await AdminSeoAPI.redirects() }
  finally { loadingRed.value = false }
}

function openCreate() {
  editing.value = {}
  Object.assign(form, { old_path: '', new_path: '', status_code: 301, is_active: true })
}
function openEdit(r) {
  editing.value = r
  Object.assign(form, { old_path: r.old_path, new_path: r.new_path, status_code: r.status_code, is_active: r.is_active })
}
function close() { editing.value = null }

async function save() {
  try {
    if (editing.value?.id) await AdminSeoAPI.updateRedirect(editing.value.id, form)
    else await AdminSeoAPI.createRedirect(form)
    toast.success("Saqlandi")
    close()
    loadRedirects()
  } catch (e) {
    toast.error(e?.response?.data?.detail || "Xatolik")
  }
}

async function remove(id) {
  await AdminSeoAPI.removeRedirect(id)
  toast.success("O'chirildi")
  loadRedirects()
}

onMounted(() => { loadGlobals(); loadRedirects() })
</script>

<template>
  <div>
    <UITabs v-model="active" :tabs="tabs">
      <template #default="{ active: a }">
        <!-- ===== Globals ===== -->
        <div v-if="a === 'globals'" class="max-w-3xl space-y-4">
          <UILoader v-if="loadingGlobals" variant="skeleton-text" :lines="6" />
          <template v-else>
            <UIInput
              v-for="item in GLOBAL_KEYS"
              :key="item.key"
              :model-value="globals[item.key] || ''"
              @update:model-value="globals[item.key] = $event"
              :label="item.label"
              :placeholder="item.placeholder"
              :textarea="item.textarea"
              :rows="3"
            />
            <div class="pt-3">
              <UIButton variant="accent" @click="saveAllGlobals">
                <template #icon-left><Save class="w-4 h-4" /></template>
                Saqlash
              </UIButton>
            </div>
          </template>
        </div>

        <!-- ===== Redirects ===== -->
        <div v-else>
          <div class="flex items-center justify-between mb-4">
            <p class="text-sm text-ink-faint dark:text-neutral-400">{{ redirects.length }} ta redirect</p>
            <UIButton variant="accent" @click="openCreate">
              <template #icon-left><Plus class="w-4 h-4" /></template>
              Qo'shish
            </UIButton>
          </div>

          <UILoader v-if="loadingRed" variant="skeleton-list" :lines="4" />
          <div v-else-if="redirects.length" class="rounded-2xl border border-surface-muted dark:border-slate-700 overflow-hidden bg-white dark:bg-slate-800">
            <table class="w-full text-sm">
              <thead class="bg-surface-soft dark:bg-slate-900 text-neutral-600 dark:text-neutral-300 text-xs uppercase tracking-wide">
                <tr>
                  <th class="px-4 py-3 text-left">Old path</th>
                  <th class="px-4 py-3 text-left">New path</th>
                  <th class="px-4 py-3 text-left">Type</th>
                  <th class="px-4 py-3 text-left">Holat</th>
                  <th class="px-4 py-3"></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="r in redirects" :key="r.id" class="border-t border-surface-muted dark:border-slate-700">
                  <td class="px-4 py-3 font-mono text-xs text-primary-700 dark:text-white">{{ r.old_path }}</td>
                  <td class="px-4 py-3 font-mono text-xs text-ink-faint inline-flex items-center gap-1 mt-2"><ExternalLink class="w-3 h-3" />{{ r.new_path }}</td>
                  <td class="px-4 py-3"><span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-neutral-100 dark:bg-slate-900">{{ r.status_code }}</span></td>
                  <td class="px-4 py-3"><span :class="['inline-flex items-center gap-1.5 px-2 py-0.5 text-xs rounded-full', r.is_active ? 'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300' : 'bg-neutral-100 text-ink-faint']">{{ r.is_active ? 'Faol' : 'Faol emas' }}</span></td>
                  <td class="px-4 py-3 text-right">
                    <button @click="openEdit(r)" class="w-8 h-8 grid place-items-center rounded text-ink-faint hover:bg-neutral-100 dark:hover:bg-primary-700 hover:text-accent-500 inline-block"><Save class="w-4 h-4" /></button>
                    <button @click="remove(r.id)" class="w-8 h-8 grid place-items-center rounded text-ink-faint hover:bg-neutral-100 dark:hover:bg-primary-700 hover:text-danger inline-block"><Trash2 class="w-4 h-4" /></button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <p v-else class="text-center py-12 text-ink-faint">Hozircha redirectlar yo'q</p>
        </div>
      </template>
    </UITabs>

    <UIModal :model-value="!!editing" @update:model-value="close" :title="editing?.id ? 'Redirect tahrirlash' : 'Yangi redirect'">
      <div class="space-y-4">
        <UIInput v-model="form.old_path" label="Eski yo'l" placeholder="/old-page" required />
        <UIInput v-model="form.new_path" label="Yangi yo'l" placeholder="/new-page" required />
        <label class="block">
          <span class="text-sm font-medium text-ink-medium dark:text-slate-300">Status code</span>
          <select v-model.number="form.status_code" class="mt-1 w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-800 text-sm">
            <option :value="301">301 — Permanent</option>
            <option :value="302">302 — Temporary</option>
          </select>
        </label>
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" v-model="form.is_active" class="w-4 h-4 accent-accent-500" />
          <span class="text-sm">Faol</span>
        </label>
      </div>
      <template #footer>
        <UIButton variant="ghost" @click="close">Bekor</UIButton>
        <UIButton variant="accent" @click="save">Saqlash</UIButton>
      </template>
    </UIModal>
  </div>
</template>
