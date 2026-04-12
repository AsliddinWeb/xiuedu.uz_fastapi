<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminIntlAPI } from '@/api/admin'

const fields = [
  { key: 'name',         label: 'Universitet nomi', type: 'text', required: true, placeholder: 'Cambridge English' },
  { key: 'country_code', label: 'Mamlakat kodi (ISO)', type: 'text', placeholder: 'GB' },
  { key: 'flag',         label: 'Flag emoji', type: 'text', placeholder: '🇬🇧' },
  { key: 'logo_url',     label: 'Logo (ixtiyoriy)', type: 'media' },
  { key: 'url',          label: 'Tashqi URL (ixtiyoriy)', type: 'text' },
  { key: 'enabled',      label: 'Faol', type: 'checkbox' },
  { key: 'sort_order',   label: 'Tartib', type: 'number' }
]
const columns = [
  { key: 'flag',         label: 'Flag' },
  { key: 'name',         label: 'Universitet' },
  { key: 'country_code', label: 'Mamlakat' },
  { key: 'enabled',      label: 'Holat' }
]
const defaultItem = {
  name: '', country_code: '', flag: '',
  logo_url: null, url: null,
  enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Hamkor universitetlar"
    description="Aniq universitet ismlari (mamlakat ro'yxati Bosh sahifa → Hamkorlar tabida alohida)"
    :api="AdminIntlAPI.partners"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
