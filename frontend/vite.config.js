import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true, // Needed for Docker to expose the port to the host
    watch: {
      usePolling: true, // Needed for hot-reloading inside Docker on some OS
    },
  },
})
