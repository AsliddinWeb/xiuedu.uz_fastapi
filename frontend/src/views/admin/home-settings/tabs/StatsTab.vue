<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminHomeAPI } from '@/api/admin'

const fields = [
  { key: 'value', label: 'Qiymat',    type: 'text', placeholder: '5,000+' },
  { key: 'label', label: 'Label',     type: 'multilingual', required: true },
  { key: 'sub',   label: 'Pastki matn', type: 'multilingual' },
  { key: 'enabled', label: 'Faol',    type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib', type: 'number' }
]
const columns = [
  { key: 'value',    label: 'Qiymat' },
  { key: 'label_uz', label: 'Label' },
  { key: 'enabled',  label: 'Holat' }
]
const defaultItem = {
  value: '0', label_uz: '', label_ru: '', label_en: '',
  sub_uz: '', sub_ru: '', sub_en: '', enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Raqamlar (Numbers in Context)"
    description="4 ta katta raqam — talabalar, bitiruvchilar, ish bilan ta'minlanganlik va h.k."
    :api="AdminHomeAPI.stats"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
