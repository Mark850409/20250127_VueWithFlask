<template>
  <section id="learning" class="py-20 bg-white">
    <div class="container mx-auto px-4 max-w-6xl">
      <!-- 標題區塊 -->
      <div class="text-center mb-16">
        <span class="span-title inline-block px-4 py-1 bg-blue-50 text-blue-500 font-medium rounded-full mb-4">
          LEARNING
        </span>
        <h2 class="text-4xl font-bold text-gray-900">
          學習中心
        </h2>
      </div>

      <!-- 卡片區塊 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- 功能導覽 -->
        <div class="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition duration-300">
          <div class="text-blue-500 text-3xl mb-4">
            <i class="fas fa-book-open"></i>
          </div>
          <h3 class="text-xl font-bold mb-3 text-gray-800">功能導覽</h3>
          <p class="text-gray-600 leading-relaxed mb-4">
            了解系統各項功能的使用方式，快速上手推薦系統。
          </p>
        </div>

        <!-- 常見問題 -->
        <div class="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition duration-300">
          <div class="text-blue-500 text-3xl mb-4">
            <i class="fas fa-question-circle"></i>
          </div>
          <h3 class="text-xl font-bold mb-3 text-gray-800">常見問題</h3>
          <p class="text-gray-600 leading-relaxed mb-4">
            解答使用過程中常見的疑問，幫助您更順暢地使用系統。
          </p>
        </div>

        <!-- 使用教學 -->
        <div class="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition duration-300">
          <div class="text-blue-500 text-3xl mb-4">
            <i class="fas fa-video"></i>
          </div>
          <h3 class="text-xl font-bold mb-3 text-gray-800">使用教學</h3>
          <p class="text-gray-600 leading-relaxed mb-4">
            觀看詳細的操作示範影片，掌握系統的進階功能。
          </p>
        </div>
      </div>

      <!-- 探索更多按鈕 -->
      <div class="text-center mt-12">
        <a href="/learning" class="learning-btn inline-flex items-center px-8 py-3 bg-white text-black hover:bg-white/90 rounded-full transition duration-300 font-semibold text-lg">
          <i class="fas fa-search mr-2"></i>
          探索更多資源
        </a>
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