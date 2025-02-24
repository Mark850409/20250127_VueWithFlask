<template>
  <footer class="front-footer relative py-16 overflow-hidden">
    <!-- 背景圖片 -->
    <div class="absolute inset-0 bg-fixed">
      <div 
        class="w-full h-full bg-center bg-no-repeat bg-cover"
        :style="{ backgroundImage: `url(${bannerData.image_url || defaultImage})` }">
      </div>
      <div class="absolute inset-0 bg-gradient-to-b from-gray-900/80 to-gray-900/75"></div>
    </div>

    <!-- 內容區域 -->
    <div class="relative container mx-auto px-4 text-gray-400">
      <!-- 主要內容區 -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-12">
        <!-- 品牌介紹區塊 -->
        <div>
          <div class="flex items-center mb-4">
            <i class="ri-drinks-2-line text-blue-500 text-2xl mr-2"></i>
            <h2 class="text-xl font-bold text-white" v-text="bannerData.title || '今天想喝什麼呢？'"></h2>
          </div>
          <p class="text-gray-400 leading-loose mb-2" v-text="bannerData.subtitle"></p>
          <p class="text-gray-400 leading-loose" v-text="bannerData.description"></p>
        </div>

        <!-- 網站導覽 -->
        <div>
          <h3 class="text-lg font-semibold text-white mb-6">網站導覽</h3>
          <ul class="space-y-4">
            <li>
              <a href="/#home" 
                 class="hover:text-blue-400 transition-colors"
                 @click.prevent="scrollToSection('home')">首頁</a>
            </li>
            <li>
              <a href="/#about" 
                 class="hover:text-blue-400 transition-colors"
                 @click.prevent="scrollToSection('about')">關於我們</a>
            </li>
            <li>
              <a href="/#features" 
                 class="hover:text-blue-400 transition-colors"
                 @click.prevent="scrollToSection('features')">平台特色</a>
            </li>
            <li>
              <a href="/#learning" 
                 class="hover:text-blue-400 transition-colors"
                 @click.prevent="scrollToSection('learning')">學習中心</a>
            </li>
            <li>
              <a href="/#pricing" 
                 class="hover:text-blue-400 transition-colors"
                 @click.prevent="scrollToSection('pricing')">定價方案</a>
            </li>
          </ul>
        </div>

        <!-- 聯絡資訊 -->
        <div>
          <h3 class="text-lg font-semibold text-white mb-6">聯絡我們</h3>
          <ul class="space-y-4">
            <li class="flex items-center">
              <i class="fas fa-map-marker-alt w-5"></i>
              <span>台北市信義區忠孝東路五段2號</span>
            </li>
            <li class="flex items-center">
              <i class="fas fa-phone w-5"></i>
              <span>(02) 2720-1230</span>
            </li>
            <li class="flex items-center">
              <i class="fas fa-envelope w-5"></i>
              <span>info@drinktoday.tw</span>
            </li>
          </ul>
        </div>

        <!-- 關注我們 -->
        <div>
          <h3 class="text-lg font-semibold text-white mb-6">關注我們</h3>
          <div class="flex space-x-4">
            <a href="#" class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-blue-500 transition duration-300">
              <i class="fab fa-facebook-f"></i>
            </a>
            <a href="#" class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-green-500 transition duration-300">
              <i class="fab fa-line"></i>
            </a>
            <a href="#" class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-pink-500 transition duration-300">
              <i class="fab fa-instagram"></i>
            </a>
            <a href="#" class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-blue-400 transition duration-300">
              <i class="fas fa-envelope"></i>
            </a>
          </div>
        </div>
      </div>

      <!-- 版權聲明 -->
      <div class="mt-12 pt-8 border-t border-gray-800/50">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <div class="text-sm">
            <p class="mb-2">
              Copyright © {{ currentYear }} 今天想喝什麼呢? All Rights Reserved.
            </p>
            <p class="text-gray-500">
              本網站受中華民國著作權法及國際著作權法律保護
              <br class="hidden md:block">
              未經授權禁止複製、散布或其他商業行為
            </p>
          </div>
          <div class="mt-4 md:mt-0 text-sm text-gray-400">
            <p>Designed & Developed by</p>
            <p class="font-medium text-gray-300">Mark HSU</p>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
import { ref, onMounted } from 'vue'
import bannerApi from '@/api/modules/banner'

export default {
  setup() {
    const bannerData = ref({})
    const currentYear = new Date().getFullYear()
    const defaultImage = 'https://plus.unsplash.com/premium_photo-1661580970887-702a4c221027?q=80&w=1932&auto=format&fit=crop'

    const fetchBannerData = async () => {
      try {
        const response = await bannerApi.getBannersByType('footer')
        if (response.data?.data?.length > 0) {
          bannerData.value = response.data.data[0]
        }
      } catch (error) {
        console.error('獲取頁腳輪播圖數據失敗:', error)
      }
    }

    onMounted(() => {
      fetchBannerData()
    })

    return {
      bannerData,
      currentYear,
      defaultImage
    }
  },
  methods: {
    scrollToSection(sectionId) {
      const element = document.getElementById(sectionId)
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

/* 背景效果 */
.bg-fixed {
  background-attachment: fixed;
}

.bg-center {
  background-position: center;
}

.bg-no-repeat {
  background-repeat: no-repeat;
}

.bg-cover {
  background-size: cover;
}

/* 社群按鈕懸浮效果 */
.rounded-full {
  transition: all 0.3s ease;
}

.rounded-full:hover {
  transform: translateY(-2px);
}

/* 漸層背景 */
.from-gray-900\/80 {
  --tw-gradient-from: rgb(17 24 39 / 0.80);
  --tw-gradient-to: rgb(17 24 39 / 0.75);
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to);
}

/* 添加滾動行為 */
html {
  scroll-behavior: smooth;
}
</style> 