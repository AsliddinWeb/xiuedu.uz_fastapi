<script setup>
import { RouterView } from 'vue-router'
import SiteHeader from './SiteHeader.vue'
import SiteFooter from './SiteFooter.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <SiteHeader />
    <main class="flex-1">
      <RouterView />
    </main>
    <SiteFooter />
  </div>
</template>
