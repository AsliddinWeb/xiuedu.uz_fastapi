<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  Image as ImageIcon, FileText, Trash2, Copy, Grid3x3, List as ListIcon,
  Download, Inbox, X
} from 'lucide-vue-next'
import { AdminMediaAPI } from '@/api/admin'
import UIFileUpload from '@/components/ui/UIFileUpload.vue'
import UIModal from '@/components/ui/UIModal.vue'
import UIPagination from '@/components/ui/UIPagination.vue'
import { useToast } from '@/composables/useToast'
import { useConfirm } from '@/composables/useConfirm'

const toast = useToast()
const confirm = useConfirm()

const items = ref([])
const total = ref(0)
const loading = ref(true)
const filter = ref('')
const sort = ref('newest')
const view = ref('grid')   // 'grid' | 'list'
const page = ref(1)
const perPage = 24

const selected = ref(new Set())
const detail = ref(null)

async function load() {
  loading.value = true
  try {
    const params = { page: page.value, limit: perPage }
    if (filter.value) params.type = filter.value
    const res = await AdminMediaAPI.list(params)
    let arr = res.items || []
    if (sort.value === 'oldest') arr = [...arr].reverse()
    if (sort.value === 'largest') arr = [...arr].sort((a, b) => b.size_bytes - a.size_bytes)
    items.value = arr
    total.value = res.total || 0
  } finally {
    loading.value = false
  }
}
onMounted(load)

async function uploadOne(file, onProgress) {
  onProgress(0.5)
  const r = await AdminMediaAPI.upload(file)
  onProgress(1)
  return r
}

function onUploaded() {
  toast.success('Yuklandi')
  load()
}

async function copy(url) {
  const full = window.location.origin + url
  await navigator.clipboard.writeText(full)
  toast.success('URL nusxalandi')
}

async function deleteItem(m) {
  const ok = await confirm({
    title: "O'chirish",
    message: `"${m.original_name}" o'chiriladi.`,
    confirmLabel: "O'chirish",
    danger: true
  })
  if (!ok) return
  await AdminMediaAPI.remove(m.id)
  toast.success("O'chirildi")
  detail.value = null
  load()
}

function toggleSelect(m, e) {
  if (e?.shiftKey || e?.ctrlKey || e?.metaKey) {
    const s = new Set(selected.value)
    s.has(m.id) ? s.delete(m.id) : s.add(m.id)
    selected.value = s
  } else {
    detail.value = m
  }
}

const isImage = (m) => /^image\//i.test(m.mime_type)

function fmtSize(b) {
  if (!b) return '0 B'
  const u = ['B','KB','MB','GB']; let i=0, v=b
  while (v >= 1024 && i < u.length-1) { v /= 1024; i++ }
  return v.toFixed(1) + ' ' + u[i]
}

function fmtDate(d) {
  return d ? new Date(d).toLocaleDateString('uz-UZ', { day: 'numeric', month: 'short', year: 'numeric' }) : ''
}
</script>

