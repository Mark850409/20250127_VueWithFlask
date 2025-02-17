<template>
  <div class="min-h-screen flex flex-col">
    <!-- 前台 Navbar -->
    <Navbar />
    
    <!-- 主要內容區域 -->
    <main class="flex-1">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 前台 Footer -->
    <Footer />
  </div>
</template>

<script>
import Navbar from '../components/common/Navbar.vue'
import Footer from '../components/common/Footer.vue'

export default {
  name: 'FrontLayout',
  components: {
    Navbar,
    Footer
  },
  mounted() {
    // 添加滾動監聽
    this.initScrollAnimation()
  },
  beforeUnmount() {
    // 移除滾動監聽
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    initScrollAnimation() {
      // 初始化需要動畫的元素
      const animatedElements = document.querySelectorAll('.fade-in-section')
      this.handleScroll = () => {
        animatedElements.forEach(element => {
          const elementTop = element.getBoundingClientRect().top
          const elementBottom = element.getBoundingClientRect().bottom
          
          // 當元素進入視窗時添加動畫類
          if (elementTop < window.innerHeight && elementBottom > 0) {
            element.classList.add('is-visible')
          }
        })
      }
      
      // 添加滾動監聽
      window.addEventListener('scroll', this.handleScroll)
      // 初始檢查
      this.handleScroll()
    }
  }
}
</script>

<style>
/* 路由切換動畫 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 滾動載入動畫 */
.fade-in-section {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
  will-change: opacity, transform;
}

.fade-in-section.is-visible {
  opacity: 1;
  transform: translateY(0);
}

/* 為了確保平滑滾動 */
html {
  scroll-behavior: smooth;
}
</style> 