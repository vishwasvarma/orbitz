import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  // GitHub Pages serves the app from /<repo>/, local dev from /
  base: process.env.VITE_BASE_PATH || '/',
  plugins: [react()],
})
