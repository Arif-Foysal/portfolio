<template>
    <div class="">

 
  <ul
    class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 lg:gap-8 max-w-full px-4 md:px-12 "
  >
    <li
      v-for="item in gridItems"
      :key="item.title"
      class="min-h-56 list-none bg-white dark:bg-gray-950 rounded-3xl w-full "
    >
      <div class=" relative h-full border p-2 rounded-3xl md:p-3">
        <GlowingEffect
          :spread="40"
          :glow="true"
          :disabled="false"
          :proximity="64"
          :inactive-zone="0.01"
        />
        <div
          class="border-0.75 relative flex h-full flex-col gap-6 overflow-hidden rounded-xl p-6 md:p-6 dark:shadow-[0px_0px_27px_0px_#2D2D2D]"
        >
          <div class="relative flex flex-1 flex-col gap-4">
            <h3 class="text-2xl font-medium text-black dark:text-white md:text-3xl">
              {{ item.title }}
            </h3>
            <div class="grid grid-cols-3 sm:grid-cols-4 gap-4 sm:gap-6">
              <div v-for="tech in item.technologies" :key="tech.name" 
                class="flex flex-col items-center gap-2 group hover:scale-110 transition-transform duration-200"
              >
                <Icon
                  :icon="tech.icon"
                  class="h-8 w-8 sm:h-10 sm:w-10 text-gray-700 dark:text-gray-300"
                />
                <span class="text-xs sm:text-sm text-center text-gray-600 dark:text-gray-400">
                  {{ tech.name }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </li>
  </ul>
     </div>
</template>

<script lang="ts" setup>
import { cn } from "@/lib/utils";
import { GlowingEffect } from "~/components/ui/glowing-effect";
import { Icon } from '@iconify/vue'

interface Technology {
  name: string;
  icon: string;
}

interface GridItem {
  title: string;
  technologies: Technology[];
}

const gridItems: GridItem[] = [
  {
    title: "Front End",
    technologies: [
      { name: "React", icon: "devicon:react" },
      { name: "Vue", icon: "devicon:vuejs" },
      { name: "Next.js", icon: "devicon:nextjs" },
      { name: "Nuxt", icon: "devicon:nuxtjs" },
      { name: "TailwindCSS", icon: "devicon:tailwindcss" },
      { name: "TypeScript", icon: "devicon:typescript" },
      { name: "JavaScript", icon: "devicon:javascript" },
      { name: "HTML5", icon: "devicon:html5" },
    ]
  },
  {
    title: "Back End",
    technologies: [
        { name: "Python", icon: "devicon:python" },
        { name: "Django", icon: "logos:django-icon" },
        { name: "FastAPI", icon: "devicon:fastapi" },
        { name: "PHP", icon: "material-icon-theme:php" },
        {name: "Laravel", icon: "devicon:laravel" },
      { name: "Node.js", icon: "devicon:nodejs" },
      { name: "Express", icon: "skill-icons:expressjs-light" },
      { name: "NestJS", icon: "devicon:nestjs" },
      { name: "GraphQL", icon: "logos:graphql" },
      { name: "REST", icon: "simple-icons:openapiinitiative" },
    ]
  },
  {
    title: "Database",
    technologies: [
      { name: "PostgreSQL", icon: "devicon:postgresql" },
      { name: "MongoDB", icon: "devicon:mongodb" },
      { name: "Redis", icon: "devicon:redis" },
      { name: "Prisma", icon: "simple-icons:prisma" },
      { name: "MySQL", icon: "devicon:mysql" },
      { name: "SQLite", icon: "devicon:sqlite" },
      { name: "Supabase", icon: "simple-icons:supabase" },
      { name: "Firebase", icon: "devicon:firebase" },
    ]
  },
  {
    title: "DevOps",
    technologies: [
      { name: "Docker", icon: "devicon:docker" },
      { name: "Kubernetes", icon: "devicon:kubernetes" },
      { name: "AWS", icon: "devicon:amazonwebservices" },
      { name: "GitHub", icon: "mdi:github" },
      { name: "GitLab", icon: "devicon:gitlab" },
      { name: "Jenkins", icon: "devicon:jenkins" },
      { name: "Nginx", icon: "devicon:nginx" },
      { name: "Linux", icon: "devicon:linux" },
    ]
  },
  {
    title: "Generative AI",
    technologies: [
      { name: "TensorFlow", icon: "devicon:tensorflow" },
      { name: "PyTorch", icon: "devicon:pytorch" },
      { name: "Langchain", icon: "simple-icons:langchain" },
      { name: "OpenAI", icon: "simple-icons:openai" },
      { name: "Hugging Face", icon: "simple-icons:huggingface" },
      { name: "scikit-learn", icon: "devicon:scikit" },
      { name: "CUDA", icon: "simple-icons:nvidia" },
      { name: "Jupyter", icon: "devicon:jupyter" },
    ]
  },
  {
    title: "Tools & Others",
    technologies: [
      { name: "Git", icon: "devicon:git" },
      { name: "VS Code", icon: "devicon:vscode" },
      { name: "Postman", icon: "devicon:postman" },
      { name: "Arduino", icon: "devicon:arduino" },
      { name: "Vim", icon: "devicon:vim" },
      { name: "Bash", icon: "logos:bash-icon" },
      { name: "WebAssembly", icon: "simple-icons:webassembly" },
      { name: "WebRTC", icon: "simple-icons:webrtc" },
    ]
  },
];
</script>