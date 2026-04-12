<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminApplicantsAPI } from '@/api/admin'

const fields = [
  { key: 'question', label: 'Savol', type: 'multilingual', required: true },
  { key: 'answer',   label: 'Javob', type: 'multilingual-textarea', rows: 4, required: true },
  { key: 'enabled', label: 'Faol', type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib', type: 'number' }
]
const columns = [
  { key: 'question_uz', label: 'Savol' },
  { key: 'enabled',     label: 'Holat' }
]
const defaultItem = {
  question_uz: '', question_ru: '', question_en: '',
  answer_uz: '', answer_ru: '', answer_en: '',
  enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="FAQ — Savol va javoblar"
    :api="AdminApplicantsAPI.faqs"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
  />
</template>
