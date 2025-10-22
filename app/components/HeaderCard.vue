<script setup lang="ts">

import { CardSpotlight } from '~/components/ui/card-spotlight'
import { computed } from "vue";
import { useColorMode } from "@vueuse/core";

const isDark = computed(() => useColorMode().value == "dark");
</script>

<template>
  <div class="flex h-[200px] w-full flex-col gap-2 sm:h-[250px] md:h-[300px] lg:h-[250px] lg:flex-row">
    <CardSpotlight
      class="cursor-pointer flex-col items-center justify-center whitespace-nowrap text-2xl sm:text-3xl md:text-4xl lg:text-5xl shadow-2xl p-4 sm:p-6 md:p-8"
      :gradient-color="isDark ? '#363636' : '#C9C9C9'"
    >
      Tools that I love working with
    </CardSpotlight>
  </div>
</template>