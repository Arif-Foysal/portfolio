<script setup lang="ts">
import { useChatState } from '~/composables/useChat';
const { initialMessage } = useChatState()

import TextGen from '~/components/TextGen.vue'
const description = `I build production-ready AI systems — model training, deployment, and MLOps.`

</script>

<template>
<SocialIcons />
<p>{{ initialMessage }}</p>

 <TextGen
    :byWord="false"
    wordEffect="scale"
    :text="description"
    :revealMs="50"
    :stagger="30"
    :showShimmer="true"
    class="text-lg leading-relaxed"
  />

</template>
