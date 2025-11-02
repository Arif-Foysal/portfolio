<script setup lang="ts">
import { ref } from 'vue'
import { useToast } from '#imports'

const columns = [{
  label: 'Resources',
  children: [{
    label: 'Help center'
  }, {
    label: 'Docs'
  }, {
    label: 'Roadmap'
  }, {
    label: 'Changelog'
  }]
}, {
  label: 'Features',
  children: [{
    label: 'Affiliates'
  }, {
    label: 'Portal'
  }, {
    label: 'Jobs'
  }, {
    label: 'Sponsors'
  }]
}, {
  label: 'Company',
  children: [{
    label: 'About'
  }, {
    label: 'Pricing'
  }, {
    label: 'Careers'
  }, {
    label: 'Blog'
  }]
}]

const toast = useToast()

const email = ref('')
const loading = ref(false)

function isValidEmail(email: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

async function onSubmit() {
  if (!isValidEmail(email.value)) {
    toast.clear() // Clear previous toasts
    toast.add({
      title: 'Invalid Email',
      description: 'Please enter a valid email address.',
      color: 'error'
    })
    return
  }
  loading.value = true
  // Mock API call: wait 2 seconds
  await new Promise(resolve => setTimeout(resolve, 2000))
  loading.value = false

  toast.clear() // Clear previous toasts
  toast.add({
    title: 'Subscribed!',
    description: 'You\'ve been subscribed to our newsletter.'
  })
}
</script>

<template>
  <USeparator icon="i-simple-icons-nuxtdotjs" class="h-px" />

  <UFooter :ui="{ top: 'border-b border-default' }">
    <template #top>
      <UContainer>
        <UFooterColumns :columns="columns">
          <template #right>
            <form @submit.prevent="onSubmit">
              <UFormField size="xl" >
                <UFieldGroup class="w-full">
                  <UInput v-model="email" color="primary" placeholder="Your Email" />
                  <UButton  type="submit" icon="ic:outline-email" color="primary" :loading="loading">
                    Subscribe
                  </UButton>
                </UFieldGroup>
              </UFormField>
            </form>
          </template>
        </UFooterColumns>
      </UContainer>
    </template>

    <template #left>
      <p class="text-muted text-sm">
      © {{ new Date().getFullYear() }} Arif Foysal - All rights reserved.
      </p>
    </template>

    <template #right>

      <SocialIcons />
    </template>
  </UFooter>
</template>
