<template>
  <!-- 圖片預覽 Modal -->
  <Transition name="fade">
    <div v-if="previewImageUrl" 
         class="fixed inset-0 bg-black/90 backdrop-blur-sm z-[99999] flex items-center justify-center"
         @click="closePreview">
      <div class="relative w-full h-full flex items-center justify-center p-4">
        <!-- 關閉按鈕 -->
        <button class="absolute top-4 right-4 text-white/80 hover:text-white transition-colors z-[100000]"
                @click="closePreview">
          <i class="fas fa-times text-2xl"></i>
        </button>
        <!-- 圖片容器 -->
        <img :src="previewImageUrl"
             class="max-w-full max-h-full object-contain select-none"
             @click.stop
             alt="圖片預覽">
      </div>
    </div>
  </Transition>

  <div class="min-h-screen bg-gray-50 pt-16">
    <PageBanner
      :title="currentBanner.title"
      :subtitle="currentBanner.subtitle"
      :description="currentBanner.description"
      :bannerImages="bannerData.bannerImages"
      :currentImageIndex="currentIndex"
      @update:currentIndex="updateIndex"
    />

    <!-- 新的主要內容區域 -->
    <div class="container mx-auto px-4 py-12 max-w-5xl">
      <h1 class="text-2xl md:text-3xl font-bold text-gray-900 mb-8">
        學習中心
      </h1>
      
      <!-- 卡片列表 -->
      <div class="grid grid-cols-1 gap-6">
        <div v-for="section in sections" 
             :key="section.id"
             class="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition-all duration-300">
          <!-- 卡片標題區 -->
          <div class="px-8 py-6 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-white">
            <div class="flex items-center justify-between cursor-pointer"
                 @click="toggleSection(`section-${section.id}`)">
              <div class="flex items-center space-x-4">
                <div class="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center shadow-inner">
                  <i class="ri-book-open-line text-blue-500 text-xl"></i>
                </div>
                <h3 class="text-xl font-bold text-gray-800 tracking-wide">{{ section.title }}</h3>
              </div>
              <i class="fas fa-chevron-down text-gray-400 transform transition-transform duration-200"
                 :class="{ 'rotate-180': openSections[`section-${section.id}`] }"></i>
            </div>
          </div>
          
          <!-- 卡片內容區 -->
          <div v-show="openSections[`section-${section.id}`]" 
               class="divide-y divide-gray-100 bg-white">
            <div v-for="subsection in section.subsections" 
                 :key="subsection.id"
                 class="px-8 py-6 hover:bg-gray-50/50 transition-all duration-300">
              <div class="flex items-start space-x-4">
                <div class="flex-shrink-0 mt-1.5">
                  <i class="ri-robot-2-line text-blue-500/70"></i>
                </div>
                <div class="flex-1">
                  <h4 class="text-lg font-semibold text-gray-800 mb-3">
                    {{ subsection.title }}
                  </h4>
                  <p class="text-base text-gray-600 leading-relaxed mb-6 whitespace-pre-line">
                    {{ subsection.content }}
                  </p>
                  
                  <!-- 圖片預覽區 -->
                  <div v-if="subsection.images?.length" 
                       class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
                    <div v-for="(image, index) in subsection.images" 
                         :key="index"
                         class="relative aspect-video rounded-xl overflow-hidden bg-gray-100 cursor-zoom-in shadow-sm hover:shadow-md transition-all duration-300"
                         @click="previewImage(getImageUrl(image))">
                      <img :src="getImageUrl(image)"
                           :alt="`${subsection.title} 圖片 ${index + 1}`"
                           class="w-full h-full object-cover hover:opacity-90 transition-opacity"/>
                    </div>
                  </div>
                  
                  <!-- 提示區塊 -->
                  <div v-if="subsection.tips" 
                       class="my-6 p-5 bg-gradient-to-r from-amber-50 to-yellow-50 rounded-xl border border-yellow-100/50 shadow-sm">
                    <div class="flex items-start space-x-3">
                      <i class="fas fa-lightbulb text-amber-500 text-lg mt-0.5"></i>
                      <p class="text-base text-amber-900 leading-relaxed">{{ subsection.tips }}</p>
                    </div>
                  </div>
                  
                  <!-- 相關連結 -->
                  <div v-if="subsection.links?.length" 
                       class="mt-6 flex flex-wrap gap-3">
                    <a v-for="(link, index) in subsection.links"
                       :key="index"
                       :href="link.url"
                       target="_blank"
                       class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-blue-50 text-blue-600 hover:bg-blue-100 hover:shadow-sm transition-all duration-300">
                      <i class="fas fa-external-link-alt mr-2 text-xs opacity-70"></i>
                      {{ link.title }}
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import PageBanner from '../PageBanner.vue'
import learningAPI from '@/api/modules/learning'
import bannerAPI from '@/api/modules/banner'

