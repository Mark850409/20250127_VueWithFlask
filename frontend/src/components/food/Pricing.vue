<template>
  <section id="pricing" class="py-20 bg-gray-50">
    <div class="container mx-auto px-4">
      <h2 class="text-3xl font-bold text-center mb-12">定價方案</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition duration-300">
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
          <button class="w-full py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-700 
                       transition duration-300">
            開始使用
          </button>
        </div>

        <div class="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition duration-300 
                    transform scale-105 border-2 border-gray-800">
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
          <button class="w-full py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-700 
                       transition duration-300">
            立即升級
          </button>
        </div>

        <div class="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition duration-300">
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
          <button class="w-full py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-700 
                       transition duration-300">
            聯繫我們
          </button>
        </div>
      </div>
      <div class="text-center mt-16">
        <router-link to="/pricing" 
          class="inline-flex items-center px-6 py-3 bg-gray-800 text-white rounded-lg 
                 hover:bg-gray-700 transition duration-300">
          <i class="fas fa-arrow-right mr-2"></i>
          了解完整方案
        </router-link>
      </div>
    </div>
  </section>
</template> 