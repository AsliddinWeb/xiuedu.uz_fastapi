<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  LayoutPanelLeft, ListOrdered, BookOpenCheck, Calendar, FileText, HelpCircle, Megaphone
} from 'lucide-vue-next'

import HeroTab from './tabs/HeroTab.vue'
import StepsTab from './tabs/StepsTab.vue'
import FormsTab from './tabs/FormsTab.vue'
import TimelineTab from './tabs/TimelineTab.vue'
import DocsTab from './tabs/DocsTab.vue'
import FaqsTab from './tabs/FaqsTab.vue'
import CtaTab from './tabs/CtaTab.vue'

const route = useRoute()
const router = useRouter()

const tabs = [
  { key: 'hero',     label: 'Hero / Sarlavhalar', icon: LayoutPanelLeft, component: HeroTab },
  { key: 'steps',    label: 'Qabul qadamlari',    icon: ListOrdered,     component: StepsTab },
  { key: 'forms',    label: "Ta'lim shakllari",   icon: BookOpenCheck,   component: FormsTab },
  { key: 'timeline', label: 'Sanalar',            icon: Calendar,        component: TimelineTab },
  { key: 'docs',     label: 'Hujjatlar',          icon: FileText,        component: DocsTab },
  { key: 'faqs',     label: 'FAQ',                icon: HelpCircle,      component: FaqsTab },
  { key: 'cta',      label: 'Yakuniy CTA',        icon: Megaphone,       component: CtaTab }
]

const activeKey = ref(route.hash.replace('#', '') || 'hero')
const activeTab = computed(() => tabs.find(t => t.key === activeKey.value) || tabs[0])
watch(activeKey, (k) => router.replace({ hash: `#${k}` }))
onMounted(() => { if (!route.hash) router.replace({ hash: '#hero' }) })
</script>

<template>
  <div>
    <div class="mb-6">
      <h1 class="text-xl font-display font-bold text-ink-dark dark:text-white">Abituriyentlarga sahifasi</h1>
      <p class="text-sm text-ink-faint mt-0.5">Qabul jarayoni, ta'lim shakllari, hujjatlar va FAQ</p>
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
