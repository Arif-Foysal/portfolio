<script setup lang="ts">
import { RadiantText } from '~/components/ui/radiant-text'
import { InteractiveHoverButton } from '~/components/ui/interactive-hover-button'
</script>
<template>


        <div class="flex flex-col items-center justify-center gap-6">
    <RadiantText
    class="inline-flex items-center justify-center px-4 py-1 transition ease-out hover:text-neutral-600 hover:duration-300 hover:dark:text-neutral-400"
    :duration="5"
    >
    <span class="text-3xl font-bold">✨ Introducing Inspira UI</span>
</RadiantText>
<InteractiveHoverButton />
</div>

</template>
