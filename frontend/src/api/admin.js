import api from './client'

// ===== Pages =====
export const AdminPagesAPI = {
  list:   () => api.get('/admin/pages/').then(r => r.data),
  get:    (id) => api.get(`/admin/pages/${id}`).then(r => r.data),
  create: (data) => api.post('/admin/pages/', data).then(r => r.data),
  update: (id, data) => api.put(`/admin/pages/${id}`, data).then(r => r.data),
  remove: (id) => api.delete(`/admin/pages/${id}`),
  publish: (id, publish = true) => api.patch(`/admin/pages/${id}/publish`, null, { params: { publish } }).then(r => r.data)
}

// ===== News =====
export const AdminNewsAPI = {
  list:   (params = {}) => api.get('/admin/news/', { params }).then(r => r.data),
  stats:  () => api.get('/admin/news/stats').then(r => r.data),
  create: (data) => api.post('/admin/news/', data).then(r => r.data),
  update: (id, data) => api.put(`/admin/news/${id}`, data).then(r => r.data),
  remove: (id) => api.delete(`/admin/news/${id}`),
  publish: (id, publish = true) => api.patch(`/admin/news/${id}/publish`, null, { params: { publish } }).then(r => r.data),
  categories: () => api.get('/admin/news/categories/').then(r => r.data),
  createCategory: (data) => api.post('/admin/news/categories/', data).then(r => r.data),
  updateCategory: (id, data) => api.put(`/admin/news/categories/${id}`, data).then(r => r.data),
  removeCategory: (id) => api.delete(`/admin/news/categories/${id}`)
}

// ===== Events =====
export const AdminEventsAPI = {
  list:   (params = {}) => api.get('/admin/events/', { params }).then(r => r.data),
  get:    (id) => api.get(`/admin/events/${id}`).then(r => r.data).catch(() => null),
  create: (data) => api.post('/admin/events/', data).then(r => r.data),
  update: (id, data) => api.put(`/admin/events/${id}`, data).then(r => r.data),
  remove: (id) => api.delete(`/admin/events/${id}`)
}

// ===== About page CMS =====
export const AdminAboutAPI = {
  page: {
    get:    () => api.get('/admin/about/page').then(r => r.data),
    update: (data) => api.put('/admin/about/page', data).then(r => r.data)
  },
  timeline: {
    list:   () => api.get('/admin/about/timeline').then(r => r.data),
    create: (data) => api.post('/admin/about/timeline', data).then(r => r.data),
    update: (id, data) => api.put(`/admin/about/timeline/${id}`, data).then(r => r.data),
    remove: (id) => api.delete(`/admin/about/timeline/${id}`)
  },
  accreditations: {
    list:   () => api.get('/admin/about/accreditations').then(r => r.data),
    create: (data) => api.post('/admin/about/accreditations', data).then(r => r.data),
    update: (id, data) => api.put(`/admin/about/accreditations/${id}`, data).then(r => r.data),
    remove: (id) => api.delete(`/admin/about/accreditations/${id}`)
  }
}

// ===== Applicants page CMS =====
function makeAppCRUD(base) {
  return {
    list:   ()         => api.get(`/admin/applicants/${base}`).then(r => r.data),
    create: (data)     => api.post(`/admin/applicants/${base}`, data).then(r => r.data),
    update: (id, data) => api.put(`/admin/applicants/${base}/${id}`, data).then(r => r.data),
    remove: (id)       => api.delete(`/admin/applicants/${base}/${id}`)
  }
}

export const AdminApplicantsAPI = {
  page: {
    get:    () => api.get('/admin/applicants/page').then(r => r.data),
    update: (data) => api.put('/admin/applicants/page', data).then(r => r.data)
  },
  steps:    makeAppCRUD('steps'),
  forms:    makeAppCRUD('forms'),
  timeline: makeAppCRUD('timeline'),
  docs:     makeAppCRUD('docs'),
  faqs:     makeAppCRUD('faqs')
}

