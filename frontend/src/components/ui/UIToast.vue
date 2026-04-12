<script setup>
/**
 * Mount once globally; reads from useToastStore.
 */
import { CheckCircle2, AlertCircle, AlertTriangle, Info, X } from 'lucide-vue-next'
import { useToastStore } from '@/stores/toast'

const toast = useToastStore()

const config = {
  success: { icon: CheckCircle2, cls: 'border-green-200 dark:border-green-900 text-green-700 dark:text-green-300' },
  error:   { icon: AlertCircle,  cls: 'border-red-200 dark:border-red-900 text-red-700 dark:text-red-300' },
  warning: { icon: AlertTriangle,cls: 'border-amber-200 dark:border-amber-900 text-amber-700 dark:text-amber-300' },
  info:    { icon: Info,         cls: 'border-sky-200 dark:border-sky-900 text-sky-700 dark:text-sky-300' }
}
</script>

<template>
  <Teleport to="body">
    <div class="fixed top-4 right-4 z-[200] flex flex-col gap-2 w-[22rem] max-w-[calc(100vw-2rem)]">
      <TransitionGroup
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0 translate-x-8"
        leave-active-class="transition duration-150 ease-in"
        leave-to-class="opacity-0 translate-x-8"
      >
        <div
          v-for="t in toast.items"
          :key="t.id"
          :class="['flex gap-3 items-start p-4 bg-white dark:bg-primary-800 border-l-4 rounded-lg shadow-soft', config[t.type].cls]"
          role="status"
        >
          <component :is="config[t.type].icon" class="w-5 h-5 flex-shrink-0 mt-0.5" />
          <div class="flex-1 text-sm">
            <p v-if="t.title" class="font-semibold text-neutral-900 dark:text-white mb-0.5">{{ t.title }}</p>
            <p class="text-neutral-700 dark:text-neutral-200">{{ t.message }}</p>
          </div>
          <button class="text-neutral-400 hover:text-neutral-700 dark:hover:text-white" @click="toast.dismiss(t.id)" aria-label="Close">
            <X class="w-4 h-4" />
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>
