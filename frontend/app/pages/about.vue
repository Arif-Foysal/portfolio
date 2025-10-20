<template>
  <div class="min-h-screen flex flex-col items-center justify-center p-4">
    <h1 class="text-4xl font-bold text-gray-800 mb-6">About Me</h1>
    <div class="max-w-2xl mx-auto text-gray-600">
      <p class="mb-4">
        I'm a passionate frontend developer with expertise in Vue.js, Nuxt.js, and modern web technologies.
      </p>
      <p class="mb-4">
        With a strong focus on creating responsive, accessible, and performant web applications,
        I strive to deliver exceptional user experiences.
      </p>
      <p class="mb-6">
        My skills include HTML, CSS, JavaScript, Vue.js, Nuxt.js, Tailwind CSS, and more.
      </p>
      
      <div class="mt-8">
        <NuxtLink to="/" class="text-blue-500 hover:underline">Back to Home</NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
useHead({
  title: 'About Me | My Portfolio',
  meta: [
    { name: 'description', content: 'Learn more about my skills, experience, and background' }
  ]
})
</script>
