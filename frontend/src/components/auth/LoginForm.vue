<template>
  <div class="min-h-screen bg-gray-50 pt-24 pb-20">
    <div class="max-w-md w-full mx-auto bg-white rounded-xl shadow-lg p-6">
      <!-- Logo -->
      <div class="text-center mb-6">
        <img src="https://api.dicebear.com/7.x/bottts/svg?seed=food" 
             alt="Logo" 
             class="h-16 w-16 mx-auto mb-3">
        <h2 class="text-2xl font-bold">歡迎回來</h2>
        <p class="text-gray-600 mt-1">使用你的帳號登入系統</p>
      </div>

      <!-- 登入表單 -->
      <form class="space-y-4">
        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-gray-700">Email</label>
          <input type="email" 
                 placeholder="請輸入Email" 
                 class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md 
                        shadow-sm focus:ring-blue-500 focus:border-blue-500">
        </div>

        <!-- 密碼 -->
        <div>
          <label class="block text-sm font-medium text-gray-700">密碼</label>
          <input type="password" 
                 placeholder="請輸入密碼" 
                 class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md 
                        shadow-sm focus:ring-blue-500 focus:border-blue-500">
        </div>

        <!-- 記住我 & 忘記密碼 -->
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input type="checkbox" 
                   class="h-4 w-4 text-blue-600 focus:ring-blue-500 
                          border-gray-300 rounded">
            <label class="ml-2 block text-sm text-gray-700">記住我</label>
          </div>
          <a href="#" class="text-sm text-blue-600 hover:text-blue-500">忘記密碼？</a>
        </div>

        <!-- 登入按鈕 -->
        <button type="submit" 
                class="w-full flex justify-center py-2 px-4 border border-transparent 
                       rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 
                       hover:bg-blue-700 focus:outline-none focus:ring-2 
                       focus:ring-offset-2 focus:ring-blue-500">
          登入
        </button>
      </form>

      <!-- 分隔線 -->
      <div class="mt-4">
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white text-gray-500">或使用以下方式</span>
          </div>
        </div>
      </div>

      <!-- 社群登入按鈕 -->
      <div class="mt-4 grid grid-cols-3 gap-3">
        <button class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 
                       rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 
                       hover:bg-gray-50">
          <i class="fab fa-google"></i>
        </button>
        <button class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 
                       rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 
                       hover:bg-gray-50">
          <i class="fab fa-facebook"></i>
        </button>
        <button class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 
                       rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 
                       hover:bg-gray-50">
          <i class="fab fa-line"></i>
        </button>
      </div>

      <!-- 註冊連結 -->
      <div class="mt-4 text-center">
        <span class="text-gray-600">還沒有帳號？</span>
        <a href="#" class="text-blue-600 hover:text-blue-500 ml-1">立即註冊</a>
      </div>
    </div>
  </div>
</template> 