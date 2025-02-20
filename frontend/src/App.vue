<template>
  <div :class="{ 'dark': isDark }" class="min-h-screen">
    <router-view></router-view>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useThemeStore } from './stores/theme'

const themeStore = useThemeStore()
const isDark = ref(themeStore.isDark)
</script>

<style>
html {
  transition: background-color 0.3s ease;
}

#app {
  min-height: 100vh;
}
</style>