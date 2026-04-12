<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminStructureAPI } from '@/api/admin'

const fields = [
  { key: 'icon', label: 'Icon (heroicon)', type: 'text', placeholder: 'BuildingLibraryIcon' },
  { key: 'name', label: 'Xizmat nomi', type: 'multilingual', required: true },
  { key: 'desc', label: 'Tavsif', type: 'multilingual-textarea', rows: 3 },
  { key: 'enabled', label: 'Faol', type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib', type: 'number' }
]
const columns = [
  { key: 'icon',    label: 'Icon' },
  { key: 'name_uz', label: 'Nomi' },
  { key: 'enabled', label: 'Holat' }
]
const defaultItem = {
  icon: 'BuildingLibraryIcon',
  name_uz: '', name_ru: '', name_en: '',
  desc_uz: '', desc_ru: '', desc_en: '',
  enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Yordamchi xizmatlar"
    description="Kutubxona, til markazi, karyera markazi va boshqalar"
    :api="AdminStructureAPI.services"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
