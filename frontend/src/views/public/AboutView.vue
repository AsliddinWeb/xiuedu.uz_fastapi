<script setup>
/**
 * AboutView — fully driven by /api/page-settings/about.
 *
 * Sections:
 *   1. PageHero (with admin override)
 *   2. Rector welcome (photo + multi-paragraph letter)
 *   3. Mission / Vision / Values
 *   4. History timeline
 *   5. Accreditation grid
 *   6. Address + map
 */
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import PageHero from '@/components/sections/PageHero.vue'
import UILoader from '@/components/ui/UILoader.vue'
import {
  Target, Eye, Heart, Award, MapPin, Mail, GraduationCap
} from 'lucide-vue-next'
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
  title: t('about.title'),
  description: t('about.subtitle'),
  schema: breadcrumbSchema([
    { name: t('nav.home'),    url: '/' },
    { name: t('about.title'), url: '/about' }
  ])
}))

const data = ref(null)
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    data.value = await PageSettingsAPI.about(lang.currentLang)
  } catch (_) {
    data.value = null
  } finally {
    loading.value = false
  }
}
onMounted(load)
watch(() => lang.currentLang, load)

const page           = computed(() => data.value?.page)
const timeline       = computed(() => data.value?.timeline || [])
const accreditations = computed(() => data.value?.accreditations || [])

// MVV cards built from page fields
const mvvCards = computed(() => {
  if (!page.value) return []
  return [
    { icon: Target, key: 'mission', title: t('about.mission'), text: page.value.mission, color: 'from-primary-700 to-primary-900' },
    { icon: Eye,    key: 'vision',  title: t('about.vision'),  text: page.value.vision,  color: 'from-accent-500 to-accent-700' },
    { icon: Heart,  key: 'values',  title: t('about.values'),  text: page.value.values,  color: 'from-emerald-600 to-primary-800' }
  ]
})
</script>

