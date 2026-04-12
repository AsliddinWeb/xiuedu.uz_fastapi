<script setup>
import { ref, reactive, computed, onMounted, watch, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  Save, ExternalLink, Trash2, ArrowLeft, Plus, Image as ImageIcon,
  GripVertical, Calendar, MapPin
} from 'lucide-vue-next'
import { AdminEventsAPI, AdminMediaAPI } from '@/api/admin'
import UIInput from '@/components/ui/UIInput.vue'
import UIButton from '@/components/ui/UIButton.vue'
import UITabs from '@/components/ui/UITabs.vue'
import RichEditor from '@/components/ui/RichEditor.vue'
import { useToast } from '@/composables/useToast'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const isNew = computed(() => route.params.id === 'new' || !route.params.id)

const form = reactive({
  slug: '',
  title_uz: '', title_ru: '', title_en: '',
  description_uz: '', description_ru: '', description_en: '',
  location_uz: '', location_ru: '', location_en: '',
  starts_at: '',
  ends_at: '',
  cover_image: null,
  gallery: [],
  is_published: false,
  is_featured: false
})

const lang = ref('uz')
const saving = ref(false)
const uploadingCover = ref(false)
const uploadingGallery = ref(false)

const tabs = [
  { key: 'uz', label: "O'zbek" },
  { key: 'ru', label: 'Rus' },
  { key: 'en', label: 'Ingliz' }
]

