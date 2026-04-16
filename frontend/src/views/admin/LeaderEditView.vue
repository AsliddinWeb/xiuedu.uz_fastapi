<script setup>
/**
 * Leader create/edit — full page (not modal).
 * Route: /admin/leaders/new or /admin/leaders/:id
 */
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Save, ArrowLeft, Trash2 } from 'lucide-vue-next'
import { AdminLeadersAPI } from '@/api/admin'
import UIButton from '@/components/ui/UIButton.vue'
import MultilingualInput from '@/components/admin/MultilingualInput.vue'
import MediaPicker from '@/components/admin/MediaPicker.vue'
import { useToast } from '@/composables/useToast'
import { useConfirm } from '@/composables/useConfirm'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const confirm = useConfirm()

const isNew = computed(() => route.params.id === 'new' || !route.params.id)
const loading = ref(!isNew.value)
const saving = ref(false)

const form = reactive({
  photo: null,
  group: 'department_head',
  name_uz: '', name_ru: '', name_en: '',
  position_uz: '', position_ru: '', position_en: '',
  degree_uz: '', degree_ru: '', degree_en: '',
  bio_uz: '', bio_ru: '', bio_en: '',
  email: null, phone: null,
  enabled: true, sort_order: 0
})

async function load() {
  if (isNew.value) return
  loading.value = true
  try {
    const data = await AdminLeadersAPI.get(route.params.id)
    Object.assign(form, data)
  } catch (_) {
    toast.error('Yuklab bo\'lmadi')
    router.push('/admin/leaders')
  } finally {
    loading.value = false
  }
}
onMounted(load)

async function save() {
  if (!form.name_uz) {
    toast.error("Ism (UZ) bo'sh bo'lmasligi kerak")
    return
  }
  saving.value = true
  try {
    const { id, created_at, updated_at, ...payload } = form
    if (isNew.value) {
      const created = await AdminLeadersAPI.create(payload)
      toast.success('Yaratildi')
      router.replace(`/admin/leaders/${created.id}`)
    } else {
      await AdminLeadersAPI.update(route.params.id, payload)
      toast.success('Saqlandi')
    }
  } catch (e) {
    toast.error(e?.response?.data?.detail || 'Saqlashda xatolik')
  } finally {
    saving.value = false
  }
}

async function remove() {
  const ok = await confirm({
    title: "O'chirish",
    message: `"${form.name_uz}" o'chiriladi. Davom etilsinmi?`,
    confirmLabel: "O'chirish",
    danger: true
  })
  if (!ok) return
  await AdminLeadersAPI.remove(route.params.id)
  toast.success("O'chirildi")
  router.push('/admin/leaders')
}
</script>

<template>
  <div class="max-w-4xl">
    <!-- Header -->
    <div class="flex items-center gap-3 mb-6">
      <UIButton variant="ghost" size="sm" @click="router.push('/admin/leaders')">
        <template #icon-left><ArrowLeft class="w-4 h-4" /></template>
        Orqaga
      </UIButton>
      <h1 class="font-display text-xl font-bold text-ink-dark dark:text-white flex-1">
        {{ isNew ? 'Yangi rahbar' : 'Rahbarni tahrirlash' }}
      </h1>
      <UIButton v-if="!isNew" variant="danger" size="sm" @click="remove">
        <template #icon-left><Trash2 class="w-4 h-4" /></template>
        O'chirish
      </UIButton>
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>
        Saqlash
      </UIButton>
    </div>

    <div v-if="loading" class="text-center py-12 text-ink-faint">Yuklanmoqda...</div>

    <div v-else class="grid lg:grid-cols-[1fr_18rem] gap-5">
      <!-- Main column -->
      <div class="space-y-5">
        <!-- Name -->
        <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 space-y-4">
          <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Asosiy ma'lumotlar</p>
          <MultilingualInput v-model="form" base="name" label="Ism-familiya" required placeholder="Madiyev Otamurod" />
          <MultilingualInput v-model="form" base="position" label="Lavozim" placeholder="Rektor" />
          <MultilingualInput v-model="form" base="degree" label="Ilmiy daraja" placeholder="Iqtisodiyot fanlari nomzodi" />
        </div>

        <!-- Bio -->
        <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 space-y-4">
          <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Biografiya</p>
          <MultilingualInput v-model="form" base="bio" label="Bio" textarea :rows="5" placeholder="Tajriba, yutuqlar va boshqalar..." />
        </div>

        <!-- Contact -->
        <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 space-y-4">
          <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Aloqa</p>
          <div class="grid sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Email</label>
              <input type="email" v-model="form.email" placeholder="rektor@xiuedu.uz"
                     class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Telefon</label>
              <input type="text" v-model="form.phone" placeholder="+998 55 406-15-15"
                     class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <aside class="space-y-5">
        <!-- Photo -->
        <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5">
          <MediaPicker v-model="form.photo" label="Foto" />
        </div>

        <!-- Settings -->
        <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 space-y-3">
          <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Sozlamalar</p>

          <div>
            <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Guruh</label>
            <select v-model="form.group"
                    class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm">
              <option value="rector">Rektor</option>
              <option value="prorector">Prorektor</option>
              <option value="dean">Dekan</option>
              <option value="department_head">Kafedra mudiri</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">Tartib</label>
            <input type="number" v-model.number="form.sort_order"
                   class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
          </div>

          <label class="flex items-center justify-between gap-2 cursor-pointer">
            <span class="text-sm">Faol</span>
            <input type="checkbox" v-model="form.enabled" class="w-4 h-4 accent-accent-500" />
          </label>
        </div>

        <!-- Save (mobile) -->
        <UIButton variant="accent" :loading="saving" block @click="save">
          <template #icon-left><Save class="w-4 h-4" /></template>
          Saqlash
        </UIButton>
      </aside>
    </div>
  </div>
</template>
