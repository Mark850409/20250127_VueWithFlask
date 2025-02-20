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
        class="bg-white rounded-lg shadow-lg overflow-hidden cursor-pointer hover:shadow-xl"
        @click="showDrinkDetail(drink)">
      <!-- 店家圖片 -->
      <div class="relative">
        <img 
          :src="drink.image_url" 
          :alt="drink.name" 
          class="w-full h-52 object-cover"
          @error="handleImageError"
        >
        <!-- 促銷標籤 -->
        <div v-if="drink.promotion" class="absolute top-4 left-4">
          <span class="px-3 py-1 text-sm bg-purple-500 text-white rounded-full inline-flex items-center shadow-md">
            {{ drink.promotion }}
          </span>
        </div>
      </div>

      <!-- 店家資訊 -->
        <div class="p-4">
        <!-- 店家名稱 -->
        <div class="flex justify-between items-start mb-4">
          <h3 class="text-lg font-bold text-gray-900">{{ drink.name }}</h3>
          <button @click.stop="toggleFavorite(drink)" 
                  class="text-2xl focus:outline-none transition-colors duration-300">
            <i class="fas fa-heart" 
              :class="{ 'text-red-500': favoriteStates[drink.id], 'text-gray-400': !favoriteStates[drink.id] }">
            </i>
          </button>
        </div>

        <!-- 縣市和評分資訊 -->
        <div class="flex justify-between items-center mb-3">
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

        <!-- 店家標籤 -->
        <div v-if="drink.tag" class="mb-3 flex">
          <span class="px-3 py-1 text-sm bg-purple-400 bg-opacity-20 text-purple-600 rounded-full inline-flex items-center">
            {{ drink.tag }}
          </span>
        </div>

        <!-- 店家描述 -->
        <p class="text-gray-600 mb-4 line-clamp-2">
            {{ truncateDescription(drink.description) }}
        </p>

        <!-- 分隔線 -->
        <div class="h-px bg-gray-200 dark:bg-gray-700 mb-4"></div>

        <!-- 功能按鈕 -->
        <div class="flex justify-end space-x-4">
          <a 
            :href="drink.foodpanda_url" 
            target="_blank"
            @click.stop
            class="p-2 text-gray-600 hover:text-pink-500 transition-colors duration-300"
            title="前往點餐"
          >
            <i class="fas fa-utensils text-xl"></i>
          </a>
          <a 
            :href="drink.navigation_url" 
            target="_blank"
            @click.stop
            class="p-2 text-gray-600 hover:text-indigo-500 transition-colors duration-300"
            title="查看地圖"
          >
            <i class="fas fa-map-marker-alt text-xl"></i>
          </a>
        </div>
      </div>
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
              'py-4 px-1 border-b-2 font-medium text-sm flex items-center',
              activeTab === 'info' 
                ? 'border-indigo-500 text-indigo-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            <i class="fas fa-info-circle mr-2"></i>
            基本資訊
          </button>
          <button 
            @click="activeTab = 'description'"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm flex items-center',
              activeTab === 'description' 
                ? 'border-indigo-500 text-indigo-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            <i class="fas fa-store mr-2"></i>
            店家介紹
          </button>
          <button 
            @click="activeTab = 'reviews'"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm flex items-center',
              activeTab === 'reviews' 
                ? 'border-indigo-500 text-indigo-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            <i class="fas fa-comments mr-2"></i>
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
          <!-- 店家標籤 -->
          <div v-if="selectedDrink.tag" class="flex items-center">
            <i class="fas fa-tags w-6"></i>
            <div class="ml-2 flex flex-wrap gap-2">
              <span v-for="(tag, index) in selectedDrink.tag.split(',')" :key="index"
                    class="px-3 py-1 text-sm bg-purple-100 text-purple-700 rounded-full flex items-center">
                <i class="fas fa-tag text-xs mr-1.5"></i>
                {{ tag.trim() }}
              </span>
            </div>
          </div>
          <!-- 距離和預估時間 -->
          <div v-if="selectedDrink.distance" class="flex items-center space-x-6">
            <div class="flex items-center">
              <i class="fas fa-route w-6 text-indigo-500"></i>
              <span class="ml-2">距離：{{ formatDistance(selectedDrink.distance) }}</span>
            </div>
            <div class="flex items-center">
              <i class="fas fa-clock w-6 text-indigo-500"></i>
              <span class="ml-2">預估時間：{{ formatDuration(selectedDrink.duration) }}</span>
            </div>
          </div>
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
            <span class="ml-2">電話：{{ selectedDrink.customer_phone || '暫無資訊' }}</span>
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
      
      <!-- 顧客評論 -->
      <div v-if="activeTab === 'reviews'" class="p-6">
        <!-- 評論統計 -->
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center space-x-4">
            <div class="text-center">
              <div class="text-3xl font-bold text-gray-900">{{ selectedDrink.rating }}</div>
              <div class="flex text-yellow-400 mt-1">
                <i v-for="n in 5" :key="n" 
                   :class="['fas', n <= selectedDrink.rating ? 'fa-star' : 'fa-star-o']">
                </i>
              </div>
              <div class="text-sm text-gray-500 mt-1">{{ selectedDrink.review_number }}次瀏覽</div>
            </div>
          </div>
          <button @click="showReviewForm = true" 
                  class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition duration-300">
            撰寫評論
          </button>
        </div>

        <!-- 評論列表 -->
        <div class="max-h-[400px] overflow-y-auto pr-2">
          <div v-if="displayedReviews.length > 0" 
                class="space-y-4">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg font-medium text-gray-900">最新評論</h3>
              <span class="text-sm text-gray-500">
                (顯示最新 3 則評論)
              </span>
            </div>
            <!-- 評論內容 -->
            <div v-for="review in displayedReviews" 
                 :key="review.id" 
                 class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
              <div class="flex items-start">
                <img :src="review.user_avatar || defaultAvatar" 
                     :alt="review.user"
                     class="w-10 h-10 rounded-full"
                     @error="handleAvatarError">
                <div class="ml-4 flex-1">
                  <div class="flex items-center justify-between">
                    <h4 class="font-medium text-gray-900">{{ review.user }}</h4>
                    <span class="text-sm text-gray-500">{{ formatDate(review.created_at) }}</span>
                  </div>
                  <div class="flex text-yellow-400 my-1">
                    <i v-for="n in 5" :key="n" 
                       :class="['fas', n <= review.rating ? 'fa-star' : 'fa-star-o']">
                    </i>
                  </div>
                  <p class="text-gray-600 mt-1">{{ review.content }}</p>
                </div>
              </div>
            </div>
            <div v-if="selectedDrink.reviews.length > 3" 
                 class="text-center text-gray-500 mt-4">
              僅顯示最新 3 則評論
            </div>
          </div>
          <div v-else class="text-center text-gray-500 py-8">
            暫無評論，成為第一個評論的人吧！
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 評論表單彈窗 -->
  <div v-if="showReviewForm" 
       class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
       @click.self="closeReviewForm">
    <div class="bg-white dark:bg-gray-800 rounded-lg w-full max-w-lg mx-4 p-6">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          撰寫評論
        </h3>
        <button @click="closeReviewForm" class="text-gray-500 hover:text-gray-700">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="rating mb-4">
        <div class="flex items-center mb-2">
          <span class="mr-2">評分：</span>
          <div class="flex text-2xl text-yellow-400">
            <button v-for="n in 5"
                    :key="n"
                    @click="setRating(n)"
                    @mouseover="hoverRating = n"
                    @mouseleave="hoverRating = 0"
                    class="focus:outline-none mr-1">
              <i class="fas fa-star" 
               :class="{
                 'text-yellow-400': hoverRating >= n || (!hoverRating && rating >= n),
                 'text-gray-300': (hoverRating && hoverRating < n) || (!hoverRating && rating < n)
               }">
              </i>
            </button>
          </div>
          <span class="ml-2 text-sm text-gray-600">{{ rating }} 分</span>
        </div>
        
        <div class="mb-4">
          <textarea v-model="comment"
                    placeholder="請寫下您的評論..."
                    class="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
                    rows="4">
          </textarea>
        </div>
        
        <button @click="handleSubmitComment"
                 class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
          發布評論
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, onUnmounted, computed } from 'vue'
import { recommendAPI } from '@/api'
import favoriteAPI from '@/api/modules/favorite'
import Swal from 'sweetalert2'
import messageAPI from '@/api/modules/message'

