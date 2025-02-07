<template>
  <nav class="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-md shadow-sm z-50">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-3">
          <img src="https://api.dicebear.com/7.x/bottts/svg?seed=food" 
               alt="Logo" class="h-10 w-10">
          <span class="text-lg font-bold text-gray-800">
            基於文字探勘與情感分析的點餐推薦系統
          </span>
        </router-link>

        <!-- 主選單 -->
        <div class="hidden md:flex items-center space-x-8">
          <router-link to="/" 
                      class="text-gray-600 hover:text-gray-900 transition-colors">
            <i class="fas fa-home mr-1"></i>
            首頁
          </router-link>
          <router-link to="/features" 
                      class="text-gray-600 hover:text-gray-900 transition-colors">
            <i class="fas fa-star mr-1"></i>
            平台特色
          </router-link>
          <router-link to="/learning" 
                      class="text-gray-600 hover:text-gray-900 transition-colors">
            <i class="fas fa-book mr-1"></i>
            學習中心
          </router-link>
          <router-link to="/pricing" 
                      class="text-gray-600 hover:text-gray-900 transition-colors">
            <i class="fas fa-tag mr-1"></i>
            定價方案
          </router-link>
        </div>

        <!-- 登入/登出按鈕 -->
        <div class="flex items-center">
          <template v-if="isLoggedIn">
            <div class="relative" @click.stop>
              <!-- 個人頭像 -->
              <div class="flex items-center cursor-pointer" 
                   @click="toggleDropdown">
                <img :src="getAvatarUrl" 
                     alt="User Avatar"
                     class="h-8 w-8 rounded-full border-2 border-blue-500"
                     @error="handleAvatarError"
                >
                <span class="ml-2 text-gray-700">{{ userName }}</span>
                <i class="fas fa-chevron-down ml-2 text-gray-500 text-xs transition-transform duration-200"
                   :class="{ 'transform rotate-180': isDropdownOpen }">
                </i>
              </div>
              <!-- 下拉選單 -->
              <div v-if="isDropdownOpen" 
                   class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-1 z-50
                          border border-gray-100 transition-all duration-200">
                <router-link to="/admin"
                            class="flex items-center px-4 py-2 text-gray-700 hover:bg-gray-50">
                  <i class="fas fa-user-cog mr-2"></i>
                  <span>管理後台</span>
                </router-link>
                <div class="border-t border-gray-100 my-1"></div>
                <button @click="handleLogout"
                        class="flex items-center w-full px-4 py-2 text-left text-red-600 
                               hover:bg-red-50 transition-colors">
                  <i class="fas fa-sign-out-alt mr-2"></i>
                  <span>登出</span>
                </button>
              </div>
            </div>
          </template>
          <template v-else>
            <!-- 登入按鈕 -->
            <router-link to="/login" 
                        class="flex items-center px-4 py-2 text-blue-600 border-2 border-blue-600 
                               rounded-lg hover:bg-blue-50 transition-all duration-200">
              <i class="fas fa-user-circle text-lg mr-2"></i>
              <span>登入 / 註冊</span>
            </router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Navbar',
  setup() {
    const router = useRouter()
    const isLoggedIn = ref(false)
    const userName = ref('')
    const isDropdownOpen = ref(false)
    const defaultAvatar = 'https://api.dicebear.com/7.x/avataaars/svg?seed=default'
    
    // 計算頭像 URL
    const getAvatarUrl = computed(() => {
      if (!isLoggedIn.value) return defaultAvatar
      
      let user = {}
      try {
        user = JSON.parse(localStorage.getItem('user') || '{}')
        console.log(user)
      } catch (error) {
        console.error('解析用戶數據失敗:', error)
        return defaultAvatar
      }
      
      const baseUrl = import.meta.env.VITE_BACKEND_URL
      
      if (!user || typeof user !== 'object') {
        return defaultAvatar
      }

      if (user.avatar && user.avatar.startsWith('http')) {
        return user.avatar
      } else if (user.avatar) {
        if (!baseUrl) {
          console.error('後端 URL 未設置')
          return defaultAvatar
        }
        console.log(`${baseUrl}/api/users/avatar/${user.avatar.split('/').pop()}`)
        return `${baseUrl}/api/users/avatar/${user.avatar.split('/').pop()}`
      } else {
        return `https://api.dicebear.com/7.x/avataaars/svg?seed=${user.username || 'default'}`
      }
    })

    // 檢查登入狀態
    const checkLoginStatus = () => {
      const token = localStorage.getItem('token')
      isLoggedIn.value = !!token
      if (isLoggedIn.value) {
        try {
          const user = JSON.parse(localStorage.getItem('user') || '{}')
          userName.value = user.username || '使用者'
        } catch (error) {
          console.error('解析用戶數據失敗:', error)
          isLoggedIn.value = false
          localStorage.removeItem('token')
          localStorage.removeItem('user')
        }
      } else {
        userName.value = ''
      }
    }

    // 切換下拉選單
    const toggleDropdown = () => {
      isDropdownOpen.value = !isDropdownOpen.value
    }

    // 點擊外部關閉下拉選單
    const closeDropdown = (e) => {
      // 檢查點擊是否發生在下拉選單外部
      const dropdown = document.querySelector('.relative')
      if (dropdown && !dropdown.contains(e.target)) {
        isDropdownOpen.value = false
      }
    }

    // 處理登出
    const handleLogout = () => {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      isLoggedIn.value = false
      userName.value = ''
      isDropdownOpen.value = false
      router.push('/login')
    }

    // 處理頭像加載錯誤
    const handleAvatarError = (e) => {
      console.error('頭像加載失敗，使用默認頭像')
      e.target.src = defaultAvatar
    }

    // 組件掛載時檢查登入狀態
    onMounted(() => {
      document.addEventListener('click', closeDropdown)
      checkLoginStatus()
    })

    // 移除監聽
    onUnmounted(() => {
      document.removeEventListener('click', closeDropdown)
    })

    return {
      isLoggedIn,
      handleLogout,
      userName,
      getAvatarUrl,
      handleAvatarError,
      isDropdownOpen,
      toggleDropdown
    }
  }
}
</script>

<style scoped>
/* 防止點擊下拉選單內部時觸發外部點擊事件 */
.relative {
  isolation: isolate;
}
</style> 