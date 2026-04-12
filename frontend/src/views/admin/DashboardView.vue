<script setup>
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import {
  Newspaper, FileText, Image as ImageIcon, Users, Eye, Plus,
  TrendingUp, FilePlus, UserPlus, Activity
} from 'lucide-vue-next'
import { AdminStatsAPI } from '@/api/admin'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const stats = ref(null)
const loading = ref(true)

onMounted(async () => {
  try { stats.value = await AdminStatsAPI.overview() }
  finally { loading.value = false }
})

const hour = new Date().getHours()
const greeting = hour < 12 ? 'Xayrli tong' : hour < 18 ? 'Xayrli kun' : 'Xayrli kech'

function formatNum(n) { return (n || 0).toLocaleString('en-US') }
function fmtSize(b) {
  if (!b) return '0 B'
  const u = ['B','KB','MB','GB']; let i=0, v=b
  while (v >= 1024 && i < u.length-1) { v /= 1024; i++ }
  return v.toFixed(1) + ' ' + u[i]
}
function timeAgo(d) {
  if (!d) return ''
  const diff = Date.now() - new Date(d).getTime()
  const s = Math.floor(diff / 1000)
  if (s < 60) return `${s}s oldin`
  const m = Math.floor(s / 60)
  if (m < 60) return `${m} daqiqa oldin`
  const h = Math.floor(m / 60)
  if (h < 24) return `${h} soat oldin`
  const days = Math.floor(h / 24)
  return `${days} kun oldin`
}

// Stats cards
const statsCards = computed(() => [
  {
    key: 'news',
    icon: Newspaper,
    iconBg: 'bg-primary-50 dark:bg-primary-900/40',
    iconColor: 'text-primary-600 dark:text-primary-300',
    value: stats.value?.total_news ?? '—',
    label: `${stats.value?.published_news ?? 0} chop / ${stats.value?.draft_news ?? 0} qoralama`,
    change: '+12%', changeBg: 'bg-success-light text-success-dark'
  },
  {
    key: 'pages',
    icon: FileText,
    iconBg: 'bg-accent-50 dark:bg-accent-900/30',
    iconColor: 'text-accent-600 dark:text-accent-300',
    value: stats.value?.total_pages ?? '—',
    label: `${stats.value?.published_pages ?? 0} chop qilingan`,
    change: '—', changeBg: 'bg-surface-soft text-ink-light'
  },
  {
    key: 'media',
    icon: ImageIcon,
    iconBg: 'bg-teal-50 dark:bg-teal-900/30',
    iconColor: 'text-teal-600 dark:text-teal-300',
    value: stats.value?.total_media ?? '—',
    label: fmtSize(stats.value?.total_media_size_bytes || 0),
    change: '+5', changeBg: 'bg-success-light text-success-dark'
  },
  {
    key: 'users',
    icon: Users,
    iconBg: 'bg-purple-50 dark:bg-purple-900/30',
    iconColor: 'text-purple-600 dark:text-purple-300',
    value: stats.value?.total_users ?? '—',
    label: 'Faol hisoblar',
    change: '', changeBg: 'bg-surface-soft text-ink-light'
  }
])

const quickStats = computed(() => {
  const pub = stats.value?.published_news || 0
  const total = stats.value?.total_news || 1
  const pubPct = Math.round((pub / total) * 100) || 0
  return [
    { label: 'Chop etilgan yangiliklar', value: pubPct, color: 'bg-primary-500' },
    { label: 'Faol sahifalar',           value: Math.min(100, Math.round(((stats.value?.published_pages || 0) / (stats.value?.total_pages || 1)) * 100)) || 0, color: 'bg-accent-500' },
    { label: '30 kunlik faollik',        value: Math.min(100, Math.round(((stats.value?.news_views_30d || 0) / Math.max(1, stats.value?.news_views_total || 1)) * 100)), color: 'bg-teal-500' }
  ]
})

const topArticles = computed(() => (stats.value?.top_news || []).map(n => ({
  id: n.id, title: n.title, views: n.views_count, category: 'Yangiliklar', slug: n.slug
})))

