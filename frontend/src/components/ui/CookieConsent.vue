<script setup>
import { ref, onMounted } from 'vue'
import { Cookie, X } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { getConsent, grantConsent, denyConsent } from '@/plugins/analytics'

const router = useRouter()
const visible = ref(false)

onMounted(() => {
  if (!getConsent()) setTimeout(() => { visible.value = true }, 1500)
})

function accept() {
  grantConsent(router)
  visible.value = false
}
function decline() {
  denyConsent()
  visible.value = false
}
</script>

<template>
  <Transition
    enter-active-class="transition duration-300"
    enter-from-class="opacity-0 translate-y-4"
    leave-active-class="transition duration-200"
    leave-to-class="opacity-0 translate-y-4"
  >
    <div
      v-if="visible"
      class="fixed bottom-4 left-4 right-4 sm:left-auto sm:max-w-md z-[90] rounded-2xl bg-white dark:bg-primary-800 border border-neutral-200 dark:border-primary-700 shadow-soft p-5"
      role="dialog"
      aria-live="polite"
    >
      <div class="flex items-start gap-3">
        <Cookie class="w-6 h-6 text-accent-500 flex-shrink-0 mt-0.5" />
        <div class="flex-1">
          <p class="font-semibold text-sm text-primary-700 dark:text-white mb-1">Cookie va analitika</p>
          <p class="text-xs text-neutral-500 dark:text-neutral-400 leading-relaxed">
            Saytdan foydalanish tajribasini yaxshilash uchun biz cookie va anonim statistikadan (Google Analytics, Yandex Metrica) foydalanamiz. Roziligingizni bering.
          </p>
          <div class="mt-3 flex items-center gap-2">
            <button class="px-3 py-1.5 rounded-lg bg-accent-500 text-primary-900 text-xs font-semibold hover:bg-accent-600" @click="accept">
              Roziman
            </button>
            <button class="px-3 py-1.5 rounded-lg border border-neutral-300 dark:border-primary-700 text-xs text-neutral-600 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-primary-700" @click="decline">
              Rad etish
            </button>
          </div>
        </div>
        <button class="text-neutral-400 hover:text-neutral-700 dark:hover:text-white -m-1 p-1" @click="decline" aria-label="Close">
          <X class="w-4 h-4" />
        </button>
      </div>
    </div>
  </Transition>
</template>
