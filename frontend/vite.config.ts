import { defineConfig } from 'vite';
// vite.config.js
export default defineConfig({
  server: {
    proxy: {
      "/api": "http://localhost:8000", 
    },
  },
});
