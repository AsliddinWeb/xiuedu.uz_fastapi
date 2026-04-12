<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { ChevronLeft, ChevronRight, X, ImageIcon } from 'lucide-vue-next'

const tiles = Array.from({ length: 8 }, (_, i) => ({
  id: i + 1,
  hue: 215 + i * 18
}))

const open = ref(false)
const idx = ref(0)

function show(i) { idx.value = i; open.value = true }
function close() { open.value = false }
function prev() { idx.value = (idx.value - 1 + tiles.length) % tiles.length }
function next() { idx.value = (idx.value + 1) % tiles.length }

function onKey(e) {
  if (!open.value) return
  if (e.key === 'Escape') close()
  if (e.key === 'ArrowLeft') prev()
  if (e.key === 'ArrowRight') next()
}
onMounted(() => document.addEventListener('keydown', onKey))
onBeforeUnmount(() => document.removeEventListener('keydown', onKey))
</script>

<template>
  <section class="py-24 bg-neutral-50 dark:bg-primary-950">
    <div class="container-wide">
      <div class="text-center max-w-2xl mx-auto mb-12">
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-accent-500 mb-3">{{ $t('nav.gallery') }}</p>
        <h2 class="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-primary-700 dark:text-white">
          Talabalar hayoti
        </h2>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        <button
          v-for="(t, i) in tiles"
          :key="t.id"
          class="group relative aspect-square rounded-xl overflow-hidden focus:outline-none focus:ring-2 focus:ring-accent-500"
          :style="{ background: `linear-gradient(135deg, hsl(${t.hue},50%,30%), hsl(${t.hue + 20},60%,18%))` }"
          @click="show(i)"
          :aria-label="`Photo ${t.id}`"
        >
          <ImageIcon class="absolute inset-0 m-auto w-10 h-10 text-white/40 group-hover:text-white/70 transition" />
          <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition" />
        </button>
      </div>
    </div>

    <!-- Lightbox -->
    <Teleport to="body">
      <Transition enter-active-class="transition duration-200" enter-from-class="opacity-0" leave-active-class="transition duration-150" leave-to-class="opacity-0">
        <div v-if="open" class="fixed inset-0 z-[100] bg-black/90 backdrop-blur flex items-center justify-center p-4" @click.self="close">
          <button class="absolute top-5 right-5 p-2 rounded-full bg-white/10 text-white hover:bg-white/20" @click="close" aria-label="Close"><X class="w-5 h-5" /></button>
          <button class="absolute left-5 p-3 rounded-full bg-white/10 text-white hover:bg-white/20" @click="prev" aria-label="Previous"><ChevronLeft class="w-6 h-6" /></button>
          <button class="absolute right-5 p-3 rounded-full bg-white/10 text-white hover:bg-white/20" @click="next" aria-label="Next"><ChevronRight class="w-6 h-6" /></button>
          <div
            class="w-full max-w-4xl aspect-video rounded-2xl shadow-2xl flex items-center justify-center text-white/40"
            :style="{ background: `linear-gradient(135deg, hsl(${tiles[idx].hue},50%,30%), hsl(${tiles[idx].hue + 20},60%,18%))` }"
          >
            <ImageIcon class="w-24 h-24" stroke-width="1" />
          </div>
        </div>
      </Transition>
    </Teleport>
  </section>
</template>
