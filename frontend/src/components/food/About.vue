<template>
  <section class="py-20 bg-white">
    <div class="container mx-auto px-4">
      <!-- 標題區塊 -->
      <div class="text-center mb-16">
        <span class="inline-block px-4 py-1 bg-blue-50 text-blue-500 font-medium rounded-full mb-4">
          關於我們
        </span>
        <h2 class="text-4xl font-bold text-gray-900">
          了解更多 <span class="text-blue-500">關於我們</span>
        </h2>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        <!-- 左側文字區塊 -->
        <div class="lg:col-span-5">
          <h3 class="text-3xl font-bold text-gray-800 mb-6">
            今天想喝什麼呢?
          </h3>
          <p class="text-gray-600 mb-8 leading-relaxed">
            在我們的飲品推薦平台，每一杯飲品都是一次獨特的體驗。透過先進的文字探勘技術和情感分析，
            我們精準解讀用戶的評價和偏好，為您提供最貼心的推薦服務。
          </p>
          <a href="#" class="inline-flex items-center text-blue-500 font-semibold hover:text-blue-600">
            Learn More <i class="fas fa-arrow-right ml-2"></i>
          </a>
        </div>

        <!-- 右側特色區塊 -->
        <div class="lg:col-span-7 grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- 特色 1 -->
          <div class="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition duration-300">
            <div class="text-blue-500 text-3xl mb-4">
              <i class="fas fa-robot"></i>
            </div>
            <h4 class="text-xl font-bold text-gray-800 mb-3">智能分析</h4>
            <p class="text-gray-600">
              運用先進的文字探勘技術，精準分析用戶評價和偏好，提供最適合的飲品推薦
            </p>
          </div>

          <!-- 特色 2 -->
          <div class="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition duration-300">
            <div class="text-blue-500 text-3xl mb-4">
              <i class="fas fa-chart-line"></i>
            </div>
            <h4 class="text-xl font-bold text-gray-800 mb-3">即時趨勢</h4>
            <p class="text-gray-600">
              實時追蹤飲品趨勢，掌握最新市場動向，讓您的選擇永遠走在潮流尖端
            </p>
          </div>

          <!-- 特色 3 -->
          <div class="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition duration-300">
            <div class="text-blue-500 text-3xl mb-4">
              <i class="fas fa-comments"></i>
            </div>
            <h4 class="text-xl font-bold text-gray-800 mb-3">社群互動</h4>
            <p class="text-gray-600">
              分享您的品飲體驗，與其他飲品愛好者交流心得，建立活躍的社群
            </p>
          </div>

          <!-- 特色 4 -->
          <div class="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition duration-300">
            <div class="text-blue-500 text-3xl mb-4">
              <i class="fas fa-map-marker-alt"></i>
            </div>
            <h4 class="text-xl font-bold text-gray-800 mb-3">在地化推薦</h4>
            <p class="text-gray-600">
              根據您的位置，推薦周邊最受歡迎的飲品店家，讓美味觸手可及
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.container {
  margin-left: auto;
  margin-right: auto;
}

@media (min-width: 1280px) {
  .container {
    max-width: 1140px;
  }
}

/* 卡片懸浮效果 */
.hover\:shadow-xl:hover {
  transform: translateY(-5px);
}
</style> 