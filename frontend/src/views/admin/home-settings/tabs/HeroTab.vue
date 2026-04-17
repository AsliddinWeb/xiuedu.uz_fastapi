<script setup>
/**
 * Hero settings — singleton row with variant-driven layout.
 */
import { ref, reactive, onMounted, computed } from 'vue'
import { Save, Image as ImageIcon, Video, LayoutPanelLeft, BarChart3, Minimize2, Plus, Trash2 } from 'lucide-vue-next'
import { AdminHomeAPI } from '@/api/admin'
import UIButton from '@/components/ui/UIButton.vue'
import MultilingualInput from '@/components/admin/MultilingualInput.vue'
import MediaPicker from '@/components/admin/MediaPicker.vue'
import { useToast } from '@/composables/useToast'

const toast = useToast()
const loading = ref(true)
const saving = ref(false)
const form = reactive({})

const variants = [
  { key: 'split',           label: 'Editorial split',     icon: LayoutPanelLeft, desc: 'Matn chap, foto o\'ng' },
  { key: 'fullbleed_photo', label: 'Full-bleed foto',     icon: ImageIcon,       desc: 'To\'liq ekran rasm' },
  { key: 'video_bg',        label: 'Video background',    icon: Video,           desc: 'Loop video orqada' },
  { key: 'stats',           label: 'Stats hero',          icon: BarChart3,       desc: 'Raqamlar bilan' },
  { key: 'minimal',         label: 'Minimal',             icon: Minimize2,       desc: 'Faqat matn + CTA' }
]

async function load() {
  loading.value = true
  try {
    const data = await AdminHomeAPI.hero.get()
    Object.assign(form, data)
  } finally {
    loading.value = false
  }
}
onMounted(load)

async function save() {
  saving.value = true
  try {
    // Send only updatable fields (skip server-managed ones)
    const { id, page, created_at, updated_at, ...payload } = form
    const updated = await AdminHomeAPI.hero.update(payload)
    Object.assign(form, updated)
    toast.success('Hero saqlandi')
  } catch (e) {
    toast.error(e?.response?.data?.detail || 'Saqlashda xatolik')
  } finally {
    saving.value = false
  }
}

const showSideImage = computed(() => form.variant === 'split')
const showBgImage   = computed(() => form.variant === 'fullbleed_photo' || form.variant === 'video_bg')
const showBgVideo   = computed(() => form.variant === 'video_bg')
const showQuote     = computed(() => form.variant === 'split')
</script>

