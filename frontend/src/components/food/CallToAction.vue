<template>
  <section class="relative py-20 overflow-hidden">
    <!-- 背景圖片 -->
    <div class="absolute inset-0 bg-fixed">
      <div class="w-full h-full bg-center bg-no-repeat bg-cover"
           style="background-image: url('https://images.unsplash.com/photo-1544145945-f90425340c7e');">
      </div>
      <div class="absolute inset-0 bg-gradient-to-b from-black/70 to-black/50"></div>
    </div>

    <!-- 內容 -->
    <div class="relative container mx-auto px-4 text-center text-white">
      <h2 class="text-4xl font-bold mb-6">
        尋找您的完美飲品
      </h2>
      <p class="text-lg mb-8 max-w-3xl mx-auto">
        透過我們的智能推薦系統，為您找到最適合的飲品選擇。
        無論是清爽的茶飲、香醇的咖啡，還是創意特調，
        讓我們一起探索屬於您的獨特風味。
      </p>
      <a href="#home" 
         @click.prevent="scrollToTop"
         class="inline-flex items-center px-8 py-3 bg-white text-black 
                hover:bg-white/90 rounded-full transition duration-300
                font-semibold text-lg">
        開始探索
      </a>
    </div>
  </section>
</template>

<script>
export default {
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

@media (min-width: 1280px) {
  .container {
    max-width: 1140px;
  }
}

/* 背景固定效果 */
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

/* 漸變背景效果 */
.from-black\/70 {
  --tw-gradient-from: rgb(0 0 0 / 0.7);
  --tw-gradient-to: rgb(0 0 0 / 0.5);
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to);
}
</style> 