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
    router.push({ path: '/chat' })
  }, 2000); // Simulate async operation
  // prompt.value = ''
}

</script>
<template>
  <form @submit.prevent="handleChat" class="w-full">
    <UFormField :label="errorlabel" size="xl" color="error" class="w-full">
      <UFieldGroup class="w-full">
        <UInput
          v-model="prompt"
          color="primary"
          variant="outline"
          placeholder="Ask anything about me..."
          :disabled="loading"
          class="flex-1 w-full"
              :ui="{ 
      base: 'md:px-4 md:py-3 md:text-xl md:placeholder:text-xl',
      leadingIcon: 'md:size-7',
      trailingIcon: 'md:size-7'
    }"
        />
        <UButton
          icon="material-symbols:magic-button-outline"
          color="primary"
          @click="handleChat"
          :loading="loading"
          class="shrink-0"
              :ui="{ 
      base: 'md:px-4 md:py-3 md:text-xl md:gap-2.5',
      leadingIcon: 'md:size-7',
      trailingIcon: 'md:size-7'
    }"
        >
          Chat Now
        </UButton>
      </UFieldGroup>
    </UFormField>
  </form>
</template>
