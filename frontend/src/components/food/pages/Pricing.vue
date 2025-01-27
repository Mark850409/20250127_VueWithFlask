<template>
  <div class="min-h-screen bg-gray-50">
    <PageBanner
      title="定價方案"
      subtitle="靈活選擇・專屬服務"
      description="我們提供多種靈活的方案選擇，從免費的基礎版到功能完整的企業版，
                  根據您的需求量身打造最適合的服務方案。無論是個人使用還是企業需求，
                  我們都能為您提供最優質的解決方案。"
    />
    
    <!-- 定價方案卡片 -->
    <div class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto mb-20">
          <!-- 基礎版 -->
          <div class="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition-shadow duration-300">
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
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>基本使用教學</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>社群支援</span>
              </li>
            </ul>
            <button class="w-full py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-700 
                       transition duration-300">
              開始使用
            </button>
          </div>

          <!-- 專業版 -->
          <div class="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition-shadow duration-300 
                      transform scale-105 border-2 border-gray-800">
            <div class="absolute top-0 right-0 -translate-y-1/2 px-3 py-1 bg-blue-500 text-white 
                        rounded-full text-sm font-semibold">
              最受歡迎
            </div>
            <h3 class="text-2xl font-bold mb-4">專業版</h3>
            <div class="text-4xl font-bold mb-6">
              <span class="text-gray-800">NT$ 249</span>
              <span class="text-lg text-gray-600 font-normal">/月</span>
            </div>
            <ul class="space-y-4 mb-8">
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>所有基本版功能</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>無限網頁爬取</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>進階腳本生成功能</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>優先技術支援</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>API 存取權限</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>自訂爬取排程</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>資料匯出功能</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>進階使用教學</span>
              </li>
            </ul>
            <button class="w-full py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-700 
                       transition duration-300">
              立即升級
            </button>
          </div>

          <!-- 企業版 -->
          <div class="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition-shadow duration-300">
            <h3 class="text-2xl font-bold mb-4">企業版</h3>
            <div class="text-4xl font-bold mb-6">
              <span class="text-gray-800">請洽專員</span>
              <span class="text-lg text-gray-600 font-normal">客製化方案</span>
            </div>
            <ul class="space-y-4 mb-8">
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>所有專業版功能</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>專屬客戶經理</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>客製化開發支援</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>企業級 API</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>優先處理序列</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>SLA 保證</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>現場技術支援</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>團隊培訓課程</span>
              </li>
            </ul>
            <button class="w-full py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-700 
                       transition duration-300">
              聯繫業務
            </button>
          </div>
        </div>
        <div class="text-center">
          <router-link to="/pricing" 
            class="inline-flex items-center px-6 py-3 bg-gray-800 text-white rounded-lg 
                   hover:bg-gray-700 transition duration-300">
            <i class="fas fa-arrow-right mr-2"></i>
            了解完整方案
          </router-link>
        </div>
      </div>
    </div>

    <!-- 方案詳細比較表格 -->
    <div class="py-20 bg-gray-50">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-12">方案詳細比較</h2>
        <div class="max-w-7xl mx-auto bg-white rounded-xl shadow-lg overflow-hidden">
          <table class="w-full">
            <thead class="bg-gray-800 text-white">
              <tr>
                <th class="h-16 px-8 text-left w-1/3 text-lg">功能</th>
                <th class="h-16 px-8 text-center text-lg">基礎版</th>
                <th class="h-16 px-8 text-center text-lg">專業版</th>
                <th class="h-16 px-8 text-center text-lg">企業版</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr class="hover:bg-gray-50 transition-colors duration-150">
                <td class="p-8 font-medium text-gray-700">推薦功能</td>
                <td class="p-8 text-center">基本</td>
                <td class="p-8 text-center font-medium text-blue-600">進階</td>
                <td class="p-8 text-center font-medium text-indigo-600">客製化</td>
              </tr>
              <tr class="hover:bg-gray-50 transition-colors duration-150">
                <td class="p-8 font-medium text-gray-700">每日查詢次數</td>
                <td class="p-8 text-center">100次</td>
                <td class="p-8 text-center font-medium text-blue-600">無限制</td>
                <td class="p-8 text-center font-medium text-indigo-600">無限制</td>
              </tr>
              <tr class="hover:bg-gray-50 transition-colors duration-150">
                <td class="p-8 font-medium text-gray-700">API 存取</td>
                <td class="p-8 text-center text-gray-400">—</td>
                <td class="p-8 text-center">
                  <i class="fas fa-check text-blue-600"></i>
                </td>
                <td class="p-8 text-center font-medium text-indigo-600">企業級</td>
              </tr>
              <tr class="hover:bg-gray-50 transition-colors duration-150">
                <td class="p-8 font-medium text-gray-700">技術支援</td>
                <td class="p-8 text-center">社群支援</td>
                <td class="p-8 text-center font-medium text-blue-600">優先支援</td>
                <td class="p-8 text-center font-medium text-indigo-600">24/7 專人</td>
              </tr>
              <tr class="hover:bg-gray-50 transition-colors duration-150">
                <td class="p-8 font-medium text-gray-700">資料分析報表</td>
                <td class="p-8 text-center">基本</td>
                <td class="p-8 text-center font-medium text-blue-600">詳細</td>
                <td class="p-8 text-center font-medium text-indigo-600">客製化</td>
              </tr>
              <tr class="hover:bg-gray-50 transition-colors duration-150">
                <td class="p-8 font-medium text-gray-700">培訓課程</td>
                <td class="p-8 text-center">基礎教學</td>
                <td class="p-8 text-center font-medium text-blue-600">進階教學</td>
                <td class="p-8 text-center font-medium text-indigo-600">團隊培訓</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PageBanner from '../PageBanner.vue'

export default {
  components: {
    PageBanner
  }
}
</script> 