<template>
  <section id="features" class="py-20 bg-gray-50">
    <div class="container mx-auto px-4">
      <h2 class="text-3xl font-bold text-center mb-12">平台特色</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition duration-300">
          <div class="text-gray-800 mb-4 text-4xl">
            <i class="fas fa-brain"></i>
          </div>
          <h3 class="text-xl font-bold mb-4">智能分析</h3>
          <p class="text-gray-600">
            運用先進的文字探勘技術，精準分析用戶評價和偏好，提供最適合的飲品推薦。
          </p>
        </div>
        <div class="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition duration-300">
          <div class="text-gray-800 mb-4 text-4xl">
            <i class="fas fa-chart-line"></i>
          </div>
          <h3 class="text-xl font-bold mb-4">即時趨勢</h3>
          <p class="text-gray-600">
            實時追蹤飲品趨勢，掌握最新市場動向，讓您的選擇永遠走在潮流尖端。
          </p>
        </div>
        <div class="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition duration-300">
          <div class="text-gray-800 mb-4 text-4xl">
            <i class="fas fa-user-friends"></i>
          </div>
          <h3 class="text-xl font-bold mb-4">社群互動</h3>
          <p class="text-gray-600">
            建立活躍的飲品愛好者社群，分享心得、交流經驗，創造更豐富的品味體驗。
          </p>
        </div>
      </div>
      <div class="text-center mt-16">
        <router-link to="/features" 
          class="inline-flex items-center px-6 py-3 bg-gray-800 text-white rounded-lg 
                 hover:bg-gray-700 transition duration-300">
          <i class="fas fa-arrow-right mr-2"></i>
          查看更多特色
        </router-link>
      </div>
    </div>
  </section>
</template> 