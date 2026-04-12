<script setup>
import { ref, reactive, computed, onMounted, watch, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Save, ExternalLink, Trash2, ArrowLeft, Plus, Image as ImageIcon } from 'lucide-vue-next'
import { AdminNewsAPI, AdminMediaAPI } from '@/api/admin'
import UIInput from '@/components/ui/UIInput.vue'
import UIButton from '@/components/ui/UIButton.vue'
import UITabs from '@/components/ui/UITabs.vue'
import RichEditor from '@/components/ui/RichEditor.vue'
import { useToast } from '@/composables/useToast'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const isNew = computed(() => route.params.id === 'new' || !route.params.id)
const draftKey = computed(() => `xiuedu_news_draft_${route.params.id || 'new'}`)

const form = reactive({
  slug: '',
  title_uz: '', title_ru: '', title_en: '',
  excerpt_uz: '', excerpt_ru: '', excerpt_en: '',
  body_uz: '', body_ru: '', body_en: '',
  cover_image: null,
  gallery: [],
  category_id: null,
  is_published: false,
  is_featured: false,
  published_at: null
})

const categories = ref([])
const lang = ref('uz')
const saving = ref(false)
const uploading = ref(false)
const uploadingGallery = ref(false)

const tabs = [
  { key: 'uz', label: "O'zbek" },
  { key: 'ru', label: 'Rus' },
  { key: 'en', label: 'Ingliz' }
]

