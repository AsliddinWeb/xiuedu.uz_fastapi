<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminIntlAPI } from '@/api/admin'

const fields = [
  { key: 'icon',  label: 'Icon (heroicon)', type: 'text', placeholder: 'PaperAirplaneIcon' },
  { key: 'title', label: 'Sarlavha',  type: 'multilingual', required: true },
  { key: 'desc',  label: 'Tavsif',    type: 'multilingual-textarea', rows: 3 },
  { key: 'enabled',    label: 'Faol', type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib', type: 'number' }
]
const columns = [
  { key: 'icon',     label: 'Icon' },
  { key: 'title_uz', label: 'Sarlavha' },
  { key: 'enabled',  label: 'Holat' }
]
const defaultItem = {
  icon: 'PaperAirplaneIcon',
  title_uz: '', title_ru: '', title_en: '',
  desc_uz: '', desc_ru: '', desc_en: '',
  enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Xalqaro dasturlar"
    description="Almashinuv, dual diploma, stajirovka, qo'shma tadqiqot va boshqalar"
    :api="AdminIntlAPI.programs"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
