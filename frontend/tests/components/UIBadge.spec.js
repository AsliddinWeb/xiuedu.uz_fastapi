import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import UIBadge from '@/components/ui/UIBadge.vue'

describe('UIBadge', () => {
  it('renders content', () => {
    const w = mount(UIBadge, { slots: { default: 'New' } })
    expect(w.text()).toBe('New')
  })

  it('applies success variant classes', () => {
    const w = mount(UIBadge, { props: { variant: 'success' }, slots: { default: 'OK' } })
    expect(w.classes().some(c => c.includes('green'))).toBe(true)
  })

  it('renders dot indicator when dot=true', () => {
    const w = mount(UIBadge, { props: { dot: true }, slots: { default: 'X' } })
    expect(w.find('span > span').exists()).toBe(true)
  })
})
