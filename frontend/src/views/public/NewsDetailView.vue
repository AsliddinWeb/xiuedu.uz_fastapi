<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import DOMPurify from 'dompurify'
import {
  Calendar, Eye, Clock, ArrowLeft, ArrowRight, Link as LinkIcon,
  X, ChevronLeft, ChevronRight
} from 'lucide-vue-next'
import TelegramIcon  from '@/components/icons/TelegramIcon.vue'
import FacebookIcon  from '@/components/icons/FacebookIcon.vue'
import InstagramIcon from '@/components/icons/InstagramIcon.vue'
import { NewsAPI } from '@/api/endpoints'
import NewsCard from '@/components/ui/NewsCard.vue'
import UILoader from '@/components/ui/UILoader.vue'
import { useSeo } from '@/composables/useSeo'
import { newsArticleSchema, breadcrumbSchema, graph } from '@/utils/schema'
import { useToast } from '@/composables/useToast'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const toast = useToast()

const article = ref(null)
const related = ref([])
const loading = ref(true)
const progress = ref(0)

async function load() {
  loading.value = true
  try {
    article.value = await NewsAPI.bySlug(route.params.slug)
    const res = await NewsAPI.list({ limit: 4 })
    related.value = (res.items || []).filter(n => n.slug !== route.params.slug).slice(0, 3)
  } catch (_) {
    article.value = null
  } finally {
    loading.value = false
  }
}

function onScroll() {
  const h = document.documentElement
  const scrollTop = h.scrollTop || document.body.scrollTop
  const scrollHeight = h.scrollHeight - h.clientHeight
  progress.value = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0
}

onMounted(() => { load(); window.addEventListener('scroll', onScroll, { passive: true }) })
onBeforeUnmount(() => window.removeEventListener('scroll', onScroll))
watch(() => route.params.slug, () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
  load()
})

useSeo(() => {
  if (!article.value) return { title: t('news.title') }
  return {
    title: article.value.title,
    description: article.value.meta_description || article.value.excerpt,
    image: article.value.cover_image,
    type: 'article',
    schema: graph(
      newsArticleSchema(article.value),
      breadcrumbSchema([
        { name: t('nav.home'),  url: '/' },
        { name: t('news.title'), url: '/news' },
        { name: article.value.title, url: `/news/${article.value.slug}` }
      ])
    )
  }
})

const safeBody = computed(() => DOMPurify.sanitize(article.value?.body || ''))

const readTime = computed(() => {
  const text = (article.value?.body || '').replace(/<[^>]+>/g, '')
  const words = text.split(/\s+/).filter(Boolean).length
  return Math.max(1, Math.round(words / 200))
})

const shareUrl = computed(() => typeof window !== 'undefined' ? window.location.href : '')

function fmt(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('uz-UZ', { day: 'numeric', month: 'long', year: 'numeric' })
}

async function copyLink() {
  await navigator.clipboard.writeText(shareUrl.value)
  toast.success(t('common.link_copied'))
}

// ===== Lightbox =====
const lightboxOpen = ref(false)
const lightboxIdx = ref(0)
const galleryImages = computed(() => article.value?.gallery || [])

function openLightbox(i) { lightboxIdx.value = i; lightboxOpen.value = true }
function closeLightbox() { lightboxOpen.value = false }
function prevImg() { lightboxIdx.value = (lightboxIdx.value - 1 + galleryImages.value.length) % galleryImages.value.length }
function nextImg() { lightboxIdx.value = (lightboxIdx.value + 1) % galleryImages.value.length }

function onLightboxKey(e) {
  if (!lightboxOpen.value) return
  if (e.key === 'Escape')      closeLightbox()
  if (e.key === 'ArrowLeft')   prevImg()
  if (e.key === 'ArrowRight')  nextImg()
}
onMounted(() => document.addEventListener('keydown', onLightboxKey))
onBeforeUnmount(() => document.removeEventListener('keydown', onLightboxKey))
</script>

