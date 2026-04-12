<script setup>
import { ref, onMounted } from 'vue'
import { Calendar, Eye, ArrowRight } from 'lucide-vue-next'
import { NewsAPI } from '@/api/endpoints'
import UILoader from '@/components/ui/UILoader.vue'
import UIBadge from '@/components/ui/UIBadge.vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const items = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await NewsAPI.list({ limit: 6 })
    items.value = res.items || []
  } catch (_) { /* silent */ }
  finally { loading.value = false }
})

function fmt(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>

<template>
  <section class="py-24 bg-neutral-50 dark:bg-primary-950">
    <div class="container-wide">
      <div class="flex flex-wrap items-end justify-between gap-4 mb-10">
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.2em] text-accent-500 mb-3">{{ t('nav.news') }}</p>
          <h2 class="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-primary-700 dark:text-white">
            {{ t('home.featured_news') }}
          </h2>
        </div>
        <RouterLink to="/news" class="inline-flex items-center gap-2 text-accent-500 font-medium hover:gap-3 transition-all">
          {{ t('home.view_all') }} <ArrowRight class="w-4 h-4" />
        </RouterLink>
      </div>

      <div v-if="loading" class="grid lg:grid-cols-3 gap-5">
        <UILoader v-for="n in 6" :key="n" variant="skeleton-card" />
      </div>

      <div v-else-if="items.length" class="grid lg:grid-cols-3 gap-5">
        <!-- Featured big card -->
        <RouterLink
          :to="`/news/${items[0].slug}`"
          class="lg:col-span-2 lg:row-span-2 group relative overflow-hidden rounded-2xl bg-white dark:bg-primary-800 border border-neutral-200 dark:border-primary-700 shadow-card hover:shadow-soft transition"
        >
          <div class="aspect-[16/10] bg-gradient-to-br from-primary-700 via-primary-800 to-primary-900 relative overflow-hidden">
            <img v-if="items[0].cover_image" :src="items[0].cover_image" :alt="items[0].title" class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/10 to-transparent" />
            <div v-if="items[0].category" class="absolute top-5 left-5">
              <UIBadge variant="accent" size="md">{{ items[0].category.name }}</UIBadge>
            </div>
            <div class="absolute bottom-0 left-0 right-0 p-6 text-white">
              <h3 class="font-display text-2xl lg:text-3xl font-bold mb-2 group-hover:text-accent-500 transition">{{ items[0].title }}</h3>
              <p class="text-sm text-neutral-200 line-clamp-2 mb-3">{{ items[0].excerpt }}</p>
              <div class="flex items-center gap-4 text-xs text-neutral-300">
                <span class="inline-flex items-center gap-1"><Calendar class="w-3 h-3" /> {{ fmt(items[0].published_at) }}</span>
                <span class="inline-flex items-center gap-1"><Eye class="w-3 h-3" /> {{ items[0].views_count }}</span>
              </div>
            </div>
          </div>
        </RouterLink>

        <!-- Smaller cards -->
        <RouterLink
          v-for="n in items.slice(1, 6)"
          :key="n.id"
          :to="`/news/${n.slug}`"
          class="group flex gap-3 p-3 rounded-xl bg-white dark:bg-primary-800 border border-neutral-200 dark:border-primary-700 hover:shadow-card transition"
        >
          <div class="w-24 h-24 rounded-lg flex-shrink-0 bg-gradient-to-br from-primary-600 to-primary-800 overflow-hidden">
            <img v-if="n.cover_image" :src="n.cover_image" :alt="n.title" class="w-full h-full object-cover" />
          </div>
          <div class="flex-1 min-w-0">
            <UIBadge v-if="n.category" variant="default" size="sm" class="mb-1">{{ n.category.name }}</UIBadge>
            <h4 class="font-semibold text-sm text-primary-700 dark:text-white line-clamp-2 group-hover:text-accent-500 transition">{{ n.title }}</h4>
            <p class="text-[11px] text-neutral-500 dark:text-neutral-400 mt-1.5 inline-flex items-center gap-2">
              <span class="inline-flex items-center gap-1"><Calendar class="w-3 h-3" /> {{ fmt(n.published_at) }}</span>
            </p>
          </div>
        </RouterLink>
      </div>

      <div v-else class="text-center py-12 text-neutral-500">{{ t('news.no_results') }}</div>
    </div>
  </section>
</template>
