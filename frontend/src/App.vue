<template>
  <div :class="{ 'dark': isDarkMode }" class="min-h-screen">
    <router-view></router-view>
  </div>
</template>

<script>
import { ref, onMounted, provide } from 'vue'

export default {
  name: 'App',
  setup() {
    const isDarkMode = ref(false)

    const toggleDarkMode = () => {
      console.log('Toggle dark mode called') // 用於調試
      isDarkMode.value = !isDarkMode.value
      localStorage.setItem('darkMode', isDarkMode.value.toString())
      
      if (isDarkMode.value) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }

    // 提供深色模式狀態和切換方法
    provide('isDarkMode', isDarkMode)
    provide('toggleDarkMode', toggleDarkMode)

    // 初始化深色模式
    onMounted(() => {
      const savedMode = localStorage.getItem('darkMode')
      if (savedMode === 'true') {
        isDarkMode.value = true
        document.documentElement.classList.add('dark')
      }
    })

    return {
      isDarkMode
    }
  }
}
</script>

<style>
html {
  transition: background-color 0.3s ease;
}

#app {
  min-height: 100vh;
}

/* 確保深色模式轉換時有平滑效果 */
.dark {
  transition: background-color 0.3s ease, color 0.3s ease;
}
</style>