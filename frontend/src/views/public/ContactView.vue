<script setup>
/**
 * ContactView — driven by /api/page-settings/contact.
 * Contact form still uses /api/contact POST (existing ContactAPI).
 */
import { ref, reactive, onMounted, watch, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import PageHero from '@/components/sections/PageHero.vue'
import UIInput from '@/components/ui/UIInput.vue'
import UIButton from '@/components/ui/UIButton.vue'
import UILoader from '@/components/ui/UILoader.vue'
import { Phone, Mail, MapPin, Clock, Send, CheckCircle2 } from 'lucide-vue-next'
import { ContactAPI, PageSettingsAPI } from '@/api/endpoints'
import { useToast } from '@/composables/useToast'
import { useSeo } from '@/composables/useSeo'
import { breadcrumbSchema } from '@/utils/schema'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import { useLanguageStore } from '@/stores/language'

const { t } = useI18n()
const lang = useLanguageStore()
const toast = useToast()
useScrollAnimation()
useSeo(() => ({
  title: t('contact.title'),
  description: t('contact.subtitle'),
  schema: breadcrumbSchema([
    { name: t('nav.home'),      url: '/' },
    { name: t('contact.title'), url: '/contact' }
  ])
}))

const page = ref(null)
const pageLoading = ref(true)

async function loadPage() {
  pageLoading.value = true
  try {
    page.value = await PageSettingsAPI.contact(lang.currentLang)
  } catch (_) {
    page.value = null
  } finally {
    pageLoading.value = false
  }
}
onMounted(loadPage)
watch(() => lang.currentLang, loadPage)

const cards = computed(() => {
  if (!page.value) return []
  const list = []
  if (page.value.address)
    list.push({ icon: MapPin, label: t('footer.address'), value: page.value.address })
  if (page.value.phone)
    list.push({ icon: Phone, label: t('footer.phone'), value: page.value.phone, href: `tel:${page.value.phone.replace(/\s/g, '')}` })
  if (page.value.email)
    list.push({ icon: Mail, label: t('footer.email'), value: page.value.email, href: `mailto:${page.value.email}` })
  if (page.value.working_hours)
    list.push({ icon: Clock, label: t('footer.working_hours'), value: page.value.working_hours })
  return list
})

const form = reactive({ name: '', email: '', phone: '', subject: '', message: '' })
const errors = reactive({})
const sending = ref(false)
const success = ref(false)

function validate() {
  const e = {}
  if (!form.name || form.name.length < 2) e.name = t('validation.min', { min: 2 })
  if (!form.email || !/^\S+@\S+\.\S+$/.test(form.email)) e.email = t('validation.email')
  if (!form.subject || form.subject.length < 2) e.subject = t('validation.required')
  if (!form.message || form.message.length < 5) e.message = t('validation.min', { min: 5 })
  Object.assign(errors, e)
  Object.keys(errors).forEach(k => { if (!(k in e)) delete errors[k] })
  return Object.keys(e).length === 0
}

async function submit() {
  if (!validate()) return
  sending.value = true
  try {
    await ContactAPI.send({ ...form })
    success.value = true
    toast.success(t('contact.success'))
    form.name = form.email = form.phone = form.subject = form.message = ''
    setTimeout(() => { success.value = false }, 5000)
  } catch (_) {
    toast.error(t('contact.error'))
  } finally {
    sending.value = false
  }
}
</script>

<template>
  <div>
    <PageHero
      :title="page?.hero_title || t('contact.title')"
      :subtitle="page?.hero_subtitle || t('contact.subtitle')"
      :items="[{ label: t('contact.title'), to: '/contact' }]"
      variant="navy"
    />

    <div v-if="pageLoading" class="min-h-[30vh] grid place-items-center">
      <UILoader />
    </div>

    <template v-else>
      <section v-if="cards.length" class="py-12 bg-surface-light dark:bg-slate-800/40 border-y border-surface-muted/60 dark:border-slate-800">
        <div class="container-narrow grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div
            v-for="(c, i) in cards"
            :key="i"
            data-animate
            :data-delay="i * 80"
            class="rounded-2xl p-5 bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 hover:border-accent-300 dark:hover:border-accent-700 hover:shadow-card-hover transition-all"
          >
            <div class="w-11 h-11 rounded-xl bg-accent-50 dark:bg-accent-900/40 grid place-items-center text-accent-600 dark:text-accent-300 mb-3">
              <component :is="c.icon" class="w-5 h-5" />
            </div>
            <p class="text-xs uppercase tracking-wider text-ink-faint mb-1">{{ c.label }}</p>
            <a v-if="c.href" :href="c.href" class="font-semibold text-ink-dark dark:text-white hover:text-primary-600 transition">{{ c.value }}</a>
            <p v-else class="font-semibold text-ink-dark dark:text-white">{{ c.value }}</p>
          </div>
        </div>
      </section>

      <section class="py-24">
        <div class="container-narrow grid lg:grid-cols-[3fr,2fr] gap-8">
          <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-8" data-animate>
            <h2 class="font-display font-bold text-2xl text-ink-dark dark:text-white mb-2">
              {{ page?.form_title || t('contact.send') }}
            </h2>
            <p v-if="page?.form_subtitle" class="text-sm text-ink-light dark:text-slate-400 mb-6">{{ page.form_subtitle }}</p>

            <Transition name="fade">
              <div v-if="success" class="mb-5 p-4 rounded-xl bg-success-light dark:bg-green-900/30 border border-success/40 text-success-dark dark:text-green-300 flex items-center gap-3">
                <CheckCircle2 class="w-5 h-5 flex-shrink-0" />
                <p class="text-sm">{{ t('contact.success') }}</p>
              </div>
            </Transition>

            <form class="space-y-4" @submit.prevent="submit">
              <UIInput v-model="form.name"    :label="t('contact.name')"    :error="errors.name"    required />
              <div class="grid sm:grid-cols-2 gap-4">
                <UIInput v-model="form.email" type="email" :label="t('contact.email')" :error="errors.email" required />
                <UIInput v-model="form.phone" :label="t('contact.phone')" />
              </div>
              <UIInput v-model="form.subject" :label="t('contact.subject')" :error="errors.subject" required />
              <UIInput v-model="form.message" textarea :rows="5" :label="t('contact.message')" :error="errors.message" required />

              <UIButton type="submit" variant="accent" block size="lg" :loading="sending">
                {{ sending ? t('contact.sending') : t('contact.send') }}
                <template #icon-right><Send class="w-4 h-4" /></template>
              </UIButton>
            </form>
          </div>

          <div v-if="page?.map_embed_url" class="rounded-2xl overflow-hidden border border-surface-muted dark:border-slate-700 min-h-[28rem] lg:min-h-0" data-animate data-delay="200">
            <iframe
              :src="page.map_embed_url"
              loading="lazy"
              class="w-full h-full min-h-[28rem]"
              frameborder="0"
              :title="t('contact.map')"
            />
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from,
.fade-leave-to { opacity: 0; }
</style>
