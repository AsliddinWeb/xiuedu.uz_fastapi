<script setup>
import { Calendar, MapPin, Clock } from 'lucide-vue-next'

const events = [
  { date: '15 Apr', time: '10:00', title: "Ochiq eshiklar kuni",       location: "Bosh bino, Toshkent" },
  { date: '22 Apr', time: '14:00', title: "Xalqaro hamkorlik forumi",  location: "Konferensiya zali" },
  { date: '02 May', time: '09:00', title: "Talabalar ilmiy konferensiyasi", location: "B-202 auditoriya" }
]
</script>

<template>
  <section class="py-24 bg-white dark:bg-primary-900">
    <div class="container-wide">
      <div class="text-center max-w-2xl mx-auto mb-12">
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-accent-500 mb-3">{{ $t('nav.events') }}</p>
        <h2 class="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-primary-700 dark:text-white">
          Yaqinlashayotgan tadbirlar
        </h2>
      </div>

      <div class="relative max-w-3xl mx-auto pl-8 md:pl-0">
        <!-- Timeline line -->
        <div class="absolute md:left-1/2 top-0 bottom-0 w-px bg-gradient-to-b from-accent-500 via-accent-500/30 to-transparent" />

        <div
          v-for="(e, i) in events"
          :key="i"
          :class="['relative mb-10 md:flex md:items-center', i % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse']"
        >
          <div class="md:w-1/2 md:pr-8" :class="i % 2 !== 0 && 'md:pl-8 md:pr-0 md:text-right'">
            <div class="rounded-2xl p-6 bg-neutral-50 dark:bg-primary-800 border border-neutral-200 dark:border-primary-700 shadow-card hover:shadow-soft hover:-translate-y-0.5 transition">
              <span class="inline-block px-3 py-1 mb-3 text-xs font-bold uppercase tracking-wider rounded-full bg-accent-500/10 text-accent-500">{{ e.date }}</span>
              <h3 class="font-display text-lg font-semibold text-primary-700 dark:text-white mb-2">{{ e.title }}</h3>
              <div class="flex flex-wrap gap-3 text-xs text-neutral-500 dark:text-neutral-400" :class="i % 2 !== 0 && 'md:justify-end'">
                <span class="inline-flex items-center gap-1"><Clock class="w-3 h-3" /> {{ e.time }}</span>
                <span class="inline-flex items-center gap-1"><MapPin class="w-3 h-3" /> {{ e.location }}</span>
              </div>
            </div>
          </div>
          <!-- Timeline dot -->
          <div class="absolute -left-2 md:left-1/2 md:-translate-x-1/2 w-4 h-4 rounded-full bg-accent-500 ring-4 ring-white dark:ring-primary-900">
            <Calendar class="w-3 h-3 text-primary-900 m-auto mt-0.5" />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
