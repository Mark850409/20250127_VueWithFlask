<template>
  <div class="min-h-screen bg-gray-100 flex">
    <!-- 側邊欄 -->
    <aside :class="[
      'fixed top-0 left-0 h-full bg-white border-r z-30 flex flex-col transition-all duration-300',
      isSidebarCollapsed ? 'w-0' : 'w-64'
    ]">
      <!-- Logo -->
      <div class="flex-shrink-0 flex items-center justify-center h-16 border-b px-6 overflow-hidden">
        <div class="flex items-center">
          <img src="https://api.dicebear.com/7.x/bottts/svg?seed=food" 
               alt="Logo" 
               class="h-8 w-8">
          <span class="ml-3 text-xl font-semibold whitespace-nowrap">
            推薦系統
          </span>
        </div>
      </div>

      <!-- 使用者資訊 -->
      <div class="flex-shrink-0 p-4 border-b overflow-hidden">
        <div class="flex items-center space-x-3">
          <img :src="getAvatarUrl"
               alt="User Avatar" 
               class="w-10 h-10 rounded-full flex-shrink-0"
               @error="handleAvatarError">
          <div class="overflow-hidden">
            <div class="font-medium text-gray-700 truncate">{{ userInfo.username }}</div>
            <div class="text-sm text-gray-500 truncate">{{ userInfo.email }}</div>
          </div>
        </div>
      </div>

      <!-- 選單 -->
      <div class="flex-1 overflow-y-auto px-4 py-4">
        <div class="space-y-4 overflow-hidden">
          <!-- Navigation 分類標題 -->
          <div v-if="!isSidebarCollapsed" class="px-4 pt-2">
            <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider">ADMIN</h3>
          </div>

          <!-- Dashboard -->
          <router-link to="/admin" 
            class="flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors duration-150"
            :class="[
              $route.path === '/admin' 
                ? 'text-blue-600 bg-blue-50' 
                : 'text-gray-700 hover:bg-gray-100'
            ]">
            <div class="flex-shrink-0 w-6">
              <i class="fas fa-home text-lg"></i>
            </div>
            <div class="ml-3 flex-1" v-if="!isSidebarCollapsed">
              <div>儀錶板管理</div>
            </div>
          </router-link>

          <!-- Apps 分類標題 -->
          <div v-if="!isSidebarCollapsed" class="px-4 pt-4">
            <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider">Apps</h3>
          </div>

          <!-- 動態生成的選單 -->
          <template v-for="category in menuCategories" :key="category">
            <div class="space-y-1">
              <!-- 主選單 -->
              <div class="flex items-center px-4 py-3 text-sm font-medium rounded-lg cursor-pointer"
                   :class="[
                     sortedMenus(category).some(menu => $route.path.includes(menu.path)) || openMenus[category]
                       ? 'text-blue-600 bg-blue-50' 
                       : 'text-gray-700 hover:bg-gray-100'
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
                            class="flex items-center px-4 py-2.5 text-sm rounded-lg transition-colors duration-150"
                            :class="[
                              $route.path === menu.path
                                ? 'text-blue-600 bg-blue-50'
                                : 'text-gray-600 hover:bg-gray-100'
                            ]">
                  <i :class="[menu.icon, 'text-lg w-6']"></i>
                  <span class="ml-3">{{ menu.name }}</span>
                </router-link>
              </div>
            </div>
          </template>
        </div>
      </div>

      <!-- 登出按鈕 -->
      <div v-show="!isSidebarCollapsed" class="flex-shrink-0 p-3 border-t">
        <button @click="logout" 
          class="flex items-center justify-center w-full px-4 py-2.5 text-gray-700 hover:bg-gray-100 rounded-lg">
          <i class="fas fa-sign-out-alt text-lg w-6"></i>
          <span class="ml-3">登出</span>
        </button>
      </div>
    </aside>

    <!-- 主要內容區域 -->
    <div class="flex-1 flex flex-col transition-all duration-300"
         :class="[
           isSidebarCollapsed ? 'ml-0' : 'ml-64'
         ]">
      <!-- Navbar -->
      <AdminNavbar 
        :isSidebarCollapsed="isSidebarCollapsed"
        @toggle-sidebar="toggleSidebar"
        :remainingTime="remainingTime"
        :formatTime="formatTime"
      />

      <!-- 內容區域 -->
      <div class="flex-1 p-6 mt-4">
        <!-- Banner -->
        <div class="bg-white shadow-sm rounded-lg overflow-hidden mb-6">
          <div class="relative banner-bg">
            <div class="absolute inset-0 bg-gradient-to-r from-gray-900/80 to-gray-800/80"></div>
            <div class="relative px-8 py-16">
              <h1 class="text-3xl font-bold text-white mb-3">
                {{ getBannerTitle }}
              </h1>
              <p class="text-gray-200 text-lg">
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
  </div>
</template>

