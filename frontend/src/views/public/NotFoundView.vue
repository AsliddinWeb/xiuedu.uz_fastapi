<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Home, Search, ArrowRight, Compass } from 'lucide-vue-next'
import UIButton from '@/components/ui/UIButton.vue'
import UIInput from '@/components/ui/UIInput.vue'
import { useSeo } from '@/composables/useSeo'

const router = useRouter()
const query = ref('')

useSeo(() => ({
  title: '404 — Sahifa topilmadi',
  description: "So'ralgan sahifa mavjud emas yoki o'chirilgan.",
  noIndex: true
}))

function search() {
  if (!query.value.trim()) return
  router.push({ path: '/news', query: { q: query.value.trim() } })
}

const suggestions = [
  { to: '/about',          label: 'Biz haqimizda' },
  { to: '/faculties',      label: 'Fakultetlar' },
  { to: '/applicants',     label: 'Abituriyentlarga' },
  { to: '/news',           label: 'Yangiliklar' },
  { to: '/contact',        label: 'Aloqa' }
]
</script>

<template>
  <section class="relative min-h-[80vh] flex items-center bg-navy-gradient text-white overflow-hidden">
    <div class="absolute inset-0 opacity-[0.05]" style="background-image: linear-gradient(rgba(255,255,255,.4) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.4) 1px, transparent 1px); background-size: 60px 60px;" />
    <div class="absolute -top-32 -right-32 w-[28rem] h-[28rem] rounded-full bg-accent-500/15 blur-3xl pointer-events-none" />

    <div class="container-wide relative grid lg:grid-cols-2 gap-10 items-center py-20">
      <div>
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-accent-500 mb-3">404 · Page not found</p>
        <h1 class="font-display text-7xl md:text-8xl font-bold leading-none mb-6">
          Bu sahifa<br/><span class="text-accent-500">topilmadi</span>
        </h1>
        <p class="text-lg text-neutral-300 max-w-xl mb-8">
          So'ralgan sahifa mavjud emas, ko'chirilgan yoki manzil noto'g'ri kiritilgan bo'lishi mumkin.
        </p>

        <form class="max-w-md mb-8" @submit.prevent="search">
          <UIInput v-model="query" placeholder="Saytdan qidirish...">
            <template #prefix><Search class="w-4 h-4 text-neutral-400" /></template>
          </UIInput>
        </form>

        <div class="flex flex-wrap gap-3">
          <UIButton variant="accent" to="/">
            <template #icon-left><Home class="w-4 h-4" /></template>
            Bosh sahifa
          </UIButton>
          <UIButton size="md" to="/contact" class="!bg-white/10 !text-white !border !border-white/30 hover:!bg-white hover:!text-primary-900">
            Aloqa
          </UIButton>
        </div>
      </div>

      <div class="hidden lg:block">
        <div class="rounded-3xl p-10 bg-white/5 backdrop-blur border border-white/10">
          <Compass class="w-12 h-12 text-accent-500 mb-5" stroke-width="1.4" />
          <h3 class="font-display text-xl font-semibold mb-4">Mashhur sahifalar</h3>
          <ul class="space-y-2">
            <li v-for="s in suggestions" :key="s.to">
              <RouterLink :to="s.to" class="group flex items-center justify-between px-3 py-2 rounded-lg text-sm text-neutral-200 hover:bg-white/10 transition">
                {{ s.label }}
                <ArrowRight class="w-4 h-4 opacity-50 group-hover:opacity-100 group-hover:text-accent-500 transition" />
              </RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>
