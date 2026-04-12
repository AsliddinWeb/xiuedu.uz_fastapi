<script setup>
/**
 * VacanciesView — fully driven by /api/page-settings/vacancies.
 */
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { Briefcase, MapPin, Calendar, Inbox, ArrowRight, Mail, Lock } from 'lucide-vue-next'
import PageHero from '@/components/sections/PageHero.vue'
import UILoader from '@/components/ui/UILoader.vue'
import { PageSettingsAPI } from '@/api/endpoints'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { useSeo } from '@/composables/useSeo'
import { breadcrumbSchema } from '@/utils/schema'
import { useLanguageStore } from '@/stores/language'

const { t } = useI18n()
const lang = useLanguageStore()
useScrollAnimation()
useSeo(() => ({
  title: t('nav.vacancies'),
  schema: breadcrumbSchema([
    { name: t('nav.home'),      url: '/' },
    { name: t('nav.vacancies'), url: '/careers' }
  ])
}))

const data = ref(null)
const loading = ref(true)
const filter = ref('')

async function load() {
  loading.value = true
  try {
    data.value = await PageSettingsAPI.vacancies(lang.currentLang)
  } catch (_) {
    data.value = null
  } finally {
    loading.value = false
  }
}
onMounted(load)
watch(() => lang.currentLang, load)

const page        = computed(() => data.value?.page)
const vacancies   = computed(() => data.value?.vacancies || [])
const departments = computed(() => data.value?.departments || [])

const visible = computed(() => {
  if (!filter.value) return vacancies.value
  return vacancies.value.filter(v => v.department === filter.value)
})

// Employment type labels (i18n could be added later)
const TYPE_LABELS = {
  full_time:  { uz: 'Kunduzgi',     ru: 'Очно',          en: 'Full-time' },
  part_time:  { uz: 'Yarim stavka', ru: 'Полставки',     en: 'Part-time' },
  contract:   { uz: 'Kontrakt',     ru: 'Контракт',      en: 'Contract' },
  internship: { uz: 'Stajirovka',   ru: 'Стажировка',    en: 'Internship' },
  online:     { uz: 'Onlayn',       ru: 'Онлайн',        en: 'Online' },
}
function typeLabel(type) {
  return (TYPE_LABELS[type] || {})[lang.currentLang] || type
}

function fmtDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString(lang.currentLang === 'ru' ? 'ru-RU' : 'uz-UZ', {
    day: 'numeric', month: 'short', year: 'numeric'
  })
}
</script>

