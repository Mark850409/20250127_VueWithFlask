<template>
  <div class="min-h-screen bg-gradient-to-b from-indigo-50 to-white flex items-center justify-center px-4">
    <div class="max-w-4xl mx-auto text-center">
      <!-- 404 圖示 -->
      <div class="mb-8 text-indigo-500">
        <svg class="w-40 h-40 mx-auto" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
        </svg>
      </div>
      
      <!-- 錯誤訊息 -->
      <h1 class="mb-4 text-6xl font-bold text-indigo-600">404</h1>
      <p class="mb-8 text-xl text-gray-600">
        {{ message || '很抱歉，找不到您要的頁面' }}
      </p>
      
      <!-- 倒數計時 -->
      <p class="mb-8 text-sm text-gray-500">
        {{ countdown }} 秒後自動返回首頁
      </p>
      
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { ref, onMounted, onBeforeUnmount } from 'vue'

export default {
  name: 'NotFound',
  
  props: {
    message: {
      type: String,
      default: ''
    }
  },
  
  setup() {
    const router = useRouter()
    const countdown = ref(5)
    let timer = null
    
    const goBack = () => {
      router.back()
    }
    
    const startCountdown = () => {
      timer = setInterval(() => {
        countdown.value--
        if (countdown.value <= 0) {
          clearInterval(timer)
          router.push('/')
        }
      }, 1000)
    }
    
    onMounted(() => {
      startCountdown()
    })
    
    onBeforeUnmount(() => {
      if (timer) {
        clearInterval(timer)
      }
    })
    
    return {
      goBack,
      countdown
    }
  }
}
</script> 