<template>
  <div>
    <div v-if="loading" class="container-narrow py-24">
      <UILoader variant="skeleton-text" :lines="8" />
    </div>

    <article v-else-if="article">
    <!-- Reading progress -->
    <div class="fixed top-0 left-0 right-0 h-1 z-[60] bg-transparent">
      <div class="h-full bg-accent-500 transition-[width] duration-150" :style="{ width: progress + '%' }" />
    </div>

    <!-- Header banner -->
    <header class="relative bg-primary-800 dark:bg-[#080E22] text-white pt-12 pb-20 overflow-hidden">
      <div class="absolute inset-0 opacity-[0.06]" style="background-image: linear-gradient(rgba(255,255,255,.4) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.4) 1px, transparent 1px); background-size: 60px 60px;" />
      <div class="container-narrow relative max-w-4xl">
        <button class="inline-flex items-center gap-1 text-sm text-slate-300 hover:text-accent-300 mb-5" @click="router.back()">
          <ArrowLeft class="w-4 h-4" /> {{ t('common.back') }}
        </button>
        <span v-if="article.category" class="badge-accent mb-4 inline-block">{{ article.category.name }}</span>
        <h1 class="text-3xl md:text-5xl font-display font-bold leading-tight mb-5">{{ article.title }}</h1>
        <div class="flex flex-wrap items-center gap-5 text-sm text-slate-300">
          <span class="inline-flex items-center gap-1.5"><Calendar class="w-4 h-4" /> {{ fmt(article.published_at) }}</span>
          <span class="inline-flex items-center gap-1.5"><Eye class="w-4 h-4" /> {{ article.views_count }} {{ t('news.views') }}</span>
          <span class="inline-flex items-center gap-1.5"><Clock class="w-4 h-4" /> {{ readTime }} min</span>
        </div>
      </div>
    </header>

    <!-- Cover image -->
    <div class="container-narrow max-w-4xl -mt-12 relative">
      <div v-if="article.cover_image" class="aspect-video rounded-2xl overflow-hidden shadow-card-hover bg-surface-soft">
        <img :src="article.cover_image" :alt="article.title" loading="eager" class="w-full h-full object-cover" />
      </div>
      <div v-else class="aspect-video rounded-2xl overflow-hidden shadow-card-hover bg-gradient-to-br from-primary-700 to-primary-900 grid place-items-center">
        <span class="font-display font-bold text-6xl text-white/20">{{ article.title.charAt(0) }}</span>
      </div>
    </div>

    <!-- Body + share -->
    <section class="container-narrow max-w-4xl py-12">
      <div class="grid lg:grid-cols-[1fr,4rem] gap-6">
        <div>
          <div
            class="prose prose-neutral dark:prose-invert max-w-none prose-headings:font-display prose-headings:text-primary-800 dark:prose-headings:text-white prose-a:text-primary-600"
            v-html="safeBody"
          />

          <!-- Gallery from model -->
          <div v-if="article.gallery && article.gallery.length" class="mt-12">
            <h3 class="font-display font-bold text-xl text-ink-dark dark:text-white mb-5">Galereya</h3>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
              <button
                v-for="(img, i) in article.gallery"
                :key="i"
                type="button"
                class="aspect-square rounded-xl overflow-hidden bg-surface-soft dark:bg-slate-700 group focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-500"
                @click="openLightbox(i)"
                :aria-label="`Photo ${i + 1}`"
              >
                <img
                  :src="img"
                  :alt="`${article.title} — ${i + 1}`"
                  width="400" height="400"
                  loading="lazy"
                  class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                />
              </button>
            </div>
          </div>
        </div>

        <!-- Sticky share rail -->
        <aside class="hidden lg:flex flex-col gap-2 pt-2 sticky top-24 h-min">
          <p class="text-[10px] uppercase tracking-wider text-ink-faint mb-1 text-center">{{ t('news.share') }}</p>
          <a
            :href="`https://t.me/share/url?url=${encodeURIComponent(shareUrl)}&text=${encodeURIComponent(article.title)}`"
            target="_blank" rel="noopener" aria-label="Telegram"
            class="w-12 h-12 grid place-items-center rounded-xl border border-surface-muted dark:border-slate-700 text-ink-light hover:bg-accent-500 hover:text-white hover:border-accent-500 transition"
          ><TelegramIcon class="w-4 h-4" /></a>
          <a
            :href="`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`"
            target="_blank" rel="noopener" aria-label="Facebook"
            class="w-12 h-12 grid place-items-center rounded-xl border border-surface-muted dark:border-slate-700 text-ink-light hover:bg-accent-500 hover:text-white hover:border-accent-500 transition"
          ><FacebookIcon class="w-4 h-4" /></a>
          <a
            :href="`https://www.instagram.com`"
            target="_blank" rel="noopener" aria-label="Instagram"
            class="w-12 h-12 grid place-items-center rounded-xl border border-surface-muted dark:border-slate-700 text-ink-light hover:bg-accent-500 hover:text-white hover:border-accent-500 transition"
          ><InstagramIcon class="w-4 h-4" /></a>
          <button
            type="button"
            aria-label="Copy link"
            class="w-12 h-12 grid place-items-center rounded-xl border border-surface-muted dark:border-slate-700 text-ink-light hover:bg-accent-500 hover:text-white hover:border-accent-500 transition"
            @click="copyLink"
          >
            <LinkIcon class="w-4 h-4" />
          </button>
        </aside>
      </div>
    </section>

    <!-- Related -->
    <section v-if="related.length" class="section bg-surface-light dark:bg-slate-900">
      <div class="container-narrow">
        <div class="flex items-end justify-between mb-8">
          <h2 class="section-title">{{ t('news.related') }}</h2>
          <RouterLink to="/news" class="text-primary-600 dark:text-primary-300 font-medium inline-flex items-center gap-1 hover:gap-2 transition-all">
            {{ t('home.view_all') }} <ArrowRight class="w-4 h-4" />
          </RouterLink>
        </div>
        <div class="grid md:grid-cols-3 gap-6">
          <NewsCard v-for="r in related" :key="r.id" :article="r" />
        </div>
      </div>
    </section>
  </article>

  <div v-else class="container-narrow py-24 text-center">
    <p class="text-ink-light">{{ t('common.not_found') }}</p>
  </div>

  <!-- Lightbox -->
  <Teleport to="body">
    <Transition enter-active-class="transition duration-200" enter-from-class="opacity-0" leave-active-class="transition duration-150" leave-to-class="opacity-0">
      <div
        v-if="lightboxOpen"
        class="fixed inset-0 z-[120] bg-black/95 backdrop-blur flex items-center justify-center p-4"
        @click.self="closeLightbox"
      >
        <button
          class="absolute top-5 right-5 p-2 rounded-full bg-white/10 text-white hover:bg-white/20"
          @click="closeLightbox" aria-label="Close"
        ><X class="w-5 h-5" /></button>
        <button
          v-if="galleryImages.length > 1"
          class="absolute left-5 p-3 rounded-full bg-white/10 text-white hover:bg-white/20"
          @click="prevImg" aria-label="Previous"
        ><ChevronLeft class="w-6 h-6" /></button>
        <button
          v-if="galleryImages.length > 1"
          class="absolute right-5 p-3 rounded-full bg-white/10 text-white hover:bg-white/20"
          @click="nextImg" aria-label="Next"
        ><ChevronRight class="w-6 h-6" /></button>
        <img
          :src="galleryImages[lightboxIdx]"
          :alt="`Photo ${lightboxIdx + 1}`"
          class="max-w-full max-h-[90vh] object-contain rounded-2xl shadow-2xl"
        />
        <p class="absolute bottom-4 left-0 right-0 text-center text-white/60 text-xs">
          {{ lightboxIdx + 1 }} / {{ galleryImages.length }}
        </p>
      </div>
    </Transition>
  </Teleport>
  </div>
</template>
