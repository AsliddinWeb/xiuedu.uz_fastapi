<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  Plus, FileText, FolderOpen, ChevronRight, ChevronDown, Edit3,
  ExternalLink, Trash2, Inbox
} from 'lucide-vue-next'
import { AdminPagesAPI } from '@/api/admin'
import { useToast } from '@/composables/useToast'
import { useConfirm } from '@/composables/useConfirm'

const router = useRouter()
const toast = useToast()
const confirm = useConfirm()

const items = ref([])
const loading = ref(true)
const expanded = ref(new Set())

async function load() {
  loading.value = true
  try {
    items.value = await AdminPagesAPI.list()
    // expand all roots by default
    items.value.forEach(p => {
      if (!p.parent_id) expanded.value.add(p.id)
    })
  } finally { loading.value = false }
}
onMounted(load)

const tree = computed(() => {
  const map = new Map()
  for (const p of items.value) map.set(p.id, { ...p, children: [] })
  const roots = []
  for (const p of map.values()) {
    if (p.parent_id && map.has(p.parent_id)) map.get(p.parent_id).children.push(p)
    else roots.push(p)
  }
  const sortRec = (arr) => {
    arr.sort((a, b) => (a.page_order - b.page_order) || a.id - b.id)
    arr.forEach(n => sortRec(n.children))
  }
  sortRec(roots)
  return roots
})

function toggle(id) {
  if (expanded.value.has(id)) expanded.value.delete(id)
  else expanded.value.add(id)
}

async function deletePage(p) {
  const ok = await confirm({
    title: "O'chirish",
    message: `"${p.title_uz}" sahifasini o'chirishni tasdiqlaysizmi?`,
    confirmLabel: "O'chirish",
    danger: true
  })
  if (!ok) return
  await AdminPagesAPI.remove(p.id)
  toast.success("O'chirildi")
  load()
}

function fmtDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('uz-UZ', { day: 'numeric', month: 'short' })
}

// Flatten tree for rendering with depth
const flat = computed(() => {
  const out = []
  const walk = (node, depth = 0) => {
    out.push({ ...node, depth })
    if (expanded.value.has(node.id)) {
      node.children.forEach(c => walk(c, depth + 1))
    }
  }
  tree.value.forEach(r => walk(r))
  return out
})
</script>

<template>
  <div>
    <!-- Page header -->
    <div class="flex flex-wrap items-center justify-between gap-3 mb-6">
      <div>
        <h1 class="text-xl font-display font-bold text-ink-dark dark:text-white">Sahifalar</h1>
        <p class="text-sm text-ink-faint mt-0.5">{{ items.length }} ta sahifa, ierarxik tuzilma</p>
      </div>
      <button class="btn-primary btn-md" @click="router.push('/admin/pages/new')">
        <Plus class="w-4 h-4" />
        Sahifa qo'shish
      </button>
    </div>

    <div v-if="loading" class="card p-8 text-center text-sm text-ink-faint">Yuklanmoqda...</div>

    <div v-else-if="!items.length" class="card p-12 text-center">
      <Inbox class="w-12 h-12 text-ink-faint mx-auto mb-3" stroke-width="1.4" />
      <h3 class="font-display font-bold text-base text-ink-dark dark:text-white mb-1">Sahifalar mavjud emas</h3>
      <p class="text-sm text-ink-light mb-4">Birinchi sahifani yaratish uchun tugmani bosing</p>
      <button class="btn-primary btn-sm" @click="router.push('/admin/pages/new')">
        <Plus class="w-4 h-4" /> Yaratish
      </button>
    </div>

    <!-- Tree table -->
    <div v-else class="card overflow-hidden">
      <div class="grid grid-cols-[1fr,auto,auto,auto] gap-4 px-5 py-3 text-[11px] font-semibold text-ink-faint uppercase tracking-wider border-b border-surface-muted dark:border-slate-700">
        <div>Sarlavha</div>
        <div class="hidden md:block">Holat</div>
        <div class="hidden md:block">Yangilangan</div>
        <div></div>
      </div>

      <div class="divide-y divide-surface-muted dark:divide-slate-800">
        <div
          v-for="row in flat"
          :key="row.id"
          class="grid grid-cols-[1fr,auto,auto,auto] gap-4 px-5 py-3 hover:bg-surface-soft/50 dark:hover:bg-slate-800/30 transition group"
        >
          <!-- Title with indent and toggle -->
          <div class="flex items-center gap-1 min-w-0" :style="{ paddingLeft: `${row.depth * 20}px` }">
            <button
              v-if="row.children?.length"
              class="w-5 h-5 grid place-items-center text-ink-faint hover:text-ink-dark"
              @click="toggle(row.id)"
              :aria-label="expanded.has(row.id) ? 'Collapse' : 'Expand'"
            >
              <ChevronDown v-if="expanded.has(row.id)" class="w-3.5 h-3.5" />
              <ChevronRight v-else class="w-3.5 h-3.5" />
            </button>
            <span v-else class="w-5" />

            <component
              :is="row.children?.length ? FolderOpen : FileText"
              class="w-4 h-4 text-primary-500 flex-shrink-0"
            />

            <RouterLink :to="`/admin/pages/${row.id}`" class="block min-w-0 group/link">
              <p class="font-semibold text-sm text-ink-dark dark:text-white truncate group-hover/link:text-primary-600 dark:group-hover/link:text-primary-300">
                {{ row.title_uz }}
              </p>
              <p class="text-[11px] text-ink-faint font-mono truncate">/p/{{ row.slug }}</p>
            </RouterLink>
          </div>

          <div class="hidden md:flex items-center">
            <span
              :class="row.is_published ? 'badge-success' : 'badge bg-surface-muted text-ink-medium dark:bg-slate-700 dark:text-slate-300'"
            >
              <span :class="['w-1.5 h-1.5 rounded-full', row.is_published ? 'bg-success' : 'bg-ink-faint']" />
              {{ row.is_published ? 'Chop' : 'Qoralama' }}
            </span>
          </div>

          <div class="hidden md:flex items-center text-xs text-ink-light">{{ fmtDate(row.updated_at) }}</div>

          <div class="flex items-center gap-0.5">
            <RouterLink
              :to="`/admin/pages/${row.id}`"
              class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-surface-soft hover:text-primary-600"
              v-tooltip="'Tahrirlash'"
            ><Edit3 class="w-3.5 h-3.5" /></RouterLink>
            <a
              :href="`/p/${row.slug}`"
              target="_blank"
              rel="noopener"
              class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-surface-soft hover:text-primary-600"
              v-tooltip="&quot;Ko'rish&quot;"
            ><ExternalLink class="w-3.5 h-3.5" /></a>
            <button
              class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-danger-light hover:text-danger-dark"
              v-tooltip="&quot;O'chirish&quot;"
              @click="deletePage(row)"
            ><Trash2 class="w-3.5 h-3.5" /></button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
