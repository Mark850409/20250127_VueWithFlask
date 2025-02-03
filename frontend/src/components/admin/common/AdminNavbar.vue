<template>
  <nav class="bg-white border-b z-40 transition-all duration-300">
    <div class="mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
         <!-- 左側區域：漢堡選單 + Logo -->
        <div class="flex items-center">
          <!-- 漢堡選單按鈕 -->
          <button @click="$emit('toggle-sidebar')" 
                  class="p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200">
            <i class="fas fa-bars text-gray-600"></i>
          </button>
          
          <!-- Logo -->
          <div class="ml-4 font-semibold text-lg text-gray-800">
            點餐推薦後台系統
          </div>
        </div>

        <!-- 中間區域：計時器 -->
        <div class="flex-1 flex justify-center items-center">
          <div v-if="remainingTime > 0" 
               class="inline-flex items-center gap-2 px-4 py-1.5 bg-gradient-to-r from-blue-500 to-indigo-600 
                      text-white rounded-full shadow-lg transition-all duration-300 
                      hover:shadow-indigo-500/30">
            <i class="fas fa-clock text-sm"></i>
            <span class="text-sm font-medium">
              登入時效：{{ formatTime(remainingTime) }}
            </span>
          </div>
        </div>

        <!-- 右側功能區 -->
        <div class="flex items-center">
          <!-- 深色模式切換 - 保持不變 -->
          <button @click="toggleDarkMode" class="p-2 text-gray-500 hover:text-gray-600">
            <i :class="['text-xl', isDarkMode ? 'fas fa-sun' : 'fas fa-moon']"></i>
          </button>

          <!-- 用戶選單 - 修改這部分 -->
          <Menu as="div" class="ml-3 relative">
            <div>
              <MenuButton class="flex items-center text-sm rounded-full focus:outline-none">
                <img
                  :src="userInfo.avatar || defaultAvatar"
                  alt="User Avatar"
                  class="h-8 w-8 rounded-full"
                >
                <span class="hidden md:block ml-2 text-gray-700">
                  {{ userInfo.username }}
                </span>
                <i class="fas fa-chevron-down ml-2 text-gray-400"></i>
              </MenuButton>
            </div>

            <transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <MenuItems class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 divide-y divide-gray-100 focus:outline-none">
                <!-- 簡化選單，只保留登出 -->
                <div class="py-1">
                  <MenuItem v-slot="{ active }">
                    <a @click="handleLogout" :class="menuItemClass(active)">
                      <i class="fas fa-sign-out-alt mr-3"></i>
                      登出
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
import { ref, onMounted } from 'vue'
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
    const isDarkMode = ref(false)
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
      toggleDarkMode() {
        isDarkMode.value = !isDarkMode.value
        // 實現深色模式切換邏輯
      }
    }
  }
}
</script> 