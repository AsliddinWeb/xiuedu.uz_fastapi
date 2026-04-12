<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminApplicantsAPI } from '@/api/admin'

const fields = [
  { key: 'month', label: 'Oy nomi', type: 'multilingual', required: true, placeholder: 'Iyun' },
  { key: 'text',  label: 'Tavsif', type: 'multilingual', placeholder: 'Onlayn ariza qabuli boshlanadi' },
  { key: 'enabled', label: 'Faol', type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib', type: 'number' }
]
const columns = [
  { key: 'month_uz', label: 'Oy' },
  { key: 'text_uz',  label: 'Tavsif' },
  { key: 'enabled',  label: 'Holat' }
]
const defaultItem = {
  month_uz: '', month_ru: '', month_en: '',
  text_uz: '', text_ru: '', text_en: '',
  enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Qabul muddatlari"
    description="Iyun → Sentabr ketma-ketligi"
    :api="AdminApplicantsAPI.timeline"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
