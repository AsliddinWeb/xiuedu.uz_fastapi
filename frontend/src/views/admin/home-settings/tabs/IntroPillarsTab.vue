<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminHomeAPI } from '@/api/admin'

const fields = [
  { key: 'icon',  label: 'Icon (heroicon nomi)', type: 'text', placeholder: 'ShieldCheckIcon' },
  { key: 'title', label: 'Sarlavha',  type: 'multilingual', required: true },
  { key: 'desc',  label: 'Tavsif',    type: 'multilingual-textarea', rows: 3 },
  { key: 'enabled',    label: 'Faol',   type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib', type: 'number' }
]
const columns = [
  { key: 'icon',     label: 'Icon' },
  { key: 'title_uz', label: 'Sarlavha' },
  { key: 'enabled',  label: 'Holat' }
]
const defaultItem = {
  icon: 'ShieldCheckIcon', title_uz: '', title_ru: '', title_en: '',
  desc_uz: '', desc_ru: '', desc_en: '', enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Intro pillarlar (3 ta card)"
    description="Universitet intro section'idagi 3 ta xususiyat card"
    :api="AdminHomeAPI.introPillars"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
