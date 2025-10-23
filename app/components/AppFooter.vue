<template>

  <footer class="bg-gray-900 text-gray-300 dark:bg-gray-950 py-12 px-6">
    <div class="max-w-7xl mx-auto">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
        <!-- Solutions Column -->
        <div>
          <h3 class="text-lg font-medium text-white mb-4">Projects</h3>
          <ul class="space-y-3">
            <li><a href="/projects" class="text-gray-400 hover:text-white transition">Portfolio</a></li>
            <li><a href="/projects/case-studies" class="text-gray-400 hover:text-white transition">Case studies</a></li>
            <li><a href="/projects/apis" class="text-gray-400 hover:text-white transition">APIs & services</a></li>
            <li><a href="/projects/libraries" class="text-gray-400 hover:text-white transition">Libraries & tooling</a></li>
            <li><a href="/projects/cli" class="text-gray-400 hover:text-white transition">CLI tools</a></li>
          </ul>
        </div>

        <!-- Open Source Column -->
        <div>
          <h3 class="text-lg font-medium text-white mb-4">Open Source</h3>
          <ul class="space-y-3">
            <li>
              <a href="https://github.com/arif" target="_blank" rel="noopener noreferrer" class="text-gray-400 hover:text-white transition">
            GitHub profile
              </a>
            </li>
            <li><a href="/opensource/contributions" class="text-gray-400 hover:text-white transition">Contributions</a></li>
            <li><a href="/opensource/stars" class="text-gray-400 hover:text-white transition">Starred projects</a></li>
            <li><a href="/packages" class="text-gray-400 hover:text-white transition">Published packages</a></li>
          </ul>
        </div>

        <!-- Resources Column -->
        <div>
          <h3 class="text-lg font-medium text-white mb-4">Resources</h3>
          <ul class="space-y-3">
            <li><a href="/blog" class="text-gray-400 hover:text-white transition">Blog & posts</a></li>
            <li><a href="/tutorials" class="text-gray-400 hover:text-white transition">Tutorials</a></li>
            <li><a href="/talks" class="text-gray-400 hover:text-white transition">Talks & slides</a></li>
            <li><a href="/notes" class="text-gray-400 hover:text-white transition">Architecture notes</a></li>
          </ul>
        </div>

        <!-- About Column -->
        <div>
          <h3 class="text-lg font-medium text-white mb-4">About</h3>
          <ul class="space-y-3">
            <li><a href="/about" class="text-gray-400 hover:text-white transition">About me</a></li>
            <li><a href="/resume.pdf" class="text-gray-400 hover:text-white transition" target="_blank" rel="noopener noreferrer">Resume</a></li>
            <li><a href="/speaking" class="text-gray-400 hover:text-white transition">Speaking & workshops</a></li>
            <li><a href="mailto:hello@example.com" class="text-gray-400 hover:text-white transition">Hire / contact</a></li>
          </ul>
        </div>

        <!-- Newsletter Column -->
        <div class="md:col-span-2 lg:col-span-1">
          <h3 class="text-lg font-medium text-white mb-4">Subscribe to my newsletter</h3>
          <p class="text-sm text-gray-400 mb-4">
            Hey, I’m sharing what I learn while building and experimenting with intelligent systems.
Subscribe if you want simple, practical, and inspiring tech content in your inbox.
          </p>
          <form @submit.prevent="subscribe" class="space-y-3">
            <div>
              <label for="email" class="sr-only">Email address</label>
              <input
            id="email"
            v-model="email"
            type="email"
            required
            class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-300"
            placeholder="you@company.com"
              />
            </div>
            <button
              type="submit"
              class="w-full px-4 py-2 bg-indigo-600 hover:bg-indigo-700 transition text-white font-medium rounded-md"
            >
              Subscribe
            </button>
          </form>
        </div>
      </div>

      <div class="mt-12 pt-8 border-t border-gray-800">
        <div class="flex flex-col md:flex-row justify-between items-center gap-4">
          <p class="text-gray-500 text-lg">
            © {{ new Date().getFullYear() }} Arif Foysal. All rights reserved.
          </p>
          <div class="flex space-x-4">
            <ContactIcons />
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { Icon } from "@iconify/vue";

const email = ref("");

function subscribe() {
  // Implement subscription logic here
  alert(`Subscribed with email: ${email.value}`);
  email.value = "";
}
</script>
