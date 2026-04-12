<script setup>
/**
 * Floating AI chat widget — bottom-right bubble.
 * Opens a chat panel with message history.
 * Calls POST /api/chat/ with session persistence.
 */
import { ref, nextTick, onMounted } from 'vue'
import { MessageCircle, X, Send, Bot, User, Loader2 } from 'lucide-vue-next'
import api from '@/api/client'
import { useLanguageStore } from '@/stores/language'

const lang = useLanguageStore()
const isOpen = ref(false)
const message = ref('')
const sending = ref(false)
const messages = ref([])
const chatBody = ref(null)
const inputRef = ref(null)

// Persistent session ID
const SESSION_KEY = 'xiuedu_chat_session'
const sessionId = ref(localStorage.getItem(SESSION_KEY) || '')

function getOrCreateSession() {
  if (!sessionId.value) {
    sessionId.value = Math.random().toString(36).slice(2) + Date.now().toString(36)
    localStorage.setItem(SESSION_KEY, sessionId.value)
  }
  return sessionId.value
}

function toggle() {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    nextTick(() => inputRef.value?.focus())
    // Welcome message on first open
    if (!messages.value.length) {
      messages.value.push({
        role: 'assistant',
        content: lang.currentLang === 'ru'
          ? 'Здравствуйте! Я AI-ассистент XIU Edu. Задайте мне вопрос об университете.'
          : lang.currentLang === 'en'
            ? "Hello! I'm XIU Edu's AI assistant. Ask me anything about the university."
            : "Assalomu alaykum! Men XIU Edu AI yordamchisiman. Universitet haqida savolingiz bo'lsa, yozing."
      })
    }
  }
}

async function send() {
  const text = message.value.trim()
  if (!text || sending.value) return

  messages.value.push({ role: 'user', content: text })
  message.value = ''
  sending.value = true
  scrollBottom()

  try {
    const res = await api.post('/chat/', {
      message: text,
      session_id: getOrCreateSession()
    }, { params: { lang: lang.currentLang } })

    messages.value.push({
      role: 'assistant',
      content: res.data.reply,
      sources: res.data.sources
    })
    sessionId.value = res.data.session_id
    localStorage.setItem(SESSION_KEY, sessionId.value)
  } catch (_) {
    messages.value.push({
      role: 'assistant',
      content: 'Kechirasiz, hozir javob berishda muammo bor. Iltimos, keyinroq urinib ko\'ring.'
    })
  } finally {
    sending.value = false
    scrollBottom()
    nextTick(() => inputRef.value?.focus())
  }
}

function scrollBottom() {
  nextTick(() => {
    if (chatBody.value) {
      chatBody.value.scrollTop = chatBody.value.scrollHeight
    }
  })
}

function onKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    send()
  }
}
</script>