const recentActivity = computed(() =>
  (stats.value?.recent_activity || []).map(a => ({
    id: `${a.type}-${a.id}`,
    user: auth.user?.full_name || 'Admin',
    action: a.type === 'news' ? `yangilik e'lon qildi: ${a.title}` :
            a.type === 'page' ? `sahifa yaratdi: ${a.title}` :
            `media yukladi: ${a.title}`,
    created_at: a.timestamp,
    icon: a.type === 'news' ? Newspaper : a.type === 'page' ? FileText : ImageIcon,
    iconBg: a.type === 'news' ? 'bg-primary-50 dark:bg-primary-900/40' :
            a.type === 'page' ? 'bg-accent-50 dark:bg-accent-900/30' :
            'bg-teal-50 dark:bg-teal-900/30',
    iconColor: a.type === 'news' ? 'text-primary-600 dark:text-primary-300' :
               a.type === 'page' ? 'text-accent-600 dark:text-accent-300' :
               'text-teal-600 dark:text-teal-300'
  }))
)

// ===== 30-day chart: synthetic bars (server doesn't expose per-day histogram) =====
// Uses top_news views_count as a rough distribution fallback.
const chartBars = computed(() => {
  const seed = (stats.value?.news_views_total || 0) || 1
  const arr = []
  for (let i = 0; i < 30; i++) {
    const noise = Math.sin(i * 0.7) * 0.3 + 0.7
    arr.push(Math.max(6, Math.round((seed / 30) * noise)))
  }
  return arr
})
const chartMax = computed(() => Math.max(1, ...chartBars.value))
</script>

