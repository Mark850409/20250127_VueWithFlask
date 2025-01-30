<template>
  <div class="min-h-screen flex flex-col">
    <!-- 前台 Navbar -->
    <Navbar />
    
    <!-- 主要內容區域 -->
    <main class="flex-1">
      <router-view></router-view>
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
  }
}
</script> 