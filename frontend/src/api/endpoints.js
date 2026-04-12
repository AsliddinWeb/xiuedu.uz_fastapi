import api from './client'

export const PagesAPI = {
  list: () => api.get('/pages/').then(r => r.data),
  bySlug: (slug) => api.get(`/pages/${slug}`).then(r => r.data)
}

export const NewsAPI = {
  list: (params = {}) => api.get('/news/', { params }).then(r => r.data),
  bySlug: (slug) => api.get(`/news/${slug}`).then(r => r.data),
  categories: () => api.get('/news/categories/').then(r => r.data)
}

export const EventsAPI = {
  list: (params = {}) => api.get('/events/', { params }).then(r => r.data),
  bySlug: (slug) => api.get(`/events/${slug}`).then(r => r.data)
}

export const ContactAPI = {
  send: (payload) => api.post('/contact', payload).then(r => r.data)
}

export const PageSettingsAPI = {
  home:          (lang) => api.get('/page-settings/home',          { params: { lang } }).then(r => r.data),
  about:         (lang) => api.get('/page-settings/about',         { params: { lang } }).then(r => r.data),
  applicants:    (lang) => api.get('/page-settings/applicants',    { params: { lang } }).then(r => r.data),
  structure:     (lang) => api.get('/page-settings/structure',     { params: { lang } }).then(r => r.data),
  international: (lang) => api.get('/page-settings/international', { params: { lang } }).then(r => r.data),
  vacancies:     (lang) => api.get('/page-settings/vacancies',     { params: { lang } }).then(r => r.data),
  contact:       (lang) => api.get('/page-settings/contact',       { params: { lang } }).then(r => r.data),
  gallery:       (lang) => api.get('/page-settings/gallery',       { params: { lang } }).then(r => r.data)
}

export const FacultiesAPI = {
  list:   (lang) => api.get('/faculties/', { params: { lang } }).then(r => r.data),
  bySlug: (slug, lang) => api.get(`/faculties/${slug}`, { params: { lang } }).then(r => r.data)
}

export const LeadersAPI = {
  list: (lang) => api.get('/leaders/', { params: { lang } }).then(r => r.data)
}
