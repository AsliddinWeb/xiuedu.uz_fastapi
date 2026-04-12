<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { ArrowDown, GraduationCap, Users, BookOpen, Award } from 'lucide-vue-next'
import UIButton from '@/components/ui/UIButton.vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Typed-effect headline
const fullText = ref('')
const display = ref('')
let timer = null

function startTyping() {
  fullText.value = t('home.hero_title')
  display.value = ''
  let i = 0
  timer = setInterval(() => {
    display.value = fullText.value.slice(0, ++i)
    if (i >= fullText.value.length) clearInterval(timer)
  }, 35)
}

onMounted(startTyping)
onBeforeUnmount(() => timer && clearInterval(timer))

const stats = [
  { icon: Users,         value: '5000+', key: 'home.stats_students' },
  { icon: GraduationCap, value: '150+',  key: 'home.stats_faculty' },
  { icon: BookOpen,      value: '12',    key: 'home.stats_programs' },
  { icon: Award,         value: '15',    key: 'home.stats_years' }
]
</script>

<template>
  <section class="relative min-h-[92vh] flex items-center overflow-hidden bg-navy-gradient text-white">
    <!-- Background pattern + glow -->
    <div class="absolute inset-0 opacity-30 pointer-events-none">
      <div class="absolute top-1/4 -left-32 w-[28rem] h-[28rem] bg-accent-500/20 rounded-full blur-3xl" />
      <div class="absolute bottom-0 right-0 w-[32rem] h-[32rem] bg-primary-500/20 rounded-full blur-3xl" />
    </div>
    <div
      class="absolute inset-0 opacity-[0.04]"
      style="background-image: linear-gradient(rgba(255,255,255,.4) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.4) 1px, transparent 1px); background-size: 60px 60px;"
    />

    <div class="container-wide relative grid lg:grid-cols-12 gap-12 items-center py-24">
      <div class="lg:col-span-7">
        <div class="inline-flex items-center gap-2 px-3 py-1 mb-6 rounded-full border border-accent-500/40 bg-accent-500/10 text-accent-300 text-xs font-semibold uppercase tracking-wider">
          <span class="w-1.5 h-1.5 rounded-full bg-accent-500 animate-pulse" />
          {{ t('site.short') }} · Premium University
        </div>
        <h1 class="font-display text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-bold leading-[1.05] mb-6 min-h-[4.5rem] sm:min-h-[6rem]">
          {{ display }}<span class="inline-block w-1 h-[0.85em] bg-accent-500 ml-1 align-middle animate-pulse" />
        </h1>
        <p class="text-lg lg:text-xl text-neutral-300 max-w-2xl leading-relaxed mb-9">
          {{ t('home.hero_subtitle') }}
        </p>
        <div class="flex flex-wrap gap-3">
          <UIButton variant="accent" size="lg" to="/applicants">{{ t('home.hero_cta') }}</UIButton>
          <UIButton size="lg" to="/about" class="!bg-white/10 !text-white !border !border-white/30 hover:!bg-white hover:!text-primary-900 backdrop-blur">
            {{ t('home.hero_secondary') }}
          </UIButton>
        </div>
      </div>

      <!-- Floating stats -->
      <div class="lg:col-span-5 grid grid-cols-2 gap-3 sm:gap-4">
        <div
          v-for="(s, i) in stats"
          :key="s.key"
          class="rounded-2xl p-5 backdrop-blur bg-white/10 border border-white/20 shadow-soft animate-slide-up"
          :style="{ animationDelay: `${i * 80}ms`, animationFillMode: 'both' }"
        >
          <component :is="s.icon" class="w-7 h-7 text-accent-500 mb-3" />
          <div class="font-display text-2xl sm:text-3xl font-bold">{{ s.value }}</div>
          <div class="text-xs text-neutral-300 mt-1">{{ t(s.key) }}</div>
        </div>
      </div>
    </div>

    <!-- Scroll indicator -->
    <a href="#about" class="absolute bottom-6 left-1/2 -translate-x-1/2 text-white/60 hover:text-accent-500 transition" aria-label="Scroll">
      <ArrowDown class="w-6 h-6 animate-bounce" />
    </a>
  </section>
</template>
