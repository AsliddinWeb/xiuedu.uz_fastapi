<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminAboutAPI } from '@/api/admin'

const fields = [
  { key: 'code', label: 'Kod (qisqa)', type: 'text', placeholder: 'OTV', required: true },
  { key: 'icon', label: 'Icon (heroicon)', type: 'text', placeholder: 'ShieldCheckIcon' },
  { key: 'name', label: 'To\'liq nomi',    type: 'multilingual', required: true },
  { key: 'enabled', label: 'Faol', type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib', type: 'number' }
]
const columns = [
  { key: 'code',    label: 'Kod' },
  { key: 'name_uz', label: 'Nomi' },
  { key: 'icon',    label: 'Icon' },
  { key: 'enabled', label: 'Holat' }
]
const defaultItem = {
  code: '', icon: 'ShieldCheckIcon',
  name_uz: '', name_ru: '', name_en: '',
  enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Akkreditatsiya badge'lari"
    description="About sahifasidagi kichik sertifikat ro'yxati (License A4 hujjatlardan farqli)"
    :api="AdminAboutAPI.accreditations"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
