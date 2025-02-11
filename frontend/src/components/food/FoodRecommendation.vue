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
        <div class="container mx-auto px-4 mb-8">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold">想找哪裡的飲料店?</h2>
            <div class="flex items-center space-x-4">
              <!-- 定位區域 -->
              <div class="relative">
                <button 
                  @click="getCurrentLocation"
                  class="flex items-center px-4 py-2 bg-gradient-to-r from-purple-500 to-indigo-600 hover:from-purple-600 hover:to-indigo-700 text-white rounded-lg transition-all duration-300 shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
                  :class="{ 'opacity-50 cursor-not-allowed': isLocating }"
                  :disabled="isLocating"
                >
                  <i class="fas fa-location-crosshairs mr-2 animate-pulse"></i>
                  {{ isLocating ? '定位中...' : '目前定位' }}
                </button>
              </div>
  
              <!-- 城市選擇下拉框 -->
              <select 
                v-model="selectedCity"
                class="px-4 py-2 border-2 border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white text-gray-700 shadow-sm hover:border-purple-300 transition-all duration-300"
                @change="handleCityChange"
              >
                <option value="">選擇城市</option>
                <option v-for="city in cities" :key="city" :value="city">
                  {{ city }}
                </option>
              </select>
            </div>
          </div>
  
          <!-- 當前位置顯示 -->
          <div v-if="currentCity" 
               class="flex items-center text-gray-600 bg-gradient-to-r from-purple-50 to-indigo-50 px-6 py-3 rounded-xl shadow-sm border border-purple-100">
            <i class="fas fa-map-marker-alt mr-3 text-purple-500"></i>
            <span class="text-gray-500">目前位置：
              <span class="font-medium text-purple-700 ml-1">{{ currentCity }}</span>
            </span>
          </div>
        </div>
        
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
import Swal from 'sweetalert2'
import { recommendAPI } from '@/api'

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
    
    const sortOptions = ref([
      { value: 'default', label: '預設排序' },
      { value: 'rating', label: '評分排序' },
      { value: 'review_number', label: '瀏覽次數' },
      { value: 'distance', label: '距離排序' }
    ])

    const selectedCity = ref('')
    const currentCity = ref('')
    const isLocating = ref(false)
    const cities = ref([
      '台北市', '新北市', '基隆市', '桃園市', '新竹市', '新竹縣',
      '苗栗縣', '台中市', '彰化縣', '南投縣', '雲林縣', '嘉義市',
      '嘉義縣', '台南市', '高雄市', '屏東縣', '宜蘭縣', '花蓮縣',
      '台東縣', '澎湖縣', '金門縣', '連江縣'
    ])

    // 設置預設城市
    onMounted(() => {
      selectedCity.value = '台北市'
      currentCity.value = '台北市'
      handleCityChange()
    })

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

    // 獲取當前位置
    const getCurrentLocation = () => {
      if (!navigator.geolocation) {
        Swal.fire({
          icon: 'error',
          title: '無法使用定位功能',
          text: '您的瀏覽器不支援地理定位功能'
        })
        return
      }

      isLocating.value = true
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          try {
            const { latitude, longitude } = position.coords
            // 使用 recommendAPI 進行反向地理編碼
            const response = await recommendAPI.reverseGeocode({
              latitude,
              longitude,
              language: 'zh-TW'
            })

            if (response.data && response.data.city) {
              // 確保返回的城市名稱在允許的城市列表中
              const cityName = response.data.city
              if (cities.value.includes(cityName)) {
                currentCity.value = cityName
                selectedCity.value = cityName
                handleCityChange()
                Swal.fire({
                  icon: 'success',
                  title: '定位成功',
                  text: '已自動選擇城市：' + cityName
                })
              } else {
                throw new Error('目前不支援該地區，請手動選擇城市')
              }
            } else {
              throw new Error(response.data?.error || '無法解析城市資訊，請手動選擇城市')
            }
          } catch (error) {
            console.error('定位失敗:', error)
            let errorMessage = '無法獲取您的位置信息'
            if (error.response?.data?.error) {
              errorMessage = error.response.data.error
            } else if (error.message) {
              errorMessage = error.message
            }
            Swal.fire({
              icon: 'error',
              title: '定位失敗',
              text: errorMessage
            })
          } finally {
            isLocating.value = false
          }
        },
        (error) => {
          console.error('定位錯誤:', error)
          let errorMessage = '無法獲取您的位置信息'
          switch(error.code) {
            case error.PERMISSION_DENIED:
              errorMessage = '您已拒絕位置存取權限，請允許網站存取您的位置'
              break
            case error.POSITION_UNAVAILABLE:
              errorMessage = '位置資訊不可用'
              break
            case error.TIMEOUT:
              errorMessage = '獲取位置超時，請再試一次'
              break
          }
          Swal.fire({
            icon: 'error',
            title: '定位失敗',
            text: errorMessage
          })
          isLocating.value = false
        },
        {
          timeout: 10000,
          enableHighAccuracy: true,
          maximumAge: 30000  // 允許使用30秒內的快取位置
        }
      )
    }

    const handleCityChange = () => {
      // 同步更新當前位置顯示
      currentCity.value = selectedCity.value

      // 發出自定義事件，通知子組件城市已更改
      window.dispatchEvent(new CustomEvent('cityChanged', {
        detail: selectedCity.value
      }))

      // 保存到 localStorage
      localStorage.setItem('selectedCity', selectedCity.value)
    }

    return {
      isLoggedIn,
      currentSort,
      currentRecommendSort,
      sortOptions,
      selectedCity,
      currentCity,
      cities,
      getCurrentLocation,
      handleCityChange,
      isLocating
    }
  }
}
</script> 