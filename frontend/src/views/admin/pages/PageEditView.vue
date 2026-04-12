<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Save, ArrowLeft, Trash2, ExternalLink } from 'lucide-vue-next'
import { AdminPagesAPI } from '@/api/admin'
import UIInput from '@/components/ui/UIInput.vue'
import UIButton from '@/components/ui/UIButton.vue'
import UITabs from '@/components/ui/UITabs.vue'
import UIModal from '@/components/ui/UIModal.vue'
import RichEditor from '@/components/ui/RichEditor.vue'
import { useToast } from '@/composables/useToast'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const isNew = computed(() => route.params.id === 'new' || !route.params.id)
const lang = ref('uz')
const saving = ref(false)
const confirmDelete = ref(false)

const form = reactive({
  slug: '',
  is_published: true,
  page_order: 0,
  parent_id: null,
  title_uz: '', title_ru: '', title_en: '',
  content_uz: '', content_ru: '', content_en: ''
})

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

async function load() {
  if (isNew.value) return
  try {
    const all = await AdminPagesAPI.list()
    const found = all.find(p => p.id === Number(route.params.id))
    if (found) Object.assign(form, found)
  } catch (_) {}
}
onMounted(load)

async function save() {
  saving.value = true
  try {
    if (isNew.value) {
      const created = await AdminPagesAPI.create(form)
      toast.success('Yaratildi')
      router.replace(`/admin/pages/${created.id}`)
    } else {
      await AdminPagesAPI.update(route.params.id, form)
      toast.success('Saqlandi')
    }
  } catch (e) {
    toast.error(e?.response?.data?.detail || "Saqlashda xatolik")
  } finally { saving.value = false }
}

async function doDelete() {
  await AdminPagesAPI.remove(route.params.id)
  toast.success("O'chirildi")
  router.push('/admin/pages')
}
</script>

<template>
  <div class="space-y-5">
    <div class="flex items-center gap-3">
      <UIButton variant="ghost" size="sm" @click="router.push('/admin/pages')">
        <template #icon-left><ArrowLeft class="w-4 h-4" /></template>
        Orqaga
      </UIButton>
      <h2 class="font-display text-xl font-bold text-primary-700 dark:text-white flex-1">
        {{ isNew ? "Yangi sahifa" : "Sahifa tahrirlash" }}
      </h2>
      <a v-if="!isNew && form.slug" :href="`/p/${form.slug}`" target="_blank" class="text-xs text-accent-500 inline-flex items-center gap-1 hover:underline">
        Preview <ExternalLink class="w-3 h-3" />
      </a>
      <UIButton v-if="!isNew" variant="danger" size="sm" @click="confirmDelete = true">
        <template #icon-left><Trash2 class="w-4 h-4" /></template>
        O'chirish
      </UIButton>
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>
        Saqlash
      </UIButton>
    </div>

    <div class="grid lg:grid-cols-[1fr,18rem] gap-5">
      <div class="space-y-4">
        <UITabs v-model="lang" :tabs="tabs">
          <template #default="{ active: a }">
            <div class="space-y-4">
              <UIInput :model-value="form[`title_${a}`]" @update:model-value="form[`title_${a}`] = $event" label="Sarlavha" required />
              <div>
                <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Kontent</label>
                <RichEditor :model-value="form[`content_${a}`]" @update:model-value="form[`content_${a}`] = $event" placeholder="Sahifa matni..." min-height="28rem" />
              </div>
            </div>
          </template>
        </UITabs>

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
            Sarlavha (UZ) ga qarab avtomatik yaratiladi: <code class="text-primary-700 dark:text-accent-400">/p/{{ form.slug || '...' }}</code>
          </p>
        </div>
      </div>

      <aside>
        <div class="rounded-2xl p-5 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 space-y-3">
          <p class="text-xs font-semibold uppercase tracking-wider text-ink-faint">Sozlamalar</p>
          <label class="flex items-center justify-between gap-2 cursor-pointer">
            <span class="text-sm">Chop qilingan</span>
            <input type="checkbox" v-model="form.is_published" class="w-4 h-4 accent-accent-500" />
          </label>
          <UIInput :model-value="form.page_order" @update:model-value="form.page_order = Number($event)" type="number" label="Tartib" />
          <UIInput :model-value="form.parent_id || ''" @update:model-value="form.parent_id = $event ? Number($event) : null" label="Parent ID" placeholder="ixtiyoriy" />
        </div>
      </aside>
    </div>

    <UIModal v-model="confirmDelete" title="Tasdiqlang" size="sm">
      <p class="text-sm text-neutral-600 dark:text-neutral-300">Bu sahifani o'chirishga ishonchingiz komilmi?</p>
      <template #footer>
        <UIButton variant="ghost" @click="confirmDelete = false">Bekor qilish</UIButton>
        <UIButton variant="danger" @click="doDelete">O'chirish</UIButton>
      </template>
    </UIModal>
  </div>
</template>
