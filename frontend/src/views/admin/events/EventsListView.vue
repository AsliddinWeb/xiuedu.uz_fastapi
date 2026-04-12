<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  Plus, Search, Eye, Edit3, Trash2, ExternalLink, CalendarDays,
  CheckCircle2, Circle, ChevronLeft, ChevronRight, MapPin
} from 'lucide-vue-next'
import { AdminEventsAPI } from '@/api/admin'
import UIDataTable from '@/components/ui/UIDataTable.vue'
import UIInput from '@/components/ui/UIInput.vue'
import { useToast } from '@/composables/useToast'
import { useConfirm } from '@/composables/useConfirm'

const router = useRouter()
const toast = useToast()
const confirm = useConfirm()

const items = ref([])
const total = ref(0)
const loading = ref(true)
const page = ref(1)
const perPage = 20
const query = ref('')
const filterStatus = ref('')
const filterWhen = ref('')
const selectedIds = ref([])
const tableRef = ref(null)

let debounceT
watch(query, () => {
  clearTimeout(debounceT)
  debounceT = setTimeout(load, 300)
})
watch([page], load)

async function load() {
  loading.value = true
  try {
    const res = await AdminEventsAPI.list({ page: page.value, limit: perPage })
    items.value = res.items || []
    total.value = res.total || 0
  } finally {
    loading.value = false
  }
}
onMounted(load)

const filtered = computed(() => {
  let arr = items.value
  if (query.value) {
    const q = query.value.toLowerCase()
    arr = arr.filter(e =>
      (e.title_uz || '').toLowerCase().includes(q) ||
      (e.slug || '').toLowerCase().includes(q) ||
      (e.location_uz || '').toLowerCase().includes(q)
    )
  }
  if (filterStatus.value === 'published') arr = arr.filter(e => e.is_published)
  if (filterStatus.value === 'draft')     arr = arr.filter(e => !e.is_published)
  if (filterWhen.value === 'upcoming') {
    const now = Date.now()
    arr = arr.filter(e => new Date(e.starts_at).getTime() >= now)
  } else if (filterWhen.value === 'past') {
    const now = Date.now()
    arr = arr.filter(e => new Date(e.starts_at).getTime() < now)
  }
  return arr
})

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / perPage)))

const columns = [
  { key: 'cover',   label: '' },
  { key: 'title',   label: 'Tadbir' },
  { key: 'date',    label: 'Sana' },
  { key: 'place',   label: 'Joy' },
  { key: 'status',  label: 'Holat' },
  { key: 'actions', label: '', align: 'right' }
]

async function bulkDelete() {
  const ok = await confirm({
    title: "O'chirishni tasdiqlang",
    message: `Tanlangan ${selectedIds.value.length} ta tadbir o'chiriladi. Bu amalni qaytarib bo'lmaydi.`,
    confirmLabel: "O'chirish",
    danger: true
  })
  if (!ok) return
  const ids = [...selectedIds.value]
  await Promise.all(ids.map(id => AdminEventsAPI.remove(id)))
  toast.success(`${ids.length} ta o'chirildi`)
  selectedIds.value = []
  tableRef.value?.clearSelection()
  load()
}

async function deleteRow(row) {
  const ok = await confirm({
    title: "O'chirilsinmi?",
    message: `"${row.title_uz}" tadbiri o'chiriladi.`,
    confirmLabel: "O'chirish",
    danger: true
  })
  if (!ok) return
  await AdminEventsAPI.remove(row.id)
  toast.success("O'chirildi")
  load()
}

function fmtDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('uz-UZ', { day: 'numeric', month: 'short', year: 'numeric' })
}
function fmtDateTime(d) {
  if (!d) return '—'
  return new Date(d).toLocaleString('uz-UZ', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}
function isPast(d) {
  if (!d) return false
  return new Date(d).getTime() < Date.now()
}
</script>

<template>
  <div>
    <!-- Page header -->
    <div class="flex flex-wrap items-center justify-between gap-3 mb-6">
      <div>
        <h1 class="text-xl font-display font-bold text-ink-dark dark:text-white">Tadbirlar</h1>
        <p class="text-sm text-ink-faint mt-0.5">Konferensiya, master-klass va boshqa tadbirlarni boshqarish</p>
      </div>
      <button class="btn-primary btn-md" @click="router.push('/admin/events/new')">
        <Plus class="w-4 h-4" />
        Tadbir qo'shish
      </button>
    </div>

    <!-- Filter bar -->
    <div class="card p-4 mb-4 flex flex-wrap items-center gap-3">
      <div class="flex-1 min-w-[200px] max-w-md">
        <UIInput v-model="query" placeholder="Sarlavha, slug yoki joy bo'yicha qidirish...">
          <template #prefix><Search class="w-4 h-4 text-ink-faint" /></template>
        </UIInput>
      </div>
      <select
        v-model="filterStatus"
        class="h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-800 text-sm text-ink-medium dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-primary-400"
      >
        <option value="">Barcha holat</option>
        <option value="published">Chop qilingan</option>
        <option value="draft">Qoralama</option>
      </select>
      <select
        v-model="filterWhen"
        class="h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-800 text-sm text-ink-medium dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-primary-400"
      >
        <option value="">Barcha vaqt</option>
        <option value="upcoming">Yaqinlashayotgan</option>
        <option value="past">O'tgan</option>
      </select>
    </div>

    <!-- Bulk action bar -->
    <Transition
      enter-active-class="transition duration-200"
      enter-from-class="opacity-0 -translate-y-1"
      leave-active-class="transition duration-150"
      leave-to-class="opacity-0"
    >
      <div
        v-if="selectedIds.length"
        class="mb-4 flex items-center gap-3 p-3 rounded-xl bg-primary-50 dark:bg-primary-900/30 border border-primary-200 dark:border-primary-800"
      >
        <span class="text-sm font-medium text-primary-700 dark:text-primary-300">
          <strong>{{ selectedIds.length }}</strong> ta tanlangan
        </span>
        <div class="flex-1" />
        <button class="btn-danger btn-sm" @click="bulkDelete">
          <Trash2 class="w-4 h-4" /> O'chirish
        </button>
      </div>
    </Transition>

    <!-- Data table -->
    <UIDataTable
      ref="tableRef"
      :columns="columns"
      :rows="filtered"
      :loading="loading"
      selectable
      @select="(ids) => selectedIds = ids"
    >
      <template #empty>
        <div class="text-center py-12">
          <CalendarDays class="w-12 h-12 text-ink-faint mx-auto mb-3" stroke-width="1.4" />
          <h3 class="font-display font-bold text-base text-ink-dark dark:text-white mb-1">Hali tadbir yo'q</h3>
          <p class="text-sm text-ink-light mb-4">Birinchi tadbirni qo'shing</p>
          <button class="btn-primary btn-sm" @click="router.push('/admin/events/new')">
            <Plus class="w-4 h-4" /> Yaratish
          </button>
        </div>
      </template>

      <template #cell-cover="{ row }">
        <div class="w-[50px] h-9 rounded-md overflow-hidden bg-surface-soft dark:bg-slate-800 flex-shrink-0">
          <img v-if="row.cover_image" :src="row.cover_image" class="w-full h-full object-cover" :alt="row.title_uz" />
          <div v-else class="w-full h-full grid place-items-center text-ink-faint">
            <CalendarDays class="w-4 h-4" />
          </div>
        </div>
      </template>

      <template #cell-title="{ row }">
        <RouterLink :to="`/admin/events/${row.id}`" class="block group">
          <p class="font-semibold text-sm text-ink-dark dark:text-white line-clamp-1 group-hover:text-primary-600 dark:group-hover:text-primary-300">
            {{ row.title_uz }}
          </p>
          <p class="text-[11px] text-ink-faint mt-0.5 font-mono truncate max-w-[20rem]">/{{ row.slug }}</p>
        </RouterLink>
      </template>

      <template #cell-date="{ row }">
        <div class="flex flex-col">
          <span class="text-xs font-medium text-ink-medium dark:text-slate-300">{{ fmtDateTime(row.starts_at) }}</span>
          <span v-if="isPast(row.starts_at)" class="text-[10px] text-ink-faint">o'tgan</span>
          <span v-else class="text-[10px] text-emerald-600 font-semibold">yaqinlashmoqda</span>
        </div>
      </template>

      <template #cell-place="{ row }">
        <span class="inline-flex items-center gap-1 text-xs text-ink-light max-w-[14rem] truncate">
          <MapPin class="w-3.5 h-3.5 flex-shrink-0 text-ink-faint" />
          <span class="truncate">{{ row.location_uz || '—' }}</span>
        </span>
      </template>

      <template #cell-status="{ row }">
        <span
          :class="row.is_published ? 'badge-success' : 'badge bg-surface-muted text-ink-medium dark:bg-slate-700 dark:text-slate-300'"
        >
          <span :class="['w-1.5 h-1.5 rounded-full', row.is_published ? 'bg-success' : 'bg-ink-faint']" />
          {{ row.is_published ? 'Chop' : 'Qoralama' }}
        </span>
        <span v-if="row.is_featured" class="ml-1 badge-accent">★</span>
      </template>

      <template #cell-actions="{ row }">
        <div class="inline-flex items-center gap-0.5">
          <RouterLink
            :to="`/admin/events/${row.id}`"
            class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-surface-soft hover:text-primary-600"
            v-tooltip="'Tahrirlash'"
          >
            <Edit3 class="w-3.5 h-3.5" />
          </RouterLink>
          <a
            :href="`/events/${row.slug}`"
            target="_blank"
            rel="noopener"
            class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-surface-soft hover:text-primary-600"
            v-tooltip="`Ko'rish`"
          >
            <ExternalLink class="w-3.5 h-3.5" />
          </a>
          <button
            class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-danger-light hover:text-danger-dark"
            v-tooltip="`O'chirish`"
            @click="deleteRow(row)"
          >
            <Trash2 class="w-3.5 h-3.5" />
          </button>
        </div>
      </template>
    </UIDataTable>

    <!-- Pagination -->
    <div v-if="!loading && total > perPage" class="mt-4 flex items-center justify-between">
      <p class="text-xs text-ink-faint">
        Jami <strong class="text-ink-dark dark:text-white">{{ total }}</strong>, sahifa
        <strong class="text-ink-dark dark:text-white">{{ page }}</strong> / {{ totalPages }}
      </p>
      <div class="flex items-center gap-1">
        <button class="btn-ghost btn-sm" :disabled="page === 1" @click="page--">
          <ChevronLeft class="w-4 h-4" /> Oldingi
        </button>
        <button class="btn-ghost btn-sm" :disabled="page === totalPages" @click="page++">
          Keyingi <ChevronRight class="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
</template>
