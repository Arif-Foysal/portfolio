<script setup lang="ts">
import { ref } from 'vue'

const prompt = ref('')
const errorlabel = ref('')
const handleChat = () => {
  if (prompt.value.trim() === '') {
    errorlabel.value = 'Please enter a prompt.'
    return
  }
  // For demonstration, we'll just log the prompt. Replace this with actual chat logic.
  console.log('User prompt:', prompt.value)
  prompt.value = ''
}

</script>
<template>
  <UFormField :label="errorlabel" size="xl" color="error">
    <UFieldGroup class="w-full" >
      <UInput 
        v-model="prompt" 
        color="secondary" 
        placeholder="Ask anything about me..." 
      />
      <UButton 
        icon="material-symbols:magic-button-outline" 
        color="secondary" 
        @click="handleChat"
      > 
        Chat Now
      </UButton>
    </UFieldGroup>
  </UFormField>
</template>