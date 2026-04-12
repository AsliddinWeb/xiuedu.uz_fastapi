<script setup>
/**
 * @prop {'spinner'|'skeleton-card'|'skeleton-text'|'skeleton-list'} variant
 * @prop {number} lines - for skeleton-text
 */
import { Loader2 } from 'lucide-vue-next'

defineProps({
  variant: { type: String, default: 'spinner' },
  lines: { type: Number, default: 3 }
})
</script>

<template>
  <div v-if="variant === 'spinner'" class="flex items-center justify-center p-8 text-primary-700 dark:text-accent-500">
    <Loader2 class="w-6 h-6 animate-spin" />
  </div>

  <div v-else-if="variant === 'skeleton-card'" class="rounded-xl bg-white dark:bg-primary-800 border border-neutral-200 dark:border-primary-700 overflow-hidden">
    <div class="aspect-video bg-neutral-200 dark:bg-primary-700 animate-pulse" />
    <div class="p-5 space-y-3">
      <div class="h-4 w-1/3 bg-neutral-200 dark:bg-primary-700 rounded animate-pulse" />
      <div class="h-5 w-3/4 bg-neutral-200 dark:bg-primary-700 rounded animate-pulse" />
      <div class="h-4 w-full bg-neutral-200 dark:bg-primary-700 rounded animate-pulse" />
    </div>
  </div>

  <div v-else-if="variant === 'skeleton-text'" class="space-y-2">
    <div
      v-for="n in lines"
      :key="n"
      :class="['h-3 bg-neutral-200 dark:bg-primary-700 rounded animate-pulse', n === lines ? 'w-2/3' : 'w-full']"
    />
  </div>

  <div v-else-if="variant === 'skeleton-list'" class="space-y-3">
    <div v-for="n in lines" :key="n" class="flex items-center gap-3">
      <div class="w-12 h-12 rounded-lg bg-neutral-200 dark:bg-primary-700 animate-pulse" />
      <div class="flex-1 space-y-2">
        <div class="h-3 w-2/3 bg-neutral-200 dark:bg-primary-700 rounded animate-pulse" />
        <div class="h-3 w-1/3 bg-neutral-200 dark:bg-primary-700 rounded animate-pulse" />
      </div>
    </div>
  </div>
</template>
