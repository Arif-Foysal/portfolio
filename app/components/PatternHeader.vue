<script setup lang="ts">
const props = defineProps<{
  title: string,
  description?: string
}>()

</script>

<template>
  <UPageCard variant="subtle">
    <div class="relative overflow-hidden rounded-sm border border-dashed border-accented p-2 flex items-center justify-center">
      <svg class="absolute inset-0 h-full w-full stroke-inverted/10 opacity-75" fill="none">
        <defs>
          <pattern
            id="pattern-5c1e4f0e-62d5-498b-8ff0-cf77bb448c8e"
            x="0"
            y="0"
            width="10"
            height="10"
            patternUnits="userSpaceOnUse"
          >
            <path d="M-3 13 15-5M-5 5l18-18M-1 21 17 3" />
          </pattern>
        </defs>
        <rect
          stroke="none"
          fill="url(#pattern-5c1e4f0e-62d5-498b-8ff0-cf77bb448c8e)"
          width="100%"
          height="100%"
        />
      </svg>

      <!-- Add your centered text here -->
      <div class="relative z-500 text-center pt-4 pb-4">
        <h1 class="text-3xl md:text-5xl text-gray-950 dark:text-white  font-bold ">{{ props.title }}</h1>
        <p class="text-lg text-gray-600 dark:text-white/80">{{ props.description }}</p>
         <!-- <UPageSection :title="title" :description="description"></UPageSection> -->
      </div>
    </div>

  </UPageCard>
  <!-- <h1 class="text-5xl font-bold text-red-500 drop-shadow-lg">Tech I love working with</h1> -->
</template>