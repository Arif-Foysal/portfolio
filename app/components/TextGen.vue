<template>
  <div class="text-generation-container">
    <!-- Word-by-word rendering -->
    <span 
      v-if="byWord"
      v-for="(word, index) in words"
      :key="`word-${index}`"
      :class="[
        'inline-block transition-all duration-500 ease-out mr-1',
        getWordClasses(index),
        index < revealedCount && props.showShimmer && shimmerActive ? shimmerClass : ''
      ]"
      :style="getWordStyle(index)"
    >
      {{ word }}
    </span>
    
    <!-- Character-by-character rendering -->
    <span
      v-else
      v-for="(char, index) in characters"
      :key="`char-${index}`"
      :class="[
        'inline-block transition-all duration-300 ease-out',
        getCharacterClasses(index),
        index < revealedCount && props.showShimmer && shimmerActive ? shimmerClass : ''
      ]"
      :style="getCharacterStyle(index)"
    >
      {{ char === ' ' ? '\u00A0' : char }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'

interface Props {
  text: string
  effect?: 'reveal' | 'typewriter' | 'fade' | 'slide'
  revealMs?: number
  stagger?: number
  showShimmer?: boolean
  autoStart?: boolean
  // New props for word-by-word animation
  byWord?: boolean
  wordEffect?: 'fade' | 'slide-up' | 'slide-down' | 'slide-left' | 'slide-right' | 'scale' | 'rotate'
}

const props = withDefaults(defineProps<Props>(), {
  effect: 'reveal',
  revealMs: 50,
  stagger: 10,
  showShimmer: false,
  autoStart: true,
  byWord: false,
  wordEffect: 'fade'
})

const revealedCount = ref(0)
const isComplete = ref(false)
const shimmerActive = ref(false)

// Split text into words or characters based on byWord prop
const words = computed(() => props.text.split(' '))
const characters = computed(() => props.text.split(''))

// Use words or characters based on byWord setting
const items = computed(() => props.byWord ? words.value : characters.value)

// Shimmer effect class
const shimmerClass = computed(() => {
  if (!props.showShimmer || !shimmerActive.value) return ''
  // Only apply shimmer to revealed characters
  return 'animate-shimmer bg-gradient-to-r from-transparent via-primary-300 to-transparent bg-clip-text'
})

// Get classes for each character based on effect and reveal state
const getCharacterClasses = (index: number) => {
  const isRevealed = index < revealedCount.value
  const baseClasses = ['transition-all', 'duration-300', 'ease-out']

  switch (props.effect) {
    case 'reveal':
      baseClasses.push(isRevealed ? 'opacity-100' : 'opacity-0')
      break
    case 'typewriter':
      baseClasses.push(isRevealed ? 'opacity-100' : 'opacity-0')
      if (index === revealedCount.value - 1 && !isComplete.value) {
        baseClasses.push('border-r-2', 'border-primary-500', 'animate-pulse')
      }
      break
    case 'fade':
      baseClasses.push(isRevealed ? 'opacity-100' : 'opacity-20')
      break
    case 'slide':
      if (isRevealed) {
        baseClasses.push('opacity-100', 'transform', 'translate-y-0')
      } else {
        baseClasses.push('opacity-0', 'transform', 'translate-y-2')
      }
      break
  }

  return baseClasses.join(' ')
}

// Get classes for each word based on wordEffect and reveal state
const getWordClasses = (index: number) => {
  const isRevealed = index < revealedCount.value
  const baseClasses = ['transition-all', 'duration-500', 'ease-out']

  switch (props.wordEffect) {
    case 'fade':
      baseClasses.push(isRevealed ? 'opacity-100' : 'opacity-0')
      break
    case 'slide-up':
      if (isRevealed) {
        baseClasses.push('opacity-100', 'transform', 'translate-y-0')
      } else {
        baseClasses.push('opacity-0', 'transform', 'translate-y-4')
      }
      break
    case 'slide-down':
      if (isRevealed) {
        baseClasses.push('opacity-100', 'transform', 'translate-y-0')
      } else {
        baseClasses.push('opacity-0', 'transform', '-translate-y-4')
      }
      break
    case 'slide-left':
      if (isRevealed) {
        baseClasses.push('opacity-100', 'transform', 'translate-x-0')
      } else {
        baseClasses.push('opacity-0', 'transform', 'translate-x-4')
      }
      break
    case 'slide-right':
      if (isRevealed) {
        baseClasses.push('opacity-100', 'transform', 'translate-x-0')
      } else {
        baseClasses.push('opacity-0', 'transform', '-translate-x-4')
      }
      break
    case 'scale':
      if (isRevealed) {
        baseClasses.push('opacity-100', 'transform', 'scale-100')
      } else {
        baseClasses.push('opacity-0', 'transform', 'scale-75')
      }
      break
    case 'rotate':
      if (isRevealed) {
        baseClasses.push('opacity-100', 'transform', 'rotate-0')
      } else {
        baseClasses.push('opacity-0', 'transform', 'rotate-12')
      }
      break
  }

  return baseClasses.join(' ')
}

// Get inline styles for character animation timing
const getCharacterStyle = (index: number) => {
  const delay = index * props.stagger
  return {
    transitionDelay: `${delay}ms`
  }
}

// Get inline styles for word animation timing
const getWordStyle = (index: number) => {
  const delay = index * props.stagger
  return {
    transitionDelay: `${delay}ms`
  }
}

// Start the reveal animation
const startReveal = () => {
  const itemsToReveal = props.byWord ? words.value : characters.value
  if (itemsToReveal.length === 0) return

  // Reset state
  revealedCount.value = 0
  isComplete.value = false
  shimmerActive.value = false // Don't start shimmer immediately
  
  console.log('Starting reveal animation with', itemsToReveal.length, props.byWord ? 'words' : 'characters')

  const revealNext = () => {
    if (revealedCount.value < itemsToReveal.length) {
      revealedCount.value++
      
      // Start shimmer after a few items are revealed
      const shimmerThreshold = props.byWord ? 2 : 3
      if (props.showShimmer && revealedCount.value > shimmerThreshold && !shimmerActive.value) {
        shimmerActive.value = true
      }
      
      console.log('Revealed', props.byWord ? 'word' : 'character', revealedCount.value, 'of', itemsToReveal.length)
      setTimeout(revealNext, props.revealMs)
    } else {
      isComplete.value = true
      console.log('Animation complete')
      if (props.showShimmer) {
        // Keep shimmer for a bit after completion
        setTimeout(() => {
          shimmerActive.value = false
        }, 500)
      }
    }
  }

  // Start with a small delay to ensure DOM is ready
  setTimeout(() => {
    revealNext()
  }, 100)
}

// Reset animation
const reset = () => {
  revealedCount.value = 0
  isComplete.value = false
  shimmerActive.value = false
}

// Expose methods for parent components
defineExpose({
  startReveal,
  reset,
  isComplete: computed(() => isComplete.value)
})

// Auto-start on mount
onMounted(() => {
  if (props.autoStart) {
    startReveal()
  }
})

// Watch for text changes and restart animation
watch(() => props.text, () => {
  if (props.autoStart) {
    reset()
    nextTick(() => {
      startReveal()
    })
  }
})
</script>

<style scoped>
.text-generation-container {
  line-height: 1.625;
}

/* Custom shimmer animation */
@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.animate-shimmer {
  animation: shimmer 2s infinite linear;
  background-size: 200% 100%;
}
</style>
