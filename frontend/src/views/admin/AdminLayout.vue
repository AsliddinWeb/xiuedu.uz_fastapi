<script setup>
/**
 * Admin shell — Linear / Vercel inspired.
 * Collapsible sidebar (60 ↔ 240), role-filtered nav groups,
 * compact topbar with breadcrumb + user controls.
 */
import { ref, computed, onMounted, watch } from 'vue'
import { RouterView, RouterLink, useRoute, useRouter } from 'vue-router'
import {
  HomeIcon, NewspaperIcon, CalendarDaysIcon, FolderIcon,
  DocumentTextIcon, UserGroupIcon, MagnifyingGlassIcon, UserCircleIcon,
  BuildingLibraryIcon, BuildingOffice2Icon, AcademicCapIcon, GlobeAltIcon,
  BriefcaseIcon, PhoneIcon, PhotoIcon,
  Bars3Icon, BellIcon, ArrowTopRightOnSquareIcon, ArrowRightOnRectangleIcon
} from '@heroicons/vue/24/outline'

import { useAuthStore } from '@/stores/auth'
import LanguageSwitcher  from '@/components/ui/LanguageSwitcher.vue'
import ThemeToggle       from '@/components/ui/ThemeToggle.vue'
import UIBreadcrumb      from '@/components/ui/UIBreadcrumb.vue'
import UIToast           from '@/components/ui/UIToast.vue'
import UIConfirmDialog   from '@/components/ui/UIConfirmDialog.vue'
import { roleBadge } from '@/utils/roles'

const auth   = useAuthStore()
const route  = useRoute()
const router = useRouter()

const sidebarCollapsed = ref(localStorage.getItem('xiuedu_admin_collapsed') === '1')
function toggleSidebar() {
  sidebarCollapsed.value = !sidebarCollapsed.value
  localStorage.setItem('xiuedu_admin_collapsed', sidebarCollapsed.value ? '1' : '0')
}

const draftCount = ref(null)

const navGroups = computed(() => {
  const role = auth.role
  const all = [
    {
      title: 'Asosiy',
      items: [
        { to: '/admin', exact: true, label: 'Dashboard', icon: HomeIcon }
      ]
    },
    {
      title: 'Kontent',
      roles: ['admin', 'content_manager'],
      items: [
        { to: '/admin/news',             label: 'Yangiliklar', icon: NewspaperIcon, badge: draftCount.value || null },
        { to: '/admin/events',           label: 'Tadbirlar',   icon: CalendarDaysIcon },
        { to: '/admin/gallery-settings', label: 'Galereya',    icon: PhotoIcon },
        { to: '/admin/media',            label: 'Media',       icon: FolderIcon }
      ]
    },
    {
      title: 'Sahifalar',
      roles: ['admin', 'page_editor', 'content_manager'],
      items: [
        { to: '/admin/home-settings',          label: 'Bosh sahifa',         icon: HomeIcon },
        { to: '/admin/about-settings',         label: 'Universitet haqida',  icon: BuildingLibraryIcon },
        { to: '/admin/structure-settings',     label: 'Tarkibiy tuzilma',    icon: BuildingOffice2Icon },
        { to: '/admin/international-settings', label: 'Xalqaro hamkorlik',   icon: GlobeAltIcon },
        { to: '/admin/applicants-settings',    label: 'Abituriyentlarga',    icon: AcademicCapIcon },
        { to: '/admin/vacancies-settings',     label: 'Vakansiyalar',        icon: BriefcaseIcon },
        { to: '/admin/contact-settings',      label: 'Aloqa sahifasi',      icon: PhoneIcon },
        { to: '/admin/leaders',                label: 'Rahbariyat',          icon: UserGroupIcon },
        { to: '/admin/pages',                  label: 'Boshqa sahifalar',    icon: DocumentTextIcon }
      ]
    },
    {
      title: 'Tizim',
      roles: ['admin', 'content_manager'],
      items: [
        { to: '/admin/users', label: 'Foydalanuvchilar', icon: UserGroupIcon },
        { to: '/admin/seo',   label: 'SEO va URL',       icon: MagnifyingGlassIcon }
      ]
    },
    {
      title: 'Hisob',
      items: [
        { to: '/admin/profile', label: 'Mening kabinetim', icon: UserCircleIcon }
      ]
    }
  ]
  return all.filter(g => !g.roles || g.roles.includes(role) || role === 'superadmin')
})

const badge = computed(() => roleBadge(auth.user?.role))

const mobileOpen = ref(false)
watch(() => route.fullPath, () => { mobileOpen.value = false })

async function logout() {
  await auth.logout()
  router.push('/login')
}

onMounted(async () => {
  if (auth.isAuthenticated && !auth.user) await auth.loadMe()
})

function isActive(item) {
  if (item.exact) return route.path === item.to
  return route.path === item.to || route.path.startsWith(item.to + '/')
}

const sidebarCls = computed(() => [
  'flex flex-col bg-white dark:bg-slate-900 border-r border-surface-muted dark:border-slate-800 transition-all duration-300 flex-shrink-0 h-full',
  sidebarCollapsed.value ? 'w-[60px]' : 'w-[240px]',
  mobileOpen.value ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',
  'fixed lg:static inset-y-0 left-0 z-40'
])
</script>

