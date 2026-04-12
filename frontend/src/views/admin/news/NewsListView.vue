<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  Plus, Search, Eye, Edit3, Trash2, ExternalLink, FileText,
  CheckCircle2, Circle, ChevronLeft, ChevronRight, Tag, X
} from 'lucide-vue-next'
import { AdminNewsAPI } from '@/api/admin'
import UIDataTable from '@/components/ui/UIDataTable.vue'
import UIInput from '@/components/ui/UIInput.vue'
import UIModal from '@/components/ui/UIModal.vue'
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
const filterCat = ref('')
const categories = ref([])
const selectedIds = ref([])
const tableRef = ref(null)

let debounceT
watch(query, () => {
  clearTimeout(debounceT)
  debounceT = setTimeout(load, 300)
})
watch([page, filterStatus, filterCat], load)

async function load() {
  loading.value = true
  try {
    const res = await AdminNewsAPI.list({ page: page.value, limit: perPage })
    items.value = res.items || []
    total.value = res.total || 0
  } finally {
    loading.value = false
  }
}
async function loadCats() {
  try { categories.value = await AdminNewsAPI.categories() } catch (_) {}
}
onMounted(() => { load(); loadCats() })

const filtered = computed(() => {
  let arr = items.value
  if (query.value) {
    const q = query.value.toLowerCase()
    arr = arr.filter(n => (n.title_uz || '').toLowerCase().includes(q) || (n.slug || '').toLowerCase().includes(q))
  }
  if (filterStatus.value === 'published') arr = arr.filter(n => n.is_published)
  if (filterStatus.value === 'draft')     arr = arr.filter(n => !n.is_published)
  if (filterCat.value) arr = arr.filter(n => n.category_id === Number(filterCat.value))
  return arr
})

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / perPage)))

const columns = [
  { key: 'cover',    label: '' },
  { key: 'title',    label: 'Sarlavha' },
  { key: 'status',   label: 'Holat' },
  { key: 'views',    label: "Ko'rishlar", align: 'right' },
  { key: 'date',     label: 'Sana' },
  { key: 'actions',  label: '', align: 'right' }
]

async function bulkPublish(publish) {
  const ids = [...selectedIds.value]
  await Promise.all(ids.map(id => AdminNewsAPI.publish(id, publish)))
  toast.success(`${ids.length} ta yangilik ${publish ? 'chop qilindi' : 'qoralamaga olindi'}`)
  selectedIds.value = []
  tableRef.value?.clearSelection()
  load()
}

async function bulkDelete() {
  const ok = await confirm({
    title: "O'chirishni tasdiqlang",
    message: `Tanlangan ${selectedIds.value.length} ta yangilik o'chiriladi. Bu amalni qaytarib bo'lmaydi.`,
    confirmLabel: "O'chirish",
    danger: true
  })
  if (!ok) return
  const ids = [...selectedIds.value]
  await Promise.all(ids.map(id => AdminNewsAPI.remove(id)))
  toast.success(`${ids.length} ta o'chirildi`)
  selectedIds.value = []
  tableRef.value?.clearSelection()
  load()
}

async function deleteRow(row) {
  const ok = await confirm({
    title: "O'chirilsinmi?",
    message: `"${row.title_uz}" yangiligi o'chiriladi.`,
    confirmLabel: "O'chirish",
    danger: true
  })
  if (!ok) return
  await AdminNewsAPI.remove(row.id)
  toast.success("O'chirildi")
  load()
}

function fmtDate(d) {
  if (!d) return '—'
  const diff = Date.now() - new Date(d).getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  if (days < 1)   return 'Bugun'
  if (days < 2)   return 'Kecha'
  if (days < 30)  return `${days} kun oldin`
  return new Date(d).toLocaleDateString('uz-UZ', { day: 'numeric', month: 'short', year: 'numeric' })
}

// ===== Categories CRUD =====
const catModalOpen = ref(false)
const editingCat = ref(null)
const catForm = ref({ slug: '', name_uz: '', name_ru: '', name_en: '', color: '#1A1F6E' })

