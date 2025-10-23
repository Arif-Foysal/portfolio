<script setup lang="ts">

import { CardSpotlight } from '~/components/ui/card-spotlight'
import { computed } from "vue";
import { useColorMode } from "@vueuse/core";

</script>

<template>
  <div class="flex h-[500px] w-full flex-col gap-4 lg:h-[250px] lg:flex-row">
    <CardSpotlight
      class="cursor-pointer flex-col items-center justify-center whitespace-nowrap text-4xl shadow-2xl bg-[#C9C9C9] dark:bg-[#363636]"
    >
      Tools that I love work with
    </CardSpotlight>
  </div>
</template>