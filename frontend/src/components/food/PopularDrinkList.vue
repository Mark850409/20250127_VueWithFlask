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
        ]"
        @click="showDrinkDetail(drink)"
        class="cursor-pointer">
      <!-- 網格視圖 -->
      <template v-if="viewMode === 'grid'">
        <div class="relative">
          <img 
            :src="drink.image_url" 
            :alt="drink.name" 
            class="w-full h-48 object-cover"
            @error="handleImageError"
          >
        </div>
        <div class="p-6">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xl font-bold text-gray-900 dark:text-white">{{ drink.name }}</h3>
            <button @click.stop="toggleFavorite(drink)" 
                    class="text-2xl focus:outline-none transition-colors duration-300">
              <i class="fas fa-heart" 
                :class="{ 'text-red-500': favoriteStates[drink.id], 'text-gray-400': !favoriteStates[drink.id] }">
              </i>
            </button>
          </div>
          
          <!-- 評分和縣市在同一行 -->
          <div class="flex justify-between items-center mb-4">
            <div class="flex items-center text-gray-600">
              <i class="fas fa-map-marker-alt mr-2"></i>
              <span>{{ drink.city_CN }}</span>
            </div>
            <div class="flex items-center">
              <span class="text-yellow-400 mr-1"><i class="fas fa-star"></i></span>
              <span class="font-bold">{{ drink.rating }}</span>
              <span class="text-gray-500 ml-1">({{ drink.review_number }}次瀏覽)</span>
            </div>
          </div>

          <p class="text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
            {{ truncateDescription(drink.description) }}
          </p>

          <!-- 添加分隔線 -->
          <div class="h-px bg-gray-200 dark:bg-gray-700 mb-4"></div>

          <div class="flex justify-end space-x-4">
            <a 
              :href="drink.foodpanda_url" 
              target="_blank"
              @click.stop
              class="p-2 text-gray-600 hover:text-pink-500 dark:text-gray-400 dark:hover:text-pink-400 transition-colors duration-300"
              title="前往點餐"
            >
              <i class="fas fa-utensils text-xl"></i>
            </a>
            <a 
              :href="drink.navigation_url" 
              target="_blank"
              @click.stop
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
          <div class="relative">
            <img 
              :src="drink.image_url" 
              :alt="drink.name" 
              class="w-24 h-24 object-cover rounded"
              @error="handleImageError"
            >
            <button @click.stop="toggleFavorite(drink)" 
                    class="absolute top-2 right-2 p-1 rounded-full bg-white/80 hover:bg-white text-gray-700">
              <i class="fas fa-heart text-sm" 
                :class="{ 'text-red-500': favoriteStates[drink.id], 'text-gray-300': !favoriteStates[drink.id] }">
              </i>
            </button>
          </div>
          <div class="ml-4 flex-grow">
            <div class="flex justify-between items-start mb-2">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ drink.name }}</h3>
            </div>
            
            <!-- 評分和縣市在同一行 -->
            <div class="flex justify-between items-center mb-2">
              <div class="flex items-center text-gray-600">
                <i class="fas fa-map-marker-alt mr-2"></i>
                <span>{{ drink.city_CN}}</span>
              </div>
              <div class="flex items-center">
                <span class="text-yellow-400 mr-1"><i class="fas fa-star"></i></span>
                <span class="font-bold">{{ drink.rating }}</span>
                <span class="text-gray-500 ml-1">({{ drink.review_number }}次瀏覽)</span>
              </div>
            </div>

            <p class="text-gray-600 dark:text-gray-400 mb-2 line-clamp-2">
              {{ truncateDescription(drink.description) }}
            </p>

            <!-- 添加分隔線 -->
            <div class="h-px bg-gray-200 dark:bg-gray-700 my-2"></div>
          </div>
          <div class="flex items-center space-x-3">
            <a 
              :href="drink.foodpanda_url" 
              target="_blank"
              @click.stop
              class="p-2 text-gray-600 hover:text-pink-500 dark:text-gray-400 dark:hover:text-pink-400 transition-colors duration-300"
              title="前往點餐"
            >
              <i class="fas fa-utensils text-xl"></i>
            </a>
            <a 
              :href="drink.navigation_url" 
              target="_blank"
              @click.stop
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

  <!-- 飲料店詳細資訊彈窗 -->
  <div v-if="selectedDrink" 
       class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
       @click.self="closeDetailModal">
    <div class="bg-white dark:bg-gray-800 rounded-lg w-full max-w-4xl mx-4 overflow-hidden">
      <div class="relative">
        <img :src="selectedDrink.image_url" 
             :alt="selectedDrink.name"
             class="w-full h-64 object-cover"
             @error="handleImageError">
        <button @click="closeDetailModal"
                class="absolute top-4 right-4 bg-black bg-opacity-50 text-white rounded-full p-2 hover:bg-opacity-70">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <!-- 頁籤選項 -->
      <div class="border-b border-gray-200 dark:border-gray-700">
        <nav class="flex space-x-8 px-6">
          <button 
            @click="activeTab = 'info'"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm',
              activeTab === 'info' 
                ? 'border-indigo-500 text-indigo-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            基本資訊
          </button>
          <button 
            @click="activeTab = 'description'"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm',
              activeTab === 'description' 
                ? 'border-indigo-500 text-indigo-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            店家介紹
          </button>
          <button 
            @click="activeTab = 'reviews'"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm',
              activeTab === 'reviews' 
                ? 'border-indigo-500 text-indigo-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            顧客評論
          </button>
        </nav>
      </div>

      <!-- 頁籤內容 -->
      <div v-if="activeTab === 'info'" class="p-6">
        <div class="mb-6">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            {{ selectedDrink.name }}
          </h2>
          <div class="flex items-center mb-4">
            <span class="text-yellow-400 mr-1">★</span>
            <span class="font-bold">{{ selectedDrink.rating }}</span>
            <span class="text-gray-500 ml-1">({{ selectedDrink.review_number }}次瀏覽)</span>
          </div>
        </div>

        <h3 class="text-lg font-semibold mb-4">飲料店資訊</h3>
        <div class="space-y-4 text-gray-600 dark:text-gray-400">
          <div class="flex items-center">
            <i class="fas fa-map-marker-alt w-6"></i>
            <span class="ml-2">縣市：{{ selectedDrink.city_CN }}</span>
          </div>
          <div class="flex items-center">
            <i class="fas fa-location-arrow w-6"></i>
            <span class="ml-2">地址：{{ selectedDrink.address || '暫無資訊' }}</span>
          </div>
          <div class="flex items-center">
            <i class="fas fa-phone w-6"></i>
            <span class="ml-2">電話：{{ selectedDrink.phone || '暫無資訊' }}</span>
          </div>
          <div class="flex items-center">
            <i class="fas fa-utensils w-6"></i>
            <span class="ml-2">食品業者登錄字號：{{ selectedDrink.license_number || '暫無資訊' }}</span>
          </div>
        </div>

        <div class="flex justify-end mt-6 space-x-4">
          <button class="p-2 text-gray-600 hover:text-pink-500 transition-colors duration-300">
            <i class="fas fa-utensils text-xl"></i>
          </button>
          <button class="p-2 text-gray-600 hover:text-blue-500 transition-colors duration-300">
            <i class="fas fa-map-marker-alt text-xl"></i>
          </button>
        </div>
      </div>

      <div v-if="activeTab === 'description'" class="p-6">
        <h3 class="text-lg font-semibold mb-4">店家介紹</h3>
        <div class="text-gray-600 dark:text-gray-400">
          <p class="whitespace-pre-line leading-relaxed">
            {{ selectedDrink.description || '暫無介紹' }}
          </p>
        </div>
      </div>

      <div v-if="activeTab === 'reviews'" class="p-6">
        <div class="flex justify-between items-center mb-6">
          <div class="flex items-center">
            <span class="text-3xl font-bold mr-3">{{ selectedDrink.rating }}</span>
            <div class="flex flex-col">
              <div class="flex text-yellow-400">
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star-half-alt"></i>
              </div>
              <span class="text-sm text-gray-500">{{ selectedDrink.review_number }}次瀏覽</span>
            </div>
          </div>
          <!-- 撰寫評論按鈕 -->
          <button 
            @click="showReviewModal"
            class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition duration-300"
          >
            撰寫評論
          </button>
        </div>

        <!-- 暫無評價時的顯示 -->
        <div class="text-center py-12 bg-gray-50 rounded-lg">
          <p class="text-xl font-bold text-gray-400 mb-2">5</p>
          <div class="flex justify-center text-yellow-400 mb-2">
            <i class="fas fa-star"></i>
          </div>
          <p class="text-gray-400 mb-4">411 次瀏覽</p>
          <p class="text-gray-500">暫無評論，成為第一個評論的人吧！</p>
        </div>
      </div>
    </div>
  </div>

  <!-- 添加評論彈窗 -->
  <div v-if="showingReviewModal" 
       class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
       @click.self="closeReviewModal">
    <div class="bg-white dark:bg-gray-800 rounded-lg w-full max-w-lg mx-4 p-6">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-xl font-bold">撰寫評論</h3>
        <button @click="closeReviewModal" class="text-gray-500 hover:text-gray-700">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="mb-4">
        <label class="block text-gray-700 mb-2">評分</label>
        <div class="flex text-yellow-400 text-2xl">
          <button 
            v-for="star in 5" 
            :key="star"
            @click="setRating(star)"
            class="focus:outline-none"
          >
            <i :class="[
              'fas',
              userRating >= star ? 'fa-star' : 'fa-star text-gray-300'
            ]"></i>
          </button>
        </div>
      </div>

      <div class="mb-4">
        <label class="block text-gray-700 mb-2">評論內容</label>
        <textarea 
          v-model="reviewContent"
          rows="4"
          class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          placeholder="分享您的用餐體驗..."
        ></textarea>
      </div>

      <div class="flex justify-end">
        <button 
          @click="submitReview"
          class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition duration-300"
        >
          發布評論
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { recommendAPI } from '@/api'
import favoriteAPI from '@/api/modules/favorite'
import Swal from 'sweetalert2'

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
    const selectedDrink = ref(null)
    const favoriteStates = ref({})
    const activeTab = ref('info')
    const showingReviewModal = ref(false)
    const userRating = ref(0)
    const reviewContent = ref('')

    const truncateDescription = (description) => {
      if (!description) return '暫無描述'
      return description.length > 100 ? description.slice(0, 100) + '...' : description
    }

    const handleImageError = (event) => {
      event.target.src = defaultImage
    }

    const showDrinkDetail = (drink) => {
      selectedDrink.value = drink
      checkFavoriteStatus(drink.id)
    }

    const closeDetailModal = () => {
      selectedDrink.value = null
    }

    const checkFavoriteStatus = async (storeId) => {
      try {
        const response = await favoriteAPI.checkFavorite(storeId)
        favoriteStates.value[storeId] = response.data.favorites?.length > 0
      } catch (error) {
        console.error('檢查收藏狀態失敗:', error)
        favoriteStates.value[storeId] = false
      }
    }

    const toggleFavorite = async (drink) => {
      try {
        const userInfo = JSON.parse(localStorage.getItem('user'))
        if (!userInfo || !userInfo.username) {
          throw new Error('請先登入')
        }

        const isFavorited = favoriteStates.value[drink.id]
        if (isFavorited) {
          const response = await favoriteAPI.checkFavorite(drink.id)
          if (response.data.favorites?.length > 0) {
            await favoriteAPI.deleteFavorite(response.data.favorites[0].id)
            favoriteStates.value[drink.id] = false
          }
          Swal.fire({
            icon: 'success',
            title: '已取消收藏',
            showConfirmButton: false,
            timer: 1500
          })
        } else {
          await favoriteAPI.addFavorite({
            store_id: drink.id,
            store_name: drink.name,
            store_image: drink.image_url || '',
            username: userInfo.username
          })
          favoriteStates.value[drink.id] = true
          Swal.fire({
            icon: 'success',
            title: '已加入收藏',
            showConfirmButton: false,
            timer: 1500
          })
        }
      } catch (error) {
        console.error('切換收藏狀態失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '操作失敗',
          text: error.message === '請先登入' ? '請先登入後再收藏' : '請稍後再試'
        })
      }
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
            city_CN: shop.city_CN || '',
            description: shop.description || '',
            image_url: shop.hero_image || shop.hero_listing_image || defaultImage,
            address: shop.address,
            phone: shop.phone,
            foodpanda_url: shop.redirection_url || '#',
            navigation_url: shop.navigation_url || '#'
          }))

          // 檢查每個店家的收藏狀態
          drinks.value.forEach(drink => {
            checkFavoriteStatus(drink.id)
          })
        }
      } catch (err) {
        error.value = err.message
        console.error('獲取熱門飲料店失敗:', err)
      } finally {
        loading.value = false
      }
    }

    const showReviewModal = () => {
      showingReviewModal.value = true
    }

    const closeReviewModal = () => {
      showingReviewModal.value = false
    }

    const setRating = (rating) => {
      userRating.value = rating
    }

    const submitReview = () => {
      // 實現提交評論的邏輯
      console.log('評論提交:', {
        rating: userRating.value,
        content: reviewContent.value
      })
      closeReviewModal()
    }

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
      truncateDescription,
      selectedDrink,
      showDrinkDetail,
      closeDetailModal,
      favoriteStates,
      toggleFavorite,
      activeTab,
      showingReviewModal,
      showReviewModal,
      closeReviewModal,
      setRating,
      submitReview
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

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 添加新的互動效果 */
.cursor-pointer:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* 工具提示效果 */
a {
  position: relative;
  transition: all 0.3s ease;
}

a:hover {
  transform: translateY(-2px);
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

.dark a:hover::after {
  background-color: rgba(255, 255, 255, 0.9);
  color: black;
}
</style> 