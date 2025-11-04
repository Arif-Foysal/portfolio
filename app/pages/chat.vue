<template>
  <!-- Main chat container -->
  <div class="min-h-screen flex flex-col">
    <!-- Chat content -->
    <main :class="messages.length > 0 ? 'flex-1 pb-24' : 'flex-1'">
      <UContainer class="max-w-4xl mx-auto py-8">
        
        <!-- Welcome screen when no messages -->
        <div v-if="messages.length === 0" class="flex flex-col items-center justify-center gap-6 text-center min-h-[60vh]">
          <div class="space-y-4">
            <div class="size-16 mx-auto bg-primary/10 rounded-full flex items-center justify-center">
              <UIcon name="i-lucide-message-circle" class="size-8 text-primary" />
            </div>
            
            <div class="space-y-2">
              <h2 class="text-2xl font-bold text-highlighted">
                How can I help you today?
              </h2>
              <p class="text-muted max-w-md">
                Ask me about my projects, skills, experience, or anything else you'd like to know!
              </p>
            </div>
          </div>

          <!-- Quick action buttons -->
          <div class="flex flex-wrap gap-2 justify-center max-w-2xl">
            <UButton
              v-for="quickChat in quickChats"
              :key="quickChat.label"
              :icon="quickChat.icon"
              :label="quickChat.label"
              size="sm"
              color="neutral"
              variant="outline"
              class="rounded-full"
              @click="sendQuickMessage(quickChat.label)"
            />
          </div>

          <!-- Input area for welcome screen -->
          <div class="w-full max-w-4xl mt-8">
            <UChatPrompt
              v-model="inputMessage"
              :disabled="isLoading"
              placeholder="Ask me about my projects, skills, experience..."
              @send="sendMessage"
            >
              <UChatPromptSubmit 
                :disabled="isLoading || !inputMessage.trim()"
                @click="sendMessage"
              />
            </UChatPrompt>
          </div>
        </div>

        <!-- Messages container -->
        <div v-else class="space-y-6" ref="messagesContainer">
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="flex gap-4"
            :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
          >
            <!-- Assistant avatar -->
            <div v-if="message.role === 'assistant'" class="shrink-0">
              <div class="size-8 bg-primary/10 rounded-full flex items-center justify-center">
                <UIcon name="i-lucide-bot" class="size-4 text-primary" />
              </div>
            </div>

            <!-- Message content -->
            <div class="max-w-3xl w-full">
              <div
                class="px-4 py-3 rounded-2xl"
                :class="message.role === 'user' 
                  ? ' ring-2 ring-primary ml-auto w-fit' 
                  : 'bg-elevated'"
              >
                <!-- User message -->
                <div v-if="message.role === 'user'" class="whitespace-pre-wrap text-right">
                  {{ message.content }}
                </div>

                <!-- Assistant message with special UI handling -->
                <div v-else>
                  <!-- Text response -->
                  <div v-if="message.type === 'text'" class="whitespace-pre-wrap">
                    {{ message.content }}
                  </div>

                  <!-- Projects list -->
                  <div v-else-if="message.type === 'projects_list'" class="space-y-4">
                    <h4 class="font-semibold text-lg">My Projects</h4>
                    <div class="grid gap-4">
                      <div
                        v-for="project in message.data"
                        :key="project.name"
                        class=" rounded-lg p-4 bg-default"
                      >
                        <div class="space-y-3">
                          <div>
                            <h5 class="font-semibold">{{ project.name }}</h5>
                            <p class="text-sm text-muted mt-1">{{ project.description }}</p>
                          </div>
                          
                          <div class="flex flex-wrap gap-1">
                            <span
                              v-for="tech in project.technologies"
                              :key="tech"
                              class="px-2 py-1 bg-primary/10 text-primary text-xs rounded-md"
                            >
                              {{ tech }}
                            </span>
                          </div>
                          
                          <div class="flex gap-2" v-if="project.link || project.github_link">
                            <UButton
                              v-if="project.link"
                              :to="project.link"
                              target="_blank"
                              size="xs"
                              icon="i-lucide-external-link"
                              label="View Live"
                            />
                            <UButton
                              v-if="project.github_link"
                              :to="project.github_link"
                              target="_blank"
                              size="xs"
                              color="neutral"
                              icon="i-lucide-github"
                              label="GitHub"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Skills list -->
                  <div v-else-if="message.type === 'skills_list'" class="space-y-4">
                    <h4 class="font-semibold text-lg">My Skills</h4>
                    <div class="space-y-4">
                      <div
                        v-for="skillCategory in message.data"
                        :key="skillCategory.category"
                        class="border border-border rounded-lg p-4 bg-default"
                      >
                        <h5 class="font-semibold mb-2">{{ skillCategory.category }}</h5>
                        <div class="flex flex-wrap gap-2 mb-2">
                          <span
                            v-for="skill in skillCategory.skills"
                            :key="skill"
                            class="px-2 py-1 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-800 dark:text-emerald-200 text-sm rounded-md"
                          >
                            {{ skill }}
                          </span>
                        </div>
                        <p v-if="skillCategory.proficiency" class="text-sm text-muted">
                          Proficiency: {{ skillCategory.proficiency }}
                        </p>
                      </div>
                    </div>
                  </div>

                  <!-- Contact info -->
                  <div v-else-if="message.type === 'contact_info'" class="space-y-4">
                    <h4 class="font-semibold text-lg">Contact Information</h4>
                    <div class="space-y-3">
                      <div class="flex items-center gap-2">
                        <UIcon name="i-lucide-mail" class="size-4 text-muted" />
                        <ULink :to="`mailto:${message.data.email}`" class="text-primary hover:underline">
                          {{ message.data.email }}
                        </ULink>
                      </div>
                      <div v-if="message.data.linkedin" class="flex items-center gap-2">
                        <UIcon name="i-lucide-linkedin" class="size-4 text-muted" />
                        <ULink :to="message.data.linkedin" target="_blank" class="text-primary hover:underline">
                          LinkedIn Profile
                        </ULink>
                      </div>
                      <div v-if="message.data.github" class="flex items-center gap-2">
                        <UIcon name="i-lucide-github" class="size-4 text-muted" />
                        <ULink :to="message.data.github" target="_blank" class="text-primary hover:underline">
                          GitHub Profile
                        </ULink>
                      </div>
                      <div v-if="message.data.website" class="flex items-center gap-2">
                        <UIcon name="i-lucide-globe" class="size-4 text-muted" />
                        <ULink :to="message.data.website" target="_blank" class="text-primary hover:underline">
                          Portfolio Website
                        </ULink>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Copy button for assistant messages -->
              <div v-if="message.role === 'assistant'" class="flex justify-end mt-2">
                <UButton
                  :icon="copiedMessageId === index ? 'i-lucide-check' : 'i-lucide-copy'"
                  size="xs"
                  color="neutral"
                  variant="ghost"
                  @click="copyMessage(message, index)"
                />
              </div>
            </div>

            <!-- User avatar -->
            <div v-if="message.role === 'user'" class="shrink-0">
              <div class="size-8 bg-primary/10 rounded-full flex items-center justify-center">
                <UIcon name="i-lucide-user" class="size-4 text-primary" />
              </div>
            </div>
          </div>

          <!-- Typing indicator -->
          <div v-if="isLoading" class="flex gap-4 justify-start">
            <div class="size-8 bg-primary/10 rounded-full flex items-center justify-center">
              <UIcon name="i-lucide-bot" class="size-4 text-primary" />
            </div>
            <div class="bg-elevated border border-border px-4 py-3 rounded-2xl">
              <div class="flex items-center gap-1">
                <div class="flex space-x-1">
                  <div class="size-2 bg-muted rounded-full animate-pulse" style="animation-delay: 0ms"></div>
                  <div class="size-2 bg-muted rounded-full animate-pulse" style="animation-delay: 150ms"></div>
                  <div class="size-2 bg-muted rounded-full animate-pulse" style="animation-delay: 300ms"></div>
                </div>
                <span class="text-sm text-muted ml-2">Thinking...</span>
              </div>
            </div>
          </div>

          <!-- Quick action suggestions at bottom -->
          <div class="mt-6">
            <div class="flex flex-wrap gap-2 justify-center max-w-2xl mx-auto">
              <UButton
                v-for="quickChat in quickChats"
                :key="quickChat.label"
                :icon="quickChat.icon"
                :label="quickChat.label"
                size="sm"
                color="neutral"
                variant="outline"
                class="rounded-full"
                @click="sendQuickMessage(quickChat.label)"
              />
            </div>
          </div>
        </div>
      </UContainer>
    </main>

    <!-- Input area - Fixed at bottom when there are messages -->
    <div 
      v-if="messages.length > 0"
      class="fixed bottom-0 left-0 right-0 bg-default/95 backdrop-blur border-t border-border p-4 z-50"
    >
      <UContainer class="max-w-4xl mx-auto">
        <UChatPrompt
          v-model="inputMessage"
          :disabled="isLoading"
          placeholder="Ask me about my projects, skills, experience..."
          @send="sendMessage"
        >
          <UChatPromptSubmit 
            :disabled="isLoading || !inputMessage.trim()"
            @click="sendMessage"
          />
        </UChatPrompt>
      </UContainer>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useChatState } from '~/composables/useChat'

