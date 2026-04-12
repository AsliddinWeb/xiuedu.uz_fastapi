<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminGalleryAPI } from '@/api/admin'

const fields = [
  { key: 'slug', label: 'Slug (URL)', type: 'text', required: true, placeholder: 'event' },
  { key: 'name', label: 'Nomi', type: 'multilingual', required: true },
  { key: 'enabled', label: 'Faol', type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib', type: 'number' }
]
const columns = [
  { key: 'slug',    label: 'Slug' },
  { key: 'name_uz', label: 'Nomi' },
  { key: 'enabled', label: 'Holat' }
]
const defaultItem = {
  slug: '', name_uz: '', name_ru: '', name_en: '',
  enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Galereya kategoriyalari"
    description="Rasmlar guruhi — event, student, sport, campus va h.k."
    :api="AdminGalleryAPI.categories"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
