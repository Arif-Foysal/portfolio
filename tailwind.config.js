/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{vue,ts,js}',
    './components/**/*.{vue,ts,js}',
    './layouts/**/*.{vue,ts,js}',
    './pages/**/*.{vue,ts,js}',
    './nuxt.config.ts'
  ],
  darkMode: 'class',
  theme: {
    extend: {},
  },
  plugins: [],
};
