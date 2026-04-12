<script setup>
/**
 * Language dropdown — Teleported to body to escape any stacking context.
 * Position is computed from the trigger button's bounding rect.
 */
import { ref, reactive, nextTick, onMounted, onBeforeUnmount } from 'vue'
import { Globe, ChevronDown, Check } from 'lucide-vue-next'
import { useLanguageStore } from '@/stores/language'

defineProps({
  compact: { type: Boolean, default: false }
})

const lang = useLanguageStore()
const open = ref(false)
const trigger = ref(null)
const position = reactive({ top: 0, right: 0, width: 176 })

function updatePosition() {
  if (!trigger.value) return
  const rect = trigger.value.getBoundingClientRect()
  position.top = rect.bottom + 8
  position.right = window.innerWidth - rect.right
}

function toggle() {
  open.value = !open.value
  if (open.value) nextTick(updatePosition)
}
function close() { open.value = false }
function pick(code) {
  lang.setLanguage(code)
  close()
}

function onKey(e) { if (e.key === 'Escape') close() }
function onScroll() { if (open.value) updatePosition() }
function onClickOutside(e) {
  if (!open.value) return
  if (trigger.value && trigger.value.contains(e.target)) return
  if (e.target.closest('[data-lang-menu]')) return
  close()
}

onMounted(() => {
  document.addEventListener('keydown', onKey)
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', onScroll, { passive: true })
  document.addEventListener('mousedown', onClickOutside)
})
onBeforeUnmount(() => {
  document.removeEventListener('keydown', onKey)
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', onScroll)
  document.removeEventListener('mousedown', onClickOutside)
})
</script>

<template>
  <button
    ref="trigger"
    type="button"
    :aria-label="$t('ui.select_language')"
    :aria-expanded="open"
    :class="[
      'inline-flex items-center gap-1.5 rounded-md font-medium transition uppercase',
      compact
        ? 'px-1.5 py-1 text-[11px] text-white/80 hover:text-white hover:bg-white/10'
        : 'px-2.5 py-1.5 text-xs text-white/80 hover:text-white hover:bg-white/10'
    ]"
    @click="toggle"
  >
    <Globe :class="compact ? 'w-3 h-3' : 'w-3.5 h-3.5'" />
    <span>{{ lang.currentLang.short }}</span>
    <ChevronDown :class="['w-3 h-3 transition-transform', open && 'rotate-180']" />
  </button>

  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-150"
      enter-from-class="opacity-0 -translate-y-1"
      leave-active-class="transition duration-100"
      leave-to-class="opacity-0"
    >
      <ul
        v-if="open"
        data-lang-menu
        role="listbox"
        class="fixed py-1 rounded-xl border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-800 shadow-dropdown z-[200]"
        :style="{ top: position.top + 'px', right: position.right + 'px', width: position.width + 'px' }"
      >
        <li v-for="l in lang.languages" :key="l.code">
          <button
            type="button"
            role="option"
            :aria-selected="lang.current === l.code"
            class="w-full flex items-center gap-2.5 px-3 py-2 text-sm text-ink-medium dark:text-slate-200 hover:bg-primary-50 hover:text-primary-700 dark:hover:bg-slate-700 transition"
            @click="pick(l.code)"
          >
            <span class="text-base leading-none">{{ l.flag }}</span>
            <span class="flex-1 text-left">{{ l.label }}</span>
            <Check v-if="lang.current === l.code" class="w-4 h-4 text-accent-500" />
          </button>
        </li>
      </ul>
    </Transition>
  </Teleport>
</template>