function newCat() {
  editingCat.value = null
  catForm.value = { slug: '', name_uz: '', name_ru: '', name_en: '', color: '#1A1F6E' }
}
function editCat(c) {
  editingCat.value = c
  catForm.value = { slug: c.slug, name_uz: c.name_uz, name_ru: c.name_ru, name_en: c.name_en, color: c.color || '#1A1F6E' }
}
async function saveCat() {
  try {
    if (editingCat.value) {
      await AdminNewsAPI.updateCategory(editingCat.value.id, catForm.value)
      toast.success('Yangilandi')
    } else {
      await AdminNewsAPI.createCategory(catForm.value)
      toast.success('Yaratildi')
    }
    editingCat.value = null
    newCat()
    loadCats()
  } catch (e) {
    toast.error(e?.response?.data?.detail || 'Xatolik')
  }
}
async function deleteCat(c) {
  const ok = await confirm({
    title: "O'chirish",
    message: `"${c.name_uz}" kategoriyasini o'chirilsinmi?`,
    confirmLabel: "O'chirish",
    danger: true
  })
  if (!ok) return
  await AdminNewsAPI.removeCategory(c.id)
  toast.success("O'chirildi")
  loadCats()
}
</script>

<template>
  <div>
    <!-- Page header -->
    <div class="flex flex-wrap items-center justify-between gap-3 mb-6">
      <div>
        <h1 class="text-xl font-display font-bold text-ink-dark dark:text-white">Yangiliklar</h1>
        <p class="text-sm text-ink-faint mt-0.5">Universitet yangiliklarini boshqarish</p>
      </div>
      <div class="flex items-center gap-2">
        <button class="btn-ghost btn-md" @click="catModalOpen = true">
          <Tag class="w-4 h-4" />
          Kategoriyalar
        </button>
        <button class="btn-primary btn-md" @click="router.push('/admin/news/new')">
          <Plus class="w-4 h-4" />
          Yangilik qo'shish
        </button>
      </div>
    </div>

    <!-- Filter bar -->
    <div class="card p-4 mb-4 flex flex-wrap items-center gap-3">
      <div class="flex-1 min-w-[200px] max-w-md">
        <UIInput v-model="query" placeholder="Sarlavha yoki slug bo'yicha qidirish...">
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
        v-model="filterCat"
        class="h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-800 text-sm text-ink-medium dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-primary-400"
      >
        <option value="">Barcha kategoriya</option>
        <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name_uz }}</option>
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
        <button class="btn-ghost btn-sm" @click="bulkPublish(true)">
          <CheckCircle2 class="w-4 h-4" /> Chop qilish
        </button>
        <button class="btn-ghost btn-sm" @click="bulkPublish(false)">
          <Circle class="w-4 h-4" /> Qoralama
        </button>
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
          <FileText class="w-12 h-12 text-ink-faint mx-auto mb-3" stroke-width="1.4" />
          <h3 class="font-display font-bold text-base text-ink-dark dark:text-white mb-1">Hali yangilik yo'q</h3>
          <p class="text-sm text-ink-light mb-4">Birinchi yangilikni qo'shing</p>
          <button class="btn-primary btn-sm" @click="router.push('/admin/news/new')">
            <Plus class="w-4 h-4" /> Yaratish
          </button>
        </div>
      </template>

      <template #cell-cover="{ row }">
        <div class="w-[50px] h-9 rounded-md overflow-hidden bg-surface-soft dark:bg-slate-800 flex-shrink-0">
          <img v-if="row.cover_image" :src="row.cover_image" class="w-full h-full object-cover" :alt="row.title_uz" />
          <div v-else class="w-full h-full grid place-items-center text-ink-faint">
            <FileText class="w-4 h-4" />
          </div>
        </div>
      </template>

      <template #cell-title="{ row }">
        <RouterLink :to="`/admin/news/${row.id}`" class="block group">
          <p class="font-semibold text-sm text-ink-dark dark:text-white line-clamp-1 group-hover:text-primary-600 dark:group-hover:text-primary-300">
            {{ row.title_uz }}
          </p>
          <p class="text-[11px] text-ink-faint mt-0.5 font-mono truncate max-w-[20rem]">/{{ row.slug }}</p>
        </RouterLink>
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

      <template #cell-views="{ row }">
        <span class="inline-flex items-center gap-1 text-xs text-ink-medium tabular-nums">
          <Eye class="w-3.5 h-3.5 text-ink-faint" /> {{ row.views_count }}
        </span>
      </template>

      <template #cell-date="{ row }">
        <span class="text-xs text-ink-light">{{ fmtDate(row.published_at || row.created_at) }}</span>
      </template>

      <template #cell-actions="{ row }">
        <div class="inline-flex items-center gap-0.5">
          <RouterLink
            :to="`/admin/news/${row.id}`"
            class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-surface-soft hover:text-primary-600"
            v-tooltip="'Tahrirlash'"
          >
            <Edit3 class="w-3.5 h-3.5" />
          </RouterLink>
          <a
            :href="`/news/${row.slug}`"
            target="_blank"
            rel="noopener"
            class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-surface-soft hover:text-primary-600"
            v-tooltip="&quot;Ko'rish&quot;"
          >
            <ExternalLink class="w-3.5 h-3.5" />
          </a>
          <button
            class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-danger-light hover:text-danger-dark"
            v-tooltip="&quot;O'chirish&quot;"
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
        <button
          class="btn-ghost btn-sm"
          :disabled="page === 1"
          @click="page--"
        >
          <ChevronLeft class="w-4 h-4" /> Oldingi
        </button>
        <button
          class="btn-ghost btn-sm"
          :disabled="page === totalPages"
          @click="page++"
        >
          Keyingi <ChevronRight class="w-4 h-4" />
        </button>
      </div>
    </div>

    <!-- ===== Categories CRUD modal ===== -->
    <UIModal v-model="catModalOpen" size="lg" title="Kategoriyalar">
      <div class="space-y-5">
        <!-- Existing list -->
        <div class="space-y-2">
          <p class="text-[11px] uppercase tracking-wider text-ink-faint mb-2">Mavjud kategoriyalar</p>
          <div
            v-for="c in categories"
            :key="c.id"
            class="flex items-center gap-3 p-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-800"
          >
            <span
              class="w-3 h-3 rounded-full flex-shrink-0"
              :style="{ background: c.color || '#1A1F6E' }"
            />
            <div class="flex-1 min-w-0">
              <p class="text-sm font-semibold text-ink-dark dark:text-white">{{ c.name_uz }}</p>
              <p class="text-[11px] text-ink-faint">{{ c.name_ru }} · {{ c.name_en }} · /{{ c.slug }}</p>
            </div>
            <button
              class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-surface-soft hover:text-primary-600"
              @click="editCat(c)"
              v-tooltip="'Tahrirlash'"
            ><Edit3 class="w-3.5 h-3.5" /></button>
            <button
              class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-danger-light hover:text-danger-dark"
              @click="deleteCat(c)"
              v-tooltip="`O'chirish`"
            ><Trash2 class="w-3.5 h-3.5" /></button>
          </div>
          <p v-if="!categories.length" class="text-center text-sm text-ink-faint py-4">Hozircha kategoriya yo'q</p>
        </div>

        <!-- Form -->
        <div class="border-t border-surface-muted dark:border-slate-700 pt-5">
          <p class="text-[11px] uppercase tracking-wider text-ink-faint mb-3">
            {{ editingCat ? 'Tahrirlash' : 'Yangi kategoriya' }}
          </p>
          <div class="grid sm:grid-cols-2 gap-3">
            <UIInput v-model="catForm.slug" label="Slug (URL)" placeholder="yangiliklar" />
            <div>
              <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Rang</label>
              <input
                v-model="catForm.color"
                type="color"
                class="w-full h-10 rounded-lg border border-surface-muted dark:border-slate-700 cursor-pointer"
              />
            </div>
            <UIInput v-model="catForm.name_uz" label="Nomi (UZ)" placeholder="Yangiliklar" />
            <UIInput v-model="catForm.name_ru" label="Nomi (RU)" placeholder="Новости" />
            <UIInput v-model="catForm.name_en" label="Nomi (EN)" placeholder="News" />
          </div>
        </div>
      </div>
      <template #footer>
        <button v-if="editingCat" class="btn-ghost btn-sm" @click="newCat">Yangi qo'shish</button>
        <button class="btn-ghost btn-sm" @click="catModalOpen = false">Yopish</button>
        <button class="btn-primary btn-sm" @click="saveCat">Saqlash</button>
      </template>
    </UIModal>
  </div>
</template>
