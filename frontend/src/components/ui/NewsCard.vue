<script setup>
import { computed } from 'vue'
import { Eye, Clock, Calendar } from 'lucide-vue-next'

const props = defineProps({
  article:  { type: Object, required: true },
  featured: { type: Boolean, default: false }
})

function formatDate(d) {
  if (!d) return ''
  const opts = { day: 'numeric', month: 'long', year: 'numeric' }
  return new Date(d).toLocaleDateString('uz-UZ', opts)
}

const readTime = computed(() => {
  const text = (props.article.body || props.article.excerpt || '').replace(/<[^>]+>/g, '')
  const words = text.split(/\s+/).filter(Boolean).length
  return Math.max(1, Math.round(words / 200))
})

const cover = computed(() => props.article.cover_image || null)
const initials = computed(() => (props.article.title || '').slice(0, 2).toUpperCase())
</script>

<template>
  <RouterLink
    :to="`/news/${article.slug}`"
    :class="[
      'card-hover group flex overflow-hidden',
      featured ? 'flex-col md:flex-row md:col-span-2' : 'flex-col'
    ]"
  >
    <div
      :class="[
        'relative overflow-hidden bg-surface-soft dark:bg-slate-700',
        featured ? 'md:w-1/2 aspect-video md:aspect-auto' : 'aspect-video'
      ]"
    >
      <img
        v-if="cover"
        :src="cover"
        :alt="article.title"
        loading="lazy"
        width="640"
        height="360"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
      />
      <div
        v-else
        class="w-full h-full bg-gradient-to-br from-primary-700 to-primary-900 grid place-items-center text-white/40 font-display font-bold text-4xl"
      >
        {{ initials }}
      </div>

      <span
        v-if="article.category"
        class="absolute top-3 left-3 badge-accent shadow-sm backdrop-blur-sm"
      >
        {{ article.category.name || article.category }}
      </span>
    </div>

    <div
      :class="[
        'flex flex-col flex-1 p-5',
        featured && 'md:p-7 md:justify-center'
      ]"
    >
      <time class="inline-flex items-center gap-1.5 text-xs text-ink-faint dark:text-slate-500 mb-2">
        <Calendar class="w-3.5 h-3.5" />
        {{ formatDate(article.published_at) }}
      </time>
      <h3
        :class="[
          'font-display font-semibold text-ink-dark dark:text-white line-clamp-2 mb-2 group-hover:text-primary-600 dark:group-hover:text-primary-300 transition-colors',
          featured ? 'text-xl md:text-2xl' : 'text-base'
        ]"
      >
        {{ article.title }}
      </h3>
      <p class="text-sm text-ink-light dark:text-slate-400 line-clamp-3 flex-1">
        {{ article.excerpt }}
      </p>
      <div class="flex items-center gap-4 mt-4 pt-4 border-t border-surface-muted dark:border-slate-700">
        <span class="flex items-center gap-1 text-xs text-ink-faint">
          <Eye class="w-3.5 h-3.5" /> {{ article.views_count || 0 }}
        </span>
        <span class="flex items-center gap-1 text-xs text-ink-faint">
          <Clock class="w-3.5 h-3.5" /> {{ readTime }} min
        </span>
      </div>
    </div>
  </RouterLink>
</template>
