<script setup>
/**
 * InternationalView — fully driven by /api/page-settings/international.
 */
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { Globe2, Mail, Phone } from 'lucide-vue-next'
import PageHero from '@/components/sections/PageHero.vue'
import UILoader from '@/components/ui/UILoader.vue'
import { PageSettingsAPI } from '@/api/endpoints'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { useSeo } from '@/composables/useSeo'
import { breadcrumbSchema } from '@/utils/schema'
import { resolveIcon } from '@/utils/iconResolver'
import { useLanguageStore } from '@/stores/language'

const { t } = useI18n()
const lang = useLanguageStore()
useScrollAnimation()
useSeo(() => ({
  title: t('nav.international'),
  schema: breadcrumbSchema([
    { name: t('nav.home'),          url: '/' },
    { name: t('nav.international'), url: '/international' }
  ])
}))

const data = ref(null)
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    data.value = await PageSettingsAPI.international(lang.currentLang)
  } catch (_) {
    data.value = null
  } finally {
    loading.value = false
  }
}
onMounted(load)
watch(() => lang.currentLang, load)

const page     = computed(() => data.value?.page)
const programs = computed(() => data.value?.programs || [])
const partners = computed(() => data.value?.partners || [])
const stats    = computed(() => (page.value?.stats || []).filter(s => s.value))
</script>

<template>
  <div>
    <PageHero
      :title="page?.hero_title || t('nav.international')"
      :subtitle="page?.hero_subtitle || ''"
      :items="[{ label: t('nav.international'), to: '/international' }]"
      variant="navy"
    />

    <div v-if="loading" class="min-h-[40vh] grid place-items-center">
      <UILoader />
    </div>

    <template v-else-if="data">
      <!-- Stats -->
      <section v-if="stats.length" class="py-12 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div
              v-for="(s, i) in stats"
              :key="i"
              data-animate
              :data-delay="i * 80"
              class="text-center"
            >
              <div class="text-4xl md:text-5xl font-display font-extrabold text-primary-700 dark:text-primary-300">{{ s.value }}</div>
              <div class="text-sm text-ink-light dark:text-slate-400 mt-2">{{ s.label }}</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Programs -->
      <section v-if="programs.length" class="py-24">
        <div class="container-narrow">
          <div class="text-center max-w-2xl mx-auto mb-14" data-animate>
            <p v-if="page?.programs_eyebrow" class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">
              {{ page.programs_eyebrow }}
            </p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white tracking-tight">
              {{ page?.programs_title }}
            </h2>
          </div>
          <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
            <article
              v-for="(p, i) in programs"
              :key="p.id"
              data-animate
              :data-delay="i * 80"
              class="rounded-2xl p-6 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-accent-300 dark:hover:border-accent-700 hover:shadow-card-hover transition-all"
            >
              <div class="w-12 h-12 rounded-xl bg-accent-50 dark:bg-accent-900/40 grid place-items-center text-accent-600 dark:text-accent-300 mb-4">
                <component :is="resolveIcon(p.icon)" class="w-6 h-6" stroke-width="1.7" />
              </div>
              <h3 class="font-display font-bold text-ink-dark dark:text-white mb-2">{{ p.title }}</h3>
              <p class="text-sm text-ink-light dark:text-slate-400 leading-relaxed">{{ p.desc }}</p>
            </article>
          </div>
        </div>
      </section>

      <!-- Partners -->
      <section v-if="partners.length" class="py-24 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div class="text-center max-w-2xl mx-auto mb-14" data-animate>
            <p v-if="page?.partners_eyebrow" class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">
              {{ page.partners_eyebrow }}
            </p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white tracking-tight">
              {{ page?.partners_title }}
            </h2>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
            <component
              v-for="(p, i) in partners"
              :is="p.url ? 'a' : 'div'"
              :key="p.id"
              :href="p.url || undefined"
              :target="p.url ? '_blank' : undefined"
              :rel="p.url ? 'noopener' : undefined"
              data-animate
              :data-delay="(i % 8) * 60"
              class="rounded-2xl p-5 text-center bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-accent-300 dark:hover:border-accent-700 hover:shadow-card-hover hover:-translate-y-0.5 transition-all"
            >
              <img v-if="p.logo_url" :src="p.logo_url" :alt="p.name" class="h-10 mx-auto mb-3 object-contain" />
              <div v-else class="text-3xl mb-3">{{ p.flag }}</div>
              <div class="font-display font-semibold text-sm text-ink-dark dark:text-white">{{ p.name }}</div>
              <div v-if="p.country_code" class="text-[10px] uppercase tracking-wider text-ink-faint mt-1">{{ p.country_code }}</div>
            </component>
          </div>
        </div>
      </section>

      <!-- Contact CTA -->
      <section v-if="page?.cta_title" class="py-24">
        <div class="container-narrow max-w-3xl">
          <div data-animate class="rounded-3xl p-10 text-center bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 shadow-card">
            <Globe2 class="w-12 h-12 text-accent-500 mx-auto mb-5" stroke-width="1.4" />
            <h2 class="text-2xl md:text-3xl font-display font-bold text-ink-dark dark:text-white mb-3">{{ page.cta_title }}</h2>
            <p v-if="page.cta_text" class="text-ink-light dark:text-slate-400 mb-6">{{ page.cta_text }}</p>
            <div class="flex flex-wrap justify-center gap-3">
              <a v-if="page.cta_email" :href="`mailto:${page.cta_email}`"
                 class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary-50 hover:bg-primary-100 text-primary-800 dark:bg-slate-700 dark:hover:bg-slate-600 dark:text-white text-[14px] font-semibold transition">
                <Mail class="w-4 h-4" /> {{ page.cta_email }}
              </a>
              <a v-if="page.cta_phone_label" :href="`tel:${page.cta_phone_url || page.cta_phone_label}`"
                 class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-surface-soft hover:bg-surface-muted text-ink-medium dark:bg-slate-700 dark:hover:bg-slate-600 dark:text-slate-300 text-[14px] font-semibold transition">
                <Phone class="w-4 h-4" /> {{ page.cta_phone_label }}
              </a>
            </div>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>
