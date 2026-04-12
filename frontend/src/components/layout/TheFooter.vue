<script setup>
/**
 * Premium 4-column footer — deep teal gradient, gold accent stripe.
 */
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { MapPin, Phone, Mail, Clock, ArrowRight, Award, ShieldCheck } from 'lucide-vue-next'
import TelegramIcon  from '@/components/icons/TelegramIcon.vue'
import InstagramIcon from '@/components/icons/InstagramIcon.vue'
import FacebookIcon  from '@/components/icons/FacebookIcon.vue'
import YoutubeIcon   from '@/components/icons/YoutubeIcon.vue'

const { t } = useI18n()
const year = computed(() => new Date().getFullYear())

const quickLinks = [
  { to: '/about',              key: 'nav.about' },
  { to: '/faculties',          key: 'nav.faculties' },
  { to: '/education/bachelor', key: 'nav.bachelor' },
  { to: '/education/master',   key: 'nav.master' },
  { to: '/applicants',         key: 'nav.admission' },
  { to: '/international',      key: 'nav.international' }
]

const studentLinks = [
  { href: 'https://hemis.uz', external: true, key: 'nav.hemis' },
  { to: '/p/courses',  key: 'nav.courses' },
  { to: '/p/clubs',    key: 'nav.clubs' },
  { to: '/p/sport',    key: 'nav.sport' },
  { to: '/p/schedule', key: 'nav.schedule' },
  { to: '/gallery',    key: 'nav.gallery' }
]

const socials = [
  { name: 'Telegram',  href: 'https://t.me/xalqaro_innovatsion_universiteti', icon: TelegramIcon  },
  { name: 'Instagram', href: 'https://www.instagram.com/xiu_edu.uz',        icon: InstagramIcon },
  { name: 'Facebook',  href: 'https://www.facebook.com/profile.php?id=100090241119598', icon: FacebookIcon },
  { name: 'YouTube',   href: 'https://www.youtube.com/@xiu_youtube',        icon: YoutubeIcon   }
]
</script>

