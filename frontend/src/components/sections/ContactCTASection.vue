<script setup>
import { ArrowRight, Phone } from 'lucide-vue-next'
import UIButton from '@/components/ui/UIButton.vue'
</script>

<template>
  <section class="relative py-24 bg-navy-gradient text-white overflow-hidden">
    <div class="absolute inset-0 opacity-[0.05]" style="background-image: radial-gradient(circle at 30% 30%, white 1px, transparent 1px); background-size: 32px 32px;" />
    <div class="absolute -top-32 -right-32 w-[28rem] h-[28rem] rounded-full bg-accent-500/15 blur-3xl pointer-events-none" />

    <div class="container-wide relative grid lg:grid-cols-2 gap-10 items-center">
      <div>
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-accent-500 mb-3">{{ $t('home.apply_title') }}</p>
        <h2 class="font-display text-3xl md:text-4xl lg:text-5xl font-bold mb-5 leading-tight">
          {{ $t('home.apply_text') }}
        </h2>
        <div class="flex flex-wrap gap-3">
          <UIButton variant="accent" size="lg" to="/applicants">
            {{ $t('home.apply_button') }}
            <template #icon-right><ArrowRight class="w-4 h-4" /></template>
          </UIButton>
          <UIButton size="lg" href="tel:+998554061515" class="!bg-white/10 !text-white !border !border-white/30 hover:!bg-white hover:!text-primary-900">
            <template #icon-left><Phone class="w-4 h-4" /></template>
            +998 55 406-15-15
          </UIButton>
        </div>
      </div>

      <div class="hidden lg:flex justify-end">
        <div class="relative w-96 h-96 rounded-3xl bg-gradient-to-br from-accent-500/30 to-accent-700/10 backdrop-blur border border-white/10 grid place-items-center">
          <span class="font-display text-9xl font-bold text-accent-500/80">X</span>
          <div class="absolute -top-4 -right-4 px-4 py-2 rounded-xl bg-accent-500 text-primary-900 text-xs font-bold uppercase tracking-wider shadow-glow">
            2026 / 2027
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
