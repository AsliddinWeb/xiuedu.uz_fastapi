<script setup>
/**
 * FacultiesView — driven by /api/faculties/.
 *
 * Lists all enabled faculties with their program counts.
 * The icon string from the CMS is resolved via iconResolver.
 */
import { ref, onMounted, watch, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ArrowRight, BookOpen, GraduationCap } from 'lucide-vue-next'
import PageHero from '@/components/sections/PageHero.vue'
import UILoader from '@/components/ui/UILoader.vue'
import { FacultiesAPI } from '@/api/endpoints'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { useSeo } from '@/composables/useSeo'
import { breadcrumbSchema } from '@/utils/schema'
import { resolveIcon } from '@/utils/iconResolver'
import { useLanguageStore } from '@/stores/language'

const { t } = useI18n()
const lang = useLanguageStore()
useScrollAnimation()
useSeo(() => ({
  title: t('faculties.title'),
  description: t('faculties.subtitle'),
  schema: breadcrumbSchema([
    { name: t('nav.home'),         url: '/' },
    { name: t('faculties.title'),  url: '/faculties' }
  ])
}))

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

// Cycle through brand-friendly accent gradients for visual variety.
const ACCENTS = [
  { gradient: 'from-primary-700 to-primary-900', bg: 'bg-primary-50 dark:bg-primary-900/30',  fg: 'text-primary-700 dark:text-primary-300' },
  { gradient: 'from-emerald-600 to-primary-800', bg: 'bg-emerald-50 dark:bg-emerald-900/30',  fg: 'text-emerald-700 dark:text-emerald-300' },
  { gradient: 'from-accent-500 to-primary-800',  bg: 'bg-accent-50 dark:bg-accent-900/30',    fg: 'text-accent-700 dark:text-accent-300' },
  { gradient: 'from-slate-700 to-primary-900',   bg: 'bg-slate-100 dark:bg-slate-800/40',     fg: 'text-slate-700 dark:text-slate-300' },
  { gradient: 'from-sky-600 to-primary-800',     bg: 'bg-sky-50 dark:bg-sky-900/30',          fg: 'text-sky-700 dark:text-sky-300' },
  { gradient: 'from-rose-500 to-primary-800',    bg: 'bg-rose-50 dark:bg-rose-900/30',        fg: 'text-rose-700 dark:text-rose-300' }
]
function accentFor(i) { return ACCENTS[i % ACCENTS.length] }
</script>

<template>
  <div>
    <PageHero
      :title="t('faculties.title')"
      :subtitle="t('faculties.subtitle')"
      :items="[{ label: t('faculties.title'), to: '/faculties' }]"
      variant="navy"
    />

    <section class="py-20 lg:py-24 bg-surface-light dark:bg-slate-900">
      <div class="container-narrow">
        <!-- Loading -->
        <div v-if="loading" class="grid place-items-center py-20">
          <UILoader />
        </div>

        <!-- Empty -->
        <div v-else-if="!faculties.length" class="text-center py-20">
          <GraduationCap class="w-16 h-16 mx-auto text-ink-faint mb-4" stroke-width="1.4" />
          <p class="text-ink-light">{{ t('common.not_found') }}</p>
        </div>

        <!-- Grid -->
        <div v-else class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <RouterLink
            v-for="(f, i) in faculties"
            :id="f.slug"
            :key="f.slug"
            :to="`/faculties/${f.slug}`"
            data-animate
            :data-delay="i * 80"
            class="group overflow-hidden rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-transparent hover:shadow-[0_24px_60px_rgba(10,13,61,0.14)] hover:-translate-y-1 transition-all duration-300"
          >
            <!-- Header band -->
            <div :class="['relative h-44 bg-gradient-to-br p-7 flex flex-col justify-between text-white overflow-hidden', accentFor(i).gradient]">
              <div class="absolute inset-0 opacity-[0.08]"
                   style="background-image: radial-gradient(circle, white 1px, transparent 1px); background-size: 24px 24px;" />
              <div class="absolute -right-10 -top-10 w-40 h-40 rounded-full bg-white/10 blur-3xl" />
              <div class="relative w-14 h-14 rounded-2xl bg-white/15 backdrop-blur grid place-items-center">
                <component :is="resolveIcon(f.icon)" class="w-7 h-7 text-white" stroke-width="1.6" />
              </div>
              <h3 class="relative font-display font-bold text-xl leading-tight">{{ f.name }}</h3>
            </div>

            <!-- Body -->
            <div class="p-6">
              <p class="text-sm text-ink-light dark:text-slate-400 mb-5 line-clamp-3 leading-relaxed">
                {{ f.description }}
              </p>

              <!-- Stat strip -->
              <div class="grid grid-cols-2 gap-3 mb-5">
                <div :class="['rounded-xl px-3 py-3 text-center', accentFor(i).bg]">
                  <div :class="['text-2xl font-display font-extrabold', accentFor(i).fg]">{{ f.programs.length }}</div>
                  <div class="text-[10px] uppercase tracking-wider text-ink-faint mt-0.5 font-semibold">
                    {{ t('faculties.programs') }}
                  </div>
                </div>
                <div :class="['rounded-xl px-3 py-3 text-center', accentFor(i).bg]">
                  <div :class="['text-2xl font-display font-extrabold inline-flex items-center gap-1', accentFor(i).fg]">
                    <BookOpen class="w-4 h-4" />
                  </div>
                  <div class="text-[10px] uppercase tracking-wider text-ink-faint mt-0.5 font-semibold">
                    {{ t('faculties.subtitle') }}
                  </div>
                </div>
              </div>

              <!-- CTA row -->
              <div class="flex items-center justify-between pt-4 border-t border-surface-muted dark:border-slate-700">
                <span class="text-[12px] font-semibold text-primary-700 dark:text-primary-300 inline-flex items-center gap-1.5 group-hover:text-accent-600 transition-colors">
                  {{ t('common.read_more') }}
                  <ArrowRight class="w-3.5 h-3.5 transition-transform group-hover:translate-x-0.5" />
                </span>
              </div>
            </div>
          </RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>
