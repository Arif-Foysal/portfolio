// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/image',
    '@nuxt/ui',
    '@nuxt/content',
    '@vueuse/nuxt',
    'nuxt-og-image',
    // 'nuxt-gtag'
  ],


  // runtimeConfig: {
  //   public: {
  //     gaId: process.env.NUXT_PUBLIC_GA_ID || '',               // set in Netlify UI
  //     enableAnalytics: process.env.NUXT_PUBLIC_ENABLE_ANALYTICS === 'true'
  //   }
  // },

  // gtag: {
  //   id: process.env.NUXT_PUBLIC_GA_ID || '',
  // },
  // devtools: {
  //   enabled: true
  // },

  css: ['~/assets/css/main.css'],

  routeRules: {
    '/docs': { redirect: '/docs/getting-started', prerender: false }
  },

  compatibilityDate: '2024-07-11',

  nitro: {
    prerender: {
      routes: [
        '/'
      ],
      crawlLinks: true
    }
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  },

  vite: {
    resolve: {
      alias: {
        // 'zod/locales': 'zod/lib/locales' // adjust if your zod version uses a different path
      }
    }
  }
})