<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminApplicantsAPI } from '@/api/admin'

const fields = [
  { key: 'title',    label: 'Sarlavha (kunduzgi/sirtqi)', type: 'multilingual', required: true },
  { key: 'desc',     label: 'Tavsif', type: 'multilingual-textarea', rows: 3 },
  { key: 'features', label: 'Xususiyatlar (ro\'yxat)', type: 'multilingual-list', hint: '"4 yil", "Stipendiya" kabi qisqa fakts' },
  { key: 'cta_label', label: 'CTA tugma matni', type: 'multilingual' },
  { key: 'cta_url',   label: 'CTA URL', type: 'text', placeholder: '/education/bachelor' },
  { key: 'enabled', label: 'Faol', type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib', type: 'number' }
]
const columns = [
  { key: 'title_uz', label: 'Sarlavha' },
  { key: 'cta_url',  label: 'URL' },
  { key: 'enabled',  label: 'Holat' }
]
const defaultItem = {
  title_uz: '', title_ru: '', title_en: '',
  desc_uz: '', desc_ru: '', desc_en: '',
  features: [],
  cta_label_uz: 'Batafsil', cta_label_ru: 'Подробнее', cta_label_en: 'Learn more',
  cta_url: '',
  enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Ta'lim shakllari"
    description="Kunduzgi, sirtqi, kechki va boshqa shakllar — har biri xususiyat ro'yxati bilan"
    :api="AdminApplicantsAPI.forms"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
