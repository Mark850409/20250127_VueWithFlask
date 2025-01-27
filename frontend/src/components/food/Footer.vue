<template>
  <footer class="bg-gray-900 text-white py-12">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- 品牌介紹 -->
        <div>
          <div class="flex items-center space-x-2 mb-4">
            <img src="https://api.dicebear.com/7.x/bottts/svg?seed=food" 
                 alt="Logo" class="w-8 h-8">
            <h3 class="text-xl font-bold">基於文字探勘與情感分析的推薦系統</h3>
          </div>
          <p class="text-gray-400">
            在我們的飲料店，每一杯都是一種心動。多樣化的飲品選擇，精緻的口感，
            讓您隨時隨地都能享受至臻完美光，無論是外帶或是堂食，
            讓我們的飲品為您完美詮釋當季享受。
          </p>
        </div>

        <!-- 聯絡資訊 -->
        <div>
          <h3 class="text-lg font-semibold mb-4">聯絡資訊</h3>
          <ul class="space-y-2 text-gray-400">
            <li class="flex items-center">
              <i class="fas fa-map-marker-alt w-5"></i>
              <span>台北市信義區XX路123號</span>
            </li>
            <li class="flex items-center">
              <i class="fas fa-phone w-5"></i>
              <span>(02) 1234-5678</span>
            </li>
            <li class="flex items-center">
              <i class="fas fa-envelope w-5"></i>
              <span>info@ourbeverageshop.com</span>
            </li>
          </ul>
        </div>

        <!-- 功能特色 -->
        <div>
          <h3 class="text-lg font-semibold mb-4">功能特色</h3>
          <ul class="space-y-2 text-gray-400">
            <li>
              <router-link to="/" class="flex items-center hover:text-white transition duration-300">
                <i class="fas fa-home w-5"></i>
                <span>首頁</span>
              </router-link>
            </li>
            <li>
              <router-link to="/features" class="flex items-center hover:text-white transition duration-300">
                <i class="fas fa-star w-5"></i>
                <span>平台特色</span>
              </router-link>
            </li>
            <li>
              <router-link to="/learning" class="flex items-center hover:text-white transition duration-300">
                <i class="fas fa-book w-5"></i>
                <span>學習中心</span>
              </router-link>
            </li>
            <li>
              <router-link to="/pricing" class="flex items-center hover:text-white transition duration-300">
                <i class="fas fa-tag w-5"></i>
                <span>定價方案</span>
              </router-link>
            </li>
          </ul>
        </div>

        <!-- 社群連結 -->
        <div>
          <h3 class="text-lg font-semibold mb-4">關注我們</h3>
          <div class="flex space-x-4">
            <a href="#" class="text-gray-400 hover:text-white transition duration-300">
              <i class="fab fa-facebook-f text-xl"></i>
            </a>
            <a href="#" class="text-gray-400 hover:text-white transition duration-300">
              <i class="fab fa-line text-xl"></i>
            </a>
            <a href="#" class="text-gray-400 hover:text-white transition duration-300">
              <i class="fab fa-instagram text-xl"></i>
            </a>
            <a href="#" class="text-gray-400 hover:text-white transition duration-300">
              <i class="fas fa-envelope text-xl"></i>
            </a>
          </div>
        </div>
      </div>

      <!-- 版權聲明 -->
      <div class="mt-8 pt-8 border-t border-gray-800 text-center text-gray-400">
        <p>© 2025 基於文字探勘與情感分析的點餐推薦系統. All rights reserved.</p>
        <p class="mt-2">Designed by Mark</p>
      </div>
    </div>
  </footer>
</template> 