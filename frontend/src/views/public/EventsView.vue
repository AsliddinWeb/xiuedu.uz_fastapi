<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PageHero from '@/components/sections/PageHero.vue'
import UILoader from '@/components/ui/UILoader.vue'
import UIPagination from '@/components/ui/UIPagination.vue'
import { Calendar, Clock, MapPin, Image as ImageIcon, ArrowRight, Inbox } from 'lucide-vue-next'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { useSeo } from '@/composables/useSeo'
import { breadcrumbSchema } from '@/utils/schema'
import { useI18n } from 'vue-i18n'
import { EventsAPI } from '@/api/endpoints'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
useScrollAnimation()
useSeo(() => ({
  title: t('nav.events'),
  schema: breadcrumbSchema([
    { name: t('nav.home'), url: '/' },
    { name: t('nav.events'), url: '/events' }
  ])
}))

const filter = ref(route.query.when || 'upcoming')
const page = ref(parseInt(route.query.page || '1', 10))
const perPage = 12
const items = ref([])
const total = ref(0)
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    const res = await EventsAPI.list({ when: filter.value, page: page.value, limit: perPage })
    items.value = res.items || []
    total.value = res.total || 0
  } catch (_) {
    items.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

watch([filter, page], () => {
  router.replace({ query: { ...route.query, when: filter.value, page: page.value } })
  load()
})

onMounted(load)

function fmtDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('uz-UZ', { day: 'numeric', month: 'long', year: 'numeric' })
}
function fmtTime(d) {
  if (!d) return ''
  return new Date(d).toLocaleTimeString('uz-UZ', { hour: '2-digit', minute: '2-digit' })
}
function dayPart(d) { return new Date(d).getDate().toString().padStart(2, '0') }
function monthPart(d) {
  const m = ['Yan','Fev','Mar','Apr','May','Iyn','Iyl','Avg','Sen','Okt','Noy','Dek']
  return m[new Date(d).getMonth()]
}
</script>

<template>
  <div>
    <PageHero
      :title="t('nav.events')"
      subtitle="Universitet hayotidagi muhim sanalar"
      :items="[{ label: t('nav.events'), to: '/events' }]"
      variant="navy"
    />

    <section class="py-16 bg-surface-light dark:bg-slate-900">
      <div class="container-narrow">
        <!-- Filter tabs -->
        <div class="flex justify-center gap-2 mb-12">
          <button
            v-for="opt in [
              { key: 'upcoming', label: t('events.filter_upcoming') },
              { key: 'past',     label: t('events.filter_past') },
              { key: 'all',      label: t('events.filter_all') }
            ]"
            :key="opt.key"
            type="button"
            :class="['px-5 py-2 rounded-full text-sm font-semibold border transition',
                     filter === opt.key
                       ? 'bg-primary-700 text-white border-primary-700'
                       : 'border-surface-muted dark:border-slate-700 text-ink-medium dark:text-slate-300 hover:border-primary-500']"
            @click="filter = opt.key; page = 1"
          >{{ opt.label }}</button>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <UILoader v-for="n in 6" :key="n" variant="skeleton-card" />
        </div>

        <!-- Empty -->
        <div v-else-if="!items.length" class="text-center py-16">
          <Inbox class="w-16 h-16 text-ink-faint mx-auto mb-4" stroke-width="1.4" />
          <p class="text-ink-light">{{ t('events.empty') }}</p>
        </div>

        <!-- Grid -->
        <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <RouterLink
            v-for="(e, i) in items"
            :key="e.id"
            :to="`/events/${e.slug}`"
            data-animate
            :data-delay="(i % 6) * 80"
            :class="['card-hover overflow-hidden flex flex-col', filter === 'past' && 'opacity-70']"
          >
            <div class="aspect-[16/9] relative bg-surface-soft dark:bg-slate-700 grid place-items-center overflow-hidden">
              <img
                v-if="e.cover_image"
                :src="e.cover_image"
                :alt="e.title"
                width="600" height="338"
                loading="lazy"
                class="w-full h-full object-cover"
              />
              <ImageIcon v-else class="w-12 h-12 text-ink-faint" stroke-width="1.2" />
              <!-- Date badge -->
              <div class="absolute top-3 left-3 bg-white dark:bg-slate-800 rounded-xl px-3 py-2 shadow-card text-center">
                <div class="text-2xl font-display font-extrabold text-accent-600 leading-none">{{ dayPart(e.starts_at) }}</div>
                <div class="text-[10px] uppercase tracking-wider text-ink-faint">{{ monthPart(e.starts_at) }}</div>
              </div>
              <span v-if="e.is_featured" class="absolute top-3 right-3 badge-accent shadow-sm">Featured</span>
            </div>
            <div class="p-5 flex-1 flex flex-col">
              <h3 class="font-display font-bold text-lg text-ink-dark dark:text-white mb-3 line-clamp-2">{{ e.title }}</h3>
              <p v-if="e.description" class="text-sm text-ink-light dark:text-slate-400 line-clamp-2 mb-4 flex-1">
                {{ e.description }}
              </p>
              <div class="flex flex-wrap gap-3 text-xs text-ink-light pt-3 border-t border-surface-muted dark:border-slate-700">
                <span class="inline-flex items-center gap-1.5"><Clock class="w-3.5 h-3.5 text-accent-500" />{{ fmtTime(e.starts_at) }}</span>
                <span v-if="e.location" class="inline-flex items-center gap-1.5"><MapPin class="w-3.5 h-3.5 text-accent-500" />{{ e.location }}</span>
              </div>
            </div>
          </RouterLink>
        </div>

        <div v-if="!loading && total > perPage" class="mt-10 flex justify-center">
          <UIPagination v-model="page" :total="total" :per-page="perPage" />
        </div>
      </div>
    </section>
  </div>
</template>