// ===== Structure page CMS =====
function makeStructCRUD(base) {
  return {
    list:   ()         => api.get(`/admin/structure/${base}`).then(r => r.data),
    create: (data)     => api.post(`/admin/structure/${base}`, data).then(r => r.data),
    update: (id, data) => api.put(`/admin/structure/${base}/${id}`, data).then(r => r.data),
    remove: (id)       => api.delete(`/admin/structure/${base}/${id}`)
  }
}

export const AdminStructureAPI = {
  page: {
    get:    () => api.get('/admin/structure/page').then(r => r.data),
    update: (data) => api.put('/admin/structure/page', data).then(r => r.data)
  },
  departments: makeStructCRUD('departments'),
  services:    makeStructCRUD('services')
}

// ===== International page CMS =====
function makeIntlCRUD(base) {
  return {
    list:   ()         => api.get(`/admin/international/${base}`).then(r => r.data),
    create: (data)     => api.post(`/admin/international/${base}`, data).then(r => r.data),
    update: (id, data) => api.put(`/admin/international/${base}/${id}`, data).then(r => r.data),
    remove: (id)       => api.delete(`/admin/international/${base}/${id}`)
  }
}

export const AdminIntlAPI = {
  page: {
    get:    () => api.get('/admin/international/page').then(r => r.data),
    update: (data) => api.put('/admin/international/page', data).then(r => r.data)
  },
  programs: makeIntlCRUD('programs'),
  partners: makeIntlCRUD('partners')
}

// ===== Gallery CMS =====
export const AdminGalleryAPI = {
  page: {
    get:    () => api.get('/admin/gallery/page').then(r => r.data),
    update: (data) => api.put('/admin/gallery/page', data).then(r => r.data)
  },
  categories: {
    list:   ()         => api.get('/admin/gallery/categories').then(r => r.data),
    create: (data)     => api.post('/admin/gallery/categories', data).then(r => r.data),
    update: (id, data) => api.put(`/admin/gallery/categories/${id}`, data).then(r => r.data),
    remove: (id)       => api.delete(`/admin/gallery/categories/${id}`)
  },
  items: {
    list:   ()         => api.get('/admin/gallery/items').then(r => r.data),
    create: (data)     => api.post('/admin/gallery/items', data).then(r => r.data),
    update: (id, data) => api.put(`/admin/gallery/items/${id}`, data).then(r => r.data),
    remove: (id)       => api.delete(`/admin/gallery/items/${id}`)
  }
}

// ===== Contact page CMS =====
export const AdminContactPageAPI = {
  get:    () => api.get('/admin/contact/page').then(r => r.data),
  update: (data) => api.put('/admin/contact/page', data).then(r => r.data)
}

// ===== Vacancies CMS =====
export const AdminVacanciesAPI = {
  page: {
    get:    () => api.get('/admin/vacancies/page').then(r => r.data),
    update: (data) => api.put('/admin/vacancies/page', data).then(r => r.data)
  },
  list:   ()         => api.get('/admin/vacancies/').then(r => r.data),
  create: (data)     => api.post('/admin/vacancies/', data).then(r => r.data),
  update: (id, data) => api.put(`/admin/vacancies/${id}`, data).then(r => r.data),
  remove: (id)       => api.delete(`/admin/vacancies/${id}`)
}

// ===== Leaders (separate from home settings) =====
export const AdminLeadersAPI = {
  list:   ()         => api.get('/admin/leaders/').then(r => r.data),
  get:    (id)       => api.get(`/admin/leaders/${id}`).then(r => r.data),
  create: (data)     => api.post('/admin/leaders/', data).then(r => r.data),
  update: (id, data) => api.put(`/admin/leaders/${id}`, data).then(r => r.data),
  remove: (id)       => api.delete(`/admin/leaders/${id}`)
}

// ===== Profile (current user) =====
export const ProfileAPI = {
  me:             () => api.get('/auth/me').then(r => r.data),
  update:         (data) => api.patch('/auth/me', data).then(r => r.data),
  changePassword: (data) => api.post('/auth/me/password', data).then(r => r.data)
}

