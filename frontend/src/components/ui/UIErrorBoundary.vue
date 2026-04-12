<script setup>
/**
 * Vue error boundary — catches descendant errors and shows ServerErrorView.
 *
 * Usage:
 *   <UIErrorBoundary>
 *     <RouterView />
 *   </UIErrorBoundary>
 */
import { ref, onErrorCaptured } from 'vue'
import ServerErrorView from '@/views/public/ServerErrorView.vue'

const error = ref(null)

onErrorCaptured((err) => {
  error.value = err
  // Log to console in dev; integrate Sentry in prod here
  console.error('[ErrorBoundary]', err)
  // Returning false stops propagation
  return false
})

function reset() { error.value = null }

defineExpose({ reset })
</script>

<template>
  <ServerErrorView v-if="error" :message="error?.message || ''" />
  <slot v-else />
</template>
