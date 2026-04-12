<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminVacanciesAPI } from '@/api/admin'

const fields = [
  { key: 'is_open',  label: 'Ochiq vakansiya', type: 'checkbox', hint: 'Ochiq emas bo\'lsa public sahifada "yopilgan" badge bilan ko\'rinadi' },
  { key: 'title',    label: 'Lavozim nomi', type: 'multilingual', required: true },
  { key: 'department', label: "Bo'lim / fakultet", type: 'multilingual' },
  { key: 'employment_type', label: 'Bandlik turi', type: 'select', options: [
      { value: 'full_time',  label: 'Kunduzgi (Full-time)' },
      { value: 'part_time',  label: 'Yarim stavka (Part-time)' },
      { value: 'contract',   label: 'Kontrakt' },
      { value: 'internship', label: 'Stajirovka' },
      { value: 'online',     label: 'Onlayn' }
    ]
  },
  { key: 'location', label: 'Joylashuv', type: 'multilingual', placeholder: 'Toshkent' },
  { key: 'description',  label: 'Tavsif', type: 'multilingual-textarea', rows: 4 },
  { key: 'requirements', label: 'Talablar', type: 'multilingual-textarea', rows: 4, hint: 'Har bir talab yangi qatorda. Markdown bullet ishlatish mumkin.' },
  { key: 'salary',        label: 'Maosh (ixtiyoriy)', type: 'text', placeholder: '8-12 mln so\'m' },
  { key: 'contact_email', label: 'Aloqa email', type: 'text', placeholder: 'hr@xiuedu.uz' },
  { key: 'apply_url',     label: 'Tashqi ariza URL (ixtiyoriy)', type: 'text' },
  { key: 'posted_at', label: 'E\'lon qilingan sana', type: 'date' },
  { key: 'deadline',  label: 'Oxirgi muddat',       type: 'date' },
  { key: 'enabled',    label: 'Faol (publish)', type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib', type: 'number' }
]

const columns = [
  { key: 'title_uz',      label: 'Lavozim' },
  { key: 'department_uz', label: "Bo'lim" },
  { key: 'is_open',       label: 'Ochiq', render: r => r.is_open ? 'Ha' : "Yo'q" },
  { key: 'enabled',       label: 'Holat' }
]

const defaultItem = {
  is_open: true,
  title_uz: '', title_ru: '', title_en: '',
  department_uz: '', department_ru: '', department_en: '',
  employment_type: 'full_time',
  location_uz: '', location_ru: '', location_en: '',
  description_uz: '', description_ru: '', description_en: '',
  requirements_uz: '', requirements_ru: '', requirements_en: '',
  salary: null, contact_email: 'hr@xiuedu.uz', apply_url: null,
  posted_at: new Date().toISOString().slice(0, 10),
  deadline: null,
  enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Vakansiyalar"
    description="Universitetning bo'sh ish o'rinlari ro'yxati"
    :api="AdminVacanciesAPI"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
    empty-text="Hozircha vakansiya yo'q"
  />
</template>
