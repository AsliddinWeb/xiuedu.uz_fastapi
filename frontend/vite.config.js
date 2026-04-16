import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0',
    port: 5176,
    strictPort: true,
    watch: { usePolling: true }
  },
  build: {
    target: 'es2020',
    sourcemap: false,
    chunkSizeWarningLimit: 1000,
    cssCodeSplit: true,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('vue-i18n'))   return 'vendor-i18n'
            if (id.includes('@vueuse'))    return 'vendor-vueuse'
            if (id.includes('lucide'))     return 'vendor-icons'
            if (id.includes('axios'))      return 'vendor-axios'
            if (id.includes('dompurify'))  return 'vendor-dompurify'
            if (id.includes('vue-router')) return 'vendor-router'
            if (id.includes('pinia'))      return 'vendor-pinia'
            if (id.includes('vue'))        return 'vendor-vue'
            return 'vendor'
          }
          // Shared files (api, components, stores, utils) — o'z chunk'iga
          // Admin va Public ularni import qiladi — circular dependency bo'lmaydi
          if (id.includes('/api/'))        return 'shared-api'
          if (id.includes('/stores/'))     return 'shared-stores'
          if (id.includes('/utils/'))      return 'shared-utils'
          if (id.includes('/composables/')) return 'shared-composables'
          if (id.includes('/components/admin/')) return 'shared-admin-components'
          if (id.includes('/components/cards/')) return 'shared-cards'
        }
      }
    }
  }
})
