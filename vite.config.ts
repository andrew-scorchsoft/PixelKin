import { defineConfig } from 'vite';
import { fileURLToPath, URL } from 'node:url';

// Web-first config. The build output (dist/) is a plain static bundle, which
// is also exactly what a Capacitor mobile shell wraps later — so keeping the
// app a self-contained static build is what makes the eventual web -> mobile
// move cheap. Relative base ('./') matters for that: Capacitor serves the
// bundle from a file-like origin, where absolute '/' asset paths break.
export default defineConfig({
  base: './',
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@game': fileURLToPath(new URL('./src/game', import.meta.url)),
      '@platform': fileURLToPath(new URL('./src/platform', import.meta.url)),
    },
  },
  server: {
    host: true,
    port: 5173,
  },
  build: {
    outDir: 'dist',
    target: 'es2021',
    sourcemap: true,
  },
});
