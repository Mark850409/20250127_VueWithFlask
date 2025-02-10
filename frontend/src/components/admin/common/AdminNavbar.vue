<template>
  <nav class="bg-white dark:bg-gray-800 border-b dark:border-gray-700 z-40 shadow-sm">
    <div class="mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- 左側區域：漢堡選單 + Logo -->
        <div class="flex items-center">
          <!-- 漢堡選單按鈕 -->
          <button @click="$emit('toggle-sidebar')" 
                  class="p-2 rounded-lg text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-gray-700 transition-colors duration-200">
            <i class="fas fa-bars text-xl"></i>
          </button>
          
          <!-- Logo -->
          <div class="ml-4 flex items-center">
            <i class="fas fa-utensils text-2xl text-indigo-600 dark:text-indigo-400"></i>
            <span class="ml-3 font-semibold text-lg text-gray-900 dark:text-white">
              基於文字探勘與情感分析的推薦系統後台
            </span>
          </div>
        </div>

        <!-- 中間區域：計時器 -->
        <div class="flex-1 flex justify-center items-center">
          <div v-if="remainingTime > 0" 
               class="inline-flex items-center gap-2 px-6 py-2 bg-gradient-to-r from-indigo-500 to-blue-500 dark:from-indigo-400 dark:to-blue-400 
                      text-white rounded-full shadow-md transition-all duration-300 
                      hover:shadow-lg hover:from-indigo-600 hover:to-blue-600 dark:hover:from-indigo-500 dark:hover:to-blue-500">
            <i class="fas fa-clock"></i>
            <span class="font-medium">
              登入時效：{{ formatTime(remainingTime) }}
            </span>
          </div>
        </div>

        <!-- 右側功能區 -->
        <div class="flex items-center space-x-4">
          <!-- 深色模式切換 -->
          <button @click="handleDarkModeToggle" 
                  class="p-2 rounded-lg transition-colors duration-200"
                  :class="[
                    isDarkMode 
                      ? 'bg-gray-700 text-yellow-400 hover:bg-gray-600' 
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  ]">
            <i :class="['text-xl', isDarkMode ? 'fas fa-sun' : 'fas fa-moon']"></i>
          </button>

          <!-- 用戶選單 -->
          <Menu as="div" class="relative">
            <MenuButton class="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-indigo-50 transition-all duration-200">
              <img :src="userInfo.avatar || defaultAvatar"
                   alt="User Avatar"
                   class="h-8 w-8 rounded-full ring-2 ring-indigo-100">
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
              <MenuItems class="absolute right-0 mt-2 w-48 rounded-lg shadow-lg bg-white ring-1 ring-black ring-opacity-5 divide-y divide-gray-100 focus:outline-none">
                <div class="py-1">
                  <MenuItem v-slot="{ active }">
                    <a @click="handleLogout" 
                       class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-indigo-50 cursor-pointer">
                      <i class="fas fa-sign-out-alt w-5 text-indigo-500"></i>
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
    const isDarkMode = inject('isDarkMode', ref(false))
    const toggleDarkMode = inject('toggleDarkMode', () => {})
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

    // 處理深色模式切換
    const handleDarkModeToggle = () => {
      console.log('Toggling dark mode') // 用於調試
      if (toggleDarkMode) {
        toggleDarkMode()
      }
    }

    return {
      isDarkMode,
      userInfo,
      defaultAvatar,
      handleLogout,
      menuItemClass: (active) => {
        return [
          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
          'group flex items-center w-full px-4 py-2 text-sm cursor-pointer'
        ]
      },
      handleDarkModeToggle
    }
  }
}
</script> 