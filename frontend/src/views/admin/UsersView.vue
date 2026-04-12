<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Plus, Edit3, Power, Trash2, Mail, Eye, EyeOff, Inbox } from 'lucide-vue-next'
import { AdminUsersAPI } from '@/api/admin'
import UIModal from '@/components/ui/UIModal.vue'
import UIInput from '@/components/ui/UIInput.vue'
import { roleBadge } from '@/utils/roles'
import { useToast } from '@/composables/useToast'
import { useConfirm } from '@/composables/useConfirm'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const toast = useToast()
const confirm = useConfirm()

const items = ref([])
const loading = ref(true)
const editing = ref(null)
const isCreate = ref(false)
const showPwd = ref(false)

const form = reactive({
  email: '', full_name: '', password: '', role: 'page_editor', is_active: true
})

async function load() {
  loading.value = true
  try { items.value = await AdminUsersAPI.list() }
  finally { loading.value = false }
}
onMounted(load)

function openCreate() {
  isCreate.value = true
  editing.value = {}
  Object.assign(form, { email: '', full_name: '', password: '', role: 'page_editor', is_active: true })
  showPwd.value = false
}
function openEdit(u) {
  isCreate.value = false
  editing.value = u
  Object.assign(form, { email: u.email, full_name: u.full_name, password: '', role: u.role, is_active: u.is_active })
  showPwd.value = false
}
function close() { editing.value = null }

async function save() {
  try {
    if (isCreate.value) {
      await AdminUsersAPI.create(form)
      toast.success("Foydalanuvchi yaratildi")
    } else {
      const payload = { ...form }
      if (!payload.password) delete payload.password
      delete payload.email
      await AdminUsersAPI.update(editing.value.id, payload)
      toast.success("Yangilandi")
    }
    close()
    load()
  } catch (e) {
    toast.error(e?.response?.data?.detail || "Xatolik")
  }
}

async function toggleActive(u) {
  await AdminUsersAPI.toggleActive(u.id)
  load()
}

async function deleteUser(u) {
  const ok = await confirm({
    title: "O'chirish",
    message: `${u.full_name} ni o'chirishni tasdiqlaysizmi? Bu amalni qaytarib bo'lmaydi.`,
    confirmLabel: "O'chirish",
    danger: true
  })
  if (!ok) return
  await AdminUsersAPI.remove(u.id)
  toast.success("O'chirildi")
  load()
}

function fmtDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('uz-UZ', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const rolesAvailable = [
  { value: 'admin',           label: 'Admin' },
  { value: 'content_manager', label: 'Content Manager' },
  { value: 'page_editor',     label: 'Page Editor' }
]
</script>

<template>
  <div>
    <!-- Page header -->
    <div class="flex flex-wrap items-center justify-between gap-3 mb-6">
      <div>
        <h1 class="text-xl font-display font-bold text-ink-dark dark:text-white">Foydalanuvchilar</h1>
        <p class="text-sm text-ink-faint mt-0.5">{{ items.length }} ta hisob</p>
      </div>
      <button class="btn-primary btn-md" @click="openCreate">
        <Plus class="w-4 h-4" />
        Foydalanuvchi qo'shish
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="card p-12 text-center text-sm text-ink-faint">Yuklanmoqda...</div>

    <!-- Empty -->
    <div v-else-if="!items.length" class="card p-16 text-center">
      <Inbox class="w-12 h-12 text-ink-faint mx-auto mb-3" stroke-width="1.4" />
      <p class="text-sm text-ink-light">Foydalanuvchilar yo'q</p>
    </div>

    <!-- Table -->
    <div v-else class="card overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-surface-soft dark:bg-slate-900/50 text-ink-light dark:text-slate-400 text-[11px] uppercase tracking-wider">
          <tr>
            <th class="text-left px-4 py-3 font-semibold">Foydalanuvchi</th>
            <th class="text-left px-4 py-3 font-semibold hidden md:table-cell">Rol</th>
            <th class="text-left px-4 py-3 font-semibold hidden md:table-cell">Holat</th>
            <th class="text-left px-4 py-3 font-semibold hidden lg:table-cell">Oxirgi kirish</th>
            <th class="px-4 py-3"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="u in items"
            :key="u.id"
            class="border-t border-surface-muted dark:border-slate-800 hover:bg-surface-soft/50 dark:hover:bg-slate-800/30"
          >
            <td class="px-4 py-3">
              <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-full bg-gradient-to-br from-primary-500 to-primary-800 grid place-items-center text-white text-xs font-bold ring-2 ring-primary-100 dark:ring-primary-900 flex-shrink-0">
                  {{ u.full_name.charAt(0) }}
                </div>
                <div class="min-w-0">
                  <p class="font-semibold text-ink-dark dark:text-white truncate">{{ u.full_name }}</p>
                  <p class="text-xs text-ink-faint inline-flex items-center gap-1">
                    <Mail class="w-3 h-3" /> {{ u.email }}
                  </p>
                </div>
              </div>
            </td>
            <td class="px-4 py-3 hidden md:table-cell">
              <span :class="['inline-block px-2 py-0.5 text-[10px] uppercase tracking-wider font-bold rounded border', roleBadge(u.role).cls]">
                {{ roleBadge(u.role).label }}
              </span>
            </td>
            <td class="px-4 py-3 hidden md:table-cell">
              <button
                v-if="u.role !== 'superadmin' && u.id !== auth.user?.id"
                @click="toggleActive(u)"
                :class="[
                  'relative inline-flex h-5 w-9 items-center rounded-full transition-colors',
                  u.is_active ? 'bg-success' : 'bg-surface-subtle dark:bg-slate-600'
                ]"
                :aria-pressed="u.is_active"
                v-tooltip="u.is_active ? 'Faolsizlantirish' : 'Faollashtirish'"
              >
                <span :class="['inline-block h-3.5 w-3.5 transform rounded-full bg-white transition', u.is_active ? 'translate-x-[1.125rem]' : 'translate-x-[2px]']" />
              </button>
              <span
                v-else
                :class="['inline-flex items-center gap-1.5 px-2 py-0.5 text-xs rounded-full',
                         u.is_active ? 'bg-success-light text-success-dark' : 'bg-surface-muted text-ink-faint']"
              >
                <span class="w-1.5 h-1.5 rounded-full" :class="u.is_active ? 'bg-success' : 'bg-ink-faint'" />
                {{ u.is_active ? 'Faol' : 'Faol emas' }}
              </span>
            </td>
            <td class="px-4 py-3 hidden lg:table-cell text-xs text-ink-light">{{ fmtDate(u.last_login) }}</td>
            <td class="px-4 py-3 text-right">
              <div class="inline-flex items-center gap-0.5">
                <button
                  v-if="u.role !== 'superadmin'"
                  @click="openEdit(u)"
                  class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-surface-soft hover:text-primary-600"
                  v-tooltip="'Tahrirlash'"
                ><Edit3 class="w-3.5 h-3.5" /></button>
                <button
                  v-if="u.role !== 'superadmin' && u.id !== auth.user?.id"
                  @click="deleteUser(u)"
                  class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-danger-light hover:text-danger-dark"
                  v-tooltip="&quot;O'chirish&quot;"
                ><Trash2 class="w-3.5 h-3.5" /></button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Edit/Create modal -->
    <UIModal :model-value="!!editing" @update:model-value="close" :title="isCreate ? 'Yangi foydalanuvchi' : 'Tahrirlash'" size="md">
      <div class="space-y-4">
        <UIInput v-model="form.full_name" label="To'liq ism" required />
        <UIInput v-model="form.email" type="email" label="Email" required :disabled="!isCreate" />

        <div>
          <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">
            {{ isCreate ? 'Parol' : 'Yangi parol (ixtiyoriy)' }}
            <span v-if="isCreate" class="text-danger ml-0.5">*</span>
          </label>
          <div class="relative">
            <input
              v-model="form.password"
              :type="showPwd ? 'text' : 'password'"
              class="input-field pr-10"
              :required="isCreate"
              placeholder="••••••••"
            />
            <button
              type="button"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-ink-faint hover:text-ink-medium"
              @click="showPwd = !showPwd"
              :aria-label="showPwd ? 'Yashirish' : 'Korsatish'"
            >
              <EyeOff v-if="showPwd" class="w-4 h-4" />
              <Eye v-else class="w-4 h-4" />
            </button>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Rol</label>
          <select v-model="form.role" class="input-field">
            <option v-for="r in rolesAvailable" :key="r.value" :value="r.value">{{ r.label }}</option>
          </select>
        </div>

        <label class="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" v-model="form.is_active" class="rounded border-surface-muted text-primary-600 focus:ring-primary-500" />
          <span class="text-sm text-ink-medium dark:text-slate-300">Faol holat</span>
        </label>
      </div>
      <template #footer>
        <button class="btn-ghost btn-sm" @click="close">Bekor qilish</button>
        <button class="btn-primary btn-sm" @click="save">Saqlash</button>
      </template>
    </UIModal>
  </div>
</template>
