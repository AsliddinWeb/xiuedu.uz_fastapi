<script setup>
/**
 * Leaders list — click to edit (separate page), no modals.
 */
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Edit3, Trash2, ChevronUp, ChevronDown, Check, X } from 'lucide-vue-next'
import { AdminLeadersAPI } from '@/api/admin'
import UIButton from '@/components/ui/UIButton.vue'
import { useToast } from '@/composables/useToast'
import { useConfirm } from '@/composables/useConfirm'

const router = useRouter()
const toast = useToast()
const confirm = useConfirm()

const items = ref([])
const loading = ref(true)

const GROUP_LABELS = {
  rector: 'Rektor',
  prorector: 'Prorektor',
  dean: 'Dekan',
  department_head: 'Kafedra mudiri'
}

async function load() {
  loading.value = true
  try { items.value = await AdminLeadersAPI.list() }
  finally { loading.value = false }
}
onMounted(load)

async function remove(item) {
  const ok = await confirm({
    title: "O'chirish",
    message: `"${item.name_uz}" o'chiriladi.`,
    confirmLabel: "O'chirish",
    danger: true
  })
  if (!ok) return
  await AdminLeadersAPI.remove(item.id)
  toast.success("O'chirildi")
  await load()
}

async function toggleEnabled(item) {
  await AdminLeadersAPI.update(item.id, { enabled: !item.enabled })
  await load()
}

async function move(item, dir) {
  const idx = items.value.findIndex(x => x.id === item.id)
  const swap = items.value[idx + dir]
  if (!swap) return
  await Promise.all([
    AdminLeadersAPI.update(item.id, { sort_order: swap.sort_order }),
    AdminLeadersAPI.update(swap.id, { sort_order: item.sort_order })
  ])
  await load()
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-xl font-display font-bold text-ink-dark dark:text-white">Rahbariyat</h1>
        <p class="text-sm text-ink-faint mt-0.5">Rektor, prorektorlar, dekanlar va kafedra mudirlari</p>
      </div>
      <UIButton variant="accent" @click="router.push('/admin/leaders/new')">
        <template #icon-left><Plus class="w-4 h-4" /></template>
        Qo'shish
      </UIButton>
    </div>

    <div v-if="loading" class="text-center py-12 text-ink-faint text-sm">Yuklanmoqda...</div>

    <div v-else-if="!items.length" class="text-center py-16 rounded-2xl border-2 border-dashed border-surface-muted dark:border-slate-700">
      <p class="text-sm text-ink-faint mb-3">Hozircha rahbar yo'q</p>
      <UIButton variant="accent" size="sm" @click="router.push('/admin/leaders/new')">
        <template #icon-left><Plus class="w-4 h-4" /></template>
        Birinchi rahbarni qo'shing
      </UIButton>
    </div>

    <div v-else class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 overflow-hidden">
      <table class="w-full">
        <thead class="bg-surface-soft dark:bg-slate-900/40">
          <tr>
            <th class="w-10 px-2 py-3"></th>
            <th class="text-left px-3 py-3 text-[10px] font-bold uppercase tracking-wider text-ink-faint">Foto</th>
            <th class="text-left px-3 py-3 text-[10px] font-bold uppercase tracking-wider text-ink-faint">Ism</th>
            <th class="text-left px-3 py-3 text-[10px] font-bold uppercase tracking-wider text-ink-faint">Guruh</th>
            <th class="text-left px-3 py-3 text-[10px] font-bold uppercase tracking-wider text-ink-faint">Lavozim</th>
            <th class="px-3 py-3 text-[10px] font-bold uppercase tracking-wider text-ink-faint">Holat</th>
            <th class="w-24 px-3 py-3"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(item, i) in items"
            :key="item.id"
            class="border-t border-surface-muted dark:border-slate-700 hover:bg-surface-soft/50 dark:hover:bg-slate-900/20 cursor-pointer"
            @click="router.push(`/admin/leaders/${item.id}`)"
          >
            <td class="px-2 py-2.5 align-middle" @click.stop>
              <div class="flex flex-col gap-0.5">
                <button type="button" :disabled="i === 0" @click="move(item, -1)"
                        class="w-6 h-5 grid place-items-center rounded text-ink-faint hover:bg-surface-muted disabled:opacity-30">
                  <ChevronUp class="w-3 h-3" />
                </button>
                <button type="button" :disabled="i === items.length - 1" @click="move(item, 1)"
                        class="w-6 h-5 grid place-items-center rounded text-ink-faint hover:bg-surface-muted disabled:opacity-30">
                  <ChevronDown class="w-3 h-3" />
                </button>
              </div>
            </td>
            <td class="px-3 py-2.5">
              <img v-if="item.photo" :src="item.photo" class="w-10 h-10 rounded-lg object-cover" />
              <div v-else class="w-10 h-10 rounded-lg bg-primary-50 dark:bg-slate-700 grid place-items-center text-primary-700 dark:text-primary-300 text-xs font-bold">
                {{ (item.name_uz || 'U').charAt(0) }}
              </div>
            </td>
            <td class="px-3 py-2.5">
              <p class="text-sm font-semibold text-ink-dark dark:text-white">{{ item.name_uz }}</p>
              <p class="text-[11px] text-ink-faint">{{ item.email || '' }}</p>
            </td>
            <td class="px-3 py-2.5">
              <span class="text-xs font-semibold px-2 py-0.5 rounded-md bg-surface-soft dark:bg-slate-700 text-ink-medium">
                {{ GROUP_LABELS[item.group] || item.group }}
              </span>
            </td>
            <td class="px-3 py-2.5 text-sm text-ink-light">{{ item.position_uz }}</td>
            <td class="px-3 py-2.5 text-center" @click.stop>
              <button type="button" @click="toggleEnabled(item)"
                      :class="['inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-bold',
                               item.enabled ? 'bg-success-light text-success-dark' : 'bg-surface-muted text-ink-faint']">
                <Check v-if="item.enabled" class="w-3 h-3" /><X v-else class="w-3 h-3" />
                {{ item.enabled ? 'Faol' : 'Faol emas' }}
              </button>
            </td>
            <td class="px-3 py-2.5 text-right" @click.stop>
              <div class="inline-flex items-center gap-0.5">
                <button type="button" @click="router.push(`/admin/leaders/${item.id}`)"
                        class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-surface-soft hover:text-primary-600">
                  <Edit3 class="w-3.5 h-3.5" />
                </button>
                <button type="button" @click="remove(item)"
                        class="w-8 h-8 grid place-items-center rounded-lg text-ink-faint hover:bg-danger-light hover:text-danger-dark">
                  <Trash2 class="w-3.5 h-3.5" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
