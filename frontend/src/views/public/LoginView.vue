<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Eye, EyeOff, AlertCircle, Loader2 } from 'lucide-vue-next'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const form = reactive({ email: '', password: '' })
const loading = ref(false)
const error = ref('')
const showPwd = ref(false)

onMounted(() => {
  if (auth.isAuthenticated) router.replace(route.query.redirect || '/admin')
})

async function submit() {
  error.value = ''
  if (!form.email || !form.password) {
    error.value = 'Email va parolni kiriting'
    return
  }
  loading.value = true
  try {
    await auth.login(form.email, form.password)
    router.replace(route.query.redirect || '/admin')
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Email yoki parol noto\'g\'ri'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen relative bg-primary-900 dark:bg-[#080E22] flex items-center justify-center p-4 overflow-hidden">
    <!-- Decorative grid -->
    <div
      class="absolute inset-0 opacity-[0.06] pointer-events-none"
      style="background-image: linear-gradient(rgba(255,255,255,.4) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.4) 1px, transparent 1px); background-size: 60px 60px;"
    />
    <div class="absolute -top-32 -right-32 w-[28rem] h-[28rem] rounded-full bg-accent-500/10 blur-3xl pointer-events-none" />
    <div class="absolute -bottom-32 -left-32 w-96 h-96 rounded-full bg-primary-500/15 blur-3xl pointer-events-none" />

    <div class="relative w-full max-w-[400px]">
      <!-- Logo + title -->
      <div class="text-center mb-8">
        <RouterLink to="/" class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-accent-400 to-accent-600 text-white font-display font-bold text-2xl mb-4 shadow-button-accent">
          X
        </RouterLink>
        <h1 class="text-xl font-display font-bold text-white">Admin Panel</h1>
        <p class="text-sm text-slate-400 mt-1">Xalqaro Innovatsion Universiteti</p>
      </div>

      <!-- Card -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl shadow-modal p-8">
        <h2 class="text-base font-display font-semibold text-ink-dark dark:text-white mb-6">
          Tizimga kirish
        </h2>

        <form class="space-y-4" @submit.prevent="submit">
          <div>
            <label class="block text-[11px] font-semibold text-ink-medium dark:text-slate-300 mb-1.5 uppercase tracking-wider">
              Email
            </label>
            <input
              v-model="form.email"
              type="email"
              required
              autocomplete="email"
              class="input-field"
              placeholder="admin@xiuedu.uz"
            />
          </div>

          <div>
            <label class="block text-[11px] font-semibold text-ink-medium dark:text-slate-300 mb-1.5 uppercase tracking-wider">
              Parol
            </label>
            <div class="relative">
              <input
                v-model="form.password"
                :type="showPwd ? 'text' : 'password'"
                required
                autocomplete="current-password"
                class="input-field pr-10"
                placeholder="••••••••"
              />
              <button
                type="button"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-ink-faint hover:text-ink-medium"
                aria-label="Toggle password visibility"
                @click="showPwd = !showPwd"
              >
                <EyeOff v-if="showPwd" class="w-4 h-4" />
                <Eye v-else class="w-4 h-4" />
              </button>
            </div>
          </div>

          <Transition
            enter-active-class="transition duration-200"
            enter-from-class="opacity-0 -translate-y-1"
            leave-active-class="transition duration-150"
            leave-to-class="opacity-0"
          >
            <div v-if="error" class="flex items-center gap-2 p-3 rounded-lg bg-danger-light text-danger-dark text-sm">
              <AlertCircle class="w-4 h-4 flex-shrink-0" />
              <span>{{ error }}</span>
            </div>
          </Transition>

          <button
            type="submit"
            class="btn-primary btn-lg w-full justify-center"
            :disabled="loading"
          >
            <Loader2 v-if="loading" class="w-4 h-4 animate-spin" />
            {{ loading ? 'Yuklanmoqda...' : 'Kirish' }}
          </button>
        </form>
      </div>

      <p class="text-center text-xs text-slate-500 mt-6">
        © {{ new Date().getFullYear() }} Xalqaro Innovatsion Universiteti
      </p>
    </div>
  </div>
</template>
