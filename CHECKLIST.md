# XIU Edu v2 — SEO & Performance Audit Checklist

A living checklist for SEO, accessibility and Core Web Vitals targets.

## 🎯 Performance budget targets

| Metric                       | Target            |
|------------------------------|-------------------|
| Lighthouse Performance       | ≥ 90              |
| Lighthouse SEO               | ≥ 95              |
| Lighthouse Accessibility     | ≥ 90              |
| Lighthouse Best Practices    | ≥ 95              |
| Initial JS (gzipped)         | < 150 KB          |
| Initial CSS (gzipped)        | < 30 KB           |
| LCP (Largest Contentful Paint) | < 2.5 s         |
| CLS (Cumulative Layout Shift) | < 0.1            |
| INP (Interaction to Next Paint) | < 200 ms       |
| TTFB                         | < 600 ms          |

## 🧱 Technical SEO

- [x] HTTPS enforced (production: nginx + cert)
- [x] `<title>` and `<meta name="description">` reactive per route ([useSeo](frontend/src/composables/useSeo.js))
- [x] Canonical link per page
- [x] hreflang tags for uz/ru/en + x-default
- [x] robots.txt with sitemap reference and crawl rules ([backend/app/routers/seo.py](backend/app/routers/seo.py))
- [x] Sitemap index splitting: `/api/sitemap.xml` → static, pages, news
- [x] Image extension in news/pages sitemap (`<image:image>`)
- [x] No duplicate content across language versions (hreflang resolves)
- [x] 404 page with proper status
- [x] 403 forbidden page for admin role mismatches
- [x] 301 legacy redirects via nginx `map` ([nginx/redirects.conf](nginx/redirects.conf))
- [x] noindex for admin/login routes (nginx rules + meta when needed)
- [ ] HTTP/2 or HTTP/3 enabled in production nginx
- [ ] Brotli compression in addition to gzip
- [ ] HSTS preload submission

## 🧠 Structured data (Schema.org)

- [x] `CollegeOrUniversity` (homepage) with offer catalog, geo, contact, openingHours, sameAs
- [x] `WebSite` with sitelinks search box (in `index.html`)
- [x] `BreadcrumbList` on inner pages
- [x] `NewsArticle` on news detail pages
- [x] `FAQPage` helper available — wire into admissions FAQ section
- [x] `Event` helper available — wire into events page
- [x] `Person` helper available — wire into leadership profiles
- [ ] `Course` schema for individual programs
- [ ] `Review` / `AggregateRating` if/when reviews appear

Helpers: [frontend/src/utils/schema.js](frontend/src/utils/schema.js)

## 🌍 Internationalization

- [x] 3 locales: uz, ru, en with vue-i18n composition mode
- [x] Lazy loading: ru/en chunks loaded on demand
- [x] `<html lang>` attribute updated on language switch
- [x] OG `og:locale` + `og:locale:alternate` per page
- [x] hreflang in HTML head AND inside sitemap (`xhtml:link`)
- [ ] Locale-prefix URL strategy (`/uz/...`, `/ru/...`, `/en/...`) — currently uses `?lang=` query (Phase 2 migration)

## 🖼 Images

- [x] [UIImage](frontend/src/components/ui/UIImage.vue) wrapper enforces:
  - required `alt`, `width`, `height` (prevents CLS)
  - native `loading="lazy"` (eager opt-in for hero/LCP)
  - `decoding="async"`, `fetchpriority` for LCP
  - `<picture>` WebP fallback
  - LQIP blur-up via `placeholder` prop
- [x] Backend `image_service` auto-converts uploads to WebP + thumbnail + medium variants
- [ ] Replace placeholder gradients in sections with real photography
- [ ] All admin-uploaded images get descriptive `alt_uz/ru/en` (DB fields exist; enforce in UI)

## ⚡ Core Web Vitals

### LCP
- [x] Preload font CSS in `index.html`
- [x] Preload hero/OG image with `fetchpriority="high"`
- [x] Self-host Inter / Playfair Display with `font-display: swap` (Google Fonts swap)
- [ ] Migrate to self-hosted woff2 subset for production
- [x] Code-splitting per vendor + per route ([vite.config.js](frontend/vite.config.js))

### CLS
- [x] All UIImage instances require width+height
- [x] Reserved aspect ratios on hero / news cards
- [x] No font-swap layout shift (preconnect + preload)
- [x] Sticky navbar uses backdrop-blur (no shift)

### INP / FID
- [x] Analytics initialization deferred via `requestIdleCallback`
- [x] Cookie consent loads after 1.5s (non-blocking)
- [x] Heavy admin chunk lazy-loaded only when entering /admin
- [x] Pinia stores instantiated lazily

