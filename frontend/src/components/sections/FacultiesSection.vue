<script setup>
import { GraduationCap, TrendingUp, Languages, ArrowRight } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const faculties = [
  {
    icon: GraduationCap,
    titleKey: 'faculties.pedagogika',
    slug: 'pedagogika',
    desc: "Boshlang'ich va o'rta ta'lim yo'nalishlari",
    departments: 5,
    students: 1800,
    color: 'from-primary-600 to-primary-800'
  },
  {
    icon: TrendingUp,
    titleKey: 'faculties.iqtisodiyot',
    slug: 'iqtisodiyot',
    desc: "Iqtisodiyot, marketing, moliya",
    departments: 4,
    students: 1500,
    color: 'from-accent-600 to-accent-800'
  },
  {
    icon: Languages,
    titleKey: 'faculties.filologiya',
    slug: 'filologiya',
    desc: "Tilshunoslik va xalqaro filologiya",
    departments: 3,
    students: 1200,
    color: 'from-primary-700 to-primary-900'
  }
]
</script>

<template>
  <section class="py-24 bg-neutral-50 dark:bg-primary-950">
    <div class="container-wide">
      <div class="max-w-2xl mb-12">
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-accent-500 mb-3">{{ t('faculties.subtitle') }}</p>
        <h2 class="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-primary-700 dark:text-white">
          {{ t('faculties.title') }}
        </h2>
      </div>

      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <RouterLink
          v-for="f in faculties"
          :key="f.slug"
          :to="`/faculties/${f.slug}`"
          class="group relative overflow-hidden rounded-2xl bg-white dark:bg-primary-800 border border-neutral-200 dark:border-primary-700 shadow-card hover:shadow-soft hover:-translate-y-1 transition-all duration-300"
        >
          <div :class="['relative h-44 bg-gradient-to-br', f.color, 'flex items-center justify-center overflow-hidden']">
            <component :is="f.icon" class="w-20 h-20 text-white/80 group-hover:scale-110 transition-transform duration-500" stroke-width="1.2" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent" />
          </div>
          <div class="p-6">
            <h3 class="font-display font-semibold text-xl text-primary-700 dark:text-white mb-2 group-hover:text-accent-500 transition">
              {{ t(f.titleKey) }}
            </h3>
            <p class="text-sm text-neutral-500 dark:text-neutral-400 mb-5">{{ f.desc }}</p>
            <div class="flex items-center justify-between text-xs text-neutral-500 dark:text-neutral-400 mb-4">
              <span><strong class="text-primary-700 dark:text-accent-500">{{ f.departments }}</strong> {{ t('faculties.departments').toLowerCase() }}</span>
              <span><strong class="text-primary-700 dark:text-accent-500">{{ f.students }}</strong> {{ t('faculties.students') }}</span>
            </div>
            <span class="inline-flex items-center gap-1 text-sm font-medium text-accent-500 group-hover:gap-2 transition-all">
              {{ t('common.read_more') }} <ArrowRight class="w-4 h-4" />
            </span>
          </div>
        </RouterLink>
      </div>
    </div>
  </section>
</template>
