<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup>
// Add this to debug - check browser console
if (process.client) {
  const colorMode = useColorMode()
  watch(() => colorMode.value, (newMode) => {
    console.log('Color mode changed to:', newMode)
    console.log('HTML classes:', document.documentElement.className)
  }, { immediate: true })
}
</script>

<style>
.page-enter-active,
.page-leave-active {
  transition: all 0.4s;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
  filter: blur(1rem);
}
</style>