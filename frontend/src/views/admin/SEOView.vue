<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Save, Plus, Trash2, ExternalLink } from 'lucide-vue-next'
import { AdminSeoAPI } from '@/api/admin'
import UIInput from '@/components/ui/UIInput.vue'
import UIButton from '@/components/ui/UIButton.vue'
import UIModal from '@/components/ui/UIModal.vue'
import UILoader from '@/components/ui/UILoader.vue'
import { useToast } from '@/composables/useToast'

const toast = useToast()

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

onMounted(loadRedirects)
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-xl font-display font-bold text-ink-dark dark:text-white">URL redirectlar</h1>
        <p class="text-sm text-ink-faint mt-0.5">Eski URL'larni yangi manzilga yo'naltirish (301/302)</p>
      </div>
      <UIButton variant="accent" @click="openCreate">
        <template #icon-left><Plus class="w-4 h-4" /></template>
        Qo'shish
      </UIButton>
    </div>

    <UILoader v-if="loadingRed" variant="skeleton-list" :lines="4" />

    <div v-else-if="redirects.length" class="rounded-2xl border border-surface-muted dark:border-slate-700 overflow-hidden bg-white dark:bg-slate-800">
      <table class="w-full text-sm">
        <thead class="bg-surface-soft dark:bg-slate-900/40">
          <tr>
            <th class="px-4 py-3 text-left text-[10px] font-bold uppercase tracking-wider text-ink-faint">Eski yo'l</th>
            <th class="px-4 py-3 text-left text-[10px] font-bold uppercase tracking-wider text-ink-faint">Yangi yo'l</th>
            <th class="px-4 py-3 text-left text-[10px] font-bold uppercase tracking-wider text-ink-faint">Turi</th>
            <th class="px-4 py-3 text-left text-[10px] font-bold uppercase tracking-wider text-ink-faint">Holat</th>
            <th class="px-4 py-3 w-24"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in redirects" :key="r.id" class="border-t border-surface-muted dark:border-slate-700">
            <td class="px-4 py-3 font-mono text-xs text-primary-700 dark:text-primary-300">{{ r.old_path }}</td>
            <td class="px-4 py-3 font-mono text-xs text-ink-faint">
              <span class="inline-flex items-center gap-1"><ExternalLink class="w-3 h-3" />{{ r.new_path }}</span>
            </td>
            <td class="px-4 py-3">
              <span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-surface-soft dark:bg-slate-700 text-ink-medium">{{ r.status_code }}</span>
            </td>
            <td class="px-4 py-3">
              <span :class="['inline-flex items-center gap-1 px-2 py-0.5 text-[11px] font-bold rounded-md',
                             r.is_active ? 'bg-success-light text-success-dark' : 'bg-surface-muted text-ink-faint']">
                {{ r.is_active ? 'Faol' : 'Faol emas' }}
              </span>
            </td>
            <td class="px-4 py-3 text-right">
              <div class="inline-flex items-center gap-0.5">
                <button @click="openEdit(r)"
                        class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-surface-soft hover:text-primary-600">
                  <Save class="w-3.5 h-3.5" />
                </button>
                <button @click="remove(r.id)"
                        class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-danger-light hover:text-danger-dark">
                  <Trash2 class="w-3.5 h-3.5" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-else class="text-center py-16 rounded-2xl border-2 border-dashed border-surface-muted dark:border-slate-700 text-sm text-ink-faint">
      Hozircha redirectlar yo'q
    </p>

    <UIModal :model-value="!!editing" @update:model-value="close" :title="editing?.id ? 'Redirect tahrirlash' : 'Yangi redirect'">
      <div class="space-y-4">
        <UIInput v-model="form.old_path" label="Eski yo'l" placeholder="/old-page" required />
        <UIInput v-model="form.new_path" label="Yangi yo'l" placeholder="/new-page" required />
        <label class="block">
          <span class="text-sm font-medium text-ink-medium dark:text-slate-300">Status code</span>
          <select v-model.number="form.status_code" class="mt-1 w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-800 text-sm">
            <option :value="301">301 — Doimiy</option>
            <option :value="302">302 — Vaqtincha</option>
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
