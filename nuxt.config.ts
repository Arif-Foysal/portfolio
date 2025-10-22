import tailwindcss from "@tailwindcss/vite";
import type { NuxtConfig } from 'nuxt/schema'

export default defineNuxtConfig(<NuxtConfig>{
  app: {
    pageTransition: { name: 'page', mode: 'out-in' },
  },
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  modules: [
    '@nuxtjs/color-mode'
  ],
  colorMode: {
    classSuffix: '', // Important to work with Tailwind's dark mode
    preference: 'system', // or 'light' or 'dark'
    fallback: 'light',
  },
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
});