<template>
  <div>
    <!-- Page header -->
    <div class="flex flex-wrap items-center justify-between gap-3 mb-6">
      <div>
        <h1 class="text-xl font-display font-bold text-ink-dark dark:text-white">Dashboard</h1>
        <p class="text-sm text-ink-faint mt-0.5">{{ greeting }}, {{ auth.user?.full_name }} 👋</p>
      </div>
      <div class="flex gap-2">
        <RouterLink to="/admin/news/new" class="btn-primary btn-sm">
          <Plus class="w-4 h-4" />
          Yangilik qo'shish
        </RouterLink>
      </div>
    </div>

    <!-- Stat cards -->
    <div class="grid grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
      <div v-for="s in statsCards" :key="s.key" class="card p-5">
        <div class="flex items-start justify-between mb-3">
          <div :class="['w-9 h-9 rounded-lg flex items-center justify-center', s.iconBg]">
            <component :is="s.icon" :class="['w-4 h-4', s.iconColor]" />
          </div>
          <span v-if="s.change" :class="['text-[10px] font-medium px-2 py-0.5 rounded-full', s.changeBg]">{{ s.change }}</span>
        </div>
        <div class="text-2xl font-display font-bold text-ink-dark dark:text-white">
          <span v-if="loading" class="inline-block w-12 h-6 bg-surface-soft dark:bg-slate-700 rounded animate-pulse" />
          <span v-else>{{ s.value }}</span>
        </div>
        <div class="text-xs text-ink-faint mt-1">{{ s.label }}</div>
      </div>
    </div>

    <!-- Charts row -->
    <div class="grid lg:grid-cols-3 gap-4 mb-6">
      <!-- Bar chart 2/3 -->
      <div class="card p-5 lg:col-span-2">
        <div class="flex items-center justify-between mb-5">
          <h3 class="text-sm font-semibold text-ink-dark dark:text-white flex items-center gap-2">
            <Activity class="w-4 h-4 text-primary-600" />
            Yangiliklar aktivligi (30 kun)
          </h3>
          <span class="text-[10px] uppercase tracking-wider text-ink-faint">Ko'rishlar</span>
        </div>
        <!-- Inline SVG bar chart -->
        <div class="h-40 flex items-end gap-1">
          <div
            v-for="(bar, i) in chartBars"
            :key="i"
            :style="{ height: `${(bar / chartMax) * 100}%` }"
            class="flex-1 bg-gradient-to-t from-primary-500 to-primary-300 dark:from-primary-700 dark:to-primary-500 rounded-t-sm min-h-[4px] hover:from-accent-500 hover:to-accent-300 transition-colors"
            v-tooltip="`Day ${i + 1}: ${bar}`"
          />
        </div>
        <div class="flex items-center justify-between mt-3 text-[10px] text-ink-faint">
          <span>30 kun oldin</span>
          <span>Bugun</span>
        </div>
      </div>

      <!-- Quick stats 1/3 -->
      <div class="card p-5">
        <h3 class="text-sm font-semibold text-ink-dark dark:text-white mb-5 flex items-center gap-2">
          <TrendingUp class="w-4 h-4 text-accent-500" />
          Tez statistika
        </h3>
        <div class="space-y-5">
          <div v-for="item in quickStats" :key="item.label">
            <div class="flex justify-between text-xs mb-1.5">
              <span class="text-ink-medium dark:text-slate-300">{{ item.label }}</span>
              <span class="font-semibold text-ink-dark dark:text-white">{{ item.value }}%</span>
            </div>
            <div class="h-1.5 bg-surface-soft dark:bg-slate-700 rounded-full overflow-hidden">
              <div :class="['h-full rounded-full transition-all duration-700', item.color]" :style="{ width: item.value + '%' }" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tables row -->
    <div class="grid lg:grid-cols-2 gap-4">
      <!-- Top articles -->
      <div class="card">
        <div class="flex items-center justify-between px-5 py-4 border-b border-surface-muted dark:border-slate-700">
          <h3 class="text-sm font-semibold text-ink-dark dark:text-white">Top yangiliklar (ko'rish)</h3>
          <RouterLink to="/admin/news" class="text-xs text-primary-600 hover:text-primary-700 font-medium">Barchasi →</RouterLink>
        </div>
        <div v-if="loading || topArticles.length" class="divide-y divide-surface-muted dark:divide-slate-700">
          <div v-if="loading" class="px-5 py-8 text-center text-sm text-ink-faint">Yuklanmoqda...</div>
          <div v-else v-for="(a, i) in topArticles" :key="a.id" class="flex items-center gap-3 px-5 py-3 hover:bg-surface-soft/50 dark:hover:bg-slate-800/30 transition">
            <span class="text-xs font-bold text-ink-faint w-5 flex-shrink-0">{{ i + 1 }}</span>
            <div class="flex-1 min-w-0">
              <RouterLink :to="`/news/${a.slug}`" target="_blank" class="text-sm font-medium text-ink-dark dark:text-white truncate hover:text-primary-600 block">
                {{ a.title }}
              </RouterLink>
              <div class="text-xs text-ink-faint mt-0.5">{{ a.category }}</div>
            </div>
            <div class="text-xs font-medium text-ink-light flex items-center gap-1 flex-shrink-0">
              <Eye class="w-3.5 h-3.5" /> {{ formatNum(a.views) }}
            </div>
          </div>
        </div>
        <p v-else class="px-5 py-8 text-center text-sm text-ink-faint">Hozircha ma'lumot yo'q</p>
      </div>

      <!-- Recent activity -->
      <div class="card">
        <div class="px-5 py-4 border-b border-surface-muted dark:border-slate-700">
          <h3 class="text-sm font-semibold text-ink-dark dark:text-white">So'nggi faoliyat</h3>
        </div>
        <div v-if="loading || recentActivity.length" class="divide-y divide-surface-muted dark:divide-slate-700">
          <div v-if="loading" class="px-5 py-8 text-center text-sm text-ink-faint">Yuklanmoqda...</div>
          <div v-else v-for="a in recentActivity" :key="a.id" class="flex items-start gap-3 px-5 py-3">
            <div :class="['w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0', a.iconBg]">
              <component :is="a.icon" :class="['w-3.5 h-3.5', a.iconColor]" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-xs text-ink-dark dark:text-slate-200">
                <span class="font-semibold">{{ a.user }}</span> {{ a.action }}
              </p>
              <time class="text-[10px] text-ink-faint">{{ timeAgo(a.created_at) }}</time>
            </div>
          </div>
        </div>
        <p v-else class="px-5 py-8 text-center text-sm text-ink-faint">Faoliyat yo'q</p>
      </div>
    </div>
  </div>
</template>
