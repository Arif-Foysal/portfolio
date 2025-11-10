<script setup lang="ts">

const publications = ref([
  {
    title: 'TritonZ: A Remotely Operated Underwater Rover with Manipulator Arm for Exploration and Rescue Operations',
    description: '27th International Conference on Computer and Information Technology (ICCIT) 2024 - Accepted Paper. This paper presents the design and implementation of TritonZ, a remotely operated underwater rover equipped with a manipulator arm, developed for underwater exploration and rescue missions. The rover integrates advanced navigation systems, real-time video streaming, and precise control mechanisms to enhance operational efficiency in challenging aquatic environments.',
    image: '/publications/tritonz.png',
    date: '2024-12-20',
    ui: {
      title: 'text-2xl sm:text-3xl font-bold'
    }
  },
])


</script>


<template>
        <PatternHeader title="Publications" />
    <br><br>
        <UBlogPosts 
 
    orientation="vertical" 
    :posts="publications" 
    class="max-w-7xl  mx-auto "
    />

</template>