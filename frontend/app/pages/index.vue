<template>
  <div class="min-h-screen flex flex-col items-center justify-center p-4">
    <h1 class="text-4xl font-bold text-gray-800 mb-6">Welcome to My Portfolio</h1>
    <p class="text-xl text-gray-600 mb-8">Frontend Developer & UI/UX Enthusiast</p>
    <div class="flex space-x-4">
      <button class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
        View Projects
      </button>
      <button class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded">
        Contact Me
      </button>
    </div>
    <div class="mt-8">
      <NuxtLink to="/about" class="text-blue-500 hover:underline">
        About
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
// Use Nuxt's useHead composable for SEO
useHead({
  title: 'Home | My Portfolio',
  meta: [
    { name: 'description', content: 'Welcome to my professional portfolio showcasing my work and skills' }
  ]
})
</script>
