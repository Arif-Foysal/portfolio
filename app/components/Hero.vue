<template>
    <div>
        <!-- <ContactIcons /> -->
<br>
        <section class="relative bg-white dark:bg-gray-950 rounded-2xl [--particle-color:#000] dark:[--particle-color:#FFF]">
            <!-- Pattern background absolutely positioned behind content -->
            <ParticlesBg class="absolute inset-0" :quantity="100" :ease="100" :color="'var(--particle-color)'"
                :staticity="10" refresh />


            <!-- Grid container for responsive layout -->
            <div
                class="relative z-10 grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-center px-6 sm:px-8 lg:px-16 py-12 lg:py-20 max-w-7xl mx-auto">
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
      placeholder="Ask me anything..."
      container-class="w-full max-w-sm"
    ></IInput>
    <!-- <Button>
            <span class="inline-flex items-center gap-2">
                <Icon icon="fluent:send-20-filled" width="30" height="30" />
                Chat Now
            </span>
    </Button> -->
 
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
                        <ContactIcons />

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
                            <img src="/profile.jpeg" alt="Portfolio profile" class="w-full h-auto object-cover" />
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
import { Button } from "@/components/ui/button"
import { Icon } from '@iconify/vue'

import { IInput } from '~/components/ui/input'
const chatMessage = ref('')
const showNotification = ref(false)
const notificationMessage = ref('Chat with me! Ask me anything about my work or projects.')

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
