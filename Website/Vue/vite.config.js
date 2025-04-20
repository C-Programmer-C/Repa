import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools(), tailwindcss()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  optimizeDeps: {
    include: ['preline'],
  },
  // Configure build output for Django integration
  build: {
    // Generate manifest.json for Django to identify assets
    manifest: true,
    // Output to Django's static directory by default (when using build:django command)
    outDir: '../djanoproject/vue_dist',
    // Configure assets paths for Django static files
    assetsDir: 'assets',
    // Configure base path for all assets
    base: '/static/'
  }
})
