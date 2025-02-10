<template>
  <div class="min-h-screen bg-gray-50">

    <!-- 內容區域 -->
    <div class="pt-16"> <!-- 添加上邊距，為固定導航欄留出空間 -->
      <div id="home">
        <Banner />
      </div>

      <div id="features">
        <Features />
      </div>

      <!-- 熱門飲料推薦區塊 - 只在登入時顯示 -->
      <div id="recommend" v-if="isLoggedIn">
        <Recommendations />
      </div>

      <div id="learning">
        <div class="py-20 bg-white">
          <div class="container mx-auto px-4">
            <h2 class="text-3xl font-bold text-center mb-12">學習中心</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
              <!-- 功能導覽 -->
              <div class="bg-white rounded-xl overflow-hidden shadow-lg">
                <img src="https://images.unsplash.com/photo-1516321318423-f06f85e504b3" 
                     class="w-full h-48 object-cover" alt="功能導覽">
                <div class="p-6">
                  <h3 class="text-xl font-bold mb-2">功能導覽</h3>
                  <p class="text-gray-600 mb-4">
                    了解系統各項功能的使用方式，快速上手推薦系統。
                  </p>
                  <div class="space-y-2 mb-4">
                    <div class="flex items-center text-gray-600">
                      <i class="fas fa-book-reader mr-2"></i>
                      <span>新手必讀</span>
                    </div>
                  </div>
                  <router-link to="/learning" 
                    class="block w-full px-4 py-2 bg-gray-800 text-white rounded-lg 
                           hover:bg-gray-700 text-center transition duration-300">
                    查看教學
                  </router-link>
                </div>
              </div>

              <!-- 常見問題 -->
              <div class="bg-white rounded-xl overflow-hidden shadow-lg">
                <img src="https://images.unsplash.com/photo-1507925921958-8a62f3d1a50d" 
                     class="w-full h-48 object-cover" alt="常見問題">
                <div class="p-6">
                  <h3 class="text-xl font-bold mb-2">常見問題</h3>
                  <p class="text-gray-600 mb-4">
                    解答使用過程中常見的疑問，幫助您更順暢地使用系統。
                  </p>
                  <div class="space-y-2 mb-4">
                    <div class="flex items-center text-gray-600">
                      <i class="fas fa-question-circle mr-2"></i>
                      <span>快速解答</span>
                    </div>
                  </div>
                  <router-link to="/learning#faq" 
                    class="block w-full px-4 py-2 bg-gray-800 text-white rounded-lg 
                           hover:bg-gray-700 text-center transition duration-300">
                    查看問題
                  </router-link>
                </div>
              </div>

              <!-- 使用教學 -->
              <div class="bg-white rounded-xl overflow-hidden shadow-lg">
                <img src="https://images.unsplash.com/photo-1434030216411-0b793f4b4173" 
                     class="w-full h-48 object-cover" alt="使用教學">
                <div class="p-6">
                  <h3 class="text-xl font-bold mb-2">使用教學</h3>
                  <p class="text-gray-600 mb-4">
                    觀看詳細的操作示範影片，掌握系統的進階功能。
                  </p>
                  <div class="space-y-2 mb-4">
                    <div class="flex items-center text-gray-600">
                      <i class="fas fa-video mr-2"></i>
                      <span>影片教學</span>
                    </div>
                  </div>
                  <router-link to="/learning#tutorials" 
                    class="block w-full px-4 py-2 bg-gray-800 text-white rounded-lg 
                           hover:bg-gray-700 text-center transition duration-300">
                    觀看影片
                  </router-link>
                </div>
              </div>
            </div>
            <div class="text-center mt-16">
              <router-link to="/learning" 
                class="inline-flex items-center px-6 py-3 bg-gray-800 text-white rounded-lg 
                       hover:bg-gray-700 transition duration-300">
                <i class="fas fa-arrow-right mr-2"></i>
                探索更多資源
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <div id="pricing">
        <Pricing />
      </div>

    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import Navbar from '../common/Navbar.vue'
import Banner from './Banner.vue'
import Recommendations from './Recommendations.vue'
import Footer from '../common/Footer.vue'
import Features from './Features.vue'
import Learning from './Learning.vue'
import Pricing from './Pricing.vue'
import axios from '@/utils/axios'
import { useAuthStore } from '@/stores/auth'

export default {
  components: {
    Navbar,
    Banner,
    Recommendations,
    Footer,
    Features,
    Learning,
    Pricing
  },
  setup() {
    const authStore = useAuthStore()
    const isLoggedIn = computed(() => authStore.isLoggedIn)
    let tokenCheckInterval = null

    const currentSort = ref('predicted')
    const currentRecommendSort = ref('predicted')
    
    const sortOptions = [
      { label: '預設排序', value: 'predicted' },
      { label: '評分排序', value: 'rating' },
      { label: '熱門排序', value: 'popular' }
    ]

    // 檢查登入狀態和 token 有效性
    const checkLoginStatus = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        authStore.isLoggedIn = false
        return
      }

      try {
        // 驗證 token 有效性
        const response = await axios.get('/users/verify', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        
        if (response.status === 200) {
          authStore.isLoggedIn = true
        } else {
          // token 無效或過期
          localStorage.removeItem('token')
          authStore.isLoggedIn = false
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
      
      // 設定定時檢查 (每10秒檢查一次)
      tokenCheckInterval = setInterval(checkLoginStatus, 10000)
      
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
      isLoggedIn,
      currentSort,
      currentRecommendSort,
      sortOptions
    }
  }
}
</script> 