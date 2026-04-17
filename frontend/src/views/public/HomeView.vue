<script setup>
/**
 * HomeView — fully driven by /api/page-settings/home.
 *
 * Hardcoded data is gone: hero variant, sections, all collections
 * (faculties+programs, partners, licenses, faqs, …) come from the CMS.
 *
 * Sections are rendered in the order returned by the API and skipped
 * if `enabled === false`. Hero supports 5 variants:
 *   split | fullbleed_photo | video_bg | stats | minimal
 */
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  ArrowRightIcon, ChevronRightIcon, ChevronDownIcon,
  StarIcon, ShieldCheckIcon, BriefcaseIcon, PhoneIcon, ClockIcon,
  PlayIcon, ArrowsPointingOutIcon, XMarkIcon, ChevronLeftIcon, MapPinIcon,
  CalendarDaysIcon
} from '@heroicons/vue/24/outline'

import { NewsAPI, EventsAPI, PageSettingsAPI } from '@/api/endpoints'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { useSeo } from '@/composables/useSeo'
import { organizationSchema, breadcrumbSchema, graph } from '@/utils/schema'
import { resolveIcon } from '@/utils/iconResolver'
import { useLanguageStore } from '@/stores/language'
import ProgramCard from '@/components/cards/ProgramCard.vue'

const { t } = useI18n()
const lang = useLanguageStore()
useScrollAnimation()
useSeo(() => ({
  title: t('site.name'),
  description: t('home.hero_subtitle'),
  type: 'website',
  schema: graph(organizationSchema(), breadcrumbSchema([{ name: t('nav.home'), url: '/' }]))
}))

// ════════════════════════════════════════════════════════════
//  Page data fetched from CMS
// ════════════════════════════════════════════════════════════
const pageData = ref(null)
const loading = ref(true)

async function loadPageData() {
  loading.value = true
  try {
    pageData.value = await PageSettingsAPI.home(lang.currentLang)
  } catch (_) {
    pageData.value = null
  } finally {
    loading.value = false
  }
}
onMounted(loadPageData)
watch(() => lang.currentLang, loadPageData)

// Convenience accessors
const hero       = computed(() => pageData.value?.hero)
const sections   = computed(() => pageData.value?.sections || [])
const quickActs  = computed(() => pageData.value?.quick_actions || [])
const introPills = computed(() => pageData.value?.intro_pillars || [])
const campus     = computed(() => pageData.value?.campus)
const whyCards   = computed(() => pageData.value?.why_cards || [])
const faculties  = computed(() => pageData.value?.faculties || [])
const admSteps   = computed(() => pageData.value?.admission_steps || [])
const stats      = computed(() => pageData.value?.stats || [])
const testis     = computed(() => pageData.value?.testimonials || [])
const partners   = computed(() => pageData.value?.partners || [])
const licenses   = computed(() => pageData.value?.licenses || [])
const faqs       = computed(() => pageData.value?.faqs || [])
const finalCta   = computed(() => pageData.value?.final_cta)

// section helper — returns the section row by key, falls back to {enabled:true}
function sectionOf(key) {
  return sections.value.find(s => s.key === key) || { enabled: true, sort_order: 0 }
}
function isOn(key) {
  return sectionOf(key).enabled
}
function ord(key) {
  return sectionOf(key).sort_order ?? 0
}

// ════════════════════════════════════════════════════════════
//  Hero — particle field (only if show_particles)
// ════════════════════════════════════════════════════════════
const particleCanvas = ref(null)
let rafId = null
let resizeHandler = null

function startParticles() {
  if (!hero.value?.show_particles) return
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
  const canvas = particleCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  let W, H, particles
  const resize = () => { W = canvas.width = canvas.offsetWidth; H = canvas.height = canvas.offsetHeight }
  const init = () => {
    particles = Array.from({ length: 44 }, () => ({
      x: Math.random() * W, y: Math.random() * H,
      r: Math.random() * 1.4 + 0.4,
      vx: (Math.random() - 0.5) * 0.16,
      vy: (Math.random() - 0.5) * 0.16,
      a: Math.random() * 0.35 + 0.1
    }))
  }
  const draw = () => {
    ctx.clearRect(0, 0, W, H)
    for (const p of particles) {
      ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
      ctx.fillStyle = `rgba(255,255,255,${p.a})`; ctx.fill()
      p.x += p.vx; p.y += p.vy
      if (p.x < 0) p.x = W; if (p.x > W) p.x = 0
      if (p.y < 0) p.y = H; if (p.y > H) p.y = 0
    }
    rafId = requestAnimationFrame(draw)
  }
  resize(); init(); draw()
  resizeHandler = () => { resize(); init() }
  window.addEventListener('resize', resizeHandler, { passive: true })
}
function stopParticles() {
  if (rafId) cancelAnimationFrame(rafId)
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
  rafId = null; resizeHandler = null
}
watch(hero, () => {
  stopParticles()
  // Re-attach when hero finishes loading or variant changes
  setTimeout(startParticles, 0)
})
onBeforeUnmount(stopParticles)

// ════════════════════════════════════════════════════════════
//  News + events still live API (their own admin CRUD)
// ════════════════════════════════════════════════════════════
const newsItems  = ref([])
const eventItems = ref([])

async function loadNewsAndEvents() {
  try {
    const [news, events] = await Promise.all([
      NewsAPI.list({ limit: 5 }).catch(() => ({ items: [] })),
      EventsAPI.list({ when: 'upcoming', limit: 3 }).catch(() => ({ items: [] }))
    ])
    newsItems.value = news.items || []
    eventItems.value = events.items || []
  } catch (_) {}
}
onMounted(loadNewsAndEvents)
watch(() => lang.currentLang, loadNewsAndEvents)

function fmtDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('uz-UZ', { day: 'numeric', month: 'short', year: 'numeric' })
}
function dayPart(d) { return d ? new Date(d).toLocaleDateString('uz-UZ', { day: '2-digit' }) : '' }
function monthPart(d) { return d ? new Date(d).toLocaleDateString('uz-UZ', { month: 'short' }).toUpperCase() : '' }

// ════════════════════════════════════════════════════════════
//  Active faculty tab (for academic section)
// ════════════════════════════════════════════════════════════
const activeFacultySlug = ref(null)
watch(faculties, (list) => {
  if (list.length && !list.find(f => f.slug === activeFacultySlug.value)) {
    activeFacultySlug.value = list[0].slug
  }
}, { immediate: true })
const visibleFaculty = computed(() =>
  faculties.value.find(f => f.slug === activeFacultySlug.value) || faculties.value[0]
)

// FAQ accordion
const openFaq = ref(0)
function toggleFaq(i) { openFaq.value = openFaq.value === i ? -1 : i }

// ════════════════════════════════════════════════════════════
//  License lightbox
// ════════════════════════════════════════════════════════════
const licenseOpen = ref(false)
const licenseIdx = ref(0)
function openLicense(i) { licenseIdx.value = i; licenseOpen.value = true }
function closeLicense() { licenseOpen.value = false }
function prevLicense() {
  const n = licenses.value.length || 1
  licenseIdx.value = (licenseIdx.value - 1 + n) % n
}
function nextLicense() {
  const n = licenses.value.length || 1
  licenseIdx.value = (licenseIdx.value + 1) % n
}
function onLicenseKey(e) {
  if (!licenseOpen.value) return
  if (e.key === 'Escape') closeLicense()
  if (e.key === 'ArrowLeft') prevLicense()
  if (e.key === 'ArrowRight') nextLicense()
}
onMounted(() => window.addEventListener('keydown', onLicenseKey))
onBeforeUnmount(() => window.removeEventListener('keydown', onLicenseKey))

