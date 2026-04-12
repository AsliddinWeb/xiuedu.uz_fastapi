<script setup>
/**
 * Premium navbar — click-based dropdowns, mega-menu support,
 * sticky scroll, mobile drawer with accordion submenus.
 *
 * Behaviors:
 *  - Click toggles dropdown; clicking another auto-closes the previous.
 *  - v-click-outside (registered globally) closes all dropdowns.
 *  - ESC also closes.
 *  - Single-column dropdowns are compact (220–280px),
 *    mega menus are 520px wide and grid-laid-out.
 */
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, RouterLink } from 'vue-router'
import {
  PhoneIcon, EnvelopeIcon, ChevronDownIcon, Bars3Icon, XMarkIcon,
  ArrowTopRightOnSquareIcon, BuildingLibraryIcon, UserGroupIcon,
  AcademicCapIcon, DocumentTextIcon, BriefcaseIcon, GlobeAltIcon,
  BookOpenIcon, ComputerDesktopIcon, TrophyIcon,
  PhotoIcon, CalendarDaysIcon, ChatBubbleLeftRightIcon,
  StarIcon, ClipboardDocumentListIcon,
  NewspaperIcon, MegaphoneIcon, SunIcon
} from '@heroicons/vue/24/outline'
import LanguageSwitcher from '@/components/ui/LanguageSwitcher.vue'
import ThemeToggle from '@/components/ui/ThemeToggle.vue'
import TelegramIcon from '@/components/icons/TelegramIcon.vue'
import InstagramIcon from '@/components/icons/InstagramIcon.vue'
import FacebookIcon from '@/components/icons/FacebookIcon.vue'
import YoutubeIcon from '@/components/icons/YoutubeIcon.vue'

const { t } = useI18n()
const route = useRoute()

// ===== state =====
const activeDropdown = ref(null)
const mobileOpen = ref(false)
const mobileAccordion = ref(null)
const scrolled = ref(false)

function toggleDropdown(key) {
  activeDropdown.value = activeDropdown.value === key ? null : key
}
function closeAll() { activeDropdown.value = null }
function toggleMobileAccordion(key) {
  mobileAccordion.value = mobileAccordion.value === key ? null : key
}

function handleKey(e) { if (e.key === 'Escape') closeAll() }
function handleScroll() { scrolled.value = window.scrollY > 20 }

onMounted(() => {
  document.addEventListener('keydown', handleKey)
  window.addEventListener('scroll', handleScroll, { passive: true })
  handleScroll()
})
onUnmounted(() => {
  document.removeEventListener('keydown', handleKey)
  window.removeEventListener('scroll', handleScroll)
})

// Auto-close menus on route change
watch(() => route.fullPath, () => {
  closeAll()
  mobileOpen.value = false
  mobileAccordion.value = null
})

// ===== Socials =====
const socials = [
  { name: 'Telegram',  href: 'https://t.me/xalqaro_innovatsion_universiteti', icon: TelegramIcon  },
  { name: 'Instagram', href: 'https://www.instagram.com/xiu_edu.uz',        icon: InstagramIcon },
  { name: 'Facebook',  href: 'https://www.facebook.com/profile.php?id=100090241119598', icon: FacebookIcon },
  { name: 'YouTube',   href: 'https://www.youtube.com/@xiu_youtube',        icon: YoutubeIcon   }
]

