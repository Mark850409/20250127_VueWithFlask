<template>
  <section class="relative min-h-[600px] overflow-hidden flex items-center">
    <!-- 背景圖片 -->
    <div class="absolute inset-0 bg-fixed">
      <div 
        class="w-full h-full bg-cover bg-center bg-no-repeat" 
        :style="{ backgroundImage: `url(${bannerData.image_url || defaultImage})` }">
      </div>
      <div class="absolute inset-0 bg-gradient-to-b from-black/70 to-black/50"></div>
    </div>

    <!-- 內容 -->
    <div class="call-to-action-section relative container mx-auto px-4 text-center text-white py-20">
      <h2 class="text-4xl font-bold mb-6" v-text="bannerData.title || '尋找您的完美飲品'"></h2>
      <p class="text-lg mb-8 max-w-3xl mx-auto" v-text="bannerData.subtitle || '透過我們的智能推薦系統，為您找到最適合的飲品選擇'"></p>
      <p class="text-base mb-8 max-w-2xl mx-auto" v-text="bannerData.description"></p>
      <a href="#home" 
         @click.prevent="scrollToTop"
         class="call-to-action-btn inline-flex items-center px-8 py-3 bg-white text-black 
                hover:bg-white/90 rounded-full transition duration-300
                font-semibold text-lg">
        開始探索
      </a>
    </div>
  </section>
</template>

<script>
import { ref, onMounted } from 'vue'
import bannerApi from '@/api/modules/banner'

export default {
  setup() {
    const bannerData = ref({})
    const defaultImage = 'https://images.unsplash.com/photo-1455225761879-2ed774963809?q=80&w=2070&auto=format&fit=crop'

    const fetchBannerData = async () => {
      try {
        const response = await bannerApi.getBannersByType('food')
        if (response.data?.data?.length > 0) {
          bannerData.value = response.data.data[0]
        }
      } catch (error) {
        console.error('獲取輪播圖數據失敗:', error)
      }
    }

    onMounted(() => {
      fetchBannerData()
    })

    return {
      bannerData,
      defaultImage
    }
  },
  methods: {
    scrollToTop() {
      const element = document.getElementById('home')
      if (element) {
        element.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        })
      }
    }
  }
}
</script>

<style scoped>
.container {
  margin-left: auto;
  margin-right: auto;
}

/* 背景固定效果 */
.bg-fixed {
  @apply fixed inset-0 w-full h-full;
  background-attachment: fixed;
  min-height: 180px;
}

/* 漸變背景效果 */
.from-black\/70 {
  --tw-gradient-from: rgb(0 0 0 / 0.7);
  --tw-gradient-to: rgb(0 0 0 / 0.5);
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to);
}

</style> 