import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { canAccess } from '@/utils/roles'

const PublicLayout = () => import('@/components/layout/AppLayout.vue')
const AdminLayout  = () => import('@/views/admin/AdminLayout.vue')

const routes = [
  // ===== Public =====
  {
    path: '/',
    component: PublicLayout,
    children: [
      { path: '',                   name: 'home',         component: () => import('@/views/public/HomeView.vue'),
        meta: { title: 'XIU Edu' } },
      { path: 'about',              name: 'about',        component: () => import('@/views/public/AboutView.vue'),
        meta: { title: 'about.title' } },
      { path: 'leadership',         name: 'leadership',   component: () => import('@/views/public/LeadershipView.vue'),
        meta: { title: 'nav.leadership' } },
      { path: 'structure',          name: 'structure',    component: () => import('@/views/public/StructureView.vue'),
        meta: { title: 'nav.structure' } },
      { path: 'faculties',          name: 'faculties',    component: () => import('@/views/public/FacultiesView.vue'),
        meta: { title: 'faculties.title' } },
      { path: 'faculties/:slug',    name: 'faculty-detail', component: () => import('@/views/public/FacultyDetailView.vue'),
        meta: { title: 'nav.faculties' } },
      { path: 'education/bachelor', name: 'bachelor',     component: () => import('@/views/public/BachelorView.vue'),
        meta: { title: 'nav.bachelor' } },
      { path: 'education/master',   name: 'master',       component: () => import('@/views/public/MasterView.vue'),
        meta: { title: 'nav.master' } },
      { path: 'students',           name: 'students',     component: () => import('@/views/public/StudentsView.vue'),
        meta: { title: 'nav.students' } },
      { path: 'applicants',         name: 'applicants',   component: () => import('@/views/public/ApplicantsView.vue'),
        meta: { title: 'nav.applicants' } },
      { path: 'news',               name: 'news',         component: () => import('@/views/public/NewsListView.vue'),
        meta: { title: 'news.title' } },
      { path: 'news/:slug',         name: 'news-detail',  component: () => import('@/views/public/NewsDetailView.vue'),
        meta: { title: 'news.title' } },
      { path: 'events',             name: 'events',       component: () => import('@/views/public/EventsView.vue'),
        meta: { title: 'nav.events' } },
      { path: 'events/:slug',       name: 'event-detail', component: () => import('@/views/public/EventDetailView.vue'),
        meta: { title: 'nav.events' } },
      { path: 'gallery',            name: 'gallery',      component: () => import('@/views/public/GalleryView.vue'),
        meta: { title: 'nav.gallery' } },
      { path: 'international',      name: 'international', component: () => import('@/views/public/InternationalView.vue'),
        meta: { title: 'nav.international' } },
      { path: 'contact',            name: 'contact',      component: () => import('@/views/public/ContactView.vue'),
        meta: { title: 'contact.title' } },
      { path: 'careers',            name: 'careers',      component: () => import('@/views/public/VacanciesView.vue'),
        meta: { title: 'nav.vacancies' } },
      { path: 'vacancies',          redirect: '/careers' },
      { path: 'p/:slug',            name: 'static-page',  component: () => import('@/views/public/StaticPageView.vue'),
        meta: { title: 'nav.university' } },
      { path: 'forbidden',          name: 'forbidden',    component: () => import('@/views/public/ForbiddenView.vue'),
        meta: { title: '403' } },
      { path: 'server-error',       name: 'server-error', component: () => import('@/views/public/ServerErrorView.vue'),
        meta: { title: '500' } }
    ]
  },

  // ===== Login =====
  { path: '/login', name: 'login', component: () => import('@/views/public/LoginView.vue') },

  // ===== Admin =====
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      { path: '',         name: 'admin-dashboard', component: () => import('@/views/admin/DashboardView.vue'),
        meta: { title: 'Dashboard' } },
      { path: 'news',     name: 'admin-news',      component: () => import('@/views/admin/news/NewsListView.vue'),
        meta: { title: 'Yangiliklar', roles: ['admin', 'content_manager'] } },
      { path: 'news/:id', name: 'admin-news-edit', component: () => import('@/views/admin/news/NewsEditView.vue'),
        meta: { title: 'Yangilik tahrirlash', roles: ['admin', 'content_manager'] } },
      { path: 'events',     name: 'admin-events',      component: () => import('@/views/admin/events/EventsListView.vue'),
        meta: { title: 'Tadbirlar', roles: ['admin', 'content_manager'] } },
      { path: 'events/:id', name: 'admin-events-edit', component: () => import('@/views/admin/events/EventsEditView.vue'),
        meta: { title: 'Tadbir tahrirlash', roles: ['admin', 'content_manager'] } },
      { path: 'profile',  name: 'admin-profile',   component: () => import('@/views/admin/ProfileView.vue'),
        meta: { title: 'Mening kabinetim' } },
      { path: 'home-settings', name: 'admin-home-settings',
        component: () => import('@/views/admin/home-settings/HomeSettingsView.vue'),
        meta: { title: 'Bosh sahifa', roles: ['admin', 'content_manager'] } },
      { path: 'leaders', name: 'admin-leaders',
        component: () => import('@/views/admin/LeadersView.vue'),
        meta: { title: 'Rahbariyat', roles: ['admin', 'content_manager'] } },
      { path: 'leaders/:id', name: 'admin-leader-edit',
        component: () => import('@/views/admin/LeaderEditView.vue'),
        meta: { title: 'Rahbar tahrirlash', roles: ['admin', 'content_manager'] } },
      { path: 'about-settings', name: 'admin-about-settings',
        component: () => import('@/views/admin/about-settings/AboutSettingsView.vue'),
        meta: { title: 'Universitet haqida', roles: ['admin', 'content_manager'] } },
      { path: 'applicants-settings', name: 'admin-applicants-settings',
        component: () => import('@/views/admin/applicants-settings/ApplicantsSettingsView.vue'),
        meta: { title: 'Abituriyentlarga', roles: ['admin', 'content_manager'] } },
      { path: 'structure-settings', name: 'admin-structure-settings',
        component: () => import('@/views/admin/structure-settings/StructureSettingsView.vue'),
        meta: { title: 'Tarkibiy tuzilma', roles: ['admin', 'content_manager'] } },
      { path: 'international-settings', name: 'admin-international-settings',
        component: () => import('@/views/admin/international-settings/IntlSettingsView.vue'),
        meta: { title: 'Xalqaro hamkorlik', roles: ['admin', 'content_manager'] } },
      { path: 'vacancies-settings', name: 'admin-vacancies-settings',
        component: () => import('@/views/admin/vacancies-settings/VacanciesSettingsView.vue'),
        meta: { title: 'Vakansiyalar', roles: ['admin', 'content_manager'] } },
      { path: 'contact-settings', name: 'admin-contact-settings',
        component: () => import('@/views/admin/ContactSettingsView.vue'),
        meta: { title: 'Aloqa sahifasi', roles: ['admin', 'content_manager'] } },
      { path: 'gallery-settings', name: 'admin-gallery-settings',
        component: () => import('@/views/admin/gallery-settings/GallerySettingsView.vue'),
        meta: { title: 'Galereya', roles: ['admin', 'content_manager'] } },
      { path: 'pages',    name: 'admin-pages',     component: () => import('@/views/admin/pages/PagesListView.vue'),
        meta: { title: 'Sahifalar', roles: ['admin', 'page_editor'] } },
      { path: 'pages/:id', name: 'admin-pages-edit', component: () => import('@/views/admin/pages/PageEditView.vue'),
        meta: { title: 'Sahifa tahrirlash', roles: ['admin', 'page_editor'] } },
      { path: 'media',    name: 'admin-media',     component: () => import('@/views/admin/MediaView.vue'),
        meta: { title: 'Media', roles: ['admin', 'content_manager', 'page_editor'] } },
      { path: 'users',    name: 'admin-users',     component: () => import('@/views/admin/UsersView.vue'),
        meta: { title: 'Foydalanuvchilar', roles: ['admin'] } },
      { path: 'seo',      name: 'admin-seo',       component: () => import('@/views/admin/SEOView.vue'),
        meta: { title: 'SEO', roles: ['admin'] } },
      { path: 'site-settings', name: 'admin-site-settings',
        component: () => import('@/views/admin/SiteSettingsView.vue'),
        meta: { title: 'Sayt sozlamalari', roles: ['admin'] } }
    ]
  },

  { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('@/views/public/NotFoundView.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, saved) {
    if (saved) return saved
    return { top: 0, behavior: 'smooth' }
  }
})

router.beforeEach(async (to) => {
  if (!to.meta.requiresAuth) return true

  const auth = useAuthStore()
  if (!auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  // Ensure user is loaded for role checks
  if (!auth.user) {
    await auth.loadMe()
    if (!auth.user) return { name: 'login', query: { redirect: to.fullPath } }
  }

  // Per-route role check
  const roles = to.meta.roles
  if (roles && roles.length && !canAccess(auth.role, roles)) {
    return { name: 'forbidden' }
  }

  return true
})

export default router
