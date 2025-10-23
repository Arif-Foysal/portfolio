<script setup lang="ts">

import { CardSpotlight } from '~/components/ui/card-spotlight'

</script>

<template>
  <div class="flex h-[200px] w-full flex-col gap-2 sm:h-[250px] md:h-[300px] lg:h-[250px] lg:flex-row">
    <CardSpotlight
      class="cursor-pointer flex-col items-center justify-center whitespace-nowrap text-2xl sm:text-3xl md:text-4xl lg:text-5xl shadow-2xl p-4 sm:p-6 md:p-8 [--gradient-color:#C9C9C9] dark:[--gradient-color:#363636]"
      :gradient-color="'var(--gradient-color)'"
    >
      This is a header card that glows when hovered over.
    </CardSpotlight>
  </div>
</template>