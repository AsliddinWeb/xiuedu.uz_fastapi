<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import PageHero from '@/components/sections/PageHero.vue'
import NewsCard from '@/components/ui/NewsCard.vue'
import UIInput from '@/components/ui/UIInput.vue'
import UIPagination from '@/components/ui/UIPagination.vue'
import UILoader from '@/components/ui/UILoader.vue'
import { Search, Inbox } from 'lucide-vue-next'
import { NewsAPI } from '@/api/endpoints'
import { useSeo } from '@/composables/useSeo'
import { breadcrumbSchema } from '@/utils/schema'
import { useScrollAnimation } from '@/composables/useScrollAnimation'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
useScrollAnimation()
useSeo(() => ({
  title: t('news.title'),
  schema: breadcrumbSchema([
    { name: t('nav.home'), url: '/' },
    { name: t('news.title'), url: '/news' }
  ])
}))

const items = ref([])
const total = ref(0)
const loading = ref(true)
const page = ref(parseInt(route.query.page || '1', 10))
const perPage = 12
const query = ref(route.query.q || '')
const cat = ref(route.query.cat || '')
const sort = ref(route.query.sort || 'newest')
const categories = ref([])

async function fetchCats() {
  try { categories.value = await NewsAPI.categories() } catch (_) {}
}
async function load() {
  loading.value = true
  try {
    const params = { page: page.value, limit: perPage }
    if (cat.value) params.category = cat.value
    const res = await NewsAPI.list(params)
    let arr = res.items || []
    if (sort.value === 'popular') arr = [...arr].sort((a, b) => b.views_count - a.views_count)
    items.value = arr
    total.value = res.total || arr.length
  } catch (_) {
    items.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

const filtered = computed(() => {
  if (!query.value) return items.value
  const q = query.value.toLowerCase()
  return items.value.filter(n => (n.title || '').toLowerCase().includes(q))
})

const featured = computed(() => filtered.value[0] || null)
const rest     = computed(() => filtered.value.slice(1))

watch([page, cat, sort], () => {
  router.replace({ query: { ...route.query, page: page.value, cat: cat.value || undefined, sort: sort.value } })
  load()
})

onMounted(() => { fetchCats(); load() })
</script>

<template>
  <div>
    <PageHero
      :title="t('news.title')"
      subtitle="Universitet hayotidan eng so'nggi yangiliklar va e'lonlar"
      :items="[{ label: t('news.title'), to: '/news' }]"
      variant="navy"
    />

    <section class="section bg-surface-light dark:bg-slate-900">
      <div class="container-narrow">
        <!-- Sticky filter bar -->
        <div class="sticky top-[72px] z-20 -mx-4 px-4 py-4 mb-8 bg-surface-light/90 dark:bg-slate-900/90 backdrop-blur border-b border-surface-muted dark:border-slate-700">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div class="md:w-96">
              <UIInput v-model="query" :placeholder="t('common.search_placeholder')">
                <template #prefix><Search class="w-4 h-4 text-ink-faint" /></template>
              </UIInput>
            </div>
            <div class="flex items-center gap-2">
              <button
                :class="['px-4 py-2 rounded-lg text-sm font-medium transition border',
                         sort === 'newest'
                           ? 'bg-primary-600 text-white border-primary-600'
                           : 'border-surface-muted dark:border-slate-700 text-ink-medium dark:text-slate-300 hover:border-primary-500']"
                @click="sort = 'newest'"
              >{{ t('news.newest') }}</button>
              <button
                :class="['px-4 py-2 rounded-lg text-sm font-medium transition border',
                         sort === 'popular'
                           ? 'bg-primary-600 text-white border-primary-600'
                           : 'border-surface-muted dark:border-slate-700 text-ink-medium dark:text-slate-300 hover:border-primary-500']"
                @click="sort = 'popular'"
              >{{ t('news.popular') }}</button>
            </div>
          </div>

          <div v-if="categories.length" class="flex flex-wrap gap-2 mt-4">
            <button
              :class="['px-3 py-1.5 rounded-full text-xs font-medium border transition',
                       !cat
                         ? 'bg-primary-600 text-white border-primary-600'
                         : 'border-surface-muted dark:border-slate-700 text-ink-medium dark:text-slate-300 hover:border-primary-500']"
              @click="cat = ''"
            >{{ t('news.all') }}</button>
            <button
              v-for="c in categories"
              :key="c.id"
              :class="['inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border transition',
                       cat === c.slug
                         ? 'bg-primary-600 text-white border-primary-600'
                         : 'border-surface-muted dark:border-slate-700 text-ink-medium dark:text-slate-300 hover:border-primary-500']"
              @click="cat = c.slug"
            >
              <span v-if="c.color" class="w-2 h-2 rounded-full" :style="{ background: c.color }" />
              {{ c.name }}
            </button>
          </div>
        </div>

        <!-- Loading skeleton -->
        <div v-if="loading" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <UILoader v-for="n in 6" :key="n" variant="skeleton-card" />
        </div>

        <!-- Empty state -->
        <div v-else-if="!filtered.length" class="text-center py-20" data-animate>
          <Inbox class="w-16 h-16 text-ink-faint mx-auto mb-4" stroke-width="1.4" />
          <h3 class="font-display font-bold text-xl text-ink-dark dark:text-white mb-2">{{ t('news.no_results') }}</h3>
          <p class="text-ink-light">Boshqa kalit so'z yoki kategoriya bilan urinib ko'ring.</p>
        </div>

        <!-- Articles grid -->
        <template v-else>
          <div v-if="featured" class="mb-6" data-animate>
            <NewsCard :article="featured" featured />
          </div>
          <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <NewsCard
              v-for="(n, i) in rest"
              :key="n.id"
              :article="n"
              data-animate
              :data-delay="(i % 6) * 60"
            />
          </div>
        </template>

        <div v-if="total > perPage" class="mt-12 flex justify-center">
          <UIPagination v-model="page" :total="total" :per-page="perPage" />
        </div>
      </div>
    </section>
  </div>
</template>
