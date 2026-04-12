<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import DOMPurify from 'dompurify'
import {
  Calendar, Clock, MapPin, ArrowLeft, Link as LinkIcon,
  X, ChevronLeft, ChevronRight
} from 'lucide-vue-next'
import TelegramIcon  from '@/components/icons/TelegramIcon.vue'
import FacebookIcon  from '@/components/icons/FacebookIcon.vue'
import { EventsAPI } from '@/api/endpoints'
import UILoader from '@/components/ui/UILoader.vue'
import { useSeo } from '@/composables/useSeo'
import { breadcrumbSchema, graph } from '@/utils/schema'
import { useToast } from '@/composables/useToast'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const toast = useToast()

const event = ref(null)
const upcoming = ref([])
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    event.value = await EventsAPI.bySlug(route.params.slug)
    const res = await EventsAPI.list({ when: 'upcoming', limit: 4 })
    upcoming.value = (res.items || []).filter(e => e.slug !== route.params.slug).slice(0, 3)
  } catch (_) {
    event.value = null
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => route.params.slug, load)

useSeo(() => {
  if (!event.value) return { title: t('nav.events') }
  return {
    title: event.value.title,
    description: event.value.meta_description || '',
    image: event.value.cover_image,
    type: 'article',
    schema: graph(
      breadcrumbSchema([
        { name: t('nav.home'),   url: '/' },
        { name: t('nav.events'), url: '/events' },
        { name: event.value.title, url: `/events/${event.value.slug}` }
      ])
    )
  }
})

const safeDescription = computed(() => DOMPurify.sanitize(event.value?.description || ''))
const shareUrl = computed(() => typeof window !== 'undefined' ? window.location.href : '')

function fmtDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('uz-UZ', { day: 'numeric', month: 'long', year: 'numeric' })
}
function fmtTime(d) {
  if (!d) return ''
  return new Date(d).toLocaleTimeString('uz-UZ', { hour: '2-digit', minute: '2-digit' })
}
function dayPart(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('uz-UZ', { day: '2-digit' })
}
function monthPart(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('uz-UZ', { month: 'short' }).toUpperCase()
}
const isPast = computed(() => event.value && new Date(event.value.starts_at).getTime() < Date.now())

async function copyLink() {
  await navigator.clipboard.writeText(shareUrl.value)
  toast.success(t('common.link_copied'))
}

// ===== Lightbox =====
const lightboxOpen = ref(false)
const lightboxIdx = ref(0)
const galleryImages = computed(() => event.value?.gallery || [])

function openLightbox(i) { lightboxIdx.value = i; lightboxOpen.value = true }
function closeLightbox() { lightboxOpen.value = false }
function prevImg() { lightboxIdx.value = (lightboxIdx.value - 1 + galleryImages.value.length) % galleryImages.value.length }
function nextImg() { lightboxIdx.value = (lightboxIdx.value + 1) % galleryImages.value.length }

function onLightboxKey(e) {
  if (!lightboxOpen.value) return
  if (e.key === 'Escape') closeLightbox()
  if (e.key === 'ArrowLeft') prevImg()
  if (e.key === 'ArrowRight') nextImg()
}
onMounted(() => window.addEventListener('keydown', onLightboxKey))
onBeforeUnmount(() => window.removeEventListener('keydown', onLightboxKey))
</script>