<template>
  <footer
    class="relative text-white overflow-hidden"
    style="background: linear-gradient(180deg, #0F1550 0%, #0A0D3D 100%);"
  >
    <!-- Top accent stripe -->
    <div
      class="h-0.5"
      style="background: linear-gradient(90deg, #2D3A8C 0%, #FFB300 50%, #2D3A8C 100%);"
    />

    <!-- Decorative blob -->
    <div class="absolute -top-32 -right-32 w-96 h-96 rounded-full bg-primary-500/8 blur-3xl pointer-events-none" />
    <div class="absolute -bottom-32 left-1/4 w-72 h-72 rounded-full bg-accent-500/5 blur-3xl pointer-events-none" />

    <div class="container-narrow relative pt-16 pb-10">
      <div class="grid gap-12 md:grid-cols-2 lg:grid-cols-4">

        <!-- Col 1: Brand -->
        <div>
          <div class="flex items-center gap-3 mb-5">
            <span class="w-12 h-12 rounded-xl grid place-items-center text-white font-display font-bold text-2xl"
                  style="background: linear-gradient(135deg, #1A1F6E, #0A0D3D); box-shadow: 0 4px 24px rgba(26,31,110,0.5);">
              X
            </span>
            <div class="leading-tight">
              <p class="font-display text-lg font-bold text-white">XIU Edu</p>
              <p class="text-[11px] text-primary-200/60">{{ t('site.short') }}</p>
            </div>
          </div>
          <p class="text-sm text-primary-200/60 leading-relaxed mb-5">
            {{ t('footer.description') }}
          </p>
          <div class="flex items-center gap-2 flex-wrap">
            <span class="inline-flex items-center gap-1.5 text-[10px] uppercase tracking-wider text-accent-400 px-2 py-1 border border-accent-500/30 rounded">
              <Award class="w-3 h-3" /> {{ t('footer.accreditation') }}
            </span>
            <span class="inline-flex items-center gap-1.5 text-[10px] uppercase tracking-wider text-accent-400 px-2 py-1 border border-accent-500/30 rounded">
              <ShieldCheck class="w-3 h-3" /> ISO 9001
            </span>
          </div>
        </div>

        <!-- Col 2: Quick links -->
        <div>
          <h4 class="text-white text-sm font-display font-semibold mb-5 relative inline-block">
            {{ t('footer.quick_links') }}
            <span class="absolute -bottom-1 left-0 w-8 h-0.5 bg-accent-500" />
          </h4>
          <ul class="space-y-2.5">
            <li v-for="l in quickLinks" :key="l.to">
              <RouterLink
                :to="l.to"
                class="group inline-flex items-center gap-1.5 text-sm text-primary-200/60 hover:text-accent-400 transition"
              >
                <ArrowRight class="w-3 h-3 opacity-0 -ml-4 group-hover:opacity-100 group-hover:ml-0 transition-all" />
                {{ t(l.key) }}
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- Col 3: Students -->
        <div>
          <h4 class="text-white text-sm font-display font-semibold mb-5 relative inline-block">
            {{ t('footer.students_resources') }}
            <span class="absolute -bottom-1 left-0 w-8 h-0.5 bg-accent-500" />
          </h4>
          <ul class="space-y-2.5">
            <li v-for="l in studentLinks" :key="l.key">
              <a
                v-if="l.external"
                :href="l.href"
                target="_blank"
                rel="noopener"
                class="group inline-flex items-center gap-1.5 text-sm text-primary-200/60 hover:text-accent-400 transition"
              >
                <ArrowRight class="w-3 h-3 opacity-0 -ml-4 group-hover:opacity-100 group-hover:ml-0 transition-all" />
                {{ t(l.key) }}
              </a>
              <RouterLink
                v-else
                :to="l.to"
                class="group inline-flex items-center gap-1.5 text-sm text-primary-200/60 hover:text-accent-400 transition"
              >
                <ArrowRight class="w-3 h-3 opacity-0 -ml-4 group-hover:opacity-100 group-hover:ml-0 transition-all" />
                {{ t(l.key) }}
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- Col 4: Contact -->
        <div>
          <h4 class="text-white text-sm font-display font-semibold mb-5 relative inline-block">
            {{ t('footer.contact_us') }}
            <span class="absolute -bottom-1 left-0 w-8 h-0.5 bg-accent-500" />
          </h4>
          <ul class="space-y-3 text-sm text-primary-200/60">
            <li class="flex items-start gap-3">
              <MapPin class="w-4 h-4 mt-0.5 text-accent-500 flex-shrink-0" />
              <span>{{ t('footer.address_value') }}</span>
            </li>
            <li class="flex items-start gap-3">
              <Phone class="w-4 h-4 mt-0.5 text-accent-500 flex-shrink-0" />
              <a href="tel:+998554061515" class="hover:text-accent-400 transition">+998 55 406-15-15</a>
            </li>
            <li class="flex items-start gap-3">
              <Mail class="w-4 h-4 mt-0.5 text-accent-500 flex-shrink-0" />
              <a href="mailto:info@xiuedu.uz" class="hover:text-accent-400 transition">info@xiuedu.uz</a>
            </li>
            <li class="flex items-start gap-3">
              <Clock class="w-4 h-4 mt-0.5 text-accent-500 flex-shrink-0" />
              <span>{{ t('footer.working_hours_value') }}</span>
            </li>
          </ul>

          <div class="mt-5">
            <p class="text-[10px] text-primary-200/40 mb-2 uppercase tracking-wider">{{ t('footer.follow_us') }}</p>
            <div class="flex items-center gap-2">
              <a
                v-for="s in socials"
                :key="s.name"
                :href="s.href"
                target="_blank"
                rel="noopener"
                :aria-label="s.name"
                class="w-9 h-9 grid place-items-center rounded-lg border border-white/10 text-primary-200/70 hover:bg-accent-500 hover:border-accent-500 hover:text-white transition"
                style="background: rgba(255,255,255,0.04);"
              >
                <component :is="s.icon" class="w-4 h-4" />
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom bar -->
      <div class="mt-14 pt-6 border-t border-white/[0.07] flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-primary-200/40">
        <p>© {{ year }} {{ t('site.name') }}. {{ t('footer.rights') }}.</p>
        <div class="flex items-center gap-5">
          <RouterLink to="/p/privacy" class="hover:text-accent-400 transition">{{ t('footer.privacy') }}</RouterLink>
          <RouterLink to="/p/terms"   class="hover:text-accent-400 transition">{{ t('footer.terms') }}</RouterLink>
        </div>
      </div>
    </div>
  </footer>
</template>
