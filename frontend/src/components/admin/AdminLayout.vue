<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 flex" :class="theme">
    <!-- 預載入動畫 -->
    <div v-if="isLoading" 
         class="fixed inset-0 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm z-50 flex items-center justify-center">
      <div class="flex flex-col items-center space-y-4">
        <div class="relative">
          <!-- 外圈動畫 -->
          <div class="absolute inset-0 rounded-full border-4 border-indigo-100 dark:border-indigo-900"></div>
          <!-- 旋轉的邊框 -->
          <div class="w-16 h-16 rounded-full border-4 border-indigo-600 dark:border-indigo-400 border-t-transparent animate-spin"></div>
          <!-- 內圈脈衝 -->
          <div class="absolute inset-3 rounded-full bg-indigo-500/20 dark:bg-indigo-400/20 animate-pulse"></div>
        </div>
        <!-- 載入文字 -->
        <div class="text-gray-600 dark:text-gray-300 text-lg font-medium tracking-wider animate-pulse">
          載入中...
        </div>
      </div>
    </div>

    <!-- 側邊欄 -->
    <aside :class="[
      'fixed top-0 left-0 h-full bg-white dark:bg-gray-800 border-r dark:border-gray-700 z-40 flex flex-col transition-all duration-300',
      'md:translate-x-0',
      isSidebarCollapsed ? '-translate-x-full w-0 overflow-hidden' : 'translate-x-0 w-[280px] md:w-72 lg:w-64'
    ]">
      <!-- Logo -->
      <div class="flex-shrink-0 flex items-center justify-between h-16 border-b dark:border-gray-700 px-4 md:px-6">
        <div class="flex items-center">
          <i class="ri-drinks-2-line text-2xl text-indigo-600 dark:text-indigo-400"></i>
          <span class="ml-3 text-base md:text-xl font-semibold text-gray-900 dark:text-white truncate max-w-[200px] lg:max-w-none">
            今天喝什麼呢?
          </span>
        </div>
        <!-- 手機版關閉按鈕 -->
        <button 
          class="md:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
          @click="toggleSidebar"
        >
          <i class="fas fa-times"></i>
        </button>
      </div>

      <!-- 使用者資訊 -->
      <div class="flex-shrink-0 p-6 border-b dark:border-gray-700 overflow-hidden">
        <div class="flex flex-col items-center text-center">
          <img :src="getAvatarUrl"
               alt="User Avatar" 
               class="w-16 h-16 md:w-[96px] md:h-[96px] rounded-full mb-4"
               @error="handleAvatarError">
          <div class="overflow-hidden w-full">
            <div class="text-lg md:text-xl font-medium text-indigo-600 dark:text-indigo-400 mb-2">
              嗨 ~ {{ userInfo.username }} 你好
            </div>
            <div class="text-sm md:text-base text-gray-500 dark:text-gray-400">
              歡迎使用後台管理系統
            </div>
          </div>
        </div>
      </div>

      <!-- 選單 -->
      <div class="flex-1 overflow-y-auto px-2 md:px-4 py-4 w-full">
        <div class="space-y-4 overflow-hidden">
          <!-- Navigation 分類標題 -->
          <div v-if="!isSidebarCollapsed" class="px-4 pt-2">
            <h3 class="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">
              {{ category }}
            </h3>
          </div>

          <!-- Dashboard -->
          <router-link to="/admin" 
            class="flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors duration-150"
            :class="[
              $route.path === '/admin' 
                ? 'text-indigo-700 bg-gradient-to-r from-indigo-50 to-blue-50 hover:from-indigo-100 hover:to-blue-100' 
                : 'text-gray-700 hover:bg-gray-50'
            ]">
            <div class="flex-shrink-0 w-6">
              <i class="ri-dashboard-3-line"></i>
            </div>
            <div class="ml-3 flex-1" v-if="!isSidebarCollapsed">
              <div>儀錶板管理</div>
            </div>
          </router-link>

          <!-- Apps 分類標題 -->
          <div v-if="!isSidebarCollapsed" class="px-4 pt-4">
            <h3 class="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Apps</h3>
          </div>

          <!-- 動態生成的選單 -->
          <template v-for="category in menuCategories" :key="category">
            <div class="space-y-1">
              <!-- 主選單 -->
              <div class="flex items-center px-4 py-3 text-sm font-medium rounded-lg cursor-pointer"
                   :class="[
                     sortedMenus(category).some(menu => $route.path.includes(menu.path)) || openMenus[category]
                       ? 'text-indigo-700 bg-gradient-to-r from-indigo-50 to-blue-50 hover:from-indigo-100 hover:to-blue-100' 
                       : 'text-gray-700 hover:bg-gray-50'
                   ]"
                   @click="toggleMenu(category)">
                <div class="flex-shrink-0 w-6">
                  <i :class="[sortedMenus(category)[0]?.icon || 'fas fa-folder', 'text-lg']"></i>
                </div>
                <div class="ml-3 flex-1" v-if="!isSidebarCollapsed">
                  <div>{{ category }}</div>
                </div>
                <i v-if="!isSidebarCollapsed" 
                   class="fas fa-chevron-right text-sm transition-transform duration-200"
                   :class="{ 'transform rotate-90': openMenus[category] }"></i>
              </div>

              <!-- 子選單 -->
              <div v-show="openMenus[category] && !isSidebarCollapsed" 
                   class="pl-4 ml-4 space-y-2 border-l border-gray-200 py-2">
                <router-link v-for="menu in sortedMenus(category)"
                            :key="menu.id"
                            :to="menu.path"
                            @click="handleMenuClick"
                            class="flex items-center px-4 py-2.5 text-sm font-medium rounded-lg transition-all duration-150"
                            :class="[
                              $route.path.includes(menu.path)
                                ? 'text-indigo-700 bg-gradient-to-r from-indigo-50 to-blue-50 hover:from-indigo-100 hover:to-blue-100 shadow-sm' 
                                : 'text-gray-700 hover:bg-gray-50'
                            ]">
                  <div class="flex-shrink-0 w-6">
                    <i :class="['text-lg', menu.icon]"></i>
                  </div>
                  <div class="ml-3 flex-1" v-if="!isSidebarCollapsed">
                    <div>{{ menu.name }}</div>
                  </div>
                </router-link>
              </div>
            </div>
          </template>
        </div>
      </div>

      <!-- 登出按鈕 -->
      <div v-show="!isSidebarCollapsed" class="flex-shrink-0 p-4 border-t dark:border-gray-700">
        <!-- 主題切換和登出按鈕容器 -->
        <div class="flex items-center gap-2">
          <!-- 主題切換按鈕 -->
          <button @click="toggleTheme" 
            class="flex items-center justify-center px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
            <i :class="[
              theme === 'dark' ? 'ri-sun-line text-yellow-400' : 'ri-moon-line text-gray-600',
              'text-lg w-6'
            ]"></i>
          </button>
          
          <!-- 登出按鈕 -->
          <button @click="logout" 
            class="flex items-center justify-center flex-1 px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
            <i class="ri-logout-box-r-line text-lg w-6"></i>
            <span class="ml-3">登出</span>
          </button>
        </div>
      </div>
    </aside>

    <!-- 主要內容區域 -->
    <div class="flex-1 flex flex-col transition-all duration-300"
         :class="[
           isSidebarCollapsed ? 'ml-0' : 'md:ml-72 lg:ml-64',
           'w-full'
         ]">
      <!-- Navbar -->
      <AdminNavbar 
        :isSidebarCollapsed="isSidebarCollapsed"
        @toggle-sidebar="toggleSidebar"
        :remainingTime="remainingTime"
        :formatTime="formatTime"
        class="z-30"
      />

      

      <!-- 內容區域 -->
      <div class="admin-page dashboard-card flex-1 p-3 xs:p-4 md:p-6">
        <!-- Banner -->
        <div class="bg-white shadow-sm rounded-lg overflow-hidden mb-6">
          <div class="relative banner-bg h-[200px]">
            <!-- 背景圖片 -->
            <div class="absolute inset-0 w-full h-full">
              <div class="w-full h-full bg-cover bg-center bg-no-repeat"
                   :style="{ backgroundImage: `url(${bannerData.image_url})` }">
              </div>
            </div>
            <!-- 半透明遮罩 -->
            <div class="absolute inset-0 bg-black/30"></div>
            
            <!-- Banner 內容 -->
            <div class="relative px-4 md:px-8 py-8 md:py-16">
              <h1 class="text-xl md:text-3xl font-bold text-white mb-2 md:mb-3 drop-shadow-lg">
                {{ bannerData.title }}
              </h1>
              <p class="text-white text-sm md:text-lg drop-shadow-md">
                {{ bannerData.subtitle }}
              </p>
              <p class="mt-2 text-sm text-gray-300">
                {{ bannerData.description }}
              </p>
            </div>
          </div>
        </div>

        <!-- 路由內容 -->
        <router-view></router-view>

        <AIChatAssistant />
      </div>

      <!-- Footer -->
      <AdminFooter />
    </div>

    <!-- 手機版側邊欄遮罩 -->
    <div v-if="!isSidebarCollapsed && windowWidth < 768"
         class="fixed inset-0 bg-black/60 backdrop-blur-sm z-30"
         @click="toggleSidebar">
    </div>
  </div>
