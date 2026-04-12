<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminHomeAPI } from '@/api/admin'

const fields = [
  { key: 'number', label: 'Raqam',     type: 'text', placeholder: '01' },
  { key: 'icon',   label: 'Icon',      type: 'text', placeholder: 'DocumentTextIcon' },
  { key: 'title',  label: 'Sarlavha',  type: 'multilingual', required: true },
  { key: 'desc',   label: 'Tavsif',    type: 'multilingual-textarea' },
  { key: 'enabled', label: 'Faol',     type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib', type: 'number' }
]
const columns = [
  { key: 'number',   label: '#' },
  { key: 'icon',     label: 'Icon' },
  { key: 'title_uz', label: 'Sarlavha' },
  { key: 'enabled',  label: 'Holat' }
]
const defaultItem = {
  number: '01', icon: 'DocumentTextIcon',
  title_uz: '', title_ru: '', title_en: '',
  desc_uz: '', desc_ru: '', desc_en: '', enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Qabul jarayoni (4 qadam)"
    description="Hujjat topshirishdan o'qishni boshlashgacha bo'lgan qadamlar"
    :api="AdminHomeAPI.admissionSteps"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
