<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminHomeAPI } from '@/api/admin'

const fields = [
  { key: 'image',  label: 'Hujjat rasmi (A4)', type: 'media', hint: '210×297 mm proportsiyada' },
  { key: 'pdf',    label: 'PDF fayl (ixtiyoriy)', type: 'media', accept: 'application/pdf', previewType: 'file' },
  { key: 'title',  label: 'Hujjat nomi',  type: 'multilingual', required: true },
  { key: 'issuer', label: 'Bergan tashkilot', type: 'multilingual' },
  { key: 'year',   label: 'Yil',          type: 'number' },
  { key: 'enabled',    label: 'Faol',     type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib',   type: 'number' }
]
const columns = [
  { key: 'image',    label: 'Rasm' },
  { key: 'title_uz', label: 'Sarlavha' },
  { key: 'year',     label: 'Yil' },
  { key: 'enabled',  label: 'Holat' }
]
const defaultItem = {
  image: null, pdf: null,
  title_uz: '', title_ru: '', title_en: '',
  issuer_uz: '', issuer_ru: '', issuer_en: '',
  year: new Date().getFullYear(), enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Litsenziya va sertifikatlar"
    description="A4 formatdagi akkreditatsiya hujjatlari"
    :api="AdminHomeAPI.licenses"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
