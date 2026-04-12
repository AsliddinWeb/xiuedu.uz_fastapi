<script setup>
/**
 * LeadershipView — fully driven by /api/leaders/.
 *
 * Same visual hierarchy as before (rector → prorectors → deans →
 * department heads) but rows now come from the Leader DB table and
 * can be edited via /admin/leaders.
 */
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { Mail, Phone, Award, GraduationCap, Briefcase } from 'lucide-vue-next'
import PageHero from '@/components/sections/PageHero.vue'
import UIModal from '@/components/ui/UIModal.vue'
import UILoader from '@/components/ui/UILoader.vue'
import { LeadersAPI } from '@/api/endpoints'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { useSeo } from '@/composables/useSeo'
import { breadcrumbSchema, graph } from '@/utils/schema'
import { useLanguageStore } from '@/stores/language'

const { t } = useI18n()
const lang = useLanguageStore()
useScrollAnimation()
useSeo(() => ({
  title: t('leadership.title'),
  description: t('leadership.subtitle'),
  type: 'website',
  schema: graph(breadcrumbSchema([
    { name: t('nav.home'),         url: '/' },
    { name: t('leadership.title'), url: '/leadership' }
  ]))
}))

const leaders = ref([])
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    leaders.value = await LeadersAPI.list(lang.currentLang)
  } catch (_) {
    leaders.value = []
  } finally {
    loading.value = false
  }
}
onMounted(load)
watch(() => lang.currentLang, load)

const rector       = computed(() => leaders.value.find(l => l.group === 'rector'))
const prorectors   = computed(() => leaders.value.filter(l => l.group === 'prorector'))
const deans        = computed(() => leaders.value.filter(l => l.group === 'dean'))
const departments  = computed(() => leaders.value.filter(l => l.group === 'department_head'))

function initials(name) {
  return (name || 'U').split(/\s+/).map(s => s[0]).slice(0, 2).join('').toUpperCase()
}

const open = ref(false)
const selected = ref(null)
function showBio(p) { selected.value = p; open.value = true }
</script>

