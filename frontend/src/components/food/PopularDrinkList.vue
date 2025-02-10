<template>
  <transition-group 
    :name="viewMode === 'grid' ? 'layout-grid' : 'layout-list'"
    tag="div"
    :class="{
      'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8': viewMode === 'grid',
      'space-y-4': viewMode === 'list'
    }"
  >
    <div v-for="drink in drinks" :key="drink.id" 
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
          <div class="flex items-center mb-2">
            <span class="text-yellow-500 mr-1">★</span>
            <span class="text-gray-600 dark:text-gray-300">{{ drink.rating }}</span>
            <span class="ml-2 text-gray-600 dark:text-gray-400">({{ drink.review_number }}次瀏覽)</span>
          </div>
          <p class="text-gray-600 dark:text-gray-400 text-sm mb-2 line-clamp-2">
            {{ truncateDescription(drink.description) }}
          </p>
          <div class="mt-2 text-gray-600 dark:text-gray-400">
            <span>{{ drink.city }}</span>
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
            <div class="flex items-center my-1">
              <span class="text-yellow-500 mr-1">★</span>
              <span class="text-gray-600 dark:text-gray-300">{{ drink.rating }}</span>
              <span class="ml-2 text-gray-600 dark:text-gray-400">({{ drink.review_number }}次瀏覽)</span>
            </div>
            <p class="text-gray-600 dark:text-gray-400 text-sm mb-1 line-clamp-2">
              {{ truncateDescription(drink.description) }}
            </p>
            <div class="text-gray-600 dark:text-gray-400">
              <span>{{ drink.city }}</span>
            </div>
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
  name: 'PopularDrinkList',
  props: {
    viewMode: {
      type: String,
      required: true
    },
    sortBy: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const drinks = ref([])
    const loading = ref(false)
    const error = ref(null)
    const defaultImage = 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=500'

    const truncateDescription = (description) => {
      if (!description) return '暫無描述'
      return description.length > 100 ? description.slice(0, 100) + '...' : description
    }

    const handleImageError = (event) => {
      event.target.src = defaultImage
    }

    const fetchPopularDrinks = async () => {
      try {
        loading.value = true
        const response = await recommendAPI.getPopularDrinks({
          limit: 12,
          sort_by: props.sortBy === 'default' ? 'review_number' : props.sortBy,
          order: 'desc'
        })
        
        if (response.data && response.data.stores) {
          drinks.value = response.data.stores.map(shop => ({
            id: shop.id,
            name: shop.name,
            rating: shop.rating || 0,
            review_number: shop.review_number || 0,
            city: shop.city || '',
            description: shop.description || '',
            image_url: shop.hero_image || shop.hero_listing_image || defaultImage
          }))
        }
      } catch (err) {
        error.value = err.message
        console.error('獲取熱門飲料店失敗:', err)
      } finally {
        loading.value = false
      }
    }

    // 監聽排序變化
    watch(() => props.sortBy, (newSort) => {
      fetchPopularDrinks()
    })

    onMounted(() => {
      fetchPopularDrinks()
    })

    return {
      drinks,
      loading,
      error,
      handleImageError,
      truncateDescription
    }
  }
}
</script>

<style scoped>
.layout-grid-move,
.layout-list-move {
  transition: transform 0.5s ease;
}

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

.layout-grid-leave-active,
.layout-list-leave-active {
  position: absolute;
}

/* 確保列表視圖的寬度正確 */
.space-y-4 > div {
  width: 100%;
}

/* 添加多行文字截斷 */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 