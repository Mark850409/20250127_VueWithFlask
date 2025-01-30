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
          <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=admin" 
               alt="User Avatar" 
               class="w-10 h-10 rounded-full flex-shrink-0">
          <div class="overflow-hidden">
            <div class="font-medium text-gray-700 truncate">管理員</div>
            <div class="text-sm text-gray-500 truncate">admin@example.com</div>
          </div>
        </div>
      </div>

      <!-- 選單 -->
      <div class="flex-1 overflow-y-auto px-4 py-4">
        <div class="space-y-4 overflow-hidden">
          <!-- Navigation 分類標題 -->
          <div v-if="!isSidebarCollapsed" class="px-4 pt-2">
            <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider">Navigation</h3>
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
              <div>Dashboards</div>
            </div>
          </router-link>

          <!-- Apps 分類標題 -->
          <div v-if="!isSidebarCollapsed" class="px-4 pt-4">
            <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider">Apps</h3>
          </div>

          <!-- 系統管理 -->
          <div class="space-y-1">
            <div class="flex items-center px-4 py-3 text-sm font-medium rounded-lg cursor-pointer"
                 :class="[
                   $route.path.includes('/admin/system') || openMenus.system
                     ? 'text-blue-600 bg-blue-50' 
                     : 'text-gray-700 hover:bg-gray-100'
                 ]"
                 @click="toggleMenu('system')">
              <div class="flex-shrink-0 w-6">
                <i class="fas fa-cog text-lg"></i>
              </div>
              <div class="ml-3 flex-1" v-if="!isSidebarCollapsed">
                <div>系統管理</div>
              </div>
              <i v-if="!isSidebarCollapsed" 
                 class="fas fa-chevron-right text-sm transition-transform duration-200"
                 :class="{ 'transform rotate-90': openMenus.system }"></i>
            </div>

            <!-- 子選單 -->
            <div v-show="openMenus.system && !isSidebarCollapsed" 
                 class="pl-4 ml-4 space-y-2 border-l border-gray-200 py-2">
              <router-link to="/admin/accounts" 
                class="flex items-center px-4 py-2.5 text-sm rounded-lg transition-colors duration-150"
                :class="[
                  $route.path === '/admin/accounts'
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-gray-600 hover:bg-gray-100'
                ]">
                <i class="fas fa-users text-lg w-6"></i>
                <span class="ml-3">帳號管理</span>
              </router-link>
              <router-link to="/admin/git" 
                class="flex items-center px-4 py-2.5 text-sm rounded-lg transition-colors duration-150"
                :class="[
                  $route.path === '/admin/git'
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-gray-600 hover:bg-gray-100'
                ]">
                <i class="fab fa-git-alt text-lg w-6"></i>
                <span class="ml-3">版控管理</span>
              </router-link>
              <router-link to="/admin/logs" 
                class="flex items-center px-4 py-2 text-sm rounded-lg transition-colors duration-150"
                :class="[
                  $route.path === '/admin/logs'
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-gray-600 hover:bg-gray-100'
                ]">
                <i class="fas fa-history text-lg w-6"></i>
                <span class="ml-3">日誌管理</span>
              </router-link>
              <router-link to="/admin/menus" 
                class="flex items-center px-4 py-2 text-sm rounded-lg transition-colors duration-150"
                :class="[
                  $route.path === '/admin/menus'
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-gray-600 hover:bg-gray-100'
                ]">
                <i class="fas fa-bars text-lg w-6"></i>
                <span class="ml-3">選單管理</span>
              </router-link>
            </div>
          </div>

          <!-- 點餐管理 -->
          <div class="space-y-1">
            <div class="flex items-center px-4 py-3 text-sm font-medium rounded-lg cursor-pointer"
                 :class="[
                   $route.path.includes('/admin/shops') || 
                   $route.path.includes('/admin/ratings') || 
                   $route.path.includes('/admin/comments') || 
                   openMenus.order
                     ? 'text-blue-600 bg-blue-50' 
                     : 'text-gray-700 hover:bg-gray-100'
                 ]"
                 @click="toggleMenu('order')">
              <i class="fas fa-coffee text-lg w-6"></i>
              <span v-if="!isSidebarCollapsed" class="ml-3 flex-1">點餐管理</span>
              <i v-if="!isSidebarCollapsed" 
                 class="fas fa-chevron-right text-sm transition-transform duration-200"
                 :class="{ 'transform rotate-90': openMenus.order }"></i>
            </div>

            <!-- 子選單 -->
            <div v-show="openMenus.order && !isSidebarCollapsed" 
                 class="pl-4 ml-4 space-y-2 border-l border-gray-200 py-2">
              <router-link to="/admin/shops" 
                class="flex items-center px-4 py-2.5 text-sm rounded-lg transition-colors duration-150"
                :class="[
                  $route.path === '/admin/shops'
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-gray-600 hover:bg-gray-100'
                ]">
                <i class="fas fa-store text-lg w-6"></i>
                <span class="ml-3">飲料店管理</span>
              </router-link>
              <router-link to="/admin/ratings" 
                class="flex items-center px-4 py-2.5 text-sm rounded-lg transition-colors duration-150"
                :class="[
                  $route.path === '/admin/ratings'
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-gray-600 hover:bg-gray-100'
                ]">
                <i class="fas fa-star text-lg w-6"></i>
                <span class="ml-3">評分管理</span>
              </router-link>
              <router-link to="/admin/comments" 
                class="flex items-center px-4 py-2.5 text-sm rounded-lg transition-colors duration-150"
                :class="[
                  $route.path === '/admin/comments'
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-gray-600 hover:bg-gray-100'
                ]">
                <i class="fas fa-comments text-lg w-6"></i>
                <span class="ml-3">留言板管理</span>
              </router-link>
            </div>
          </div>

          <!-- 個人設定管理 -->
          <div class="space-y-1">
            <div class="flex items-center px-4 py-3 text-sm font-medium rounded-lg cursor-pointer"
                 :class="[
                   $route.path.includes('/admin/users') || 
                   $route.path.includes('/admin/favorites') || 
                   openMenus.personal
                     ? 'text-blue-600 bg-blue-50' 
                     : 'text-gray-700 hover:bg-gray-100'
                 ]"
                 @click="toggleMenu('personal')">
              <i class="fas fa-user-cog text-lg w-6"></i>
              <span v-if="!isSidebarCollapsed" class="ml-3 flex-1">個人設定管理</span>
              <i v-if="!isSidebarCollapsed" 
                 class="fas fa-chevron-right text-sm transition-transform duration-200"
                 :class="{ 'transform rotate-90': openMenus.personal }"></i>
            </div>

            <!-- 子選單 -->
            <div v-show="openMenus.personal && !isSidebarCollapsed" 
                 class="pl-4 ml-4 space-y-2 border-l border-gray-200 py-2">
              <router-link to="/admin/users" 
                class="flex items-center px-4 py-2.5 text-sm rounded-lg transition-colors duration-150"
                :class="[
                  $route.path === '/admin/users'
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-gray-600 hover:bg-gray-100'
                ]">
                <i class="fas fa-user text-lg w-6"></i>
                <span class="ml-3">使用者管理</span>
              </router-link>
              <router-link to="/admin/favorites" 
                class="flex items-center px-4 py-2.5 text-sm rounded-lg transition-colors duration-150"
                :class="[
                  $route.path === '/admin/favorites'
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-gray-600 hover:bg-gray-100'
                ]">
                <i class="fas fa-heart text-lg w-6"></i>
                <span class="ml-3">最愛管理</span>
              </router-link>
            </div>
          </div>
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