</template>

<script>
import AdminNavbar from './common/AdminNavbar.vue'
import AdminFooter from './common/AdminFooter.vue'
import axios from '@/utils/axios'
import Swal from 'sweetalert2'
import AIChatAssistant from '@/components/chat/AIChatAssistant.vue'
import { onBeforeMount, onMounted, ref, onUnmounted, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { menuAPI } from '@/api'
import accountApi from '@/api/modules/account'
import { useAuthStore } from '@/stores/auth'
import bannerApi from '@/api/modules/banner'

export default {
  name: 'AdminLayout',
  components: {
    AdminNavbar,
    AdminFooter,
    AIChatAssistant
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const tokenExpireTime = ref(null)
    const remainingTime = ref(0)
    const timerInterval = ref(null)
    const tokenCheckInterval = ref(null)
    const menus = ref([])
    const loading = ref(false)
    const openMenus = ref({})
    const isSidebarCollapsed = ref(false)
    const isSidebarVisible = ref(true)
    const userInfo = ref({
      username: '',
      email: '',
      avatar: ''
    })
    const defaultAvatar = 'https://api.dicebear.com/7.x/avataaars/svg?seed=default'
    const windowWidth = ref(window.innerWidth)
    const theme = ref('light')
    const authStore = useAuthStore()
    const bannerData = ref({})
    const isTokenVerified = ref(false)
    const isLoading = ref(false)
    const isCheckingAuth = ref(false)
    
    // 動態載入 CSS
    const loadThemeCSS = async (themeName) => {
      // 移除所有主題相關的 style 標籤
      const existingStyles = document.querySelectorAll('style[data-theme]')
      existingStyles.forEach(style => style.remove())

      try {
        // 使用 glob 導入 CSS
        const themes = import.meta.glob('../../assets/css/*.css', { query: '?inline' })
        const cssPath = `../../assets/css/${themeName}.css`
        if (themes[cssPath]) {
          const cssModule = await themes[cssPath]()
          
          // 創建新的 style 元素
          const styleElement = document.createElement('style')
          styleElement.setAttribute('data-theme', themeName)
          styleElement.setAttribute('data-priority', 'high')
          styleElement.textContent = cssModule.default
          document.head.appendChild(styleElement)
          
          // 強制重新應用樣式
          document.documentElement.className = ''
          requestAnimationFrame(() => {
            document.documentElement.className = themeName
          })
        }
      } catch (error) {
        console.error('載入主題 CSS 失敗:', error)
      }
    }
    
    // 同步主題設置
    const syncTheme = async () => {
      const savedTheme = localStorage.getItem('theme')
      theme.value = savedTheme || 'light'
      await loadThemeCSS(theme.value)
    }
    
    // 切換主題
    const toggleTheme = async () => {
      theme.value = theme.value === 'dark' ? 'light' : 'dark'
      localStorage.setItem('theme', theme.value)
      await loadThemeCSS(theme.value)
    }
    
    // 監聽主題變化
    const handleThemeChange = async (e) => {
      if (e.key === 'theme') {
        theme.value = e.newValue
        await loadThemeCSS(e.newValue)
      }
    }

    // 監聽路由變化
    router.beforeEach((to, from, next) => {
      isLoading.value = true
      next()
    })

    router.afterEach(() => {
      // 添加短暫延遲以確保動畫效果
      setTimeout(() => {
        isLoading.value = false
      }, 500)
    })

    onMounted(async () => {
      window.addEventListener('storage', handleThemeChange)
      await syncTheme()
      await fetchBannerData()
    })

    onUnmounted(() => {
      window.removeEventListener('storage', handleThemeChange)
      window.removeEventListener('storage', () => {})
    })

    // 開始計時器
    const startExpirationTimer = () => {
      // 防止重複啟動
      if (timerInterval.value || tokenCheckInterval.value) {
        console.log('Timer 已存在，不重複啟動')
        return
      }
      // 從 localStorage 獲取登入時間戳
      const loginTime = localStorage.getItem('loginTime')
      if (!loginTime) {
        // 如果沒有登入時間，記錄當前時間
        localStorage.setItem('loginTime', Date.now().toString())
      }
      
      // 計算剩餘秒數
      const currentTime = Date.now()
      const loginTimeStamp = parseInt(localStorage.getItem('loginTime'))
      const elapsedSeconds = Math.floor((currentTime - loginTimeStamp) / 1000)
      const totalSeconds = Math.floor(import.meta.env.VITE_JWT_EXPIRES_IN)  // 一天的秒數
      const remainingSeconds = Math.max(0, totalSeconds - elapsedSeconds)
      
      console.log('登入時間:', new Date(loginTimeStamp).toLocaleString())
      console.log('當前時間:', new Date(currentTime).toLocaleString())
      console.log('已經過時間:', elapsedSeconds, '秒')
      console.log('剩餘時間:', remainingSeconds, '秒')
      
      // 如果已經過期，執行登出
      if (remainingSeconds <= 0) {
        handleLogout()
        return
      }
      
      // 設置初始剩餘時間
      remainingTime.value = remainingSeconds
      
      // 設置倒數計時器
      timerInterval.value = setInterval(() => {
        remainingTime.value--
        if (remainingTime.value <= 0) {
          clearInterval(timerInterval.value)
          handleLogout()
        }
      }, 1000)

      // 設置 token 檢查計時器
      tokenCheckInterval.value = setInterval(async () => {
        try {
          console.log('執行 token 檢查...')
          await axios.get('/users/verify')
          console.log('Token 驗證成功')
        } catch (error) {
          if (error.response?.status === 401 || 
              error.response?.data?.code === 403 ||
              error.response?.data?.msg === 'permission error') {
            console.error('Token 驗證失敗 (未授權):', error)
            await handleLogout()
          } else {
            console.error('Token 驗證其他錯誤:', error)
          }
        }
      }, parseInt(import.meta.env.VITE_CHECK_TOKEN_INTERVAL)) // 預設 1 小時
    }

    // 格式化時間
    const formatTime = (seconds) => {
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      const remainingSeconds = seconds % 60
      
      const parts = []
      if (hours > 0) parts.push(`${hours}時`)
      if (minutes > 0 || hours > 0) parts.push(`${minutes}分`)
      parts.push(`${remainingSeconds}秒`)
      
      return parts.join('')
    }

    // 處理 token 過期
    const handleLogout = async () => {
      try {
        // 先清除計時器
        clearInterval(timerInterval.value)
        clearInterval(tokenCheckInterval.value)
        timerInterval.value = null
        tokenCheckInterval.value = null
        
        // 重置驗證狀態
        isTokenVerified.value = false

        await Swal.fire({
          icon: 'warning',
          title: '登入已過期',
          text: '請重新登入',
          confirmButtonText: '確定',
          allowOutsideClick: false
        })
        
        // 使用 auth store 的 clearAuth 方法
        await authStore.clearAuth()

        // 清除所有本地存儲
        localStorage.clear()
        
        // 重置計時相關的狀態
        remainingTime.value = 0
        tokenExpireTime.value = null
        
        router.push('/login')
      } catch (error) {
        console.error('登出失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '登出失敗',
          text: '請稍後再試',
          confirmButtonText: '確定'
        })
      }
    }

    // 主動登出
    const logout = async () => {
      try {
        // 先詢問用戶是否確定要登出
        const result = await Swal.fire({
          title: '確定要登出嗎？',
          icon: 'question',
          showCancelButton: true,
          confirmButtonText: '確定',
          cancelButtonText: '取消',
          confirmButtonColor: '#dc2626',
          cancelButtonColor: '#6b7280',
        })
        
        if (result.isConfirmed) {
          // 清除計時器
          clearInterval(timerInterval.value)
          clearInterval(tokenCheckInterval.value)
          timerInterval.value = null
          tokenCheckInterval.value = null
          
          await accountApi.logout()
          
          // 使用 auth store 的 clearAuth 方法
          await authStore.clearAuth()

          // 清除所有本地存儲
          localStorage.clear()
          
          // 重置計時相關的狀態
          remainingTime.value = 0
          tokenExpireTime.value = null
          
          router.push('/login')
          
          await Swal.fire({
            icon: 'success',
            title: '已成功登出',
            timer: 1500,
            showConfirmButton: false
          })
        }
      } catch (error) {
        console.error('登出失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '登出失敗',
          text: '請稍後再試',
          confirmButtonText: '確定'
        })
      }
    }

    // 檢查用戶是否已登入
    const checkAuth = async () => {
      // 如果已經驗證過，或正在驗證，直接返回 true
      if (isTokenVerified.value || isCheckingAuth.value) {
        return true
      }
      isCheckingAuth.value = true

      const token = localStorage.getItem('token')
      const user = localStorage.getItem('user')

      if (!token || !user) {
        await Swal.fire({
          icon: 'error',
          title: '未授權訪問',
          text: '請先登入後再訪問管理後台',
          confirmButtonText: '確定',
          allowOutsideClick: false
        })
        router.push('/login')
        isCheckingAuth.value = false
        return false
      }

      try {
        const response = await axios.get('/users/verify')
        if (response.status === 200) {
          startExpirationTimer() // 驗證成功後開始計時
          await syncTheme() // 同步主題設置
          isTokenVerified.value = true  // 標記已驗證
          isCheckingAuth.value = false
          return true
        }
        isCheckingAuth.value = false
        return false
      } catch (error) {
        console.error('Token 驗證失敗:', error)
        await handleLogout()
        isCheckingAuth.value = false
        return false
      }
    }

    // 修改 onBeforeMount
    onBeforeMount(async () => {
      // 只在未驗證時執行一次檢查
      if (!isTokenVerified.value) {
        await checkAuth()
      }
    })

    // 組件卸載時清理計時器
    onUnmounted(() => {
      console.log('組件卸載，清理計時器')
      if (timerInterval.value) {
        clearInterval(timerInterval.value)
        timerInterval.value = null
      }
      if (tokenCheckInterval.value) {
        clearInterval(tokenCheckInterval.value)
        tokenCheckInterval.value = null
      }
    })

    const getAvatarUrl = computed(() => {
      const user = JSON.parse(localStorage.getItem('user'))
      
      if (!user) return defaultAvatar
      
      if (!user.avatar) return defaultAvatar
      
      // 判斷是否為完整的 URL（Google 頭像）
      if (user.avatar.startsWith('http')) {
        return user.avatar
      }
      
      // 本地上傳的頭像
      if (user.avatar.includes('/')) {
        // 已經是完整路徑
        return `${import.meta.env.VITE_BACKEND_URL}/api/users/avatar/${user.avatar.split('/').pop()}`
      } else {
        // 只有檔名
        return `${import.meta.env.VITE_BACKEND_URL}/uploads/avatars/${user.avatar}`
      }
    })

    // 獲取後台 banner 數據
    const fetchBannerData = async () => {
      try {
        // 獲取當前路由名稱並轉換為小寫
        const currentRouteName = route.name?.toLowerCase() || ''
        console.log('currentRouteName', currentRouteName)
        // 構建特定路由的 banner_type
        const specificBannerType = `admin_${currentRouteName}`
        console.log('specificBannerType', specificBannerType)
        // 先嘗試獲取特定路由的 banner
        let response = await bannerApi.getBannersByType(specificBannerType)
        console.log('response_current', response.data)
        // 如果沒有找到特定路由的 banner，則獲取通用後台 banner
        if (!response.data?.data?.length) {
          response = await bannerApi.getBannersByType('admin')
          console.log('response_admin', response.data)
        }
        
        if (response.data?.data?.length > 0) {
          bannerData.value = response.data.data[0]
        }
      } catch (error) {
        console.error('獲取後台 banner 數據失敗:', error)
      }
    }

    // 監聽路由變化時重新獲取 banner
    watch(() => route.name, () => {
      fetchBannerData()
    }, { immediate: true })

    return {
      remainingTime,
      formatTime,
      startExpirationTimer,
      menus,
      loading,
      openMenus,
      isSidebarCollapsed,
      isSidebarVisible,
      userInfo,
      defaultAvatar,
      windowWidth,
      theme,
      syncTheme,
      toggleTheme,
      getAvatarUrl,
      handleLogout,
      logout,
      bannerData,
      isLoading
    }
  },
  computed: {
    menuCategories() {
      // 根據 section_order 排序類別
      const categories = [...new Set(this.menus.map(menu => menu.category))]
      return categories.sort((a, b) => {
        const menuA = this.menus.find(m => m.category === a)
        const menuB = this.menus.find(m => m.category === b)
        return (menuA?.section_order || 0) - (menuB?.section_order || 0)
      })
    },
    sortedMenus() {
      return (category) => {
        // 根據 sort_order 排序該類別下的選單
        return this.menus
          .filter(menu => menu.category === category)
          .sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0))
      }
    }
  },
  methods: {
    updateMenuState() {
      const currentPath = this.$route.path
      const newOpenMenus = {}
      
      // 先將所有選單設為關閉狀態
      this.menuCategories.forEach(category => {
        newOpenMenus[category] = false
      })
      
      // 找到當前路徑所屬的類別
      for (const category of this.menuCategories) {
        const categoryMenus = this.sortedMenus(category)
        if (categoryMenus.some(menu => currentPath.includes(menu.path))) {
          // 只打開當前路徑所屬的類別
          newOpenMenus[category] = true
          break // 找到後就跳出循環
        }
      }
      
      // 特殊處理：如果是儀表板，則全部折疊
      if (currentPath === '/admin') {
        Object.keys(newOpenMenus).forEach(key => {
          newOpenMenus[key] = false
        })
      }
      
      this.openMenus = newOpenMenus
    },
    toggleMenu(category) {
      // 關閉其他所有選單
      const newOpenMenus = {}
      this.menuCategories.forEach(cat => {
        newOpenMenus[cat] = cat === category ? !this.openMenus[category] : false
      })
      
      this.openMenus = newOpenMenus
    },
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed
    },
    async getUserInfo() {
      try {
        const token = localStorage.getItem('token')
        console.log('從 AdminLayout 獲取的 token:', token)
        if (!token) {
          console.warn('No token found')
          this.router.push('/login')
          return
        }

        const response = await axios.get('/users/verify')
        if (response.data && response.data.user_id) {
          const userResponse = await axios.get(`/users/${response.data.user_id}`)
          this.userInfo = userResponse.data
        }
      } catch (error) {
        console.error('獲取用戶信息失敗:', error)
        localStorage.removeItem('token')
        this.router.push('/login')
      }
    },
    handleResize() {
      if (window.innerWidth >= 1024) {
        this.isSidebarVisible = true
      }
    },
    handleAvatarError(e) {
      console.error('頭像加載失敗，使用默認頭像')
      e.target.src = this.defaultAvatar
    },
    isCurrentRoute(path) {
      return this.$route.path === path
    },
    async fetchMenus() {
      try {
        this.loading = true
        const response = await menuAPI.getMenus()
        this.menus = response.data.menus || []
        // 初始化選單狀態
        const initialOpenMenus = {}
        this.menuCategories.forEach(category => {
          initialOpenMenus[category] = false
        })
        this.openMenus = initialOpenMenus
        // 根據當前路由設置選單狀態
        this.updateMenuState()
      } catch (error) {
        console.error('獲取選單失敗:', error)
      } finally {
        this.loading = false
      }
    },
    handleWindowResize() {
      this.windowWidth = window.innerWidth
      // 在大螢幕時展開，小螢幕時收合
      if (window.innerWidth >= 768) {
        this.isSidebarCollapsed = false
      } else {
        this.isSidebarCollapsed = true
      }
    },
    handleMenuClick() {
      // 只在小螢幕下自動收合側邊欄
      if (window.innerWidth < 768) {
        this.isSidebarCollapsed = true
      }
    }
  },
  watch: {
    // 監聽路由變化，自動更新選單狀態
    '$route'() {
      this.updateMenuState()
      if (window.innerWidth < 768) {
        this.isSidebarCollapsed = true
      }
    }
  },
  async created() {
    await this.fetchMenus()
    // 根據當前路由設置初始選單狀態
    this.updateMenuState()
  },
  mounted() {
    // 獲取用戶信息
    this.getUserInfo()
    window.addEventListener('resize', this.handleResize)
    this.handleResize()
    this.windowWidth = window.innerWidth
    window.addEventListener('resize', this.handleWindowResize)
    // 初始化時根據螢幕寬度設置側邊欄狀態
    this.handleWindowResize()
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize)
    window.removeEventListener('resize', this.handleWindowResize)
  }
}
</script>

