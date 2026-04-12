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
            if (id.includes('vue-i18n')) return 'vendor-i18n'
            if (id.includes('@vueuse'))   return 'vendor-vueuse'
            if (id.includes('lucide'))    return 'vendor-icons'
            if (id.includes('axios'))     return 'vendor-axios'
            if (id.includes('dompurify')) return 'vendor-dompurify'
            if (id.includes('vue-router')) return 'vendor-router'
            if (id.includes('pinia'))     return 'vendor-pinia'
            if (id.includes('vue'))       return 'vendor-vue'
            return 'vendor'
          }
          if (id.includes('/views/admin/') || id.includes('/components/layout/AdminLayout')) return 'app-admin'
          if (id.includes('/views/public/') || id.includes('/components/sections/')) return 'app-public'
        }
      }
    }
  }
})
