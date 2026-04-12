<script setup>
/**
 * Home page CMS — vertical sidebar with 14 sub-views.
 * URL hash drives the active tab so admins can deep-link.
 */
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  Sparkles, LayoutGrid, MousePointerClick, Star, Building2, Trophy,
  GraduationCap, ListOrdered, BarChart3, MessageSquareQuote, Globe,
  FileBadge, HelpCircle, Megaphone
} from 'lucide-vue-next'

import HeroTab from './tabs/HeroTab.vue'
import SectionsTab from './tabs/SectionsTab.vue'
import QuickActionsTab from './tabs/QuickActionsTab.vue'
import IntroPillarsTab from './tabs/IntroPillarsTab.vue'
import CampusTab from './tabs/CampusTab.vue'
import WhyCardsTab from './tabs/WhyCardsTab.vue'
import FacultiesTab from './tabs/FacultiesTab.vue'
import AdmissionStepsTab from './tabs/AdmissionStepsTab.vue'
import StatsTab from './tabs/StatsTab.vue'
import TestimonialsTab from './tabs/TestimonialsTab.vue'
import PartnersTab from './tabs/PartnersTab.vue'
import LicensesTab from './tabs/LicensesTab.vue'
import FaqsTab from './tabs/FaqsTab.vue'
import FinalCtaTab from './tabs/FinalCtaTab.vue'

const route = useRoute()
const router = useRouter()

const tabs = [
  { key: 'hero',           label: 'Hero',                icon: Sparkles,           component: HeroTab },
  { key: 'sections',       label: 'Sectionlar',          icon: LayoutGrid,         component: SectionsTab },
  { key: 'quick-actions',  label: 'Tezkor tugmalar',     icon: MousePointerClick,  component: QuickActionsTab },
  { key: 'intro-pillars',  label: 'Intro pillarlar',     icon: Star,               component: IntroPillarsTab },
  { key: 'campus',         label: 'Kampus',              icon: Building2,          component: CampusTab },
  { key: 'why-cards',      label: 'Why XIU',             icon: Trophy,             component: WhyCardsTab },
  { key: 'faculties',      label: 'Fakultetlar',         icon: GraduationCap,      component: FacultiesTab },
  { key: 'admission',      label: 'Qabul jarayoni',      icon: ListOrdered,        component: AdmissionStepsTab },
  { key: 'stats',          label: 'Raqamlar',            icon: BarChart3,          component: StatsTab },
  { key: 'testimonials',   label: 'Sharhlar',            icon: MessageSquareQuote, component: TestimonialsTab },
  { key: 'partners',       label: 'Hamkorlar',           icon: Globe,              component: PartnersTab },
  { key: 'licenses',       label: 'Litsenziyalar',       icon: FileBadge,          component: LicensesTab },
  { key: 'faqs',           label: 'FAQ',                 icon: HelpCircle,         component: FaqsTab },
  { key: 'final-cta',      label: 'Yakuniy CTA',         icon: Megaphone,          component: FinalCtaTab }
]

const activeKey = ref(route.hash.replace('#', '') || 'hero')
const activeTab = computed(() => tabs.find(t => t.key === activeKey.value) || tabs[0])

watch(activeKey, (k) => router.replace({ hash: `#${k}` }))
onMounted(() => {
  if (!route.hash) router.replace({ hash: '#hero' })
})
</script>

<template>
  <div>
    <!-- Page header -->
    <div class="mb-6">
      <h1 class="text-xl font-display font-bold text-ink-dark dark:text-white">Bosh sahifa sozlamalari</h1>
      <p class="text-sm text-ink-faint mt-0.5">Hero, sectionlar va barcha home content blockslarini boshqarish</p>
    </div>

    <div class="grid lg:grid-cols-[220px_1fr] gap-6">
      <!-- Vertical tab nav -->
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

      <!-- Active tab content -->
      <div class="rounded-2xl bg-surface-light dark:bg-slate-900/40 p-6 border border-surface-muted dark:border-slate-700 min-h-[400px]">
        <component :is="activeTab.component" :key="activeKey" />
      </div>
    </div>
  </div>
</template>
