<script setup lang="ts">
import { Dock, DockIcon, DockSeparator } from '~/components/ui/dock'
import { Icon } from '@iconify/vue'
</script>

<template>
  <div class="flex justify-center items-center w-full">
    <Dock class="mb-2 mt-2 scale-70 sm:scale-80 md:scale-100">
    <DockIcon class="gap-1 sm:gap-3">
      <Icon
        icon="mdi:github"
        class="size-10 "
      />
    </DockIcon>
    <DockSeparator class="mx-1 sm:mx-2" />
    <DockIcon class="gap-1 sm:gap-3">
      <Icon
        icon="logos:google-gmail"
        class="size-10 "
      />
    </DockIcon>

    <DockIcon class="gap-1 sm:gap-3">
      <Icon
        icon="logos:whatsapp-icon"
        class="size-10"
      />
    </DockIcon>
    <DockSeparator class="mx-1 sm:mx-2" />

    <DockIcon class="gap-1 sm:gap-3">
      <Icon
        icon="logos:linkedin-icon"
        class="size-10"
      />
    </DockIcon>
    <DockIcon class="gap-1 sm:gap-3">
      <Icon
        icon="logos:facebook"
        class="size-10 "
      />
    </DockIcon>

    <DockSeparator class="mx-1 sm:mx-2" />
    <DockIcon class="gap-1 sm:gap-3">
      <Icon
        icon="ri:threads-fill"
        class="size-10 text-black dark:text-white"
      />
    </DockIcon>
    <DockIcon class="gap-2 sm:gap-3">
      <Icon
        icon="ri:twitter-x-line"
        class="size-10 "
      />
    </DockIcon>
  </Dock>
  </div>
</template>