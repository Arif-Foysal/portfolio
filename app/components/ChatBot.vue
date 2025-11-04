<!-- 
Chatbot Component for Portfolio Website
This component demonstrates how to consume the chatbot API and render different UI elements
based on the response type (text, projects_list, skills_list, etc.)
-->

<template>
  <div class="chatbot-container">
    <!-- Chat Header -->
    <div class="chat-header">
      <h3>Chat with Arif</h3>
      <p>Ask me about my projects, skills, experience, or anything else!</p>
    </div>

    <!-- Chat Messages -->
    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.sender]"
      >
        <!-- User Messages -->
        <div v-if="message.sender === 'user'" class="message-content">
          {{ message.content }}
        </div>

        <!-- Bot Text Responses -->
        <div v-else-if="message.type === 'text'" class="message-content">
          {{ message.content }}
        </div>

        <!-- Projects List UI -->
        <div v-else-if="message.type === 'projects_list'" class="special-ui projects-grid">
          <h4>My Projects</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div
              v-for="project in message.data"
              :key="project.name"
              class="project-card"
            >
              <img
                v-if="project.image"
                :src="project.image"
                :alt="project.name"
                class="project-image"
              />
              <div class="project-info">
                <h5>{{ project.name }}</h5>
                <p>{{ project.description }}</p>
                <div class="tech-stack">
                  <span
                    v-for="tech in project.technologies"
                    :key="tech"
                    class="tech-tag"
                  >
                    {{ tech }}
                  </span>
                </div>
                <div class="project-links">
                  <a v-if="project.link" :href="project.link" target="_blank" class="link-button">
                    View Live
                  </a>
                  <a v-if="project.github_link" :href="project.github_link" target="_blank" class="link-button">
                    GitHub
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Skills List UI -->
        <div v-else-if="message.type === 'skills_list'" class="special-ui skills-grid">
          <h4>My Skills</h4>
          <div class="skills-categories">
            <div
              v-for="skillCategory in message.data"
              :key="skillCategory.category"
              class="skill-category"
            >
              <h5>{{ skillCategory.category }}</h5>
              <div class="skills-list">
                <span
                  v-for="skill in skillCategory.skills"
                  :key="skill"
                  class="skill-tag"
                >
                  {{ skill }}
                </span>
              </div>
              <p v-if="skillCategory.proficiency" class="proficiency">
                Proficiency: {{ skillCategory.proficiency }}
              </p>
            </div>
          </div>
        </div>

        <!-- Education List UI -->
        <div v-else-if="message.type === 'education_list'" class="special-ui education-list">
          <h4>My Education</h4>
          <div class="education-items">
            <div
              v-for="edu in message.data"
              :key="edu.institution"
              class="education-item"
            >
              <h5>{{ edu.degree }} in {{ edu.field }}</h5>
              <p class="institution">{{ edu.institution }}</p>
              <p class="year">{{ edu.year }}</p>
              <p v-if="edu.description" class="description">{{ edu.description }}</p>
            </div>
          </div>
        </div>

        <!-- Experience List UI -->
        <div v-else-if="message.type === 'experience_list'" class="special-ui experience-list">
          <h4>My Work Experience</h4>
          <div class="experience-items">
            <div
              v-for="exp in message.data"
              :key="exp.company"
              class="experience-item"
            >
              <h5>{{ exp.position }}</h5>
              <p class="company">{{ exp.company }}</p>
              <p class="duration">{{ exp.duration }}</p>
              <p class="description">{{ exp.description }}</p>
              <div class="tech-stack">
                <span
                  v-for="tech in exp.technologies"
                  :key="tech"
                  class="tech-tag"
                >
                  {{ tech }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Contact Info UI -->
        <div v-else-if="message.type === 'contact_info'" class="special-ui contact-info">
          <h4>Contact Information</h4>
          <div class="contact-details">
            <div class="contact-item">
              <strong>Email:</strong> 
              <a :href="`mailto:${message.data.email}`">{{ message.data.email }}</a>
            </div>
            <div v-if="message.data.linkedin" class="contact-item">
              <strong>LinkedIn:</strong> 
              <a :href="message.data.linkedin" target="_blank">Connect with me</a>
            </div>
            <div v-if="message.data.github" class="contact-item">
              <strong>GitHub:</strong> 
              <a :href="message.data.github" target="_blank">View my code</a>
            </div>
            <div v-if="message.data.website" class="contact-item">
              <strong>Website:</strong> 
              <a :href="message.data.website" target="_blank">Visit my portfolio</a>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Typing indicator -->
      <div v-if="isTyping" class="message bot typing">
        <div class="typing-indicator">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>

    <!-- Chat Input -->
    <div class="chat-input">
      <form @submit.prevent="sendMessage" class="input-form">
        <input
          v-model="inputMessage"
          :disabled="isTyping"
          placeholder="Ask me about my projects, skills, experience..."
          class="message-input"
        />
        <button type="submit" :disabled="isTyping || !inputMessage.trim()" class="send-button">
          Send
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

// Reactive data
const messages = ref([])
const inputMessage = ref('')
const isTyping = ref(false)
const sessionId = ref(null)
const messagesContainer = ref(null)

// API configuration
const API_BASE_URL = 'https://portfolio-lyart-rho-bxg93lsyt1.vercel.app'  // Update with your backend URL

// Generate or get session ID
if (process.client && !sessionId.value) {
  sessionId.value = localStorage.getItem('chat_session_id') || generateSessionId()
  localStorage.setItem('chat_session_id', sessionId.value)
}

function generateSessionId() {
  return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now()
}

// Send message to chatbot
async function sendMessage() {
  if (!inputMessage.value.trim() || isTyping.value) return

  const userMessage = inputMessage.value.trim()
  inputMessage.value = ''

  // Add user message to chat
  messages.value.push({
    sender: 'user',
    content: userMessage,
    timestamp: new Date()
  })

  // Scroll to bottom
  await nextTick()
  scrollToBottom()

  // Show typing indicator
  isTyping.value = true

  try {
    // Call chatbot API
    const response = await fetch(`${API_BASE_URL}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: userMessage,
        session_id: sessionId.value
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()

    // Add bot response to chat
    messages.value.push({
      sender: 'bot',
      type: data.type,
      content: data.type === 'text' ? data.data : null,
      data: data.type !== 'text' ? data.data : null,
      timestamp: new Date()
    })

    // Update session ID if provided
    if (data.session_id) {
      sessionId.value = data.session_id
      if (process.client) {
        localStorage.setItem('chat_session_id', data.session_id)
      }
    }

  } catch (error) {
    console.error('Error sending message:', error)
    
    // Add error message
    messages.value.push({
      sender: 'bot',
      type: 'text',
      content: 'Sorry, I encountered an error. Please try again later.',
      timestamp: new Date()
    })
  } finally {
    isTyping.value = false
    await nextTick()
    scrollToBottom()
  }
}

// Scroll to bottom of messages
function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Initialize with a welcome message
if (process.client && messages.value.length === 0) {
  messages.value.push({
    sender: 'bot',
    type: 'text',
    content: "Hi! I'm Arif's AI assistant. Feel free to ask me about his projects, skills, work experience, education, or anything else you'd like to know!",
    timestamp: new Date()
  })
}
</script>

<style scoped>
.chatbot-container {
  @apply max-w-4xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden;
  height: 600px;
  display: flex;
  flex-direction: column;
}

.chat-header {
  @apply bg-blue-600 text-white p-4;
}

.chat-header h3 {
  @apply text-xl font-bold mb-1;
}

.chat-header p {
  @apply text-blue-100 text-sm;
}

.chat-messages {
  @apply flex-1 overflow-y-auto p-4 space-y-4;
}

.message {
  @apply flex;
}

.message.user {
  @apply justify-end;
}

.message.bot {
  @apply justify-start;
}

.message-content {
  @apply max-w-xs lg:max-w-md px-4 py-2 rounded-lg;
}

.message.user .message-content {
  @apply bg-blue-600 text-white;
}

.message.bot .message-content {
  @apply bg-gray-200 text-gray-800;
}

.special-ui {
  @apply max-w-full bg-gray-50 p-4 rounded-lg border;
}

.special-ui h4 {
  @apply text-lg font-bold mb-3 text-gray-800;
}

.projects-grid .project-card {
  @apply bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow;
}

.project-image {
  @apply w-full h-32 object-cover rounded mb-3;
}

.project-info h5 {
  @apply font-bold text-gray-800 mb-2;
}

.project-info p {
  @apply text-gray-600 text-sm mb-3;
}

.tech-stack {
  @apply flex flex-wrap gap-1 mb-3;
}

.tech-tag {
  @apply bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs;
}

.project-links {
  @apply flex gap-2;
}

.link-button {
  @apply bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors;
}

.skills-categories {
  @apply space-y-4;
}

.skill-category {
  @apply bg-white p-4 rounded-lg;
}

.skill-category h5 {
  @apply font-bold text-gray-800 mb-2;
}

.skills-list {
  @apply flex flex-wrap gap-2 mb-2;
}

.skill-tag {
  @apply bg-green-100 text-green-800 px-2 py-1 rounded text-sm;
}

.proficiency {
  @apply text-gray-600 text-sm font-medium;
}

.education-items, .experience-items {
  @apply space-y-4;
}

.education-item, .experience-item {
  @apply bg-white p-4 rounded-lg;
}

.education-item h5, .experience-item h5 {
  @apply font-bold text-gray-800 mb-1;
}

.institution, .company {
  @apply text-blue-600 font-medium;
}

.year, .duration {
  @apply text-gray-500 text-sm mb-2;
}

.description {
  @apply text-gray-600 text-sm mb-3;
}

.contact-details {
  @apply space-y-3;
}

.contact-item {
  @apply flex items-center gap-2;
}

.contact-item a {
  @apply text-blue-600 hover:text-blue-800;
}

.typing-indicator {
  @apply flex space-x-1 px-4 py-2;
}

.typing-indicator span {
  @apply w-2 h-2 bg-gray-400 rounded-full animate-pulse;
  animation-delay: calc(var(--i) * 0.2s);
}

.typing-indicator span:nth-child(1) { --i: 0; }
.typing-indicator span:nth-child(2) { --i: 1; }
.typing-indicator span:nth-child(3) { --i: 2; }

.chat-input {
  @apply p-4 border-t bg-gray-50;
}

.input-form {
  @apply flex gap-2;
}

.message-input {
  @apply flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500;
}

.send-button {
  @apply bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors;
}
</style>