export default {
  components: {
    PageBanner
  },
  data() {
    return {
      openSections: {},
      activeSection: '',
      sections: [],
      previewImageUrl: null,
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
      const response = await bannerAPI.getBannersByType('learning')
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
    fetchSections() {
      learningAPI.getLearningBlocks()
        .then(response => {
          this.sections = response.data.sections || []
          this.sections.forEach(section => {
            if (section.subsections) {
              section.subsections.forEach(sub => {
                this.openSections[sub.id] = false
              })
            }
          })
          if (this.sections[0]?.subsections?.[0]) {
            this.openSections[this.sections[0].subsections[0].id] = true
          }
        })
        .catch(error => {
          console.error('獲取學習內容失敗:', error)
        })
    },
    toggleSection(sectionId) {
      this.openSections[sectionId] = !this.openSections[sectionId]
    },
    updateActiveSection() {
      const sections = document.querySelectorAll('section[id]')
      const scrollPosition = window.scrollY + 100

      sections.forEach(section => {
        const sectionTop = section.offsetTop
        const sectionHeight = section.offsetHeight
        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
          this.activeSection = section.id
        }
      })
    },
    getImageUrl(image) {
      if (!image) return ''
      if (image.startsWith('http')) return image
      return `${import.meta.env.VITE_BACKEND_URL}/api/learning/uploads/${image.split('/').pop()}`
    },
    previewImage(url) {
      this.previewImageUrl = url
      document.body.style.overflow = 'hidden'
      document.body.style.paddingRight = '0px'
    },
    closePreview() {
      this.previewImageUrl = null
      document.body.style.overflow = ''
      document.body.style.paddingRight = ''
    },
    updateIndex(newIndex) {
      this.currentIndex = newIndex
    },
    handleKeyDown(e) {
      if (e.key === 'Escape' && this.previewImageUrl) {
        this.closePreview()
      }
    }
  },
  mounted() {
    this.currentIndex = 0
    window.addEventListener('scroll', this.updateActiveSection)
    this.updateActiveSection()
    this.fetchSections()
    window.addEventListener('keydown', this.handleKeyDown)
  },
  unmounted() {
    window.removeEventListener('scroll', this.updateActiveSection)
    window.removeEventListener('keydown', this.handleKeyDown)
    document.body.style.overflow = ''
    document.body.style.paddingRight = ''
  }
}
</script>

<style scoped>
/* 平滑滾動 */
html {
  scroll-behavior: smooth;
}

/* 固定側邊欄 */
.sticky {
  position: sticky;
  top: 6rem;
}

/* 內容區塊間距 */
section {
  scroll-margin-top: 6rem;
}

/* 淡入淡出動畫 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 圖片預覽時禁用選取 */
.select-none {
  user-select: none;
  -webkit-user-select: none;
}

/* 文字內容樣式 */
.prose {
  @apply text-base;
}

.prose p {
  @apply mb-4 last:mb-0;
}

.prose ul {
  @apply list-disc pl-6 mb-4;
}

.prose ol {
  @apply list-decimal pl-6 mb-4;
}

.prose strong {
  @apply font-semibold text-gray-900;
}

.prose em {
  @apply italic text-gray-800;
}

.prose code {
  @apply px-1.5 py-0.5 bg-gray-100 rounded text-sm font-mono text-gray-800;
}

.prose blockquote {
  @apply pl-4 border-l-4 border-gray-200 text-gray-700 italic;
}
</style> 