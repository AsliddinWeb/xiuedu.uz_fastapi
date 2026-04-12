/**
 * Schema.org JSON-LD builders.
 * Each function returns a plain JS object ready to JSON-stringify.
 */

const SITE_URL  = 'https://xiuedu.uz'
const SITE_NAME = 'Xalqaro Innovatsion Universiteti'
const LOGO_URL  = 'https://xiuedu.uz/logo.png'

// ===== CollegeOrUniversity (homepage) =====
export function organizationSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'CollegeOrUniversity',
    name: SITE_NAME,
    alternateName: ['XIU', 'XIU Edu', 'ХИУ', 'International Innovation University'],
    url: SITE_URL,
    logo: { '@type': 'ImageObject', url: LOGO_URL },
    image: `${SITE_URL}/og-image.jpg`,
    description: "O'zbekistondagi yetakchi xususiy universitet — bakalavr va magistratura dasturlari, xalqaro hamkorlik.",
    telephone: '+998554061515',
    email: 'info@xiuedu.uz',
    foundingDate: '2009',
    address: {
      '@type': 'PostalAddress',
      streetAddress: "Mirzo Ulug'bek tumani",
      addressLocality: 'Toshkent',
      addressRegion: 'Toshkent shahri',
      postalCode: '100000',
      addressCountry: 'UZ'
    },
    geo: {
      '@type': 'GeoCoordinates',
      latitude: 41.299496,
      longitude: 69.240073
    },
    numberOfStudents: { '@type': 'QuantitativeValue', value: 5000 },
    openingHoursSpecification: [{
      '@type': 'OpeningHoursSpecification',
      dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
      opens: '09:00',
      closes: '18:00'
    }],
    contactPoint: [{
      '@type': 'ContactPoint',
      telephone: '+998554061515',
      contactType: 'admissions',
      email: 'info@xiuedu.uz',
      areaServed: 'UZ',
      availableLanguage: ['uz', 'ru', 'en']
    }],
    hasOfferCatalog: {
      '@type': 'OfferCatalog',
      name: 'Akademik dasturlar',
      itemListElement: [
        { '@type': 'OfferCatalog', name: 'Bakalavriat', url: `${SITE_URL}/education/bachelor` },
        { '@type': 'OfferCatalog', name: 'Magistratura', url: `${SITE_URL}/education/master` }
      ]
    },
    sameAs: [
      'https://t.me/xiuedu',
      'https://facebook.com/xiuedu',
      'https://instagram.com/xiuedu',
      'https://youtube.com/@xiuedu',
      'https://linkedin.com/school/xiuedu'
    ]
  }
}

// ===== NewsArticle =====
export function newsArticleSchema(article) {
  return {
    '@context': 'https://schema.org',
    '@type': 'NewsArticle',
    headline: article.title,
    description: article.meta_description || article.excerpt,
    image: article.cover_image ? [article.cover_image] : [`${SITE_URL}/og-image.jpg`],
    datePublished: article.published_at,
    dateModified: article.updated_at || article.published_at,
    author: {
      '@type': 'Organization',
      name: SITE_NAME,
      url: SITE_URL
    },
    publisher: {
      '@type': 'Organization',
      name: SITE_NAME,
      logo: { '@type': 'ImageObject', url: LOGO_URL }
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': `${SITE_URL}/news/${article.slug}`
    },
    articleSection: article.category?.name,
    inLanguage: 'uz'
  }
}

// ===== BreadcrumbList =====
/**
 * @param {Array<{name: string, url: string}>} items - in order, root → current
 */
export function breadcrumbSchema(items) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((it, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: it.name,
      item: it.url.startsWith('http') ? it.url : `${SITE_URL}${it.url}`
    }))
  }
}

// ===== FAQPage =====
/**
 * @param {Array<{q: string, a: string}>} items
 */
export function faqSchema(items) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: items.map(({ q, a }) => ({
      '@type': 'Question',
      name: q,
      acceptedAnswer: { '@type': 'Answer', text: a }
    }))
  }
}

// ===== Event =====
export function eventSchema(event) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Event',
    name: event.name,
    description: event.description,
    startDate: event.start,
    endDate: event.end || event.start,
    eventStatus: 'https://schema.org/EventScheduled',
    eventAttendanceMode: 'https://schema.org/OfflineEventAttendanceMode',
    location: {
      '@type': 'Place',
      name: event.location || SITE_NAME,
      address: {
        '@type': 'PostalAddress',
        addressLocality: 'Toshkent',
        addressCountry: 'UZ'
      }
    },
    image: event.image,
    organizer: { '@type': 'Organization', name: SITE_NAME, url: SITE_URL }
  }
}

// ===== Person (faculty / leadership) =====
export function personSchema(person) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Person',
    name: person.name,
    jobTitle: person.position,
    image: person.image,
    email: person.email,
    worksFor: { '@type': 'CollegeOrUniversity', name: SITE_NAME, url: SITE_URL }
  }
}

// ===== Combine multiple into a @graph =====
export function graph(...nodes) {
  return {
    '@context': 'https://schema.org',
    '@graph': nodes.filter(Boolean)
  }
}