// ===== Navigation structure =====
// `megaMenu: true`              → multi-column grid layout (520px wide)
// `children: [...]` (no mega)   → simple single-column dropdown (220–280px)
// `to: ...` (no children)       → direct link
const navItems = computed(() => [
  {
    key: 'university',
    labelKey: 'nav.university',
    megaMenu: true,
    columns: [
      {
        titleKey: 'nav.col_about',
        links: [
          { to: '/about',         labelKey: 'nav.about',       icon: BuildingLibraryIcon },
          { to: '/leadership',    labelKey: 'nav.leadership',  icon: UserGroupIcon },
          { to: '/structure',     labelKey: 'nav.structure',   icon: ClipboardDocumentListIcon },
          { to: '/international', labelKey: 'nav.international', icon: GlobeAltIcon },
          { to: '/careers',       labelKey: 'nav.vacancies',   icon: BriefcaseIcon }
        ]
      },
      {
        titleKey: 'nav.col_documents',
        links: [
          { to: '/p/laws',            labelKey: 'nav.doc_laws',       icon: DocumentTextIcon },
          { to: '/p/decisions',       labelKey: 'nav.doc_decisions',  icon: DocumentTextIcon },
          { to: '/p/labor-code',      labelKey: 'nav.doc_labor_code', icon: DocumentTextIcon },
          { to: '/p/kelajakka-qadam', labelKey: 'nav.doc_kelajakka',  icon: StarIcon },
          { to: '/faculties',         labelKey: 'nav.faculties',      icon: AcademicCapIcon }
        ]
      }
    ]
  },
  {
    key: 'education',
    labelKey: 'nav.education',
    children: [
      { to: '/education/bachelor', labelKey: 'nav.bachelor',   icon: AcademicCapIcon },
      { to: '/education/master',   labelKey: 'nav.master',     icon: BookOpenIcon },
      { to: '/p/management',       labelKey: 'nav.management', icon: BriefcaseIcon }
    ]
  },
  {
    key: 'students',
    labelKey: 'nav.students',
    megaMenu: true,
    columns: [
      {
        titleKey: 'nav.col_e_learning',
        links: [
          { href: 'https://student.xiuedu.uz', external: true, labelKey: 'nav.hemis', icon: ComputerDesktopIcon },
          { to: '/p/courses',  labelKey: 'nav.courses',   icon: BookOpenIcon },
          { to: '/p/schedule', labelKey: 'nav.schedule',  icon: CalendarDaysIcon },
          { to: '/p/exams',    labelKey: 'nav.exams',     icon: DocumentTextIcon }
        ]
      },
      {
        titleKey: 'nav.col_activities',
        links: [
          { to: '/p/clubs/youth',   labelKey: 'nav.club_youth',   icon: UserGroupIcon },
          { to: '/p/clubs/english', labelKey: 'nav.club_english', icon: ChatBubbleLeftRightIcon },
          { to: '/p/clubs/fintech', labelKey: 'nav.club_fintech', icon: StarIcon },
          { to: '/p/sport',         labelKey: 'nav.sport',        icon: TrophyIcon },
          { to: '/gallery',         labelKey: 'nav.student_life', icon: PhotoIcon }
        ]
      }
    ]
  },
  {
    key: 'applicants',
    labelKey: 'nav.applicants',
    megaMenu: true,
    columns: [
      {
        titleKey: 'nav.col_admission',
        links: [
          { to: '/applicants',           labelKey: 'nav.adm_when',     icon: CalendarDaysIcon },
          { to: '/p/admission-docs',     labelKey: 'nav.adm_docs',     icon: DocumentTextIcon },
          { to: '/p/admission-schedule', labelKey: 'nav.adm_schedule', icon: ClipboardDocumentListIcon }
        ]
      },
      {
        titleKey: 'nav.col_education_forms',
        links: [
          { to: '/education/bachelor', labelKey: 'nav.form_full_time', icon: AcademicCapIcon },
          { to: '/education/master',   labelKey: 'nav.master',         icon: BookOpenIcon },
          { href: 'https://qabul.xiuedu.uz', external: true, labelKey: 'nav.apply_online', icon: ArrowTopRightOnSquareIcon }
        ]
      }
    ]
  },
  {
    key: 'media',
    labelKey: 'nav.media',
    children: [
      { to: '/news',     labelKey: 'nav.news',          icon: NewspaperIcon },
      { to: '/events',   labelKey: 'nav.events',        icon: CalendarDaysIcon },
      { to: '/gallery',  labelKey: 'nav.gallery',       icon: PhotoIcon },
      { to: '/p/press',  labelKey: 'nav.press_service', icon: MegaphoneIcon },
      { to: '/p/green',  labelKey: 'nav.green_uni',     icon: SunIcon }
    ]
  },
  {
    key: 'contact',
    labelKey: 'nav.contact',
    to: '/contact'
  }
])

const isActive = (item) =>
  item.to && (route.path === item.to || route.path.startsWith(item.to + '/'))
</script>