// ===== Home page CMS =====
//
// Singletons use GET/PUT; collections use full CRUD.
// All endpoints require admin or content_manager role.
//
function makeCRUD(base) {
  return {
    list:   ()         => api.get(`/admin/home/${base}`).then(r => r.data),
    create: (data)     => api.post(`/admin/home/${base}`, data).then(r => r.data),
    update: (id, data) => api.put(`/admin/home/${base}/${id}`, data).then(r => r.data),
    remove: (id)       => api.delete(`/admin/home/${base}/${id}`)
  }
}

export const AdminHomeAPI = {
  // Singletons
  hero: {
    get:    () => api.get('/admin/home/hero').then(r => r.data),
    update: (data) => api.put('/admin/home/hero', data).then(r => r.data)
  },
  campus: {
    get:    () => api.get('/admin/home/campus').then(r => r.data),
    update: (data) => api.put('/admin/home/campus', data).then(r => r.data)
  },
  finalCta: {
    get:    () => api.get('/admin/home/final-cta').then(r => r.data),
    update: (data) => api.put('/admin/home/final-cta', data).then(r => r.data)
  },

  // Sections (no add/delete, only update by key)
  sections: {
    list:   () => api.get('/admin/home/sections').then(r => r.data),
    update: (key, data) => api.put(`/admin/home/sections/${key}`, data).then(r => r.data)
  },

  // Collections (factory-driven CRUD)
  quickActions:   makeCRUD('quick-actions'),
  introPillars:   makeCRUD('intro-pillars'),
  whyCards:       makeCRUD('why-cards'),
  admissionSteps: makeCRUD('admission-steps'),
  stats:          makeCRUD('stats'),
  testimonials:   makeCRUD('testimonials'),
  partners:       makeCRUD('partners'),
  licenses:       makeCRUD('licenses'),
  faqs:           makeCRUD('faqs'),

  // Faculties (nested programs — custom paths)
  faculties: {
    list:   ()         => api.get('/admin/home/faculties').then(r => r.data),
    get:    (id)       => api.get(`/admin/home/faculties/${id}`).then(r => r.data),
    create: (data)     => api.post('/admin/home/faculties', data).then(r => r.data),
    update: (id, data) => api.put(`/admin/home/faculties/${id}`, data).then(r => r.data),
    remove: (id)       => api.delete(`/admin/home/faculties/${id}`)
  },
  programs: {
    create: (facultyId, data) => api.post(`/admin/home/faculties/${facultyId}/programs`, data).then(r => r.data),
    update: (id, data)        => api.put(`/admin/home/programs/${id}`, data).then(r => r.data),
    remove: (id)              => api.delete(`/admin/home/programs/${id}`)
  }
}

// ===== Media =====
export const AdminMediaAPI = {
  list: (params = {}) => api.get('/admin/media/', { params }).then(r => r.data),
  upload: (file) => {
    const fd = new FormData()
    fd.append('file', file)
    return api.post('/admin/media/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } }).then(r => r.data)
  },
  remove: (id) => api.delete(`/admin/media/${id}`),
  updateAlt: (id, data) => api.patch(`/admin/media/${id}/alt`, data).then(r => r.data)
}

// ===== Users =====
export const AdminUsersAPI = {
  list:   () => api.get('/admin/users/').then(r => r.data),
  create: (data) => api.post('/admin/users/', data).then(r => r.data),
  update: (id, data) => api.put(`/admin/users/${id}`, data).then(r => r.data),
  toggleActive: (id) => api.patch(`/admin/users/${id}/toggle-active`).then(r => r.data),
  remove: (id) => api.delete(`/admin/users/${id}`)
}

// ===== Stats =====
export const AdminStatsAPI = {
  overview: () => api.get('/admin/stats/overview').then(r => r.data)
}

// ===== SEO =====
export const AdminSeoAPI = {
  globals: () => api.get('/admin/seo/globals').then(r => r.data),
  setGlobal: (key, payload) => api.put(`/admin/seo/globals/${key}`, payload).then(r => r.data),
  redirects: () => api.get('/admin/seo/redirects').then(r => r.data),
  createRedirect: (data) => api.post('/admin/seo/redirects', data).then(r => r.data),
  updateRedirect: (id, data) => api.put(`/admin/seo/redirects/${id}`, data).then(r => r.data),
  removeRedirect: (id) => api.delete(`/admin/seo/redirects/${id}`)
}
