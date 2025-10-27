<script setup lang="ts">
import PromptInput from '~/components/PromptInput.vue'
import { Icon } from '@iconify/vue'

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
      { name: "React", icon: "devicon:react" },
      { name: "Svelte", icon: "vscode-icons:file-type-svelte" },
      { name: "Shadcn", icon: "vscode-icons:file-type-shadcn" },
      { name: "Nuxt", icon: "devicon:nuxtjs" },
      { name: "Next.js", icon: "devicon:nextjs" },
      { name: "TailwindCSS", icon: "devicon:tailwindcss" },
      { name: "Streamlit", icon: "logos:streamlit" },
      { name: "Vite", icon: "vscode-icons:file-type-vite" },
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
      { name: "WebAssembly", icon: "simple-icons:webassembly" },
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
  {
    label: 'Explore components',
    to: '/docs/components/app',
    color: 'neutral',
    variant: 'subtle',
    trailingIcon: 'i-lucide-arrow-right'
  }
])


const { data: page } = await useAsyncData('index', () => queryCollection('index').first())

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
    <!-- <UPageHero
      :title="page.title"
      :description="page.description"
      :links="page.hero.links"
    >
      <template #top>
        <HeroBackground />
      </template>

<template #title>
        <MDC
          :value="page.title"
          unwrap="p"
        />
      </template>

<PromotionalVideo />
</UPageHero> -->
    <UPageHero :title="page.title" :description="page.description" :links="page.hero.links" headline="Welcome"
      orientation="horizontal">
      <template #top>
        <HeroBackground />
      </template>
      <template #title>
        <MDC :value="page.title" unwrap="p" class="leading-tight" />
      </template>
      <img src="/profile.jpeg" alt="App screenshot" class="rounded-lg shadow-2xl ring ring-default" />
      <template #links>
        <PromptInput />
        <ContactIcons />
        <!-- <MyCTAs /> -->
      </template>
    </UPageHero>
<!-- <br> -->
 

    <div>
      <PatternHeader :title="page.features.title" />
    </div>
    <UPageSection>
      <div class="relative grid grid-cols-1 xl:grid-cols-2 gap-8">
        <UPageCard v-for="item in skillsData" :key="item.title" :title="item.title" spotlight 
            spotlight-color="secondary"
            
          :ui="{ title: 'text-xl sm:text-2xl lg:text-3xl font-medium text-highlighted' }">
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

    <section class="">

      <div >
        <PatternHeader title="Projects I've built" />
      </div>

  
<br> <br>


<!-- Projects section -->
      <div v-for="(section, index) in page.sections" :key="index" class="text-secondary">
        <hr />
        <UPageSection
          :title="section.title"
          :description="section.description"
          :orientation="section.orientation"
          :reverse="section.reverse"
          :links="Projectlinks"
          :features="section.features"
          :ui="{ container: 'border-l border-r border-secondary cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-900 ' }"
        >
          <template #title>
            <!-- title template (unchanged) -->
            <section class="flex flex-col gap-4">
              <h2 class=" text-3xl sm:text-4xl lg:text-5xl text-pretty tracking-tight font-bold text-highlighted">
                {{ section.title }}
              </h2>
              <div class="flex gap-2">
                <UBadge icon="devicon:javascript" size="xl" color="neutral" variant="subtle" class="tracking-wider">JavaScript</UBadge>
                <UBadge icon="devicon:react" size="xl" color="neutral" variant="subtle" class="tracking-wider">React</UBadge>
                <UBadge icon="devicon:vuejs" size="xl" color="neutral" variant="subtle" class="tracking-wider">Vue</UBadge>
                <UBadge icon="devicon:vuejs" size="xl" color="neutral" variant="subtle" class="tracking-wider">Vue</UBadge>
              </div>
            </section>
          </template>

          <div class="mt-6 w-full ">
            <img
              src="/profile.jpeg"
              :alt="section.title + ' screenshot'"
              class="w-full max-h-[500px] object-cover rounded-xl shadow-md hover:scale-[1.02] transition-transform duration-300"
              loading="lazy"
            />
          </div>
        </UPageSection>

        <!-- divider after each section (omit after last to avoid duplicate separators) -->
        <hr/>
      </div>
    </section>

    <UPageSection id="testimonials" :headline="page.testimonials.headline" :title="page.testimonials.title"
      :description="page.testimonials.description">
      <UPageColumns class="xl:columns-4">
        <UPageCard v-for="(testimonial, index) in page.testimonials.items" :key="index" variant="subtle"
          :description="testimonial.quote"
          :ui="{ description: 'before:content-[open-quote] after:content-[close-quote]' }">
          <template #footer>
            <UUser v-bind="testimonial.user" size="lg" />
          </template>
        </UPageCard>
      </UPageColumns>
    </UPageSection>

    <USeparator />

    <UPageCTA v-bind="page.cta" variant="naked" class="overflow-hidden">
      <LazyStarsBg />
    </UPageCTA>
  </div>
</template>
