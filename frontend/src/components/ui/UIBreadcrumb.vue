<script setup>
/**
 * Auto-generates from current route or accepts items prop.
 * @prop {Array<{label:string, to?:string}>} items
 */
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ChevronRight, Home } from 'lucide-vue-next'

const props = defineProps({
  items: { type: Array, default: null }
})

const route = useRoute()
const { t } = useI18n()

const computedItems = computed(() => {
  if (props.items) return props.items
  // auto from route
  const segs = route.path.split('/').filter(Boolean)
  let path = ''
  return segs.map((s) => {
    path += '/' + s
    return { label: s.replace(/-/g, ' '), to: path }
  })
})
</script>

<template>
  <nav aria-label="Breadcrumb" class="text-sm">
    <ol class="flex items-center flex-wrap gap-1.5 text-neutral-500 dark:text-neutral-400">
      <li>
        <router-link to="/" class="flex items-center gap-1 hover:text-primary-700 dark:hover:text-accent-500">
          <Home class="w-3.5 h-3.5" />
          <span>{{ t('nav.home') }}</span>
        </router-link>
      </li>
      <li v-for="(item, i) in computedItems" :key="i" class="flex items-center gap-1.5">
        <ChevronRight class="w-3.5 h-3.5" />
        <router-link
          v-if="item.to && i < computedItems.length - 1"
          :to="item.to"
          class="capitalize hover:text-primary-700 dark:hover:text-accent-500"
        >
          {{ item.label }}
        </router-link>
        <span v-else class="capitalize text-primary-700 dark:text-white font-medium">{{ item.label }}</span>
      </li>
    </ol>
  </nav>
</template>
