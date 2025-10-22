import tailwindcss from "@tailwindcss/vite";
import type { NuxtConfig } from 'nuxt/schema'

export default defineNuxtConfig(<NuxtConfig>{
  ssr: true, // or false, but SSR is okay for static too
  nitro: {
    preset: 'netlify'
  },


  app: {
    pageTransition: { name: 'page', mode: 'out-in' },
  },
  typescript: {
    typeCheck: true,
  },
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  modules: [
    '@nuxtjs/color-mode',
    'nuxt-icon',
    '@nuxt/image'
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