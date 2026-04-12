<script setup>
import { ref, onMounted } from 'vue'
import { Megaphone, X } from 'lucide-vue-next'
import { NewsAPI } from '@/api/endpoints'

const visible = ref(true)
const items = ref([])

onMounted(async () => {
  if (sessionStorage.getItem('xiuedu_ann_dismissed')) { visible.value = false; return }
  try {
    const res = await NewsAPI.list({ limit: 3 })
    items.value = res.items || []
  } catch (_) { /* silent */ }
})

function dismiss() {
  visible.value = false
  sessionStorage.setItem('xiuedu_ann_dismissed', '1')
}
</script>

<template>
  <div v-if="visible && items.length" class="bg-accent-500 text-primary-900">
    <div class="container-wide flex items-center gap-3 py-2 text-sm">
      <Megaphone class="w-4 h-4 flex-shrink-0" />
      <div class="flex-1 overflow-hidden whitespace-nowrap">
        <div class="inline-block animate-[scroll_30s_linear_infinite]">
          <RouterLink
            v-for="(n, i) in items"
            :key="n.id"
            :to="`/news/${n.slug}`"
            class="mx-6 font-medium hover:underline"
          >
            <span class="opacity-60 mr-2">#{{ i + 1 }}</span>{{ n.title }}
          </RouterLink>
        </div>
      </div>
      <button class="opacity-70 hover:opacity-100" @click="dismiss" aria-label="Dismiss">
        <X class="w-4 h-4" />
      </button>
    </div>
  </div>
</template>

<style scoped>
@keyframes scroll {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
</style>
