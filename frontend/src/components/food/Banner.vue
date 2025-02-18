<template>
  <PageBanner
    :title="currentBanner.title"
    :subtitle="currentBanner.subtitle"
    :description="currentBanner.description"
    :bannerImages="bannerData.bannerImages"
    :currentImageIndex="currentIndex"
    @update:currentIndex="updateIndex"
  />
</template>

<script>
import PageBanner from './PageBanner.vue'
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
    // 計算當前要顯示的 banner 內容
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
      const response = await bannerAPI.getBannersByType('home')
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
    // 確保從第一張圖開始
    this.currentIndex = 0
  }
}
</script> 