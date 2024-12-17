import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Allows Railway to expose the server
    port: process.env.PORT || 5173, // Uses Railway's dynamic port
  },
  preview: {
    port: process.env.PORT || 4173, // Ensure production works
    host: '0.0.0.0',
  },
});
