import { watchEffect } from 'vue'
import { useLanguageStore } from '@/stores/language'

const SITE_NAME = 'XIU Edu'
const SITE_BASE = (typeof window !== 'undefined' && window.location.origin) || 'https://xiuedu.uz'

function setMeta(name, content, attr = 'name') {
  if (content == null || content === '') return removeMeta(name, attr)
  let el = document.querySelector(`meta[${attr}="${name}"]`)
  if (!el) {
    el = document.createElement('meta')
    el.setAttribute(attr, name)
    document.head.appendChild(el)
  }
  el.setAttribute('content', content)
}

function removeMeta(name, attr = 'name') {
  const el = document.querySelector(`meta[${attr}="${name}"]`)
  if (el) el.remove()
}

function setLink(rel, href, attrs = {}) {
  const key = attrs.hreflang ? `[hreflang="${attrs.hreflang}"]` : ''
  let el = document.querySelector(`link[rel="${rel}"]${key}`)
  if (!el) {
    el = document.createElement('link')
    el.setAttribute('rel', rel)
    document.head.appendChild(el)
  }
  el.setAttribute('href', href)
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v)
}

function clearHreflang() {
  document.querySelectorAll('link[rel="alternate"][hreflang]').forEach(el => el.remove())
}

function clearPageJsonLd() {
  document.querySelectorAll('script[type="application/ld+json"][data-page]').forEach(el => el.remove())
}

function appendJsonLd(data) {
  const el = document.createElement('script')
  el.setAttribute('type', 'application/ld+json')
  el.setAttribute('data-page', '1')
  el.textContent = JSON.stringify(data)
  document.head.appendChild(el)
}

function setJsonLd(payload) {
  clearPageJsonLd()
  if (!payload) return
  const list = Array.isArray(payload) ? payload : [payload]
  for (const item of list) appendJsonLd(item)
}

/**
 * Reactive SEO head manager.
 *
 * @param {() => {
 *   title?: string,
 *   description?: string,
 *   image?: string,
 *   url?: string,
 *   type?: string,    // og:type — website | article
 *   schema?: object | object[]   // schema.org JSON-LD payload (single or array)
 *   noIndex?: boolean
 * }} getter
 */
export function useSeo(getter) {
  const lang = (() => {
    try { return useLanguageStore() } catch { return null }
  })()

  watchEffect(() => {
    const data = getter() || {}
    const locale = lang?.current || 'uz'
    const pageUrl = data.url || (typeof window !== 'undefined' ? window.location.href : SITE_BASE)
    const path = (typeof window !== 'undefined') ? window.location.pathname : '/'

    // Title
    document.title = data.title ? `${data.title} — ${SITE_NAME}` : SITE_NAME

    // Standard meta
    setMeta('description', data.description)
    setMeta('robots', data.noIndex ? 'noindex, nofollow' : 'index, follow')

    // Twitter
    setMeta('twitter:card', 'summary_large_image')
    setMeta('twitter:title', data.title)
    setMeta('twitter:description', data.description)
    setMeta('twitter:image', data.image)

    // OpenGraph
    setMeta('og:title', data.title, 'property')
    setMeta('og:description', data.description, 'property')
    setMeta('og:image', data.image, 'property')
    setMeta('og:url', pageUrl, 'property')
    setMeta('og:type', data.type || 'website', 'property')
    setMeta('og:site_name', SITE_NAME, 'property')
    setMeta('og:locale', locale === 'uz' ? 'uz_UZ' : locale === 'ru' ? 'ru_RU' : 'en_US', 'property')

    // Canonical
    setLink('canonical', `${SITE_BASE}${path}`)

    // hreflang for 3 languages
    clearHreflang()
    const supported = ['uz', 'ru', 'en']
    for (const code of supported) {
      setLink('alternate', `${SITE_BASE}${path}?lang=${code}`, { hreflang: code })
    }
    setLink('alternate', `${SITE_BASE}${path}`, { hreflang: 'x-default' })

    // JSON-LD per page (single object or array)
    setJsonLd(data.schema)
  })
}
