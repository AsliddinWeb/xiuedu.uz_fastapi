<script setup>
/**
 * Shared component used by BachelorView & MasterView.
 *
 * Loads all faculties from DB, then flatMaps their programs
 * and filters by `level` prop. Shows a professional table + sidebar.
 * All data comes from the CMS (FacultyProgram model).
 */
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import {
  ArrowRight, CheckCircle2, FileText, GraduationCap
} from 'lucide-vue-next'
import PageHero from '@/components/sections/PageHero.vue'
import ProgramCard from '@/components/cards/ProgramCard.vue'
import UILoader from '@/components/ui/UILoader.vue'
import UIButton from '@/components/ui/UIButton.vue'
import { FacultiesAPI } from '@/api/endpoints'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { useSeo } from '@/composables/useSeo'
import { breadcrumbSchema } from '@/utils/schema'
import { resolveIcon } from '@/utils/iconResolver'
import { useLanguageStore } from '@/stores/language'

const props = defineProps({
  level: { type: String, required: true } // 'bachelor' | 'master' | 'short' | 'phd'
})

const { t } = useI18n()
const lang = useLanguageStore()
useScrollAnimation()

const faculties = ref([])
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    faculties.value = await FacultiesAPI.list(lang.currentLang)
  } catch (_) {
    faculties.value = []
  } finally {
    loading.value = false
  }
}
onMounted(load)
watch(() => lang.currentLang, load)

// Flatten all programs from all faculties, filter by level
const programs = computed(() => {
  const all = []
  for (const f of faculties.value) {
    for (const p of (f.programs || [])) {
      if (p.level === props.level) {
        all.push({ ...p, faculty_name: f.name, faculty_slug: f.slug, faculty_icon: f.icon })
      }
    }
  }
  return all
})

// Group by faculty for the table view
const groupedByFaculty = computed(() => {
  const map = new Map()
  for (const p of programs.value) {
    if (!map.has(p.faculty_slug)) {
      map.set(p.faculty_slug, { name: p.faculty_name, slug: p.faculty_slug, icon: p.faculty_icon, items: [] })
    }
    map.get(p.faculty_slug).items.push(p)
  }
  return [...map.values()]
})

const levelMeta = computed(() => {
  switch (props.level) {
    case 'master':
      return {
        title: t('home.level_master'),
        subtitle: t('home.level_master') + ' — ' + t('home.academic_lead'),
        heroVariant: 'navy'
      }
    case 'short':
      return { title: t('home.level_short'), subtitle: '', heroVariant: 'navy' }
    case 'phd':
      return { title: t('home.level_phd'), subtitle: '', heroVariant: 'navy' }
    default:
      return {
        title: t('home.level_bachelor'),
        subtitle: t('home.level_bachelor') + ' — ' + t('home.academic_lead'),
        heroVariant: 'navy'
      }
  }
})

useSeo(() => ({
  title: levelMeta.value.title,
  description: levelMeta.value.subtitle,
  schema: breadcrumbSchema([
    { name: t('nav.home'),        url: '/' },
    { name: t('nav.education'),   url: '/faculties' },
    { name: levelMeta.value.title, url: `/education/${props.level}` }
  ])
}))
</script>