<script>
import AdminNavbar from './common/AdminNavbar.vue'
import AdminFooter from './common/AdminFooter.vue'
import axios from '@/utils/axios'
import Swal from 'sweetalert2'
import { onBeforeMount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { menuAPI } from '@/api'

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
    let timerInterval = null
    const menus = ref([])
    const loading = ref(false)

    // 開始計時器
    const startExpirationTimer = () => {
      const expiresIn = parseInt(import.meta.env.VITE_JWT_EXPIRES_IN || '10') // 從環境變數讀取，預設10秒
      tokenExpireTime.value = Date.now() + (expiresIn * 1000)
      remainingTime.value = expiresIn

      // 清除舊的計時器
      if (timerInterval) clearInterval(timerInterval)

      // 設置新的計時器
      timerInterval = setInterval(() => {
        const now = Date.now()
        const timeLeft = Math.max(0, Math.ceil((tokenExpireTime.value - now) / 1000))
        remainingTime.value = timeLeft

        if (timeLeft <= 0) {
          clearInterval(timerInterval)
          handleTokenExpiration()
        }
      }, 1000)
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
    const handleTokenExpiration = async () => {
      clearInterval(timerInterval)
      await Swal.fire({
        icon: 'warning',
        title: '登入已過期',
        text: '請重新登入',
        confirmButtonText: '確定',
        allowOutsideClick: false
      })
      localStorage.removeItem('token')
      localStorage.removeItem('user')
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
        // 驗證 token 是否有效
        await axios.get('/users/verify')
        startExpirationTimer() // 驗證成功後開始計時
        return true
      } catch (error) {
        console.error('Token 驗證失敗:', error)
        await Swal.fire({
          icon: 'error',
          title: '登入已過期',
          text: '請重新登入',
          confirmButtonText: '確定',
          allowOutsideClick: false
        })
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        router.push('/login')
        return false
      }
    }

    onBeforeMount(async () => {
      await checkAuth()
    })

    // 組件卸載時清理計時器
    onMounted(() => {
      if (timerInterval) clearInterval(timerInterval)
    })

    return {
      remainingTime,
      formatTime,
      startExpirationTimer,
      menus,
      loading
    }
  },
  data() {
    return {
      openMenus: {}, // 初始化為空對象
      isSidebarCollapsed: false,
      isSidebarVisible: true,
      userInfo: {
        username: '',
        email: '',
        avatar: ''
      },
      defaultAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=default'
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
        'Dashboard': '儀表板管理',
        'AccountManagement': '帳號管理',
        'LogManagement': '日誌管理',
        'MenuManagement': '選單管理',
        'ShopManagement': '飲料店管理',
        'RatingManagement': '評分管理',
        'CommentManagement': '留言板管理',
        'UserManagement': '管理員管理',
        'FavoriteManagement': '最愛管理',
        'GitManagement': '版控管理',
      }
      return titles[route] || '後台管理系統'
    },
    getBannerDescription() {
      const route = this.$route.name
      const descriptions = {
        'Dashboard': '查看系統整體運營狀況和關鍵指標',
        'AccountManagement': '管理系統用戶帳號和權限設定',
        'LogManagement': '查看系統操作日誌和異常記錄',
        'MenuManagement': '管理系統選單結構和權限',
        'ShopManagement': '管理合作飲料店資訊和狀態',
        'RatingManagement': '管理用戶評分與評論內容',
        'CommentManagement': '管理用戶留言與討論內容',
        'UserManagement': '管理使用者個人資料設定',
        'FavoriteManagement': '管理用戶收藏的飲品項目',
        'GitManagement': '管理系統版本控制和代碼更新',
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
    toggleMenu(menu) {
      const newOpenMenus = { ...this.openMenus }
      
      // 切換當前選單的狀態
      newOpenMenus[menu] = !newOpenMenus[menu]
      
      // 如果是打開當前選單，則關閉其他選單
      if (newOpenMenus[menu]) {
        Object.keys(newOpenMenus).forEach(key => {
          if (key !== menu) {
            newOpenMenus[key] = false
          }
        })
      }
      
      this.openMenus = newOpenMenus
    },
    // 根據當前路由自動展開對應的選單
    updateMenuState() {
      const path = this.$route.path
      const newOpenMenus = { ...this.openMenus }
      
      // 根據路徑決定要展開哪個選單
      if (path.includes('/admin/system') || path.includes('/admin/accounts') || 
          path.includes('/admin/logs') || path.includes('/admin/menus') ||
          path.includes('/admin/git')) {
        newOpenMenus['系統管理'] = true
      } else if (path.includes('/admin/shops') || path.includes('/admin/ratings') || 
                path.includes('/admin/comments')) {
        newOpenMenus['點餐管理'] = true
      } else if (path.includes('/admin/users') || path.includes('/admin/favorites')) {
        newOpenMenus['個人設定管理'] = true
      }
      
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
    }
  },
  watch: {
    // 監聽路由變化，自動更新選單狀態
    '$route'() {
      this.updateMenuState()
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
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize)
  }
}
</script>

<style scoped>
/* 自定義滾動條樣式 */
nav::-webkit-scrollbar {
  width: 3px;
}

nav::-webkit-scrollbar-track {
  background: transparent;
}

nav::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.3);
  border-radius: 3px;
}

nav::-webkit-scrollbar-thumb:hover {
  background-color: rgba(156, 163, 175, 0.5);
}

.banner-bg {
  background-image: url('https://images.unsplash.com/photo-1499638673689-79a0b5115d87?w=1000');
  background-size: cover;
  background-position: center;
  min-height: 240px; /* 增加最小高度 */
}

/* 移除之前的 Banner 相關樣式 */
.relative.px-8.py-8,
.flex-1.p-6.mt-16,
.bg-white.shadow-sm.rounded-lg.overflow-hidden.mb-6 {
  /* 移除這些樣式，改用直接在元素上設置 class */
}

/* 可以根據需要調整以下樣式 */
.text-gray-200 {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.text-white {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

/* 添加過渡效果 */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}
</style> 