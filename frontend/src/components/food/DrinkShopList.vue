<template>
  <transition-group 
    :name="viewMode === 'grid' ? 'layout-grid' : 'layout-list'"
    tag="div"
    :class="{
      'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8': viewMode === 'grid',
      'space-y-4': viewMode === 'list'
    }"
  >
    <div v-for="drink in drinks" :key="drink.name" 
        :class="[
          'bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden transform transition-all duration-300',
          viewMode === 'grid' ? 'hover:scale-105' : 'hover:shadow-xl'
        ]">
      <!-- 網格視圖 -->
      <template v-if="viewMode === 'grid'">
        <img 
          :src="drink.image_url" 
          :alt="drink.name" 
          class="w-full h-48 object-cover"
          @error="handleImageError"
        >
        <div class="p-4">
          <h3 class="text-xl font-semibold mb-2 text-gray-900 dark:text-white">{{ drink.name }}</h3>
          <p class="text-gray-600 dark:text-gray-400 mb-2 line-clamp-3">{{ drink.description || '暫無描述' }}</p>
          <div class="flex items-center mb-2">
            <span class="text-yellow-500 mr-1">★</span>
            <span class="text-gray-600 dark:text-gray-300">{{ drink.rating }}</span>
            <span class="ml-2 text-gray-600 dark:text-gray-400">({{ drink.review_number }}次瀏覽)</span>
          </div>
          <div class="mt-4 flex justify-between items-center">
            <span class="text-gray-600 dark:text-gray-400">{{ drink.city_CN || drink.city }}</span>
          </div>
          <div class="mt-4 flex justify-end space-x-3">
            <a 
              :href="drink.foodpanda_url" 
              target="_blank"
              class="p-2 text-gray-600 hover:text-pink-500 dark:text-gray-400 dark:hover:text-pink-400 transition-colors duration-300"
              title="前往點餐"
            >
              <i class="fas fa-utensils text-xl"></i>
            </a>
            <a 
              :href="drink.navigation_url" 
              target="_blank"
              class="p-2 text-gray-600 hover:text-indigo-500 dark:text-gray-400 dark:hover:text-indigo-400 transition-colors duration-300"
              title="查看地圖"
            >
              <i class="fas fa-map-marker-alt text-xl"></i>
            </a>
          </div>
        </div>
      </template>
      
      <!-- 列表視圖 -->
      <template v-else>
        <div class="flex items-center p-4">
          <img 
            :src="drink.image_url" 
            :alt="drink.name" 
            class="w-24 h-24 object-cover rounded"
            @error="handleImageError"
          >
          <div class="ml-4 flex-grow">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ drink.name }}</h3>
            <p class="text-gray-600 dark:text-gray-400 mb-2 line-clamp-2">{{ drink.description || '暫無描述' }}</p>
            <div class="flex items-center my-1">
              <span class="text-yellow-500 mr-1">★</span>
              <span class="text-gray-600 dark:text-gray-300">{{ drink.rating }}</span>
              <span class="ml-2 text-gray-600 dark:text-gray-400">({{ drink.review_number }}次瀏覽)</span>
            </div>
            <div class="flex items-center text-gray-600 dark:text-gray-400">
              <span>{{ drink.city_CN || drink.city }}</span>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <a 
              :href="drink.foodpanda_url" 
              target="_blank"
              class="p-2 text-gray-600 hover:text-pink-500 dark:text-gray-400 dark:hover:text-pink-400 transition-colors duration-300"
              title="前往點餐"
            >
              <i class="fas fa-utensils text-xl"></i>
            </a>
            <a 
              :href="drink.navigation_url" 
              target="_blank"
              class="p-2 text-gray-600 hover:text-indigo-500 dark:text-gray-400 dark:hover:text-indigo-400 transition-colors duration-300"
              title="查看地圖"
            >
              <i class="fas fa-map-marker-alt text-xl"></i>
            </a>
          </div>
        </div>
      </template>
    </div>
  </transition-group>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { recommendAPI } from '@/api'

export default {
  name: 'DrinkShopList',
  props: {
    viewMode: {
      type: String,
      required: true
    },
    sortBy: {
      type: String,
      required: true
    },
    userId: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    console.log('props', props)
    const drinks = ref([])
    const loading = ref(false)
    const error = ref(null)
    const defaultImage = 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=500'

    const handleImageError = (event) => {
      event.target.src = defaultImage
    }

    const fetchRecommendations = async () => {
      try {
        loading.value = true
        let response

        // 根據排序方式選擇不同的推薦 API
        switch (props.sortBy) {
          case 'rating':
            response = await recommendAPI.getContentRecommendations({
              limit: 10,
              user_id: props.userId
            })
            break
          case 'preference':
            response = await recommendAPI.getCollaborativeRecommendations({
              limit: 10,
              user_id: props.userId
            })
            break
          default:
            response = await recommendAPI.getHybridRecommendations({
              limit: 10,
              user_id: props.userId
            })
        }
        
        // 統一處理不同 API 的回傳格式
        let storesData = []
        if (response.data) {
          if (response.data.stores) {
            storesData = response.data.stores
          } else if (response.data.data) {
            storesData = response.data.data
          }
        }

        // 統一數據格式
        drinks.value = storesData.map(shop => ({
          id: shop.id || shop.store_id,
          name: shop.name || shop.store_name,
          rating: shop.rating || 0,
          review_number: shop.review_number || 0,
          city: shop.city || '',
          city_CN: shop.city_CN || '',
          description: shop.description ? 
            (shop.description.length > 100 ? 
              shop.description.substring(0, 100) + '...' : 
              shop.description) : 
            '暫無描述',
          navigation_url: shop.navigation_url || '#',
          foodpanda_url: shop.redirection_url || '#',
          image_url: shop.hero_image || shop.hero_listing_image || defaultImage
        }))

        console.log('推薦數據:', {
          sortBy: props.sortBy,
          responseData: response.data,
          processedData: drinks.value
        })
      } catch (err) {
        error.value = err.message
        console.error('獲取推薦飲料店失敗:', err)
      } finally {
        loading.value = false
      }
    }

    // 監聽排序變化和用戶 ID 變化
    watch([() => props.sortBy, () => props.userId], ([newSort, newUserId]) => {
      fetchRecommendations()
    })

    onMounted(() => {
      fetchRecommendations()
    })

    return {
      drinks,
      loading,
      error,
      handleImageError
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

/* 按鈕動畫效果 */
a {
  transition: all 0.3s ease;
}

a:hover {
  transform: translateY(-2px);
}

/* 添加工具提示效果 */
a {
  position: relative;
}

a:hover::after {
  content: attr(title);
  position: absolute;
  bottom: -25px;
  left: 50%;
  transform: translateX(-50%);
  padding: 4px 8px;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  pointer-events: none;
}

/* 確保按鈕在暗色模式下也有正確的樣式 */
.dark a:hover::after {
  background-color: rgba(255, 255, 255, 0.9);
  color: black;
}
</style> 