import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import UIButton from '@/components/ui/UIButton.vue'

describe('UIButton', () => {
  it('renders default slot', () => {
    const wrap = mount(UIButton, { slots: { default: 'Click me' } })
    expect(wrap.text()).toContain('Click me')
  })

  it('applies primary variant by default', () => {
    const wrap = mount(UIButton, { slots: { default: 'X' } })
    expect(wrap.classes().some(c => c.includes('bg-primary-700'))).toBe(true)
  })

  it('applies accent variant', () => {
    const wrap = mount(UIButton, { props: { variant: 'accent' }, slots: { default: 'X' } })
    expect(wrap.classes().some(c => c.includes('bg-accent-500'))).toBe(true)
  })

  it('shows loader when loading=true', () => {
    const wrap = mount(UIButton, { props: { loading: true } })
    expect(wrap.attributes('aria-busy')).toBe('true')
  })

  it('disabled prop disables the button', () => {
    const wrap = mount(UIButton, { props: { disabled: true } })
    expect(wrap.attributes('disabled')).toBeDefined()
  })
})
