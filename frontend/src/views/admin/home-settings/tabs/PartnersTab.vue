<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminHomeAPI } from '@/api/admin'

const fields = [
  { key: 'flag',     label: 'Flag emoji', type: 'text', placeholder: '🇬🇧' },
  { key: 'country',  label: 'Mamlakat',   type: 'multilingual', required: true },
  { key: 'count',    label: 'Hamkor soni', type: 'number' },
  { key: 'logo_url', label: 'Logo (ixtiyoriy)', type: 'media' },
  { key: 'url',      label: 'Tashqi URL (ixtiyoriy)', type: 'text' },
  { key: 'enabled',    label: 'Faol',     type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib',   type: 'number' }
]
const columns = [
  { key: 'flag',       label: 'Flag' },
  { key: 'country_uz', label: 'Mamlakat' },
  { key: 'count',      label: 'Soni' },
  { key: 'enabled',    label: 'Holat' }
]
const defaultItem = {
  flag: '', country_uz: '', country_ru: '', country_en: '',
  count: 1, logo_url: null, url: null, enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Xalqaro hamkorlar"
    description="Mamlakatlar bo'yicha hamkor universitetlar ro'yxati"
    :api="AdminHomeAPI.partners"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
