<script setup lang="ts">
interface ProjectSection {
  title: string
  description: string
  orientation?: string
  reverse?: boolean
  links?: any[]
  features?: any[]
  badges?: Array<{ icon: string; label: string }>
  video?: {
    src: string
    poster: string
    description: string
    duration: string
    uploadDate: string
  }
}

defineProps<{
  sections: ProjectSection[]
}>()
</script>
<template>

    <section class="">

      <div>
        <PatternHeader title="Projects I've built" />
      </div>


      <br> <br>


      <!-- Projects section -->
      <USeparator color="secondary" type="solid" size="sm" />
      <div v-for="(section, index) in sections" :key="index" class="text-secondary">
        <UPageSection :title="section.title" :description="section.description" :orientation="section.orientation"
          :reverse="section.reverse" :links="section.links" :features="section.features"
          :ui="{ container: ' md:border-l-2 md:border-r-2 border-secondary cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-900 ' }">
          <template #title>
            <section class="flex flex-col gap-4">
              <h2 class=" text-3xl sm:text-4xl lg:text-5xl text-pretty tracking-tight font-bold text-highlighted">
                {{ section.title }}
              </h2>
              <div class="flex gap-2 flex-wrap">
                <UBadge v-for="(badge, i) in section.badges" :key="i" :icon="badge.icon" size="lg" color="neutral"
                  variant="subtle" class="tracking-wider">
                  {{ badge.label }}
                </UBadge>
              </div>
            </section>
          </template>

          <div class="mt-6 w-full">
            <ProjectVideo
              v-if="section.video"
              :video-src="section.video.src"
              :poster-src="section.video.poster"
              :alt="`${section.title} demo video`"
              :title="section.title"
              :description="section.video.description"
              :duration="section.video.duration"
              :upload-date="section.video.uploadDate"
              :thumbnail-url="section.video.poster"
              class="glowing-shadow"
            />
            <img 
              v-else
              src="/projects/blue-horizon/main.jpg" 
              :alt="section.title + ' screenshot'"
              class="w-full max-h-[500px] object-cover rounded-xl shadow-md hover:scale-[1.02] transition-transform duration-300"
              loading="lazy" 
            />
          </div>
        </UPageSection>

        <!-- divider after each section (omit after last to avoid duplicate separators) -->
        <!-- <hr class="border-secondary" /> -->
        <USeparator color="secondary" type="solid" size="sm" />
      </div>
      <br> <br>


 


      <br> <br>
    </section>

</template>