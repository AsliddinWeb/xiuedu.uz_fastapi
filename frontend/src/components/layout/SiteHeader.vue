<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { Menu, X, Sun, Moon, Globe } from 'lucide-vue-next'
import { useThemeStore } from '@/stores/theme'
import { useLanguageStore } from '@/stores/language'

const theme = useThemeStore()
const lang = useLanguageStore()
const open = ref(false)
const langOpen = ref(false)
</script>

<template>
  <header class="sticky top-0 z-40 bg-white/90 dark:bg-primary-900/90 backdrop-blur border-b border-neutral-200 dark:border-primary-700">
    <div class="container-wide flex items-center justify-between h-16">
      <RouterLink to="/" class="flex items-center gap-2">
        <span class="w-9 h-9 rounded-lg bg-primary-700 dark:bg-accent-500 grid place-items-center text-white dark:text-primary-900 font-display font-bold">X</span>
        <span class="font-display text-lg font-semibold text-primary-700 dark:text-white">XIU Edu</span>
      </RouterLink>

      <nav class="hidden lg:flex items-center gap-6 text-sm font-medium">
        <RouterLink to="/" class="hover:text-accent-500">{{ $t('nav.home') }}</RouterLink>
        <RouterLink to="/about" class="hover:text-accent-500">{{ $t('nav.about') }}</RouterLink>
        <RouterLink to="/faculties" class="hover:text-accent-500">{{ $t('nav.faculties') }}</RouterLink>
        <RouterLink to="/education/bachelor" class="hover:text-accent-500">{{ $t('nav.education') }}</RouterLink>
        <RouterLink to="/applicants" class="hover:text-accent-500">{{ $t('nav.applicants') }}</RouterLink>
        <RouterLink to="/news" class="hover:text-accent-500">{{ $t('nav.news') }}</RouterLink>
        <RouterLink to="/contact" class="hover:text-accent-500">{{ $t('nav.contact') }}</RouterLink>
      </nav>

      <div class="flex items-center gap-2">
        <div class="relative">
          <button @click="langOpen = !langOpen" class="btn-outline !px-3 !py-2 text-xs uppercase">
            <Globe class="w-4 h-4" /> {{ lang.locale }}
          </button>
          <div v-if="langOpen" class="absolute right-0 mt-2 w-28 card p-1 z-50">
            <button v-for="l in lang.supported" :key="l"
                    @click="lang.set(l); langOpen = false"
                    class="w-full text-left px-3 py-1.5 rounded hover:bg-neutral-100 dark:hover:bg-primary-700 uppercase text-xs">
              {{ l }}
            </button>
          </div>
        </div>

        <button @click="theme.toggle" class="btn-outline !px-3 !py-2" :aria-label="'Toggle theme'">
          <Sun v-if="theme.mode === 'dark'" class="w-4 h-4" />
          <Moon v-else class="w-4 h-4" />
        </button>

        <button class="lg:hidden btn-outline !px-3 !py-2" @click="open = !open">
          <X v-if="open" class="w-5 h-5" />
          <Menu v-else class="w-5 h-5" />
        </button>
      </div>
    </div>

    <div v-if="open" class="lg:hidden border-t border-neutral-200 dark:border-primary-700">
      <nav class="container-wide flex flex-col py-4 gap-3 text-sm">
        <RouterLink @click="open = false" to="/">{{ $t('nav.home') }}</RouterLink>
        <RouterLink @click="open = false" to="/about">{{ $t('nav.about') }}</RouterLink>
        <RouterLink @click="open = false" to="/faculties">{{ $t('nav.faculties') }}</RouterLink>
        <RouterLink @click="open = false" to="/education/bachelor">{{ $t('nav.bachelor') }}</RouterLink>
        <RouterLink @click="open = false" to="/education/master">{{ $t('nav.master') }}</RouterLink>
        <RouterLink @click="open = false" to="/applicants">{{ $t('nav.applicants') }}</RouterLink>
        <RouterLink @click="open = false" to="/news">{{ $t('nav.news') }}</RouterLink>
        <RouterLink @click="open = false" to="/contact">{{ $t('nav.contact') }}</RouterLink>
      </nav>
    </div>
  </header>
</template>
