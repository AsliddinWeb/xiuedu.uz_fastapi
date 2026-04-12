<script setup>
/**
 * FacultyDetailView — driven by /api/faculties/{slug}.
 *
 * Shows the faculty hero, description, list of programs in card form,
 * and a call-to-action linking to the admissions site.
 */
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  ArrowRight, ArrowLeft, Clock, GraduationCap, Languages
} from 'lucide-vue-next'
import UILoader from '@/components/ui/UILoader.vue'
import ProgramCard from '@/components/cards/ProgramCard.vue'
import { FacultiesAPI } from '@/api/endpoints'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { useSeo } from '@/composables/useSeo'
import { breadcrumbSchema } from '@/utils/schema'
import { resolveIcon } from '@/utils/iconResolver'
import { useLanguageStore } from '@/stores/language'

const { t } = useI18n()
const route = useRoute()
const lang = useLanguageStore()
useScrollAnimation()

const faculty = ref(null)
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    faculty.value = await FacultiesAPI.bySlug(route.params.slug, lang.currentLang)
  } catch (_) {
    faculty.value = null
  } finally {
    loading.value = false
  }
}
onMounted(load)
watch(() => route.params.slug, load)
watch(() => lang.currentLang, load)

useSeo(() => {
  if (!faculty.value) return { title: t('common.not_found'), noIndex: true }
  return {
    title: faculty.value.name,
    description: faculty.value.description,
    image: faculty.value.cover_image,
    schema: breadcrumbSchema([
      { name: t('nav.home'),        url: '/' },
      { name: t('nav.faculties'),   url: '/faculties' },
      { name: faculty.value.name,   url: route.path }
    ])
  }
})

// Stats from the program list
const stats = computed(() => {
  if (!faculty.value) return null
  const programs = faculty.value.programs || []
  const langs = new Set(programs.map(p => p.language).filter(Boolean))
  return {
    programs: programs.length,
    languages: langs.size
  }
})
</script>

