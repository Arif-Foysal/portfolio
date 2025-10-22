<template>
  <button
    ref="buttonRef"
    :class="
      cn(
        'group relative w-auto cursor-pointer overflow-hidden rounded-full  border-2 bg-background p-2 px-6 text-center font-semibold',
        props.class,
      )
    "
  >
    <div class="flex items-center gap-2">
      <!-- <div
        class="size-2 scale-100 rounded-lg bg-primary transition-all duration-300 group-hover:scale-[100.8]"
      > -->
    <Icon icon="ix:ai" width="30" height="30" class="size-6 scale-100  transition-all duration-300 group-hover:scale-[10.8] dark:group-hover:bg-white group-hover:bg-gray-950" />
    <!-- </div> -->
      <span
        class="inline-block whitespace-nowrap transition-all duration-300 group-hover:translate-x-12 group-hover:opacity-0"
      >
        {{ text }}
      </span>
    </div>

    <div
      class="absolute top-0 z-10 flex size-full translate-x-12 items-center justify-center gap-2 text-primary-foreground opacity-0 transition-all duration-300 group-hover:-translate-x-5 group-hover:opacity-100"
    >
      <span class="whitespace-nowrap">{{ text }}</span>
      <!-- <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="lucide lucide-arrow-right"
      >
        <path d="M5 12h14" />
        <path d="m12 5 7 7-7 7" />
      </svg> -->
      <Icon icon="fluent:send-48-filled" width="26" height="26" />
    </div>
  </button>
</template>

<script lang="ts" setup>
import { cn } from "@/lib/utils";
import { ref } from "vue";
import { Icon } from '@iconify/vue';

interface Props {
  text?: string;
  class?: string;
}
const props = withDefaults(defineProps<Props>(), {
  text: "Chat Now",
});

const buttonRef = ref<HTMLButtonElement>();
</script>

<style></style>