export default {
  name: 'PopularDrinkList',
  props: {
    viewMode: {
      type: String,
      default: 'grid'
    },
    sortBy: {
      type: String,
      default: 'default',
      validator: function(value) {
        return ['default', 'rating', 'review_number', 'distance'].includes(value)
      }
    },
    userId: {
      type: String,
      default: null
    }
  },
  setup(props) {
    const drinks = ref([])
    const loading = ref(true)
    const error = ref(null)
    const distanceCalculated = ref(false)
    const currentCity = ref('')
    const storesWithDistance = ref([])
    const defaultImage = 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=500'
    const selectedDrink = ref(null)
    const favoriteStates = ref({})
    const activeTab = ref('info')
    const showingReviewModal = ref(false)
    const userRating = ref(0)
    const reviewContent = ref('')
    const selectedCity = ref('')
    const showReviewForm = ref(false)
    const comment = ref('')
    const rating = ref(null)
    const hoverRating = ref(0)
    const defaultAvatar = ref('https://api.dicebear.com/7.x/avataaars/svg?seed=default')
    let cityChangeHandler = null

    const getStoredCity = () => {
      return localStorage.getItem('selectedCity') || '台北市'
    }

    const truncateDescription = (description) => {
      if (!description) return '暫無描述'
      return description.length > 100 ? description.slice(0, 100) + '...' : description
    }

    const handleImageError = (event) => {
      event.target.src = defaultImage
    }

    const handleAvatarError = (event) => {
      event.target.src = defaultAvatar.value
    }

    const showDrinkDetail = async (drink) => {
      try {
        // 獲取店家評論資訊
        const response = await messageAPI.getMessages()
        if (response.data && response.data.messages) {
          // 過濾出當前店家的評論
          const storeReviews = response.data.messages.filter(
            message => message.store_id === drink.id
          )
          
          selectedDrink.value = {
            ...drink,
            reviews: storeReviews
          }
          
          console.log('Selected drink with reviews:', selectedDrink.value)
        } else {
          selectedDrink.value = drink
        }
      } catch (error) {
        console.error('獲取店家評論失敗:', error)
        selectedDrink.value = drink
      }
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
      loading.value = true
      try {
        const params = {
          sort_by: props.sortBy,
          limit: 12
        }
        
        params.city = selectedCity.value || getStoredCity()
        
        const response = await recommendAPI.getPopularDrinks(params)
        
        if (response.data && response.data.stores) {
          let mappedStores = response.data.stores.map(shop => ({
            id: shop.id,
            name: shop.name,
            rating: shop.rating || 0,
            review_number: shop.review_number || 0,
            city: shop.city || '',
            city_CN: shop.city_CN || '',
            description: shop.description || '',
            image_url: shop.hero_image || shop.hero_listing_image || defaultImage,
            address: shop.address,
            customer_phone: shop.customer_phone,
            tag: Array.isArray(shop.tag) ? shop.tag.join(', ') : (shop.tag || ''),
            promotion: shop.promotion || shop.tag || '',
            foodpanda_url: shop.redirection_url || '#',
            navigation_url: shop.navigation_url || '#',
            distance: null
          }))

          const needToCalculateDistance = 
            !distanceCalculated.value || 
            currentCity.value !== (selectedCity.value || getStoredCity()) ||
            storesWithDistance.value.length === 0;

          if (props.sortBy === 'distance' && needToCalculateDistance) {
            const distancePromises = mappedStores.map(async (store) => {
              try {
                const response = await recommendAPI.calculateDistance({
                  origin: '東吳大學(城中校區)',
                  destination: store.address
                })
                if (response.data && 
                    response.data.rows && 
                    response.data.rows[0] && 
                    response.data.rows[0].elements && 
                    response.data.rows[0].elements[0] &&
                    response.data.rows[0].elements[0].status === 'OK') {
                  const element = response.data.rows[0].elements[0]
                  store.distance = element.distance.value
                  store.duration = element.duration.value
                } else {
                  console.warn(`無法計算到 ${store.name} 的距離`)
                  store.distance = Infinity
                  store.duration = null
                }
                return store
              } catch (error) {
                console.error(`計算距離失敗 (${store.name}):`, error)
                store.distance = Infinity
                store.duration = null
                return store
              }
            })
            
            mappedStores = await Promise.all(distancePromises)
            distanceCalculated.value = true
            currentCity.value = selectedCity.value || getStoredCity()
            storesWithDistance.value = [...mappedStores]
          } else if (props.sortBy === 'distance') {
            mappedStores = storesWithDistance.value
          }
          
          if (props.sortBy === 'distance') {
            mappedStores.sort((a, b) => {
              if (a.distance === Infinity) return 1
              if (b.distance === Infinity) return -1
              return b.distance - a.distance
            })
          }
          
          drinks.value = mappedStores

          if (!Object.keys(favoriteStates.value).length) {
            const checkPromises = drinks.value.map(drink => checkFavoriteStatus(drink.id))
            await Promise.all(checkPromises)
          }
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

    const setRating = (value) => {
      if (value === rating.value) {
        rating.value = null
      } else {
        rating.value = value
      }
    }

    const submitReview = () => {
      console.log('評論提交:', {
        rating: userRating.value,
        content: reviewContent.value
      })
      closeReviewModal()
    }

    const formatDistance = (distance) => {
      if (!distance) return '未知距離'
      const km = distance / 1000
      return km >= 1 
        ? `${km.toFixed(1)} 公里`
        : `${Math.round(distance)} 公尺`
    }

    const formatDuration = (duration) => {
      if (!duration) return '未知時間'
      const minutes = Math.round(duration / 60)
      if (minutes >= 60) {
        const hours = Math.floor(minutes / 60)
        const remainingMinutes = minutes % 60
        return `${hours} 小時 ${remainingMinutes} 分鐘`
      }
      return `${minutes} 分鐘`    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('zh-TW', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const handleSubmitComment = async () => {
      const userInfo = JSON.parse(localStorage.getItem('user'))
      if (!userInfo || !userInfo.id) {
        Swal.fire({
          icon: 'warning',
          title: '請先登入',
          text: '發布評論前請先登入系統',
          confirmButtonText: '確定'
        })
        return
      }
      
      if (!rating.value) {
        Swal.fire({
          icon: 'warning',
          title: '請選擇評分',
          text: '評分為必填項目',
          confirmButtonText: '確定'
        })
        return
      }
      
      if (!comment.value.trim()) {
        Swal.fire({
          icon: 'warning',
          title: '請填寫評論內容',
          text: '評論內容不能為空',
          confirmButtonText: '確定'
        })
        return
      }
      
      try {
        const commentData = {
          content: comment.value.trim(),
          store_id: selectedDrink.value.id,
          rating: rating.value,
          user_id: userInfo.id
        }
        
        await messageAPI.createMessage(commentData)
        showReviewForm.value = false
        rating.value = null
        comment.value = ''
        
        Swal.fire({
          icon: 'success',
          title: '評論發布成功',
          text: '您的評論已送出審核',
          confirmButtonText: '確定'
        })
      } catch (error) {
        console.error('發布評論失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '發布失敗',
          text: error.response?.data?.message || '請稍後再試',
          confirmButtonText: '確定'
        })
      }
    }

    const closeReviewForm = () => {
      showReviewForm.value = false
      rating.value = null
      comment.value = ''
      hoverRating.value = 0
    }

    const displayedReviews = computed(() => {
      // 檢查 selectedDrink 是否存在且有 reviews 屬性
      if (!selectedDrink.value?.reviews) {
        console.log('No reviews available for selected drink')
        return []
      }
      
      // 確保 reviews 是陣列
      const reviews = Array.isArray(selectedDrink.value.reviews) 
        ? selectedDrink.value.reviews 
        : []
      
      // 過濾並排序評論
      const approvedReviews = reviews
        .filter(review => review.status === 'approved')
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .slice(0, 3)
      
      console.log('Approved reviews:', approvedReviews)
      return approvedReviews
    })

    const getReviewCount = computed(() => {
      // 檢查 selectedDrink 是否存在且有 reviews 屬性
      if (!selectedDrink.value?.reviews) {
        console.log('No reviews available for review count')
        return 0
      }
      
      // 確保 reviews 是陣列
      const reviews = Array.isArray(selectedDrink.value.reviews) 
        ? selectedDrink.value.reviews 
        : []
      
      // 計算審核通過的評論數量
      const count = reviews.filter(review => review.status === 'approved').length
      console.log('Approved review count:', count)
      return count
    })

    watch(() => props.sortBy, () => {
      if (props.sortBy === 'distance') {
        if (storesWithDistance.value.length > 0) {
          drinks.value = [...storesWithDistance.value].sort((a, b) => {
            if (a.distance === Infinity) return 1
            if (b.distance === Infinity) return -1
            return b.distance - a.distance
          })
        }
      } else {
        const params = {
          sort_by: props.sortBy,
          limit: 12,
          city: selectedCity.value || getStoredCity()
        }
        drinks.value = drinks.value.sort((a, b) => {
          if (props.sortBy === 'rating') {
            return b.rating - a.rating
          } else if (props.sortBy === 'review_number') {
            return b.review_number - a.review_number
          }
          return 0
        })
      }
    }, { immediate: true })

    onMounted(() => {
      cityChangeHandler = (event) => {
        selectedCity.value = event.detail
        localStorage.setItem('selectedCity', event.detail)
        distanceCalculated.value = false
        storesWithDistance.value = []
      fetchPopularDrinks()
      }
      
      window.addEventListener('cityChanged', cityChangeHandler)
      selectedCity.value = getStoredCity()
    })

    onMounted(fetchPopularDrinks)

    onUnmounted(() => {
      if (cityChangeHandler) {
        window.removeEventListener('cityChanged', cityChangeHandler)
      }
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
      submitReview,
      selectedCity,
      formatDistance,
      formatDuration,
      distanceCalculated,
      currentCity,
      storesWithDistance,
      showReviewForm,
      comment,
      rating,
      hoverRating,
      formatDate,
      handleSubmitComment,
      closeReviewForm,
      displayedReviews,
      getReviewCount,
      defaultAvatar,
      handleAvatarError
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

.cursor-pointer:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

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

</style> 