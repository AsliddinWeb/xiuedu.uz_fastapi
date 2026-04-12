<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminHomeAPI } from '@/api/admin'

const fields = [
  { key: 'icon',     label: 'Icon (heroicon nomi)',  type: 'text', placeholder: 'BookOpenIcon', hint: 'masalan: ArrowUpRightIcon, BookOpenIcon, UserCircleIcon' },
  { key: 'title',    label: 'Sarlavha',              type: 'multilingual', required: true },
  { key: 'desc',     label: 'Tavsif',                type: 'multilingual' },
  { key: 'url',      label: 'URL',                   type: 'text', placeholder: '/faculties yoki https://...' },
  { key: 'external', label: 'Tashqi havola',         type: 'checkbox', hint: 'Yangi tab da ochiladi' },
  { key: 'accent',   label: 'Asosiy (sariq) variant',type: 'checkbox' },
  { key: 'enabled',  label: 'Faol',                  type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib',              type: 'number' }
]

const columns = [
  { key: 'icon',  label: 'Icon' },
  { key: 'title_uz', label: 'Sarlavha' },
  { key: 'url',   label: 'URL' },
  { key: 'enabled', label: 'Holat' }
]

const defaultItem = {
  icon: 'BookOpenIcon', title_uz: '', title_ru: '', title_en: '',
  desc_uz: '', desc_ru: '', desc_en: '',
  url: '', external: false, accent: false, enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Hero ostidagi tezkor tugmalar"
    description="4 ta tugma — Hero section ostida ribbon shaklida ko'rinadi"
    :api="AdminHomeAPI.quickActions"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