<template>
  <div>
    <!-- Loading -->
    <div v-if="loading" class="min-h-[60vh] grid place-items-center">
      <UILoader />
    </div>

    <!-- Not found -->
    <div v-else-if="!faculty" class="container-narrow py-32 text-center">
      <GraduationCap class="w-16 h-16 mx-auto text-ink-faint mb-4" stroke-width="1.4" />
      <h1 class="text-2xl font-display font-bold text-ink-dark dark:text-white mb-3">{{ t('common.not_found') }}</h1>
      <RouterLink to="/faculties" class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary-800 hover:bg-primary-900 text-white font-semibold text-sm">
        <ArrowLeft class="w-4 h-4" /> {{ t('nav.faculties') }}
      </RouterLink>
    </div>

    <template v-else>
      <!-- ═══════════════════════════════════════════════════════
           Hero
      ════════════════════════════════════════════════════════════ -->
      <section
        class="relative overflow-hidden text-white"
        :class="faculty.cover_image ? 'min-h-[420px]' : 'min-h-[280px]'"
        style="background: linear-gradient(135deg, #0A0D3D 0%, #1A1F6E 60%, #2D3A8C 100%);"
      >
        <img
          v-if="faculty.cover_image"
          :src="faculty.cover_image"
          :alt="faculty.name"
          class="absolute inset-0 w-full h-full object-cover opacity-30"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-[#0A0D3D]/95 via-[#0A0D3D]/60 to-transparent" />
        <div class="absolute inset-0 opacity-[0.05] pointer-events-none"
             style="background-image: radial-gradient(circle, white 1px, transparent 1px); background-size: 32px 32px;" />

        <div class="relative container-narrow pt-20 pb-16">
          <!-- Breadcrumb -->
          <div class="text-sm text-white/65 mb-6">
            <RouterLink to="/" class="hover:text-white">{{ t('nav.home') }}</RouterLink>
            <span class="mx-2">/</span>
            <RouterLink to="/faculties" class="hover:text-white">{{ t('nav.faculties') }}</RouterLink>
          </div>

          <div class="flex items-start gap-5 max-w-3xl">
            <div class="w-16 h-16 rounded-2xl bg-white/15 backdrop-blur grid place-items-center flex-shrink-0">
              <component :is="resolveIcon(faculty.icon)" class="w-9 h-9 text-accent-400" stroke-width="1.5" />
            </div>
            <div>
              <h1 class="text-3xl md:text-4xl xl:text-5xl font-display font-bold leading-[1.1] mb-3 tracking-tight">{{ faculty.name }}</h1>
              <p class="text-white/85 text-lg max-w-2xl leading-relaxed">{{ faculty.description }}</p>
            </div>
          </div>

          <!-- Stat strip -->
          <div v-if="stats" class="mt-10 flex items-center gap-8 max-w-3xl">
            <div>
              <div class="text-3xl font-display font-extrabold tracking-tight">{{ stats.programs }}</div>
              <div class="text-[11px] uppercase tracking-wider text-white/50 mt-0.5">{{ t('faculties.programs') }}</div>
            </div>
            <div class="h-10 w-px bg-white/15" />
            <div>
              <div class="text-3xl font-display font-extrabold tracking-tight">{{ stats.languages }}</div>
              <div class="text-[11px] uppercase tracking-wider text-white/50 mt-0.5">{{ t('common.show_more') }}</div>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           Programs grid
      ════════════════════════════════════════════════════════════ -->
      <section class="py-24 lg:py-28">
        <div class="container-narrow">
          <div class="text-center max-w-2xl mx-auto mb-14" data-animate>
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">
              {{ t('faculties.programs') }}
            </p>
            <h2 class="text-3xl md:text-4xl xl:text-5xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight">
              {{ t('home.academic_title') }}
            </h2>
          </div>

          <div v-if="!faculty.programs.length" class="text-center py-16 text-ink-faint">
            {{ t('common.not_found') }}
          </div>

          <div v-else class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <div v-for="(p, i) in faculty.programs" :key="p.id" data-animate :data-delay="i * 60">
              <ProgramCard :program="p" />
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           CTA
      ════════════════════════════════════════════════════════════ -->
      <section class="py-20 bg-surface-light dark:bg-slate-800/40 border-t border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div
            data-animate
            class="rounded-3xl p-10 lg:p-14 text-center text-white relative overflow-hidden"
            style="background: linear-gradient(135deg, #0A0D3D 0%, #1A1F6E 60%, #2D3A8C 100%);"
          >
            <div class="absolute inset-0 opacity-[0.06] pointer-events-none"
                 style="background-image: radial-gradient(circle, white 1px, transparent 1px); background-size: 28px 28px;" />
            <div class="relative max-w-xl mx-auto">
              <h2 class="text-2xl md:text-3xl font-display font-bold mb-3">
                {{ faculty.name }}
              </h2>
              <p class="text-white/70 text-[15px] mb-7">
                {{ t('home.final_cta_text') }}
              </p>
              <div class="flex flex-wrap items-center justify-center gap-3">
                <a
                  href="https://qabul.xiuedu.uz"
                  target="_blank"
                  rel="noopener"
                  class="inline-flex items-center gap-2 px-7 py-3.5 rounded-xl font-bold text-[14px] transition hover:scale-[1.03]"
                  style="background: linear-gradient(135deg, #FFB300 0%, #FF8C00 100%); color: #0A0D3D; box-shadow: 0 8px 32px rgba(255,179,0,0.45);"
                >
                  {{ t('home.cta_apply') }}
                  <ArrowRight class="w-4 h-4" />
                </a>
                <RouterLink
                  to="/faculties"
                  class="inline-flex items-center gap-2 px-6 py-3 rounded-xl font-semibold text-[14px] text-white border border-white/20 hover:bg-white/[0.06] transition"
                >
                  <ArrowLeft class="w-4 h-4" />
                  {{ t('common.back') }}
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>
