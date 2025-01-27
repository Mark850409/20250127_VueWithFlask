<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 內容區域 -->
    <div class="pt-16"> <!-- 添加上邊距，為固定導航欄留出空間 -->
      <div id="home">
        <Banner />
      </div>

      <div id="recommend">
        <Recommendations />
      </div>

      <div id="about">
        <About />
      </div>

      <Footer />
    </div>
  </div>
</template>

<script>
import Banner from './Banner.vue'
import Recommendations from './Recommendations.vue'
import About from './About.vue'
import Footer from './Footer.vue'

export default {
  components: {
    Banner,
    Recommendations,
    About,
    Footer
  }
}
</script> 