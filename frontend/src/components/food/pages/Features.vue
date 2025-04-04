<template>
  <div class="min-h-screen bg-gray-50 pt-16">
    <PageBanner
      :title="currentBanner.title"
      :subtitle="currentBanner.subtitle"
      :description="currentBanner.description"
      :bannerImages="bannerData.bannerImages"
      :currentImageIndex="currentIndex"
      @update:currentIndex="updateIndex"
    />
    
    <!-- 詳細特色說明區塊 -->
    <div class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-12">深入了解我們的特色</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto mb-20">
          <!-- 特色項目詳細內容 -->
          <div class="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 border border-gray-100">
            <div class="text-gray-800 mb-6 text-5xl">
              <i class="fas fa-brain"></i>
            </div>
            <h2 class="text-2xl font-bold mb-4">智能分析</h2>
            <p class="text-gray-600 mb-6">
              運用先進的文字探勘技術，精準分析用戶評價和偏好，提供最適合的飲品推薦。
              我們的系統能夠理解用戶的細微需求，從海量數據中找出最匹配的選擇。
            </p>
            <ul class="space-y-3 text-gray-600">
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-3"></i>
                自然語言處理
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-3"></i>
                情感分析技術
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-3"></i>
                個性化推薦
              </li>
            </ul>
          </div>

          <div class="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 border border-gray-100">
            <div class="text-gray-800 mb-6 text-5xl">
              <i class="fas fa-chart-line"></i>
            </div>
            <h2 class="text-2xl font-bold mb-4">即時趨勢</h2>
            <p class="text-gray-600 mb-6">
              實時追蹤飲品趨勢，掌握最新市場動向，讓您的選擇永遠走在潮流尖端。
              系統會分析當前熱門選擇和季節性偏好，提供最及時的建議。
            </p>
            <ul class="space-y-3 text-gray-600">
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-3"></i>
                實時數據分析
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-3"></i>
                季節性推薦
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-3"></i>
                熱門排行榜
              </li>
            </ul>
          </div>

          <div class="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 border border-gray-100">
            <div class="text-gray-800 mb-6 text-5xl">
              <i class="fas fa-user-friends"></i>
            </div>
            <h2 class="text-2xl font-bold mb-4">社群互動</h2>
            <p class="text-gray-600 mb-6">
              建立活躍的飲品愛好者社群，分享心得、交流經驗，創造更豐富的品味體驗。
              透過社群互動，發現更多美味的可能性。
            </p>
            <ul class="space-y-3 text-gray-600">
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-3"></i>
                用戶評價分享
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-3"></i>
                社群互動功能
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-3"></i>
                個人化收藏
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PageBanner from '../PageBanner.vue'
import bannerAPI from '@/api/modules/banner'

export default {
  components: {
    PageBanner
  },
  data() {
    return {
      currentIndex: 0,
      bannerData: {
        bannerImages: []
      }
    }
  },
  computed: {
    currentBanner() {
      if (this.bannerData.bannerImages.length === 0) {
        return {
          title: '',
          subtitle: '',
          description: ''
        }
      }
      return this.bannerData.bannerImages[this.currentIndex] || this.bannerData.bannerImages[0]
    }
  },
  async created() {
    try {
      const response = await bannerAPI.getBannersByType('feature')
      if (response.data && response.data.data) {
        const banners = response.data.data
        this.bannerData.bannerImages = banners.map(banner => ({
          id: banner.id,
          image_url: banner.image_url,
          alt: banner.alt,
          title: banner.title,
          subtitle: banner.subtitle,
          description: banner.description
        }))
      }
    } catch (error) {
      console.error('Failed to fetch banner data:', error)
    }
  },
  methods: {
    updateIndex(newIndex) {
      this.currentIndex = newIndex
    }
  },
  mounted() {
    this.currentIndex = 0
  }
}
</script> 