function slugify(s) {
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

watch(() => form.title_uz, (v) => {
  if (isNew.value) form.slug = slugify(v)
  else if (!form.slug) form.slug = slugify(v)
})

// Convert ISO datetime → "YYYY-MM-DDTHH:mm" for datetime-local input
function toLocalInput(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  if (isNaN(d.getTime())) return ''
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
}
function toIso(localStr) {
  if (!localStr) return null
  return new Date(localStr).toISOString()
}

async function loadAll() {
  if (isNew.value) return
  try {
    const ev = await AdminEventsAPI.get(route.params.id)
    if (ev) {
      Object.assign(form, ev)
      form.starts_at = toLocalInput(ev.starts_at)
      form.ends_at = toLocalInput(ev.ends_at)
      form.gallery = Array.isArray(ev.gallery) ? [...ev.gallery] : []
    }
  } catch (e) {
    toast.error("Yuklashda xatolik")
  }
}

onMounted(loadAll)

async function onUploadCover(e) {
  const file = e.target.files[0]
  if (!file) return
  uploadingCover.value = true
  try {
    const res = await AdminMediaAPI.upload(file)
    form.cover_image = res.url
    toast.success('Cover yuklandi')
  } catch (_) {
    toast.error('Yuklashda xatolik')
  } finally {
    uploadingCover.value = false
    e.target.value = ''
  }
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

async function save() {
  if (!form.title_uz || !form.starts_at) {
    toast.error("Sarlavha (UZ) va boshlanish vaqtini kiriting")
    return
  }
  saving.value = true
  try {
    const payload = {
      ...form,
      starts_at: toIso(form.starts_at),
      ends_at: toIso(form.ends_at),
      gallery: [...form.gallery]
    }
    if (isNew.value) {
      const created = await AdminEventsAPI.create(payload)
      toast.success('Yaratildi')
      router.replace(`/admin/events/${created.id}`)
    } else {
      await AdminEventsAPI.update(route.params.id, payload)
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
    <!-- Header bar -->
    <div class="flex items-center gap-3">
      <UIButton variant="ghost" size="sm" @click="router.push('/admin/events')">
        <template #icon-left><ArrowLeft class="w-4 h-4" /></template>
        Orqaga
      </UIButton>
      <h2 class="font-display text-xl font-bold text-primary-700 dark:text-white flex-1">
        {{ isNew ? "Yangi tadbir" : "Tadbirni tahrirlash" }}
      </h2>
      <a v-if="!isNew && form.slug" :href="`/events/${form.slug}`" target="_blank" class="text-xs text-accent-500 inline-flex items-center gap-1 hover:underline">
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
              <UIInput
                :model-value="form[`title_${active}`]"
                @update:model-value="form[`title_${active}`] = $event"
                label="Sarlavha"
                :required="active === 'uz'"
              />
              <UIInput
                :model-value="form[`location_${active}`]"
                @update:model-value="form[`location_${active}`] = $event"
                label="Joylashuv"
                placeholder="Masalan: Bosh bino, 1-zal"
              />
              <div>
                <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Tavsif</label>
                <RichEditor
                  :model-value="form[`description_${active}`]"
                  @update:model-value="form[`description_${active}`] = $event"
                  placeholder="Tadbir tavsifi..."
                />
              </div>
            </div>
          </template>
        </UITabs>

        <!-- Gallery section -->
        <div class="rounded-2xl p-5 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700">
          <div class="flex items-center justify-between mb-4">
            <div>
              <p class="text-sm font-bold text-ink-dark dark:text-white">Galereya</p>
              <p class="text-[11px] text-ink-faint mt-0.5">{{ form.gallery.length }} ta rasm</p>
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
              <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity flex gap-1">
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
                  class="px-1.5 h-6 rounded bg-white/90 hover:bg-white text-[11px] font-bold text-primary-800"
                  :disabled="i === 0"
                  @click="moveGallery(i, -1)"
                >←</button>
                <button
                  type="button"
                  class="px-1.5 h-6 rounded bg-white/90 hover:bg-white text-[11px] font-bold text-primary-800"
                  :disabled="i === form.gallery.length - 1"
                  @click="moveGallery(i, 1)"
                >→</button>
              </div>
              <div class="absolute bottom-1 right-2 text-[10px] font-bold text-white drop-shadow">
                {{ i + 1 }}
              </div>
            </div>
          </div>

          <div
            v-else
            class="rounded-xl border-2 border-dashed border-surface-muted dark:border-slate-700 p-8 text-center"
          >
            <ImageIcon class="w-8 h-8 mx-auto text-ink-faint mb-2" />
            <p class="text-xs text-ink-faint">Galereyaga rasmlar qo'shish uchun yuqoridagi tugmadan foydalaning</p>
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
            Sarlavha (UZ) ga qarab avtomatik yaratiladi: <code class="text-primary-700 dark:text-accent-400">/events/{{ form.slug || '...' }}</code>
          </p>
        </div>
      </div>

      <!-- Sidebar -->
      <aside class="space-y-4">
        <!-- Cover image -->
        <div class="rounded-2xl p-5 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 space-y-3">
          <p class="text-xs font-semibold uppercase tracking-wider text-ink-faint">Asosiy rasm</p>
          <div v-if="form.cover_image" class="aspect-video rounded-lg overflow-hidden bg-surface-soft dark:bg-slate-900">
            <img :src="form.cover_image" alt="" class="w-full h-full object-cover" />
          </div>
          <label class="block">
            <input type="file" accept="image/*" class="hidden" @change="onUploadCover" />
            <span class="block text-center px-4 py-2 rounded-lg border-2 border-dashed border-surface-muted dark:border-slate-700 text-xs text-ink-faint hover:border-accent-500 cursor-pointer">
              {{ uploadingCover ? 'Yuklanmoqda...' : (form.cover_image ? 'Boshqa rasm tanlash' : 'Rasm tanlash') }}
            </span>
          </label>
          <button v-if="form.cover_image" type="button" class="text-xs text-danger inline-flex items-center gap-1" @click="form.cover_image = null">
            <Trash2 class="w-3 h-3" /> Olib tashlash
          </button>
        </div>

        <!-- Date / Time -->
        <div class="rounded-2xl p-5 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 space-y-3">
          <p class="text-xs font-semibold uppercase tracking-wider text-ink-faint flex items-center gap-1.5">
            <Calendar class="w-3.5 h-3.5" /> Sana va vaqt
          </p>
          <label class="block">
            <span class="text-sm font-medium text-ink-medium dark:text-slate-300">Boshlanishi <span class="text-danger">*</span></span>
            <input
              v-model="form.starts_at"
              type="datetime-local"
              class="mt-1 w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-primary-400"
            />
          </label>
          <label class="block">
            <span class="text-sm font-medium text-ink-medium dark:text-slate-300">Tugashi (ixtiyoriy)</span>
            <input
              v-model="form.ends_at"
              type="datetime-local"
              class="mt-1 w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-primary-400"
            />
          </label>
        </div>

        <!-- Settings -->
        <div class="rounded-2xl p-5 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 space-y-3">
          <p class="text-xs font-semibold uppercase tracking-wider text-ink-faint">Sozlamalar</p>
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