<template>
  <div>
    <PageHero
      :title="t('leadership.title')"
      :subtitle="t('leadership.subtitle')"
      :items="[{ label: t('leadership.title'), to: '/leadership' }]"
    />

    <!-- Loading -->
    <div v-if="loading" class="min-h-[40vh] grid place-items-center">
      <UILoader />
    </div>

    <template v-else>
      <!-- ═══════════════════════════════════════════════════════
           Rector — featured hero card
      ════════════════════════════════════════════════════════════ -->
      <section v-if="rector" class="py-20 lg:py-24">
        <div class="container-narrow">
          <div data-animate class="text-center mb-12">
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ t('leadership.section_rector') }}</p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white tracking-tight">{{ t('leadership.section_rector_title') }}</h2>
          </div>

          <div data-animate data-delay="100" class="relative overflow-hidden rounded-3xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 shadow-[0_30px_80px_rgba(10,13,61,0.10)]">
            <div class="h-2 bg-gradient-to-r from-primary-700 via-primary-800 to-accent-500" />

            <div class="grid lg:grid-cols-[320px_1fr] gap-0">
              <div class="relative bg-gradient-to-br from-primary-50 to-accent-50/40 dark:from-slate-900 dark:to-slate-800/50 p-8 lg:p-10 grid place-items-center">
                <div class="relative">
                  <div class="absolute -inset-3 rounded-2xl opacity-20 blur-xl" style="background: linear-gradient(135deg, #FFB300 0%, #FF8C00 100%);" />
                  <img v-if="rector.photo" :src="rector.photo" :alt="rector.name"
                       class="relative w-44 h-56 lg:w-52 lg:h-64 rounded-2xl object-cover shadow-xl border-4 border-white dark:border-slate-700" />
                  <div v-else class="relative w-44 h-56 lg:w-52 lg:h-64 rounded-2xl bg-gradient-to-br from-primary-700 to-primary-900 grid place-items-center text-white text-6xl font-display font-bold shadow-xl border-4 border-white dark:border-slate-700">
                    {{ initials(rector.name) }}
                  </div>
                  <div class="absolute -bottom-3 -right-3 w-12 h-12 rounded-2xl bg-gradient-to-br from-accent-400 to-accent-600 grid place-items-center shadow-lg ring-4 ring-white dark:ring-slate-800">
                    <Award class="w-6 h-6 text-primary-900" stroke-width="2" />
                  </div>
                </div>
              </div>

              <div class="p-8 lg:p-10 flex flex-col">
                <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent-50 dark:bg-accent-900/30 text-accent-700 dark:text-accent-300 text-[11px] font-bold uppercase tracking-wider self-start mb-4">
                  <span class="w-1.5 h-1.5 rounded-full bg-accent-500" />
                  {{ rector.position }}
                </div>
                <h3 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white leading-tight mb-2">{{ rector.name }}</h3>
                <p v-if="rector.degree" class="text-[14px] text-ink-light dark:text-slate-400 mb-5 inline-flex items-center gap-1.5">
                  <GraduationCap class="w-4 h-4 text-primary-600" /> {{ rector.degree }}
                </p>
                <p v-if="rector.bio" class="text-[15px] text-ink-medium dark:text-slate-300 leading-relaxed mb-6 flex-1">{{ rector.bio }}</p>

                <div v-if="rector.email || rector.phone" class="flex flex-wrap gap-3 pt-5 border-t border-surface-muted dark:border-slate-700">
                  <a v-if="rector.email" :href="`mailto:${rector.email}`"
                     class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-primary-50 hover:bg-primary-100 dark:bg-slate-700 dark:hover:bg-slate-600 text-primary-800 dark:text-white text-[13px] font-semibold transition">
                    <Mail class="w-4 h-4" /> {{ rector.email }}
                  </a>
                  <a v-if="rector.phone" :href="`tel:${rector.phone.replace(/\s/g, '')}`"
                     class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-surface-soft hover:bg-surface-muted dark:bg-slate-700 dark:hover:bg-slate-600 text-ink-medium dark:text-slate-300 text-[13px] font-semibold transition">
                    <Phone class="w-4 h-4" /> {{ rector.phone }}
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           Prorectors
      ════════════════════════════════════════════════════════════ -->
      <section v-if="prorectors.length" class="py-20 lg:py-24 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div data-animate class="text-center mb-12">
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ t('leadership.section_prorectors') }}</p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white tracking-tight">{{ t('leadership.section_prorectors_title') }}</h2>
          </div>

          <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <button v-for="(p, i) in prorectors" :key="p.id" data-animate :data-delay="i * 80"
                    class="group text-left rounded-2xl p-7 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-primary-300 dark:hover:border-primary-600 hover:shadow-[0_20px_50px_rgba(10,13,61,0.10)] hover:-translate-y-1 transition-all duration-300"
                    @click="showBio(p)">
              <div class="flex items-center gap-4 mb-5">
                <div v-if="p.photo" class="w-16 h-16 rounded-2xl overflow-hidden shadow-md flex-shrink-0">
                  <img :src="p.photo" :alt="p.name" class="w-full h-full object-cover" />
                </div>
                <div v-else class="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-700 to-primary-900 grid place-items-center text-white text-2xl font-display font-bold shadow-md flex-shrink-0">
                  {{ initials(p.name) }}
                </div>
                <div class="flex-1 min-w-0">
                  <h3 class="text-base font-display font-bold text-ink-dark dark:text-white leading-tight group-hover:text-primary-700 dark:group-hover:text-primary-300 transition-colors">{{ p.name }}</h3>
                  <p v-if="p.degree" class="text-[11px] text-ink-faint mt-1 inline-flex items-center gap-1">
                    <GraduationCap class="w-3 h-3" /> {{ p.degree }}
                  </p>
                </div>
              </div>
              <p class="inline-flex items-center gap-1.5 text-[12px] font-semibold text-accent-700 dark:text-accent-400 px-2.5 py-1 rounded-md bg-accent-50 dark:bg-accent-900/30 mb-4">
                <Briefcase class="w-3 h-3" /> {{ p.position }}
              </p>
              <p v-if="p.bio" class="text-[13px] text-ink-light dark:text-slate-400 leading-relaxed line-clamp-3 mb-4">{{ p.bio }}</p>
              <p v-if="p.email" class="pt-4 border-t border-surface-muted dark:border-slate-700 text-[11px] text-primary-700 dark:text-primary-300 inline-flex items-center gap-1.5 font-semibold">
                <Mail class="w-3 h-3" /> {{ p.email }}
              </p>
            </button>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           Deans
      ════════════════════════════════════════════════════════════ -->
      <section v-if="deans.length" class="py-20 lg:py-24">
        <div class="container-narrow">
          <div data-animate class="text-center mb-12">
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ t('leadership.section_deans') }}</p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white tracking-tight">{{ t('leadership.section_deans_title') }}</h2>
          </div>

          <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <button v-for="(p, i) in deans" :key="p.id" data-animate :data-delay="i * 80"
                    class="group text-left rounded-2xl p-6 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-accent-300 dark:hover:border-accent-700 hover:shadow-[0_18px_44px_rgba(10,13,61,0.10)] hover:-translate-y-0.5 transition-all duration-300"
                    @click="showBio(p)">
              <div class="flex items-start gap-4">
                <div v-if="p.photo" class="w-14 h-14 rounded-xl overflow-hidden shadow-md flex-shrink-0">
                  <img :src="p.photo" :alt="p.name" class="w-full h-full object-cover" />
                </div>
                <div v-else class="w-14 h-14 rounded-xl bg-gradient-to-br from-accent-400 to-accent-600 grid place-items-center text-primary-900 text-xl font-display font-extrabold shadow-md flex-shrink-0">
                  {{ initials(p.name) }}
                </div>
                <div class="flex-1 min-w-0">
                  <h3 class="text-base font-display font-bold text-ink-dark dark:text-white leading-tight group-hover:text-primary-700 dark:group-hover:text-primary-300 transition-colors">{{ p.name }}</h3>
                  <p class="text-[12px] font-semibold text-accent-700 dark:text-accent-400 mt-1">{{ p.position }}</p>
                  <p v-if="p.degree" class="text-[11px] text-ink-faint mt-2 inline-flex items-center gap-1">
                    <GraduationCap class="w-3 h-3" /> {{ p.degree }}
                  </p>
                  <p v-if="p.email" class="text-[11px] text-ink-light mt-3 inline-flex items-center gap-1.5">
                    <Mail class="w-3 h-3" /> {{ p.email }}
                  </p>
                </div>
              </div>
            </button>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════════════════════════════
           Department heads
      ════════════════════════════════════════════════════════════ -->
      <section v-if="departments.length" class="py-20 lg:py-24 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow">
          <div data-animate class="text-center mb-12">
            <p class="text-[12px] font-semibold uppercase tracking-[0.2em] text-accent-600 mb-3">{{ t('leadership.section_departments') }}</p>
            <h2 class="text-3xl md:text-4xl font-display font-bold text-ink-dark dark:text-white tracking-tight">{{ t('leadership.section_departments_title') }}</h2>
          </div>

          <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <button v-for="(p, i) in departments" :key="p.id" data-animate :data-delay="i * 60"
                    class="group text-left rounded-xl p-5 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-primary-300 dark:hover:border-primary-600 hover:shadow-md transition-all"
                    @click="showBio(p)">
              <div v-if="p.photo" class="w-12 h-12 rounded-xl overflow-hidden mb-3">
                <img :src="p.photo" :alt="p.name" class="w-full h-full object-cover" />
              </div>
              <div v-else class="w-12 h-12 rounded-xl bg-primary-50 dark:bg-slate-700 grid place-items-center text-primary-700 dark:text-primary-300 text-lg font-display font-bold mb-3">
                {{ initials(p.name) }}
              </div>
              <h3 class="text-sm font-display font-bold text-ink-dark dark:text-white leading-tight group-hover:text-primary-700 dark:group-hover:text-primary-300 transition-colors line-clamp-1">{{ p.name }}</h3>
              <p class="text-[11px] text-ink-light dark:text-slate-400 mt-1.5 line-clamp-2 leading-snug">{{ p.position }}</p>
            </button>
          </div>
        </div>
      </section>

      <!-- Empty state -->
      <div v-if="!leaders.length" class="container-narrow py-24 text-center">
        <p class="text-ink-faint">{{ t('common.not_found') }}</p>
      </div>
    </template>

    <!-- ═══════════════════════════════════════════════════════
         Bio modal
    ════════════════════════════════════════════════════════════ -->
    <UIModal v-model="open" size="lg" :title="selected?.name">
      <div v-if="selected" class="flex flex-col sm:flex-row gap-6">
        <div v-if="selected.photo" class="w-32 h-32 rounded-2xl overflow-hidden flex-shrink-0 shadow-lg">
          <img :src="selected.photo" :alt="selected.name" class="w-full h-full object-cover" />
        </div>
        <div v-else class="w-32 h-32 rounded-2xl bg-gradient-to-br from-primary-700 to-primary-900 grid place-items-center text-white font-display font-bold text-4xl shadow-lg flex-shrink-0">
          {{ initials(selected.name) }}
        </div>
        <div class="flex-1">
          <p class="text-sm font-semibold text-accent-600 mb-1">{{ selected.position }}</p>
          <p v-if="selected.degree" class="text-xs text-ink-faint mb-3 inline-flex items-center gap-1">
            <GraduationCap class="w-3 h-3" /> {{ selected.degree }}
          </p>
          <p v-if="selected.bio" class="text-ink-medium dark:text-slate-300 leading-relaxed mb-4">{{ selected.bio }}</p>
          <div class="flex flex-wrap gap-3">
            <a v-if="selected.email" :href="`mailto:${selected.email}`" class="inline-flex items-center gap-2 text-sm text-primary-700 dark:text-accent-400 hover:underline">
              <Mail class="w-4 h-4" /> {{ selected.email }}
            </a>
            <a v-if="selected.phone" :href="`tel:${selected.phone.replace(/\s/g, '')}`" class="inline-flex items-center gap-2 text-sm text-ink-light hover:text-primary-700">
              <Phone class="w-4 h-4" /> {{ selected.phone }}
            </a>
          </div>
        </div>
      </div>
    </UIModal>
  </div>
</template>