<template>
  <div>
    <!-- Page header -->
    <div class="flex flex-wrap items-center justify-between gap-3 mb-6">
      <div>
        <h1 class="text-xl font-display font-bold text-ink-dark dark:text-white">Media</h1>
        <p class="text-sm text-ink-faint mt-0.5">{{ total }} ta fayl</p>
      </div>
    </div>

    <!-- Upload zone (compact when has files) -->
    <div class="mb-6">
      <UIFileUpload :upload="uploadOne" multiple accept="*/*" @uploaded="onUploaded" />
    </div>

    <!-- Toolbar: filter + view + sort -->
    <div class="flex flex-wrap items-center gap-3 mb-4">
      <div class="flex items-center gap-1">
        <button
          v-for="opt in [
            { key: '',         label: 'Barchasi' },
            { key: 'image',    label: 'Rasmlar' },
            { key: 'document', label: 'Hujjatlar' }
          ]"
          :key="opt.key"
          :class="['px-3 py-1.5 text-xs rounded-lg font-medium transition',
                   filter === opt.key
                     ? 'bg-primary-600 text-white'
                     : 'text-ink-medium dark:text-slate-300 hover:bg-surface-soft dark:hover:bg-slate-800']"
          @click="filter = opt.key; load()"
        >{{ opt.label }}</button>
      </div>

      <div class="flex-1" />

      <select
        v-model="sort"
        @change="load"
        class="h-9 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-800 text-xs text-ink-medium dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-primary-400"
      >
        <option value="newest">Eng yangi</option>
        <option value="oldest">Eng eski</option>
        <option value="largest">Hajmi katta</option>
      </select>

      <div class="flex items-center gap-0.5 p-0.5 rounded-lg border border-surface-muted dark:border-slate-700">
        <button
          :class="['w-7 h-7 grid place-items-center rounded transition',
                   view === 'grid' ? 'bg-primary-600 text-white' : 'text-ink-faint hover:text-ink-dark']"
          @click="view = 'grid'"
          v-tooltip="'Grid'"
        ><Grid3x3 class="w-3.5 h-3.5" /></button>
        <button
          :class="['w-7 h-7 grid place-items-center rounded transition',
                   view === 'list' ? 'bg-primary-600 text-white' : 'text-ink-faint hover:text-ink-dark']"
          @click="view = 'list'"
          v-tooltip="&quot;Ro'yxat&quot;"
        ><ListIcon class="w-3.5 h-3.5" /></button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="card p-12 text-center text-sm text-ink-faint">Yuklanmoqda...</div>

    <!-- Empty -->
    <div v-else-if="!items.length" class="card p-16 text-center">
      <Inbox class="w-12 h-12 text-ink-faint mx-auto mb-3" stroke-width="1.4" />
      <h3 class="font-display font-bold text-base text-ink-dark dark:text-white mb-1">Hozircha fayllar yo'q</h3>
      <p class="text-sm text-ink-light">Tepadagi yuklash zonasidan foydalaning</p>
    </div>

    <!-- Grid view -->
    <div
      v-else-if="view === 'grid'"
      class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3"
    >
      <div
        v-for="m in items"
        :key="m.id"
        :class="[
          'group relative rounded-xl overflow-hidden border bg-white dark:bg-slate-800 cursor-pointer transition',
          selected.has(m.id)
            ? 'border-primary-500 ring-2 ring-primary-500/30'
            : 'border-surface-muted dark:border-slate-700 hover:border-primary-400'
        ]"
        @click="toggleSelect(m, $event)"
      >
        <div class="aspect-square bg-surface-soft dark:bg-slate-900 grid place-items-center overflow-hidden">
          <img v-if="isImage(m)" :src="m.url" :alt="m.original_name" class="w-full h-full object-cover" loading="lazy" />
          <FileText v-else class="w-10 h-10 text-ink-faint" />
        </div>
        <div class="p-2">
          <p class="text-xs font-medium text-ink-dark dark:text-white truncate" :title="m.original_name">{{ m.original_name }}</p>
          <p class="text-[10px] text-ink-faint">{{ fmtSize(m.size_bytes) }}</p>
        </div>
        <!-- Overlay -->
        <div class="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition flex items-center justify-center gap-1.5 opacity-0 group-hover:opacity-100">
          <button
            class="w-8 h-8 rounded-lg bg-white text-primary-600 hover:bg-primary-50 grid place-items-center"
            v-tooltip="'URL nusxalash'"
            @click.stop="copy(m.url)"
          ><Copy class="w-4 h-4" /></button>
          <button
            class="w-8 h-8 rounded-lg bg-white text-danger hover:bg-danger-light grid place-items-center"
            v-tooltip="&quot;O'chirish&quot;"
            @click.stop="deleteItem(m)"
          ><Trash2 class="w-4 h-4" /></button>
        </div>
        <span
          v-if="selected.has(m.id)"
          class="absolute top-2 right-2 w-5 h-5 rounded-full bg-primary-600 text-white grid place-items-center text-xs font-bold"
        >✓</span>
      </div>
    </div>

    <!-- List view -->
    <div v-else class="card overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-surface-soft dark:bg-slate-900/50 text-ink-light dark:text-slate-400 text-[11px] uppercase tracking-wider">
          <tr>
            <th class="text-left px-4 py-3 font-semibold">Fayl</th>
            <th class="text-left px-4 py-3 font-semibold hidden md:table-cell">Tur</th>
            <th class="text-right px-4 py-3 font-semibold">Hajmi</th>
            <th class="text-left px-4 py-3 font-semibold hidden md:table-cell">Sana</th>
            <th class="px-4 py-3"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="m in items" :key="m.id" class="border-t border-surface-muted dark:border-slate-800 hover:bg-surface-soft/50 dark:hover:bg-slate-800/30">
            <td class="px-4 py-3">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded bg-surface-soft dark:bg-slate-900 overflow-hidden grid place-items-center flex-shrink-0">
                  <img v-if="isImage(m)" :src="m.url" :alt="m.original_name" class="w-full h-full object-cover" />
                  <FileText v-else class="w-4 h-4 text-ink-faint" />
                </div>
                <button class="text-left min-w-0" @click="detail = m">
                  <p class="text-sm font-medium text-ink-dark dark:text-white truncate hover:text-primary-600">{{ m.original_name }}</p>
                  <p class="text-[11px] text-ink-faint font-mono truncate">{{ m.url }}</p>
                </button>
              </div>
            </td>
            <td class="px-4 py-3 text-xs text-ink-light hidden md:table-cell">{{ m.mime_type }}</td>
            <td class="px-4 py-3 text-xs text-ink-light text-right tabular-nums">{{ fmtSize(m.size_bytes) }}</td>
            <td class="px-4 py-3 text-xs text-ink-light hidden md:table-cell">{{ fmtDate(m.created_at) }}</td>
            <td class="px-4 py-3 text-right">
              <div class="inline-flex items-center gap-0.5">
                <button class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-surface-soft hover:text-primary-600" @click="copy(m.url)" v-tooltip="'Copy URL'">
                  <Copy class="w-3.5 h-3.5" />
                </button>
                <button class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-danger-light hover:text-danger-dark" @click="deleteItem(m)" v-tooltip="&quot;O'chirish&quot;">
                  <Trash2 class="w-3.5 h-3.5" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div v-if="!loading && total > perPage" class="mt-4 flex justify-end">
      <UIPagination v-model="page" :total="total" :per-page="perPage" @update:model-value="load" />
    </div>

    <!-- Detail modal -->
    <UIModal :model-value="!!detail" @update:model-value="detail = null" size="lg" :title="detail?.original_name">
      <div v-if="detail" class="grid md:grid-cols-[1fr,16rem] gap-5">
        <div class="rounded-xl overflow-hidden bg-surface-soft dark:bg-slate-900 grid place-items-center min-h-[20rem]">
          <img v-if="isImage(detail)" :src="detail.url" :alt="detail.original_name" class="max-w-full max-h-[60vh] object-contain" />
          <div v-else class="text-center p-10">
            <FileText class="w-16 h-16 text-ink-faint mx-auto mb-2" stroke-width="1.4" />
            <p class="text-sm text-ink-light">{{ detail.mime_type }}</p>
          </div>
        </div>
        <div class="space-y-3 text-sm">
          <div>
            <p class="text-[10px] uppercase tracking-wider text-ink-faint mb-1">Fayl nomi</p>
            <p class="text-ink-dark dark:text-white truncate">{{ detail.original_name }}</p>
          </div>
          <div>
            <p class="text-[10px] uppercase tracking-wider text-ink-faint mb-1">URL</p>
            <p class="text-ink-dark dark:text-white text-xs font-mono break-all">{{ detail.url }}</p>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <p class="text-[10px] uppercase tracking-wider text-ink-faint mb-1">Hajmi</p>
              <p class="text-ink-dark dark:text-white">{{ fmtSize(detail.size_bytes) }}</p>
            </div>
            <div>
              <p class="text-[10px] uppercase tracking-wider text-ink-faint mb-1">Sana</p>
              <p class="text-ink-dark dark:text-white text-xs">{{ fmtDate(detail.created_at) }}</p>
            </div>
          </div>
          <div v-if="detail.width" class="grid grid-cols-2 gap-3">
            <div>
              <p class="text-[10px] uppercase tracking-wider text-ink-faint mb-1">Kenglik</p>
              <p class="text-ink-dark dark:text-white">{{ detail.width }}px</p>
            </div>
            <div>
              <p class="text-[10px] uppercase tracking-wider text-ink-faint mb-1">Balandlik</p>
              <p class="text-ink-dark dark:text-white">{{ detail.height }}px</p>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <button class="btn-ghost btn-sm" @click="copy(detail.url)">
          <Copy class="w-3.5 h-3.5" /> URL nusxalash
        </button>
        <a :href="detail.url" download class="btn-ghost btn-sm">
          <Download class="w-3.5 h-3.5" /> Yuklab olish
        </a>
        <button class="btn-danger btn-sm" @click="deleteItem(detail)">
          <Trash2 class="w-3.5 h-3.5" /> O'chirish
        </button>
      </template>
    </UIModal>
  </div>
</template>
