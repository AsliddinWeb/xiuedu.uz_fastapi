<script setup>
const partners = [
  'Cambridge', 'Oxford', 'Sorbonne', 'TU Berlin', 'KAIST', 'ETH Zurich',
  'Bocconi', 'NUS', 'McGill', 'KU Leuven', 'Lund', 'Tsinghua'
]
const loop = [...partners, ...partners]
</script>

<template>
  <section class="py-16 bg-white dark:bg-primary-900 border-y border-neutral-200 dark:border-primary-800">
    <div class="container-wide">
      <p class="text-center text-xs font-semibold uppercase tracking-[0.2em] text-neutral-500 dark:text-neutral-400 mb-8">
        Xalqaro hamkorlar
      </p>
    </div>
    <div class="overflow-hidden relative" style="mask-image: linear-gradient(90deg, transparent, black 10%, black 90%, transparent);">
      <div class="flex gap-12 animate-[slide_30s_linear_infinite] whitespace-nowrap will-change-transform">
        <div
          v-for="(p, i) in loop"
          :key="i"
          class="px-8 py-4 rounded-xl border border-neutral-200 dark:border-primary-700 text-neutral-500 dark:text-neutral-300 font-display font-semibold text-lg flex-shrink-0"
        >
          {{ p }}
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
@keyframes slide {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
</style>
