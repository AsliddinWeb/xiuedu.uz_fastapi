<script setup>
/**
 * ApplicantsView — fully driven by /api/page-settings/applicants.
 *
 * Sections (in order):
 *   1. PageHero (admin override of title/subtitle)
 *   2. Steps    — 4 numbered cards
 *   3. Forms    — study form cards (kunduzgi/sirtqi/...)
 *   4. Timeline — month-anchored cards
 *   5. Docs     — accordion with bullet items
 *   6. FAQ      — accordion
 *   7. CTA      — orange banner
 */
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { CheckCircle2, ArrowRight, Calendar, Phone, ChevronDown } from 'lucide-vue-next'
import { ArrowTopRightOnSquareIcon } from '@heroicons/vue/24/outline'
import PageHero from '@/components/sections/PageHero.vue'
import UILoader from '@/components/ui/UILoader.vue'
import { PageSettingsAPI } from '@/api/endpoints'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { useSeo } from '@/composables/useSeo'
import { breadcrumbSchema, faqSchema, graph } from '@/utils/schema'
import { resolveIcon } from '@/utils/iconResolver'
import { useLanguageStore } from '@/stores/language'

const { t } = useI18n()
const lang = useLanguageStore()
useScrollAnimation()

const data = ref(null)
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    data.value = await PageSettingsAPI.applicants(lang.currentLang)
  } catch (_) {
    data.value = null
  } finally {
    loading.value = false
  }
}
onMounted(load)
watch(() => lang.currentLang, load)

const page     = computed(() => data.value?.page)
const steps    = computed(() => data.value?.steps || [])
const forms    = computed(() => data.value?.forms || [])
const timeline = computed(() => data.value?.timeline || [])
const docs     = computed(() => data.value?.docs || [])
const faqs     = computed(() => data.value?.faqs || [])

useSeo(() => ({
  title: t('applicants.title'),
  description: t('applicants.subtitle'),
  schema: graph(
    breadcrumbSchema([
      { name: t('nav.home'),         url: '/' },
      { name: t('applicants.title'), url: '/applicants' }
    ]),
    faqSchema(faqs.value.map(f => ({ q: f.question, a: f.answer })))
  )
}))

// Accordion state — open by index
const docsOpen = ref(new Set())
const faqOpen  = ref(new Set([0]))
function toggleDoc(i) {
  docsOpen.value.has(i) ? docsOpen.value.delete(i) : docsOpen.value.add(i)
  docsOpen.value = new Set(docsOpen.value)
}
function toggleFaq(i) {
  faqOpen.value.has(i) ? faqOpen.value.delete(i) : faqOpen.value.add(i)
  faqOpen.value = new Set(faqOpen.value)
}

function ctaTag(external) { return external ? 'a' : 'router-link' }
</script>

