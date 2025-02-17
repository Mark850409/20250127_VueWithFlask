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
    <!-- Banner 區塊保持不變 -->
    <PageBanner
      title="學習中心"
      subtitle="功能導覽・使用教學"
      description="我們提供完整的功能說明和使用教學，幫助您快速掌握系統的各項功能。
                  無論是新手入門還是進階應用，都能在這裡找到答案。"
    />

    <!-- 主要內容區域 -->
    <div class="container mx-auto px-4 py-12">
      <div class="flex gap-12">
        <!-- 左側導航選單 -->
        <div class="w-72 flex-shrink-0">
          <div class="sticky top-24 p-6 bg-white rounded-lg shadow-sm">
            <h3 class="text-xl font-bold mb-6">功能導覽</h3>
            <ul class="space-y-3">
              <li v-for="section in sections" :key="section.id">
                <a :href="`#section-${section.id}`"
                   class="block py-2 px-4 rounded-lg transition-colors hover:bg-blue-50 hover:text-blue-600"
                   :class="{ 'bg-blue-50 text-blue-600': activeSection === `section-${section.id}` }">
                   {{ section.title }}
                </a>
                <!-- 次標題選單 -->
                <ul v-if="section.subsections?.length" class="mt-2 space-y-2">
                  <li v-for="sub in section.subsections" :key="sub.id">
                    <a :href="`#subsection-${sub.id}`"
                       class="block py-2 px-4 rounded-lg transition-colors hover:bg-blue-50 hover:text-blue-600 pl-8"
                       :class="{ 'bg-blue-50 text-blue-600': activeSection === `subsection-${sub.id}` }">
                       {{ sub.title }}
                    </a>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
        </div>

        <!-- 右側內容區域 -->
        <div class="flex-1 max-w-3xl">
          <!-- 動態內容區域 -->
          <div v-for="section in sections" :key="section.id" class="mb-16">
            <section :id="`section-${section.id}`">
              <h2 class="text-3xl font-bold mb-8">{{ section.title }}</h2>
            
              <!-- 次標題內容 -->
              <div v-for="subsection in section.subsections" 
                   :key="subsection.id" 
                   :id="`subsection-${subsection.id}`"
                   class="mb-12">
                <div class="bg-white rounded-xl shadow-sm overflow-hidden">
                  <div class="flex items-center p-6 cursor-pointer" 
                       @click="toggleSection(subsection.id)">
                    <i class="fas fa-chevron-right mr-2 transform transition-transform duration-200"
                       :class="{ 'rotate-90': openSections[subsection.id] }"></i>
                    <h3 class="text-xl font-semibold">{{ subsection.title }}</h3>
                  </div>
                  
                  <div v-show="openSections[subsection.id]" class="px-6 pb-6">
                    <!-- 圖片區域 -->
                    <div v-if="subsection.images?.length" 
                         class="mb-6">
                      <div v-for="(image, index) in subsection.images" 
                           :key="index"
                           class="bg-white rounded-lg shadow-sm overflow-hidden mb-6 relative"
                           style="min-height: 400px">
                        <img :src="getImageUrl(image)"
                             :alt="`${subsection.title} 圖片 ${index + 1}`"
                             class="w-full h-full absolute inset-0 object-contain cursor-zoom-in hover:opacity-90 transition-opacity"
                             @click="previewImage(getImageUrl(image))"/>
                      </div>
                    </div>
                    
                    <!-- 文字內容 -->
                    <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-8 mb-6">
                      <!-- 內容標題 -->
                      <h4 class="text-lg font-medium text-gray-900 mb-4">
                        <i class="fas fa-info-circle mr-2 text-blue-500"></i>
                        說明內容
                      </h4>
                      <!-- 內容文字 -->
                      <div class="prose prose-blue max-w-none">
                        <p class="text-gray-600 leading-relaxed whitespace-pre-line">
                          {{ subsection.content }}
                        </p>
                      </div>
                      <!-- 補充提示 -->
                      <div v-if="subsection.tips" 
                           class="mt-6 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded">
                        <p class="text-yellow-800">
                          <i class="fas fa-lightbulb mr-2"></i>
                          <span class="font-medium">提示：</span>
                          {{ subsection.tips }}
                        </p>
                      </div>
                      <!-- 相關連結 -->
                      <div v-if="subsection.links?.length" class="mt-6">
                        <h5 class="font-medium text-gray-900 mb-2">相關連結：</h5>
                        <ul class="space-y-2">
                          <li v-for="(link, index) in subsection.links" 
                              :key="index"
                              class="text-blue-600 hover:text-blue-800">
                            <i class="fas fa-external-link-alt mr-2"></i>
                            <a :href="link.url" target="_blank" rel="noopener">
                              {{ link.title }}
                            </a>
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
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

export default {
  components: {
    PageBanner
  },
  setup() {
    const openSections = ref({})  // 改為空物件，根據實際資料動態添加
    const activeSection = ref('')
    const sections = ref([])
    const previewImageUrl = ref(null)
    
    // 獲取學習內容
    const fetchSections = async () => {
      try {
        const response = await learningAPI.getLearningBlocks()
        // 確保資料結構正確
        sections.value = response.data.sections || []
        
        // 初始化展開狀態
        sections.value.forEach(section => {
          if (section.subsections) {
            section.subsections.forEach(sub => {
              openSections.value[sub.id] = false
            })
          }
        })
        
        // 預設打開第一個區塊
        if (sections.value[0]?.subsections?.[0]) {
          openSections.value[sections.value[0].subsections[0].id] = true
        }
      } catch (error) {
        console.error('獲取學習內容失敗:', error)
      }
    }

    const toggleSection = (sectionId) => {
      openSections.value[sectionId] = !openSections.value[sectionId]
    }

    const updateActiveSection = () => {
      const sections = document.querySelectorAll('section[id]')
      const scrollPosition = window.scrollY + 100

      sections.forEach(section => {
        const sectionTop = section.offsetTop
        const sectionHeight = section.offsetHeight
        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
          activeSection.value = section.id
        }
      })
    }

    const getImageUrl = (image) => {
      if (!image) return ''
      if (image.startsWith('http')) return image
      return `${import.meta.env.VITE_BACKEND_URL}/api/learning/uploads/${image.split('/').pop()}`
    }

    const previewImage = (url) => {
      previewImageUrl.value = url
      // 保存當前滾動位置並禁用滾動
      document.body.style.overflow = 'hidden'
      document.body.style.paddingRight = '0px' // 防止滾動條消失導致頁面跳動
    }

    // 監聽 ESC 鍵關閉預覽
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && previewImageUrl.value) {
        closePreview()
      }
    }

    // 關閉預覽
    const closePreview = () => {
      previewImageUrl.value = null
      // 恢復滾動
      document.body.style.overflow = ''
      document.body.style.paddingRight = ''
    }

    onMounted(() => {
      window.addEventListener('scroll', updateActiveSection)
      updateActiveSection()
      fetchSections()
      window.addEventListener('keydown', handleKeyDown)
    })

    onUnmounted(() => {
      window.removeEventListener('scroll', updateActiveSection)
      window.removeEventListener('keydown', handleKeyDown)
      // 確保組件卸載時恢復滾動
      document.body.style.overflow = ''
      document.body.style.paddingRight = ''
    })

    return {
      openSections,
      toggleSection,
      activeSection,
      sections,
      getImageUrl,
      previewImage,
      previewImageUrl,
      closePreview
    }
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