<template>
  <div>
    <PageHero
      :title="levelMeta.title"
      :subtitle="levelMeta.subtitle"
      :items="[
        { label: t('nav.education'), to: '/faculties' },
        { label: levelMeta.title, to: `/education/${level}` }
      ]"
      variant="navy"
    />

    <div v-if="loading" class="min-h-[40vh] grid place-items-center">
      <UILoader />
    </div>

    <template v-else>
      <!-- Stats strip -->
      <section v-if="programs.length" class="py-12 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow grid grid-cols-3 gap-6 text-center">
          <div data-animate>
            <div class="text-4xl font-display font-extrabold text-primary-700 dark:text-primary-300">{{ programs.length }}</div>
            <div class="text-sm text-ink-light mt-1">{{ t('faculties.programs') }}</div>
          </div>
          <div data-animate data-delay="80">
            <div class="text-4xl font-display font-extrabold text-primary-700 dark:text-primary-300">{{ groupedByFaculty.length }}</div>
            <div class="text-sm text-ink-light mt-1">{{ t('nav.faculties') }}</div>
          </div>
          <div data-animate data-delay="160">
            <div class="text-4xl font-display font-extrabold text-primary-700 dark:text-primary-300">
              {{ programs.reduce((s, p) => s + (p.credits || 0), 0) / programs.length || 0 }}
            </div>
            <div class="text-sm text-ink-light mt-1">{{ t('home.program_credits') }} (o'rtacha)</div>
          </div>
        </div>
      </section>

      <!-- Programs grouped by faculty -->
      <section class="py-24">
        <div class="container-narrow">
          <div v-if="!programs.length" class="text-center py-20">
            <GraduationCap class="w-16 h-16 mx-auto text-ink-faint mb-4" stroke-width="1.4" />
            <p class="text-ink-light">{{ t('common.not_found') }}</p>
          </div>

          <div v-else class="space-y-16">
            <div v-for="(group, gi) in groupedByFaculty" :key="group.slug" data-animate :data-delay="gi * 80">
              <!-- Faculty header -->
              <div class="flex items-center gap-4 mb-8">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-700 to-primary-900 grid place-items-center text-white shadow-md flex-shrink-0">
                  <component :is="resolveIcon(group.icon)" class="w-6 h-6" stroke-width="1.6" />
                </div>
                <div>
                  <h2 class="text-xl font-display font-bold text-ink-dark dark:text-white">{{ group.name }}</h2>
                  <RouterLink :to="`/faculties/${group.slug}`" class="text-[12px] font-semibold text-primary-700 dark:text-primary-300 hover:text-accent-600 inline-flex items-center gap-1">
                    {{ t('home.fac_open') }} <ArrowRight class="w-3 h-3" />
                  </RouterLink>
                </div>
              </div>

              <!-- Program cards -->
              <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
                <div v-for="(p, i) in group.items" :key="p.id" data-animate :data-delay="i * 50">
                  <ProgramCard :program="p" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA -->
      <section class="py-20 bg-surface-light dark:bg-slate-800/40 border-t border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div class="grid lg:grid-cols-[1fr_20rem] gap-10 items-start">
            <div data-animate>
              <h2 class="text-2xl md:text-3xl font-display font-bold text-ink-dark dark:text-white mb-3">
                {{ levelMeta.title }} {{ t('home.cta_apply') }}
              </h2>
              <p class="text-[15px] text-ink-light dark:text-slate-400 mb-6 max-w-xl">
                {{ t('home.final_cta_text') }}
              </p>
              <div class="flex flex-wrap gap-3">
                <a href="https://qabul.xiuedu.uz" target="_blank" rel="noopener"
                   class="inline-flex items-center gap-2 px-6 py-3 rounded-xl font-bold text-[14px] transition hover:scale-[1.02]"
                   style="background: linear-gradient(135deg, #FFB300 0%, #FF8C00 100%); color: #0A0D3D;">
                  {{ t('home.cta_apply') }} <ArrowRight class="w-4 h-4" />
                </a>
                <RouterLink to="/applicants" class="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-primary-50 hover:bg-primary-100 dark:bg-slate-700 dark:hover:bg-slate-600 text-primary-800 dark:text-white text-[14px] font-semibold transition">
                  {{ t('applicants.title') }}
                </RouterLink>
              </div>
            </div>
            <aside data-animate data-delay="200">
              <div class="rounded-2xl p-6 text-white sticky top-24"
                   style="background: linear-gradient(135deg, #0A0D3D 0%, #1A1F6E 100%);">
                <FileText class="w-10 h-10 text-accent-400 mb-4" stroke-width="1.5" />
                <h3 class="font-display text-lg font-bold mb-3">{{ t('applicants.documents') }}</h3>
                <ul class="space-y-2 text-sm text-white/80 mb-6">
                  <li class="flex gap-2"><CheckCircle2 class="w-4 h-4 text-accent-400 flex-shrink-0 mt-0.5" /> {{ t('common.apply') }}</li>
                </ul>
                <UIButton variant="accent" block to="/applicants">
                  {{ t('applicants.title') }}
                  <template #icon-right><ArrowRight class="w-4 h-4" /></template>
                </UIButton>
              </div>
            </aside>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>