<template>
  <div>
    <PageHero
      :title="page?.hero_title || t('applicants.title')"
      :subtitle="page?.hero_subtitle || t('applicants.subtitle')"
      :items="[{ label: t('applicants.title'), to: '/applicants' }]"
      variant="orange"
      align="center"
    />

    <div v-if="loading" class="min-h-[40vh] grid place-items-center">
      <UILoader />
    </div>

    <template v-else-if="data">
      <!-- ═══════════════════════════════════════════════════════
           Steps
      ════════════════════════════════════════════════════════════ -->
      <section v-if="steps.length" class="py-24 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div class="text-center mb-14" data-animate>
            <p v-if="page?.steps_eyebrow" class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">
              {{ page.steps_eyebrow }}
            </p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white tracking-tight">
              {{ page?.steps_title || t('applicants.process') }}
            </h2>
          </div>

          <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
            <div
              v-for="(s, i) in steps"
              :key="s.id"
              data-animate
              :data-delay="i * 100"
              class="relative rounded-2xl p-6 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:shadow-card-hover transition-shadow"
            >
              <div class="absolute -top-3 -right-3 w-10 h-10 rounded-full bg-accent-500 text-white font-display font-extrabold grid place-items-center shadow-button-accent">
                {{ s.number }}
              </div>
              <div class="w-12 h-12 rounded-xl bg-primary-50 dark:bg-primary-900/40 grid place-items-center text-primary-700 dark:text-primary-300 mb-4">
                <component :is="resolveIcon(s.icon)" class="w-6 h-6" />
              </div>
              <h3 class="font-display font-bold text-ink-dark dark:text-white mb-2">{{ s.title }}</h3>
              <p class="text-sm text-ink-light dark:text-slate-400">{{ s.desc }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           Forms
      ════════════════════════════════════════════════════════════ -->
      <section v-if="forms.length" class="py-24 bg-white dark:bg-slate-900">
        <div class="container-narrow">
          <div class="text-center mb-14" data-animate>
            <p v-if="page?.forms_eyebrow" class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">
              {{ page.forms_eyebrow }}
            </p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white tracking-tight">
              {{ page?.forms_title }}
            </h2>
          </div>

          <div class="grid md:grid-cols-2 gap-6">
            <article
              v-for="(f, i) in forms"
              :key="f.id"
              data-animate
              :data-delay="i * 100"
              class="rounded-2xl p-8 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-accent-300 dark:hover:border-accent-700 hover:shadow-card-hover transition-all"
            >
              <h3 class="font-display font-bold text-2xl text-ink-dark dark:text-white mb-3">{{ f.title }}</h3>
              <p class="text-ink-light dark:text-slate-400 mb-5">{{ f.desc }}</p>
              <ul v-if="f.features.length" class="space-y-2 mb-6">
                <li v-for="x in f.features" :key="x" class="flex items-center gap-2 text-sm text-ink-medium dark:text-slate-300">
                  <CheckCircle2 class="w-4 h-4 text-accent-500 flex-shrink-0" /> {{ x }}
                </li>
              </ul>
              <RouterLink
                v-if="f.cta_url"
                :to="f.cta_url"
                class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary-50 hover:bg-primary-100 text-primary-800 dark:bg-slate-700 dark:hover:bg-slate-600 dark:text-white text-[13px] font-semibold transition"
              >
                {{ f.cta_label || t('common.read_more') }} <ArrowRight class="w-4 h-4" />
              </RouterLink>
            </article>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           Timeline
      ════════════════════════════════════════════════════════════ -->
      <section v-if="timeline.length" class="py-24 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div class="text-center mb-14" data-animate>
            <p v-if="page?.timeline_eyebrow" class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">
              {{ page.timeline_eyebrow }}
            </p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white tracking-tight">
              {{ page?.timeline_title }}
            </h2>
          </div>

          <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
            <div
              v-for="(item, i) in timeline"
              :key="item.id"
              data-animate
              :data-delay="i * 100"
              class="rounded-2xl p-6 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 text-center"
            >
              <div class="w-14 h-14 mx-auto mb-3 rounded-2xl bg-accent-50 dark:bg-accent-900/30 grid place-items-center">
                <Calendar class="w-7 h-7 text-accent-600" />
              </div>
              <div class="font-display font-extrabold text-2xl text-primary-700 dark:text-primary-300">{{ item.month }}</div>
              <p class="text-xs text-ink-light dark:text-slate-400 mt-2">{{ item.text }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           Documents accordion
      ════════════════════════════════════════════════════════════ -->
      <section v-if="docs.length" class="py-24 bg-white dark:bg-slate-900">
        <div class="container-narrow max-w-3xl">
          <div class="text-center mb-12" data-animate>
            <p v-if="page?.docs_eyebrow" class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">
              {{ page.docs_eyebrow }}
            </p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white tracking-tight">
              {{ page?.docs_title || t('applicants.documents') }}
            </h2>
          </div>

          <div class="space-y-3" data-animate>
            <div
              v-for="(d, i) in docs"
              :key="d.id"
              class="border border-surface-muted dark:border-slate-700 rounded-xl overflow-hidden bg-white dark:bg-slate-800"
            >
              <button
                type="button"
                @click="toggleDoc(i)"
                :aria-expanded="docsOpen.has(i)"
                class="w-full flex items-center justify-between gap-4 px-6 py-5 text-left hover:bg-surface-light dark:hover:bg-slate-800/80 transition-colors"
              >
                <span class="text-[15px] font-semibold text-ink-dark dark:text-white">{{ d.title }}</span>
                <ChevronDown :class="['w-5 h-5 text-ink-faint flex-shrink-0 transition-transform duration-200', docsOpen.has(i) && 'rotate-180']" />
              </button>
              <div v-show="docsOpen.has(i)" class="px-6 pb-5 border-t border-surface-muted dark:border-slate-700 pt-4">
                <ul class="space-y-2 text-sm text-ink-medium dark:text-slate-300">
                  <li v-for="(item, j) in d.items" :key="j" class="flex items-start gap-2">
                    <span class="text-accent-500 mt-0.5">•</span>
                    <span>{{ item }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           FAQ
      ════════════════════════════════════════════════════════════ -->
      <section v-if="faqs.length" class="py-24 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow max-w-3xl">
          <div class="text-center mb-12" data-animate>
            <p v-if="page?.faq_eyebrow" class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">
              {{ page.faq_eyebrow }}
            </p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white tracking-tight">
              {{ page?.faq_title }}
            </h2>
          </div>

          <div class="space-y-3" data-animate>
            <div
              v-for="(f, i) in faqs"
              :key="f.id"
              class="border border-surface-muted dark:border-slate-700 rounded-xl overflow-hidden bg-white dark:bg-slate-800"
            >
              <button
                type="button"
                @click="toggleFaq(i)"
                :aria-expanded="faqOpen.has(i)"
                class="w-full flex items-center justify-between gap-4 px-6 py-5 text-left hover:bg-surface-light dark:hover:bg-slate-800/80 transition-colors"
              >
                <span class="text-[15px] font-semibold text-ink-dark dark:text-white">{{ f.question }}</span>
                <ChevronDown :class="['w-5 h-5 text-ink-faint flex-shrink-0 transition-transform duration-200', faqOpen.has(i) && 'rotate-180']" />
              </button>
              <div v-show="faqOpen.has(i)" class="px-6 pb-5 text-[14px] text-ink-light dark:text-slate-400 leading-relaxed border-t border-surface-muted dark:border-slate-700 pt-4">
                {{ f.answer }}
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           CTA
      ════════════════════════════════════════════════════════════ -->
      <section v-if="page?.cta_title" class="py-20 bg-gradient-to-br from-accent-600 via-accent-500 to-accent-400 text-white relative overflow-hidden">
        <div class="absolute inset-0 opacity-[0.06]" style="background-image: radial-gradient(circle at 30% 30%, white 1px, transparent 1px); background-size: 32px 32px;" />
        <div class="container-narrow relative text-center">
          <h2 class="text-3xl md:text-4xl lg:text-5xl font-display font-bold mb-4">{{ page.cta_title }}</h2>
          <p v-if="page.cta_text" class="text-white/90 max-w-xl mx-auto mb-8">{{ page.cta_text }}</p>
          <div class="flex flex-wrap justify-center gap-3">
            <component
              v-if="page.cta_primary_label && page.cta_primary_url"
              :is="ctaTag(page.cta_primary_external)"
              :to="!page.cta_primary_external ? page.cta_primary_url : undefined"
              :href="page.cta_primary_external ? page.cta_primary_url : undefined"
              :target="page.cta_primary_external ? '_blank' : undefined"
              :rel="page.cta_primary_external ? 'noopener' : undefined"
              class="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-white text-accent-700 hover:bg-accent-50 font-bold text-[15px] transition"
            >
              {{ page.cta_primary_label }}
              <ArrowTopRightOnSquareIcon class="w-4 h-4" />
            </component>
            <a
              v-if="page.cta_phone_label"
              :href="`tel:${page.cta_phone_url || page.cta_phone_label}`"
              class="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl border-2 border-white text-white hover:bg-white/10 font-bold text-[15px] transition"
            >
              <Phone class="w-4 h-4" /> {{ page.cta_phone_label }}
            </a>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>
