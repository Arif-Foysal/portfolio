<script setup lang="ts">

import { HaloSearch } from '~/components/ui/halo-search'

</script>

<template>
  <div class="w-full flex flex-col items-center justify-center h-96 relative z-0">

    <HaloSearch class=""/>

    <span class="mt-24 text-muted-foreground font-light">
      Try hovering over component and typing in it.
    </span>
  </div>
</template>