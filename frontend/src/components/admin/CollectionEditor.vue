<script setup>
/**
 * Generic CRUD list editor for home page collections.
 *
 * Props:
 *   title       — section heading
 *   description — short helper text
 *   api         — { list, create, update, remove } object from AdminHomeAPI
 *   fields      — array describing each form field:
 *                  { key, label, type, ... }
 *                 type ∈ 'text' | 'textarea' | 'number' | 'checkbox'
 *                       | 'multilingual' | 'multilingual-textarea'
 *                       | 'media' | 'icon' | 'select'
 *                 multilingual fields use `key` as the BASE (key_uz/_ru/_en)
 *   listColumns — array of { key, label, render?(row) } for the table preview
 *   defaultItem — object with default values for new items
 */
import { ref, reactive, onMounted } from 'vue'
import {
  Plus, Edit3, Trash2, ChevronUp, ChevronDown, Save, X, Check
} from 'lucide-vue-next'
import UIModal from '@/components/ui/UIModal.vue'
import UIButton from '@/components/ui/UIButton.vue'
import MultilingualInput from './MultilingualInput.vue'
import MultilingualListField from './MultilingualListField.vue'
import MediaPicker from './MediaPicker.vue'
import { useToast } from '@/composables/useToast'
import { useConfirm } from '@/composables/useConfirm'

const props = defineProps({
  title:       { type: String, required: true },
  description: String,
  api:         { type: Object, required: true },
  fields:      { type: Array,  required: true },
  listColumns: { type: Array,  required: true },
  defaultItem: { type: Object, default: () => ({}) },
  emptyText:   { type: String, default: "Hozircha element yo'q" }
})

const toast = useToast()
const confirm = useConfirm()
const items = ref([])
const loading = ref(true)
const modalOpen = ref(false)
const editing = ref(null)
const form = reactive({})
const saving = ref(false)

async function load() {
  loading.value = true
  try {
    items.value = (await props.api.list()) || []
  } finally {
    loading.value = false
  }
}
onMounted(load)

function newItem() {
  editing.value = null
  Object.keys(form).forEach(k => delete form[k])
  Object.assign(form, JSON.parse(JSON.stringify(props.defaultItem)))
  modalOpen.value = true
}
function editItem(item) {
  editing.value = item
  Object.keys(form).forEach(k => delete form[k])
  Object.assign(form, JSON.parse(JSON.stringify(item)))
  modalOpen.value = true
}

async function save() {
  saving.value = true
  try {
    if (editing.value) {
      await props.api.update(editing.value.id, form)
      toast.success('Yangilandi')
    } else {
      await props.api.create(form)
      toast.success('Yaratildi')
    }
    modalOpen.value = false
    await load()
  } catch (e) {
    toast.error(e?.response?.data?.detail || 'Saqlashda xatolik')
  } finally {
    saving.value = false
  }
}

async function removeItem(item) {
  const ok = await confirm({
    title: "O'chirish",
    message: 'Bu element o\'chiriladi. Davom etilsinmi?',
    confirmLabel: "O'chirish",
    danger: true
  })
  if (!ok) return
  await props.api.remove(item.id)
  toast.success("O'chirildi")
  await load()
}

async function toggleEnabled(item) {
  await props.api.update(item.id, { enabled: !item.enabled })
  await load()
}

async function move(item, dir) {
  const idx = items.value.findIndex(x => x.id === item.id)
  const swap = items.value[idx + dir]
  if (!swap) return
  await Promise.all([
    props.api.update(item.id, { sort_order: swap.sort_order }),
    props.api.update(swap.id, { sort_order: item.sort_order })
  ])
  await load()
}
</script>

