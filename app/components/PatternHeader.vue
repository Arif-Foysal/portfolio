<script setup lang="ts">
const props = defineProps<{
  title: string,
  description?: string
}>()

</script>

<template>
  <!-- replaced UPageCard with a plain container to remove the automatic card border/margin -->

   <br>
  <!-- keep the rounded, colored card look but remove any visible border -->
  <div class="m-0 p-0 text-primary bg-white dark:bg-slate-900/60">
    <hr>
  <div class="relative overflow-hidden p-6 flex items-center justify-center w-full ">
      <!-- kept SVG pattern and removed the dashed border so only the pattern + text show -->
  <svg class="absolute inset-0 h-full w-full stroke-inverted/10 dark:stroke-white/10 opacity-75" fill="none">
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
      <div class="relative z-10 text-center py-4">
        <h1 class="text-3xl md:text-5xl text-gray-900 dark:text-white font-bold">{{ props.title }}</h1>
        <p class="text-lg text-gray-700 dark:text-white/80">{{ props.description }}</p>
         <!-- <UPageSection :title="title" :description="description"></UPageSection> -->
      </div>
    </div>
    <hr>
  </div>

</template>