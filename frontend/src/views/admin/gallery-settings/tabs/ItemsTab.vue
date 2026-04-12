<script setup>
/**
 * Gallery items — CRUD with category_id select + image upload.
 * Loads categories dynamically for the select dropdown.
 */
import { ref, onMounted } from 'vue'
import CollectionEditor from '@/components/admin/CollectionEditor.vue'
import { AdminGalleryAPI } from '@/api/admin'

const catOptions = ref([])

onMounted(async () => {
  try {
    const cats = await AdminGalleryAPI.categories.list()
    catOptions.value = cats.map(c => ({ value: c.id, label: `${c.name_uz} (${c.slug})` }))
  } catch (_) {}
})

const fields = [
  { key: 'image',       label: 'Rasm', type: 'media', required: true },
  { key: 'category_id', label: 'Kategoriya', type: 'select', options: catOptions },
  { key: 'caption',     label: 'Caption (ixtiyoriy)', type: 'multilingual' },
  { key: 'alt',         label: 'Alt matn', type: 'multilingual', hint: 'Accessibility uchun' },
  { key: 'enabled',     label: 'Faol', type: 'checkbox' },
  { key: 'sort_order',  label: 'Tartib', type: 'number' }
]
const columns = [
  { key: 'image',      label: 'Rasm' },
  { key: 'caption_uz', label: 'Caption' },
  { key: 'category_id', label: 'Kat ID' },
  { key: 'enabled',    label: 'Holat' }
]
const defaultItem = {
  image: '', category_id: null,
  caption_uz: '', caption_ru: '', caption_en: '',
  alt_uz: '', alt_ru: '', alt_en: '',
  enabled: true, sort_order: 0
}
</script>

<template>
  <CollectionEditor
    title="Galereya rasmlari"
    description="Rasmlarni yuklang va kategoriyaga biriktiring"
    :api="AdminGalleryAPI.items"
    :fields="fields"
    :list-columns="columns"
    :default-item="defaultItem"
    empty-text="Hozircha rasm yo'q — rasmlar qo'shish uchun Media tab'dan avval yuklang"
  />
</template>
