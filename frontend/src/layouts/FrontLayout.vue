<template>
  <div class="min-h-screen flex flex-col" :class="theme">
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

    <AIChatAssistant />
    <Footer />

    <!-- 主題切換按鈕 -->
    <button 
      @click="toggleTheme" 
      class="fixed bottom-4 left-4 p-3 rounded-full shadow-lg transition-all duration-300 z-[999]"
      :class="[
        theme === 'dark' 
          ? 'bg-gray-800/90 hover:bg-gray-700' 
          : 'bg-white/90 hover:bg-gray-100'
      ]"
    >
      <i 
        class="text-xl block"
        :class="[
          theme === 'dark' 
            ? 'ri-sun-line text-yellow-400' 
            : 'ri-moon-line text-gray-600'
        ]"
      ></i>
    </button>
  </div>
</template>

<script>
import Navbar from '../components/common/Navbar.vue'
import Footer from '../components/common/Footer.vue'
import AIChatAssistant from '../components/chat/AIChatAssistant.vue'
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from '@/utils/axios'

// 預加載 CSS 文件
const themes = import.meta.glob('../assets/css/*.css', { query: '?inline' })

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
    const theme = ref('light')

    // 動態載入 CSS
    const loadThemeCSS = async (themeName) => {
      // 移除現有的主題 CSS
      const existingThemeLink = document.getElementById('theme-css')
      if (existingThemeLink) {
        existingThemeLink.remove()
      }

      try {
        // 使用 glob 導入 CSS
        const cssPath = `../assets/css/${themeName}.css`
        if (themes[cssPath]) {
          const cssModule = await themes[cssPath]()
          
          // 創建新的 style 元素
          const styleElement = document.createElement('style')
          styleElement.id = 'theme-css'
          styleElement.textContent = cssModule.default
          document.head.appendChild(styleElement)
        }
      } catch (error) {
        console.error('載入主題 CSS 失敗:', error)
      }
    }

    // 切換主題
    const toggleTheme = () => {
      theme.value = theme.value === 'dark' ? 'light' : 'dark'
      localStorage.setItem('theme', theme.value)
      loadThemeCSS(theme.value)
    }

    // 監聽主題變化
    watch(() => theme.value, (newTheme) => {
      loadThemeCSS(newTheme)
    })

    onMounted(() => {
      // 初始化主題
      const savedTheme = localStorage.getItem('theme')
      if (savedTheme) {
        theme.value = savedTheme
      }
      loadThemeCSS(theme.value)

      // 初始檢查登入狀態
      checkLoginStatus()
      tokenCheckInterval = setInterval(checkLoginStatus, 3600000)
      window.addEventListener('storage', checkLoginStatus)
    })

    onUnmounted(() => {
      if (tokenCheckInterval) {
        clearInterval(tokenCheckInterval)
      }
      window.removeEventListener('storage', checkLoginStatus)
    })

    // 檢查登入狀態
    const checkLoginStatus = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        authStore.isLoggedIn = false
        return
      }

      try {
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

    return {
      theme,
      toggleTheme,
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

/* 主題切換動畫 */
.min-h-screen {
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* 按鈕動畫 */
button i {
  transition: transform 0.3s ease;
}

button:hover i {
  transform: rotate(30deg);
}
</style> 