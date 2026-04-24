/** @type {import('tailwindcss').Config} */
import typography from '@tailwindcss/typography'
import forms from '@tailwindcss/forms'
import aspectRatio from '@tailwindcss/aspect-ratio'

export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  // Safelist classes coming from the CMS (faculty/program bg_class, icon_bg_class, ring_class)
  safelist: [
    {
      pattern: /^(bg|ring)-(slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-(50|100|200|300|400|500|600|700|800|900)(\/\d{1,3})?$/,
      variants: ['dark', 'hover', 'group-hover'],
    },
    {
      pattern: /^(dark:bg|dark:ring)-(slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-(50|100|200|300|400|500|600|700|800|900)(\/\d{1,3})?$/,
    },
  ],
  theme: {
    extend: {
      colors: {
        // ===== PRIMARY — Indigo Navy (uobs.uz inspired) =====
        primary: {
          50:  '#EEF0FF',
          100: '#DDE0F5',
          200: '#B8BFE8',
          300: '#8F99D6',
          400: '#5D6BBF',
          500: '#2D3A8C',  // mid indigo
          600: '#222B75',
          700: '#1A1F6E',  // deep navy
          800: '#0F1550',  // deeper — hero mid
          900: '#0A0D3D'   // darkest — hero top / footer
        },

        // ===== SECONDARY — Cool slate navy =====
        secondary: {
          50:  '#EEF1F7',
          100: '#D3D9EA',
          200: '#A9B3D2',
          300: '#7E8AB5',
          400: '#5868A0',
          500: '#3B4788',
          600: '#2A336B',
          700: '#1F2652',
          800: '#151B3D',
          900: '#0B0F28'
        },

        // ===== ACCENT — Golden Yellow =====
        accent: {
          50:  '#FFF9E6',
          100: '#FFF2C2',
          200: '#FFE588',
          300: '#FFD74D',
          400: '#FFC107',
          500: '#FFB300',  // main golden CTA
          600: '#E6A000',
          700: '#C48A00',
          800: '#996B00',
          900: '#6B4A00'
        },

        // ===== GOLD alias =====
        gold: {
          300: '#FFD74D',
          400: '#FFC107',
          500: '#FFB300',
          600: '#E6A000'
        },

        // ===== SURFACE — whites with cool-blue tint =====
        surface: {
          white:  '#FFFFFF',
          light:  '#F5F7FF',
          soft:   '#EEF0FF',
          muted:  '#DDE0F5',
          subtle: '#B8BFE8'
        },

        // ===== INK — brand-matching text =====
        ink: {
          dark:    '#0A0D3D',
          medium:  '#2D3561',
          light:   '#6B74A8',
          faint:   '#9BA3C8',
          inverse: '#FFFFFF'
        },

        // ===== Semantic =====
        success: { light: '#DCFCE7', DEFAULT: '#22C55E', dark: '#15803D' },
        warning: { light: '#FEF9C3', DEFAULT: '#EAB308', dark: '#A16207' },
        danger:  { light: '#FEE2E2', DEFAULT: '#EF4444', dark: '#B91C1C' },
        info:    { light: '#DBEAFE', DEFAULT: '#3B82F6', dark: '#1D4ED8' },

        // Backwards-compat
        neutral: {
          50:  '#F5F7FF',
          100: '#EEF0FF',
          200: '#DDE0F5',
          300: '#B8BFE8',
          400: '#9BA3C8',
          500: '#6B74A8',
          600: '#4D5689',
          700: '#2D3561',
          800: '#1A1F45',
          900: '#0A0D3D'
        }
      },

      fontFamily: {
        sans:    ['Inter', 'system-ui', '-apple-system', 'Segoe UI', 'sans-serif'],
        display: ['"Plus Jakarta Sans"', 'Inter', 'sans-serif'],
        mono:    ['"JetBrains Mono"', 'monospace']
      },

      fontSize: {
        xs:   ['0.75rem',  { lineHeight: '1rem' }],
        sm:   ['0.875rem', { lineHeight: '1.25rem' }],
        base: ['1rem',     { lineHeight: '1.6rem' }],
        lg:   ['1.125rem', { lineHeight: '1.75rem' }],
        xl:   ['1.25rem',  { lineHeight: '1.75rem' }],
        '2xl':['1.5rem',   { lineHeight: '2rem' }],
        '3xl':['1.875rem', { lineHeight: '2.25rem' }],
        '4xl':['2.25rem',  { lineHeight: '2.5rem' }],
        '5xl':['3rem',     { lineHeight: '1.15' }],
        '6xl':['3.75rem',  { lineHeight: '1.1' }]
      },

      boxShadow: {
        card:            '0 1px 3px rgba(10,13,61,0.06), 0 4px 16px rgba(10,13,61,0.08)',
        'card-hover':    '0 4px 12px rgba(10,13,61,0.10), 0 12px 32px rgba(10,13,61,0.14)',
        nav:             '0 2px 20px rgba(10,13,61,0.08)',
        dropdown:        '0 8px 32px rgba(10,13,61,0.12), 0 2px 8px rgba(10,13,61,0.06)',
        modal:           '0 20px 60px rgba(10,13,61,0.20)',
        button:          '0 2px 8px rgba(26,31,110,0.30)',
        'button-accent': '0 4px 28px rgba(255,179,0,0.45)',
        soft:            '0 4px 24px -8px rgba(10,13,61,0.12)',
        glow:            '0 0 24px -4px rgba(255,179,0,0.45)',
        inner:           'inset 0 1px 3px rgba(10,13,61,0.08)'
      },

      borderRadius: {
        sm: '6px', DEFAULT: '8px', md: '10px', lg: '12px', xl: '16px', '2xl': '20px', '3xl': '28px'
      },

      spacing: { 18: '4.5rem', 88: '22rem', 128: '32rem' },

      container: {
        center: true,
        padding: { DEFAULT: '1rem', sm: '1.5rem', lg: '2rem' }
      },

      backgroundImage: {
        'hero-gradient':   'linear-gradient(135deg, #0A0D3D 0%, #1A1F6E 50%, #2D3A8C 100%)',
        'navy-gradient':   'linear-gradient(180deg, #0F1550 0%, #0A0D3D 100%)',
        'accent-gradient': 'linear-gradient(135deg, #FFB300 0%, #FF8C00 100%)',
        'gold-text':       'linear-gradient(135deg, #FFD74D 0%, #FFB300 45%, #FF8C00 100%)'
      },

      transitionTimingFunction: {
        smooth:        'cubic-bezier(0.4, 0, 0.2, 1)',
        'bounce-soft': 'cubic-bezier(0.34, 1.56, 0.64, 1)'
      },

      animation: {
        'fade-in':        'fadeIn 0.3s ease-out',
        'hero-enter':     'heroEnter 0.65s cubic-bezier(0.4, 0, 0.2, 1) forwards',
        'slide-up':       'slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
        'slide-down':     'slideDown 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
        'slide-in-right': 'slideInRight 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
        'scale-in':       'scaleIn 0.2s cubic-bezier(0.34, 1.56, 0.64, 1)',
        'float':          'floatCard 6s ease-in-out infinite'
      },

      keyframes: {
        fadeIn:    { from: { opacity: '0' }, to: { opacity: '1' } },
        heroEnter: { from: { opacity: '0', transform: 'translateY(22px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        slideUp:   { from: { opacity: '0', transform: 'translateY(16px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        slideDown: { from: { opacity: '0', transform: 'translateY(-8px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        slideInRight: { from: { opacity: '0', transform: 'translateX(20px)' }, to: { opacity: '1', transform: 'translateX(0)' } },
        scaleIn:   { from: { opacity: '0', transform: 'scale(0.95)' }, to: { opacity: '1', transform: 'scale(1)' } },
        floatCard: { '0%, 100%': { transform: 'translateY(0)' }, '50%': { transform: 'translateY(-8px)' } }
      }
    }
  },
  plugins: [typography, forms, aspectRatio]
}
