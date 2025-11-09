<script setup lang="ts">
const versions = ref([
  {
    title: 'United International University',
    logo: '/uiu.png',
    description: 'Bachelor of Science in Computer Science and Engineering. Major in Software Engineering.',
    date: '2025-04-27',
    ui: {
      container: 'max-w-lg',
      title: 'text-2xl sm:text-3xl font-bold'
    }
  },
  {
    title: 'Police Lines School & College',
    logo: '/plscr.png',
    description: 'Higher Secondary Certificate (HSC) in Science Group.',
    date: '2018-03-07',
    ui: {
      container: 'max-w-lg',
      title: 'text-2xl sm:text-3xl font-bold'
    }
  },
  {
    title: 'Police Lines School & College',
    logo: '/plscr.png',
    description: 'Secondary School Certificate (SSC) in Science Group.',
    date: '2016-02-15',
    ui: {
      container: 'max-w-lg',
      title: 'text-2xl sm:text-3xl font-bold'
    }
  }
])
</script>

<template>
  <div class="">
    <PatternHeader title="Education" />
<br><br>
    <section class="max-w-7xl  mx-auto ">

         
    <UChangelogVersions :versions="versions">
      <template #title="{ version }">
        <div class="flex items-center gap-3">
          <img :src="version.logo" class="w-12" alt="Icon" />
          <span>{{ version.title }}</span>
        </div>
      </template>
    </UChangelogVersions>
     </section>
  </div>
  </template>
