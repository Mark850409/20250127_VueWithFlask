<template>
  <div class="min-h-screen flex flex-col">
    <!-- 前台 Navbar -->
    <Navbar />
    
    <!-- 主要內容區域 -->
    <main class="flex-1">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

        <!-- 在最外層 div 結尾前添加 AI 聊天助手 -->
    <AIChatAssistant />

    <!-- 前台 Footer -->
    <Footer />
  </div>
</template>

<script>
import Navbar from '../components/common/Navbar.vue'
import Footer from '../components/common/Footer.vue'
import AIChatAssistant from '../components/chat/AIChatAssistant.vue'
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from '@/utils/axios'

export default {
  name: 'FrontLayout',
  components: {
    Navbar,
    Footer,
    AIChatAssistant
  },
  setup() {
    const authStore = useAuthStore()
    let tokenCheckInterval = null

    // 檢查登入狀態和 token 有效性
    const checkLoginStatus = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        authStore.isLoggedIn = false
        return
      }

      try {
        // 驗證 token 有效性
        const response = await axios.get('/users/verify')
        if (response.status === 200) {
          authStore.isLoggedIn = true
        }
      } catch (error) {
        console.error('Token 驗證失敗:', error)
        localStorage.removeItem('token')
        authStore.isLoggedIn = false
      }
    }

    onMounted(() => {
      // 初始檢查
      checkLoginStatus()
      
      // 設定每小時檢查一次
      tokenCheckInterval = setInterval(checkLoginStatus, 3600000)
      
      // 監聽 localStorage 變化
      window.addEventListener('storage', checkLoginStatus)
    })

    // 組件卸載時清理定時器
    onUnmounted(() => {
      if (tokenCheckInterval) {
        clearInterval(tokenCheckInterval)
      }
      window.removeEventListener('storage', checkLoginStatus)
    })

    return {
      checkLoginStatus
    }
  },
  mounted() {
    // 添加滾動監聽
    this.initScrollAnimation()
  },
  beforeUnmount() {
    // 移除滾動監聽
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    initScrollAnimation() {
      // 初始化需要動畫的元素
      const animatedElements = document.querySelectorAll('.fade-in-section')
      this.handleScroll = () => {
        animatedElements.forEach(element => {
          const elementTop = element.getBoundingClientRect().top
          const elementBottom = element.getBoundingClientRect().bottom
          
          // 當元素進入視窗時添加動畫類
          if (elementTop < window.innerHeight && elementBottom > 0) {
            element.classList.add('is-visible')
          }
        })
      }
      
      // 添加滾動監聽
      window.addEventListener('scroll', this.handleScroll)
      // 初始檢查
      this.handleScroll()
    }
  }
}
</script>

<style>
/* 路由切換動畫 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 滾動載入動畫 */
.fade-in-section {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
  will-change: opacity, transform;
}

.fade-in-section.is-visible {
  opacity: 1;
  transform: translateY(0);
}

/* 為了確保平滑滾動 */
html {
  scroll-behavior: smooth;
}
</style> 