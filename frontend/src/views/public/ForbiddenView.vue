<script setup>
import { ShieldX } from 'lucide-vue-next'
import UIButton from '@/components/ui/UIButton.vue'
</script>

<template>
  <section class="min-h-[60vh] grid place-items-center px-4">
    <div class="text-center max-w-md">
      <ShieldX class="w-20 h-20 text-danger mx-auto mb-5" stroke-width="1.4" />
      <h1 class="font-display text-4xl font-bold text-primary-700 dark:text-white mb-3">403</h1>
      <p class="text-neutral-500 dark:text-neutral-400 mb-6">{{ $t('errors.forbidden') }}</p>
      <UIButton variant="primary" to="/">{{ $t('errors.go_home') }}</UIButton>
    </div>
  </section>
</template>
