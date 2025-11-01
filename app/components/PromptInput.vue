<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useChatState } from '~/composables/useChat';
const { initialMessage } = useChatState()

const loading = ref(false)
const prompt = ref('')
const errorlabel = ref('')
const router = useRouter()
const handleChat = () => {
  if (prompt.value.trim() === '') {
    errorlabel.value = 'Please enter a prompt.'
    return
  }
  initialMessage.value = prompt.value
  errorlabel.value = ''
  loading.value = true
  setTimeout(() => {
    loading.value = false
    router.push({ path: '/chat', query: { prompt: prompt.value } })
  }, 2000); // Simulate async operation
  // prompt.value = ''
}

</script>
<template>
  <UFormField :label="errorlabel" size="xl" color="error">
    <UFieldGroup class="w-full" >
      <UInput 
        v-model="prompt" 
        color="primary" 
        placeholder="Ask anything about me..." 
      />
      <UButton 
        icon="material-symbols:magic-button-outline" 
        color="primary" 
        @click="handleChat"
        :loading="loading"
      > 
        Chat Now
      </UButton>
    </UFieldGroup>
  </UFormField>
</template>