<template>
  <div v-if="loading" class="text-center py-12 text-ink-faint text-sm">Yuklanmoqda...</div>

  <div v-else>
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-lg font-display font-bold text-ink-dark dark:text-white">Hero section</h2>
        <p class="text-xs text-ink-faint mt-0.5">Bosh sahifaning eng yuqori qismi — variant, matn, media va CTA</p>
      </div>
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>
        Saqlash
      </UIButton>
    </div>

    <!-- Enable toggle -->
    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5">
      <label class="flex items-center justify-between gap-3 cursor-pointer">
        <span>
          <span class="text-sm font-bold text-ink-dark dark:text-white">Hero ko'rsatilsin</span>
          <span class="block text-[12px] text-ink-faint mt-0.5">Agar o'chirilsa, sahifa darhol Quick Actions ribbon'idan boshlanadi</span>
        </span>
        <input type="checkbox" v-model="form.enabled" class="w-5 h-5 accent-accent-500" />
      </label>
    </div>

    <!-- Variant selector -->
    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint mb-3">Variant</p>
      <div class="grid sm:grid-cols-2 lg:grid-cols-5 gap-2">
        <button
          v-for="v in variants"
          :key="v.key"
          type="button"
          @click="form.variant = v.key"
          :class="[
            'group flex flex-col items-start text-left gap-2 px-4 py-3 rounded-xl border-2 transition-all',
            form.variant === v.key
              ? 'border-accent-500 bg-accent-50 dark:bg-accent-900/20'
              : 'border-surface-muted dark:border-slate-700 hover:border-primary-300'
          ]"
        >
          <div :class="['w-9 h-9 rounded-lg grid place-items-center',
                        form.variant === v.key ? 'bg-accent-500 text-white' : 'bg-surface-soft dark:bg-slate-700 text-primary-700']">
            <component :is="v.icon" class="w-4 h-4" />
          </div>
          <div>
            <p class="text-xs font-bold text-ink-dark dark:text-white">{{ v.label }}</p>
            <p class="text-[10px] text-ink-faint mt-0.5">{{ v.desc }}</p>
          </div>
        </button>
      </div>
    </div>

    <!-- Text content -->
    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Matn</p>
      <MultilingualInput v-model="form" base="eyebrow" label="Eyebrow (kichik label)" placeholder="O'zbekistonning yetakchi xususiy universiteti" />

      <div class="grid sm:grid-cols-3 gap-3">
        <MultilingualInput v-model="form" base="title"           label="Title (1-qism)" placeholder="Bilim," />
        <MultilingualInput v-model="form" base="title_highlight" label="Title (2 — sariq)" placeholder="innovatsiya" />
        <MultilingualInput v-model="form" base="title_tail"      label="Title (3-qism)" placeholder="va kelajak." />
      </div>

      <MultilingualInput v-model="form" base="subtitle" label="Subtitle" textarea :rows="3" />
    </div>

    <!-- Media -->
    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Media</p>

      <MediaPicker
        v-if="showSideImage"
        v-model="form.side_image"
        label="Yon rasm (split variant uchun)"
        hint="O'ng tomondagi katta foto"
      />

      <MediaPicker
        v-if="showBgImage"
        v-model="form.bg_image"
        label="Background rasm"
        hint="To'liq ekran rasm — full-bleed va video fallback uchun"
      />

      <MediaPicker
        v-if="showBgVideo"
        v-model="form.bg_video"
        label="Background video"
        accept="video/mp4,video/webm"
        previewType="video"
        hint=".mp4 yoki .webm, autoplay va loop"
      />

      <MediaPicker
        v-if="showBgVideo"
        v-model="form.bg_video_poster"
        label="Video poster (fallback rasm)"
      />

      <div v-if="showBgImage || showBgVideo">
        <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">
          Overlay opacity ({{ form.overlay_opacity }}%)
        </label>
        <input
          type="range"
          v-model.number="form.overlay_opacity"
          min="0"
          max="100"
          class="w-full accent-accent-500"
        />
      </div>
    </div>

    <!-- CTAs -->
    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Asosiy CTA tugma</p>
      <MultilingualInput v-model="form" base="cta_primary_label" label="Tugma matni" placeholder="Hujjat topshirish" />
      <div class="grid sm:grid-cols-[1fr_auto] gap-3 items-end">
        <div>
          <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">URL</label>
          <input
            type="text"
            v-model="form.cta_primary_url"
            placeholder="https://qabul.xiuedu.uz"
            class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:border-primary-500"
          />
        </div>
        <label class="flex items-center gap-2 h-10">
          <input type="checkbox" v-model="form.cta_primary_external" class="w-4 h-4 accent-accent-500" />
          <span class="text-sm">Tashqi link</span>
        </label>
      </div>

      <div class="border-t border-surface-muted dark:border-slate-700 pt-4">
        <p class="text-xs font-bold uppercase tracking-wider text-ink-faint mb-3">Qo'shimcha (sekundar) CTA</p>
        <MultilingualInput v-model="form" base="cta_secondary_label" label="Tugma matni" placeholder="Video tur" />
        <div class="grid sm:grid-cols-[1fr_auto] gap-3 items-end mt-3">
          <div>
            <label class="block text-sm font-medium text-ink-medium dark:text-slate-300 mb-1.5">URL</label>
            <input
              type="text"
              v-model="form.cta_secondary_url"
              placeholder="/about"
              class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:border-primary-500"
            />
          </div>
          <label class="flex items-center gap-2 h-10">
            <input type="checkbox" v-model="form.cta_secondary_external" class="w-4 h-4 accent-accent-500" />
            <span class="text-sm">Tashqi link</span>
          </label>
        </div>
      </div>
    </div>

    <!-- Quote (split variant only) -->
    <div v-if="showQuote" class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Sitata (foto ustida)</p>
      <MultilingualInput v-model="form" base="quote_text"   label="Sitata matni"   textarea :rows="2" />
      <MultilingualInput v-model="form" base="quote_author" label="Muallif"        placeholder="Madina K. — Bitiruvchi 2024" />
    </div>

    <!-- Floating badge cards -->
    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5 space-y-4">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Floating badge cardlar (foto ustida)</p>
      <p class="text-[11px] text-ink-faint">Split variantda foto yuqori-o'ng va pastki-chap burchakda ko'rinadigan kichik cardlar.</p>

      <div class="grid sm:grid-cols-2 gap-4 p-4 rounded-xl bg-surface-soft dark:bg-slate-900/30">
        <p class="sm:col-span-2 text-[11px] font-bold uppercase tracking-wider text-accent-600">Badge 1 (yuqori-o'ng)</p>
        <div>
          <label class="block text-sm font-medium text-ink-medium mb-1.5">Qiymat</label>
          <input type="text" v-model="form.badge1_value" placeholder="TOP-3"
                 class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
        </div>
        <div>
          <label class="block text-sm font-medium text-ink-medium mb-1.5">Icon (heroicon)</label>
          <input type="text" v-model="form.badge1_icon" placeholder="StarIcon"
                 class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
        </div>
        <div class="sm:col-span-2">
          <MultilingualInput v-model="form" base="badge1_label" label="Label" placeholder="O'zbekiston reytingida" />
        </div>
      </div>

      <div class="grid sm:grid-cols-2 gap-4 p-4 rounded-xl bg-surface-soft dark:bg-slate-900/30">
        <p class="sm:col-span-2 text-[11px] font-bold uppercase tracking-wider text-accent-600">Badge 2 (pastki-chap)</p>
        <div>
          <label class="block text-sm font-medium text-ink-medium mb-1.5">Qiymat</label>
          <input type="text" v-model="form.badge2_value" placeholder="95%"
                 class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
        </div>
        <div>
          <label class="block text-sm font-medium text-ink-medium mb-1.5">Icon (heroicon)</label>
          <input type="text" v-model="form.badge2_icon" placeholder="BriefcaseIcon"
                 class="w-full h-10 px-3 rounded-lg border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-sm" />
        </div>
        <div class="sm:col-span-2">
          <MultilingualInput v-model="form" base="badge2_label" label="Label" placeholder="Bitiruvchilar ish bilan" />
        </div>
      </div>
    </div>

    <!-- Trust badges strip -->
    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5">
      <div class="flex items-center justify-between mb-3">
        <div>
          <p class="text-xs font-bold uppercase tracking-wider text-ink-faint">Akkreditatsiya va sheriklar</p>
          <p class="text-[11px] text-ink-faint mt-0.5">CTA tugmalardan pastda ko'rinadigan kichik badge'lar</p>
        </div>
        <button type="button" class="text-[11px] font-bold text-primary-700 hover:text-accent-600"
                @click="if (!form.trust_badges) form.trust_badges = []; form.trust_badges.push({label:'', sub_uz:'', sub_ru:'', sub_en:'', icon:'ShieldCheckIcon'})">
          <Plus class="w-3 h-3 inline" /> Qo'shish
        </button>
      </div>
      <div v-if="!form.trust_badges?.length" class="text-xs text-ink-faint text-center py-4">Hozircha yo'q</div>
      <div v-else class="space-y-3">
        <div
          v-for="(b, i) in form.trust_badges"
          :key="i"
          class="grid grid-cols-[1fr_1fr_1fr_1fr_auto] gap-2 items-end p-3 rounded-xl bg-surface-soft dark:bg-slate-900/30"
        >
          <div>
            <label class="block text-[10px] uppercase tracking-wider text-ink-faint mb-1">Label</label>
            <input type="text" v-model="b.label" placeholder="Cambridge"
                   class="w-full h-9 px-2 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs" />
          </div>
          <div>
            <label class="block text-[10px] uppercase tracking-wider text-ink-faint mb-1">UZ</label>
            <input type="text" v-model="b.sub_uz" placeholder="English Partner"
                   class="w-full h-9 px-2 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs" />
          </div>
          <div>
            <label class="block text-[10px] uppercase tracking-wider text-ink-faint mb-1">RU</label>
            <input type="text" v-model="b.sub_ru" placeholder="Партнёр"
                   class="w-full h-9 px-2 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs" />
          </div>
          <div>
            <label class="block text-[10px] uppercase tracking-wider text-ink-faint mb-1">EN</label>
            <input type="text" v-model="b.sub_en" placeholder="Partner"
                   class="w-full h-9 px-2 rounded border border-surface-muted dark:border-slate-700 bg-white dark:bg-slate-900 text-xs" />
          </div>
          <button type="button" class="w-8 h-9 grid place-items-center rounded text-ink-faint hover:text-danger"
                  @click="form.trust_badges.splice(i, 1)">
            <Trash2 class="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>

    <!-- Decorative toggles -->
    <div class="rounded-2xl bg-white dark:bg-slate-800 border border-surface-muted dark:border-slate-700 p-5 mb-5">
      <p class="text-xs font-bold uppercase tracking-wider text-ink-faint mb-3">Dekorativ elementlar</p>
      <div class="grid sm:grid-cols-2 gap-3">
        <label class="flex items-center justify-between gap-2 px-4 py-3 rounded-lg border border-surface-muted dark:border-slate-700 cursor-pointer hover:bg-surface-soft">
          <span class="text-sm font-medium">Particles (zarrachalar)</span>
          <input type="checkbox" v-model="form.show_particles" class="w-4 h-4 accent-accent-500" />
        </label>
        <label class="flex items-center justify-between gap-2 px-4 py-3 rounded-lg border border-surface-muted dark:border-slate-700 cursor-pointer hover:bg-surface-soft">
          <span class="text-sm font-medium">Scroll indicator</span>
          <input type="checkbox" v-model="form.show_scroll_indicator" class="w-4 h-4 accent-accent-500" />
        </label>
        <label class="flex items-center justify-between gap-2 px-4 py-3 rounded-lg border border-surface-muted dark:border-slate-700 cursor-pointer hover:bg-surface-soft">
          <span class="text-sm font-medium">Trust badges</span>
          <input type="checkbox" v-model="form.show_trust_badges" class="w-4 h-4 accent-accent-500" />
        </label>
        <label class="flex items-center justify-between gap-2 px-4 py-3 rounded-lg border border-surface-muted dark:border-slate-700 cursor-pointer hover:bg-surface-soft">
          <span class="text-sm font-medium">Floating cards</span>
          <input type="checkbox" v-model="form.show_floating_cards" class="w-4 h-4 accent-accent-500" />
        </label>
      </div>
    </div>

    <!-- Bottom save -->
    <div class="flex justify-end">
      <UIButton variant="accent" :loading="saving" @click="save">
        <template #icon-left><Save class="w-4 h-4" /></template>
        Saqlash
      </UIButton>
    </div>
  </div>
</template>
