<script setup lang="ts">
const posts = ref([
  {
    title: 'Finalist – National Project Showcase, UIU CSE Fest',
    description: 'Selected as a finalist in the national-level project showcase at UIU CSE Fest — recognized among top student innovators for presenting a solution-driven tech project demonstrating strong concept, execution and real-world relevance.',
    image: '/projectshow.jpg',
    date: '2024-11-25',
    ui: {
      title: 'text-2xl sm:text-3xl font-bold'
    }
  },
  {
    title: 'Champion - UIU CSE Project Show, Fall 2023',
    description: 'Nuxt 3.13 is out!',
    image: '/projects/blue-horizon/award.jpg',
    date: '2024-11-04',
    ui: {
      title: 'text-2xl sm:text-3xl font-bold'
    }
  },
  {
    title: 'Finalist - National Project Showcase, Inventious 4.1, MIST',
    description: 'Nuxt 3.13 is out!',
    image: '/certs/inventious.png',
    date: '2024-08-22',
    ui: {
      title: 'text-2xl sm:text-3xl font-bold'
    }
  },
    {
    title: 'Finalist - National Project Showcase, Hult Prize Bangladesh 2025',
    description: 'Nuxt 3.13 is out!',
    image: '/hult2.jpg',
    date: '2024-08-22',
    ui: {
      title: 'text-2xl sm:text-3xl font-bold'
    }
  },
      {
    title: 'Google IT Support Professional Certificate',
    description: 'Nuxt 3.13 is out!',
    image: '/certs/os&u.jpg',
    date: '2024-08-22',
    ui: {
      title: 'text-2xl sm:text-3xl font-bold'
    }
  }
])
</script>

<template>
        <PatternHeader title="Achievements" />
      <br> <br>

    <UBlogPosts 
 
    orientation="vertical" 
    :posts="posts" 
    class="max-w-7xl  mx-auto "
    />
 
</template>