<template>
  <div class="bg-white dark:bg-slate-900">
    <div v-if="loading" class="container-narrow py-32 text-center">
      <UILoader />
    </div>

    <!-- Not found -->
    <div v-else-if="!event" class="container-narrow py-32 text-center">
      <h1 class="text-3xl font-display font-bold text-ink-dark dark:text-white mb-3">Tadbir topilmadi</h1>
      <p class="text-ink-light mb-6">So'ralgan tadbir mavjud emas yoki o'chirilgan.</p>
      <RouterLink to="/events" class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary-800 hover:bg-primary-900 text-white font-semibold text-sm">
        <ArrowLeft class="w-4 h-4" /> Tadbirlar ro'yxati
      </RouterLink>
    </div>

    <article v-else>
      <!-- Hero with cover -->
      <div
        class="relative overflow-hidden"
        :class="event.cover_image ? 'min-h-[420px]' : 'min-h-[280px]'"
        style="background: linear-gradient(135deg, #0A0D3D 0%, #1A1F6E 60%, #2D3A8C 100%);"
      >
        <img
          v-if="event.cover_image"
          :src="event.cover_image"
          :alt="event.title"
          class="absolute inset-0 w-full h-full object-cover opacity-40"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-[#0A0D3D]/95 via-[#0A0D3D]/60 to-transparent" />

        <div class="relative container-narrow pt-20 pb-12">
          <RouterLink
            to="/events"
            class="inline-flex items-center gap-1.5 text-[13px] text-white/70 hover:text-accent-400 mb-6"
          >
            <ArrowLeft class="w-4 h-4" /> Tadbirlar
          </RouterLink>

          <div class="flex items-start gap-5 mb-5">
            <!-- Date badge -->
            <div class="bg-white rounded-2xl px-4 py-3 text-center shadow-lg flex-shrink-0">
              <div class="text-3xl font-display font-extrabold text-primary-800 leading-none">{{ dayPart(event.starts_at) }}</div>
              <div class="text-[11px] font-bold text-ink-faint mt-1 tracking-wider">{{ monthPart(event.starts_at) }}</div>
            </div>

            <div class="flex-1 min-w-0">
              <span
                class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-semibold uppercase tracking-wider"
                :class="isPast ? 'bg-white/10 text-white/60' : 'bg-accent-500 text-primary-900'"
              >
                <span class="w-1.5 h-1.5 rounded-full" :class="isPast ? 'bg-white/40' : 'bg-primary-900'" />
                {{ isPast ? "O'tgan tadbir" : "Yaqinlashayotgan" }}
              </span>
              <h1 class="mt-3 text-3xl md:text-4xl xl:text-5xl font-display font-bold text-white leading-[1.15] tracking-tight">
                {{ event.title }}
              </h1>
            </div>
          </div>

          <!-- Meta row -->
          <div class="flex flex-wrap items-center gap-x-6 gap-y-2 text-[13px] text-white/75">
            <span class="inline-flex items-center gap-1.5">
              <Calendar class="w-4 h-4" /> {{ fmtDate(event.starts_at) }}
            </span>
            <span class="inline-flex items-center gap-1.5">
              <Clock class="w-4 h-4" />
              {{ fmtTime(event.starts_at) }}<span v-if="event.ends_at"> — {{ fmtTime(event.ends_at) }}</span>
            </span>
            <span v-if="event.location" class="inline-flex items-center gap-1.5">
              <MapPin class="w-4 h-4" /> {{ event.location }}
            </span>
          </div>
        </div>
      </div>

      <!-- Body -->
      <div class="container-narrow py-16">
        <div class="grid lg:grid-cols-[1fr,18rem] gap-12">
          <div>
            <div
              v-if="safeDescription"
              class="prose prose-lg dark:prose-invert max-w-none prose-headings:font-display prose-headings:text-ink-dark dark:prose-headings:text-white prose-a:text-accent-600 hover:prose-a:text-accent-700"
              v-html="safeDescription"
            />
            <p v-else class="text-ink-light italic">Tavsif yo'q.</p>

            <!-- Gallery -->
            <div v-if="galleryImages.length" class="mt-12">
              <h3 class="text-lg font-display font-bold text-ink-dark dark:text-white mb-4">Galereya</h3>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <button
                  v-for="(img, i) in galleryImages"
                  :key="i"
                  type="button"
                  class="aspect-[4/3] rounded-xl overflow-hidden bg-surface-soft dark:bg-slate-800 group relative"
                  @click="openLightbox(i)"
                >
                  <img :src="img" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                </button>
              </div>
            </div>
          </div>

          <!-- Sidebar -->
          <aside class="space-y-5">
            <div class="rounded-2xl p-5 bg-surface-light dark:bg-slate-800 border border-surface-muted dark:border-slate-700">
              <p class="text-[11px] font-semibold uppercase tracking-wider text-ink-faint mb-3">Ulashish</p>
              <div class="flex items-center gap-2">
                <a
                  :href="`https://t.me/share/url?url=${encodeURIComponent(shareUrl)}&text=${encodeURIComponent(event.title)}`"
                  target="_blank"
                  rel="noopener"
                  class="w-9 h-9 rounded-lg grid place-items-center bg-white dark:bg-slate-900 border border-surface-muted dark:border-slate-700 text-[#26A5E4] hover:bg-[#26A5E4] hover:text-white transition-colors"
                >
                  <TelegramIcon class="w-4 h-4" />
                </a>
                <a
                  :href="`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`"
                  target="_blank"
                  rel="noopener"
                  class="w-9 h-9 rounded-lg grid place-items-center bg-white dark:bg-slate-900 border border-surface-muted dark:border-slate-700 text-[#1877F2] hover:bg-[#1877F2] hover:text-white transition-colors"
                >
                  <FacebookIcon class="w-4 h-4" />
                </a>
                <button
                  type="button"
                  class="w-9 h-9 rounded-lg grid place-items-center bg-white dark:bg-slate-900 border border-surface-muted dark:border-slate-700 text-ink-medium hover:bg-primary-700 hover:text-white transition-colors"
                  @click="copyLink"
                >
                  <LinkIcon class="w-4 h-4" />
                </button>
              </div>
            </div>

            <div v-if="upcoming.length" class="rounded-2xl p-5 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700">
              <p class="text-[11px] font-semibold uppercase tracking-wider text-ink-faint mb-3">Yaqinlashayotgan</p>
              <div class="space-y-3">
                <RouterLink
                  v-for="e in upcoming"
                  :key="e.id"
                  :to="`/events/${e.slug}`"
                  class="flex items-start gap-3 group"
                >
                  <div class="bg-surface-light dark:bg-slate-900 rounded-lg px-2 py-1.5 text-center flex-shrink-0 min-w-[44px]">
                    <div class="text-base font-display font-extrabold text-primary-800 dark:text-accent-400 leading-none">{{ dayPart(e.starts_at) }}</div>
                    <div class="text-[9px] font-bold text-ink-faint mt-0.5 tracking-wider">{{ monthPart(e.starts_at) }}</div>
                  </div>
                  <p class="text-[13px] font-semibold text-ink-dark dark:text-white leading-snug line-clamp-2 group-hover:text-primary-700 dark:group-hover:text-primary-300">
                    {{ e.title }}
                  </p>
                </RouterLink>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </article>

    <!-- Lightbox -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition duration-200"
        enter-from-class="opacity-0"
        leave-active-class="transition duration-150"
        leave-to-class="opacity-0"
      >
        <div
          v-if="lightboxOpen"
          class="fixed inset-0 z-[120] bg-black/95 flex items-center justify-center"
          @click.self="closeLightbox"
        >
          <button
            type="button"
            class="absolute top-5 right-5 w-11 h-11 rounded-full bg-white/10 hover:bg-white/20 text-white grid place-items-center"
            @click="closeLightbox"
          >
            <X class="w-5 h-5" />
          </button>
          <button
            v-if="galleryImages.length > 1"
            type="button"
            class="absolute left-5 w-11 h-11 rounded-full bg-white/10 hover:bg-white/20 text-white grid place-items-center"
            @click="prevImg"
          >
            <ChevronLeft class="w-5 h-5" />
          </button>
          <button
            v-if="galleryImages.length > 1"
            type="button"
            class="absolute right-5 w-11 h-11 rounded-full bg-white/10 hover:bg-white/20 text-white grid place-items-center"
            @click="nextImg"
          >
            <ChevronRight class="w-5 h-5" />
          </button>
          <img
            :src="galleryImages[lightboxIdx]"
            class="max-w-[92vw] max-h-[88vh] object-contain"
            alt=""
          />
          <div class="absolute bottom-5 left-1/2 -translate-x-1/2 text-white/60 text-xs">
            {{ lightboxIdx + 1 }} / {{ galleryImages.length }}
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>