<template>
  <div class="flex h-screen bg-surface-light dark:bg-[#0A0F1E] overflow-hidden">
    <!-- ===== Sidebar ===== -->
    <aside :class="sidebarCls">
      <div class="flex items-center gap-3 px-4 h-16 border-b border-surface-muted dark:border-slate-800">
        <span class="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-600 to-primary-800 grid place-items-center text-white font-display font-bold text-sm flex-shrink-0">X</span>
        <span v-if="!sidebarCollapsed" class="font-display font-bold text-primary-800 dark:text-white text-sm whitespace-nowrap">
          XIU Admin
        </span>
      </div>

      <nav class="flex-1 py-4 overflow-y-auto">
        <div v-for="group in navGroups" :key="group.title" class="mb-4">
          <div
            v-if="!sidebarCollapsed"
            class="px-4 mb-1 text-[10px] font-semibold uppercase tracking-wider text-ink-faint dark:text-slate-500"
          >
            {{ group.title }}
          </div>
          <RouterLink
            v-for="item in group.items"
            :key="item.to"
            :to="item.to"
            v-tooltip="sidebarCollapsed ? item.label : ''"
            :class="[
              'relative flex items-center gap-3 mx-2 rounded-lg transition-all duration-150',
              sidebarCollapsed ? 'px-2 py-2.5 justify-center' : 'px-3 py-2',
              isActive(item)
                ? 'bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 font-semibold'
                : 'text-ink-medium dark:text-slate-400 hover:bg-surface-soft dark:hover:bg-slate-800 hover:text-ink-dark dark:hover:text-white'
            ]"
          >
            <span
              v-if="isActive(item)"
              class="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 bg-primary-600 rounded-r-full"
            />
            <component :is="item.icon" class="w-4 h-4 flex-shrink-0" />
            <span v-if="!sidebarCollapsed" class="text-sm flex-1">{{ item.label }}</span>
            <span
              v-if="!sidebarCollapsed && item.badge"
              class="ml-auto text-[10px] px-1.5 py-0.5 rounded-full bg-primary-100 dark:bg-primary-900/50 text-primary-700 dark:text-primary-300 font-bold"
            >
              {{ item.badge }}
            </span>
          </RouterLink>
        </div>
      </nav>

      <div class="border-t border-surface-muted dark:border-slate-800 p-3">
        <div :class="['flex items-center gap-3', sidebarCollapsed && 'justify-center']">
          <RouterLink
            to="/admin/profile"
            class="w-8 h-8 rounded-full bg-gradient-to-br from-primary-500 to-primary-800 grid place-items-center text-white text-xs font-bold flex-shrink-0 ring-2 ring-primary-100 dark:ring-primary-900 overflow-hidden hover:ring-accent-300 transition"
            v-tooltip="sidebarCollapsed ? 'Mening kabinetim' : null"
          >
            <img v-if="auth.user?.avatar_url" :src="auth.user.avatar_url" alt="" class="w-full h-full object-cover" />
            <span v-else>{{ (auth.user?.full_name || 'U').charAt(0) }}</span>
          </RouterLink>
          <RouterLink
            v-if="!sidebarCollapsed"
            to="/admin/profile"
            class="flex-1 min-w-0 hover:opacity-80 transition"
          >
            <div class="text-xs font-semibold text-ink-dark dark:text-white truncate">
              {{ auth.user?.full_name || '...' }}
            </div>
            <div class="text-[10px] text-ink-faint">{{ badge.label }}</div>
          </RouterLink>
          <button
            v-if="!sidebarCollapsed"
            @click="logout"
            class="p-1.5 rounded-lg hover:bg-surface-soft dark:hover:bg-slate-700 text-ink-faint hover:text-danger transition-colors"
            v-tooltip="'Chiqish'"
          >
            <ArrowRightOnRectangleIcon class="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>

    <!-- Mobile backdrop -->
    <div
      v-if="mobileOpen"
      class="fixed inset-0 z-30 bg-black/50 backdrop-blur-sm lg:hidden"
      @click="mobileOpen = false"
    />

    <!-- ===== Main column ===== -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <header class="h-16 bg-white dark:bg-slate-900 border-b border-surface-muted dark:border-slate-800 flex items-center px-4 lg:px-6 gap-4 flex-shrink-0">
        <button
          class="p-1.5 rounded-lg hover:bg-surface-soft dark:hover:bg-slate-800 text-ink-faint transition-colors lg:hidden"
          @click="mobileOpen = true"
          aria-label="Menu"
        >
          <Bars3Icon class="w-4 h-4" />
        </button>
        <button
          class="p-1.5 rounded-lg hover:bg-surface-soft dark:hover:bg-slate-800 text-ink-faint transition-colors hidden lg:block"
          @click="toggleSidebar"
          aria-label="Toggle sidebar"
        >
          <Bars3Icon class="w-4 h-4" />
        </button>

        <UIBreadcrumb class="flex-1 text-xs" />

        <div class="flex items-center gap-2">
          <LanguageSwitcher />
          <ThemeToggle />
          <button
            class="relative p-1.5 rounded-lg hover:bg-surface-soft dark:hover:bg-slate-800 text-ink-faint transition-colors"
            aria-label="Notifications"
          >
            <BellIcon class="w-4 h-4" />
            <span class="absolute top-1 right-1 w-1.5 h-1.5 bg-accent-500 rounded-full" />
          </button>
          <a
            href="/"
            target="_blank"
            rel="noopener"
            class="hidden md:inline-flex items-center gap-1.5 text-xs font-medium text-ink-faint hover:text-primary-600 transition-colors px-2"
          >
            <ArrowTopRightOnSquareIcon class="w-3.5 h-3.5" />
            Saytni ko'rish
          </a>
        </div>
      </header>

      <main class="flex-1 overflow-y-auto p-4 lg:p-6">
        <RouterView />
      </main>
    </div>

    <UIToast />
    <UIConfirmDialog />
  </div>
</template>