function slugify(s) {
  // Cyrillic → Latin transliteration for slugs
  const map = {
    а:'a', б:'b', в:'v', г:'g', д:'d', е:'e', ё:'yo', ж:'j', з:'z',
    и:'i', й:'y', к:'k', л:'l', м:'m', н:'n', о:'o', п:'p', р:'r',
    с:'s', т:'t', у:'u', ф:'f', х:'x', ц:'ts', ч:'ch', ш:'sh', щ:'sh',
    ъ:'', ы:'y', ь:'', э:'e', ю:'yu', я:'ya'
  }
  return (s || '').toLowerCase()
    .split('').map(ch => map[ch] ?? ch).join('')
    .replace(/[ʻ'`]/g, '')
    .replace(/[^a-z0-9\s-]/g, ' ')
    .trim()
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .slice(0, 80)
}

// Auto-generate slug from title_uz on every change for new items;
// for existing items, only fill if empty (so the URL stays stable).
watch(() => form.title_uz, (v) => {
  if (isNew.value) form.slug = slugify(v)
  else if (!form.slug) form.slug = slugify(v)
})

async function loadAll() {
  try { categories.value = await AdminNewsAPI.categories() } catch (_) {}
  if (isNew.value) {
    const draft = localStorage.getItem(draftKey.value)
    if (draft) Object.assign(form, JSON.parse(draft))
    return
  }
  try {
    const list = await AdminNewsAPI.list({ limit: 200 })
    const found = (list.items || []).find(n => n.id === Number(route.params.id))
    if (found) {
      Object.assign(form, found)
      form.gallery = Array.isArray(found.gallery) ? [...found.gallery] : []
    }
  } catch (_) {}
}

async function onUploadGallery(e) {
  const files = Array.from(e.target.files || [])
  if (!files.length) return
  uploadingGallery.value = true
  try {
    for (const f of files) {
      const res = await AdminMediaAPI.upload(f)
      form.gallery.push(res.url)
    }
    toast.success(`${files.length} ta rasm qo'shildi`)
  } catch (_) {
    toast.error('Yuklashda xatolik')
  } finally {
    uploadingGallery.value = false
    e.target.value = ''
  }
}
function removeFromGallery(idx) {
  form.gallery.splice(idx, 1)
}
function moveGallery(idx, dir) {
  const next = idx + dir
  if (next < 0 || next >= form.gallery.length) return
  const tmp = form.gallery[idx]
  form.gallery[idx] = form.gallery[next]
  form.gallery[next] = tmp
}

onMounted(loadAll)

// Auto-save draft to localStorage every 30s
const autoSaveTimer = setInterval(() => {
  localStorage.setItem(draftKey.value, JSON.stringify(form))
}, 30000)
onBeforeUnmount(() => clearInterval(autoSaveTimer))

async function onUpload(e) {
  const file = e.target.files[0]
  if (!file) return
  uploading.value = true
  try {
    const res = await AdminMediaAPI.upload(file)
    form.cover_image = res.url
    toast.success('Cover yuklandi')
  } catch (_) {} finally {
    uploading.value = false
    e.target.value = ''
  }
}

async function save() {
  saving.value = true
  try {
    const payload = {
      ...form,
      category_id: form.category_id ? Number(form.category_id) : null,
      gallery: [...form.gallery]
    }
    if (isNew.value) {
      const created = await AdminNewsAPI.create(payload)
      toast.success('Yaratildi')
      localStorage.removeItem(draftKey.value)
      router.replace(`/admin/news/${created.id}`)
    } else {
      await AdminNewsAPI.update(route.params.id, payload)
      toast.success('Saqlandi')
    }
  } catch (e) {
    toast.error(e?.response?.data?.detail || "Saqlashda xatolik")
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="space-y-5">
    <div class="flex items-center gap-3">
      <UIButton variant="ghost" size="sm" @click="router.push('/admin/news')">
        <template #icon-left><ArrowLeft class="w-4 h-4" /></template>
        Orqaga
      </UIButton>
      <h2 class="font-display text-xl font-bold text-primary-700 dark:text-white flex-1">
        {{ isNew ? "Yangi yangilik" : "Tahrirlash" }}
      </h2>
      <a v-if="!isNew && form.slug" :href="`/news/${form.slug}`" target="_blank" class="text-xs text-accent-500 inline-flex items-center gap-1 hover:underline">
        Preview <ExternalLink class="w-3 h-3" />
      </a>
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>
        Saqlash
      </UIButton>
    </div>

    <div class="grid lg:grid-cols-[1fr,20rem] gap-5">
      <!-- Main column -->
      <div class="space-y-4">
        <UITabs v-model="lang" :tabs="tabs">
          <template #default="{ active }">
            <div class="space-y-4">
              <UIInput :model-value="form[`title_${active}`]" @update:model-value="form[`title_${active}`] = $event" label="Sarlavha" required />
              <UIInput :model-value="form[`excerpt_${active}`]" @update:model-value="form[`excerpt_${active}`] = $event" textarea :rows="3" label="Qisqa tavsif" />
              <div>
                <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Asosiy matn</label>
                <RichEditor :model-value="form[`body_${active}`]" @update:model-value="form[`body_${active}`] = $event" placeholder="Matn..." />
              </div>
            </div>
          </template>
        </UITabs>

        <!-- Gallery section -->
        <div class="rounded-2xl p-5 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700">
          <div class="flex items-center justify-between mb-4">
            <div>
              <p class="text-sm font-bold text-ink-dark dark:text-white">Qo'shimcha rasmlar (galereya)</p>
              <p class="text-[11px] text-ink-faint mt-0.5">{{ form.gallery.length }} ta rasm — yangilik ichida ko'rsatiladi</p>
            </div>
            <label class="btn-ghost btn-sm cursor-pointer">
              <input type="file" accept="image/*" multiple class="hidden" @change="onUploadGallery" />
              <Plus class="w-4 h-4" /> {{ uploadingGallery ? 'Yuklanmoqda...' : "Rasm qo'shish" }}
            </label>
          </div>

          <div v-if="form.gallery.length" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
            <div
              v-for="(img, i) in form.gallery"
              :key="i"
              class="group relative aspect-square rounded-lg overflow-hidden bg-surface-soft dark:bg-slate-900 border border-surface-muted dark:border-slate-700"
            >
              <img :src="img" alt="" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-colors" />
              <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  type="button"
                  class="w-7 h-7 grid place-items-center rounded-md bg-white/90 hover:bg-white text-danger"
                  @click="removeFromGallery(i)"
                  v-tooltip="`O'chirish`"
                >
                  <Trash2 class="w-3.5 h-3.5" />
                </button>
              </div>
              <div class="absolute bottom-2 left-2 opacity-0 group-hover:opacity-100 transition-opacity flex gap-1">
                <button
                  type="button"
                  class="px-1.5 h-6 rounded bg-white/90 hover:bg-white text-[11px] font-bold text-primary-800 disabled:opacity-40"
                  :disabled="i === 0"
                  @click="moveGallery(i, -1)"
                >←</button>
                <button
                  type="button"
                  class="px-1.5 h-6 rounded bg-white/90 hover:bg-white text-[11px] font-bold text-primary-800 disabled:opacity-40"
                  :disabled="i === form.gallery.length - 1"
                  @click="moveGallery(i, 1)"
                >→</button>
              </div>
              <div class="absolute bottom-1 right-2 text-[10px] font-bold text-white drop-shadow">{{ i + 1 }}</div>
            </div>
          </div>

          <div
            v-else
            class="rounded-xl border-2 border-dashed border-surface-muted dark:border-slate-700 p-8 text-center"
          >
            <ImageIcon class="w-8 h-8 mx-auto text-ink-faint mb-2" />
            <p class="text-xs text-ink-faint">Asosiy rasmdan tashqari qo'shimcha rasmlar qo'shing</p>
          </div>
        </div>

        <!-- Auto-generated slug (read-only) -->
        <div class="rounded-xl bg-surface-soft dark:bg-slate-900/40 border border-surface-muted dark:border-slate-700 p-4">
          <div class="flex items-center justify-between mb-1.5">
            <label class="text-[11px] font-semibold uppercase tracking-wider text-ink-faint">URL (slug)</label>
            <span class="text-[10px] text-ink-faint">avtomatik</span>
          </div>
          <input
            type="text"
            :value="form.slug"
            readonly
            class="w-full px-3 py-2 rounded-lg bg-white dark:bg-slate-900 border border-surface-muted dark:border-slate-700 text-sm font-mono text-ink-medium dark:text-slate-300 cursor-default focus:outline-none"
          />
          <p class="text-[11px] text-ink-faint mt-1.5">
            Sarlavha (UZ) ga qarab avtomatik yaratiladi: <code class="text-primary-700 dark:text-accent-400">/news/{{ form.slug || '...' }}</code>
          </p>
        </div>
      </div>

      <!-- Sidebar -->
      <aside class="space-y-4">
        <div class="rounded-2xl p-5 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 space-y-3">
          <p class="text-xs font-semibold uppercase tracking-wider text-ink-faint">Asosiy rasm</p>
          <div v-if="form.cover_image" class="aspect-video rounded-lg overflow-hidden bg-surface-soft dark:bg-slate-900">
            <img :src="form.cover_image" alt="" class="w-full h-full object-cover" />
          </div>
          <label class="block">
            <input type="file" accept="image/*" class="hidden" @change="onUpload" />
            <span class="block text-center px-4 py-2 rounded-lg border-2 border-dashed border-surface-muted dark:border-slate-700 text-xs text-ink-faint hover:border-accent-500 cursor-pointer">
              {{ uploading ? 'Yuklanmoqda...' : (form.cover_image ? 'Boshqa rasm tanlash' : 'Rasm tanlash') }}
            </span>
          </label>
          <button v-if="form.cover_image" type="button" class="text-xs text-danger inline-flex items-center gap-1" @click="form.cover_image = null">
            <Trash2 class="w-3 h-3" /> Olib tashlash
          </button>
        </div>

        <div class="rounded-2xl p-5 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 space-y-3">
          <p class="text-xs font-semibold uppercase tracking-wider text-ink-faint">Sozlamalar</p>
          <label class="block">
            <span class="text-sm font-medium text-ink-medium dark:text-slate-300">Kategoriya</span>
            <select v-model="form.category_id" class="mt-1 w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-800 text-sm">
              <option :value="null">— Tanlanmagan —</option>
              <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name_uz }}</option>
            </select>
          </label>
          <label class="flex items-center justify-between gap-2 cursor-pointer">
            <span class="text-sm">Chop qilingan</span>
            <input type="checkbox" v-model="form.is_published" class="w-4 h-4 accent-accent-500" />
          </label>
          <label class="flex items-center justify-between gap-2 cursor-pointer">
            <span class="text-sm">Featured</span>
            <input type="checkbox" v-model="form.is_featured" class="w-4 h-4 accent-accent-500" />
          </label>
        </div>
      </aside>
    </div>
  </div>
</template>