<style scoped>
/* 基礎樣式 */
.banner-bg {
  background-attachment: fixed;
  background-position: center center;
  background-repeat: no-repeat;
  background-size: cover;
  height: 300px;
  position: relative;
}

@screen md {
  .banner-bg {
    min-height: 240px;
  }
}

/* 文字陰影效果 */
.text-white {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

/* 移除原有的動態光影效果 */
.banner-bg::after {
  display: none;
}

/* 可以根據需要調整以下樣式 */
.text-gray-200 {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* 添加過渡效果 */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

/* 優化滾動條 */
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 2px;
}

/* 側邊欄收合時的過渡效果 */
aside {
  visibility: visible;
  opacity: 1;
}

aside.w-0 {
  visibility: hidden;
  opacity: 0;
}

/* 預載入動畫相關樣式 */
@keyframes fadeIn {
  from { 
    opacity: 0;
    transform: scale(0.95);
  }
  to { 
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes fadeOut {
  from { 
    opacity: 1;
    transform: scale(1);
  }
  to { 
    opacity: 0;
    transform: scale(0.95);
  }
}

.fixed {
  animation: fadeIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fixed.hidden {
  animation: fadeOut 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 添加漸變背景效果 */
.bg-white\/80, .dark\:bg-gray-900\/80 {
  backdrop-filter: blur(8px);
  transition: background-color 0.3s ease;
}
</style> 