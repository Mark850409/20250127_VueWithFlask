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

        <!-- 登入按鈕 -->
        <div class="flex items-center">
          <router-link to="/login" 
                      class="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg 
                             hover:bg-blue-700 transition-colors">
            <i class="fas fa-user mr-2"></i>
            登入 / 註冊
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar'
}
</script> 