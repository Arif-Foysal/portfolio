<script setup lang="ts">
const posts = ref([
  {
    title: 'Finalist – National Project Showcase, UIU CSE Fest',
    description: 'Selected as a finalist in the national-level project showcase at UIU CSE Fest — recognized among top student innovators for presenting a solution-driven tech project demonstrating strong concept, execution and real-world relevance.',
    image: 'https://nuxt.com/assets/blog/nuxt-icon/cover.png',
    date: '2024-11-25',
    ui: {
      title: 'text-2xl sm:text-3xl font-bold'
    }
  },
  {
    title: 'Nuxt 3.14',
    description: 'Nuxt 3.14 is out!',
    image: 'https://nuxt.com/assets/blog/v3.14.png',
    date: '2024-11-04',
    ui: {
      title: 'text-2xl sm:text-3xl font-bold'
    }
  },
  {
    title: 'Nuxt 3.13',
    description: 'Nuxt 3.13 is out!',
    image: 'https://nuxt.com/assets/blog/v3.13.png',
    date: '2024-08-22',
    ui: {
      title: 'text-2xl sm:text-3xl font-bold'
    }
  }
])
</script>

<template>
  <UBlogPosts 
    orientation="vertical" 
    :posts="posts" 
  />
</template>
