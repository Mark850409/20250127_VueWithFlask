<template>
  <section class="relative h-screen overflow-hidden bg-black -mt-16">
    <!-- 輪播圖片 -->
    <div class="absolute inset-0">
      <transition-group name="fade">
        <img v-if="hasImages"
             v-for="(image, index) in bannerImages" 
             :key="image.id"
             v-show="currentImageIndex === index"
             :src="image.image_url" 
             class="w-full h-full object-cover transition-opacity duration-500"
             :alt="image.alt">
        <!-- 無圖片時顯示預設背景 -->
        <div v-else
             key="default-bg"
             class="w-full h-full bg-gray-900"></div>
      </transition-group>
      <!-- 深色漸層遮罩 -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/50 to-black/30"></div>
    </div>

    <!-- 只在有圖片時顯示箭頭 -->
    <div v-if="hasImages" 
         class="absolute inset-x-0 top-1/2 -translate-y-1/2 flex justify-between items-center px-4 pointer-events-none z-30">
      <button @click.stop="prevSlide" 
              class="w-12 h-12 flex items-center justify-center 
                     text-white/70 hover:text-white bg-black/30 hover:bg-black/50 rounded-full 
                     transition-all duration-300 cursor-pointer pointer-events-auto z-30">
        <i class="fas fa-chevron-left text-2xl"></i>
      </button>
      <button @click.stop="nextSlide"
              class="w-12 h-12 flex items-center justify-center 
                     text-white/70 hover:text-white bg-black/30 hover:bg-black/50 rounded-full 
                     transition-all duration-300 cursor-pointer pointer-events-auto z-30">
        <i class="fas fa-chevron-right text-2xl"></i>
      </button>
    </div>

    <!-- Banner 內容 -->
    <div class="absolute inset-0 flex items-center justify-center pt-16 z-20">
      <div class="container mx-auto px-4 text-center text-white">
        <h1 class="banner-title text-5xl font-bold mb-4">{{ title }}</h1>
        <p class="banner-subtitle text-xl mb-6">{{ subtitle }}</p>
        <p class="banner-description text-lg mb-8 max-w-2xl mx-auto text-gray-200">
          {{ description }}
        </p>
        <div class="flex justify-center">
          <a href="#features" 
             @click.prevent="scrollToSection('features')"
             class="banner-btn inline-flex items-center px-8 py-3 bg-white text-black 
                    hover:bg-white/90 rounded-full transition duration-300
                    font-semibold text-lg">
            GET STARTED
          </a>
        </div>
      </div>
    </div>

    <!-- 只在有圖片時顯示輪播控制按鈕 -->
    <div v-if="hasImages"
         class="absolute bottom-6 left-1/2 transform -translate-x-1/2 flex space-x-2 z-30">
      <button v-for="(_, index) in bannerImages"
              :key="index"
              @click="updateCurrentIndex(index)"
              class="banner-control-btn w-3 h-3 rounded-full transition-all duration-300"
              :class="currentImageIndex === index ? 'bg-white scale-125' : 'bg-white/50 hover:bg-white/70'">
      </button>
    </div>
  </section>
</template>

<script>
export default {
  name: 'PageBanner',
  props: {
    title: {
      type: String,
      required: true
    },
    subtitle: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    },
    bannerImages: {
      type: Array,
      required: true,
      default: () => []
    },
    currentImageIndex: {
      type: Number,
      required: true,
      default: 0
    }
  },
  emits: ['update:currentIndex'],
  data() {
    return {
      autoPlayInterval: null
    }
  },
  computed: {
    hasImages() {
      return this.bannerImages && this.bannerImages.length > 0
    }
  },
  mounted() {
    if (this.hasImages) {
      this.$emit('update:currentIndex', 0)
      this.startAutoPlay()
    }
  },
  beforeUnmount() {
    this.stopAutoPlay()
  },
  methods: {
    prevSlide() {
      if (!this.hasImages) return
      const newIndex = (this.currentImageIndex - 1 + this.bannerImages.length) % this.bannerImages.length
      this.$emit('update:currentIndex', newIndex)
    },
    nextSlide() {
      if (!this.hasImages) return
      const newIndex = (this.currentImageIndex + 1) % this.bannerImages.length
      this.$emit('update:currentIndex', newIndex)
    },
    updateCurrentIndex(index) {
      this.$emit('update:currentIndex', index)
    },
    startAutoPlay() {
      if (!this.hasImages) return
      this.stopAutoPlay()
      this.autoPlayInterval = setInterval(() => {
        this.nextSlide()
      }, 5000)
    },
    stopAutoPlay() {
      if (this.autoPlayInterval) {
        clearInterval(this.autoPlayInterval)
        this.autoPlayInterval = null
      }
    },
    scrollToSection(sectionId) {
      const element = document.getElementById(sectionId)
      if (element) {
        element.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        })
      }
    }
  },
  watch: {
    bannerImages: {
      handler(newVal) {
        if (newVal && newVal.length > 0) {
          this.startAutoPlay()
        } else {
          this.stopAutoPlay()
        }
      },
      immediate: true
    }
  }
}
</script>

<style scoped>
/* 修改淡入淡出效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.8s ease-in-out;
  position: absolute;
  width: 100%;
  height: 100%;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}

/* 確保圖片容器定位正確 */
.relative {
  position: relative;
}

/* 確保所有圖片佔滿容器 */
img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  background-color: black;
}

/* 箭頭按鈕在 hover 時的效果 */
button:hover i {
  transform: scale(1.1);
}

button i {
  transition: transform 0.2s;
}

/* 恢復箭頭按鈕的 z-index 設定 */
button {
  position: relative;
  z-index: 30;
}

/* 確保內容區域在遮罩之上 */
.container {
  position: relative;
  z-index: 20;
}

/* 添加滾動行為 */
html {
  scroll-behavior: smooth;
}
</style> 