<template>
  <header class=" backdrop-blur border-b border-gray-200 dark:border-gray-800 h-16 sticky top-0 z-50 transition-colors duration-200">
    <div class="flex items-center justify-between gap-3 h-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Left Section -->
      <div class="lg:flex-1 flex items-center gap-1.5">
        <slot name="left">
          <!-- Title/Logo -->
          <NuxtLink 
            :to="to" 
            class="shrink-0 font-bold text-3xl text-gray-900 dark:text-white flex items-end gap-1.5 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
          >
            <slot name="title">
              {{ title }}
            </slot>
          </NuxtLink>
        </slot>
      </div>

      <!-- Center Section (Desktop Navigation) -->
      <div class="hidden lg:flex">
        <slot name="default">
          <nav class="flex items-center space-x-8">
            <NuxtLink 
              v-for="item in navigationItems" 
              :key="item.label"
              :to="item.to"
              :target="item.target"
              class="text-lg font-medium transition-colors"
              :class="item.active 
                ? 'text-blue-600 dark:text-blue-400' 
                : 'text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400'"
            >
              {{ item.label }}
            </NuxtLink>
          </nav>
        </slot>
      </div>

      <!-- Right Section -->
      <div class="flex items-center justify-end lg:flex-1 gap-1.5">
        <slot name="right">
          <!-- Color Mode Toggle -->
          <button
            @click="toggleColorMode"
            class="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white transition-colors"
            aria-label="Toggle theme"
          >
            <svg v-if="isDarkMode" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>
        </slot>

        <!-- Mobile Menu Toggle -->
        <button
          @click="toggleMobileMenu"
          class="lg:hidden p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white transition-colors -me-1.5"
          aria-label="Toggle mobile menu"
        >
          <slot name="toggle">
            <svg v-if="!isMenuOpen" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </slot>
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-75 ease-in"
      leave-from-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-95 opacity-0"
    >
      <div v-if="isMenuOpen" class="lg:hidden border-t border-gray-200 dark:border-gray-800 bg-white/95 backdrop-blur">
        <slot name="body">
          <div class="p-4 sm:p-6 overflow-y-auto space-y-1">
            <NuxtLink 
              v-for="item in navigationItems" 
              :key="item.label"
              :to="item.to"
              :target="item.target"
              @click="closeMobileMenu"
              class="block px-3 py-2 rounded-lg text-base font-medium transition-colors"
              :class="item.active
                ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400'
                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white'"
            >
              {{ item.label }}
            </NuxtLink>
          </div>
        </slot>
      </div>
    </Transition>
  </header>
</template>

<script setup lang="ts">
interface NavigationMenuItem {
  label: string
  to: string
  target?: string
  active?: boolean
}

interface Props {
  title?: string
  to?: string
  navigationItems?: NavigationMenuItem[]
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Arif Foysal',
  to: '/',
  navigationItems: () => []
})

const route = useRoute()
const isMenuOpen = ref(false)

// Nuxt Color Mode + Tailwind (no manual DOM/localStorage)

import { useColorMode } from '#imports'
const colorMode = useColorMode()
const isDarkMode = computed(() => colorMode.value === 'dark')
const toggleColorMode = () => {
//   colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark';
  colorMode.preference = colorMode.preference === 'dark' ? 'light' : 'dark';
}

// Default navigation items if none provided
const defaultItems = computed<NavigationMenuItem[]>(() => [
  {
    label: 'Home',
    to: '/',
    active: route.path === '/'
  },
  {
    label: 'Chat',
    to: '/chat',
    active: route.path === '/chat'
  },
  {
    label: 'Docs',
    to: '/docs',
    active: route.path === '/docs'
  },
  {
    label: 'About',
    to: '/about',
    active: route.path === '/about'
  },
  {
    label: 'Projects',
    to: '/projects',
    active: route.path === '/projects'
  },
  {
    label: 'Contact',
    to: '/contact',
    active: route.path === '/contact'
  }
])

const navigationItems = computed(() => 
  props.navigationItems.length > 0 ? props.navigationItems : defaultItems.value
)

const toggleMobileMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMobileMenu = () => {
  isMenuOpen.value = false
}

watch(() => route.path, () => {
  closeMobileMenu()
})
</script>