<template>
  <footer class="bg-gradient-to-b from-gray-800 to-gray-900 text-white py-12">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
        <!-- 品牌資訊 -->
        <div class="text-center md:text-left">
          <div class="flex items-center justify-center md:justify-start mb-4">
            <img src="@/assets/food/food-logo.svg" alt="Logo" class="w-10 h-10 mr-2">
            <span class="text-2xl font-bold bg-gradient-to-r from-red-500 to-orange-500 
                         bg-clip-text text-transparent">美食推薦</span>
          </div>
          <p class="text-gray-400">今天喝什麼呢？</p>
        </div>

        <!-- 聯絡資訊 -->
        <div class="text-center md:text-left">
          <h3 class="text-lg font-semibold mb-4">聯絡資訊</h3>
          <div class="space-y-2 text-gray-400">
            <p>地址：台北市信義區XX路123號</p>
            <p>電話：(02) 1234-5678</p>
            <p>信箱：info@ourbeverageshop.com</p>
          </div>
        </div>

        <!-- 營業時間 -->
        <div class="text-center md:text-left">
          <h3 class="text-lg font-semibold mb-4">營業時間</h3>
          <div class="space-y-2 text-gray-400">
            <p>週一至週日</p>
            <p>10:00 - 22:00</p>
          </div>
        </div>

        <!-- 社群連結 -->
        <div class="text-center md:text-left">
          <h3 class="text-lg font-semibold mb-4">關注我們</h3>
          <!-- 社交媒體圖標 -->
          <div class="flex justify-center md:justify-start space-x-6">
            <a href="#" class="hover:text-red-500 transition duration-300">
              <i class="fab fa-facebook-f text-2xl hover:scale-110 transform transition-all"></i>
            </a>
            <a href="#" class="hover:text-red-500 transition duration-300">
              <i class="fab fa-line text-2xl hover:scale-110 transform transition-all"></i>
            </a>
            <a href="#" class="hover:text-red-500 transition duration-300">
              <i class="fab fa-instagram text-2xl hover:scale-110 transform transition-all"></i>
            </a>
            <a href="#" class="hover:text-red-500 transition duration-300">
              <i class="far fa-envelope text-2xl hover:scale-110 transform transition-all"></i>
            </a>
          </div>
        </div>
      </div>

      <!-- 版權信息 -->
      <div class="text-center text-gray-400 pt-8 border-t border-gray-700">
        <p>&copy; 2025 美食推薦系統. All rights reserved.</p>
        <p class="mt-2 text-sm">Designed by Mark</p>
      </div>
    </div>
  </footer>
</template> 