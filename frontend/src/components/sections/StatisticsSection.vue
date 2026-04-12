<script setup>
import { Users, GraduationCap, BookOpen, Globe2 } from 'lucide-vue-next'
import { useReveal } from '@/composables/useReveal'
import { useCounter } from '@/composables/useCounter'

const { target, visible } = useReveal()

const c1 = useCounter(5000, visible)
const c2 = useCounter(150,  visible)
const c3 = useCounter(12,   visible)
const c4 = useCounter(50,   visible)

const items = [
  { icon: Users,         value: c1, suffix: '+', key: 'home.stats_students' },
  { icon: GraduationCap, value: c2, suffix: '+', key: 'home.stats_faculty' },
  { icon: BookOpen,      value: c3, suffix: '',  key: 'home.stats_programs' },
  { icon: Globe2,        value: c4, suffix: '+', key: 'home.stats_partners' }
]
</script>

<template>
  <section ref="target" class="py-20 bg-gradient-to-br from-primary-700 via-primary-800 to-primary-900 text-white relative overflow-hidden">
    <div class="absolute inset-0 opacity-[0.04]" style="background-image: radial-gradient(circle at 20% 50%, white 1px, transparent 1px); background-size: 24px 24px;" />
    <div class="container-wide relative grid grid-cols-2 lg:grid-cols-4 gap-6">
      <div
        v-for="(s, i) in items"
        :key="s.key"
        class="text-center px-4 py-6 rounded-2xl border border-white/10 bg-white/5 backdrop-blur"
        :style="{ animationDelay: `${i * 80}ms` }"
      >
        <component :is="s.icon" class="w-10 h-10 text-accent-500 mx-auto mb-4" stroke-width="1.5" />
        <div class="font-display text-4xl md:text-5xl font-bold tracking-tight">
          {{ s.value }}<span class="text-accent-500">{{ s.suffix }}</span>
        </div>
        <div class="mt-2 text-sm text-neutral-300">{{ $t(s.key) }}</div>
      </div>
    </div>
  </section>
</template>
