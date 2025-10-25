<template>
  <div class="glow-border-wrapper">
    <div class="glow-border-animated" />
    <div class="glow-border-content">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  color?: 'primary' | 'blue' | 'purple' | 'pink'
}>()
</script>

<style scoped>
.glow-border-wrapper {
  position: relative;
  padding: 2px;
  border-radius: 0.75rem;
  overflow: hidden;
  background: transparent;
}

.glow-border-animated {
  position: absolute;
  inset: -2px;
  border-radius: 0.75rem;
  background: conic-gradient(
    from var(--angle),
    transparent 0%,
    rgb(var(--color-primary-500)) 10%,
    transparent 20%,
    transparent 80%,
    rgb(var(--color-primary-500)) 90%,
    transparent 100%
  );
  animation: rotate 3s linear infinite;
  z-index: 0;
}

.glow-border-animated::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: conic-gradient(
    from calc(var(--angle) + 180deg),
    transparent 0%,
    rgb(var(--color-primary-400)) 10%,
    transparent 20%
  );
  filter: blur(20px);
  opacity: 0.8;
}

.glow-border-content {
  position: relative;
  z-index: 1;
  background: rgb(var(--color-background));
  border-radius: calc(0.75rem - 2px);
  padding: 1.5rem;
}

@property --angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

@keyframes rotate {
  0% {
    --angle: 0deg;
  }
  100% {
    --angle: 360deg;
  }
}

:root.dark .glow-border-content {
  background: rgb(var(--color-background));
}
</style>
