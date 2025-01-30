<template>
  <nav class="bg-white border-b z-40 transition-all duration-300">
    <div class="px-4 h-16 flex justify-between items-center">
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

      <!-- 右側功能區 -->
      <div class="flex items-center space-x-4">
        <!-- 通知 -->
        <button class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg relative">
          <i class="fas fa-bell"></i>
          <span class="absolute top-1 right-1 w-2 h-2 bg-blue-500 rounded-full"></span>
        </button>

        <!-- 深色模式切換 -->
        <button class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg">
          <i class="fas fa-moon"></i>
        </button>

        <!-- 語言切換 -->
        <button class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg">
          <img src="https://flagcdn.com/w20/tw.png" alt="Taiwan" class="w-5 h-5">
        </button>

        <!-- 使用者選單 -->
        <div class="relative">
          <button @click="isUserMenuOpen = !isUserMenuOpen"
                  class="flex items-center space-x-2 p-2 hover:bg-gray-100 rounded-lg">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=admin" 
                 alt="User Avatar" 
                 class="w-8 h-8 rounded-full">
            <span class="text-sm font-medium text-gray-700">管理員</span>
            <i class="fas fa-chevron-down text-xs text-gray-400"></i>
          </button>

          <!-- 下拉選單 -->
          <div v-if="isUserMenuOpen" 
               class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-1 border">
            <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
              <i class="fas fa-user mr-2"></i>個人資料
            </a>
            <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
              <i class="fas fa-cog mr-2"></i>設定
            </a>
            <hr class="my-1">
            <a href="#" class="block px-4 py-2 text-sm text-red-600 hover:bg-gray-100">
              <i class="fas fa-sign-out-alt mr-2"></i>登出
            </a>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AdminNavbar',
  props: {
    isSidebarCollapsed: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isUserMenuOpen: false
    }
  },
  emits: ['toggle-sidebar']
}
</script> 