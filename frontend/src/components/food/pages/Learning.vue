<template>
  <div class="min-h-screen bg-gray-50">
    <PageBanner
      title="學習中心"
      subtitle="功能導覽・使用教學"
      description="我們提供完整的功能說明和使用教學，幫助您快速掌握系統的各項功能。
                  無論是新手入門還是進階應用，都能在這裡找到答案。"
    />
    
    <!-- 功能導覽區塊 -->
    <div class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-12">功能導覽</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-12 max-w-6xl mx-auto">
          <!-- 智能推薦 -->
          <div class="bg-white p-8 rounded-xl shadow-lg">
            <div class="text-gray-800 mb-6 text-4xl">
              <i class="fas fa-robot"></i>
            </div>
            <h3 class="text-xl font-bold mb-4">智能推薦功能</h3>
            <p class="text-gray-600 mb-6">
              了解如何使用我們的智能推薦系統，獲得最適合的飲品建議。
            </p>
            <ul class="space-y-3 text-gray-600">
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-3"></i>
                個人化偏好設定
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-3"></i>
                推薦結果解釋
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-3"></i>
                評分與反饋
              </li>
            </ul>
          </div>

          <!-- 搜尋功能 -->
          <div class="bg-white p-8 rounded-xl shadow-lg">
            <div class="text-gray-800 mb-6 text-4xl">
              <i class="fas fa-search"></i>
            </div>
            <h3 class="text-xl font-bold mb-4">搜尋與篩選</h3>
            <p class="text-gray-600 mb-6">
              掌握進階搜尋技巧，快速找到想要的飲品資訊。
            </p>
            <ul class="space-y-3 text-gray-600">
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-3"></i>
                關鍵字搜尋
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-3"></i>
                條件篩選
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-3"></i>
                排序功能
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- 常見問題區塊 -->
    <div id="faq" class="py-20 bg-gray-50">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-12">常見問題</h2>
        <div class="max-w-3xl mx-auto space-y-6">
          <div class="bg-white rounded-xl shadow-lg p-6">
            <h3 class="text-xl font-bold mb-4">如何開始使用推薦系統？</h3>
            <p class="text-gray-600">
              只需註冊帳號並完成偏好設定，系統就會開始為您推薦合適的飲品。
            </p>
          </div>
          <div class="bg-white rounded-xl shadow-lg p-6">
            <h3 class="text-xl font-bold mb-4">推薦結果如何更新？</h3>
            <p class="text-gray-600">
              系統會根據您的使用習慣和評分持續學習，自動更新推薦結果。
            </p>
          </div>
          <div class="bg-white rounded-xl shadow-lg p-6">
            <h3 class="text-xl font-bold mb-4">如何提供反饋？</h3>
            <p class="text-gray-600">
              在每個推薦結果旁都有評分和評論功能，您可以隨時提供您的意見。
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- 影片教學區塊 -->
    <div id="tutorials" class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-12">使用教學</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <div class="bg-white rounded-xl shadow-lg overflow-hidden">
            <div class="aspect-w-16 aspect-h-9">
              <img src="https://images.unsplash.com/photo-1516321318423-f06f85e504b3" 
                   class="w-full h-48 object-cover" alt="新手教學">
            </div>
            <div class="p-6">
              <h3 class="text-xl font-bold mb-2">新手入門教學</h3>
              <p class="text-gray-600 mb-4">
                從零開始，了解系統的基本功能和操作方式。
              </p>
              <button class="w-full px-4 py-2 bg-gray-800 text-white rounded-lg 
                           hover:bg-gray-700 transition duration-300">
                觀看影片
              </button>
            </div>
          </div>
          <!-- 可以添加更多影片教學卡片 -->
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