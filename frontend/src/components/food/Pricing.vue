<template>
  <section id="pricing" class="py-20 bg-gray-50">
    <div class="container mx-auto px-4 max-w-6xl">
      <!-- 標題區塊 -->
      <div class="text-center mb-16">
        <span class="span-title inline-block px-4 py-1 bg-blue-50 text-blue-500 font-medium rounded-full mb-4">
          PRICING
        </span>
        <h2 class="text-4xl font-bold text-gray-900">
          定價方案
        </h2>
      </div>

      <!-- 方案卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- 基礎版 -->
        <div class="basic-card bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition duration-300">
          <h3 class="text-2xl font-bold mb-4">基礎版</h3>
          <div class="text-4xl font-bold mb-6">
            <span class="text-gray-800">$0</span>
            <span class="text-lg text-gray-600 font-normal">/月</span>
          </div>
          <ul class="space-y-4 mb-8">
            <li class="flex items-center">
              <i class="fas fa-check text-green-500 mr-2"></i>
              <span>基本飲品推薦</span>
            </li>
            <li class="flex items-center">
              <i class="fas fa-check text-green-500 mr-2"></i>
              <span>每日限量查詢</span>
            </li>
            <li class="flex items-center">
              <i class="fas fa-check text-green-500 mr-2"></i>
              <span>基礎社群功能</span>
            </li>
          </ul>
          <button class="basic-btn w-full py-3 bg-gray-800 text-white rounded-full hover:bg-gray-700 
                       transition duration-300 ">
            開始使用
          </button>
        </div>

        <!-- 專業版 -->
        <div class="professional-card bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition duration-300 
                    transform scale-105 border-2 border-blue-500">
          <h3 class="text-2xl font-bold mb-4">專業版</h3>
          <div class="text-4xl font-bold mb-6">
            <span class="text-gray-800">$299</span>
            <span class="text-lg text-gray-600 font-normal">/月</span>
          </div>
          <ul class="space-y-4 mb-8">
            <li class="flex items-center">
              <i class="fas fa-check text-green-500 mr-2"></i>
              <span>進階智能推薦</span>
            </li>
            <li class="flex items-center">
              <i class="fas fa-check text-green-500 mr-2"></i>
              <span>無限次查詢</span>
            </li>
            <li class="flex items-center">
              <i class="fas fa-check text-green-500 mr-2"></i>
              <span>專屬課程內容</span>
            </li>
            <li class="flex items-center">
              <i class="fas fa-check text-green-500 mr-2"></i>
              <span>優先客服支援</span>
            </li>
          </ul>
          <button class="professional-btn w-full py-3 bg-blue-500 text-white rounded-full hover:bg-blue-600 
                       transition duration-300">
            立即升級
          </button>
        </div>

        <!-- 企業版 -->
        <div class="enterprise-card bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition duration-300">
          <h3 class="text-2xl font-bold mb-4">企業版</h3>
          <div class="text-4xl font-bold mb-6">
            <span class="text-gray-800">$799</span>
            <span class="text-lg text-gray-600 font-normal">/月</span>
          </div>
          <ul class="space-y-4 mb-8">
            <li class="flex items-center">
              <i class="fas fa-check text-green-500 mr-2"></i>
              <span>客製化推薦系統</span>
            </li>
            <li class="flex items-center">
              <i class="fas fa-check text-green-500 mr-2"></i>
              <span>數據分析報表</span>
            </li>
            <li class="flex items-center">
              <i class="fas fa-check text-green-500 mr-2"></i>
              <span>專屬顧問服務</span>
            </li>
            <li class="flex items-center">
              <i class="fas fa-check text-green-500 mr-2"></i>
              <span>API 整合支援</span>
            </li>
          </ul>
          <button class="enterprise-btn w-full py-3 bg-gray-800 text-white rounded-full hover:bg-gray-700 
                       transition duration-300">
            聯繫我們
          </button>
        </div>
      </div>
      <div class="text-center mt-16">
        <router-link to="/pricing" 
          class="pricing-btn inline-flex items-center px-8 py-3 bg-white text-black hover:bg-white/90 rounded-full transition duration-300 font-semibold text-lg">
          <i class="fas fa-arrow-right mr-2"></i>
          了解完整方案
        </router-link>
      </div>
    </div>
  </section>
</template>

<style scoped>
.container {
  margin-left: auto;
  margin-right: auto;
}
</style> 