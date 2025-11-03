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
  
  try {
    const response = await fetch('https://portfolio-lyart-rho-bxg93lsyt1.vercel.app/newsletter/subscribe', {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email.value
      })
    })
    
    const data = await response.json()
    
    toast.clear() // Clear previous toasts
    
    if (response.ok && data.success) {
      toast.add({
        title: 'Subscribed!',
        description: data.message || 'You\'ve been subscribed to our newsletter.'
      })
      email.value = '' // Clear the email input
    } else if (response.ok && !data.success) {
      // Handle case where email is already subscribed
      toast.add({
        title: 'Already Subscribed',
        description: data.message || 'You are already subscribed.',
        color: 'warning'
      })
    } else {
      // Handle HTTP errors
      toast.add({
        title: 'Subscription Failed',
        description: 'There was an error subscribing to the newsletter. Please try again.',
        color: 'error'
      })
    }
  } catch (error) {
    console.error('Newsletter subscription error:', error)
    toast.clear()
    toast.add({
      title: 'Network Error',
      description: 'Unable to connect to the server. Please check your connection and try again.',
      color: 'error'
    })
  } finally {
    loading.value = false
  }
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
