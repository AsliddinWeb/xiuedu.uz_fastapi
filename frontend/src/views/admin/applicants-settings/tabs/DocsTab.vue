<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminApplicantsAPI } from '@/api/admin'

const fields = [
  { key: 'title', label: 'Kategoriya nomi', type: 'multilingual', required: true, placeholder: "Bakalavr uchun hujjatlar" },
  { key: 'items', label: 'Hujjatlar ro\'yxati', type: 'multilingual-list', hint: "Har bir element accordion ichida bullet bo'lib chiqadi" },
  { key: 'enabled', label: 'Faol', type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib', type: 'number' }
]
const columns = [
  { key: 'title_uz', label: 'Kategoriya' },
  { key: 'enabled',  label: 'Holat' }
]
const defaultItem = {
  title_uz: '', title_ru: '', title_en: '',
  items: [],
  enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Hujjatlar (accordion)"
    description="Har bir kategoriya alohida accordion bo'lib ochiladi"
    :api="AdminApplicantsAPI.docs"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
