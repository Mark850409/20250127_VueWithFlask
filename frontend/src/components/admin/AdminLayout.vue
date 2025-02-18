<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 flex">
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
      <div class="flex-shrink-0 p-4 border-b dark:border-gray-700 overflow-hidden">
        <div class="flex flex-col items-center text-center">
          <img :src="getAvatarUrl"
               alt="User Avatar" 
               class="w-14 h-14 md:w-16 md:h-16 rounded-full mb-2"
               @error="handleAvatarError">
          <div class="overflow-hidden w-full">
            <div class="text-base md:text-lg font-medium text-indigo-600 dark:text-indigo-400 mb-1">
              嗨 ~ {{ userInfo.username }} 你好
            </div>
            <div class="text-xs md:text-sm text-gray-500 dark:text-gray-400">
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
        <button @click="logout" 
          class="flex items-center justify-center w-full px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
          <i class="ri-logout-box-r-line text-lg w-6"></i>
          <span class="ml-3">登出</span>
        </button>
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
      <div class="flex-1 p-3 xs:p-4 md:p-6 mt-4">
        <!-- Banner -->
        <div class="bg-white shadow-sm rounded-lg overflow-hidden mb-6">
          <div class="relative banner-bg">
            <!-- 半透明遮罩 -->
            <div class="absolute inset-0 bg-black/30"></div>
            
            <!-- Banner 內容 -->
            <div class="relative px-4 md:px-8 py-8 md:py-16">
              <h1 class="text-xl md:text-3xl font-bold text-white mb-2 md:mb-3 drop-shadow-lg">
                {{ getBannerTitle }}
              </h1>
              <p class="text-white text-sm md:text-lg drop-shadow-md">
                {{ getBannerDescription }}
              </p>
            </div>
          </div>
        </div>

        <!-- 路由內容 -->
        <router-view></router-view>
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
import { onBeforeMount, onMounted, ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { menuAPI } from '@/api'
import os from 'os'

export default {
  name: 'AdminLayout',
  components: {
    AdminNavbar,
    AdminFooter
  },
  setup() {
    const router = useRouter()
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

    // 開始計時器
    const startExpirationTimer = () => {
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
      
      // 清除現有的計時器
      if (timerInterval.value) clearInterval(timerInterval.value)
      if (tokenCheckInterval.value) clearInterval(tokenCheckInterval.value)
      
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
          console.log('執行token 檢查...')
          await axios.get('/users/verify')
          console.log('Token 驗證成功')
        } catch (error) {
          // 只有在特定錯誤碼時才登出
          if (error.response?.status === 401 || 
              error.response?.data?.code === 403 ||
              error.response?.data?.msg === 'permission error') {
            console.error('Token 驗證失敗 (未授權):', error)
            await handleLogout()
          } else {
            console.error('Token 驗證其他錯誤:', error)
          }
        }
      }, parseInt(import.meta.env.VITE_CHECK_TOKEN_INTERVAL))  // 預設 1 小時
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
      // 先清除計時器
      clearInterval(timerInterval.value)
      clearInterval(tokenCheckInterval.value)
      timerInterval.value = null
      tokenCheckInterval.value = null
      
      await Swal.fire({
        icon: 'warning',
        title: '登入已過期',
        text: '請重新登入',
        confirmButtonText: '確定',
        allowOutsideClick: false
      })
      
      // 清除所有相關的 localStorage 項目
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      localStorage.removeItem('loginTime')
      
      // 重置計時相關的狀態
      remainingTime.value = 0
      tokenExpireTime.value = null
      
      router.push('/login')
    }

    // 檢查用戶是否已登入
    const checkAuth = async () => {
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
        return false
      }

      try {
        // 只在初始化時進行一次驗證，之後由計時器定期檢查
        const response = await axios.get('/users/verify')
        if (response.status === 200) {
          startExpirationTimer() // 驗證成功後開始計時
        }
        return true
      } catch (error) {
        console.error('Token 驗證失敗:', error)
        await handleLogout()
        return false
      }
    }

    onBeforeMount(async () => {
      await checkAuth()
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
      windowWidth
    }
  },
  computed: {
    getAvatarUrl() {
      if (this.userInfo.avatar) {
        return `${import.meta.env.VITE_BACKEND_URL}/api/users/avatar/${this.userInfo.avatar.split('/').pop()}`
      }
      return this.defaultAvatar
    },
    getBannerTitle() {
      const route = this.$route.name
      const titles = {
        Dashboard: '儀表板管理',
        AccountManagement: '帳號管理',
        LogManagement: '日誌管理',
        MenuManagement: '選單管理',
        ShopManagement: '飲料店管理',
        RatingManagement: '評分管理',
        CommentManagement: '留言板管理',
        UserManagement: '管理員管理',
        FavoriteManagement: '最愛管理',
        GitManagement: '版控管理',
        BotManagement: '快速提問管理',
        KnowledgeManagement: '知識庫管理',
        MonitorManagement: '機器人監控管理',
        ProjectManagement: '專案管理',
        BannerManagement: '輪播圖管理',
        LearningManagement: '學習中心管理'
      }
      return titles[route] || '後台管理系統'
    },
    getBannerDescription() {
      const route = this.$route.name
      const descriptions = {
        Dashboard: '查看系統整體運營狀況和關鍵指標',
        AccountManagement: '管理系統用戶帳號和權限設定',
        LogManagement: '查看系統操作日誌和異常記錄',
        MenuManagement: '管理系統選單結構和權限',
        ShopManagement: '管理合作飲料店資訊和狀態',
        RatingManagement: '管理用戶評分與評論內容',
        CommentManagement: '管理用戶留言與討論內容',
        UserManagement: '管理使用者個人資料設定',
        FavoriteManagement: '管理用戶收藏的飲品項目',
        GitManagement: '管理系統版本控制和代碼更新',
        BotManagement: '管理快速提問設定',
        KnowledgeManagement: '管理知識庫設定',
        MonitorManagement: '機器人監控管理',
        ProjectManagement: '管理專案設定',
        BannerManagement: '管理輪播圖設定',
        LearningManagement: '管理學習中心'
      }
      return descriptions[route] || '歡迎使用後台管理系統'
    },
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
    async logout() {
      try {
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
          await axios.post('/users/logout')
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          localStorage.removeItem('loginTime')
          this.$router.push('/login')
          
          Swal.fire({
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
  background-image: url('https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1920&auto=format&fit=crop');
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-position: center;
  background-size: cover;
  min-height: 180px;
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

/* RWD 樣式 */
/* 手機版 (小於 640px) */
@media (max-width: 639px) {
  .banner-bg {
    min-height: 180px;
  }
  
  /* 調整內容區域的間距 */
  .flex-1.p-6 {
    padding: 1rem;
  }
  
  /* 調整 Banner 內容的間距和字體大小 */
  .banner-bg .px-8.py-16 {
    padding: 1.5rem 1rem;
  }
  
  .banner-bg h1 {
    font-size: 1.5rem;
  }
  
  .banner-bg p {
    font-size: 1rem;
  }
}

/* 平板版 (640px - 1023px) */
@media (min-width: 640px) and (max-width: 1023px) {
  .banner-bg {
    min-height: 200px;
  }
  
  /* 調整側邊欄寬度 */
  .w-64 {
    width: 16rem;
  }
  
  /* 調整內容區域的間距 */
  .flex-1.p-6 {
    padding: 1.5rem;
  }
}

/* 電腦版 (大於 1024px) */
@media (min-width: 1024px) {
  /* 保持原有樣式 */
}

/* 確保側邊欄在所有裝置上都能正常顯示 */
.sidebar-transition {
  transition: all 0.3s ease-in-out;
}

/* 確保內容區域在所有裝置上都能正常顯示 */
.content-transition {
  transition: margin-left 0.3s ease-in-out;
}

/* 優化表格和卡片在小螢幕上的顯示 */
@media (max-width: 767px) {
  .overflow-x-auto {
    -webkit-overflow-scrolling: touch;
  }
  
  .grid {
    grid-template-columns: repeat(1, minmax(0, 1fr)) !important;
  }
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

/* 防止側邊欄出現時body滾動 */
@media (max-width: 767px) {
  :root {
    overflow: hidden;
  }
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
</style> 