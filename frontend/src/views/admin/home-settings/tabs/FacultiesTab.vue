<script setup>
/**
 * Faculties — list with expandable program panel.
 * Two modals: faculty form, program form.
 */
import { ref, reactive, onMounted } from 'vue'
import {
  Plus, Edit3, Trash2, ChevronUp, ChevronDown, Save,
  ChevronRight, GraduationCap
} from 'lucide-vue-next'
import { AdminHomeAPI } from '@/api/admin'
import UIModal from '@/components/ui/UIModal.vue'
import UIButton from '@/components/ui/UIButton.vue'
import MultilingualInput from '@/components/admin/MultilingualInput.vue'
import MediaPicker from '@/components/admin/MediaPicker.vue'
import { useToast } from '@/composables/useToast'
import { useConfirm } from '@/composables/useConfirm'

const toast = useToast()
const confirm = useConfirm()
const items = ref([])
const loading = ref(true)
const expanded = ref(new Set())

// Faculty modal
const facModalOpen = ref(false)
const editingFac = ref(null)
const facForm = reactive({})
const facSaving = ref(false)

// Program modal
const progModalOpen = ref(false)
const editingProg = ref(null)
const progFacultyId = ref(null)
const progForm = reactive({})
const progSaving = ref(false)

async function load() {
  loading.value = true
  try {
    items.value = await AdminHomeAPI.faculties.list()
  } finally {
    loading.value = false
  }
}
onMounted(load)

function toggleExpand(id) {
  if (expanded.value.has(id)) expanded.value.delete(id)
  else expanded.value.add(id)
}

// ── Faculty CRUD ──
function newFaculty() {
  editingFac.value = null
  Object.keys(facForm).forEach(k => delete facForm[k])
  Object.assign(facForm, {
    slug: '', icon: 'AcademicCapIcon',
    name_uz: '', name_ru: '', name_en: '',
    description_uz: '', description_ru: '', description_en: '',
    cover_image: null, enabled: true, sort_order: 0
  })
  facModalOpen.value = true
}
function editFaculty(f) {
  editingFac.value = f
  Object.keys(facForm).forEach(k => delete facForm[k])
  Object.assign(facForm, JSON.parse(JSON.stringify(f)))
  facModalOpen.value = true
}
async function saveFaculty() {
  facSaving.value = true
  try {
    const { id, programs, created_at, updated_at, ...payload } = facForm
    if (editingFac.value) {
      await AdminHomeAPI.faculties.update(editingFac.value.id, payload)
      toast.success('Yangilandi')
    } else {
      await AdminHomeAPI.faculties.create(payload)
      toast.success('Yaratildi')
    }
    facModalOpen.value = false
    await load()
  } catch (e) {
    toast.error(e?.response?.data?.detail || 'Saqlashda xatolik')
  } finally {
    facSaving.value = false
  }
}
async function removeFaculty(f) {
  const ok = await confirm({
    title: "O'chirish",
    message: `"${f.name_uz}" fakulteti va uning ${f.programs?.length || 0} ta dasturi o'chiriladi.`,
    confirmLabel: "O'chirish", danger: true
  })
  if (!ok) return
  await AdminHomeAPI.faculties.remove(f.id)
  toast.success("O'chirildi")
  await load()
}
async function moveFaculty(f, dir) {
  const idx = items.value.findIndex(x => x.id === f.id)
  const swap = items.value[idx + dir]
  if (!swap) return
  await Promise.all([
    AdminHomeAPI.faculties.update(f.id,    { sort_order: swap.sort_order }),
    AdminHomeAPI.faculties.update(swap.id, { sort_order: f.sort_order })
  ])
  await load()
}

// ── Program CRUD ──
function newProgram(facultyId) {
  editingProg.value = null
  progFacultyId.value = facultyId
  Object.keys(progForm).forEach(k => delete progForm[k])
  Object.assign(progForm, {
    icon: 'BookOpenIcon', bg_class: 'bg-indigo-50',
    icon_bg_class: 'bg-indigo-500', ring_class: 'ring-indigo-200/60',
    level: 'bachelor', study_form: 'full_time',
    study_forms: [{ form: 'full_time', tuition: '', seats: null }],
    name_uz: '', name_ru: '', name_en: '',
    duration_uz: '', duration_ru: '', duration_en: '',
    tuition: '',
    language_uz: '', language_ru: '', language_en: '',
    degree_uz: '', degree_ru: '', degree_en: '',
    credits: null, seats: null,
    enabled: true, sort_order: 0
  })
  progModalOpen.value = true
}

