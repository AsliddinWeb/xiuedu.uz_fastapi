<script setup>
import PageHero from '@/components/sections/PageHero.vue'
import {
  Monitor, BookOpen, Calendar, FileText, Users, Trophy,
  ChevronRight, Image as ImageIcon, ArrowRight
} from 'lucide-vue-next'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { useSeo } from '@/composables/useSeo'
import { breadcrumbSchema } from '@/utils/schema'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
useScrollAnimation()
useSeo(() => ({
  title: t('students.title'),
  description: t('students.subtitle'),
  schema: breadcrumbSchema([
    { name: t('nav.home'), url: '/' },
    { name: t('students.title'), url: '/students' }
  ])
}))

const quickLinks = [
  { icon: Monitor,  label: 'HEMIS tizimi',     desc: 'Baholar va jadval', href: 'https://student.xiuedu.uz', external: true },
  { icon: BookOpen, label: 'Onlayn kurslar',   desc: 'E-learning platform', to: '/p/courses' },
  { icon: Calendar, label: 'Dars jadvallari',  desc: 'Joriy semestr', to: '/p/schedule' },
  { icon: FileText, label: 'Imtihonlar',       desc: 'Jadval va natijalar', to: '/p/exams' },
  { icon: Users,    label: 'Klublar',          desc: 'Qiziqishlarga ko\'ra', to: '/p/clubs/youth' },
  { icon: Trophy,   label: 'Sport',            desc: 'Sport bo\'limlari', to: '/p/sport' }
]

const clubs = [
  { title: 'Yoshlar ittifoqi', desc: 'Talabalar tashabbuslari va volontyorlik dasturlari.',     hue: 215 },
  { title: 'Ingliz tili klubi', desc: 'Cambridge English bilan haftalik mashg\'ulotlar.',     hue: 30 },
  { title: 'Fintech klubi',     desc: 'Moliya texnologiyalari va startaplar bo\'yicha tadqiqot.', hue: 270 }
]

const sports = [
  { title: 'Futbol',    sub: 'Erkaklar va ayollar jamoalari' },
  { title: 'Voleybol',  sub: 'Universitet jamoasi' },
  { title: 'Basketbol', sub: 'Yangi mavsum boshlandi' },
  { title: 'Shaxmat',   sub: 'Klub mashg\'ulotlari' }
]
</script>

<template>
  <div>
    <PageHero
      :title="t('students.title')"
      :subtitle="t('students.subtitle')"
      :items="[{ label: t('students.title'), to: '/students' }]"
      variant="navy"
    />

    <!-- ===== Quick links ===== -->
    <section class="section bg-surface-light dark:bg-slate-900">
      <div class="container-narrow">
        <div class="text-center mb-12" data-animate>
          <span class="badge-primary mb-3 inline-block">Tezkor havolalar</span>
          <h2 class="section-title">Talabalar uchun xizmatlar</h2>
        </div>
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <component
            v-for="(l, i) in quickLinks"
            :key="l.label"
            :is="l.external ? 'a' : 'router-link'"
            :href="l.external ? l.href : undefined"
            :to="!l.external ? l.to : undefined"
            :target="l.external ? '_blank' : undefined"
            :rel="l.external ? 'noopener' : undefined"
            class="card-hover p-6 group"
            data-animate
            :data-delay="i * 80"
          >
            <div class="flex items-start gap-4">
              <div class="w-12 h-12 rounded-xl bg-primary-100 dark:bg-primary-900/40 grid place-items-center text-primary-600 dark:text-primary-300 flex-shrink-0">
                <component :is="l.icon" class="w-6 h-6" />
              </div>
              <div class="flex-1">
                <h3 class="font-display font-semibold text-ink-dark dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-300 transition">{{ l.label }}</h3>
                <p class="text-sm text-ink-light dark:text-slate-400 mt-1">{{ l.desc }}</p>
              </div>
              <ChevronRight class="w-5 h-5 text-ink-faint group-hover:text-accent-500 group-hover:translate-x-1 transition-all flex-shrink-0" />
            </div>
          </component>
        </div>
      </div>
    </section>

    <!-- ===== Clubs ===== -->
    <section class="section bg-white dark:bg-slate-800">
      <div class="container-narrow">
        <div class="text-center mb-12" data-animate>
          <span class="badge-accent mb-3 inline-block">Talabalar klublari</span>
          <h2 class="section-title">Qiziqishlarga ko'ra to'garaklar</h2>
        </div>
        <div class="grid md:grid-cols-3 gap-6">
          <div
            v-for="(c, i) in clubs"
            :key="c.title"
            class="card-hover overflow-hidden"
            data-animate
            :data-delay="i * 100"
          >
            <div
              class="aspect-[16/10] grid place-items-center"
              :style="{ background: `linear-gradient(135deg, hsl(${c.hue},45%,30%), hsl(${c.hue + 25},55%,18%))` }"
            >
              <ImageIcon class="w-12 h-12 text-white/30" stroke-width="1.2" />
            </div>
            <div class="p-6">
              <h3 class="font-display font-bold text-lg text-ink-dark dark:text-white mb-2">{{ c.title }}</h3>
              <p class="text-sm text-ink-light dark:text-slate-400">{{ c.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== Sport ===== -->
    <section class="section bg-surface-light dark:bg-slate-900">
      <div class="container-narrow">
        <div class="text-center mb-12" data-animate>
          <span class="badge-primary mb-3 inline-block">Sport</span>
          <h2 class="section-title">Sport bo'limlari</h2>
        </div>
        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div
            v-for="(s, i) in sports"
            :key="s.title"
            class="card-hover p-6 text-center"
            data-animate
            :data-delay="i * 80"
          >
            <div class="w-14 h-14 mx-auto mb-4 rounded-2xl bg-accent-100 dark:bg-accent-900/40 grid place-items-center text-accent-600 dark:text-accent-300">
              <Trophy class="w-7 h-7" stroke-width="1.6" />
            </div>
            <h3 class="font-display font-semibold text-ink-dark dark:text-white">{{ s.title }}</h3>
            <p class="text-xs text-ink-light dark:text-slate-400 mt-1">{{ s.sub }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== Gallery preview ===== -->
    <section class="section bg-white dark:bg-slate-800">
      <div class="container-narrow">
        <div class="text-center mb-10" data-animate>
          <span class="badge-accent mb-3 inline-block">Talabalar hayoti</span>
          <h2 class="section-title">Lahzalar va hotiralar</h2>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div
            v-for="i in 8"
            :key="i"
            class="aspect-square rounded-xl overflow-hidden relative"
            :style="{ background: `linear-gradient(135deg, hsl(${200 + i * 18},45%,30%), hsl(${220 + i * 18},55%,18%))` }"
          >
            <ImageIcon class="absolute inset-0 m-auto w-10 h-10 text-white/30" />
          </div>
        </div>
        <div class="text-center mt-8">
          <RouterLink to="/gallery" class="btn-outline btn-md inline-flex">
            Galereyani ko'rish <ArrowRight class="w-4 h-4" />
          </RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>
