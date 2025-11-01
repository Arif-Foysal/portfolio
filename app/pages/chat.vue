<script setup lang="ts">
import { useChatState } from '~/composables/useChat';
const { initialMessage } = useChatState()

</script>

<template>
<SocialIcons />
<p>{{ initialMessage }}</p>
</template>
