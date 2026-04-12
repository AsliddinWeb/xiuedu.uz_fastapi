<script setup>
/**
 * Professional data table.
 *
 * @prop {Array<{ key, label, sortable?, align?, width?, render? }>} columns
 * @prop {Array} rows
 * @prop {boolean} loading
 * @prop {boolean} selectable
 * @prop {string}  rowKey — field to use as unique id
 * @emits sort, select
 *
 * Slots:
 *   cell-<key> — custom cell renderer per column
 *   empty      — empty state
 *   header-actions
 */
import { ref, computed } from 'vue'
import { ChevronUp, ChevronDown, ChevronsUpDown, Inbox } from 'lucide-vue-next'

const props = defineProps({
  columns:    { type: Array, required: true },
  rows:       { type: Array, default: () => [] },
  loading:    { type: Boolean, default: false },
  selectable: { type: Boolean, default: false },
  rowKey:     { type: String, default: 'id' }
})
const emit = defineEmits(['sort', 'select', 'row-click'])

const sortKey = ref(null)
const sortDir = ref('asc')
const selected = ref(new Set())

function toggleSort(col) {
  if (!col.sortable) return
  if (sortKey.value === col.key) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = col.key
    sortDir.value = 'asc'
  }
  emit('sort', { key: sortKey.value, dir: sortDir.value })
}

const sorted = computed(() => {
  if (!sortKey.value) return props.rows
  const dir = sortDir.value === 'asc' ? 1 : -1
  return [...props.rows].sort((a, b) => {
    const av = a[sortKey.value]; const bv = b[sortKey.value]
    if (av == null) return 1
    if (bv == null) return -1
    return av > bv ? dir : av < bv ? -dir : 0
  })
})

const allSelected = computed(
  () => props.rows.length > 0 && selected.value.size === props.rows.length
)

function toggleAll() {
  if (allSelected.value) selected.value = new Set()
  else selected.value = new Set(props.rows.map(r => r[props.rowKey]))
  emit('select', Array.from(selected.value))
}

function toggleRow(row) {
  const id = row[props.rowKey]
  const s = new Set(selected.value)
  s.has(id) ? s.delete(id) : s.add(id)
  selected.value = s
  emit('select', Array.from(s))
}

function clearSelection() {
  selected.value = new Set()
  emit('select', [])
}

defineExpose({ clearSelection })

function alignCls(a) {
  return a === 'right' ? 'text-right' : a === 'center' ? 'text-center' : 'text-left'
}
</script>

<template>
  <div class="card overflow-hidden">
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead class="bg-surface-soft dark:bg-slate-900/50 text-ink-light dark:text-slate-400">
          <tr>
            <th v-if="selectable" class="w-10 px-4 py-3">
              <input
                type="checkbox"
                :checked="allSelected"
                class="rounded border-surface-muted text-primary-600 focus:ring-primary-500"
                @change="toggleAll"
              />
            </th>
            <th
              v-for="col in columns"
              :key="col.key"
              :class="[
                'px-4 py-3 font-semibold uppercase text-[11px] tracking-wider',
                alignCls(col.align),
                col.sortable && 'cursor-pointer select-none hover:text-ink-dark dark:hover:text-white'
              ]"
              :style="col.width ? { width: col.width } : null"
              @click="toggleSort(col)"
            >
              <span class="inline-flex items-center gap-1">
                {{ col.label }}
                <template v-if="col.sortable">
                  <ChevronUp   v-if="sortKey === col.key && sortDir === 'asc'"  class="w-3 h-3" />
                  <ChevronDown v-else-if="sortKey === col.key && sortDir === 'desc'" class="w-3 h-3" />
                  <ChevronsUpDown v-else class="w-3 h-3 opacity-40" />
                </template>
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <!-- Loading skeleton -->
          <template v-if="loading">
            <tr v-for="n in 5" :key="`s${n}`" class="border-t border-surface-muted dark:border-slate-800">
              <td v-if="selectable" class="px-4 py-4"><div class="w-4 h-4 rounded bg-surface-soft dark:bg-slate-800 animate-pulse" /></td>
              <td v-for="col in columns" :key="col.key" class="px-4 py-4">
                <div class="h-3 rounded bg-surface-soft dark:bg-slate-800 animate-pulse" :style="{ width: col.key === columns[0].key ? '70%' : '50%' }" />
              </td>
            </tr>
          </template>

          <!-- Empty state -->
          <tr v-else-if="!sorted.length">
            <td :colspan="columns.length + (selectable ? 1 : 0)" class="px-4 py-16">
              <slot name="empty">
                <div class="text-center">
                  <Inbox class="w-12 h-12 text-ink-faint mx-auto mb-3" stroke-width="1.4" />
                  <p class="text-sm text-ink-light">Ma'lumot topilmadi</p>
                </div>
              </slot>
            </td>
          </tr>

          <!-- Rows -->
          <tr
            v-for="row in sorted"
            v-else
            :key="row[rowKey]"
            :class="[
              'border-t border-surface-muted dark:border-slate-800 transition-colors',
              'hover:bg-surface-soft/50 dark:hover:bg-slate-800/50',
              selected.has(row[rowKey]) && 'bg-primary-50/50 dark:bg-primary-900/10'
            ]"
            @click="$emit('row-click', row)"
          >
            <td v-if="selectable" class="px-4 py-3" @click.stop>
              <input
                type="checkbox"
                :checked="selected.has(row[rowKey])"
                class="rounded border-surface-muted text-primary-600 focus:ring-primary-500"
                @change="toggleRow(row)"
              />
            </td>
            <td v-for="col in columns" :key="col.key" :class="['px-4 py-3', alignCls(col.align)]">
              <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">
                {{ row[col.key] }}
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