export default {
  name: 'AdminLayout',
  components: {
    AdminNavbar,
    AdminFooter
  },
  data() {
    return {
      openMenus: {
        system: false,
        order: false,
        personal: false
      },
      isSidebarCollapsed: false,
      isSidebarVisible: true
    }
  },
  computed: {
    getBannerTitle() {
      const route = this.$route.name
      const titles = {
        'Dashboard': '儀表板',
        'AccountManagement': '帳號管理',
        'LogManagement': '日誌管理',
        'MenuManagement': '選單管理',
        'ShopManagement': '飲料店管理',
        'RatingManagement': '評分管理',
        'CommentManagement': '留言板管理',
        'UserManagement': '使用者管理',
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
    }
  },
  methods: {
    toggleMenu(menu) {
      // 關閉其他選單，只保持當前選單打開
      Object.keys(this.openMenus).forEach(key => {
        this.openMenus[key] = key === menu ? !this.openMenus[key] : false
      })
    },
    // 根據當前路由自動展開對應的選單
    updateMenuState() {
      const path = this.$route.path
      // 重置所有選單狀態
      Object.keys(this.openMenus).forEach(key => {
        this.openMenus[key] = false
      })
      // 根據路徑決定要展開哪個選單
      if (path.includes('/admin/system') || path.includes('/admin/accounts') || 
          path.includes('/admin/logs') || path.includes('/admin/menus') ||
          path.includes('/admin/git')) {
        this.openMenus.system = true
      } else if (path.includes('/admin/shops') || path.includes('/admin/ratings') || 
                path.includes('/admin/comments')) {
        this.openMenus.order = true
      } else if (path.includes('/admin/users') || path.includes('/admin/favorites')) {
        this.openMenus.personal = true
      }
    },
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed
    },
    logout() {
      // 實作登出邏輯
      this.$router.push('/login')
    },
    handleResize() {
      if (window.innerWidth >= 1024) {
        this.isSidebarVisible = true
      }
    }
  },
  watch: {
    // 監聽路由變化，自動更新選單狀態
    '$route'() {
      this.updateMenuState()
    }
  },
  mounted() {
    // 初始化時設置選單狀態
    this.updateMenuState()
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