// Page metadata
useSeoMeta({
  title: 'Chat with Arif - Portfolio Assistant',
  description: 'Ask me anything about my projects, skills, experience, and background.'
})

// Chat state
const { initialMessage } = useChatState()

// Reactive data
const messages = ref([])
const inputMessage = ref('')
const isLoading = ref(false)
const sessionId = ref(null)
const messagesContainer = ref(null)
const copiedMessageId = ref(null)

// API configuration
const API_BASE_URL = 'https://portfolio-lyart-rho-bxg93lsyt1.vercel.app' // Update with your backend URL

// Quick chat suggestions
const quickChats = [
  {
    label: 'Show me your projects',
    icon: 'i-lucide-folder'
  },
  {
    label: 'What are your skills?',
    icon: 'i-lucide-code'
  },
  {
    label: 'Tell me about your experience',
    icon: 'i-lucide-briefcase'
  },
  {
    label: 'How can I contact you?',
    icon: 'i-lucide-mail'
  },
  {
    label: 'What is your background?',
    icon: 'i-lucide-user'
  }
]

// Generate session ID
function generateSessionId() {
  return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now()
}

// Initialize session
onMounted(() => {
  if (!sessionId.value) {
    sessionId.value = sessionStorage.getItem('chat_session_id') || generateSessionId()
    sessionStorage.setItem('chat_session_id', sessionId.value)
  }
  
  // Check for initial message from PromptInput component
  if (initialMessage.value) {
    inputMessage.value = initialMessage.value
    // Clear the initial message to prevent it from being used again
    initialMessage.value = ''
    // Send the message automatically
    nextTick(() => {
      sendMessage()
    })
  }
})

