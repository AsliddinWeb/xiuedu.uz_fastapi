<script setup>
/**
 * StructureView — fully driven by /api/page-settings/structure.
 *
 * Combines:
 *   - top management (rector + prorectors from Leader DB)
 *   - faculties (from Faculty DB, programs_count)
 *   - admin departments (own model)
 *   - support services (own model)
 *   - all section titles + bottom CTA from StructurePage singleton
 */
import { ref, computed, onMounted, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { UserCircleIcon, BriefcaseIcon, BeakerIcon, GlobeAltIcon } from '@heroicons/vue/24/outline'
import PageHero from '@/components/sections/PageHero.vue'
import UILoader from '@/components/ui/UILoader.vue'
import { PageSettingsAPI } from '@/api/endpoints'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { useSeo } from '@/composables/useSeo'
import { breadcrumbSchema, graph } from '@/utils/schema'
import { resolveIcon } from '@/utils/iconResolver'
import { useLanguageStore } from '@/stores/language'

const { t } = useI18n()
const lang = useLanguageStore()
useScrollAnimation()
useSeo(() => ({
  title: t('structure.title'),
  description: t('structure.subtitle'),
  type: 'website',
  schema: graph(breadcrumbSchema([
    { name: t('nav.home'),        url: '/' },
    { name: t('structure.title'), url: '/structure' }
  ]))
}))

const data = ref(null)
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    data.value = await PageSettingsAPI.structure(lang.currentLang)
  } catch (_) {
    data.value = null
  } finally {
    loading.value = false
  }
}
onMounted(load)
watch(() => lang.currentLang, load)

const page        = computed(() => data.value?.page)
const rector      = computed(() => data.value?.rector)
const prorectors  = computed(() => data.value?.prorectors || [])
const faculties   = computed(() => data.value?.faculties || [])
const departments = computed(() => data.value?.departments || [])
const services    = computed(() => data.value?.services || [])

// Pick a fallback icon for prorectors based on position keyword
function prorectorIcon(p) {
  const pos = (p.position || '').toLowerCase()
  if (pos.includes('xalqaro') || pos.includes('international') || pos.includes('международ')) return GlobeAltIcon
  if (pos.includes('ilm') || pos.includes('research') || pos.includes('научн')) return BeakerIcon
  return BriefcaseIcon
}
</script>

