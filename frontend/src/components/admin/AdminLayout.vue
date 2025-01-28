<template>
  <div class="min-h-screen bg-gray-100">
    <!-- 側邊欄 -->
    <aside class="fixed top-0 left-0 w-64 h-full bg-white shadow-lg z-30 flex flex-col">
      <!-- Logo -->
      <div class="flex-shrink-0 flex items-center justify-center h-16 border-b">
        <img src="https://api.dicebear.com/7.x/bottts/svg?seed=food" alt="Logo" class="h-8 w-8">
        <span class="ml-2 text-lg font-semibold">點餐推薦系統</span>
      </div>

      <!-- 使用者資訊 -->
      <div class="flex-shrink-0 p-4 border-b">
        <div class="flex items-center space-x-3">
          <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=admin" 
               alt="User Avatar" 
               class="w-10 h-10 rounded-full">
          <div>
            <div class="font-medium text-gray-700">管理員</div>
            <div class="text-sm text-gray-500">admin@example.com</div>
          </div>
        </div>
      </div>

      <!-- 選單 - 添加滾動容器 -->
      <nav class="flex-1 overflow-y-auto">
        <div class="px-3 space-y-1 py-4">
          <!-- Dashboard -->
          <router-link to="/admin" 
            class="flex items-center px-4 py-2.5 text-gray-700 hover:bg-gray-100 rounded-lg"
            :class="{ 'bg-gray-100': $route.path === '/admin' }">
            <i class="fas fa-home text-lg w-6"></i>
            <span class="ml-3">Dashboard</span>
          </router-link>

          <!-- 系統管理 -->
          <div>
            <div class="flex items-center px-4 py-2.5 text-gray-700 cursor-pointer hover:bg-gray-100 rounded-lg"
                 @click="toggleMenu('system')">
              <i class="fas fa-cog text-lg w-6"></i>
              <span class="ml-3">系統管理</span>
              <i class="fas fa-chevron-down ml-auto transition-transform duration-200"
                 :class="{ 'transform rotate-180': openMenus.system }"></i>
            </div>
            <div v-show="openMenus.system" class="mt-1 pl-4">
              <router-link to="/admin/accounts" 
                class="flex items-center px-4 py-2.5 text-gray-600 hover:bg-gray-100 rounded-lg">
                <i class="fas fa-users text-lg w-6"></i>
                <span class="ml-3">帳號管理</span>
              </router-link>
              <router-link to="/admin/logs" 
                class="flex items-center px-4 py-2.5 text-gray-600 hover:bg-gray-100 rounded-lg">
                <i class="fas fa-history text-lg w-6"></i>
                <span class="ml-3">日誌管理</span>
              </router-link>
              <router-link to="/admin/menus" 
                class="flex items-center px-4 py-2.5 text-gray-600 hover:bg-gray-100 rounded-lg">
                <i class="fas fa-bars text-lg w-6"></i>
                <span class="ml-3">選單管理</span>
              </router-link>
            </div>
          </div>

          <!-- 點餐管理 -->
          <div>
            <div class="flex items-center px-4 py-2.5 text-gray-700 cursor-pointer hover:bg-gray-100 rounded-lg"
                 @click="toggleMenu('order')">
              <i class="fas fa-coffee text-lg w-6"></i>
              <span class="ml-3">點餐管理</span>
              <i class="fas fa-chevron-down ml-auto transition-transform duration-200"
                 :class="{ 'transform rotate-180': openMenus.order }"></i>
            </div>
            <div v-show="openMenus.order" class="mt-1 pl-4">
              <router-link to="/admin/shops" 
                class="flex items-center px-4 py-2.5 text-gray-600 hover:bg-gray-100 rounded-lg">
                <i class="fas fa-store text-lg w-6"></i>
                <span class="ml-3">飲料店管理</span>
              </router-link>
              <router-link to="/admin/ratings" 
                class="flex items-center px-4 py-2.5 text-gray-600 hover:bg-gray-100 rounded-lg">
                <i class="fas fa-star text-lg w-6"></i>
                <span class="ml-3">評分管理</span>
              </router-link>
              <router-link to="/admin/comments" 
                class="flex items-center px-4 py-2.5 text-gray-600 hover:bg-gray-100 rounded-lg">
                <i class="fas fa-comments text-lg w-6"></i>
                <span class="ml-3">留言板管理</span>
              </router-link>
            </div>
          </div>

          <!-- 個人設定管理 -->
          <div>
            <div class="flex items-center px-4 py-2.5 text-gray-700 cursor-pointer hover:bg-gray-100 rounded-lg"
                 @click="toggleMenu('personal')">
              <i class="fas fa-user-cog text-lg w-6"></i>
              <span class="ml-3">個人設定管理</span>
              <i class="fas fa-chevron-down ml-auto transition-transform duration-200"
                 :class="{ 'transform rotate-180': openMenus.personal }"></i>
            </div>
            <div v-show="openMenus.personal" class="mt-1 pl-4">
              <router-link to="/admin/users" 
                class="flex items-center px-4 py-2.5 text-gray-600 hover:bg-gray-100 rounded-lg">
                <i class="fas fa-user text-lg w-6"></i>
                <span class="ml-3">使用者管理</span>
              </router-link>
              <router-link to="/admin/favorites" 
                class="flex items-center px-4 py-2.5 text-gray-600 hover:bg-gray-100 rounded-lg">
                <i class="fas fa-heart text-lg w-6"></i>
                <span class="ml-3">最愛管理</span>
              </router-link>
            </div>
          </div>
        </div>
      </nav>

      <!-- 登出按鈕 - 固定在底部 -->
      <div class="flex-shrink-0 p-3 border-t">
        <button @click="logout" 
          class="flex items-center w-full px-4 py-2.5 text-gray-700 hover:bg-gray-100 rounded-lg">
          <i class="fas fa-sign-out-alt text-lg w-6"></i>
          <span class="ml-3">登出</span>
        </button>
      </div>
    </aside>

    <!-- 主要內容區 -->
    <div class="ml-64">
      <!-- 頂部間距 -->
      <div class="h-16"></div>
      
      <!-- Banner 組件 -->
      <div class="bg-white shadow-sm z-20 mx-8 mt-8 rounded-lg overflow-hidden">
        <div class="relative banner-bg">
          <!-- 背景漸層 - 調整透明度讓底圖若隱若現 -->
          <div class="absolute inset-0 bg-gradient-to-r from-gray-900/80 to-gray-800/80"></div>
          
          <!-- Banner 內容 -->
          <div class="relative px-8 py-12">
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
      <div class="p-8">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminLayout',
  data() {
    return {
      openMenus: {
        system: false,
        order: false,
        personal: false
      }
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
        'FavoriteManagement': '最愛管理'
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
        'FavoriteManagement': '管理用戶收藏的飲品項目'
      }
      return descriptions[route] || '歡迎使用後台管理系統'
    }
  },
  methods: {
    toggleMenu(menu) {
      this.openMenus[menu] = !this.openMenus[menu]
    },
    logout() {
      // 實作登出邏輯
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
/* 自定義滾動條樣式 */
nav::-webkit-scrollbar {
  width: 4px;
}

nav::-webkit-scrollbar-track {
  background: transparent;
}

nav::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 2px;
}

nav::-webkit-scrollbar-thumb:hover {
  background-color: rgba(156, 163, 175, 0.8);
}

.banner-bg {
  background-image: url('https://images.unsplash.com/photo-1499638673689-79a0b5115d87?w=1000');
  /* 這是一張奶茶特寫照片 */
  background-size: cover;
  background-position: center;
  min-height: 200px; /* 設定最小高度 */
}

/* 可以根據需要調整以下樣式 */
.text-gray-200 {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.text-white {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}
</style> 