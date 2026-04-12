import { describe, it, expect } from 'vitest'
import {
  organizationSchema,
  newsArticleSchema,
  breadcrumbSchema,
  faqSchema,
  graph
} from '@/utils/schema'

describe('schema helpers', () => {
  it('organizationSchema is CollegeOrUniversity', () => {
    const s = organizationSchema()
    expect(s['@type']).toBe('CollegeOrUniversity')
    expect(s.name).toMatch(/Universitet/)
    expect(s.address.addressCountry).toBe('UZ')
    expect(s.sameAs.length).toBeGreaterThan(0)
  })

  it('newsArticleSchema includes headline and publisher', () => {
    const s = newsArticleSchema({
      title: 'Hello',
      slug: 'hello',
      published_at: '2026-01-01',
      excerpt: 'short'
    })
    expect(s['@type']).toBe('NewsArticle')
    expect(s.headline).toBe('Hello')
    expect(s.publisher['@type']).toBe('Organization')
  })

  it('breadcrumbSchema produces ordered ListItems', () => {
    const s = breadcrumbSchema([
      { name: 'Home', url: '/' },
      { name: 'News', url: '/news' }
    ])
    expect(s['@type']).toBe('BreadcrumbList')
    expect(s.itemListElement).toHaveLength(2)
    expect(s.itemListElement[0].position).toBe(1)
    expect(s.itemListElement[1].position).toBe(2)
  })

  it('faqSchema wraps Q/A as Question/Answer', () => {
    const s = faqSchema([{ q: 'Q1?', a: 'A1' }])
    expect(s['@type']).toBe('FAQPage')
    expect(s.mainEntity[0]['@type']).toBe('Question')
  })

  it('graph combines multiple schemas', () => {
    const g = graph(organizationSchema(), breadcrumbSchema([{ name: 'Home', url: '/' }]))
    expect(g['@graph']).toHaveLength(2)
  })
})