<template>
  <!-- ============ Top utility bar ============ -->
  <div class="hidden lg:block relative z-[60] bg-[#080A2D] text-white border-b border-white/[0.06]">
    <div class="container-fluid h-10 flex items-center justify-between text-[12px]">
      <div class="flex items-center gap-6">
        <a href="tel:+998554061515" class="inline-flex items-center gap-1.5 text-white/65 hover:text-accent-400 transition">
          <PhoneIcon class="w-3.5 h-3.5" />
          <span class="font-medium tracking-tight">+998 (55) 406-15-15</span>
        </a>
        <a href="mailto:info@xiuedu.uz" class="inline-flex items-center gap-1.5 text-white/65 hover:text-accent-400 transition">
          <EnvelopeIcon class="w-3.5 h-3.5" />
          <span class="font-medium tracking-tight">info@xiuedu.uz</span>
        </a>
      </div>

      <div class="flex items-center gap-5">
        <a
          href="https://student.xiuedu.uz"
          target="_blank"
          rel="noopener"
          class="inline-flex items-center gap-1.5 text-white/65 hover:text-accent-400 transition font-medium"
        >
          HEMIS
          <ArrowTopRightOnSquareIcon class="w-3 h-3" />
        </a>
        <div class="h-3.5 w-px bg-white/15" />
        <div class="flex items-center gap-1">
          <a
            v-for="s in socials"
            :key="s.name"
            :href="s.href"
            target="_blank"
            rel="noopener"
            :aria-label="s.name"
            class="w-7 h-7 grid place-items-center text-white/55 hover:text-accent-400 transition"
          >
            <component :is="s.icon" class="w-3.5 h-3.5" />
          </a>
        </div>
        <div class="h-3.5 w-px bg-white/15" />
        <LanguageSwitcher compact />
        <ThemeToggle compact />
      </div>
    </div>
  </div>

  <!-- ============ Main navbar ============ -->
  <header
    :class="[
      'sticky top-0 z-50 transition-all duration-300 bg-[#0a0d3d] border-b border-white/[0.08]',
      scrolled && 'shadow-[0_4px_24px_rgba(10,13,61,0.5)]'
    ]"
  >
    <div class="container-fluid">
      <div class="flex items-center justify-between h-[72px]">

        <!-- ===== Logo ===== -->
        <RouterLink to="/" class="flex items-center gap-3 flex-shrink-0">
          <span class="w-11 h-11 rounded-xl bg-gradient-to-br from-primary-600 to-primary-800 grid place-items-center text-white font-display font-bold text-xl shadow-button">
            X
          </span>
          <div class="hidden sm:block leading-tight">
            <div class="text-white font-display font-bold text-sm">
              Xalqaro Innovatsion
            </div>
            <div class="text-white/70 text-xs font-medium">
              Universiteti
            </div>
          </div>
        </RouterLink>

        <!-- ===== Desktop nav ===== -->
        <nav class="hidden xl:flex items-center gap-1" v-click-outside="closeAll">
          <div v-for="item in navItems" :key="item.key" class="relative">

            <!-- Item with dropdown -->
            <button
              v-if="item.children || item.megaMenu"
              type="button"
              :aria-expanded="activeDropdown === item.key"
              :class="[
                'flex items-center gap-1 px-3 py-2 text-sm font-medium transition-all duration-150',
                activeDropdown === item.key
                  ? 'text-white'
                  : 'text-white/75 hover:text-white'
              ]"
              @click.stop="toggleDropdown(item.key)"
            >
              {{ t(item.labelKey) }}
              <ChevronDownIcon
                :class="[
                  'w-3.5 h-3.5 transition-transform duration-200',
                  activeDropdown === item.key && 'rotate-180'
                ]"
              />
            </button>

            <!-- Simple link -->
            <RouterLink
              v-else
              :to="item.to"
              :class="[
                'relative inline-flex px-3 py-2 text-sm font-medium transition-all duration-150',
                isActive(item) ? 'text-white' : 'text-white/75 hover:text-white'
              ]"
            >
              {{ t(item.labelKey) }}
              <span
                v-if="isActive(item)"
                class="absolute left-3 right-3 -bottom-0.5 h-[2px] rounded-full bg-accent-500"
              />
            </RouterLink>

            <!-- Dropdown panel -->
            <Transition name="dropdown">
              <div
                v-if="(item.children || item.megaMenu) && activeDropdown === item.key"
                :class="[
                  'absolute top-full mt-1.5 rounded-xl shadow-dropdown border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-800 overflow-hidden z-50',
                  item.megaMenu ? 'left-0 w-[520px]' : 'left-0 min-w-[220px] max-w-[280px]'
                ]"
              >
                <!-- Mega menu (multi-column) -->
                <div v-if="item.megaMenu" class="p-5">
                  <div class="grid grid-cols-2 gap-x-6 gap-y-1">
                    <div v-for="col in item.columns" :key="col.titleKey">
                      <div class="text-[11px] font-semibold text-ink-faint dark:text-slate-500 uppercase tracking-wider mb-2 px-2">
                        {{ t(col.titleKey) }}
                      </div>
                      <template v-for="link in col.links" :key="link.labelKey">
                        <a
                          v-if="link.external"
                          :href="link.href"
                          target="_blank"
                          rel="noopener"
                          class="flex items-center gap-2.5 px-2 py-2 rounded-lg text-sm text-ink-medium dark:text-slate-300 hover:bg-primary-50 hover:text-primary-700 dark:hover:bg-primary-900/30 dark:hover:text-primary-300 transition group"
                          @click="closeAll"
                        >
                          <span class="text-primary-500 group-hover:text-primary-600 transition-colors">
                            <component :is="link.icon" class="w-4 h-4" />
                          </span>
                          {{ t(link.labelKey) }}
                          <ArrowTopRightOnSquareIcon class="w-3 h-3 ml-auto opacity-0 group-hover:opacity-60 transition" />
                        </a>
                        <RouterLink
                          v-else
                          :to="link.to"
                          class="flex items-center gap-2.5 px-2 py-2 rounded-lg text-sm text-ink-medium dark:text-slate-300 hover:bg-primary-50 hover:text-primary-700 dark:hover:bg-primary-900/30 dark:hover:text-primary-300 transition group"
                          @click="closeAll"
                        >
                          <span class="text-primary-500 group-hover:text-primary-600 transition-colors">
                            <component :is="link.icon" class="w-4 h-4" />
                          </span>
                          {{ t(link.labelKey) }}
                        </RouterLink>
                      </template>
                    </div>
                  </div>
                </div>

                <!-- Simple dropdown -->
                <div v-else class="py-1.5">
                  <RouterLink
                    v-for="link in item.children"
                    :key="link.to"
                    :to="link.to"
                    class="group/link flex items-center gap-2.5 mx-1.5 px-3 py-2 rounded-lg text-sm text-ink-medium dark:text-slate-300 hover:bg-primary-50 hover:text-primary-700 dark:hover:bg-primary-900/30 dark:hover:text-primary-300 transition"
                    @click="closeAll"
                  >
                    <span v-if="link.icon" class="text-primary-500 group-hover/link:text-primary-600 flex-shrink-0 transition-colors">
                      <component :is="link.icon" class="w-4 h-4" />
                    </span>
                    {{ t(link.labelKey) }}
                  </RouterLink>
                </div>
              </div>
            </Transition>
          </div>
        </nav>

        <!-- ===== Right actions ===== -->
        <div class="flex items-center gap-2">
          <a
            href="https://qabul.xiuedu.uz"
            target="_blank"
            rel="noopener"
            class="hidden md:inline-flex items-center gap-1.5 px-5 py-2.5 rounded-xl text-sm font-bold transition-all duration-200 hover:scale-[1.03]"
            style="background: linear-gradient(135deg, #FFB300 0%, #FF8C00 100%); color: #0A0D3D; box-shadow: 0 4px 20px rgba(255,179,0,0.4);"
          >
            {{ t('nav.apply') }}
            <ArrowTopRightOnSquareIcon class="w-3.5 h-3.5" />
          </a>

          <button
            type="button"
            class="xl:hidden p-2 rounded-lg text-white/80 hover:bg-white/10 hover:text-white transition"
            :aria-label="mobileOpen ? t('ui.close_menu') : t('ui.open_menu')"
            @click="mobileOpen = !mobileOpen"
          >
            <Bars3Icon v-if="!mobileOpen" class="w-5 h-5" />
            <XMarkIcon v-else class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>

    <!-- ============ Mobile drawer ============ -->
    <Transition name="mobile-menu">
      <div
        v-if="mobileOpen"
        class="xl:hidden border-t border-white/[0.08] bg-[#0a0d3d]"
      >
        <div class="container-fluid py-3 max-h-[80vh] overflow-y-auto">
          <!-- Utilities -->
          <div class="flex items-center justify-between py-2 mb-2 border-b border-white/[0.08]">
            <LanguageSwitcher />
            <ThemeToggle />
          </div>

          <div v-for="item in navItems" :key="item.key">
            <div v-if="item.children || item.megaMenu">
              <button
                type="button"
                class="w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium text-white/85 hover:bg-white/5 hover:text-white transition"
                @click="toggleMobileAccordion(item.key)"
              >
                {{ t(item.labelKey) }}
                <ChevronDownIcon
                  :class="[
                    'w-4 h-4 text-white/50 transition-transform duration-200',
                    mobileAccordion === item.key && 'rotate-180'
                  ]"
                />
              </button>
              <Transition name="accordion">
                <div
                  v-if="mobileAccordion === item.key"
                  class="ml-3 mb-1 border-l-2 border-white/[0.08] pl-3"
                >
                  <template v-if="item.megaMenu">
                    <template v-for="col in item.columns" :key="col.titleKey">
                      <div class="text-[10px] uppercase tracking-wider text-white/40 mt-2 mb-1 px-2">
                        {{ t(col.titleKey) }}
                      </div>
                      <template v-for="link in col.links" :key="link.labelKey">
                        <a
                          v-if="link.external"
                          :href="link.href"
                          target="_blank"
                          rel="noopener"
                          class="block px-2 py-2 text-sm text-white/65 hover:text-accent-400 rounded-lg hover:bg-white/5 transition"
                          @click="mobileOpen = false"
                        >
                          {{ t(link.labelKey) }} ↗
                        </a>
                        <RouterLink
                          v-else
                          :to="link.to"
                          class="block px-2 py-2 text-sm text-white/65 hover:text-accent-400 rounded-lg hover:bg-white/5 transition"
                          @click="mobileOpen = false"
                        >
                          {{ t(link.labelKey) }}
                        </RouterLink>
                      </template>
                    </template>
                  </template>
                  <template v-else>
                    <RouterLink
                      v-for="link in item.children"
                      :key="link.to"
                      :to="link.to"
                      class="block px-2 py-2 text-sm text-white/65 hover:text-accent-400 rounded-lg hover:bg-white/5 transition"
                      @click="mobileOpen = false"
                    >
                      {{ t(link.labelKey) }}
                    </RouterLink>
                  </template>
                </div>
              </Transition>
            </div>

            <RouterLink
              v-else
              :to="item.to"
              class="block px-3 py-2.5 rounded-lg text-sm font-medium text-white/85 hover:bg-white/5 hover:text-white transition"
              @click="mobileOpen = false"
            >
              {{ t(item.labelKey) }}
            </RouterLink>
          </div>

          <div class="mt-3 pt-3 border-t border-white/[0.08]">
            <a
              href="https://qabul.xiuedu.uz"
              target="_blank"
              rel="noopener"
              class="inline-flex w-full items-center justify-center gap-2 px-6 py-3 rounded-xl text-sm font-bold transition-all duration-200 hover:scale-[1.02]"
              style="background: linear-gradient(135deg, #FFB300 0%, #FF8C00 100%); color: #0A0D3D; box-shadow: 0 4px 20px rgba(255,179,0,0.4);"
              @click="mobileOpen = false"
            >
              {{ t('nav.apply') }}
              <ArrowTopRightOnSquareIcon class="w-4 h-4" />
            </a>
          </div>
        </div>
      </div>
    </Transition>
  </header>
</template>

<style scoped>
/* Dropdown panel transition */
.dropdown-enter-active { animation: dropdownIn 0.2s cubic-bezier(0.4, 0, 0.2, 1); }
.dropdown-leave-active { animation: dropdownIn 0.15s cubic-bezier(0.4, 0, 0.2, 1) reverse; }
@keyframes dropdownIn {
  from { opacity: 0; transform: translateY(-6px) scale(0.98); }
  to   { opacity: 1; transform: translateY(0)    scale(1); }
}

/* Mobile drawer slide */
.mobile-menu-enter-active { animation: drawerSlide 0.25s ease-out; }
.mobile-menu-leave-active { animation: drawerSlide 0.20s ease-in reverse; }
@keyframes drawerSlide {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Accordion submenu */
.accordion-enter-active,
.accordion-leave-active {
  transition: max-height 0.25s ease, opacity 0.2s ease;
  overflow: hidden;
}
.accordion-enter-from,
.accordion-leave-to { opacity: 0; max-height: 0; }
.accordion-enter-to,
.accordion-leave-from { opacity: 1; max-height: 600px; }
</style>
