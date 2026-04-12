<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import DOMPurify from 'dompurify'
import PageHero from '@/components/sections/PageHero.vue'
import UILoader from '@/components/ui/UILoader.vue'
import { PagesAPI } from '@/api/endpoints'
import { useSeo } from '@/composables/useSeo'
import { useLanguageStore } from '@/stores/language'

const props = defineProps({
  slug: { type: String, default: null }
})

const route = useRoute()
const lang = useLanguageStore()

const page = ref(null)
const loading = ref(true)
const errorMsg = ref('')

const targetSlug = computed(() => props.slug || route.params.slug || route.meta?.slug)

async function load() {
  loading.value = true
  errorMsg.value = ''
  try {
    page.value = await PagesAPI.bySlug(targetSlug.value)
  } catch (e) {
    page.value = null
    errorMsg.value = e?.response?.status === 404 ? 'not_found' : 'error'
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch([targetSlug, () => lang.current], load)

useSeo(() => ({
  title: page.value?.title,
  description: page.value?.meta_description
}))

const safeContent = computed(() => DOMPurify.sanitize(page.value?.content || ''))
</script>

<template>
  <div>
    <PageHero v-if="page" :title="page.title" />
    <PageHero v-else-if="loading" title="..." />
    <PageHero v-else title="Sahifa topilmadi" />

    <section class="py-16">
      <div class="container-wide max-w-4xl">
        <div v-if="loading"><UILoader variant="skeleton-text" :lines="8" /></div>
        <div v-else-if="page" class="prose prose-neutral dark:prose-invert max-w-none prose-headings:font-display prose-headings:text-primary-700 dark:prose-headings:text-white prose-a:text-accent-500" v-html="safeContent" />
        <div v-else class="text-center py-12 text-neutral-500">
          <p>{{ errorMsg === 'not_found' ? 'Bu sahifa hali tayyorlanmagan' : 'Sahifani yuklashda xatolik' }}</p>
        </div>
      </div>
    </section>
  </div>
</template>
