<script setup>
import { Sparkles, Globe2, Award, BookOpen } from 'lucide-vue-next'
import { useReveal } from '@/composables/useReveal'

const { target, visible } = useReveal()

const features = [
  { icon: Globe2,   title: 'Xalqaro standartlar', text: 'Yevropa universitetlari bilan hamkorlik dasturlari' },
  { icon: Award,    title: 'Akkreditatsiya',     text: 'Davlat va xalqaro akkreditatsiyaga ega dasturlar' },
  { icon: BookOpen, title: 'Tajribali ustozlar', text: 'Jahon darajasidagi professorlar va amaliyotchilar' },
  { icon: Sparkles, title: 'Innovatsiya',        text: 'Zamonaviy laboratoriyalar va raqamli infratuzilma' }
]
</script>

<template>
  <section id="about" ref="target" class="py-24 bg-white dark:bg-primary-900">
    <div class="container-wide grid lg:grid-cols-2 gap-14 items-center">
      <!-- Image montage -->
      <div :class="['grid grid-cols-2 gap-3', visible && 'animate-fade-in']">
        <div class="space-y-3">
          <div class="aspect-[4/5] rounded-2xl bg-gradient-to-br from-primary-700 to-primary-900 grid place-items-center text-accent-500/80 shadow-soft">
            <BookOpen class="w-16 h-16" stroke-width="1.2" />
          </div>
          <div class="aspect-square rounded-2xl bg-gradient-to-br from-accent-500/30 to-accent-700/10 grid place-items-center text-accent-700/70 shadow-soft">
            <Award class="w-14 h-14" stroke-width="1.2" />
          </div>
        </div>
        <div class="space-y-3 mt-8">
          <div class="aspect-square rounded-2xl bg-gradient-to-br from-primary-100 to-primary-300 dark:from-primary-700 dark:to-primary-800 grid place-items-center text-primary-700 dark:text-accent-500 shadow-soft">
            <Globe2 class="w-14 h-14" stroke-width="1.2" />
          </div>
          <div class="aspect-[4/5] rounded-2xl bg-gradient-to-br from-accent-500 to-accent-700 grid place-items-center text-primary-900 shadow-glow">
            <Sparkles class="w-16 h-16" stroke-width="1.2" />
          </div>
        </div>
      </div>

      <!-- Text + features -->
      <div :class="visible && 'animate-slide-up'">
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-accent-500 mb-3">{{ $t('home.why_subtitle') }}</p>
        <h2 class="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-primary-700 dark:text-white mb-6">
          {{ $t('home.why_title') }}
        </h2>
        <p class="text-neutral-600 dark:text-neutral-300 leading-relaxed mb-8">
          {{ $t('site.tagline') }} — {{ $t('home.hero_subtitle') }}
        </p>

        <div class="grid sm:grid-cols-2 gap-4">
          <div
            v-for="f in features"
            :key="f.title"
            class="p-4 rounded-xl border border-neutral-200 dark:border-primary-700 bg-neutral-50 dark:bg-primary-800 hover:border-accent-500 hover:shadow-card transition"
          >
            <div class="w-10 h-10 mb-3 rounded-lg bg-accent-500/10 grid place-items-center text-accent-500">
              <component :is="f.icon" class="w-5 h-5" />
            </div>
            <h3 class="font-semibold text-primary-700 dark:text-white mb-1">{{ f.title }}</h3>
            <p class="text-xs text-neutral-500 dark:text-neutral-400 leading-relaxed">{{ f.text }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