<template>
  <div>
    <PageHero
      :title="page?.hero_title || t('structure.title')"
      :subtitle="page?.hero_subtitle || t('structure.subtitle')"
      :items="[{ label: t('structure.title'), to: '/structure' }]"
    />

    <div v-if="loading" class="min-h-[40vh] grid place-items-center">
      <UILoader />
    </div>

    <template v-else-if="data">
      <!-- ═══════════════════════════════════════════════════════
           Top management — rector + prorectors
      ════════════════════════════════════════════════════════════ -->
      <section v-if="rector || prorectors.length" class="py-20 lg:py-24">
        <div class="container-narrow">
          <div data-animate class="text-center max-w-2xl mx-auto mb-14">
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">
              {{ page?.top_eyebrow || t('structure.eyebrow_top') }}
            </p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white tracking-tight">
              {{ page?.top_title || t('structure.title_top') }}
            </h2>
          </div>

          <div class="relative">
            <!-- Rector card centered -->
            <div v-if="rector" data-animate class="flex justify-center mb-12">
              <div class="relative w-full max-w-md">
                <div
                  class="relative rounded-3xl p-7 text-white shadow-[0_30px_80px_rgba(10,13,61,0.25)] overflow-hidden"
                  style="background: linear-gradient(135deg, #0A0D3D 0%, #1A1F6E 50%, #2D3A8C 100%);"
                >
                  <div class="absolute inset-0 opacity-[0.08] pointer-events-none"
                       style="background-image: radial-gradient(circle, white 1px, transparent 1px); background-size: 24px 24px;" />
                  <div class="relative flex items-center gap-5">
                    <div v-if="rector.photo" class="w-16 h-16 rounded-2xl overflow-hidden flex-shrink-0 ring-2 ring-white/20">
                      <img :src="rector.photo" :alt="rector.name" class="w-full h-full object-cover" />
                    </div>
                    <div v-else class="w-16 h-16 rounded-2xl bg-white/15 backdrop-blur grid place-items-center flex-shrink-0">
                      <UserCircleIcon class="w-9 h-9 text-accent-400" stroke-width="1.6" />
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-[10px] uppercase tracking-[0.2em] text-accent-300 mb-1 font-bold">{{ rector.position }}</p>
                      <h3 class="text-xl font-display font-bold leading-tight">{{ rector.name }}</h3>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Connector lines (desktop only) -->
            <div v-if="rector && prorectors.length" class="hidden lg:block relative mb-8">
              <div class="absolute left-1/2 -top-12 w-px h-12 bg-gradient-to-b from-primary-300 to-transparent" />
              <div class="absolute left-[16.66%] right-[16.66%] top-0 h-px bg-primary-300" />
            </div>

            <!-- Prorectors row -->
            <div v-if="prorectors.length" class="grid sm:grid-cols-3 gap-5">
              <div
                v-for="(p, i) in prorectors"
                :key="p.id"
                data-animate
                :data-delay="i * 80"
                class="relative rounded-2xl p-6 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-primary-300 dark:hover:border-primary-600 hover:shadow-[0_18px_44px_rgba(10,13,61,0.10)] transition-all duration-300"
              >
                <div class="hidden lg:block absolute left-1/2 -top-8 w-px h-8 bg-primary-300 -translate-x-1/2" />
                <div class="hidden lg:block absolute left-1/2 -top-1 w-2 h-2 rounded-full bg-primary-500 ring-4 ring-white dark:ring-slate-900 -translate-x-1/2" />

                <div v-if="p.photo" class="w-12 h-12 rounded-xl overflow-hidden mb-4 ring-1 ring-surface-muted">
                  <img :src="p.photo" :alt="p.name" class="w-full h-full object-cover" />
                </div>
                <div v-else class="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-700 to-primary-900 grid place-items-center text-white shadow-md mb-4">
                  <component :is="prorectorIcon(p)" class="w-6 h-6" stroke-width="1.7" />
                </div>
                <p class="text-[11px] uppercase tracking-wider text-accent-600 font-bold mb-2">{{ p.position }}</p>
                <h4 class="text-base font-display font-bold text-ink-dark dark:text-white">{{ p.name }}</h4>
              </div>
            </div>
          </div>

          <div class="mt-12 text-center" data-animate>
            <RouterLink
              to="/leadership"
              class="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-primary-50 hover:bg-primary-100 dark:bg-slate-800 dark:hover:bg-slate-700 text-primary-800 dark:text-white text-[13px] font-bold transition-colors"
            >
              {{ t('structure.full_leadership') }} →
            </RouterLink>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           Faculties (academic units)
      ════════════════════════════════════════════════════════════ -->
      <section v-if="faculties.length" class="py-20 lg:py-24 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div data-animate class="text-center max-w-2xl mx-auto mb-14">
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">
              {{ page?.academic_eyebrow || t('structure.eyebrow_academic') }}
            </p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white tracking-tight">
              {{ page?.academic_title || t('structure.title_academic') }}
            </h2>
            <p v-if="page?.academic_lead" class="mt-3 text-[15px] text-ink-light dark:text-slate-400">
              {{ page.academic_lead }}
            </p>
          </div>

          <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <RouterLink
              v-for="(f, i) in faculties"
              :key="f.slug"
              :to="`/faculties/${f.slug}`"
              data-animate
              :data-delay="i * 60"
              class="group rounded-2xl p-6 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-accent-300 dark:hover:border-accent-700 hover:shadow-[0_18px_44px_rgba(10,13,61,0.10)] hover:-translate-y-0.5 transition-all duration-300"
            >
              <div class="flex items-start gap-4 mb-4">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-50 to-primary-100 dark:from-slate-700 dark:to-slate-700 grid place-items-center text-primary-700 dark:text-primary-300 shadow-sm flex-shrink-0">
                  <component :is="resolveIcon(f.icon)" class="w-6 h-6" stroke-width="1.6" />
                </div>
                <div class="flex-1 min-w-0">
                  <h3 class="text-base font-display font-bold text-ink-dark dark:text-white leading-tight group-hover:text-primary-700 dark:group-hover:text-primary-300 transition-colors">
                    {{ f.name }}
                  </h3>
                </div>
              </div>
              <div class="pt-4 border-t border-surface-muted dark:border-slate-700">
                <div class="text-xl font-display font-extrabold text-primary-800 dark:text-accent-400">{{ f.programs_count }}</div>
                <div class="text-[10px] uppercase tracking-wider text-ink-faint font-semibold mt-0.5">
                  {{ t('structure.programs') }}
                </div>
              </div>
            </RouterLink>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           Administrative departments
      ════════════════════════════════════════════════════════════ -->
      <section v-if="departments.length" class="py-20 lg:py-24">
        <div class="container-narrow">
          <div data-animate class="text-center max-w-2xl mx-auto mb-14">
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">
              {{ page?.admin_eyebrow || t('structure.eyebrow_admin') }}
            </p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white tracking-tight">
              {{ page?.admin_title || t('structure.title_admin') }}
            </h2>
            <p v-if="page?.admin_lead" class="mt-3 text-[15px] text-ink-light dark:text-slate-400">
              {{ page.admin_lead }}
            </p>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
            <div
              v-for="(d, i) in departments"
              :key="d.id"
              data-animate
              :data-delay="i * 40"
              class="group flex flex-col items-center text-center px-4 py-5 rounded-xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-primary-300 dark:hover:border-primary-600 hover:shadow-md transition-all"
            >
              <div class="w-11 h-11 rounded-xl bg-primary-50 dark:bg-slate-700 grid place-items-center text-primary-700 dark:text-primary-300 mb-3 group-hover:scale-110 transition-transform">
                <component :is="resolveIcon(d.icon)" class="w-5 h-5" stroke-width="1.8" />
              </div>
              <p class="text-[12px] font-semibold text-ink-dark dark:text-white leading-snug">{{ d.name }}</p>
              <p v-if="d.head" class="text-[10px] text-ink-faint mt-1 line-clamp-1">{{ d.head }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           Support services
      ════════════════════════════════════════════════════════════ -->
      <section v-if="services.length" class="py-20 lg:py-24 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div data-animate class="text-center max-w-2xl mx-auto mb-14">
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">
              {{ page?.services_eyebrow || t('structure.eyebrow_services') }}
            </p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white tracking-tight">
              {{ page?.services_title || t('structure.title_services') }}
            </h2>
            <p v-if="page?.services_lead" class="mt-3 text-[15px] text-ink-light dark:text-slate-400">
              {{ page.services_lead }}
            </p>
          </div>

          <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <article
              v-for="(s, i) in services"
              :key="s.id"
              data-animate
              :data-delay="i * 60"
              class="rounded-2xl p-6 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-accent-300 dark:hover:border-accent-700 hover:shadow-[0_18px_44px_rgba(10,13,61,0.10)] transition-all duration-300"
            >
              <div class="flex items-start gap-4">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-accent-400 to-accent-600 grid place-items-center text-primary-900 shadow-md flex-shrink-0">
                  <component :is="resolveIcon(s.icon)" class="w-6 h-6" stroke-width="1.7" />
                </div>
                <div class="flex-1">
                  <h3 class="text-base font-display font-bold text-ink-dark dark:text-white leading-tight mb-2">{{ s.name }}</h3>
                  <p class="text-[13px] text-ink-light dark:text-slate-400 leading-relaxed">{{ s.desc }}</p>
                </div>
              </div>
            </article>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           Bottom CTA
      ════════════════════════════════════════════════════════════ -->
      <section v-if="page?.cta_title" class="py-20">
        <div class="container-narrow">
          <div
            data-animate
            class="rounded-3xl p-10 lg:p-14 text-center text-white relative overflow-hidden"
            style="background: linear-gradient(135deg, #0A0D3D 0%, #1A1F6E 60%, #2D3A8C 100%);"
          >
            <div class="absolute inset-0 opacity-[0.06] pointer-events-none"
                 style="background-image: radial-gradient(circle, white 1px, transparent 1px); background-size: 28px 28px;" />
            <div class="relative max-w-xl mx-auto">
              <h3 class="text-2xl md:text-3xl font-display font-bold mb-3">{{ page.cta_title }}</h3>
              <p v-if="page.cta_text" class="text-white/70 text-[15px] mb-7">{{ page.cta_text }}</p>
              <div class="flex flex-wrap items-center justify-center gap-3">
                <RouterLink
                  v-if="page.cta_primary_url"
                  :to="page.cta_primary_url"
                  class="inline-flex items-center gap-2 px-6 py-3 rounded-xl font-bold text-[14px] transition hover:scale-[1.02]"
                  style="background: linear-gradient(135deg, #FFB300 0%, #FF8C00 100%); color: #0A0D3D;"
                >
                  {{ page.cta_primary_label }}
                </RouterLink>
                <RouterLink
                  v-if="page.cta_secondary_url"
                  :to="page.cta_secondary_url"
                  class="inline-flex items-center gap-2 px-6 py-3 rounded-xl font-semibold text-[14px] text-white border border-white/20 hover:bg-white/[0.06] transition"
                >
                  {{ page.cta_secondary_label }}
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>