<template>
  <div>
    <PageHero
      :title="page?.hero_title || t('nav.vacancies')"
      :subtitle="page?.hero_subtitle || ''"
      :items="[{ label: t('nav.vacancies'), to: '/careers' }]"
      variant="navy"
    />

    <div v-if="loading" class="min-h-[40vh] grid place-items-center">
      <UILoader />
    </div>

    <template v-else-if="data">
      <section class="py-20">
        <div class="container-narrow">
          <!-- Filter chips -->
          <div v-if="departments.length" class="flex flex-wrap justify-center gap-2 mb-10">
            <button
              type="button"
              @click="filter = ''"
              :class="['px-4 py-2 rounded-full text-sm font-medium border transition',
                       !filter
                         ? 'bg-primary-700 text-white border-primary-700'
                         : 'border-surface-muted dark:border-slate-700 text-ink-medium dark:text-slate-300 hover:border-primary-500']"
            >{{ t('common.show_more') }}</button>
            <button
              v-for="d in departments"
              :key="d"
              type="button"
              :class="['px-4 py-2 rounded-full text-sm font-medium border transition',
                       filter === d
                         ? 'bg-primary-700 text-white border-primary-700'
                         : 'border-surface-muted dark:border-slate-700 text-ink-medium dark:text-slate-300 hover:border-primary-500']"
              @click="filter = d"
            >{{ d }}</button>
          </div>

          <!-- List -->
          <div v-if="visible.length" class="grid md:grid-cols-2 gap-6">
            <article
              v-for="(v, i) in visible"
              :key="v.id"
              data-animate
              :data-delay="i * 80"
              :class="['rounded-2xl p-6 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-accent-300 dark:hover:border-accent-700 hover:shadow-card-hover transition-all',
                       !v.is_open && 'opacity-60']"
            >
              <div class="flex items-start gap-4">
                <div class="w-12 h-12 rounded-xl bg-primary-50 dark:bg-primary-900/40 grid place-items-center text-primary-700 dark:text-primary-300 flex-shrink-0">
                  <Briefcase class="w-6 h-6" />
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-start justify-between gap-2 mb-1">
                    <h3 class="font-display font-bold text-lg text-ink-dark dark:text-white leading-snug">{{ v.title }}</h3>
                    <span v-if="!v.is_open" class="inline-flex items-center gap-1 text-[10px] font-bold uppercase px-2 py-0.5 rounded-md bg-surface-muted text-ink-faint">
                      <Lock class="w-3 h-3" /> closed
                    </span>
                  </div>
                  <p v-if="v.department" class="text-sm text-ink-light dark:text-slate-400 mb-3">{{ v.department }}</p>

                  <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-[12px] text-ink-medium dark:text-slate-300 mb-3">
                    <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-accent-50 dark:bg-accent-900/30 text-accent-700 dark:text-accent-300 font-semibold">
                      {{ typeLabel(v.employment_type) }}
                    </span>
                    <span v-if="v.location" class="inline-flex items-center gap-1">
                      <MapPin class="w-3 h-3 text-ink-faint" /> {{ v.location }}
                    </span>
                    <span v-if="v.salary" class="text-primary-700 dark:text-accent-400 font-bold">{{ v.salary }}</span>
                  </div>

                  <p v-if="v.description" class="text-[13px] text-ink-light dark:text-slate-400 line-clamp-2 mb-3">{{ v.description }}</p>

                  <div class="flex items-center justify-between pt-3 border-t border-surface-muted dark:border-slate-700">
                    <span v-if="v.posted_at" class="inline-flex items-center gap-1 text-[11px] text-ink-faint">
                      <Calendar class="w-3 h-3" /> {{ fmtDate(v.posted_at) }}
                    </span>
                    <span v-else class="text-[11px] text-ink-faint">&nbsp;</span>
                    <a
                      v-if="v.is_open && (v.apply_url || v.contact_email)"
                      :href="v.apply_url || `mailto:${v.contact_email}`"
                      :target="v.apply_url ? '_blank' : undefined"
                      :rel="v.apply_url ? 'noopener' : undefined"
                      class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary-50 hover:bg-primary-100 dark:bg-slate-700 dark:hover:bg-slate-600 text-primary-800 dark:text-white text-[12px] font-semibold transition"
                    >
                      {{ t('common.apply') }} <ArrowRight class="w-3.5 h-3.5" />
                    </a>
                  </div>
                </div>
              </div>
            </article>
          </div>

          <!-- Empty state -->
          <div v-else class="text-center py-20">
            <Inbox class="w-16 h-16 text-ink-faint mx-auto mb-4" stroke-width="1.4" />
            <h3 class="font-display font-bold text-xl text-ink-dark dark:text-white mb-2">
              {{ page?.empty_title || "Hozircha bo'sh ish o'rni yo'q" }}
            </h3>
            <p v-if="page?.empty_text" class="text-ink-light">{{ page.empty_text }}</p>
          </div>

          <!-- CV CTA -->
          <div v-if="page?.cv_title" class="mt-12 rounded-2xl p-8 text-center bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700" data-animate>
            <h3 class="font-display font-bold text-xl text-ink-dark dark:text-white mb-2">{{ page.cv_title }}</h3>
            <p v-if="page.cv_text" class="text-sm text-ink-light dark:text-slate-400 mb-5 max-w-xl mx-auto">{{ page.cv_text }}</p>
            <a v-if="page.cv_email" :href="`mailto:${page.cv_email}`"
               class="inline-flex items-center gap-2 px-6 py-3 rounded-xl font-bold text-[14px] transition hover:scale-[1.03]"
               style="background: linear-gradient(135deg, #FFB300 0%, #FF8C00 100%); color: #0A0D3D; box-shadow: 0 8px 32px rgba(255,179,0,0.35);">
              <Mail class="w-4 h-4" /> {{ page.cv_email }}
            </a>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>
