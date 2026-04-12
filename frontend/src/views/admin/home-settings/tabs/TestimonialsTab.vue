<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminHomeAPI } from '@/api/admin'

const fields = [
  { key: 'avatar', label: 'Avatar rasmi', type: 'media' },
  { key: 'name',   label: 'Ism-familiya', type: 'multilingual', required: true },
  { key: 'role',   label: 'Rol / fakultet', type: 'multilingual', placeholder: 'Filologiya, 2024' },
  { key: 'text',   label: 'Sharh matni',  type: 'multilingual-textarea', rows: 4, required: true },
  { key: 'rating', label: 'Reyting (1-5)', type: 'number' },
  { key: 'year',   label: 'Yil',          type: 'number' },
  { key: 'enabled',    label: 'Faol',     type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib',   type: 'number' }
]
const columns = [
  { key: 'avatar',  label: 'Foto' },
  { key: 'name_uz', label: 'Ism' },
  { key: 'role_uz', label: 'Rol' },
  { key: 'enabled', label: 'Holat' }
]
const defaultItem = {
  avatar: null, name_uz: '', name_ru: '', name_en: '',
  role_uz: '', role_ru: '', role_en: '',
  text_uz: '', text_ru: '', text_en: '',
  rating: 5, year: null, enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Talabalar sharhlari"
    description="Bitiruvchilarning fikrlari — Testimonials section"
    :api="AdminHomeAPI.testimonials"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
