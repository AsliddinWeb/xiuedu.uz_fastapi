<script setup>
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminLeadersAPI } from '@/api/admin'

const fields = [
  { key: 'photo',    label: 'Foto',           type: 'media' },
  { key: 'group',    label: 'Guruh',          type: 'select', options: [
      { value: 'rector',          label: 'Rektor' },
      { value: 'prorector',       label: 'Prorektor' },
      { value: 'dean',            label: 'Dekan' },
      { value: 'department_head', label: 'Kafedra mudiri' }
    ]
  },
  { key: 'name',     label: 'Ism-familiya',   type: 'multilingual', required: true },
  { key: 'position', label: 'Lavozim',        type: 'multilingual' },
  { key: 'degree',   label: 'Ilmiy daraja',   type: 'multilingual', placeholder: 'Pedagogika fanlari doktori' },
  { key: 'bio',      label: 'Biografiya',     type: 'multilingual-textarea', rows: 4 },
  { key: 'email',    label: 'Email',          type: 'text' },
  { key: 'phone',    label: 'Telefon',        type: 'text', placeholder: '+998 71 200 00 00' },
  { key: 'enabled',    label: 'Faol',         type: 'checkbox' },
  { key: 'sort_order', label: 'Tartib',       type: 'number' }
]

const columns = [
  { key: 'photo',   label: 'Foto' },
  { key: 'name_uz', label: 'Ism' },
  { key: 'group',   label: 'Guruh', render: (r) => ({
      rector: 'Rektor', prorector: 'Prorektor', dean: 'Dekan', department_head: 'Kafedra mudiri'
    }[r.group] || r.group)
  },
  { key: 'position_uz', label: 'Lavozim' },
  { key: 'enabled', label: 'Holat' }
]

const defaultItem = {
  photo: null, group: 'department_head',
  name_uz: '', name_ru: '', name_en: '',
  position_uz: '', position_ru: '', position_en: '',
  degree_uz: '', degree_ru: '', degree_en: '',
  bio_uz: '', bio_ru: '', bio_en: '',
  email: null, phone: null,
  enabled: true, sort_order: 0
}
</script>

<template>
  <div>
    <div class="mb-6">
      <h1 class="text-xl font-display font-bold text-ink-dark dark:text-white">Rahbariyat</h1>
      <p class="text-sm text-ink-faint mt-0.5">Rektor, prorektorlar, dekanlar va kafedra mudirlari</p>
    </div>

    <CollectionEditor
      title="Rahbariyat ro'yxati"
      description="Public /leadership sahifasida ko'rsatiladi. Tartib bilan saralanadi."
      :api="AdminLeadersAPI"
      :fields="fields"
      :list-columns="columns"
      :default-item="defaultItem"
      empty-text="Hozircha rahbar yo'q"
    />
  </div>
</template>
