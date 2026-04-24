<script setup>
/**
 * Reusable program card — shows level badge, degree, duration, language,
 * credits, and **multiple study forms** with per-form tuition and seats.
 */
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { Clock, GraduationCap, Languages, Award, Users, BookOpenCheck } from 'lucide-vue-next'
import { resolveIcon } from '@/utils/iconResolver'

const props = defineProps({
  program: { type: Object, required: true }
})
const { t } = useI18n()

const levelLabel = computed(() => t(`home.level_${props.program.level || 'bachelor'}`))
const formLabel = (form) => t(`home.form_${form || 'full_time'}`)

const levelStyle = computed(() => {
  switch (props.program.level) {
    case 'master':   return 'bg-violet-100 text-violet-800 dark:bg-violet-900/40 dark:text-violet-200'
    case 'phd':      return 'bg-rose-100   text-rose-800   dark:bg-rose-900/40   dark:text-rose-200'
    case 'short':    return 'bg-amber-100  text-amber-800  dark:bg-amber-900/40  dark:text-amber-200'
    default:         return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-200'
  }
})

const studyForms = computed(() => props.program.study_forms || [])
const totalSeats = computed(() => studyForms.value.reduce((s, f) => s + (f.seats || 0), 0))

// For bachelor-level programs we want to always show both kunduzgi and sirtqi
// rows (keeps card height consistent). Missing forms render as a greyed-out
// "mavjud emas" row so they visually take the same space.
const COMPLEMENT_FORMS = ['full_time', 'part_time']
const displayForms = computed(() => {
  const present = new Map(studyForms.value.map(f => [f.form, f]))
  const rows = []
  for (const form of COMPLEMENT_FORMS) {
    if (present.has(form)) rows.push({ ...present.get(form), missing: false })
    else rows.push({ form, missing: true })
  }
  for (const f of studyForms.value) {
    if (!COMPLEMENT_FORMS.includes(f.form)) rows.push({ ...f, missing: false })
  }
  return rows
})
</script>

<template>
  <article
    :class="[
      'group relative overflow-hidden rounded-2xl p-6 lg:p-7 ring-1 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_20px_50px_rgba(10,13,61,0.10)]',
      program.bg_class,
      program.ring_class
    ]"
  >
    <!-- Decorative blob -->
    <div :class="['absolute -top-10 -right-10 w-32 h-32 rounded-full blur-3xl opacity-30 group-hover:opacity-50 transition-opacity', program.icon_bg_class]" />

    <div class="relative flex flex-col h-full">
      <!-- Header: icon + level badge -->
      <div class="flex items-start justify-between mb-4">
        <div :class="['w-14 h-14 rounded-2xl grid place-items-center text-white shadow-lg', program.icon_bg_class]">
          <component :is="resolveIcon(program.icon)" class="w-7 h-7" stroke-width="1.7" />
        </div>
        <div class="flex flex-col items-end gap-1">
          <span :class="['inline-flex items-center px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider', levelStyle]">
            {{ levelLabel }}
          </span>
          <span v-if="studyForms.length > 1" class="text-[10px] font-semibold text-ink-faint">
            {{ studyForms.length }} ta shakl
          </span>
        </div>
      </div>

      <!-- Title -->
      <h3 class="text-lg font-display font-bold text-ink-dark dark:text-white leading-snug mb-2 group-hover:text-primary-800 dark:group-hover:text-white">
        {{ program.name }}
      </h3>

      <!-- Degree -->
      <p v-if="program.degree" class="text-[12px] text-ink-faint inline-flex items-center gap-1 mb-3">
        <Award class="w-3 h-3" /> {{ program.degree }}
      </p>

      <!-- Meta: duration / language / credits -->
      <div class="grid grid-cols-2 gap-x-3 gap-y-1.5 text-[12px] text-ink-medium dark:text-slate-300 mb-3">
        <span class="inline-flex items-center gap-1.5 font-semibold">
          <Clock class="w-3.5 h-3.5 text-ink-faint" /> {{ program.duration }}
        </span>
        <span class="inline-flex items-center gap-1.5">
          <Languages class="w-3.5 h-3.5 text-ink-faint" /> {{ program.language }}
        </span>
        <span v-if="program.credits" class="inline-flex items-center gap-1.5">
          <GraduationCap class="w-3.5 h-3.5 text-ink-faint" /> {{ program.credits }} {{ t('home.program_credits') }}
        </span>
        <span v-if="totalSeats" class="inline-flex items-center gap-1">
          <Users class="w-3.5 h-3.5 text-ink-faint" /> {{ totalSeats }} {{ t('home.program_seats') }}
        </span>
      </div>

      <!-- Study forms — per-form tuition strip -->
      <div class="mt-auto pt-4 border-t border-ink-dark/10 dark:border-white/10 space-y-2">
        <div
          v-for="(sf, i) in displayForms"
          :key="i"
          :class="['flex items-center justify-between text-[12px]', sf.missing && 'opacity-50']"
        >
          <span class="inline-flex items-center gap-1.5">
            <BookOpenCheck class="w-3.5 h-3.5 text-ink-faint" />
            <span class="font-semibold text-ink-medium dark:text-slate-300">{{ formLabel(sf.form) }}</span>
            <span v-if="!sf.missing && sf.seats" class="text-ink-faint">({{ sf.seats }} {{ t('home.program_seats') }})</span>
          </span>
          <span
            v-if="!sf.missing"
            class="px-2.5 py-0.5 rounded-md bg-white/80 dark:bg-slate-900/40 font-bold text-primary-800 dark:text-accent-400"
          >{{ sf.tuition }}</span>
          <span
            v-else
            class="px-2.5 py-0.5 rounded-md bg-surface-muted/60 dark:bg-slate-700/40 font-semibold text-ink-faint italic"
          >{{ t('home.form_unavailable') }}</span>
        </div>
      </div>
    </div>
  </article>
</template>
