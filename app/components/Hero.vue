<script setup lang="ts">
import ContactIcons from './ContactIcons.vue';

const links = ref([
  {
    label: 'Get started',
    to: '/docs/getting-started',
    icon: 'i-lucide-square-play'
  },
  {
    label: 'Learn more',
    to: '/docs/getting-started/theme/design-system',
    color: 'neutral',
    variant: 'subtle',
    trailingIcon: 'i-lucide-arrow-right'
  }
])
</script>

<template>
  <UPageHero
    title="Ultimate Vue UI library"
    description="A Nuxt/Vue-integrated UI library providing a rich set of fully-styled, accessible and highly customizable components for building modern web applications."
    headline="Welcome"
    orientation="horizontal"
    :links="links"
  >
    <!-- Default slot content -->
    <div>
      <p>This is a component</p>
      <img
        src="/profile.jpegd"
        alt="App screenshot"
        class="rounded-lg shadow-2xl ring ring-default"
      />
      <ContactIcons />
    </div>
  </UPageHero>
</template>
