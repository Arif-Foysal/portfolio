<script setup lang="ts"> 

import { GlowBorder } from '~/components/ui/glow-border'

</script>
<template>
  <div class="bg-white dark:bg-gray-950 rounded-lg relative h-[150px] md:h-[180px] lg:h-[200px] w-full overflow-hidden">
    <GlowBorder
      :color="['#A07CFE', '#FE8FB5', '#FFBE7B']"
      :border-radius="10"
    />
    <div class="h-full w-full flex items-center justify-center p-4 sm:p-6 md:p-8">
      <span
        class=" text-center text-3xl sm:text-4xl md:text-5xl lg:text-6xl  text-gray-900 dark:text-gray-200"
      >
        Tools I love working with
      </span>
    </div>
  </div>
</template>