<script setup>
import { ServerCrash, RefreshCw, Home, Phone, Mail } from 'lucide-vue-next'
import UIButton from '@/components/ui/UIButton.vue'
import { useSeo } from '@/composables/useSeo'

defineProps({
  message: { type: String, default: '' }
})

useSeo(() => ({
  title: '500 — Server xatoligi',
  description: 'Kechirasiz, server tomonida xatolik yuz berdi.',
  noIndex: true
}))

function reload() { window.location.reload() }
</script>

<template>
  <section class="min-h-[80vh] grid place-items-center px-4 bg-white dark:bg-primary-900">
    <div class="text-center max-w-xl">
      <ServerCrash class="w-24 h-24 text-danger mx-auto mb-6" stroke-width="1.4" />
      <p class="text-xs font-semibold uppercase tracking-[0.2em] text-accent-500 mb-3">500 · Internal server error</p>
      <h1 class="font-display text-4xl md:text-5xl font-bold text-primary-700 dark:text-white mb-4">Server xatoligi</h1>

      <div class="space-y-1 text-neutral-500 dark:text-neutral-400 mb-8">
        <p>🇺🇿 Kechirasiz, server tomonida xatolik yuz berdi. Iltimos, birozdan keyin qayta urinib ko'ring.</p>
        <p>🇷🇺 Извините, на сервере произошла ошибка. Попробуйте позже.</p>
        <p>🇬🇧 Sorry, something went wrong on our server. Please try again later.</p>
      </div>

      <p v-if="message" class="text-xs font-mono text-danger bg-red-50 dark:bg-red-900/20 p-3 rounded mb-6">
        {{ message }}
      </p>

      <div class="flex flex-wrap items-center justify-center gap-3 mb-8">
        <UIButton variant="primary" @click="reload">
          <template #icon-left><RefreshCw class="w-4 h-4" /></template>
          Qayta urinib ko'rish
        </UIButton>
        <UIButton variant="outline" to="/">
          <template #icon-left><Home class="w-4 h-4" /></template>
          Bosh sahifa
        </UIButton>
      </div>

      <div class="flex flex-wrap items-center justify-center gap-5 text-sm text-neutral-500 dark:text-neutral-400">
        <a href="tel:+998554061515" class="inline-flex items-center gap-1.5 hover:text-accent-500 transition"><Phone class="w-4 h-4" /> +998 55 406-15-15</a>
        <a href="mailto:info@xiuedu.uz" class="inline-flex items-center gap-1.5 hover:text-accent-500 transition"><Mail class="w-4 h-4" /> info@xiuedu.uz</a>
      </div>
    </div>
  </section>
</template>
