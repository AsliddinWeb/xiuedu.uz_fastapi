<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminHomeAPI } from '@/api/admin'

const fields = [
  { key: 'icon',       label: 'Icon (heroicon)',          type: 'text', placeholder: 'GlobeAltIcon' },
  { key: 'icon_bg',    label: 'Icon background CSS',      type: 'text', placeholder: 'bg-primary-50', hint: 'Tailwind class' },
  { key: 'icon_color', label: 'Icon rang CSS',            type: 'text', placeholder: 'text-primary-700' },
  { key: 'number',     label: 'Katta raqam',              type: 'text', placeholder: '50+' },
  { key: 'number_label', label: "Raqam label (kichik)",   type: 'multilingual' },
  { key: 'title',      label: 'Sarlavha',                 type: 'multilingual', required: true },
  { key: 'desc',       label: 'Tavsif',                   type: 'multilingual-textarea', rows: 3 },
  { key: 'enabled',    label: 'Faol',                     type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib',                   type: 'number' }
]
const columns = [
  { key: 'icon',     label: 'Icon' },
  { key: 'number',   label: 'Raqam' },
  { key: 'title_uz', label: 'Sarlavha' },
  { key: 'enabled',  label: 'Holat' }
]
const defaultItem = {
  icon: 'GlobeAltIcon', icon_bg: 'bg-primary-50', icon_color: 'text-primary-700',
  number: '', number_label_uz: '', number_label_ru: '', number_label_en: '',
  title_uz: '', title_ru: '', title_en: '',
  desc_uz: '', desc_ru: '', desc_en: '', enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Why XIU cardlari (4 ta)"
    description="Universitet afzalliklarini ko'rsatuvchi katta cardlar"
    :api="AdminHomeAPI.whyCards"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
