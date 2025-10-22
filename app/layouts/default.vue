<template>
  <ColorScheme>
    <div class="min-h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100">
      <AppHeader />
      <div class="h-screen w-full md:pl-6 md:pr-6 
           bg-[image:repeating-linear-gradient(315deg,var(--pattern-fg)_0,var(--pattern-fg)_1px,transparent_0,transparent_50%)] 
           bg-[size:10px_10px] bg-fixed 
           [--pattern-fg:#e5e7eb] dark:[--pattern-fg:#374151]">
          <slot />
      </div>
      <AppFooter />
    </div>
  </ColorScheme>
</template>
