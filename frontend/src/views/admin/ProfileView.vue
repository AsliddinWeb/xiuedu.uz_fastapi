<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { Save, KeyRound, User as UserIcon, Mail, Shield, Camera, Trash2 } from 'lucide-vue-next'
import { ProfileAPI, AdminMediaAPI } from '@/api/admin'
import { useAuthStore } from '@/stores/auth'
import UIInput from '@/components/ui/UIInput.vue'
import UIButton from '@/components/ui/UIButton.vue'
import { useToast } from '@/composables/useToast'

const auth = useAuthStore()
const toast = useToast()

const loading = ref(true)
const savingProfile = ref(false)
const savingPassword = ref(false)
const uploadingAvatar = ref(false)

const profile = reactive({
  email: '',
  full_name: '',
  avatar_url: null,
  role: '',
  is_active: true,
  last_login: null,
  created_at: null
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const initials = computed(() => {
  const name = profile.full_name || profile.email || 'U'
  return name.split(/\s+/).map(s => s[0]).slice(0, 2).join('').toUpperCase()
})

const roleLabels = {
  superadmin: 'Super admin',
  admin: 'Administrator',
  content_manager: 'Kontent menejeri',
  page_editor: 'Sahifa muharriri'
}

async function loadProfile() {
  loading.value = true
  try {
    const me = await ProfileAPI.me()
    Object.assign(profile, me)
  } catch (_) {
    toast.error('Profilni yuklab bo\'lmadi')
  } finally {
    loading.value = false
  }
}
onMounted(loadProfile)

async function onUploadAvatar(e) {
  const file = e.target.files[0]
  if (!file) return
  uploadingAvatar.value = true
  try {
    const res = await AdminMediaAPI.upload(file)
    profile.avatar_url = res.url
    await ProfileAPI.update({ avatar_url: res.url })
    auth.setUser({ ...auth.user, avatar_url: res.url })
    toast.success('Avatar yangilandi')
  } catch (_) {
    toast.error('Yuklashda xatolik')
  } finally {
    uploadingAvatar.value = false
    e.target.value = ''
  }
}

async function removeAvatar() {
  try {
    profile.avatar_url = null
    await ProfileAPI.update({ avatar_url: null })
    auth.setUser({ ...auth.user, avatar_url: null })
    toast.success('Avatar olib tashlandi')
  } catch (_) {}
}

async function saveProfile() {
  if (!profile.full_name) {
    toast.error("Ism-familiya bo'sh bo'lmasligi kerak")
    return
  }
  savingProfile.value = true
  try {
    const updated = await ProfileAPI.update({ full_name: profile.full_name })
    auth.setUser({ ...auth.user, full_name: updated.full_name })
    toast.success('Profil yangilandi')
  } catch (e) {
    toast.error(e?.response?.data?.detail || 'Xatolik')
  } finally {
    savingProfile.value = false
  }
}

async function changePassword() {
  if (!passwordForm.current_password || !passwordForm.new_password) {
    toast.error("Maydonlarni to'ldiring")
    return
  }
  if (passwordForm.new_password.length < 8) {
    toast.error("Yangi parol kamida 8 ta belgi bo'lishi kerak")
    return
  }
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    toast.error("Parol tasdiqlanmadi")
    return
  }
  savingPassword.value = true
  try {
    await ProfileAPI.changePassword({
      current_password: passwordForm.current_password,
      new_password: passwordForm.new_password
    })
    toast.success("Parol o'zgartirildi")
    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
  } catch (e) {
    toast.error(e?.response?.data?.detail || 'Xatolik')
  } finally {
    savingPassword.value = false
  }
}

function fmtDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleString('uz-UZ', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>

<template>
  <div class="max-w-4xl">
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-xl font-display font-bold text-ink-dark dark:text-white">Mening kabinetim</h1>
      <p class="text-sm text-ink-faint mt-0.5">Profil va xavfsizlik sozlamalari</p>
    </div>

    <div v-if="loading" class="text-center py-12 text-ink-faint">Yuklanmoqda...</div>

    <div v-else class="space-y-5">
      <!-- Profile card -->
      <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 overflow-hidden">
        <!-- Banner -->
        <div class="h-24 bg-gradient-to-br from-primary-700 via-primary-800 to-primary-900 relative">
          <div
            class="absolute inset-0 opacity-20"
            style="background-image: radial-gradient(circle, white 1px, transparent 1px); background-size: 24px 24px;"
          />
        </div>

        <div class="px-6 pb-6">
          <!-- Avatar -->
          <div class="flex items-end gap-5 -mt-12">
            <div class="relative">
              <div class="w-24 h-24 rounded-2xl border-4 border-white dark:border-slate-800 bg-gradient-to-br from-accent-400 to-accent-600 grid place-items-center text-white text-2xl font-display font-extrabold overflow-hidden shadow-lg">
                <img v-if="profile.avatar_url" :src="profile.avatar_url" alt="" class="w-full h-full object-cover" />
                <span v-else>{{ initials }}</span>
              </div>
              <label class="absolute -bottom-1 -right-1 w-8 h-8 rounded-full bg-white dark:bg-slate-900 border border-surface-muted dark:border-slate-700 grid place-items-center text-ink-medium hover:text-accent-600 cursor-pointer shadow-md">
                <input type="file" accept="image/*" class="hidden" @change="onUploadAvatar" />
                <Camera class="w-4 h-4" />
              </label>
            </div>
            <div class="flex-1 mb-2">
              <h2 class="text-lg font-display font-bold text-ink-dark dark:text-white">{{ profile.full_name || profile.email }}</h2>
              <div class="flex items-center gap-2 mt-1">
                <span class="inline-flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-md bg-primary-50 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300 font-semibold">
                  <Shield class="w-3 h-3" /> {{ roleLabels[profile.role] || profile.role }}
                </span>
                <span v-if="!profile.is_active" class="text-[11px] px-2 py-0.5 rounded-md bg-danger-light text-danger-dark font-semibold">
                  Faolsiz
                </span>
              </div>
            </div>
            <button v-if="profile.avatar_url" type="button" class="text-xs text-ink-faint hover:text-danger inline-flex items-center gap-1 mb-2" @click="removeAvatar">
              <Trash2 class="w-3 h-3" /> Olib tashlash
            </button>
          </div>

          <!-- Meta info -->
          <dl class="mt-6 grid sm:grid-cols-3 gap-4 text-xs">
            <div>
              <dt class="text-ink-faint uppercase tracking-wider mb-1">Email</dt>
              <dd class="text-ink-medium dark:text-slate-300 font-medium truncate">{{ profile.email }}</dd>
            </div>
            <div>
              <dt class="text-ink-faint uppercase tracking-wider mb-1">Oxirgi kirish</dt>
              <dd class="text-ink-medium dark:text-slate-300 font-medium">{{ fmtDate(profile.last_login) }}</dd>
            </div>
            <div>
              <dt class="text-ink-faint uppercase tracking-wider mb-1">Ro'yxatdan o'tgan</dt>
              <dd class="text-ink-medium dark:text-slate-300 font-medium">{{ fmtDate(profile.created_at) }}</dd>
            </div>
          </dl>
        </div>
      </div>

      <!-- Edit profile -->
      <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-6">
        <div class="flex items-center gap-2 mb-5">
          <UserIcon class="w-5 h-5 text-primary-700 dark:text-primary-300" />
          <h3 class="font-display font-bold text-base text-ink-dark dark:text-white">Profil ma'lumotlari</h3>
        </div>
        <div class="grid sm:grid-cols-2 gap-4">
          <UIInput v-model="profile.full_name" label="Ism-familiya" placeholder="Akmal Rahimov" />
          <UIInput :model-value="profile.email" label="Email" disabled hint="Email o'zgartirilmaydi" />
        </div>
        <div class="mt-5 flex justify-end">
          <UIButton variant="accent" :loading="savingProfile" @click="saveProfile">
            <template #icon-left><Save class="w-4 h-4" /></template>
            Saqlash
          </UIButton>
        </div>
      </div>

      <!-- Change password -->
      <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-6">
        <div class="flex items-center gap-2 mb-5">
          <KeyRound class="w-5 h-5 text-primary-700 dark:text-primary-300" />
          <h3 class="font-display font-bold text-base text-ink-dark dark:text-white">Parolni o'zgartirish</h3>
        </div>
        <div class="space-y-4 max-w-md">
          <UIInput v-model="passwordForm.current_password" type="password" label="Joriy parol" />
          <UIInput v-model="passwordForm.new_password" type="password" label="Yangi parol" hint="Kamida 8 ta belgi" />
          <UIInput v-model="passwordForm.confirm_password" type="password" label="Yangi parolni tasdiqlash" />
        </div>
        <div class="mt-5 flex justify-end">
          <UIButton variant="primary" :loading="savingPassword" @click="changePassword">
            <template #icon-left><KeyRound class="w-4 h-4" /></template>
            Parolni o'zgartirish
          </UIButton>
        </div>
      </div>
    </div>
  </div>
</template>