<template>
  <div>
    <PageHero
      :title="page?.hero_title || t('about.title')"
      :subtitle="page?.hero_subtitle || t('about.subtitle')"
      :items="[{ label: t('about.title'), to: '/about' }]"
      variant="navy"
    />

    <!-- Loading -->
    <div v-if="loading" class="min-h-[40vh] grid place-items-center">
      <UILoader />
    </div>

    <template v-else-if="page">
      <!-- ═══════════════════════════════════════════════════════
           Rector welcome
      ════════════════════════════════════════════════════════════ -->
      <section v-if="page.rector_letter_paragraphs.length" class="py-24 lg:py-32 bg-white dark:bg-slate-900">
        <div class="container-narrow">
          <div class="grid lg:grid-cols-[1fr_1.4fr] gap-12 lg:gap-20 items-center">
            <!-- Portrait -->
            <div v-if="page.rector_image" class="relative max-w-[380px] mx-auto lg:mx-0" data-animate>
              <div class="absolute -inset-3 rounded-3xl"
                   style="background: linear-gradient(135deg, #FFB300 0%, #FFD74D 100%); opacity: 0.15;" />
              <div class="relative aspect-[4/5] rounded-2xl overflow-hidden bg-surface-soft dark:bg-slate-800">
                <img :src="page.rector_image" :alt="page.rector_name || ''" loading="lazy" class="w-full h-full object-cover" />
              </div>
              <div class="absolute -bottom-5 left-1/2 -translate-x-1/2 w-[85%] bg-white dark:bg-slate-800 rounded-xl px-5 py-3.5 shadow-card-hover border border-surface-muted dark:border-slate-700">
                <p v-if="page.rector_role" class="text-xs text-ink-faint">{{ page.rector_role }}</p>
                <p class="text-base font-display font-bold text-ink-dark dark:text-white tracking-tight">{{ page.rector_name }}</p>
                <p v-if="page.rector_degree" class="text-[11px] text-ink-light mt-0.5">{{ page.rector_degree }}</p>
              </div>
            </div>

            <!-- Letter -->
            <div data-animate data-delay="150">
              <p v-if="page.rector_letter_eyebrow" class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-4">
                {{ page.rector_letter_eyebrow }}
              </p>
              <h2 v-if="page.rector_letter_title" class="text-3xl md:text-4xl xl:text-5xl font-display font-bold text-ink-dark dark:text-white leading-[1.1] tracking-tight mb-7">
                {{ page.rector_letter_title }}
              </h2>
              <svg class="w-12 h-12 text-accent-200 mb-3" viewBox="0 0 32 32" fill="currentColor" aria-hidden="true">
                <path d="M9.352 4C4.456 7.456 1 13.12 1 19.36c0 5.088 3.072 8.064 6.624 8.064 3.36 0 5.856-2.688 5.856-5.856 0-3.168-2.208-5.472-5.088-5.472-.576 0-1.344.096-1.536.192.48-3.264 3.552-7.104 6.624-9.024L9.352 4zm16.512 0c-4.8 3.456-8.256 9.12-8.256 15.36 0 5.088 3.072 8.064 6.624 8.064 3.264 0 5.856-2.688 5.856-5.856 0-3.168-2.304-5.472-5.184-5.472-.576 0-1.248.096-1.44.192.48-3.264 3.456-7.104 6.528-9.024L25.864 4z"/>
              </svg>
              <div class="space-y-4 text-[16px] md:text-[17px] text-ink-medium dark:text-slate-300 leading-[1.75] max-w-2xl">
                <p v-for="(para, i) in page.rector_letter_paragraphs" :key="i">{{ para }}</p>
              </div>
              <div v-if="page.rector_name" class="mt-8 flex items-center gap-4">
                <div class="w-12 h-px bg-accent-500" />
                <span class="text-sm font-display font-semibold text-ink-dark dark:text-white">{{ page.rector_name }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           Mission / Vision / Values
      ════════════════════════════════════════════════════════════ -->
      <section v-if="mvvCards.length" class="py-24 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div class="text-center max-w-2xl mx-auto mb-14" data-animate>
            <p v-if="page.mvv_eyebrow" class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">
              {{ page.mvv_eyebrow }}
            </p>
            <h2 class="text-3xl md:text-4xl xl:text-5xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight">
              {{ page.mvv_title || t('about.mission') }}
            </h2>
          </div>

          <div class="grid md:grid-cols-3 gap-6">
            <article
              v-for="(item, i) in mvvCards"
              :key="item.key"
              data-animate
              :data-delay="i * 100"
              class="p-8 rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:shadow-card-hover transition-all duration-300"
            >
              <div :class="['w-14 h-14 rounded-2xl flex items-center justify-center mb-5 bg-gradient-to-br text-white shadow-md', item.color]">
                <component :is="item.icon" class="w-7 h-7" stroke-width="1.6" />
              </div>
              <h3 class="font-display text-xl font-bold text-ink-dark dark:text-white mb-3">{{ item.title }}</h3>
              <p class="text-[14.5px] text-ink-light dark:text-slate-400 leading-relaxed">{{ item.text }}</p>
            </article>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           History timeline
      ════════════════════════════════════════════════════════════ -->
      <section v-if="timeline.length" class="py-24 bg-white dark:bg-slate-900">
        <div class="container-narrow">
          <div class="text-center max-w-2xl mx-auto mb-14" data-animate>
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ t('about.history') }}</p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight">
              2009 → {{ new Date().getFullYear() }}
            </h2>
          </div>

          <div class="relative max-w-4xl mx-auto">
            <div class="absolute left-4 md:left-1/2 md:-translate-x-1/2 top-0 bottom-0 w-px bg-gradient-to-b from-accent-500 via-accent-500/30 to-transparent" />
            <div
              v-for="(item, i) in timeline"
              :key="item.id"
              :class="['relative pl-12 md:pl-0 md:flex md:items-center mb-10', i % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse']"
              data-animate
              :data-delay="i * 100"
            >
              <div class="md:w-1/2 md:px-8">
                <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-6 shadow-card hover:shadow-card-hover transition-shadow">
                  <span class="inline-block px-3 py-1 mb-3 text-xs font-bold uppercase tracking-wider rounded-full bg-accent-100 dark:bg-accent-900/40 text-accent-700 dark:text-accent-300">{{ item.year }}</span>
                  <h3 class="font-display text-lg font-semibold text-ink-dark dark:text-white mb-2">{{ item.title }}</h3>
                  <p class="text-sm text-ink-light dark:text-slate-400">{{ item.text }}</p>
                </div>
              </div>
              <div class="absolute left-2 md:left-1/2 md:-translate-x-1/2 top-6 md:top-1/2 md:-translate-y-1/2 w-5 h-5 rounded-full bg-accent-500 ring-4 ring-white dark:ring-slate-900" />
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           Accreditation
      ════════════════════════════════════════════════════════════ -->
      <section v-if="accreditations.length" class="py-24 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div class="text-center max-w-2xl mx-auto mb-12" data-animate>
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ t('home.licenses_eyebrow') }}</p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight">
              {{ t('home.recognition_title') }}
            </h2>
            <p class="mt-3 text-[14px] text-ink-light dark:text-slate-400">{{ t('home.recognition_lead') }}</p>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div
              v-for="(a, i) in accreditations"
              :key="a.id"
              data-animate
              :data-delay="i * 80"
              class="p-6 text-center rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-accent-300 dark:hover:border-accent-700 hover:shadow-card-hover transition-all"
            >
              <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-primary-700 to-primary-900 grid place-items-center text-white shadow-md">
                <component :is="resolveIcon(a.icon)" class="w-7 h-7" stroke-width="1.6" />
              </div>
              <p class="text-sm font-semibold text-ink-dark dark:text-white">{{ a.name }}</p>
              <p class="text-[10px] uppercase tracking-wider text-ink-faint mt-1">{{ a.code }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           Address + map
      ════════════════════════════════════════════════════════════ -->
      <section v-if="page.map_embed_url || page.address" class="py-24 bg-white dark:bg-slate-900">
        <div class="container-narrow">
          <div class="grid lg:grid-cols-[2fr,1fr] gap-8">
            <div v-if="page.map_embed_url" class="rounded-2xl overflow-hidden shadow-card border border-surface-muted dark:border-slate-700 min-h-[24rem]" data-animate>
              <iframe
                :src="page.map_embed_url"
                loading="lazy"
                class="w-full h-full min-h-[24rem]"
                frameborder="0"
                title="Xarita"
              />
            </div>
            <div data-animate data-delay="200">
              <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ t('contact.title') }}</p>
              <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight mb-4">
                {{ t('contact.subtitle') }}
              </h2>
              <ul class="space-y-3 text-sm">
                <li v-if="page.address" class="flex items-start gap-3">
                  <MapPin class="w-5 h-5 text-accent-500 mt-0.5 flex-shrink-0" />
                  <span class="text-ink-medium dark:text-slate-300">{{ page.address }}</span>
                </li>
                <li v-if="page.contact_email" class="flex items-start gap-3">
                  <Mail class="w-5 h-5 text-accent-500 mt-0.5 flex-shrink-0" />
                  <a :href="`mailto:${page.contact_email}`" class="text-primary-700 dark:text-primary-300 hover:underline">{{ page.contact_email }}</a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>
