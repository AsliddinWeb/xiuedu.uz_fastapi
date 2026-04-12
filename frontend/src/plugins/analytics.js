/**
 * Lightweight analytics with GDPR-lite consent gate.
 *
 * - Loads gtag.js (GA4) and Yandex Metrica only AFTER user consent.
 * - Tracks SPA route changes via vue-router afterEach hook.
 * - Exposes trackEvent() helper.
 */

const STORAGE_KEY = 'xiuedu_analytics_consent'

const cfg = {
  ga4: import.meta.env.VITE_GA4_ID || '',          // e.g. G-XXXXXXX
  metrica: import.meta.env.VITE_YM_ID || ''        // e.g. 12345678
}

let initialized = false

function loadGA4() {
  if (!cfg.ga4 || window.gtag) return
  const s = document.createElement('script')
  s.async = true
  s.src = `https://www.googletagmanager.com/gtag/js?id=${cfg.ga4}`
  document.head.appendChild(s)
  window.dataLayer = window.dataLayer || []
  window.gtag = function () { window.dataLayer.push(arguments) }
  window.gtag('js', new Date())
  window.gtag('config', cfg.ga4, { send_page_view: false, anonymize_ip: true })
}

function loadMetrica() {
  if (!cfg.metrica || window.ym) return
  // Inline Metrica snippet
  ;(function (m, e, t, r, i, k, a) {
    m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments) }
    m[i].l = +new Date()
    k = e.createElement(t); a = e.getElementsByTagName(t)[0]
    k.async = 1; k.src = r; a.parentNode.insertBefore(k, a)
  })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js', 'ym')
  window.ym(Number(cfg.metrica), 'init', {
    clickmap: true, trackLinks: true, accurateTrackBounce: true, webvisor: false
  })
}

export function initAnalytics(router) {
  if (initialized) return
  initialized = true

  const consent = localStorage.getItem(STORAGE_KEY)
  if (consent === 'granted') startAnalytics(router)
}

export function grantConsent(router) {
  localStorage.setItem(STORAGE_KEY, 'granted')
  startAnalytics(router)
}

export function denyConsent() {
  localStorage.setItem(STORAGE_KEY, 'denied')
}

export function getConsent() {
  return localStorage.getItem(STORAGE_KEY)
}

function startAnalytics(router) {
  // Defer to idle so it doesn't compete with LCP
  const start = () => {
    loadGA4()
    loadMetrica()
    if (router) {
      router.afterEach((to) => {
        const path = to.fullPath
        if (window.gtag && cfg.ga4) {
          window.gtag('event', 'page_view', {
            page_path: path,
            page_title: document.title,
            page_location: window.location.href
          })
        }
        if (window.ym && cfg.metrica) {
          window.ym(Number(cfg.metrica), 'hit', path, { title: document.title })
        }
      })
    }
  }
  if ('requestIdleCallback' in window) requestIdleCallback(start, { timeout: 2000 })
  else setTimeout(start, 1500)
}

/** Custom event tracking — works once consent is granted. */
export function trackEvent(name, params = {}) {
  if (window.gtag) window.gtag('event', name, params)
  if (window.ym && cfg.metrica) window.ym(Number(cfg.metrica), 'reachGoal', name, params)
}