<template>
  <!-- Floating bubble -->
  <Teleport to="body">
    <div class="fixed bottom-6 right-6 z-[100]">
      <!-- Chat panel -->
      <Transition
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="opacity-0 translate-y-4 scale-95"
        leave-active-class="transition duration-200 ease-in"
        leave-to-class="opacity-0 translate-y-4 scale-95"
      >
        <div
          v-if="isOpen"
          class="absolute bottom-16 right-0 w-[380px] max-w-[calc(100vw-2rem)] rounded-2xl bg-white dark:bg-slate-900 shadow-[0_30px_80px_rgba(10,13,61,0.30)] border border-surface-muted dark:border-slate-700 overflow-hidden flex flex-col"
          style="height: 520px; max-height: calc(100vh - 8rem);"
        >
          <!-- Header -->
          <div
            class="flex items-center gap-3 px-5 py-4 text-white flex-shrink-0"
            style="background: linear-gradient(135deg, #0A0D3D 0%, #1A1F6E 100%);"
          >
            <div class="w-10 h-10 rounded-full bg-white/15 grid place-items-center flex-shrink-0">
              <Bot class="w-5 h-5 text-accent-400" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-bold">XIU Yordamchi</p>
              <p class="text-[11px] text-white/60">
                <span class="inline-flex items-center gap-1">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  Onlayn
                </span>
              </p>
            </div>
            <button
              type="button"
              class="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 grid place-items-center"
              @click="toggle"
            >
              <X class="w-4 h-4" />
            </button>
          </div>

          <!-- Messages -->
          <div
            ref="chatBody"
            class="flex-1 overflow-y-auto px-4 py-4 space-y-3 bg-surface-light dark:bg-slate-900/50"
          >
            <div
              v-for="(msg, i) in messages"
              :key="i"
              :class="['flex gap-2.5', msg.role === 'user' ? 'flex-row-reverse' : '']"
            >
              <!-- Avatar -->
              <div
                :class="[
                  'w-7 h-7 rounded-full grid place-items-center flex-shrink-0 text-white',
                  msg.role === 'user'
                    ? 'bg-accent-500'
                    : 'bg-gradient-to-br from-primary-700 to-primary-900'
                ]"
              >
                <User v-if="msg.role === 'user'" class="w-3.5 h-3.5" />
                <Bot v-else class="w-3.5 h-3.5" />
              </div>

              <!-- Bubble -->
              <div
                :class="[
                  'max-w-[80%] px-4 py-2.5 rounded-2xl text-[13px] leading-relaxed',
                  msg.role === 'user'
                    ? 'bg-primary-700 text-white rounded-br-md'
                    : 'bg-white dark:bg-slate-800 text-ink-medium dark:text-slate-300 border border-surface-muted dark:border-slate-700 rounded-bl-md shadow-sm'
                ]"
              >
                <p class="whitespace-pre-wrap">{{ msg.content }}</p>
                <div v-if="msg.sources?.length" class="mt-2 pt-2 border-t border-black/10 dark:border-white/10">
                  <p class="text-[10px] text-ink-faint dark:text-slate-500 mb-1">Manbalar:</p>
                  <div class="flex flex-wrap gap-1">
                    <span
                      v-for="s in msg.sources"
                      :key="s"
                      class="inline-block px-1.5 py-0.5 rounded bg-surface-soft dark:bg-slate-700 text-[9px] text-ink-faint"
                    >{{ s }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Typing indicator -->
            <div v-if="sending" class="flex gap-2.5">
              <div class="w-7 h-7 rounded-full bg-gradient-to-br from-primary-700 to-primary-900 grid place-items-center text-white flex-shrink-0">
                <Bot class="w-3.5 h-3.5" />
              </div>
              <div class="px-4 py-3 rounded-2xl rounded-bl-md bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 shadow-sm">
                <div class="flex items-center gap-1">
                  <span class="w-2 h-2 rounded-full bg-ink-faint animate-bounce" style="animation-delay: 0ms" />
                  <span class="w-2 h-2 rounded-full bg-ink-faint animate-bounce" style="animation-delay: 150ms" />
                  <span class="w-2 h-2 rounded-full bg-ink-faint animate-bounce" style="animation-delay: 300ms" />
                </div>
              </div>
            </div>
          </div>

          <!-- Input -->
          <div class="flex items-end gap-2 p-3 border-t border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 flex-shrink-0">
            <textarea
              ref="inputRef"
              v-model="message"
              @keydown="onKeydown"
              :placeholder="lang.currentLang === 'ru' ? 'Задайте вопрос...' : lang.currentLang === 'en' ? 'Ask a question...' : 'Savol yozing...'"
              rows="1"
              class="flex-1 resize-none px-4 py-2.5 rounded-xl bg-surface-soft dark:bg-slate-800 border-0 text-sm text-ink-dark dark:text-white placeholder:text-ink-faint focus:outline-none focus:ring-2 focus:ring-primary-400 max-h-24"
            />
            <button
              type="button"
              :disabled="!message.trim() || sending"
              class="w-10 h-10 rounded-xl grid place-items-center text-white transition-all disabled:opacity-40"
              :class="message.trim() && !sending ? 'bg-accent-500 hover:bg-accent-600 shadow-md' : 'bg-surface-muted text-ink-faint'"
              @click="send"
            >
              <Loader2 v-if="sending" class="w-4 h-4 animate-spin" />
              <Send v-else class="w-4 h-4" />
            </button>
          </div>
        </div>
      </Transition>

      <!-- Trigger button -->
      <button
        type="button"
        class="group w-14 h-14 rounded-full shadow-[0_8px_32px_rgba(10,13,61,0.30)] grid place-items-center transition-all hover:scale-110 active:scale-95"
        :class="isOpen
          ? 'bg-ink-dark text-white'
          : 'bg-gradient-to-br from-primary-700 to-primary-900 text-white'"
        @click="toggle"
      >
        <X v-if="isOpen" class="w-5 h-5" />
        <MessageCircle v-else class="w-6 h-6" />

        <!-- Notification dot -->
        <span
          v-if="!isOpen"
          class="absolute -top-0.5 -right-0.5 w-4 h-4 rounded-full bg-accent-500 border-2 border-white grid place-items-center"
        >
          <span class="w-1.5 h-1.5 rounded-full bg-white" />
        </span>
      </button>
    </div>
  </Teleport>
</template>
