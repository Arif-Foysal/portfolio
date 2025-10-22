<template>
    <div>
        <ContactIcons />
        <section class="relative bg-white dark:bg-gray-950">
            <!-- Pattern background absolutely positioned behind content -->
            <ParticlesBg class="absolute inset-0" :quantity="100" :ease="100" :color="isDark ? '#FFF' : '#000'"
                :staticity="10" refresh />


            <!-- Grid container for responsive layout -->
            <div
                class="relative z-10 grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-center px-6 sm:px-8 lg:px-16 py-12 lg:py-20 max-w-8xl mx-auto">
                <!-- Left Content Section -->
                <div class="flex flex-col justify-center space-y-8">
                    <!-- Content (above pattern) -->
                    <div class="relative z-10 space-y-8">
                        <!-- Greeting -->
                        <div class="space-y-4">
                            <p class="text-sm font-semibold text-blue-400 tracking-widest uppercase">Welcome</p>
                            <h1 class="text-5xl sm:text-6xl lg:text-7xl font-bold leading-tight text-balance">
                                Hey, I'm <span
                                    class="pointer-events-none whitespace-pre-wrap bg-linear-to-r from-blue-400 to-cyan-400/80 bg-clip-text text-center leading-none text-transparent">Arif
                                    Foysal</span>

                            </h1>
                        </div>

                        <!-- Subtitle -->
                        <div class="space-y-4">
                            <h2 class="text-2xl sm:text-3xl font-semibold text-slate-900 dark:text-slate-200">
                                AI & Software Engineer
                            </h2>
                            <p class="text-lg text-slate-400 leading-relaxed max-w-md">
                                I help startups scale their business with intelligent software solutions. From
                                AI-powered features to full-stack development, I turn ideas into reality.
                            </p>
                        </div>

                        <!-- Chat Input Section -->
                        <div class="pt-4 space-y-3">
                            <RadiantText
                                class="inline-flex items-center justify-center px-4 py-1 transition ease-out hover:text-neutral-600 hover:duration-300 hover:dark:text-neutral-400"
                                :duration="10">
                                <label class="text-2xl font-bold">
                                    ✨ Chat with my second brain 🧠</label>
                            </RadiantText>
                            <div class="flex gap-2">


                                <!-- <input v-model="chatMessage" type="text" placeholder="Ask me anything..."
                                    @keyup.enter="sendMessage"
                                    class="flex-1 px-4 py-3 rounded-lg bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-gray-700 dark:text-white placeholder-slate-500 focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-400/20 transition-all" /> -->
                                    <IInput
      id="inputDemo"
      placeholder="Hover over me"
      container-class="w-full max-w-sm"
    ></IInput>
                                <InteractiveHoverButton />
                                <!-- <button @click="sendMessage" :disabled="!chatMessage.trim()"
                                    class="px-6 py-3 rounded-lg bg-linear-to-r from-blue-500 to-cyan-500 text-white font-semibold hover:from-blue-600 hover:to-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center gap-2">
                                    <span class="hidden sm:inline">Send</span>
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M13 10V3L4 14h7v7l9-11h-7z" />
                                    </svg>
                                </button> -->
                            </div>
                        </div>

                        <!-- Social Links -->
                        <div class="flex gap-4 pt-4">
                            <a href="#" class="p-3 rounded-lg bg-slate-800 hover:bg-slate-700 transition-colors">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path
                                        d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v 3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                                </svg>
                            </a>
                            <a href="#" class="p-3 rounded-lg bg-slate-800 hover:bg-slate-700 transition-colors">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path
                                        d="M20.447 20.452h-3.554v-5.569c0-1.328-.475-2.236-1.986-2.236-1.081 0-1.722.722-2.004 1.418-.103.249-.129.597-.129.946v5.441h-3.554s.05-8.736 0-9.646h3.554v1.348c.42-.648 1.36-1.573 3.322-1.573 2.429 0 4.251 1.574 4.251 4.963v5.908zM5.337 8.855c-1.144 0-1.915-.762-1.915-1.715 0-.957.77-1.715 1.958-1.715 1.187 0 1.927.758 1.927 1.715 0 .953-.74 1.715-1.97 1.715zm1.946 11.597H3.392V9.806h3.891v10.646zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.225 0z" />
                                </svg>
                            </a>
                            <a href="#" class="p-3 rounded-lg bg-slate-800 hover:bg-slate-700 transition-colors">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path
                                        d="M23.953 4.57a10 10 0 002.856-3.51 10.02 10.02 0 01-2.856 1.1 4.96 4.96 0 002.165-2.724c-.951.564-2.005.974-3.127 1.195a4.948 4.948 0 00-8.506 4.513A14.025 14.025 0 011.671 3.149a4.93 4.93 0 001.523 6.574 4.903 4.903 0 01-2.229-.616c-.054 2.281 1.581 4.415 3.949 4.89a4.935 4.935 0 01-2.224.084 4.928 4.928 0 004.6 3.419A9.9 9.9 0 010 19.54a13.994 13.994 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z" />
                                </svg>
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Right Image Section -->
                <div class="flex justify-center lg:justify-end">
                    <div class="relative w-full max-w-md">
                        <!-- Decorative background elements -->
                        <div
                            class="absolute inset-0 bg-linear-to-br from-blue-500/20 to-cyan-500/20 rounded-2xl blur-3xl">
                        </div>

                        <!-- Image container -->
                        <div class="relative rounded-2xl overflow-hidden border border-slate-700 shadow-2xl">
                            <img src="/profile.png" alt="Portfolio profile" class="w-full h-auto object-cover" />
                            <!-- Overlay gradient -->
                            <div
                                class="absolute inset-0 bg-linear-to-t from-slate-950 via-transparent to-transparent opacity-40">
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Floating chat notification (optional) -->
            <transition name="fade">
                <div v-if="showNotification"
                    class="fixed bottom-6 right-6 bg-slate-800 border border-slate-700 rounded-lg p-4 shadow-lg max-w-xs z-50">
                    <p class="text-sm text-slate-300">{{ notificationMessage }}</p>
                </div>
            </transition>
        </section>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ParticlesBg from '~/components/ui/particles-bg/ParticlesBg.vue'
import { RadiantText } from '~/components/ui/radiant-text'
import { InteractiveHoverButton } from '~/components/ui/interactive-hover-button'

import { IInput } from '~/components/ui/input'
import { useColorMode } from "@vueuse/core"
import { computed } from 'vue'

const colorMode = useColorMode()
const isDark = computed(() => colorMode.value === "dark")

const chatMessage = ref('')
const showNotification = ref(false)
const notificationMessage = ref('')

const sendMessage = () => {
    if (!chatMessage.value.trim()) return

    notificationMessage.value = `Message sent: "${chatMessage.value}"`
    showNotification.value = true
    chatMessage.value = ''

    setTimeout(() => {
        showNotification.value = false
    }, 3000)
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
