<template>
  <div v-if="isLoggedIn">
    <!-- 熱門飲料店推薦 -->
    <section class="py-16 bg-white dark:bg-gray-900">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-8 text-gray-900 dark:text-white">熱門飲料店推薦</h2>
        
        <!-- 排序和視圖切換選項 -->
        <div class="flex justify-between items-center mb-8">
          <div class="flex space-x-4">
            <button 
              v-for="sort in sortOptions" 
              :key="sort.value"
              @click="currentSort = sort.value"
              :class="[
                'px-4 py-2 rounded-full transition duration-300',
                currentSort === sort.value 
                  ? 'bg-gray-800 text-white dark:bg-gray-700' 
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
              ]"
            >
              {{ sort.label }}
            </button>
          </div>
          
          <!-- 視圖切換按鈕 -->
          <div class="flex space-x-2">
            <button 
              @click="viewMode = 'grid'"
              :class="[
                'p-2 rounded-lg transition-colors',
                viewMode === 'grid' 
                  ? 'bg-gray-800 text-white dark:bg-gray-700' 
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
              ]"
            >
              <i class="fas fa-th-large"></i>
            </button>
            <button 
              @click="viewMode = 'list'"
              :class="[
                'p-2 rounded-lg transition-colors',
                viewMode === 'list' 
                  ? 'bg-gray-800 text-white dark:bg-gray-700' 
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
              ]"
            >
              <i class="fas fa-list"></i>
            </button>
          </div>
        </div>

        <!-- 飲料店列表 -->
        <DrinkShopList 
          :drinks="sortedDrinks" 
          :viewMode="viewMode" 
        />
      </div>
    </section>

    <!-- 您可能感興趣的飲料店 -->
    <section class="py-16 bg-gray-50 dark:bg-gray-800">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-8 text-gray-900 dark:text-white">您可能感興趣的飲料店</h2>
        
        <!-- 排序和視圖切換選項 -->
        <div class="flex justify-between items-center mb-8">
          <div class="flex space-x-4">
            <button 
              v-for="sort in sortOptions" 
              :key="sort.value"
              @click="currentRecommendSort = sort.value"
              :class="[
                'px-4 py-2 rounded-full transition duration-300',
                currentRecommendSort === sort.value 
                  ? 'bg-gray-800 text-white dark:bg-gray-700' 
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
              ]"
            >
              {{ sort.label }}
            </button>
          </div>
          
          <!-- 視圖切換按鈕 -->
          <div class="flex space-x-2">
            <button 
              @click="recommendViewMode = 'grid'"
              :class="[
                'p-2 rounded-lg transition-colors',
                recommendViewMode === 'grid' 
                  ? 'bg-gray-800 text-white dark:bg-gray-700' 
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
              ]"
            >
              <i class="fas fa-th-large"></i>
            </button>
            <button 
              @click="recommendViewMode = 'list'"
              :class="[
                'p-2 rounded-lg transition-colors',
                recommendViewMode === 'list' 
                  ? 'bg-gray-800 text-white dark:bg-gray-700' 
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
              ]"
            >
              <i class="fas fa-list"></i>
            </button>
          </div>
        </div>

        <!-- 推薦飲料店列表 -->
        <DrinkShopList 
          :drinks="sortedRecommendedDrinks" 
          :viewMode="recommendViewMode" 
        />
      </div>
    </section>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import DrinkShopList from './DrinkShopList.vue'
import axios from '@/utils/axios'

export default {
  components: {
    DrinkShopList
  },

  setup() {
    const authStore = useAuthStore()
    const isLoggedIn = computed(() => authStore.isLoggedIn)

    const viewMode = ref('grid')
    const recommendViewMode = ref('grid')
    const currentSort = ref('default')
    const currentRecommendSort = ref('default')

    const sortOptions = [
      { label: '預設排序', value: 'default' },
      { label: '評分排序', value: 'rating' },
      { label: '熱門排序', value: 'review_number' }
    ]

    // 店家數據
    const drinks = ref([])
    const recommendedDrinks = ref([])

    // 獲取熱門飲料店數據
    const fetchPopularShops = async () => {
      try {
        const response = await axios.get('/stores/query', {
          params: {
            limit: 12,
            sort_by: 'review_number',
            order: 'desc'
          }
        })
        drinks.value = response.data.stores.map(shop => ({
          id: shop.id,
          name: shop.name,
          description: shop.description || '',
          price: shop.budget || 0,
          rating: shop.rating || 0,
          views: shop.review_number || 0,
          image: shop.hero_image || shop.hero_listing_image || 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=500'
        }))
      } catch (error) {
        console.error('獲取熱門飲料店失敗:', error)
      }
    }

    // 獲取推薦飲料店數據
    const fetchRecommendedShops = async () => {
      try {
        const response = await axios.get('/stores/query', {
          params: {
            limit: 12,
            sort_by: 'rating',
            order: 'desc'
          }
        })
        recommendedDrinks.value = response.data.stores.map(shop => ({
          id: shop.id,
          name: shop.name,
          description: shop.description || '',
          price: shop.budget || 0,
          rating: shop.rating || 0,
          views: shop.review_number || 0,
          image: shop.hero_image || shop.hero_listing_image || 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=500'
        }))
      } catch (error) {
        console.error('獲取推薦飲料店失敗:', error)
      }
    }

    // 排序邏輯
    const sortedDrinks = computed(() => {
      return [...drinks.value].sort((a, b) => {
        switch (currentSort.value) {
          case 'rating':
            return b.rating - a.rating
          case 'review_number':
            return b.views - a.views
          default:
            return 0
        }
      })
    })

    const sortedRecommendedDrinks = computed(() => {
      return [...recommendedDrinks.value].sort((a, b) => {
        switch (currentRecommendSort.value) {
          case 'rating':
            return b.rating - a.rating
          case 'review_number':
            return b.views - a.views
          default:
            return 0
        }
      })
    })

    // 組件掛載時獲取數據
    onMounted(() => {
      if (isLoggedIn.value) {
        fetchPopularShops()
        fetchRecommendedShops()
      }
    })

    // 監聽登入狀態變化
    watch(isLoggedIn, (newValue) => {
      if (newValue) {
        fetchPopularShops()
        fetchRecommendedShops()
      } else {
        drinks.value = []
        recommendedDrinks.value = []
      }
    })

    return {
      isLoggedIn,
      viewMode,
      recommendViewMode,
      currentSort,
      currentRecommendSort,
      sortOptions,
      sortedDrinks,
      sortedRecommendedDrinks
    }
  }
}
</script>

<style scoped>
/* 網格布局動畫 */
.layout-grid-move {
  transition: transform 0.5s ease;
}

/* 列表布局動畫 */
.layout-list-move {
  transition: transform 0.5s ease;
}

/* 進入和離開動畫 */
.layout-grid-enter-active,
.layout-grid-leave-active,
.layout-list-enter-active,
.layout-list-leave-active {
  transition: all 0.5s ease;
}

.layout-grid-enter-from,
.layout-grid-leave-to,
.layout-list-enter-from,
.layout-list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

/* 確保動畫期間元素不會消失 */
.layout-grid-leave-active,
.layout-list-leave-active {
  position: absolute;
}
</style> 