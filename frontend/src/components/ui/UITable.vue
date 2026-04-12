<script setup>
/**
 * @prop {Array<{key:string, label:string, sortable?:boolean, align?:'left'|'center'|'right', width?:string}>} columns
 * @prop {Array} rows
 * @prop {boolean} loading
 */
import { ref, computed } from 'vue'
import { ChevronUp, ChevronDown, ChevronsUpDown } from 'lucide-vue-next'

const props = defineProps({
  columns: { type: Array, required: true },
  rows: { type: Array, default: () => [] },
  loading: Boolean,
  rowKey: { type: String, default: 'id' }
})
const emit = defineEmits(['row-click'])

const sortKey = ref(null)
const sortDir = ref('asc')

function toggleSort(col) {
  if (!col.sortable) return
  if (sortKey.value === col.key) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = col.key
    sortDir.value = 'asc'
  }
}

const sortedRows = computed(() => {
  if (!sortKey.value) return props.rows
  const dir = sortDir.value === 'asc' ? 1 : -1
  return [...props.rows].sort((a, b) => {
    const av = a[sortKey.value]
    const bv = b[sortKey.value]
    if (av == null) return 1
    if (bv == null) return -1
    return av > bv ? dir : av < bv ? -dir : 0
  })
})

const alignCls = (a) => (a === 'right' ? 'text-right' : a === 'center' ? 'text-center' : 'text-left')
</script>

<template>
  <div class="overflow-x-auto rounded-xl border border-neutral-200 dark:border-primary-700">
    <table class="w-full text-sm">
      <thead class="bg-neutral-50 dark:bg-primary-900 text-neutral-600 dark:text-neutral-300">
        <tr>
          <th
            v-for="col in columns"
            :key="col.key"
            :class="['px-4 py-3 font-semibold uppercase tracking-wide text-xs', alignCls(col.align), col.sortable && 'cursor-pointer select-none']"
            :style="col.width ? { width: col.width } : null"
            @click="toggleSort(col)"
          >
            <span class="inline-flex items-center gap-1">
              {{ col.label }}
              <template v-if="col.sortable">
                <ChevronUp v-if="sortKey === col.key && sortDir === 'asc'" class="w-3 h-3" />
                <ChevronDown v-else-if="sortKey === col.key && sortDir === 'desc'" class="w-3 h-3" />
                <ChevronsUpDown v-else class="w-3 h-3 opacity-40" />
              </template>
            </span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="loading">
          <td :colspan="columns.length" class="p-8 text-center text-neutral-500">{{ $t('common.loading') }}</td>
        </tr>
        <tr v-else-if="!sortedRows.length">
          <td :colspan="columns.length" class="p-8 text-center text-neutral-500">
            <slot name="empty">{{ $t('common.not_found') }}</slot>
          </td>
        </tr>
        <tr
          v-for="row in sortedRows"
          v-else
          :key="row[rowKey]"
          class="border-t border-neutral-200 dark:border-primary-700 hover:bg-neutral-50 dark:hover:bg-primary-900/40 transition cursor-pointer"
          @click="$emit('row-click', row)"
        >
          <td v-for="col in columns" :key="col.key" :class="['px-4 py-3', alignCls(col.align)]">
            <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">
              {{ row[col.key] }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