## 📊 Analytics & Tracking

- [x] [analytics plugin](frontend/src/plugins/analytics.js) — GA4 + Yandex Metrica
- [x] GDPR-lite cookie consent banner ([CookieConsent.vue](frontend/src/components/ui/CookieConsent.vue))
- [x] No tracking until consent granted
- [x] SPA route changes tracked via `router.afterEach`
- [x] `trackEvent()` helper for custom goals (apply_click, contact_submit, news_view)
- [ ] Set GA4 ID and Yandex Metrica counter ID via `VITE_GA4_ID` / `VITE_YM_ID` env vars

## ♿ Accessibility

- [x] Semantic HTML5 (header/main/footer/nav/article/section)
- [x] `:focus-visible` outline (gold accent ring) on all interactive elements
- [x] ARIA labels on icon-only buttons
- [x] Modal: `role="dialog"`, `aria-modal`, focus return on close
- [x] Dropdown: `role="listbox"`, keyboard ESC + click-outside
- [x] Color contrast meets WCAG AA (verified for primary/accent on white & navy)
- [x] `prefers-reduced-motion` honored — animations collapse to 0.01ms
- [x] Skip-to-content not yet — TODO

## 🛡 Security headers (in [nginx/default.conf](nginx/default.conf))

- [x] `X-Frame-Options: SAMEORIGIN`
- [x] `X-Content-Type-Options: nosniff`
- [x] `Referrer-Policy: strict-origin-when-cross-origin`
- [x] `Permissions-Policy`
- [x] `Strict-Transport-Security` (HSTS)
- [x] `Content-Security-Policy`
- [ ] CSP nonce strategy (currently allows `unsafe-inline` for Vue)

## 📱 Mobile / PWA

- [x] Responsive viewport meta
- [x] `theme-color` light + dark variants
- [x] Web app manifest ([frontend/public/manifest.webmanifest](frontend/public/manifest.webmanifest))
- [x] `mobile-web-app-capable` (deprecated `apple-` kept for backward compat)
- [ ] Service worker for static asset caching (Phase 2)
- [ ] Real PNG icon set (currently SVG only)

## 🔍 Content SEO

- [x] CMS supports per-language `meta_title` and `meta_description` for pages and news
- [x] OG image field per page
- [x] Slug field editable per content (auto-generated from UZ title)
- [ ] Internal linking strategy doc
- [ ] Cornerstone content marked
- [ ] Author byline on articles (DB has author_id; UI doesn't display yet)

## 📝 Backend / API SEO

- [x] `/api/sitemap.xml` — sitemap index
- [x] `/api/sitemap-static.xml`, `/api/sitemap-pages.xml`, `/api/sitemap-news.xml`
- [x] `/api/robots.txt` — server-rendered with absolute Sitemap URL
- [x] News view counter via `GET /api/news/{slug}` (server-side, no JS pixel)
- [x] Cache layer ready ([cache.py](backend/app/middleware/cache.py)) for hot endpoints

## 🔁 Migration / launch checklist

- [ ] Submit new sitemap to Google Search Console
- [ ] Submit new sitemap to Yandex Webmaster
- [ ] Verify ownership in both consoles
- [ ] Set `VITE_GA4_ID` and `VITE_YM_ID` in production `.env`
- [ ] Audit legacy redirects with `curl -I` against production
- [ ] Run Lighthouse CI on key routes (home, about, news, news/:slug, contact)
- [ ] Test hreflang tags with `curl -s URL | grep hreflang`
- [ ] Verify JSON-LD with [Rich Results Test](https://search.google.com/test/rich-results)
- [ ] Check sitemap with [XML Sitemap validator](https://www.xml-sitemaps.com/validate-xml-sitemap.html)
- [ ] Submit sitemaps and ping `https://www.google.com/ping?sitemap=...`

## 🆚 vs current xiuedu.uz (issues fixed)

| Issue                           | Status | Fix                                              |
|--------------------------------|--------|--------------------------------------------------|
| Missing structured data         | ✅     | Schema.org @graph on every page                  |
| Generic meta descriptions       | ✅     | Per-language meta in CMS + reactive useSeo       |
| No hreflang for multilingual    | ✅     | hreflang in HTML head + sitemap xhtml:link       |
| Sitemap not optimized           | ✅     | Index split, image extensions, lastmod, priority |
| Images without alt              | ✅     | UIImage enforces alt + DB ml alt fields          |
| Slow Core Web Vitals            | ⚙️     | Code splitting + LCP preload + lazy chunks       |
| No breadcrumb markup            | ✅     | BreadcrumbList JSON-LD on inner pages            |
| Duplicate content (lang)        | ✅     | hreflang resolves; canonical per locale          |
