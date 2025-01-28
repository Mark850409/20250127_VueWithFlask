<template>
  <div>
    <!-- 移除原有標題，直接從統計卡片開始 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <!-- 用戶數統計 -->
      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-gray-600">總用戶數</h3>
          <i class="fas fa-users text-blue-500 text-xl"></i>
        </div>
        <p class="text-3xl font-bold">2,451</p>
        <p class="text-green-500 text-sm mt-2">
          <i class="fas fa-arrow-up mr-1"></i>
          較上月增加 12%
        </p>
      </div>

      <!-- 店家數統計 -->
      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-gray-600">合作店家</h3>
          <i class="fas fa-store text-purple-500 text-xl"></i>
        </div>
        <p class="text-3xl font-bold">128</p>
        <p class="text-green-500 text-sm mt-2">
          <i class="fas fa-arrow-up mr-1"></i>
          較上月增加 5%
        </p>
      </div>

      <!-- 評論數統計 -->
      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-gray-600">評論總數</h3>
          <i class="fas fa-comments text-yellow-500 text-xl"></i>
        </div>
        <p class="text-3xl font-bold">8,642</p>
        <p class="text-green-500 text-sm mt-2">
          <i class="fas fa-arrow-up mr-1"></i>
          較上月增加 18%
        </p>
      </div>

      <!-- 平均評分統計 -->
      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-gray-600">平均評分</h3>
          <i class="fas fa-star text-orange-500 text-xl"></i>
        </div>
        <p class="text-3xl font-bold">4.8</p>
        <p class="text-green-500 text-sm mt-2">
          <i class="fas fa-arrow-up mr-1"></i>
          較上月增加 0.2
        </p>
      </div>
    </div>

    <!-- 圖表區域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 用戶活躍度趨勢 -->
      <div class="bg-white rounded-xl shadow-sm p-6">
        <h3 class="text-lg font-semibold mb-4">用戶活躍度趨勢</h3>
        <div class="h-80 bg-gray-50 rounded-lg">
          <!-- 這裡可以放置圖表組件 -->
          <div class="w-full h-full flex items-center justify-center text-gray-400">
            圖表區域
          </div>
        </div>
      </div>

      <!-- 熱門店家排行 -->
      <div class="bg-white rounded-xl shadow-sm p-6">
        <h3 class="text-lg font-semibold mb-4">熱門店家排行</h3>
        <div class="space-y-4">
          <div v-for="(shop, index) in topShops" :key="index" 
               class="flex items-center p-3 bg-gray-50 rounded-lg">
            <span class="w-8 h-8 flex items-center justify-center bg-gray-200 rounded-full mr-4">
              {{ index + 1 }}
            </span>
            <div class="flex-1">
              <h4 class="font-medium">{{ shop.name }}</h4>
              <p class="text-sm text-gray-500">評分: {{ shop.rating }}</p>
            </div>
            <span class="text-green-500">
              <i class="fas fa-arrow-up mr-1"></i>
              {{ shop.increase }}%
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      topShops: [
        { name: '春水堂', rating: 4.9, increase: 15 },
        { name: '五桐號', rating: 4.8, increase: 12 },
        { name: '可不可熟成紅茶', rating: 4.7, increase: 10 },
        { name: '清心福全', rating: 4.6, increase: 8 },
        { name: '50嵐', rating: 4.5, increase: 5 }
      ]
    }
  }
}
</script> 