// Helper for hero CTA component (RouterLink vs <a>)
function ctaTag(external) { return external ? 'a' : 'router-link' }

// Section title helpers — admin override > i18n default
function sectionTitle(key, fallbackKey) {
  return sectionOf(key).title || t(fallbackKey)
}
function sectionEyebrow(key, fallbackKey) {
  return sectionOf(key).eyebrow || t(fallbackKey)
}
function sectionSubtitle(key, fallbackKey) {
  return sectionOf(key).subtitle || (fallbackKey ? t(fallbackKey) : '')
}

// Trust badges — kept hardcoded since they're brand-fixed
const heroTrust = [
  { label: 'Cambridge', sub: 'English Partner' },
  { label: 'ISO 9001',  sub: 'Quality Cert' },
  { label: 'OTV',       sub: 'Litsenziya' }
]
</script>

<template>
  <div class="bg-white dark:bg-slate-900">
    <!-- ─────────────────────────────────────────────────────────
         Loading skeleton while page settings fetch
    ──────────────────────────────────────────────────────────── -->
    <div v-if="loading" class="min-h-[60vh] grid place-items-center text-ink-faint">
      <div class="text-center">
        <div class="w-10 h-10 rounded-full border-4 border-primary-200 border-t-primary-700 animate-spin mx-auto mb-3" />
        <p class="text-xs">Yuklanmoqda...</p>
      </div>
    </div>

    <template v-else-if="pageData">
      <!-- ═══════════════════════════════════════════════════════
           HERO — variant-driven
      ════════════════════════════════════════════════════════════ -->
      <section
        v-if="hero?.enabled"
        class="relative overflow-hidden"
        :class="hero.variant === 'video_bg' || hero.variant === 'fullbleed_photo' ? 'min-h-[88vh]' : ''"
        :style="hero.variant !== 'fullbleed_photo' && hero.variant !== 'video_bg'
                  ? 'background: linear-gradient(135deg, #0A0D3D 0%, #1A1F6E 55%, #2D3A8C 100%);'
                  : 'background:#0A0D3D'"
      >
        <!-- Variant: video background -->
        <video
          v-if="hero.variant === 'video_bg' && hero.bg_video"
          :src="hero.bg_video"
          :poster="hero.bg_video_poster || hero.bg_image || undefined"
          autoplay
          muted
          loop
          playsinline
          class="absolute inset-0 w-full h-full object-cover"
        />

        <!-- Variant: full-bleed photo -->
        <img
          v-else-if="hero.variant === 'fullbleed_photo' && hero.bg_image"
          :src="hero.bg_image"
          alt=""
          class="absolute inset-0 w-full h-full object-cover"
        />

        <!-- Overlay for image/video variants -->
        <div
          v-if="hero.variant === 'video_bg' || hero.variant === 'fullbleed_photo'"
          class="absolute inset-0"
          :style="`background: linear-gradient(135deg, rgba(10,13,61,${hero.overlay_opacity / 100}) 0%, rgba(10,13,61,${(hero.overlay_opacity * 0.6) / 100}) 100%);`"
        />

        <!-- Decorative blobs (split / stats / minimal) -->
        <template v-if="hero.variant === 'split' || hero.variant === 'stats' || hero.variant === 'minimal'">
          <div class="absolute pointer-events-none"
               style="right: -15%; top: 50%; transform: translateY(-50%); width: 800px; height: 800px;
                      background: radial-gradient(circle, rgba(80,100,210,0.32) 0%, rgba(80,100,210,0.10) 35%, transparent 65%);" />
          <div class="absolute pointer-events-none"
               style="top: -10%; left: -8%; width: 500px; height: 500px;
                      background: radial-gradient(circle, rgba(30,40,120,0.45) 0%, transparent 65%);" />
          <div class="absolute inset-0 pointer-events-none"
               style="background-image: radial-gradient(circle, rgba(255,255,255,0.05) 1px, transparent 1px); background-size: 38px 38px;" />
        </template>

        <canvas v-if="hero.show_particles" ref="particleCanvas" class="absolute inset-0 pointer-events-none opacity-30" />

        <div class="relative z-10 container-narrow pt-16 pb-32 lg:pt-20 lg:pb-40">
          <!-- ─── Variant: split (text left, photo right) ─── -->
          <div v-if="hero.variant === 'split'" class="grid lg:grid-cols-[1.05fr_1fr] gap-12 xl:gap-16 items-center">
            <div>
              <div v-if="hero.eyebrow" class="hero-enter inline-flex items-center gap-2 px-3.5 py-1.5 mb-7 rounded-full"
                   style="animation-delay: 0.05s; background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.14);">
                <span class="relative flex h-1.5 w-1.5">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent-400 opacity-75" />
                  <span class="relative inline-flex rounded-full h-1.5 w-1.5 bg-accent-500" />
                </span>
                <span class="text-[12px] text-white/80 font-medium tracking-tight">{{ hero.eyebrow }}</span>
              </div>

              <h1 class="font-display font-bold text-white leading-[1.05] tracking-tight">
                <span v-if="hero.title" class="hero-enter block text-[40px] md:text-[52px] xl:text-[64px]" style="animation-delay: 0.15s;">{{ hero.title }}</span>
                <span v-if="hero.title_highlight" class="hero-enter block text-[40px] md:text-[52px] xl:text-[64px]" style="animation-delay: 0.28s;">
                  <span class="text-transparent bg-clip-text"
                        style="background-image: linear-gradient(135deg, #FFD74D 0%, #FFB300 50%, #FF8C00 100%); -webkit-background-clip: text;">{{ hero.title_highlight }}</span>
                </span>
                <span v-if="hero.title_tail" class="hero-enter block text-[34px] md:text-[44px] xl:text-[52px] text-white/70 font-semibold mt-1" style="animation-delay: 0.42s;">{{ hero.title_tail }}</span>
              </h1>

              <p v-if="hero.subtitle" class="hero-enter mt-7 text-[17px] md:text-lg text-white/60 leading-relaxed max-w-[520px]" style="animation-delay: 0.55s;">{{ hero.subtitle }}</p>

              <!-- Stats inline (split + stats variants) -->
              <div v-if="stats.length" class="hero-enter mt-8 flex items-center gap-8" style="animation-delay: 0.65s;">
                <div v-for="s in stats.slice(0, 4)" :key="s.id">
                  <div class="text-3xl md:text-[32px] font-display font-extrabold text-white tracking-tight">{{ s.value }}</div>
                  <div class="text-[11px] text-white/45 mt-0.5 uppercase tracking-wider">{{ s.label }}</div>
                </div>
              </div>

              <!-- CTAs -->
              <div class="hero-enter mt-9 flex flex-wrap items-center gap-4" style="animation-delay: 0.78s;">
                <component
                  v-if="hero.cta_primary_label && hero.cta_primary_url"
                  :is="ctaTag(hero.cta_primary_external)"
                  :to="!hero.cta_primary_external ? hero.cta_primary_url : undefined"
                  :href="hero.cta_primary_external ? hero.cta_primary_url : undefined"
                  :target="hero.cta_primary_external ? '_blank' : undefined"
                  :rel="hero.cta_primary_external ? 'noopener' : undefined"
                  class="group relative inline-flex items-center gap-2 px-7 py-3.5 rounded-xl font-bold text-[15px] overflow-hidden transition-all duration-300 hover:scale-[1.02] active:scale-[0.98]"
                  style="background: linear-gradient(135deg, #FFB300 0%, #FF8C00 100%); color: #0A0D3D; box-shadow: 0 8px 32px rgba(255,179,0,0.35);"
                >
                  <span class="relative z-10">{{ hero.cta_primary_label }}</span>
                  <ArrowRightIcon class="relative z-10 w-4 h-4 transition-transform group-hover:translate-x-0.5" />
                </component>

                <component
                  v-if="hero.cta_secondary_label && hero.cta_secondary_url"
                  :is="ctaTag(hero.cta_secondary_external)"
                  :to="!hero.cta_secondary_external ? hero.cta_secondary_url : undefined"
                  :href="hero.cta_secondary_external ? hero.cta_secondary_url : undefined"
                  :target="hero.cta_secondary_external ? '_blank' : undefined"
                  :rel="hero.cta_secondary_external ? 'noopener' : undefined"
                  class="group inline-flex items-center gap-2 px-6 py-3.5 rounded-xl font-semibold text-[15px] text-white border border-white/20 hover:bg-white/[0.06] hover:border-white/30 transition-all"
                >
                  <PlayIcon class="w-4 h-4" />
                  {{ hero.cta_secondary_label }}
                </component>
              </div>

              <!-- Trust badges -->
              <div v-if="hero.show_trust_badges" class="hero-enter mt-10 pt-8 border-t border-white/10" style="animation-delay: 0.92s;">
                <p class="text-[10px] uppercase tracking-[0.2em] text-white/40 mb-4 font-semibold">{{ t('home.hero_trust_label') }}</p>
                <div class="flex flex-wrap items-center gap-x-7 gap-y-3">
                  <div v-for="b in heroTrust" :key="b.label" class="flex items-center gap-2">
                    <div class="w-9 h-9 rounded-lg grid place-items-center"
                         style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12);">
                      <ShieldCheckIcon class="w-4 h-4 text-accent-400" />
                    </div>
                    <div class="leading-tight">
                      <p class="text-[12px] font-bold text-white/85">{{ b.label }}</p>
                      <p class="text-[10px] text-white/40">{{ b.sub }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Right side image -->
            <div v-if="hero.side_image" class="hero-enter relative hidden lg:block" style="animation-delay: 0.4s;">
              <div class="absolute inset-0 rounded-3xl translate-x-5 translate-y-5"
                   style="border: 1px solid rgba(255,255,255,0.12); background: rgba(255,255,255,0.03);" />

              <div v-if="hero.show_floating_cards"
                   class="absolute -top-4 -right-4 z-20 px-4 py-3 rounded-2xl flex items-center gap-3"
                   style="background: rgba(255,255,255,0.96); backdrop-filter: blur(20px); box-shadow: 0 20px 60px rgba(0,0,0,0.35);">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-accent-400 to-accent-600 grid place-items-center text-white">
                  <StarIcon class="w-5 h-5" />
                </div>
                <div class="leading-tight">
                  <p class="text-[15px] font-display font-extrabold text-primary-900">TOP-12</p>
                  <p class="text-[10px] font-semibold text-ink-faint">{{ t('home.hero_badge_rating') }}</p>
                </div>
              </div>

              <div class="relative aspect-[4/5] rounded-3xl overflow-hidden"
                   style="box-shadow: 0 30px 80px rgba(0,0,0,0.45); border: 1px solid rgba(255,255,255,0.1);">
                <img :src="hero.side_image" alt="" class="w-full h-full object-cover" loading="eager" />
                <div class="absolute inset-0 bg-gradient-to-tr from-[#0A0D3D]/55 via-transparent to-transparent" />

                <div v-if="hero.quote_text" class="absolute bottom-6 left-6 right-6 p-5 rounded-2xl"
                     style="background: rgba(10,13,61,0.78); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.12);">
                  <div class="flex items-start gap-3">
                    <div class="w-10 h-10 rounded-xl grid place-items-center flex-shrink-0"
                         style="background: rgba(255,179,0,0.15); border: 1px solid rgba(255,179,0,0.3);">
                      <StarIcon class="w-5 h-5 text-accent-400" />
                    </div>
                    <div class="min-w-0">
                      <p class="text-[13px] text-white/85 leading-snug">"{{ hero.quote_text }}"</p>
                      <p v-if="hero.quote_author" class="text-[11px] text-white/50 mt-1.5">{{ hero.quote_author }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="hero.show_floating_cards"
                   class="absolute -bottom-5 -left-5 z-20 px-4 py-3 rounded-2xl"
                   style="background: rgba(255,255,255,0.96); backdrop-filter: blur(20px); box-shadow: 0 20px 60px rgba(0,0,0,0.35);">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-400 to-emerald-600 grid place-items-center text-white">
                    <BriefcaseIcon class="w-5 h-5" />
                  </div>
                  <div class="leading-tight">
                    <p class="text-[15px] font-display font-extrabold text-primary-900">80%</p>
                    <p class="text-[10px] font-semibold text-ink-faint">{{ t('home.hero_badge_employed') }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- ─── Variant: full-bleed photo, video_bg, minimal — centered text ─── -->
          <div v-else-if="hero.variant === 'fullbleed_photo' || hero.variant === 'video_bg' || hero.variant === 'minimal'"
               class="max-w-3xl text-center mx-auto py-16">
            <div v-if="hero.eyebrow" class="hero-enter inline-flex items-center gap-2 px-3.5 py-1.5 mb-7 rounded-full"
                 style="animation-delay: 0.05s; background: rgba(255,255,255,0.10); border: 1px solid rgba(255,255,255,0.18);">
              <span class="text-[12px] text-white/85 font-medium tracking-tight">{{ hero.eyebrow }}</span>
            </div>
            <h1 class="font-display font-bold text-white leading-[1.05] tracking-tight">
              <span v-if="hero.title" class="hero-enter block text-[44px] md:text-[60px] xl:text-[72px]" style="animation-delay: 0.15s;">{{ hero.title }}</span>
              <span v-if="hero.title_highlight" class="hero-enter block text-[44px] md:text-[60px] xl:text-[72px]" style="animation-delay: 0.28s;">
                <span class="text-transparent bg-clip-text"
                      style="background-image: linear-gradient(135deg, #FFD74D 0%, #FFB300 50%, #FF8C00 100%); -webkit-background-clip: text;">{{ hero.title_highlight }}</span>
              </span>
              <span v-if="hero.title_tail" class="hero-enter block text-[36px] md:text-[48px] xl:text-[60px] text-white/85 font-semibold mt-1" style="animation-delay: 0.42s;">{{ hero.title_tail }}</span>
            </h1>
            <p v-if="hero.subtitle" class="hero-enter mt-7 text-[17px] md:text-xl text-white/75 leading-relaxed max-w-2xl mx-auto" style="animation-delay: 0.55s;">{{ hero.subtitle }}</p>

            <div class="hero-enter mt-10 flex flex-wrap items-center justify-center gap-4" style="animation-delay: 0.78s;">
              <component v-if="hero.cta_primary_label && hero.cta_primary_url"
                :is="ctaTag(hero.cta_primary_external)"
                :to="!hero.cta_primary_external ? hero.cta_primary_url : undefined"
                :href="hero.cta_primary_external ? hero.cta_primary_url : undefined"
                :target="hero.cta_primary_external ? '_blank' : undefined"
                :rel="hero.cta_primary_external ? 'noopener' : undefined"
                class="group inline-flex items-center gap-2 px-8 py-4 rounded-xl font-bold text-[15px] transition-all hover:scale-[1.03]"
                style="background: linear-gradient(135deg, #FFB300 0%, #FF8C00 100%); color: #0A0D3D; box-shadow: 0 8px 32px rgba(255,179,0,0.45);"
              >
                {{ hero.cta_primary_label }}
                <ArrowRightIcon class="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
              </component>
              <component v-if="hero.cta_secondary_label && hero.cta_secondary_url"
                :is="ctaTag(hero.cta_secondary_external)"
                :to="!hero.cta_secondary_external ? hero.cta_secondary_url : undefined"
                :href="hero.cta_secondary_external ? hero.cta_secondary_url : undefined"
                :target="hero.cta_secondary_external ? '_blank' : undefined"
                :rel="hero.cta_secondary_external ? 'noopener' : undefined"
                class="group inline-flex items-center gap-2 px-6 py-3.5 rounded-xl font-semibold text-[15px] text-white border border-white/30 hover:bg-white/[0.08] transition"
              >
                <PlayIcon class="w-4 h-4" />
                {{ hero.cta_secondary_label }}
              </component>
            </div>
          </div>

          <!-- ─── Variant: stats hero (text left + grid right) ─── -->
          <div v-else-if="hero.variant === 'stats'" class="grid lg:grid-cols-[1fr_1fr] gap-12 items-center">
            <div>
              <div v-if="hero.eyebrow" class="hero-enter inline-block px-3 py-1 mb-7 rounded-full text-[12px] text-white/85 font-medium tracking-tight"
                   style="background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.14);">{{ hero.eyebrow }}</div>
              <h1 class="font-display font-bold text-white leading-[1.05] tracking-tight">
                <span v-if="hero.title" class="hero-enter block text-[40px] md:text-[56px]">{{ hero.title }} <span v-if="hero.title_highlight" class="text-transparent bg-clip-text" style="background-image: linear-gradient(135deg, #FFD74D 0%, #FFB300 100%); -webkit-background-clip: text;">{{ hero.title_highlight }}</span> {{ hero.title_tail }}</span>
              </h1>
              <p v-if="hero.subtitle" class="hero-enter mt-6 text-lg text-white/70 max-w-lg">{{ hero.subtitle }}</p>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div v-for="s in stats.slice(0, 4)" :key="s.id"
                   class="rounded-2xl p-6 text-white" style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); backdrop-filter: blur(12px);">
                <p class="text-4xl font-display font-extrabold text-accent-400">{{ s.value }}</p>
                <p class="text-sm font-semibold mt-2">{{ s.label }}</p>
                <p class="text-[11px] text-white/50 mt-0.5">{{ s.sub }}</p>
              </div>
            </div>
          </div>

          <!-- Scroll indicator -->
          <div v-if="hero.show_scroll_indicator" class="hero-enter mt-16 hidden lg:flex justify-center" style="animation-delay: 1.1s;">
            <div class="flex flex-col items-center gap-2 text-white/40">
              <span class="text-[10px] uppercase tracking-[0.25em] font-semibold">{{ t('home.hero_scroll') }}</span>
              <span class="w-px h-10 bg-gradient-to-b from-white/40 to-transparent animate-pulse" />
            </div>
          </div>
        </div>

        <div class="absolute bottom-0 left-0 right-0 h-24 pointer-events-none"
             style="background: linear-gradient(to bottom, transparent 0%, #F5F7FF 100%);" />
      </section>

      <!-- ═══════════════════════════════════════════════════════
           QUICK ACTIONS RIBBON
      ════════════════════════════════════════════════════════════ -->
      <section v-if="quickActs.length" class="relative -mt-16 z-10">
        <div class="container-narrow">
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-3" data-animate>
            <component
              v-for="qa in quickActs"
              :key="qa.id"
              :is="qa.external ? 'a' : 'router-link'"
              :href="qa.external ? qa.url : undefined"
              :to="!qa.external ? qa.url : undefined"
              :target="qa.external ? '_blank' : undefined"
              :rel="qa.external ? 'noopener' : undefined"
              :class="['group flex items-center gap-4 p-5 rounded-2xl bg-white dark:bg-slate-800 transition-all duration-200 hover:-translate-y-0.5',
                       qa.accent ? 'shadow-[0_12px_40px_rgba(255,179,0,0.25)] ring-1 ring-accent-200/60'
                                 : 'shadow-[0_12px_40px_rgba(10,13,61,0.10)] ring-1 ring-surface-muted/60']"
            >
              <div :class="['w-11 h-11 rounded-xl grid place-items-center flex-shrink-0',
                            qa.accent ? 'bg-accent-500 text-white group-hover:bg-accent-600'
                                      : 'bg-primary-50 text-primary-700 group-hover:bg-primary-100 dark:bg-slate-700 dark:text-primary-300']">
                <component :is="resolveIcon(qa.icon)" class="w-5 h-5" />
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-bold text-ink-dark dark:text-white">{{ qa.title }}</p>
                <p class="text-xs text-ink-light dark:text-slate-400 mt-0.5 truncate">{{ qa.desc }}</p>
              </div>
              <ArrowRightIcon class="w-4 h-4 text-ink-faint group-hover:text-accent-500 group-hover:translate-x-0.5 transition-all flex-shrink-0" />
            </component>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           INTRO STRIP — text + 3 pillars
      ════════════════════════════════════════════════════════════ -->
      <section v-if="isOn('intro') && introPills.length" class="py-24 lg:py-28">
        <div class="container-narrow">
          <div class="grid lg:grid-cols-[1fr_1.05fr] gap-12 lg:gap-20 items-center">
            <div data-animate>
              <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">
                {{ sectionEyebrow('intro', 'home.intro_eyebrow') }}
              </p>
              <h2 class="text-3xl md:text-4xl xl:text-5xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight mb-6">
                {{ sectionTitle('intro', 'home.intro_title') }}
              </h2>
              <p class="text-[16px] text-ink-light dark:text-slate-400 leading-relaxed mb-4">{{ t('home.intro_p1') }}</p>
              <p class="text-[16px] text-ink-light dark:text-slate-400 leading-relaxed mb-8">{{ t('home.intro_p2') }}</p>
              <RouterLink to="/about"
                class="group inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-primary-50 hover:bg-primary-100 text-primary-800 dark:bg-slate-800 dark:text-white dark:hover:bg-slate-700 font-semibold text-[14px] transition-colors"
              >
                {{ t('home.intro_link') }}
                <ArrowRightIcon class="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
              </RouterLink>
            </div>
            <div class="space-y-4" data-animate data-delay="100">
              <div v-for="(p, i) in introPills" :key="p.id"
                   class="group relative p-6 rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-accent-300 dark:hover:border-accent-600 hover:shadow-[0_10px_40px_rgba(10,13,61,0.08)] transition-all duration-300">
                <div class="flex items-start gap-5">
                  <div class="w-12 h-12 rounded-xl grid place-items-center flex-shrink-0 bg-gradient-to-br from-primary-700 to-primary-900 text-white shadow-md">
                    <component :is="resolveIcon(p.icon)" class="w-6 h-6" stroke-width="1.8" />
                  </div>
                  <div class="flex-1">
                    <h3 class="text-base font-display font-bold text-ink-dark dark:text-white mb-1.5">{{ p.title }}</h3>
                    <p class="text-[13.5px] text-ink-light dark:text-slate-400 leading-relaxed">{{ p.desc }}</p>
                  </div>
                </div>
                <div class="absolute right-5 top-5 w-7 h-7 rounded-full grid place-items-center text-[11px] font-bold text-accent-600 bg-accent-50 dark:bg-accent-900/30">
                  0{{ i + 1 }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           NEWS — editorial layout
      ════════════════════════════════════════════════════════════ -->
      <section v-if="isOn('news')" class="py-24 lg:py-28 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-12">
            <div data-animate>
              <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">
                {{ sectionEyebrow('news', 'home.news_compact_eyebrow') }}
              </p>
              <h2 class="text-3xl md:text-4xl xl:text-5xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight">
                {{ sectionTitle('news', 'home.news_compact_title') }}
              </h2>
              <p class="mt-3 text-[15px] text-ink-light dark:text-slate-400 max-w-xl">{{ t('home.news_lead') }}</p>
            </div>
            <RouterLink to="/news" class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary-50 hover:bg-primary-100 dark:bg-slate-800 dark:hover:bg-slate-700 text-primary-800 dark:text-white text-[13px] font-bold transition-colors group whitespace-nowrap self-start sm:self-auto">
              {{ t('home.news_all') }}
              <ArrowRightIcon class="w-3.5 h-3.5 transition-transform group-hover:translate-x-0.5" />
            </RouterLink>
          </div>

          <div v-if="!newsItems.length" class="text-center text-ink-faint py-8 text-sm">{{ t('common.loading') }}</div>

          <div v-else class="grid lg:grid-cols-[1.55fr_1fr] gap-6">
            <RouterLink v-if="newsItems[0]" :to="`/news/${newsItems[0].slug}`" data-animate
                        class="group relative overflow-hidden rounded-3xl bg-surface-soft dark:bg-slate-800 lg:row-span-1 min-h-[460px] lg:min-h-[560px]">
              <img :src="newsItems[0].cover_image || `https://picsum.photos/seed/xiu-news${newsItems[0].id}/1200/900`"
                   :alt="newsItems[0].title" loading="lazy"
                   class="absolute inset-0 w-full h-full object-cover transition-transform duration-[1200ms] group-hover:scale-[1.04]" />
              <div class="absolute inset-0 bg-gradient-to-t from-[#0A0D3D] via-[#0A0D3D]/70 to-transparent" />
              <div class="absolute top-5 left-5 inline-flex items-center gap-2">
                <span class="px-3 py-1 rounded-full bg-accent-500 text-primary-900 text-[10px] font-bold uppercase tracking-wider shadow-md">{{ t('home.news_featured') }}</span>
                <span v-if="newsItems[0].category" class="px-3 py-1 rounded-full bg-white/15 backdrop-blur text-white text-[10px] font-semibold uppercase tracking-wider">{{ newsItems[0].category.name }}</span>
              </div>
              <div class="absolute inset-x-0 bottom-0 p-7 lg:p-9">
                <h3 class="text-2xl lg:text-3xl xl:text-[34px] font-display font-bold text-white leading-[1.15] tracking-tight mb-3 line-clamp-3 group-hover:text-accent-300 transition-colors">{{ newsItems[0].title }}</h3>
                <p v-if="newsItems[0].excerpt" class="hidden sm:block text-[14px] text-white/70 leading-relaxed line-clamp-2 mb-4">{{ newsItems[0].excerpt }}</p>
                <div class="flex items-center gap-4 text-[12px] text-white/60">
                  <time>{{ fmtDate(newsItems[0].published_at) }}</time>
                  <span>·</span>
                  <span class="inline-flex items-center gap-1.5 font-semibold text-accent-300 group-hover:text-accent-200">{{ t('home.news_read') }} <ArrowRightIcon class="w-3.5 h-3.5" /></span>
                </div>
              </div>
            </RouterLink>

            <div class="space-y-3">
              <RouterLink v-for="(n, i) in newsItems.slice(1, 5)" :key="n.id" :to="`/news/${n.slug}`" data-animate :data-delay="i * 60"
                          class="group flex gap-4 p-3 lg:p-4 rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-accent-300 dark:hover:border-accent-700 hover:shadow-[0_10px_30px_rgba(10,13,61,0.08)] transition-all duration-300">
                <div class="w-24 lg:w-28 aspect-[4/3] rounded-xl overflow-hidden bg-surface-soft dark:bg-slate-700 flex-shrink-0">
                  <img :src="n.cover_image || `https://picsum.photos/seed/xiu-news${n.id}/300/225`" :alt="n.title" loading="lazy"
                       class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-[1.06]" />
                </div>
                <div class="flex-1 min-w-0 flex flex-col py-1">
                  <p v-if="n.category" class="text-[10px] font-semibold uppercase tracking-wider text-accent-600 mb-1">{{ n.category.name }}</p>
                  <h4 class="text-[14px] font-display font-bold text-ink-dark dark:text-white leading-snug line-clamp-2 group-hover:text-primary-700 dark:group-hover:text-primary-300 transition-colors">{{ n.title }}</h4>
                  <time class="mt-auto pt-2 text-[11px] text-ink-faint">{{ fmtDate(n.published_at) }}</time>
                </div>
              </RouterLink>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           CAMPUS
      ════════════════════════════════════════════════════════════ -->
      <section v-if="isOn('campus') && campus" class="py-24">
        <div class="container-narrow">
          <div class="grid lg:grid-cols-[1.3fr_1fr] gap-12 lg:gap-16 items-center">
            <div class="grid grid-cols-3 gap-3 lg:gap-4" data-animate>
              <div class="col-span-2 row-span-2 rounded-2xl overflow-hidden bg-surface-soft relative group">
                <img :src="campus.main_image" alt="" loading="lazy"
                     class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-[1.03]" />
                <div class="absolute inset-0 bg-gradient-to-t from-primary-900/30 via-transparent to-transparent" />
                <a v-if="campus.video_url" :href="campus.video_url" target="_blank" rel="noopener"
                   class="absolute bottom-5 left-5 inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/90 backdrop-blur text-primary-900 text-xs font-semibold shadow-md hover:bg-white transition-colors">
                  <PlayIcon class="w-3.5 h-3.5" />{{ t('home.campus_video') }}
                </a>
              </div>
              <div class="aspect-square rounded-2xl overflow-hidden bg-surface-soft">
                <img :src="campus.image_2" alt="" loading="lazy" class="w-full h-full object-cover hover:scale-[1.04] transition-transform duration-700" />
              </div>
              <div class="aspect-square rounded-2xl overflow-hidden bg-surface-soft">
                <img :src="campus.image_3" alt="" loading="lazy" class="w-full h-full object-cover hover:scale-[1.04] transition-transform duration-700" />
              </div>
            </div>

            <div data-animate data-delay="150">
              <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ campus.eyebrow }}</p>
              <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight mb-5">{{ campus.title }}</h2>
              <p class="text-[16px] text-ink-light dark:text-slate-400 leading-relaxed mb-7 max-w-md">{{ campus.text }}</p>
              <ul class="space-y-3 mb-8">
                <li v-for="(b, i) in campus.bullets" :key="i" class="flex items-start gap-3 text-[14px] text-ink-medium dark:text-slate-300">
                  <span class="w-5 h-5 rounded-full bg-accent-100 dark:bg-accent-900/40 grid place-items-center flex-shrink-0 mt-0.5">
                    <span class="w-1.5 h-1.5 rounded-full bg-accent-500" />
                  </span>
                  {{ b }}
                </li>
              </ul>
              <RouterLink v-if="campus.cta_url" :to="campus.cta_url"
                class="group inline-flex items-center gap-2 text-sm font-semibold text-primary-700 dark:text-primary-300 hover:text-accent-600">
                <span class="border-b border-current pb-0.5">{{ campus.cta_label }}</span>
                <ArrowRightIcon class="w-4 h-4 transition-transform group-hover:translate-x-1" />
              </RouterLink>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           WHY XIU
      ════════════════════════════════════════════════════════════ -->
      <section v-if="isOn('why_xiu') && whyCards.length" class="py-24 relative overflow-hidden bg-gradient-to-br from-primary-50 via-white to-accent-50/40 dark:from-slate-900 dark:via-slate-900/50 dark:to-slate-900">
        <div class="absolute inset-0 pointer-events-none opacity-[0.04]" style="background-image: radial-gradient(circle, #1A1F6E 1px, transparent 1px); background-size: 28px 28px;" />
        <div class="container-narrow relative">
          <div class="max-w-2xl mb-14" data-animate>
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ sectionEyebrow('why_xiu', 'home.why_eyebrow') }}</p>
            <h2 class="text-3xl md:text-4xl xl:text-5xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight">{{ sectionTitle('why_xiu', 'home.why_title') }}</h2>
          </div>
          <div class="grid sm:grid-cols-2 gap-5">
            <article v-for="(c, i) in whyCards" :key="c.id" data-animate :data-delay="i * 80"
                     class="group p-7 lg:p-8 rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-accent-300 dark:hover:border-accent-700 hover:shadow-card-hover transition-all duration-300">
              <div class="flex items-start gap-5">
                <div :class="['w-12 h-12 rounded-xl grid place-items-center flex-shrink-0', c.icon_bg]">
                  <component :is="resolveIcon(c.icon)" :class="['w-6 h-6', c.icon_color]" stroke-width="1.8" />
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-baseline gap-2 mb-2">
                    <span class="text-3xl font-display font-extrabold text-ink-dark dark:text-white tracking-tight">{{ c.number }}</span>
                    <span class="text-xs text-ink-faint">{{ c.number_label }}</span>
                  </div>
                  <h3 class="text-lg font-display font-bold text-ink-dark dark:text-white mb-2 group-hover:text-primary-700 dark:group-hover:text-primary-300 transition-colors">{{ c.title }}</h3>
                  <p class="text-[14px] text-ink-light dark:text-slate-400 leading-relaxed">{{ c.desc }}</p>
                </div>
              </div>
            </article>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           ACADEMIC — Faculties + programs
      ════════════════════════════════════════════════════════════ -->
      <section v-if="isOn('academic') && faculties.length" class="py-24 lg:py-28 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6 mb-14">
            <div data-animate class="max-w-2xl">
              <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ sectionEyebrow('academic', 'home.academic_eyebrow') }}</p>
              <h2 class="text-3xl md:text-4xl xl:text-5xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight">{{ sectionTitle('academic', 'home.academic_title') }}</h2>
              <p class="mt-4 text-[15px] text-ink-light dark:text-slate-400">{{ t('home.academic_lead') }}</p>
            </div>
            <RouterLink to="/faculties" class="hidden lg:inline-flex items-center gap-1.5 text-sm font-semibold text-primary-700 dark:text-primary-300 hover:text-accent-600 group whitespace-nowrap">
              <span class="border-b border-current pb-0.5">{{ t('home.academic_all') }}</span>
              <ArrowRightIcon class="w-3.5 h-3.5 transition-transform group-hover:translate-x-0.5" />
            </RouterLink>
          </div>

          <!-- Faculty filter tabs -->
          <div class="flex flex-wrap items-center gap-2 mb-10" data-animate>
            <button v-for="f in faculties" :key="f.slug" type="button" @click="activeFacultySlug = f.slug"
                    :class="['group inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-[13px] font-semibold transition-all',
                             activeFacultySlug === f.slug
                               ? 'bg-primary-800 text-white shadow-md scale-[1.02]'
                               : 'bg-white dark:bg-slate-800 text-ink-medium dark:text-slate-300 border border-surface-muted dark:border-slate-700 hover:border-primary-300 hover:text-primary-700 dark:hover:text-primary-300']">
              <component :is="resolveIcon(f.icon)" class="w-4 h-4" stroke-width="1.8" />
              <span>{{ f.name }}</span>
              <span :class="['text-[10px] px-1.5 py-0.5 rounded-md font-bold',
                             activeFacultySlug === f.slug ? 'bg-white/20 text-white' : 'bg-surface-soft dark:bg-slate-700 text-ink-faint']">{{ f.programs.length }}</span>
            </button>
          </div>

          <!-- Program cards -->
          <div v-if="visibleFaculty" :key="visibleFaculty.slug" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <div v-for="(p, i) in visibleFaculty.programs" :key="`${visibleFaculty.slug}-${p.id}`" data-animate :data-delay="i * 60">
              <ProgramCard :program="p" />
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           ADMISSION JOURNEY
      ════════════════════════════════════════════════════════════ -->
      <section v-if="isOn('admission') && admSteps.length" class="py-24">
        <div class="container-narrow">
          <div class="text-center max-w-2xl mx-auto mb-16" data-animate>
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ sectionEyebrow('admission', 'home.adm_eyebrow') }}</p>
            <h2 class="text-3xl md:text-4xl xl:text-5xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight mb-4">{{ sectionTitle('admission', 'home.adm_title') }}</h2>
            <p class="text-[15px] text-ink-light dark:text-slate-400">{{ t('home.adm_lead') }}</p>
          </div>
          <div class="relative">
            <div class="hidden lg:block absolute left-0 right-0 top-[60px] h-px bg-gradient-to-r from-transparent via-accent-300 to-transparent" />
            <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-4 relative">
              <div v-for="(s, i) in admSteps" :key="s.id" data-animate :data-delay="i * 100" class="relative text-center">
                <div class="relative mx-auto w-[120px] h-[120px] mb-6">
                  <div class="absolute inset-0 rounded-full bg-white dark:bg-slate-900 border-2 border-surface-muted dark:border-slate-700" />
                  <div class="absolute inset-3 rounded-full bg-gradient-to-br from-primary-700 to-primary-900 grid place-items-center text-white shadow-lg">
                    <component :is="resolveIcon(s.icon)" class="w-9 h-9" stroke-width="1.6" />
                  </div>
                  <div class="absolute -top-1 -right-1 w-9 h-9 rounded-full bg-accent-500 text-white text-xs font-bold grid place-items-center shadow-md ring-4 ring-white dark:ring-slate-900">{{ s.number }}</div>
                </div>
                <h3 class="text-lg font-display font-bold text-ink-dark dark:text-white mb-2">{{ s.title }}</h3>
                <p class="text-[13.5px] text-ink-light dark:text-slate-400 leading-relaxed max-w-[240px] mx-auto">{{ s.desc }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           NUMBERS IN CONTEXT
      ════════════════════════════════════════════════════════════ -->
      <section v-if="isOn('numbers') && stats.length" class="py-24 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div class="text-center max-w-2xl mx-auto mb-14" data-animate>
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ sectionEyebrow('numbers', 'home.numbers_eyebrow') }}</p>
            <h2 class="text-3xl md:text-4xl xl:text-5xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight">{{ sectionTitle('numbers', 'home.numbers_title') }}</h2>
          </div>
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-5">
            <div v-for="(n, i) in stats" :key="n.id" data-animate :data-delay="i * 80"
                 class="p-7 lg:p-8 rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700">
              <p class="text-4xl lg:text-5xl font-display font-extrabold text-primary-800 dark:text-accent-400 tracking-tight">{{ n.value }}</p>
              <p class="mt-3 text-sm font-bold text-ink-dark dark:text-white">{{ n.label }}</p>
              <p class="text-[12px] text-ink-light dark:text-slate-400 mt-0.5">{{ n.sub }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           UPCOMING EVENTS (live API)
      ════════════════════════════════════════════════════════════ -->
      <section v-if="isOn('events')" class="py-24">
        <div class="container-narrow">
          <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6 mb-12">
            <div data-animate class="max-w-2xl">
              <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ sectionEyebrow('events', 'home.events_eyebrow') }}</p>
              <h2 class="text-3xl md:text-4xl xl:text-5xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight">{{ sectionTitle('events', 'home.events_title') }}</h2>
              <p class="mt-4 text-[15px] text-ink-light dark:text-slate-400">{{ t('home.events_lead') }}</p>
            </div>
            <RouterLink to="/events" class="hidden lg:inline-flex items-center gap-1.5 text-sm font-semibold text-primary-700 dark:text-primary-300 hover:text-accent-600 group whitespace-nowrap">
              <span class="border-b border-current pb-0.5">{{ t('home.events_all') }}</span>
              <ArrowRightIcon class="w-3.5 h-3.5 transition-transform group-hover:translate-x-0.5" />
            </RouterLink>
          </div>

          <div v-if="eventItems.length" class="grid md:grid-cols-3 gap-5">
            <RouterLink v-for="(e, i) in eventItems" :key="e.id" :to="`/events/${e.slug}`" data-animate :data-delay="i * 80"
                        class="group relative overflow-hidden rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-accent-300 dark:hover:border-accent-700 hover:shadow-card-hover transition-all duration-300">
              <div class="aspect-[16/10] relative bg-surface-soft dark:bg-slate-700 overflow-hidden">
                <img :src="e.cover_image || `https://picsum.photos/seed/xiu-event${e.id}/800/500`" :alt="e.title" loading="lazy"
                     class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-[1.04]" />
                <div class="absolute inset-0 bg-gradient-to-t from-primary-900/40 via-transparent to-transparent" />
                <div class="absolute top-4 left-4 bg-white dark:bg-slate-900 rounded-xl px-3 py-2 text-center shadow-md min-w-[60px]">
                  <div class="text-xl font-display font-extrabold text-primary-800 dark:text-accent-400 leading-none">{{ dayPart(e.starts_at) }}</div>
                  <div class="text-[10px] font-bold text-ink-faint mt-0.5 tracking-wider">{{ monthPart(e.starts_at) }}</div>
                </div>
              </div>
              <div class="p-5">
                <h3 class="text-base font-display font-bold text-ink-dark dark:text-white leading-snug line-clamp-2 mb-3 group-hover:text-primary-700 dark:group-hover:text-primary-300 transition-colors">{{ e.title }}</h3>
                <div class="flex items-center gap-2 text-[12px] text-ink-light dark:text-slate-400">
                  <MapPinIcon class="w-3.5 h-3.5 flex-shrink-0" />
                  <span class="truncate">{{ e.location || t('home.events_tba') }}</span>
                </div>
              </div>
            </RouterLink>
          </div>
          <div v-else class="rounded-2xl bg-white dark:bg-slate-800 border border-dashed border-surface-muted dark:border-slate-700 p-12 text-center">
            <CalendarDaysIcon class="w-10 h-10 mx-auto text-ink-faint mb-3" />
            <p class="text-sm font-semibold text-ink-medium dark:text-slate-300">{{ t('home.events_empty') }}</p>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           TESTIMONIALS
      ════════════════════════════════════════════════════════════ -->
      <section v-if="isOn('testimonials') && testis.length" class="py-24 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div class="text-center max-w-2xl mx-auto mb-14" data-animate>
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ sectionEyebrow('testimonials', 'home.test_eyebrow') }}</p>
            <h2 class="text-3xl md:text-4xl xl:text-5xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight">{{ sectionTitle('testimonials', 'home.test_title') }}</h2>
          </div>
          <div class="grid md:grid-cols-3 gap-5">
            <article v-for="(t_, i) in testis" :key="t_.id" data-animate :data-delay="i * 100"
                     class="p-7 lg:p-8 rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 flex flex-col">
              <svg class="w-8 h-8 text-accent-300 mb-4" viewBox="0 0 32 32" fill="currentColor" aria-hidden="true">
                <path d="M9.352 4C4.456 7.456 1 13.12 1 19.36c0 5.088 3.072 8.064 6.624 8.064 3.36 0 5.856-2.688 5.856-5.856 0-3.168-2.208-5.472-5.088-5.472-.576 0-1.344.096-1.536.192.48-3.264 3.552-7.104 6.624-9.024L9.352 4zm16.512 0c-4.8 3.456-8.256 9.12-8.256 15.36 0 5.088 3.072 8.064 6.624 8.064 3.264 0 5.856-2.688 5.856-5.856 0-3.168-2.304-5.472-5.184-5.472-.576 0-1.248.096-1.44.192.48-3.264 3.456-7.104 6.528-9.024L25.864 4z"/>
              </svg>
              <p class="text-[15px] text-ink-medium dark:text-slate-300 leading-[1.7] flex-1">{{ t_.text }}</p>
              <div class="mt-6 pt-6 border-t border-surface-muted dark:border-slate-700 flex items-center gap-3">
                <img v-if="t_.avatar" :src="t_.avatar" :alt="t_.name" loading="lazy" class="w-12 h-12 rounded-full object-cover" />
                <div>
                  <p class="text-sm font-bold text-ink-dark dark:text-white">{{ t_.name }}</p>
                  <p class="text-[12px] text-ink-light">{{ t_.role }}</p>
                </div>
              </div>
            </article>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           PARTNERS
      ════════════════════════════════════════════════════════════ -->
      <section v-if="isOn('partners') && partners.length" class="py-24">
        <div class="container-narrow">
          <div class="text-center max-w-2xl mx-auto mb-14" data-animate>
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ sectionEyebrow('partners', 'home.partners_eyebrow') }}</p>
            <h2 class="text-3xl md:text-4xl xl:text-5xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight mb-4">{{ sectionTitle('partners', 'home.partners_title_h') }}</h2>
            <p class="text-[15px] text-ink-light dark:text-slate-400">{{ t('home.partners_lead') }}</p>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3" data-animate data-delay="100">
            <div v-for="p in partners" :key="p.id"
                 class="group flex items-center gap-3 px-4 py-3.5 rounded-xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-accent-300 dark:hover:border-accent-700 hover:-translate-y-0.5 transition-all">
              <span class="text-2xl flex-shrink-0">{{ p.flag }}</span>
              <div class="min-w-0 flex-1">
                <p class="text-[13px] font-bold text-ink-dark dark:text-white truncate">{{ p.country }}</p>
                <p class="text-[10.5px] text-ink-faint">{{ p.count }} {{ t('home.partners_count') }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           LICENSES
      ════════════════════════════════════════════════════════════ -->
      <section v-if="isOn('licenses') && licenses.length" class="py-24 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div class="text-center max-w-2xl mx-auto mb-14" data-animate>
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ sectionEyebrow('licenses', 'home.licenses_eyebrow') }}</p>
            <h2 class="text-3xl md:text-4xl xl:text-5xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight mb-4">{{ sectionTitle('licenses', 'home.recognition_title') }}</h2>
            <p class="text-[15px] text-ink-light dark:text-slate-400">{{ t('home.recognition_lead') }}</p>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            <button v-for="(lic, i) in licenses" :key="lic.id" type="button" data-animate :data-delay="i * 80"
                    class="group text-left focus:outline-none" @click="openLicense(i)">
              <div class="relative overflow-hidden rounded-md bg-white shadow-[0_8px_30px_rgba(10,13,61,0.15)] group-hover:shadow-[0_18px_50px_rgba(10,13,61,0.25)] group-hover:-translate-y-1.5 transition-all duration-300"
                   style="aspect-ratio: 1 / 1.4142;">
                <div class="absolute inset-0 ring-1 ring-black/[0.06] rounded-md pointer-events-none z-10" />
                <img :src="lic.image" :alt="lic.title" loading="lazy" class="absolute inset-0 w-full h-full object-cover" />
                <div class="absolute inset-x-0 bottom-0 p-4 bg-gradient-to-t from-[#0A0D3D]/95 via-[#0A0D3D]/70 to-transparent">
                  <p class="text-[13px] font-display font-bold text-white leading-tight line-clamp-2">{{ lic.title }}</p>
                  <p class="text-[10px] text-white/65 mt-1 truncate">{{ lic.issuer }} <template v-if="lic.year">· {{ lic.year }}</template></p>
                </div>
                <div class="absolute top-3 right-3 w-9 h-9 rounded-full bg-white/95 backdrop-blur grid place-items-center shadow-md opacity-0 group-hover:opacity-100 -translate-y-1 group-hover:translate-y-0 transition-all duration-300">
                  <ArrowsPointingOutIcon class="w-4 h-4 text-primary-800" />
                </div>
                <div v-if="lic.year" class="absolute top-3 left-3 px-2 py-0.5 rounded-md bg-accent-500 text-primary-900 text-[10px] font-bold tracking-wider shadow-md">{{ lic.year }}</div>
              </div>
            </button>
          </div>

          <p class="text-center text-[12px] text-ink-faint mt-8" data-animate>{{ t('home.licenses_hint') }}</p>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           FAQ
      ════════════════════════════════════════════════════════════ -->
      <section v-if="isOn('faq') && faqs.length" class="py-24">
        <div class="container-narrow max-w-3xl">
          <div class="text-center mb-12" data-animate>
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ sectionEyebrow('faq', 'home.faq_eyebrow') }}</p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white leading-[1.15] tracking-tight">{{ sectionTitle('faq', 'home.faq_title') }}</h2>
          </div>
          <div class="space-y-3" data-animate data-delay="100">
            <div v-for="(item, i) in faqs" :key="item.id"
                 class="border border-surface-muted dark:border-slate-700 rounded-xl overflow-hidden bg-white dark:bg-slate-800">
              <button type="button" @click="toggleFaq(i)" :aria-expanded="openFaq === i"
                      class="w-full flex items-center justify-between gap-4 px-6 py-5 text-left hover:bg-surface-light dark:hover:bg-slate-800/80 transition-colors">
                <span class="text-[15px] font-semibold text-ink-dark dark:text-white">{{ item.question }}</span>
                <ChevronDownIcon :class="['w-5 h-5 text-ink-faint flex-shrink-0 transition-transform duration-200', openFaq === i && 'rotate-180']" />
              </button>
              <div v-show="openFaq === i" class="px-6 pb-5 text-[14px] text-ink-light dark:text-slate-400 leading-relaxed border-t border-surface-muted dark:border-slate-700 pt-4">
                {{ item.answer }}
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           FINAL CTA
      ════════════════════════════════════════════════════════════ -->
      <section v-if="finalCta?.enabled" class="relative overflow-hidden py-24 lg:py-32"
               style="background: linear-gradient(135deg, #0A0D3D 0%, #1A1F6E 50%, #2D3A8C 100%);">
        <div class="absolute inset-0 pointer-events-none"
             style="background: radial-gradient(circle at 25% 50%, rgba(80,100,210,0.30) 0%, transparent 50%), radial-gradient(circle at 75% 50%, rgba(255,179,0,0.18) 0%, transparent 50%);" />
        <div class="absolute inset-0 opacity-[0.05] pointer-events-none"
             style="background-image: radial-gradient(circle, white 1px, transparent 1px); background-size: 32px 32px;" />
        <div class="relative container-narrow">
          <div class="max-w-3xl mx-auto text-center">
            <p v-if="finalCta.eyebrow" class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-400 mb-4" data-animate>{{ finalCta.eyebrow }}</p>
            <h2 class="text-4xl md:text-5xl xl:text-6xl font-display font-bold text-white leading-[1.1] tracking-tight mb-5" data-animate data-delay="100">{{ finalCta.title }}</h2>
            <p v-if="finalCta.text" class="text-[17px] text-white/65 mb-10 max-w-xl mx-auto" data-animate data-delay="200">{{ finalCta.text }}</p>
            <div class="flex flex-wrap justify-center items-center gap-5" data-animate data-delay="300">
              <component v-if="finalCta.cta_label && finalCta.cta_url"
                :is="ctaTag(finalCta.cta_external)"
                :to="!finalCta.cta_external ? finalCta.cta_url : undefined"
                :href="finalCta.cta_external ? finalCta.cta_url : undefined"
                :target="finalCta.cta_external ? '_blank' : undefined"
                :rel="finalCta.cta_external ? 'noopener' : undefined"
                class="group inline-flex items-center gap-2 px-8 py-4 rounded-xl font-bold text-[15px] transition-all hover:scale-[1.03]"
                style="background: linear-gradient(135deg, #FFB300 0%, #FF8C00 100%); color: #0A0D3D; box-shadow: 0 8px 32px rgba(255,179,0,0.45);"
              >
                {{ finalCta.cta_label }}
                <ArrowRightIcon class="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
              </component>
              <a v-if="finalCta.phone_label" :href="`tel:${finalCta.phone_url || finalCta.phone_label}`"
                 class="group inline-flex items-center gap-2 text-[15px] font-semibold text-white/85 hover:text-accent-400 transition">
                <PhoneIcon class="w-4 h-4" />
                <span>{{ finalCta.phone_label }}</span>
              </a>
            </div>
          </div>
        </div>
      </section>
    </template>

    <!-- ═══════════════════════════════════════════════════════
         License lightbox
    ════════════════════════════════════════════════════════════ -->
    <Teleport to="body">
      <Transition enter-active-class="transition duration-200" enter-from-class="opacity-0"
                  leave-active-class="transition duration-150" leave-to-class="opacity-0">
        <div v-if="licenseOpen && licenses.length"
             class="fixed inset-0 z-[120] bg-[#0A0D3D]/95 backdrop-blur-sm flex items-center justify-center p-6"
             @click.self="closeLicense">
          <button type="button" class="absolute top-5 right-5 w-11 h-11 rounded-full bg-white/10 hover:bg-white/20 text-white grid place-items-center" @click="closeLicense">
            <XMarkIcon class="w-5 h-5" />
          </button>
          <button v-if="licenses.length > 1" type="button" class="absolute left-5 top-1/2 -translate-y-1/2 w-11 h-11 rounded-full bg-white/10 hover:bg-white/20 text-white grid place-items-center" @click="prevLicense">
            <ChevronLeftIcon class="w-5 h-5" />
          </button>
          <button v-if="licenses.length > 1" type="button" class="absolute right-5 top-1/2 -translate-y-1/2 w-11 h-11 rounded-full bg-white/10 hover:bg-white/20 text-white grid place-items-center" @click="nextLicense">
            <ChevronRightIcon class="w-5 h-5" />
          </button>
          <div class="relative max-w-[90vw] max-h-[88vh] flex flex-col items-center">
            <img :src="licenses[licenseIdx].image" :alt="licenses[licenseIdx].title"
                 class="rounded-md shadow-[0_30px_80px_rgba(0,0,0,0.6)] max-h-[78vh] w-auto bg-white" style="aspect-ratio: 1 / 1.4142;" />
            <div class="mt-5 text-center">
              <p class="text-base font-display font-bold text-white">{{ licenses[licenseIdx].title }}</p>
              <p class="text-[12px] text-white/60 mt-1">{{ licenses[licenseIdx].issuer }}<template v-if="licenses[licenseIdx].year"> · {{ licenses[licenseIdx].year }}</template></p>
            </div>
          </div>
          <div class="absolute bottom-4 left-1/2 -translate-x-1/2 text-white/50 text-xs">{{ licenseIdx + 1 }} / {{ licenses.length }}</div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.hero-enter {
  opacity: 0;
  animation: hero-fade-up 0.85s cubic-bezier(0.2, 0.7, 0.2, 1) forwards;
}
@keyframes hero-fade-up {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
