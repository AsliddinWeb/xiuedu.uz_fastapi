<script setup>
/**
 * Public layout: navbar + animated router-view + footer + global toast.
 * Auto scroll-to-top on route change.
 */
import { watch, nextTick, onMounted } from 'vue'
import { useRoute, RouterView } from 'vue-router'
import TheNavbar from './TheNavbar.vue'
import TheFooter from './TheFooter.vue'
import UIToast from '@/components/ui/UIToast.vue'
import CookieConsent from '@/components/ui/CookieConsent.vue'
import UIErrorBoundary from '@/components/ui/UIErrorBoundary.vue'
import ChatWidget from '@/components/chat/ChatWidget.vue'
import { useSiteSettingsStore } from '@/stores/siteSettings'

const route = useRoute()
const siteSettings = useSiteSettingsStore()

onMounted(async () => {
  await siteSettings.ensureLoaded()
  const fav = siteSettings.faviconUrl
  if (fav) {
    let link = document.querySelector("link[rel~='icon']")
    if (!link) {
      link = document.createElement('link')
      link.rel = 'icon'
      document.head.appendChild(link)
    }
    link.href = fav
  }
})

watch(
  () => route.fullPath,
  () => {
    nextTick(() => window.scrollTo({ top: 0, behavior: 'instant' in window ? 'instant' : 'auto' }))
  }
)
</script>

<template>
  <div class="min-h-screen flex flex-col bg-white dark:bg-primary-900">
    <TheNavbar />
    <main class="flex-1">
      <UIErrorBoundary>
        <RouterView v-slot="{ Component, route: r }">
          <Transition
            enter-active-class="transition duration-300 ease-smooth"
            enter-from-class="opacity-0 translate-y-2"
            leave-active-class="transition duration-150 ease-smooth"
            leave-to-class="opacity-0 -translate-y-1"
            mode="out-in"
          >
            <component :is="Component" :key="r.fullPath" />
          </Transition>
        </RouterView>
      </UIErrorBoundary>
    </main>
    <TheFooter />
    <UIToast />
    <CookieConsent />
    <ChatWidget />
  </div>
</template>
