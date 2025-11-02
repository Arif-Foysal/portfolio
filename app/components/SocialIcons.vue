<script setup lang="ts">
import { computed } from 'vue'

interface SocialLink {
  icon: string
  to: string
  label?: string
  target?: string
  color?: string
  variant?: string
  square?: boolean
}

const props = defineProps<{
  links?: SocialLink[]
  size?: string
  fieldGroupSize?: string
  uiBasePadding?: string
  leadingIconClass?: string
  btnClass?: string
}>()

const defaults: SocialLink[] = [
  { icon: 'mdi:github', to: 'https://github.com/arif-foysal', label: 'GitHub' },
  { icon: 'logos:google-gmail', to: 'mailto:ariffaysal.nayem@gmail.com', label: 'Email' },
  { icon: 'logos:whatsapp-icon', to: 'https://wa.me/8801707820797', label: 'WhatsApp' },
  { icon: 'logos:linkedin-icon', to: 'https://www.linkedin.com/in/md-arif-foysal-nayem-206979215/', label: 'LinkedIn' },
  { icon: 'logos:facebook', to: 'https://www.facebook.com/ariffoysal.nayeem.9/', label: 'Facebook' },
  { icon: 'ri:threads-fill', to: 'https://linkedin.com/in/yourusername', label: 'Threads' },
  { icon: 'ri:twitter-x-line', to: 'https://linkedin.com/in/yourusername', label: 'X' }
]

const links = computed(() => props.links && props.links.length ? props.links : defaults)
const size = computed(() => props.size || 'xl')
const fieldGroupSize = computed(() => props.fieldGroupSize || 'xl')
const uiBasePadding = computed(() => props.uiBasePadding || ' lg:p-3')
const leadingIconClass = computed(() => props.leadingIconClass || ' size-8')
const btnClass = computed(() => props.btnClass || 'transition-transform duration-200 hover:scale-110 hover:-translate-y-1')
</script>

<template>
  <UFieldGroup :size="fieldGroupSize">
    <UButton
      v-for="link in links"
      :key="link.to + link.icon"
      :icon="link.icon"
      :size="size"
      :color="link.color || 'neutral'"
      :variant="link.variant || 'outline'"
      :square="link.square ?? true"
      :to="link.to"
      :target="link.target || '_blank'"
      :class="btnClass"
      :ui="{ base: uiBasePadding, leadingIcon: leadingIconClass }"
    >
      <span v-if="link.label" class="sr-only">{{ link.label }}</span>
    </UButton>
  </UFieldGroup>
</template>