function addStudyForm() {
  if (!progForm.study_forms) progForm.study_forms = []
  progForm.study_forms.push({ form: 'part_time', tuition: '', seats: null })
}
function removeStudyForm(i) {
  progForm.study_forms.splice(i, 1)
}
function editProgram(facultyId, p) {
  editingProg.value = p
  progFacultyId.value = facultyId
  Object.keys(progForm).forEach(k => delete progForm[k])
  Object.assign(progForm, JSON.parse(JSON.stringify(p)))
  if (!Array.isArray(progForm.study_forms) || !progForm.study_forms.length) {
    progForm.study_forms = [{ form: progForm.study_form || 'full_time', tuition: progForm.tuition || '', seats: progForm.seats }]
  }
  progModalOpen.value = true
}
async function saveProgram() {
  progSaving.value = true
  try {
    const { id, faculty_id, ...payload } = progForm
    if (editingProg.value) {
      await AdminHomeAPI.programs.update(editingProg.value.id, payload)
      toast.success('Yangilandi')
    } else {
      await AdminHomeAPI.programs.create(progFacultyId.value, payload)
      toast.success('Yaratildi')
    }
    progModalOpen.value = false
    await load()
  } catch (e) {
    toast.error(e?.response?.data?.detail || 'Saqlashda xatolik')
  } finally {
    progSaving.value = false
  }
}
async function removeProgram(p) {
  const ok = await confirm({
    title: "O'chirish",
    message: `"${p.name_uz}" dasturi o'chiriladi.`,
    confirmLabel: "O'chirish", danger: true
  })
  if (!ok) return
  await AdminHomeAPI.programs.remove(p.id)
  toast.success("O'chirildi")
  await load()
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-5">
      <div>
        <h2 class="text-lg font-display font-bold text-ink-dark dark:text-white">Fakultetlar</h2>
        <p class="text-xs text-ink-faint mt-0.5">Fakultet va uning yo'nalishlari (programs). Har birini kengaytirib o'zgartiring.</p>
      </div>
      <UIButton variant="accent" size="sm" @click="newFaculty">
        <template #icon-left><Plus class="w-4 h-4" /></template>
        Fakultet qo'shish
      </UIButton>
    </div>

    <div v-if="loading" class="text-center py-12 text-ink-faint text-sm">Yuklanmoqda...</div>

    <div v-else class="space-y-3">
      <article
        v-for="(f, i) in items"
        :key="f.id"
        class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 overflow-hidden"
      >
        <!-- Faculty header row -->
        <div class="flex items-center gap-3 p-4">
          <div class="flex flex-col gap-0.5">
            <button
              type="button"
              :disabled="i === 0"
              @click="moveFaculty(f, -1)"
              class="w-6 h-5 grid place-items-center rounded text-ink-faint hover:bg-surface-muted disabled:opacity-30"
            ><ChevronUp class="w-3 h-3" /></button>
            <button
              type="button"
              :disabled="i === items.length - 1"
              @click="moveFaculty(f, 1)"
              class="w-6 h-5 grid place-items-center rounded text-ink-faint hover:bg-surface-muted disabled:opacity-30"
            ><ChevronDown class="w-3 h-3" /></button>
          </div>

          <button
            type="button"
            class="w-9 h-9 grid place-items-center rounded-lg bg-primary-50 dark:bg-slate-700 text-primary-700 dark:text-primary-300 hover:bg-primary-100"
            @click="toggleExpand(f.id)"
          >
            <ChevronRight :class="['w-4 h-4 transition-transform', expanded.has(f.id) && 'rotate-90']" />
          </button>

          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <p class="text-sm font-bold text-ink-dark dark:text-white">{{ f.name_uz }}</p>
              <span class="text-[11px] font-mono text-ink-faint">/{{ f.slug }}</span>
              <span v-if="!f.enabled" class="text-[10px] px-1.5 py-0.5 rounded bg-surface-muted text-ink-faint">o'chirilgan</span>
            </div>
            <p class="text-xs text-ink-faint mt-0.5">
              <GraduationCap class="w-3 h-3 inline mr-1" />
              {{ f.programs?.length || 0 }} ta yo'nalish
            </p>
          </div>

          <div class="inline-flex items-center gap-0.5">
            <button
              type="button"
              class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-surface-soft hover:text-primary-600"
              @click="editFaculty(f)"
            ><Edit3 class="w-3.5 h-3.5" /></button>
            <button
              type="button"
              class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-danger-light hover:text-danger-dark"
              @click="removeFaculty(f)"
            ><Trash2 class="w-3.5 h-3.5" /></button>
          </div>
        </div>

        <!-- Programs panel -->
        <div v-if="expanded.has(f.id)" class="border-t border-surface-muted dark:border-slate-700 bg-surface-soft/50 dark:bg-slate-900/30 p-4">
          <div class="flex items-center justify-between mb-3">
            <p class="text-[11px] uppercase tracking-wider font-bold text-ink-faint">Yo'nalishlar (programs)</p>
            <UIButton variant="ghost" size="xs" @click="newProgram(f.id)">
              <template #icon-left><Plus class="w-3.5 h-3.5" /></template>
              Yo'nalish qo'shish
            </UIButton>
          </div>

          <div v-if="!f.programs?.length" class="text-xs text-ink-faint text-center py-6">
            Hozircha yo'nalish yo'q
          </div>

          <div v-else class="space-y-2">
            <div
              v-for="p in f.programs"
              :key="p.id"
              class="flex items-center gap-3 p-3 rounded-lg bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700"
            >
              <div :class="['w-8 h-8 rounded-lg grid place-items-center text-white text-[10px] font-bold flex-shrink-0', p.icon_bg_class]">
                {{ p.icon.replace('Icon', '').slice(0, 2) }}
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-semibold text-ink-dark dark:text-white truncate">{{ p.name_uz }}</p>
                <p class="text-[11px] text-ink-faint">
                  {{ p.duration_uz }} · {{ p.tuition }} · {{ p.language_uz }}
                </p>
              </div>
              <div class="inline-flex items-center gap-0.5">
                <button
                  type="button"
                  class="w-7 h-7 grid place-items-center rounded text-ink-faint hover:text-primary-600"
                  @click="editProgram(f.id, p)"
                ><Edit3 class="w-3.5 h-3.5" /></button>
                <button
                  type="button"
                  class="w-7 h-7 grid place-items-center rounded text-ink-faint hover:text-danger"
                  @click="removeProgram(p)"
                ><Trash2 class="w-3.5 h-3.5" /></button>
              </div>
            </div>
          </div>
        </div>
      </article>
    </div>

    <!-- Faculty modal -->
    <UIModal v-model="facModalOpen" size="lg" :title="editingFac ? 'Fakultetni tahrirlash' : 'Yangi fakultet'">
      <div class="space-y-4 max-h-[70vh] overflow-y-auto pr-1">
        <div class="grid sm:grid-cols-2 gap-3">
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">Slug</label>
            <input type="text" v-model="facForm.slug" placeholder="pedagogika"
              class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm font-mono" />
          </div>
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">Icon (heroicon)</label>
            <input type="text" v-model="facForm.icon" placeholder="AcademicCapIcon"
              class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
        </div>

        <MultilingualInput v-model="facForm" base="name"        label="Nomi" required />
        <MultilingualInput v-model="facForm" base="description" label="Tavsif" textarea :rows="3" />

        <MediaPicker v-model="facForm.cover_image" label="Cover rasm (ixtiyoriy)" />

        <div class="grid sm:grid-cols-2 gap-3">
          <label class="flex items-center justify-between gap-2 px-4 py-3 rounded-lg border border-surface-muted">
            <span class="text-sm">Faol</span>
            <input type="checkbox" v-model="facForm.enabled" class="w-4 h-4 accent-accent-500" />
          </label>
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">Tartib</label>
            <input type="number" v-model.number="facForm.sort_order"
              class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
        </div>
      </div>
      <template #footer>
        <UIButton variant="ghost" @click="facModalOpen = false">Bekor qilish</UIButton>
        <UIButton variant="accent" :loading="facSaving" @click="saveFaculty">
          <template #icon-left><Save class="w-4 h-4" /></template>
          Saqlash
        </UIButton>
      </template>
    </UIModal>

    <!-- Program modal -->
    <UIModal v-model="progModalOpen" size="lg" :title="editingProg ? 'Yo\'nalishni tahrirlash' : 'Yangi yo\'nalish'">
      <div class="space-y-4 max-h-[70vh] overflow-y-auto pr-1">
        <MultilingualInput v-model="progForm" base="name" label="Yo'nalish nomi" required />

        <!-- Level + study form (radio cards) -->
        <div class="grid sm:grid-cols-2 gap-3">
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">Daraja</label>
            <select v-model="progForm.level"
              class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm">
              <option value="bachelor">Bakalavr</option>
              <option value="master">Magistratura</option>
              <option value="phd">PhD / Doktorantura</option>
              <option value="short">Qisqa kurs / Sertifikat</option>
            </select>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-ink-medium mb-1.5">Icon (heroicon)</label>
          <input type="text" v-model="progForm.icon" placeholder="BookOpenIcon"
            class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
        </div>

        <!-- Study forms — multi-row editor -->
        <div class="rounded-lg border border-surface-muted dark:border-slate-700 p-4">
          <div class="flex items-center justify-between mb-3">
            <label class="text-sm font-bold text-ink-dark dark:text-white">Ta'lim shakllari va narxlar</label>
            <button type="button" class="text-[11px] font-bold text-primary-700 hover:text-accent-600" @click="addStudyForm">+ Shakl qo'shish</button>
          </div>
          <div v-if="!progForm.study_forms?.length" class="text-xs text-ink-faint py-3 text-center">Kamida 1 ta shakl kiriting</div>
          <div v-else class="space-y-2">
            <div
              v-for="(sf, i) in progForm.study_forms"
              :key="i"
              class="grid grid-cols-[1fr_1fr_80px_auto] gap-2 items-end p-2 rounded-lg bg-surface-soft dark:bg-slate-900/30"
            >
              <div>
                <label class="block text-[10px] uppercase tracking-wider text-ink-faint mb-1">Shakl</label>
                <select v-model="sf.form" class="w-full h-9 px-2 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs">
                  <option value="full_time">Kunduzgi</option>
                  <option value="part_time">Sirtqi</option>
                  <option value="evening">Kechki</option>
                  <option value="online">Onlayn</option>
                </select>
              </div>
              <div>
                <label class="block text-[10px] uppercase tracking-wider text-ink-faint mb-1">Narx</label>
                <input type="text" v-model="sf.tuition" placeholder="16 mln"
                  class="w-full h-9 px-2 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs" />
              </div>
              <div>
                <label class="block text-[10px] uppercase tracking-wider text-ink-faint mb-1">O'rin</label>
                <input type="number" v-model.number="sf.seats" placeholder="50"
                  class="w-full h-9 px-2 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs" />
              </div>
              <button type="button" class="w-8 h-9 grid place-items-center rounded text-ink-faint hover:text-danger" @click="removeStudyForm(i)">
                <Trash2 class="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>

        <MultilingualInput v-model="progForm" base="duration" label="Davomiyligi" placeholder="4 yil" />
        <MultilingualInput v-model="progForm" base="language" label="O'qitish tili" placeholder="O'zbek" />
        <MultilingualInput v-model="progForm" base="degree"   label="Beriladigan daraja" placeholder="Bakalavr diplomi" />

        <!-- Numeric extras -->
        <div class="grid sm:grid-cols-2 gap-3">
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">ECTS kreditlar</label>
            <input type="number" v-model.number="progForm.credits" placeholder="240"
              class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">O'rinlar soni</label>
            <input type="number" v-model.number="progForm.seats" placeholder="50"
              class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
        </div>

        <!-- Visual styling (collapsible — advanced) -->
        <details class="rounded-lg border border-surface-muted dark:border-slate-700 p-3">
          <summary class="text-xs font-bold uppercase tracking-wider text-ink-faint cursor-pointer select-none">Vizual sozlamalar (Tailwind classlar)</summary>
          <div class="grid sm:grid-cols-3 gap-3 mt-3">
            <div>
              <label class="block text-[11px] uppercase tracking-wider text-ink-faint mb-1">Card BG class</label>
              <input type="text" v-model="progForm.bg_class" placeholder="bg-indigo-50"
                class="w-full h-9 px-3 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-mono" />
            </div>
            <div>
              <label class="block text-[11px] uppercase tracking-wider text-ink-faint mb-1">Icon BG class</label>
              <input type="text" v-model="progForm.icon_bg_class" placeholder="bg-indigo-500"
                class="w-full h-9 px-3 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-mono" />
            </div>
            <div>
              <label class="block text-[11px] uppercase tracking-wider text-ink-faint mb-1">Ring class</label>
              <input type="text" v-model="progForm.ring_class" placeholder="ring-indigo-200/60"
                class="w-full h-9 px-3 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-mono" />
            </div>
          </div>
        </details>

        <div class="grid sm:grid-cols-2 gap-3">
          <label class="flex items-center justify-between gap-2 px-4 py-3 rounded-lg border border-surface-muted">
            <span class="text-sm">Faol</span>
            <input type="checkbox" v-model="progForm.enabled" class="w-4 h-4 accent-accent-500" />
          </label>
          <div>
            <label class="block text-sm font-medium text-ink-medium mb-1.5">Tartib</label>
            <input type="number" v-model.number="progForm.sort_order"
              class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>
        </div>
      </div>
      <template #footer>
        <UIButton variant="ghost" @click="progModalOpen = false">Bekor qilish</UIButton>
        <UIButton variant="accent" :loading="progSaving" @click="saveProgram">
          <template #icon-left><Save class="w-4 h-4" /></template>
          Saqlash
        </UIButton>
      </template>
    </UIModal>
  </div>
</template>
