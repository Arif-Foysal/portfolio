<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'

interface Props {
  videoSrc: string
  posterSrc: string
  alt: string
  title: string
  description?: string
  duration?: string // ISO 8601 duration format, e.g., "PT30S" for 30 seconds
  uploadDate?: string // ISO 8601 date, e.g., "2024-11-05"
  thumbnailUrl?: string
}

const props = defineProps<Props>()

const videoRef = ref<HTMLVideoElement | null>(null)
const isIntersecting = ref(false)
const hasLoaded = ref(false)

// Intersection Observer for auto-play/pause
let observer: IntersectionObserver | null = null

onMounted(() => {
  if (!videoRef.value) return

  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        isIntersecting.value = entry.isIntersecting
        
        if (entry.isIntersecting && hasLoaded.value && videoRef.value) {
          // Play when in viewport
          videoRef.value.play().catch(() => {
            // Silently handle autoplay restrictions
          })
        } else if (!entry.isIntersecting && videoRef.value) {
          // Pause when out of viewport
          videoRef.value.pause()
        }
      })
    },
    {
      threshold: 0.5, // Play when 50% visible
      rootMargin: '0px'
    }
  )

  observer.observe(videoRef.value)
})

onUnmounted(() => {
  if (observer && videoRef.value) {
    observer.unobserve(videoRef.value)
    observer.disconnect()
  }
})

// Handle video load event
const handleLoadedData = () => {
  hasLoaded.value = true
  if (isIntersecting.value && videoRef.value) {
    videoRef.value.play().catch(() => {
      // Silently handle autoplay restrictions
    })
  }
}

// Handle video error
const handleError = () => {
  // Silently handle video loading errors
  hasLoaded.value = false
}

// Generate JSON-LD structured data for SEO
const videoStructuredData = computed(() => {
  return {
    '@context': 'https://schema.org',
    '@type': 'VideoObject',
    name: props.title,
    description: props.description || `Video demonstration of ${props.title}`,
    thumbnailUrl: props.thumbnailUrl || props.posterSrc,
    uploadDate: props.uploadDate || new Date().toISOString().split('T')[0],
    duration: props.duration || 'PT30S',
    contentUrl: props.videoSrc,
    embedUrl: props.videoSrc,
  }
})

// Add structured data to head
useHead({
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify(videoStructuredData.value),
    }
  ]
})
</script>

<template>
  <div class="relative w-full">
    <!-- Video Element with Safari compatibility fixes -->
    <video
      ref="videoRef"
      :poster="posterSrc"
      :alt="alt"
      class="w-full max-h-[500px] object-cover rounded-xl shadow-md hover:scale-[1.02] transition-transform duration-300 bg-gray-100 dark:bg-gray-800"
      muted
      loop
      playsinline
      webkit-playsinline
      preload="auto"
      x-webkit-airplay="allow"
      @loadeddata="handleLoadedData"
      @canplay="handleLoadedData"
      @error="handleError"
    >
      <source :src="videoSrc" type="video/mp4; codecs=avc1.42E01E,mp4a.40.2" />
      
      <!-- Fallback for browsers that don't support video -->
      <img 
        :src="posterSrc" 
        :alt="alt"
        class="w-full max-h-[500px] object-cover rounded-xl shadow-md"
      />
    </video>

    <!-- Loading Indicator (optional) -->
    <div 
      v-if="!hasLoaded" 
      class="absolute inset-0 flex items-center justify-center bg-gray-900/20 rounded-xl"
    >
      <div class="animate-spin rounded-full h-12 w-12 border-b-3 border-primary"></div>
    </div>
  </div>
</template>

<style scoped>
/* Ensure video doesn't flash on load */
video {
  background: transparent;
}

/* Style the poster image */
video[poster] {
  object-fit: cover; /* or object-contain, object-fill, etc. */
  /* Add any other poster-specific styles here */
  /* Examples:
  filter: blur(5px);
  opacity: 0.8;
  transform: scale(1.05);
  */




}
</style>
