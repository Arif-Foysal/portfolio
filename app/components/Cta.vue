<script setup lang="ts">
interface CtaData {
  title?: string
  description?: string
  links?: any[]
  [key: string]: any
}

defineProps<{
  cta: CtaData
}>()
</script>
<template>
        <UPageCTA v-bind="cta" variant="naked" class="overflow-hidden">
      <LazyStarsBg />
    </UPageCTA>
</template>