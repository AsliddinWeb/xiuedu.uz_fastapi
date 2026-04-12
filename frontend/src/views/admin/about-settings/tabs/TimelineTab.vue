<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminAboutAPI } from '@/api/admin'

const fields = [
  { key: 'year',  label: 'Yil',     type: 'text', placeholder: '2009', required: true },
  { key: 'title', label: 'Sarlavha', type: 'multilingual', required: true },
  { key: 'text',  label: 'Tavsif',   type: 'multilingual-textarea', rows: 3 },
  { key: 'enabled', label: 'Faol',   type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib', type: 'number' }
]
const columns = [
  { key: 'year',     label: 'Yil' },
  { key: 'title_uz', label: 'Sarlavha' },
  { key: 'enabled',  label: 'Holat' }
]
const defaultItem = {
  year: '', title_uz: '', title_ru: '', title_en: '',
  text_uz: '', text_ru: '', text_en: '',
  enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Tarix (timeline)"
    description="Universitet tarixidagi muhim sanalar"
    :api="AdminAboutAPI.timeline"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
