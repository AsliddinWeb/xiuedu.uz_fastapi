<script setup>
/**
 * About page CMS — vertical sidebar with sub-views.
 */
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { LayoutPanelLeft, UserCircle, Compass, MapPin, Clock, Award } from 'lucide-vue-next'

import HeroTab from './tabs/HeroTab.vue'
import RectorTab from './tabs/RectorTab.vue'
import MvvTab from './tabs/MvvTab.vue'
import AddressTab from './tabs/AddressTab.vue'
import TimelineTab from './tabs/TimelineTab.vue'
import AccreditationsTab from './tabs/AccreditationsTab.vue'

const route = useRoute()
const router = useRouter()

const tabs = [
  { key: 'hero',    label: 'Hero / Sarlavha', icon: LayoutPanelLeft, component: HeroTab },
  { key: 'rector',  label: 'Rektor murojaati', icon: UserCircle,     component: RectorTab },
  { key: 'mvv',     label: 'Missiya / Vizyon', icon: Compass,        component: MvvTab },
  { key: 'address', label: 'Manzil / Xarita',  icon: MapPin,         component: AddressTab },
  { key: 'timeline', label: 'Tarix (timeline)', icon: Clock,         component: TimelineTab },
  { key: 'accreditations', label: 'Akkreditatsiya', icon: Award,     component: AccreditationsTab }
]

const activeKey = ref(route.hash.replace('#', '') || 'hero')
const activeTab = computed(() => tabs.find(t => t.key === activeKey.value) || tabs[0])

watch(activeKey, (k) => router.replace({ hash: `#${k}` }))
onMounted(() => { if (!route.hash) router.replace({ hash: '#hero' }) })
</script>

<template>
  <div>
    <div class="mb-6">
      <h1 class="text-xl font-display font-bold text-ink-dark dark:text-white">Universitet haqida sahifasi</h1>
      <p class="text-sm text-ink-faint mt-0.5">Hero, rektor murojaati, missiya/vizyon, manzil, timeline va akkreditatsiya</p>
    </div>

    <div class="grid lg:grid-cols-[220px_1fr] gap-6">
      <aside class="lg:sticky lg:top-4 self-start">
        <nav class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-2 space-y-0.5">
          <button
            v-for="t in tabs"
            :key="t.key"
            type="button"
            @click="activeKey = t.key"
            :class="[
              'w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition-colors text-left',
              activeKey === t.key
                ? 'bg-primary-50 text-primary-800 font-semibold dark:bg-primary-900/40 dark:text-white'
                : 'text-ink-medium dark:text-slate-300 hover:bg-surface-soft dark:hover:bg-slate-700/40'
            ]"
          >
            <component :is="t.icon" class="w-4 h-4 flex-shrink-0" />
            <span class="truncate">{{ t.label }}</span>
          </button>
        </nav>
      </aside>

      <div class="rounded-2xl bg-surface-light dark:bg-slate-900/40 p-6 border border-surface-muted dark:border-slate-700 min-h-[400px]">
        <component :is="activeTab.component" :key="activeKey" />
      </div>
    </div>
  </div>
</template>
