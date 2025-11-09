<script setup lang="ts">
import PromptInput from '~/components/PromptInput.vue'
import TextGen from '~/components/TextGen.vue'
import { Icon } from '@iconify/vue'
import { ref } from 'vue';
import Publications from '~/components/Publications.vue';


interface Technology {
  name: string;
  icon: string;
  iconClass?: string;
}

interface SkillItem {
  title: string;
  technologies: Technology[];
}

const skillsData: SkillItem[] = [
  {
    title: "Front End",
    technologies: [
      { name: "Vue", icon: "devicon:vuejs" },
      { name: "Nuxt", icon: "devicon:nuxtjs" },
      { name: "React", icon: "devicon:react" },
      { name: "Next.js", icon: "devicon:nextjs" },
      { name: "Vite", icon: "vscode-icons:file-type-vite" },
      { name: "Shadcn", icon: "simple-icons:shadcnui" },
      { name: "Svelte", icon: "vscode-icons:file-type-svelte" },
      { name: "Streamlit", icon: "logos:streamlit" },
      { name: "TailwindCSS", icon: "devicon:tailwindcss" },
      { name: "TypeScript", icon: "devicon:typescript" },
      { name: "JavaScript", icon: "devicon:javascript" },
      // { name: "HTML5", icon: "devicon:html5" },
      { name: "Markdown", icon: "fa7-brands:markdown" }
    ]
  },
  {
    title: "Back End",
    technologies: [
      { name: "Python", icon: "devicon:python" },
      { name: "Django", icon: "logos:django-icon" },
      { name: "FastAPI", icon: "devicon:fastapi" },
      { name: "Flask", icon: "file-icons:flask" },
      { name: "Next.js", icon: "devicon:nextjs" },
      { name: "Nuxt", icon: "devicon:nuxtjs" },
      { name: "PHP", icon: "material-icon-theme:php" },
      { name: "Laravel", icon: "devicon:laravel" },
      { name: "Express", icon: "skill-icons:expressjs-light" },
      { name: "GraphQL", icon: "logos:graphql" },
      { name: "REST", icon: "simple-icons:openapiinitiative" },
    ]
  },
  {
    title: "Mobile Development",
    technologies: [
      { name: "React Native", icon: "devicon:reactnative" },
      { name: "NestJs", icon: "devicon:nestjs" },
      { name: "Appwrite", icon: "devicon:appwrite" },
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
      { name: "Supabase", icon: "devicon:supabase" },
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
      { name: "Langchain", icon: "simple-icons:langchain", iconClass: "text-teal-600" },
      { name: "OpenAI", icon: "simple-icons:openai" },
      { name: "Hugging Face", icon: "logos:hugging-face-icon" },
      { name: "scikit-learn", icon: "skill-icons:scikitlearn-light" },
      { name: "CUDA", icon: "vscode-icons:file-type-cuda" },
      { name: "Jupyter", icon: "devicon:jupyter" },
    ]
  },
  {
    title: "Testing",
    technologies: [
      { name: "Postman", icon: "devicon:postman" },
      { name: "Curl", icon: "simple-icons:curl" },
      { name: "Swagger", icon: "devicon:swagger" },
      { name: "Pytest", icon: "vscode-icons:file-type-pytest" },
    ]
  },
  {
    title: "Tools & Others",
    technologies: [
      { name: "Git", icon: "devicon:git" },
      { name: "VS Code", icon: "devicon:vscode" },
      { name: "Micro Python", icon: "simple-icons:micropython", iconClass: "text-green-500" },
      { name: "Arduino", icon: "devicon:arduino" },
      { name: "Vim", icon: "devicon:vim" },
      { name: "Bash", icon: "logos:bash-icon" },
      { name: "WebRTC", icon: "simple-icons:webrtc" },
    ]
  },
];

const Projectlinks = ref([
  {
    label: 'Live Demo',
    to: '/docs/getting-started',
    icon: 'i-lucide-square-play',
    color: 'neutral'
  },
])


const { data: page } = await useAsyncData('index-page', () => queryCollection('index').first())

const title = page.value?.seo?.title || page.value?.title
const description = page.value?.seo?.description || page.value?.description

useSeoMeta({
  titleTemplate: '',
  title,
  ogTitle: title,
  description,
  ogDescription: description
})
</script>

<template>
  <div class="" v-if="page">

    <UPageHero :title="page.title" :links="page.hero.links" headline="Welcome"
      orientation="horizontal">
      <template #top>
        <HeroBackground />
      </template>
      <template #title>
        <MDC :value="page.title" unwrap="p" class="leading-tight" />
        
        <p class="mt-2 text-4xl md:text-5xl font-medium leading-tight">AI and Software Engineer</p>
      </template>
      <template #description>
        <TextGen
          :byWord="true"
          wordEffect="fade"
          :text="page.description"
          :revealMs="150"
          :stagger="30"
          :showShimmer="false"
          :autoStart="true"
          class="text-lg leading-relaxed"
        />
      </template>
      <img src="/profile.jpeg" alt="App screenshot" class="rounded-lg glowing-shadow" />

      <template #links>
        <div class="flex flex-col justify-center items-center gap-8 w-full">
          <PromptInput />
          <SocialIcons />
        </div>
      </template>
      <LazyStarsBg />
    </UPageHero>
    <!-- <br> -->

<!-- make it seperate component -->
    <div>
      <PatternHeader :title="page.features.title" />
    </div>
    <UPageSection>
      <div class="relative grid grid-cols-1 xl:grid-cols-2 gap-8">
        <UPageCard v-for="item in skillsData" :key="item.title" :title="item.title" spotlight
          spotlight-color="secondary" :ui="{
            root: 'ring-2 before:-inset-[2px]', // or ring-4, ring-8 for even thicker borders
            title: 'text-xl sm:text-2xl lg:text-3xl font-medium text-highlighted'
          }">
          <div class="grid grid-cols-3 sm:grid-cols-4 gap-4 sm:gap-6">
            <div v-for="tech in item.technologies" :key="tech.name"
              class="flex flex-col items-center gap-2 group hover:scale-110 transition-transform duration-200">
              <Icon :icon="tech.icon" :class="[
                'h-8 w-8 sm:h-10 sm:w-10',
                tech.iconClass || ''
              ]" />
              <span class="text-md sm:text-xl text-center">
                {{ tech.name }}
              </span>
            </div>
          </div>
        </UPageCard>
      </div>
    </UPageSection>


      <!-- Publications Section -->
      <Projects :sections="page.sections" />
      <br><br>
      <Achievements/>
      <br><br>
      
      <Publications />
      <br><br>

      <Education />
      <br><br>  

      <Cta :cta="page.cta" />

  </div>
</template>
