<template>
  <nav class="bg-white dark:bg-gray-800 border-b dark:border-gray-700 z-40 shadow-sm">
    <div class="mx-auto px-3 sm:px-4 lg:px-6">
      <div class="flex justify-between h-16">
        <!-- 左側區域：漢堡選單 + Logo -->
        <div class="flex items-center">
          <!-- 漢堡選單按鈕 -->
          <button @click="$emit('toggle-sidebar')" 
                  class="p-2 rounded-lg text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-gray-700 transition-colors duration-200 focus:outline-none">
            <i class="ri-menu-3-line text-xl"></i>
          </button>
          
          <!-- Logo -->
          <div class="ml-2 sm:ml-4 flex items-center">
            <i class="ri-drinks-2-line text-2xl text-indigo-600 dark:text-indigo-400"></i>
            <span class="hidden md:block ml-3 font-semibold text-base lg:text-lg text-gray-900 dark:text-white truncate max-w-[200px] lg:max-w-none">
              今天喝什麼呢【後台管理系統】
            </span>
            <span class="md:hidden ml-3 font-semibold text-base text-gray-900 dark:text-white">
              推薦系統後台
            </span>
          </div>
        </div>

        <!-- 中間區域：計時器 -->
        <!-- 桌面版計時器 -->
        <div class="hidden md:flex flex-1 justify-center items-center">
          <div v-if="remainingTime > 0" 
               class="group relative flex items-center gap-2 px-4 py-1.5 bg-white dark:bg-gray-700 
                      border border-indigo-100 dark:border-gray-600 rounded-lg 
                      shadow-sm hover:shadow-md transition-all duration-300">
            <div class="flex items-center gap-3">
              <!-- 進度條背景 -->
              <div class="absolute inset-0 bg-gradient-to-r from-indigo-100 to-blue-50 
                          dark:from-indigo-900/30 dark:to-blue-900/20 rounded-lg transition-all duration-300
                          group-hover:from-indigo-50 group-hover:to-blue-50
                          dark:group-hover:from-indigo-800/30 dark:group-hover:to-blue-800/20">
              </div>
              <!-- 時鐘圖示 -->
              <div class="relative z-10 w-8 h-8 flex items-center justify-center 
                          bg-indigo-500 dark:bg-indigo-400 rounded-full">
                <i class="fas fa-clock text-white text-sm"></i>
              </div>
              <!-- 時間文字 -->
              <div class="relative z-10 flex flex-col">
                <span class="text-xs text-gray-500 dark:text-gray-400">登入時效</span>
                <span class="text-sm font-medium text-gray-700 dark:text-gray-200">
                  {{ formatTime(remainingTime) }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 手機版計時器 -->
        <div class="md:hidden flex items-center mx-2">
          <div v-if="remainingTime > 0" 
               class="flex items-center justify-center w-8 h-8 bg-indigo-500 dark:bg-indigo-400 
                      rounded-full relative group">
            <i class="fas fa-clock text-white text-sm"></i>
            <!-- 懸浮提示 -->
            <div class="absolute invisible group-hover:visible opacity-0 group-hover:opacity-100
                        bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1
                        bg-gray-800 text-white text-xs rounded whitespace-nowrap
                        transition-all duration-200 transform scale-95 group-hover:scale-100">
              {{ formatTime(remainingTime) }}
              <div class="absolute top-full left-1/2 -translate-x-1/2 -mt-1
                          border-4 border-transparent border-t-gray-800"></div>
            </div>
          </div>
        </div>

        <!-- 右側功能區 -->
        <div class="flex items-center space-x-2 sm:space-x-4">
          <!-- 用戶選單 -->
          <Menu as="div" class="relative">
            <MenuButton class="flex items-center space-x-2 sm:space-x-3 px-2 sm:px-3 py-1.5 sm:py-2 rounded-lg hover:bg-indigo-50 transition-all duration-200">
              <img :src="userInfo.avatar || defaultAvatar"
                   alt="User Avatar"
                   class="h-7 w-7 sm:h-8 sm:w-8 rounded-full ring-2 ring-indigo-100">
              <span class="hidden md:block font-medium text-gray-700">
                {{ userInfo.username }}
              </span>
              <i class="fas fa-chevron-down text-indigo-400"></i>
            </MenuButton>

            <transition
              enter-active-class="transition ease-out duration-200"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-150"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <MenuItems class="absolute right-0 mt-2 w-40 sm:w-48 rounded-lg shadow-lg bg-white ring-1 ring-black ring-opacity-5 divide-y divide-gray-100 focus:outline-none">
                <div class="py-1">
                  <MenuItem v-slot="{ active }">
                    <a @click="handleLogout" 
                       class="flex items-center px-3 sm:px-4 py-2 text-xs sm:text-sm text-gray-700 hover:bg-indigo-50 cursor-pointer">
                      <i class="ri-logout-box-r-line w-5 text-indigo-500"></i>
                      <span>登出</span>
                    </a>
                  </MenuItem>
                </div>
              </MenuItems>
            </transition>
          </Menu>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import { ref, onMounted, watch, inject } from 'vue'
import axios from '@/utils/axios'
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'

export default {
  name: 'AdminNavbar',
  components: {
    Menu,
    MenuButton,
    MenuItems,
    MenuItem
  },
  props: {
    title: {
      type: String,
      default: '點餐推薦後台系統'
    },
    remainingTime: {
      type: Number,
      default: 0
    },
    formatTime: {
      type: Function,
      required: true
    }
  },
  setup() {
    const router = useRouter()
    const userInfo = ref({
      username: '',
      avatar: '',
      email: ''
    })
    const defaultAvatar = 'https://api.dicebear.com/7.x/avataaars/svg?seed=default'

    // 獲取用戶信息
    const getUserInfo = async () => {
      try {
        const userData = JSON.parse(localStorage.getItem('user'))
        if (userData?.id) {
          const response = await axios.get(`/users/${userData.id}`)
          const { username, email, avatar } = response.data
          
          // 設置基本信息
          userInfo.value = {
            username,
            email,
            avatar: avatar ? `${import.meta.env.VITE_API_URL}/users/avatar/${response.data.avatar.split('/').pop()}` : defaultAvatar
          }
        }
      } catch (error) {
        console.error('獲取用戶信息失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '獲取用戶信息失敗',
          text: '請重新登入',
          confirmButtonText: '確定'
        })
        userInfo.value.avatar = defaultAvatar
      }
    }

    onMounted(() => {
      getUserInfo()
    })

    const handleLogout = async () => {
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
          await axios.post('/users/logout')
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          localStorage.removeItem('isAdmin')
          router.push('/login')
          
          // 顯示登出成功訊息
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

    return {
      userInfo,
      defaultAvatar,
      handleLogout,
      menuItemClass: (active) => {
        return [
          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
          'group flex items-center w-full px-4 py-2 text-sm cursor-pointer'
        ]
      }
    }
  }
}
</script> 