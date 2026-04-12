<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminStructureAPI } from '@/api/admin'

const fields = [
  { key: 'icon', label: 'Icon (heroicon)', type: 'text', placeholder: 'BookOpenIcon' },
  { key: 'name', label: "Bo'lim nomi", type: 'multilingual', required: true },
  { key: 'head', label: 'Rahbar (ixtiyoriy)', type: 'multilingual' },
  { key: 'email', label: 'Email', type: 'text' },
  { key: 'phone', label: 'Telefon', type: 'text' },
  { key: 'enabled', label: 'Faol', type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib', type: 'number' }
]
const columns = [
  { key: 'icon',    label: 'Icon' },
  { key: 'name_uz', label: 'Nomi' },
  { key: 'head_uz', label: 'Rahbar' },
  { key: 'enabled', label: 'Holat' }
]
const defaultItem = {
  icon: 'BuildingOffice2Icon',
  name_uz: '', name_ru: '', name_en: '',
  head_uz: null, head_ru: null, head_en: null,
  email: null, phone: null,
  enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Ma'muriy bo'limlar"
    description="Universitet faoliyatini ta'minlovchi bo'limlar (kompakt tile grid)"
    :api="AdminStructureAPI.departments"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
