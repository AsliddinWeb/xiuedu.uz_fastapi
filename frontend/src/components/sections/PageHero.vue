<script setup>
import UIBreadcrumb from '@/components/ui/UIBreadcrumb.vue'

defineProps({
  title:    { type: String, required: true },
  subtitle: { type: String, default: '' },
  items:    { type: Array, default: null },     // breadcrumb items
  variant:  { type: String, default: 'navy' },  // 'navy' | 'orange' | 'light'
  align:    { type: String, default: 'left' }   // 'left' | 'center'
})
</script>

<template>
  <section
    :class="[
      'relative overflow-hidden pt-10 pb-14 md:pt-14 md:pb-20',
      variant === 'orange' && 'bg-gradient-to-br from-accent-600 via-accent-500 to-accent-400 text-white',
      variant === 'navy'   && 'text-white',
      variant === 'light'  && 'bg-surface-light dark:bg-slate-900'
    ]"
    :style="variant === 'navy' ? 'background: linear-gradient(135deg, #0A0D3D 0%, #1A1F6E 50%, #2D3A8C 100%);' : ''"
  >
    <div
      v-if="variant !== 'light'"
      class="absolute inset-0 opacity-[0.07] pointer-events-none"
      style="background-image: linear-gradient(rgba(255,255,255,.4) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.4) 1px, transparent 1px); background-size: 60px 60px;"
    />
    <div
      v-if="variant === 'navy'"
      class="absolute -top-32 -right-32 w-96 h-96 rounded-full bg-accent-500/10 blur-3xl pointer-events-none"
    />

    <div :class="['container-narrow relative', align === 'center' && 'text-center']">
      <UIBreadcrumb
        :items="items"
        :class="[
          align === 'center' && 'flex justify-center',
          variant !== 'light'
            ? '[&_a]:text-white/70 [&_a:hover]:text-accent-300 [&_span:last-child]:text-white [&_svg]:text-white/40'
            : ''
        ]"
      />

      <h1
        :class="[
          'mt-4 text-3xl md:text-4xl lg:text-5xl font-display font-bold leading-tight',
          variant === 'light' ? 'text-primary-800 dark:text-white' : 'text-white'
        ]"
      >
        {{ title }}
      </h1>
      <p
        v-if="subtitle"
        :class="[
          'mt-3 text-lg max-w-2xl',
          align === 'center' && 'mx-auto',
          variant === 'light' ? 'text-ink-light dark:text-slate-400' : 'text-slate-200/90'
        ]"
      >
        {{ subtitle }}
      </p>
    </div>
  </section>
</template>
