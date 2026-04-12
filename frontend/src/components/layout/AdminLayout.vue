<script setup>
import { RouterView, RouterLink } from 'vue-router'
import { LayoutDashboard, Users, Newspaper, FileText, Image } from 'lucide-vue-next'
</script>

<template>
  <div class="min-h-screen flex bg-neutral-100 dark:bg-primary-900">
    <aside class="w-64 bg-primary-900 text-white p-5 hidden md:block">
      <div class="flex items-center gap-2 mb-8">
        <span class="w-9 h-9 rounded-lg bg-accent-500 grid place-items-center text-primary-900 font-bold">X</span>
        <span class="font-display font-semibold">Admin</span>
      </div>
      <nav class="space-y-1 text-sm">
        <RouterLink to="/admin" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-primary-800"><LayoutDashboard class="w-4 h-4" /> Dashboard</RouterLink>
        <RouterLink to="/admin/users" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-primary-800"><Users class="w-4 h-4" /> Users</RouterLink>
        <RouterLink to="/admin/news" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-primary-800"><Newspaper class="w-4 h-4" /> News</RouterLink>
        <RouterLink to="/admin/pages" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-primary-800"><FileText class="w-4 h-4" /> Pages</RouterLink>
        <RouterLink to="/admin/media" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-primary-800"><Image class="w-4 h-4" /> Media</RouterLink>
      </nav>
    </aside>
    <main class="flex-1 p-6 overflow-auto">
      <RouterView />
    </main>
  </div>
</template>
