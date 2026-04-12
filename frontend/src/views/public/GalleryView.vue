<script setup>
/**
 * GalleryView — driven by /api/page-settings/gallery.
 * Real images from DB, categories as filter chips, lightbox.
 */
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { ChevronLeft, ChevronRight, X, Image as ImageIcon } from 'lucide-vue-next'
import PageHero from '@/components/sections/PageHero.vue'
import UILoader from '@/components/ui/UILoader.vue'
import { PageSettingsAPI } from '@/api/endpoints'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { useSeo } from '@/composables/useSeo'
import { breadcrumbSchema } from '@/utils/schema'
import { useLanguageStore } from '@/stores/language'

const { t } = useI18n()
const lang = useLanguageStore()
useScrollAnimation()
useSeo(() => ({
  title: t('gallery.title'),
  schema: breadcrumbSchema([
    { name: t('nav.home'),      url: '/' },
    { name: t('gallery.title'), url: '/gallery' }
  ])
}))

const data = ref(null)
const loading = ref(true)
const filter = ref('all')

async function load() {
  loading.value = true
  try {
    data.value = await PageSettingsAPI.gallery(lang.currentLang)
  } catch (_) {
    data.value = null
  } finally {
    loading.value = false
  }
}
onMounted(load)
watch(() => lang.currentLang, load)

const page       = computed(() => data.value?.page)
const categories = computed(() => data.value?.categories || [])
const allItems   = computed(() => data.value?.items || [])
const visible    = computed(() =>
  filter.value === 'all' ? allItems.value : allItems.value.filter(i => i.category_slug === filter.value)
)

// Lightbox
const open = ref(false)
const idx = ref(0)
function show(i) { idx.value = i; open.value = true }
function close() { open.value = false }
function prev() { idx.value = (idx.value - 1 + visible.value.length) % visible.value.length }
function next() { idx.value = (idx.value + 1) % visible.value.length }

function onKey(e) {
  if (!open.value) return
  if (e.key === 'Escape')     close()
  if (e.key === 'ArrowLeft')  prev()
  if (e.key === 'ArrowRight') next()
}
onMounted(() => document.addEventListener('keydown', onKey))
onBeforeUnmount(() => document.removeEventListener('keydown', onKey))
</script>

<template>
  <div>
    <PageHero
      :title="page?.hero_title || t('gallery.title')"
      :subtitle="page?.hero_subtitle || t('gallery.subtitle')"
      :items="[{ label: t('gallery.title'), to: '/gallery' }]"
      variant="navy"
    />

    <div v-if="loading" class="min-h-[40vh] grid place-items-center">
      <UILoader />
    </div>

    <template v-else>
      <section class="py-20 bg-surface-light dark:bg-slate-900">
        <div class="container-narrow">
          <!-- Category tabs -->
          <div v-if="categories.length" class="flex justify-center flex-wrap gap-2 mb-10">
            <button
              type="button"
              @click="filter = 'all'"
              :class="['px-4 py-2 rounded-full text-sm font-medium border transition',
                       filter === 'all'
                         ? 'bg-primary-700 text-white border-primary-700'
                         : 'border-surface-muted dark:border-slate-700 text-ink-medium dark:text-slate-300 hover:border-primary-500']"
            >{{ t('gallery.cat_all') }}</button>
            <button
              v-for="c in categories"
              :key="c.slug"
              type="button"
              :class="['px-4 py-2 rounded-full text-sm font-medium border transition',
                       filter === c.slug
                         ? 'bg-primary-700 text-white border-primary-700'
                         : 'border-surface-muted dark:border-slate-700 text-ink-medium dark:text-slate-300 hover:border-primary-500']"
              @click="filter = c.slug"
            >{{ c.name }}</button>
          </div>

          <!-- Empty -->
          <div v-if="!visible.length" class="text-center py-20">
            <ImageIcon class="w-16 h-16 text-ink-faint mx-auto mb-4" stroke-width="1.4" />
            <p class="text-ink-light">{{ t('common.not_found') }}</p>
          </div>

          <!-- Masonry grid -->
          <div v-else class="columns-1 sm:columns-2 lg:columns-3 gap-4 [&>*]:mb-4">
            <button
              v-for="(item, i) in visible"
              :key="item.id"
              class="block w-full break-inside-avoid rounded-xl overflow-hidden focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-500 group relative bg-surface-soft dark:bg-slate-800"
              @click="show(i)"
              :aria-label="item.alt || item.caption || `Photo ${item.id}`"
              data-animate
            >
              <img
                :src="item.image"
                :alt="item.alt || item.caption"
                loading="lazy"
                class="w-full h-auto object-cover group-hover:scale-[1.03] transition-transform duration-500"
              />
              <div class="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-colors" />
              <div v-if="item.caption" class="absolute bottom-0 inset-x-0 p-3 bg-gradient-to-t from-black/70 to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
                <p class="text-xs text-white font-semibold truncate">{{ item.caption }}</p>
              </div>
            </button>
          </div>
        </div>
      </section>
    </template>

    <!-- Lightbox -->
    <Teleport to="body">
      <Transition enter-active-class="transition duration-200" enter-from-class="opacity-0" leave-active-class="transition duration-150" leave-to-class="opacity-0">
        <div v-if="open && visible.length" class="fixed inset-0 z-[100] bg-black/95 backdrop-blur flex items-center justify-center p-4" @click.self="close">
          <button class="absolute top-5 right-5 p-2 rounded-full bg-white/10 text-white hover:bg-white/20" @click="close"><X class="w-5 h-5" /></button>
          <button v-if="visible.length > 1" class="absolute left-5 p-3 rounded-full bg-white/10 text-white hover:bg-white/20" @click="prev"><ChevronLeft class="w-6 h-6" /></button>
          <button v-if="visible.length > 1" class="absolute right-5 p-3 rounded-full bg-white/10 text-white hover:bg-white/20" @click="next"><ChevronRight class="w-6 h-6" /></button>

          <div class="flex flex-col items-center max-w-5xl max-h-[88vh]">
            <img
              :src="visible[idx]?.image"
              :alt="visible[idx]?.alt || visible[idx]?.caption"
              class="max-w-full max-h-[78vh] rounded-lg shadow-2xl object-contain"
            />
            <p v-if="visible[idx]?.caption" class="mt-3 text-white/80 text-sm text-center">{{ visible[idx].caption }}</p>
          </div>

          <p class="absolute bottom-4 left-0 right-0 text-center text-white/60 text-xs">{{ idx + 1 }} / {{ visible.length }}</p>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>
