<script setup>
import { Mail, Phone, MapPin } from 'lucide-vue-next'
</script>

<template>
  <footer class="bg-primary-900 text-neutral-200 mt-20">
    <div class="container-wide py-14 grid gap-10 md:grid-cols-4">
      <div>
        <div class="flex items-center gap-2 mb-4">
          <span class="w-9 h-9 rounded-lg bg-accent-500 grid place-items-center text-primary-900 font-display font-bold">X</span>
          <span class="font-display text-lg font-semibold text-white">XIU Edu</span>
        </div>
        <p class="text-sm text-neutral-400">{{ $t('site.tagline') }}</p>
      </div>

      <div>
        <h4 class="text-white text-sm font-semibold mb-3">{{ $t('nav.education') }}</h4>
        <ul class="space-y-2 text-sm text-neutral-400">
          <li><RouterLink to="/education/bachelor" class="hover:text-accent-500">{{ $t('nav.bachelor') }}</RouterLink></li>
          <li><RouterLink to="/education/master" class="hover:text-accent-500">{{ $t('nav.master') }}</RouterLink></li>
          <li><RouterLink to="/faculties" class="hover:text-accent-500">{{ $t('nav.faculties') }}</RouterLink></li>
          <li><RouterLink to="/applicants" class="hover:text-accent-500">{{ $t('nav.applicants') }}</RouterLink></li>
        </ul>
      </div>

      <div>
        <h4 class="text-white text-sm font-semibold mb-3">{{ $t('nav.about') }}</h4>
        <ul class="space-y-2 text-sm text-neutral-400">
          <li><RouterLink to="/leadership" class="hover:text-accent-500">{{ $t('nav.leadership') }}</RouterLink></li>
          <li><RouterLink to="/structure" class="hover:text-accent-500">{{ $t('nav.structure') }}</RouterLink></li>
          <li><RouterLink to="/international" class="hover:text-accent-500">{{ $t('nav.international') }}</RouterLink></li>
          <li><RouterLink to="/careers" class="hover:text-accent-500">{{ $t('nav.careers') }}</RouterLink></li>
        </ul>
      </div>

      <div>
        <h4 class="text-white text-sm font-semibold mb-3">{{ $t('nav.contact') }}</h4>
        <ul class="space-y-2 text-sm text-neutral-400">
          <li class="flex items-start gap-2"><MapPin class="w-4 h-4 mt-0.5 text-accent-500" /> Toshkent, O'zbekiston</li>
          <li class="flex items-start gap-2"><Phone class="w-4 h-4 mt-0.5 text-accent-500" /> +998 71 000 00 00</li>
          <li class="flex items-start gap-2"><Mail class="w-4 h-4 mt-0.5 text-accent-500" /> info@xiuedu.uz</li>
        </ul>
      </div>
    </div>
    <div class="border-t border-primary-800">
      <div class="container-wide py-5 text-center text-xs text-neutral-500">
        © {{ new Date().getFullYear() }} XIU Edu. {{ $t('footer.rights') }}.
      </div>
    </div>
  </footer>
</template>
