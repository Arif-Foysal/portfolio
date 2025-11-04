<script setup lang="ts">

const route = useRoute()

const items = computed(() => [
{
  label: 'Home',
  to: '/',
  active: route.path === '/',
  icon: 'i-lucide-home'
},
{
  label: 'Chat',
  to: '/chat',
  active: route.path === '/chat',
  icon: 'i-lucide-bot'
},
{
  label: 'Docs',
  to: '/docs',
  active: route.path.startsWith('/docs'),
  icon: 'i-lucide-book-open'
}, 
{
  label: 'Blog',
  to: '/blog',
  icon: 'i-lucide-file-text'
}, 
// {
//   label: 'About',
//   to: '/about',
//   icon: 'i-lucide-user'
// }, 
])
</script>

<template>
  <UHeader class="items-center">
    <template #left>
      <NuxtLink to="/">
        <!-- <AppLogo class=" h-6" /> -->
         
        <h1 class="text-3xl">Arif Foysal</h1>
      </NuxtLink>
      <!-- <TemplateMenu /> -->
    </template>

    <UNavigationMenu
      :items="items"
      variant="pill"
    />

    <template #right>
      <UColorModeButton />

      <UButton
        icon="i-lucide-log-in"
        color="neutral"
        variant="ghost"
        to="/login"
        class="lg:hidden"
      />

      <UButton
        label="Sign in"
        color="neutral"
        variant="outline"
        to="/login"
        class="hidden lg:inline-flex"
      />

      <UButton
        label="Sign up"
        color="neutral"
        trailing-icon="i-lucide-arrow-right"
        class="hidden lg:inline-flex"
        to="/signup"
      />
    </template>

    <template #body>
      <UNavigationMenu
        :items="items"
        orientation="vertical"
        class="-mx-2.5"
      />

      <USeparator class="my-6" />

      <UButton
        label="Sign in"
        color="neutral"
        variant="subtle"
        to="/login"
        block
        class="mb-3"
      />
      <UButton
        label="Sign up"
        color="neutral"
        to="/signup"
        block
      />
    </template>
  </UHeader>
</template>
