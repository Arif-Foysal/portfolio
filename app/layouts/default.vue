<template>
  <div >
    <AppHeader />


  <UMain>
    <slot />
  </UMain>


    <AppFooter v-if="$route.name !== 'chat'" />
  </div>
</template>
