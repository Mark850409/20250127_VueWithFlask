<template>
  <nav class="fixed top-0 left-0 right-0 z-[9999] transition-all duration-300"
       :class="[
         scrolled 
           ? 'bg-[rgba(0,0,0,0.85)]' 
           : 'bg-[rgba(0,0,0,0)]'
       ]">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-3">
          <i class="fas fa-utensils text-white text-2xl"></i>
          <span class="text-lg font-bold text-white">
            今天想喝什麼呢？
          </span>
        </router-link>

        <!-- 主選單 -->
        <div class="hidden md:flex items-center space-x-8">
          <a href="/" 
             :class="[
               'text-white hover:text-gray-200',
               'transition-colors'
             ]">
            <i class="fas fa-home mr-1"></i>
            首頁
          </a>
          <a href="/features" 
             :class="[
               'text-white hover:text-gray-200',
               'transition-colors'
             ]">
            <i class="fas fa-star mr-1"></i>
            平台特色
          </a>
          <a href="/learning" 
             :class="[
               'text-white hover:text-gray-200',
               'transition-colors'
             ]">
            <i class="fas fa-coffee mr-1"></i>
            學習中心
          </a>
          <a href="/pricing" 
             :class="[
               'text-white hover:text-gray-200',
               'transition-colors'
             ]">
            <i class="fas fa-th mr-1"></i>
            定價方案
          </a>
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
                <span class="ml-2 text-white">
                  {{ userName }}
                </span>
                <i class="fas fa-chevron-down ml-2 text-white/70 text-xs transition-transform duration-200"
                   :class="{ 'transform rotate-180': isDropdownOpen }">
                </i>
              </div>
              <!-- 下拉選單 -->
              <div v-if="isDropdownOpen" 
                   class="absolute right-0 mt-2 w-48 bg-black/90 backdrop-blur-md rounded-lg shadow-lg py-1 z-50
                          border border-white/20 transition-all duration-200">
                <router-link to="/admin"
                            class="flex items-center px-4 py-2 text-white hover:bg-white/10">
                  <i class="fas fa-user-cog mr-2"></i>
                  <span>管理後台</span>
                </router-link>
                <div class="border-t border-white/20 my-1"></div>
                <button @click="handleLogout"
                        class="flex items-center w-full px-4 py-2 text-left text-red-400 
                               hover:bg-white/10 transition-colors">
                  <i class="fas fa-sign-out-alt mr-2"></i>
                  <span>登出</span>
                </button>
              </div>
            </div>
          </template>
          <template v-else>
            <!-- 登入按鈕 -->
            <router-link to="/login" 
                       :class="[
                         'text-white border-white hover:bg-white/10',
                         'flex items-center px-4 py-2 border-2 rounded-lg transition-all duration-200'
                       ]">
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
    const scrolled = ref(false)
    const router = useRouter()
    const isLoggedIn = ref(false)
    const userName = ref('')
    const isDropdownOpen = ref(false)
    const currentImageIndex = ref(0)
    const autoPlayInterval = ref(null)
    const defaultAvatar = 'https://api.dicebear.com/7.x/avataaars/svg?seed=default'
    
    // Banner 圖片
    const bannerImages = [
      {
        id: 1,
        url: 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&q=80&w=1920&h=600',
        alt: 'Banner 1'
      },
      // ... 其他圖片
    ]

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

    // 監聽滾動事件
    const handleScroll = () => {
      scrolled.value = window.scrollY > 50
    }

    // 輪播功能
    const startAutoPlay = () => {
      autoPlayInterval.value = setInterval(() => {
        currentImageIndex.value = (currentImageIndex.value + 1) % bannerImages.length
      }, 5000)
    }

    const stopAutoPlay = () => {
      if (autoPlayInterval.value) {
        clearInterval(autoPlayInterval.value)
      }
    }

    // 組件掛載時檢查登入狀態和添加滾動監聽
    onMounted(() => {
      document.addEventListener('click', closeDropdown)
      window.addEventListener('scroll', handleScroll)
      checkLoginStatus()
      startAutoPlay()
    })

    // 移除監聽
    onUnmounted(() => {
      document.removeEventListener('click', closeDropdown)
      window.removeEventListener('scroll', handleScroll)
      stopAutoPlay()
    })

    return {
      scrolled,
      isLoggedIn,
      handleLogout,
      userName,
      getAvatarUrl,
      handleAvatarError,
      isDropdownOpen,
      toggleDropdown,
      currentImageIndex,
      bannerImages
    }
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

img {
  background-color: black;
}

.relative {
  isolation: isolate;
}

.container {
  margin-left: auto;
  margin-right: auto;
}

@media (min-width: 1280px) {
  .container {
    max-width: 1140px;
  }
}

/* 添加底線動畫效果 */
.after\:scale-x-0::after {
  transform: scaleX(0);
  transform-origin: center;
}

.after\:scale-x-100::after {
  transform: scaleX(1);
}

.hover\:after\:scale-x-100:hover::after {
  transform: scaleX(1);
}
</style> 