// Scroll to bottom
async function scrollToBottom() {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Send quick message
function sendQuickMessage(message) {
  inputMessage.value = message
  sendMessage()
}

// Copy message content
function copyMessage(message, index) {
  let textToCopy = ''
  
  if (message.type === 'text') {
    textToCopy = message.content
  } else {
    textToCopy = `${message.type}: ${JSON.stringify(message.data, null, 2)}`
  }
  
  navigator.clipboard.writeText(textToCopy).then(() => {
    copiedMessageId.value = index
    setTimeout(() => {
      copiedMessageId.value = null
    }, 2000)
  })
}

// Send message to chatbot
async function sendMessage() {
  if (!inputMessage.value.trim() || isLoading.value) return

  const userMessage = inputMessage.value.trim()
  inputMessage.value = ''

  // Add user message to chat
  messages.value.push({
    role: 'user',
    content: userMessage,
    timestamp: new Date()
  })

  // Scroll to bottom
  await scrollToBottom()

  // Show loading indicator
  isLoading.value = true

  try {
    // Call chatbot API
    const response = await $fetch(`${API_BASE_URL}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: {
        message: userMessage,
        session_id: sessionId.value
      }
    })

    // Add bot response to chat
    messages.value.push({
      role: 'assistant',
      type: response.type,
      content: response.type === 'text' ? response.data : null,
      data: response.type !== 'text' ? response.data : null,
      timestamp: new Date()
    })

    // Update session ID if provided
    if (response.session_id) {
      sessionId.value = response.session_id
      sessionStorage.setItem('chat_session_id', response.session_id)
    }

  } catch (error) {
    console.error('Error sending message:', error)
    
    // Add error message
    messages.value.push({
      role: 'assistant',
      type: 'text',
      content: 'Sorry, I encountered an error. Please try again later.',
      timestamp: new Date()
    })
  } finally {
    isLoading.value = false
    await scrollToBottom()
  }
}
</script>


