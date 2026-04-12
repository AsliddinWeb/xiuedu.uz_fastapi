<script setup>
import { ref } from 'vue'
import UITabs from '@/components/ui/UITabs.vue'
import { GraduationCap, Briefcase, BookOpen, Clock, Calendar, ArrowRight } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const active = ref('bachelor')

const tabs = [
  { key: 'bachelor', label: t('nav.bachelor'),   icon: GraduationCap },
  { key: 'master',   label: t('nav.master'),     icon: BookOpen },
  { key: 'mgmt',     label: t('nav.management'), icon: Briefcase }
]

const programs = {
  bachelor: [
    { name: "Boshlang'ich ta'lim",          duration: "4 yil", cost: "16 mln", form: "Kunduzgi" },
    { name: "Maktabgacha ta'lim",           duration: "4 yil", cost: "14 mln", form: "Kunduzgi" },
    { name: "Iqtisodiyot",                  duration: "4 yil", cost: "18 mln", form: "Kunduzgi/Sirtqi" },
    { name: "Ingliz tili va adabiyoti",     duration: "4 yil", cost: "17 mln", form: "Kunduzgi" }
  ],
  master: [
    { name: "Pedagogika boshqaruvi",        duration: "2 yil", cost: "22 mln", form: "Kunduzgi" },
    { name: "Iqtisodiyot va menejment",     duration: "2 yil", cost: "24 mln", form: "Kunduzgi/Sirtqi" },
    { name: "Lingvistika",                  duration: "2 yil", cost: "21 mln", form: "Kunduzgi" }
  ],
  mgmt: [
    { name: "MBA",                          duration: "1.5 yil", cost: "32 mln", form: "Kechki" },
    { name: "Loyihalarni boshqarish",       duration: "1 yil",   cost: "26 mln", form: "Kechki" }
  ]
}
</script>

<template>
  <section class="py-24 bg-white dark:bg-primary-900">
    <div class="container-wide">
      <div class="text-center max-w-2xl mx-auto mb-12">
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-accent-500 mb-3">{{ $t('nav.education') }}</p>
        <h2 class="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-primary-700 dark:text-white">
          Yo'nalishlar
        </h2>
      </div>

      <UITabs v-model="active" :tabs="tabs">
        <template #default="{ active: a }">
          <div class="grid gap-3">
            <div
              v-for="p in programs[a]"
              :key="p.name"
              class="grid md:grid-cols-[1fr,auto,auto,auto] items-center gap-4 p-5 rounded-xl border border-neutral-200 dark:border-primary-700 bg-neutral-50 dark:bg-primary-800 hover:border-accent-500 hover:shadow-card transition group"
            >
              <h3 class="font-semibold text-primary-700 dark:text-white group-hover:text-accent-500 transition">{{ p.name }}</h3>
              <span class="text-xs text-neutral-500 dark:text-neutral-400 inline-flex items-center gap-1.5"><Clock class="w-3.5 h-3.5" /> {{ p.duration }}</span>
              <span class="text-xs text-neutral-500 dark:text-neutral-400 inline-flex items-center gap-1.5"><Calendar class="w-3.5 h-3.5" /> {{ p.form }}</span>
              <span class="text-sm font-bold text-accent-500">{{ p.cost }}</span>
            </div>
          </div>
          <div class="mt-8 text-center">
            <RouterLink :to="`/education/${a === 'master' ? 'master' : 'bachelor'}`" class="inline-flex items-center gap-2 text-accent-500 font-medium hover:gap-3 transition-all">
              {{ $t('common.read_more') }} <ArrowRight class="w-4 h-4" />
            </RouterLink>
          </div>
        </template>
      </UITabs>
    </div>
  </section>
</template>