<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-5">
      <div>
        <h2 class="text-lg font-display font-bold text-ink-dark dark:text-white">{{ title }}</h2>
        <p v-if="description" class="text-xs text-ink-faint mt-0.5">{{ description }}</p>
      </div>
      <UIButton variant="accent" size="sm" @click="newItem">
        <template #icon-left><Plus class="w-4 h-4" /></template>
        Qo'shish
      </UIButton>
    </div>

    <!-- List -->
    <div v-if="loading" class="text-center py-12 text-ink-faint text-sm">Yuklanmoqda...</div>
    <div v-else-if="!items.length" class="text-center py-12 rounded-2xl border-2 border-dashed border-surface-muted dark:border-slate-700">
      <p class="text-sm text-ink-faint">{{ emptyText }}</p>
    </div>

    <div v-else class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 overflow-hidden">
      <table class="w-full">
        <thead class="bg-surface-soft dark:bg-slate-900/40">
          <tr>
            <th class="w-10 px-2 py-3"></th>
            <th
              v-for="col in listColumns"
              :key="col.key"
              class="text-left px-3 py-3 text-[10px] font-bold uppercase tracking-wider text-ink-faint"
            >{{ col.label }}</th>
            <th class="w-24 px-3 py-3"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(item, i) in items"
            :key="item.id"
            class="border-t border-surface-muted dark:border-slate-700 hover:bg-surface-soft/50 dark:hover:bg-slate-900/20"
          >
            <td class="px-2 py-2.5 align-middle">
              <div class="flex flex-col gap-0.5">
                <button
                  type="button"
                  class="w-6 h-5 grid place-items-center rounded text-ink-faint hover:bg-surface-muted disabled:opacity-30"
                  :disabled="i === 0"
                  @click="move(item, -1)"
                ><ChevronUp class="w-3 h-3" /></button>
                <button
                  type="button"
                  class="w-6 h-5 grid place-items-center rounded text-ink-faint hover:bg-surface-muted disabled:opacity-30"
                  :disabled="i === items.length - 1"
                  @click="move(item, 1)"
                ><ChevronDown class="w-3 h-3" /></button>
              </div>
            </td>
            <td
              v-for="col in listColumns"
              :key="col.key"
              class="px-3 py-2.5 text-sm text-ink-medium dark:text-slate-300"
            >
              <slot :name="`cell-${col.key}`" :row="item">
                <span v-if="col.key === 'enabled'">
                  <button
                    type="button"
                    @click="toggleEnabled(item)"
                    :class="[
                      'inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-bold',
                      item.enabled
                        ? 'bg-success-light text-success-dark'
                        : 'bg-surface-muted text-ink-faint'
                    ]"
                  >
                    <Check v-if="item.enabled" class="w-3 h-3" /><X v-else class="w-3 h-3" />
                    {{ item.enabled ? 'Faol' : "Faol emas" }}
                  </button>
                </span>
                <span v-else-if="col.key === 'image' || col.key === 'avatar'">
                  <img v-if="item[col.key]" :src="item[col.key]" :alt="item.title_uz || ''" class="w-12 h-9 rounded object-cover" />
                  <span v-else class="text-ink-faint">—</span>
                </span>
                <span v-else>{{ col.render ? col.render(item) : (item[col.key] ?? '—') }}</span>
              </slot>
            </td>
            <td class="px-3 py-2.5 text-right">
              <div class="inline-flex items-center gap-0.5">
                <button
                  type="button"
                  class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-surface-soft hover:text-primary-600"
                  @click="editItem(item)"
                ><Edit3 class="w-3.5 h-3.5" /></button>
                <button
                  type="button"
                  class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-danger-light hover:text-danger-dark"
                  @click="removeItem(item)"
                ><Trash2 class="w-3.5 h-3.5" /></button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Edit modal -->
    <UIModal v-model="modalOpen" size="lg" :title="editing ? 'Tahrirlash' : 'Yangi qo\'shish'">
      <div class="space-y-4 max-h-[70vh] overflow-y-auto pr-1">
        <template v-for="f in fields" :key="f.key">
          <!-- Multilingual single line -->
          <MultilingualInput
            v-if="f.type === 'multilingual'"
            v-model="form"
            :base="f.key"
            :label="f.label"
            :placeholder="f.placeholder"
            :hint="f.hint"
            :required="f.required"
          />

          <!-- Multilingual textarea -->
          <MultilingualInput
            v-else-if="f.type === 'multilingual-textarea'"
            v-model="form"
            :base="f.key"
            :label="f.label"
            :placeholder="f.placeholder"
            :hint="f.hint"
            :required="f.required"
            textarea
            :rows="f.rows || 3"
          />

          <!-- Multilingual list (uz/ru/en items) -->
          <MultilingualListField
            v-else-if="f.type === 'multilingual-list'"
            :model-value="form[f.key] || []"
            @update:model-value="form[f.key] = $event"
            :label="f.label"
            :hint="f.hint"
          />

          <!-- Media upload -->
          <MediaPicker
            v-else-if="f.type === 'media'"
            :model-value="form[f.key]"
            @update:model-value="form[f.key] = $event"
            :label="f.label"
            :hint="f.hint"
            :accept="f.accept || 'image/*'"
            :preview="f.previewType || 'image'"
          />

          <!-- Plain textarea -->
          <div v-else-if="f.type === 'textarea'">
            <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">{{ f.label }}</label>
            <textarea
              v-model="form[f.key]"
              :rows="f.rows || 3"
              :placeholder="f.placeholder"
              class="w-full px-3 py-2.5 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:border-primary-500"
            />
            <p v-if="f.hint" class="mt-1 text-[11px] text-ink-faint">{{ f.hint }}</p>
          </div>

          <!-- Checkbox -->
          <label v-else-if="f.type === 'checkbox'" class="flex items-center justify-between gap-2 cursor-pointer">
            <span>
              <span class="text-sm font-medium text-ink-medium dark:text-slate-300">{{ f.label }}</span>
              <span v-if="f.hint" class="block text-[11px] text-ink-faint mt-0.5">{{ f.hint }}</span>
            </span>
            <input type="checkbox" v-model="form[f.key]" class="w-4 h-4 accent-accent-500" />
          </label>

          <!-- Number -->
          <div v-else-if="f.type === 'number'">
            <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">{{ f.label }}</label>
            <input
              type="number"
              v-model.number="form[f.key]"
              :placeholder="f.placeholder"
              class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:border-primary-500"
            />
            <p v-if="f.hint" class="mt-1 text-[11px] text-ink-faint">{{ f.hint }}</p>
          </div>

          <!-- Date -->
          <div v-else-if="f.type === 'date'">
            <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">{{ f.label }}</label>
            <input
              type="date"
              v-model="form[f.key]"
              class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:border-primary-500"
            />
            <p v-if="f.hint" class="mt-1 text-[11px] text-ink-faint">{{ f.hint }}</p>
          </div>

          <!-- Select -->
          <div v-else-if="f.type === 'select'">
            <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">{{ f.label }}</label>
            <select
              v-model="form[f.key]"
              class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:border-primary-500"
            >
              <option v-for="opt in f.options" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
            <p v-if="f.hint" class="mt-1 text-[11px] text-ink-faint">{{ f.hint }}</p>
          </div>

          <!-- Plain text (default) -->
          <div v-else>
            <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">{{ f.label }}</label>
            <input
              type="text"
              v-model="form[f.key]"
              :placeholder="f.placeholder"
              class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:border-primary-500"
            />
            <p v-if="f.hint" class="mt-1 text-[11px] text-ink-faint">{{ f.hint }}</p>
          </div>
        </template>
      </div>

      <template #footer>
        <UIButton variant="ghost" @click="modalOpen = false">Bekor qilish</UIButton>
        <UIButton variant="accent" :loading="saving" @click="save">
          <template #icon-left><Save class="w-4 h-4" /></template>
          Saqlash
        </UIButton>
      </template>
    </UIModal>
  </div>
</template>
