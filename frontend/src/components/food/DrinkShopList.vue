<template>
  <transition-group 
    :name="viewMode === 'grid' ? 'layout-grid' : 'layout-list'"
    tag="div"
    :class="{
      'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8': viewMode === 'grid',
      'space-y-4': viewMode === 'list'
    }"
  >
    <!-- 當是最愛排序且沒有資料時顯示提示 -->
    <div v-if="sortBy === 'favorite' && (!drinks || drinks.length === 0)"
         class="col-span-full flex flex-col items-center justify-center py-12 bg-white rounded-lg shadow">
      <i class="fas fa-heart text-6xl text-gray-300 mb-4"></i>
      <p class="text-xl text-gray-600 mb-2">目前尚未加入最愛</p>
      <p class="text-gray-500">趕快新增一個吧！</p>
    </div>

    <div v-else v-for="drink in drinks" :key="drink.id" 
        class="bg-white rounded-lg shadow-lg overflow-hidden cursor-pointer"
        @click="showDrinkDetail(drink)">
      <!-- 店家圖片 -->
      <div class="relative">
        <img 
          :src="drink.image_url" 
          :alt="drink.name" 
          class="w-full h-48 object-cover"
          @error="handleImageError"
        >
        <!-- 商品標籤 -->
        <div v-if="drink.tag" class="absolute top-4 left-4">
          <span class="px-3 py-1 text-sm bg-purple-500 text-white rounded-full flex items-center shadow-md">
            <i class="fas fa-tag text-xs mr-1.5"></i>
            {{ drink.tag }}
          </span>
        </div>
      </div>

      <!-- 店家資訊 -->
      <div class="p-6">
        <!-- 店家名稱 -->
        <div class="flex justify-between items-start mb-4">
          <h3 class="text-xl font-bold text-gray-900">{{ drink.name }}</h3>
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
        <div v-if="drink.tag" class="mb-3">
          <div class="flex flex-wrap gap-2">
            <span v-for="(tag, index) in drink.tag.split(',')" :key="index"
                  class="px-3 py-1 text-sm bg-purple-100 text-purple-700 rounded-full flex items-center">
              <i class="fas fa-tag text-xs mr-1.5"></i>
              {{ tag.trim() }}
            </span>
          </div>
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
        <!-- 店家圖片 -->
        <img :src="selectedDrink.image_url" 
             :alt="selectedDrink.name"
             class="w-full h-64 object-cover"
             @error="handleImageError">
        
        <!-- 關閉按鈕 -->
        <button @click="closeDetailModal"
                class="absolute top-4 right-4 bg-black bg-opacity-50 text-white rounded-full p-2 hover:bg-opacity-70">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <!-- 店家資訊 -->
      <div class="p-6">
        <!-- 頁籤選項 -->
        <div class="border-b border-gray-200 dark:border-gray-700">
          <nav class="flex space-x-4 px-4">
            <button 
              @click="activeTab = 'info'"
              :class="[
                'py-4 px-2 font-medium border-b-2 transition-colors flex items-center space-x-2',
                activeTab === 'info' 
                  ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400' 
                  : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400'
              ]"
            >
              <i class="fas fa-info-circle"></i>
              <span>基本資訊</span>
            </button>
            <button 
              @click="activeTab = 'description'"
              :class="[
                'py-4 px-2 font-medium border-b-2 transition-colors flex items-center space-x-2',
                activeTab === 'description' 
                  ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400' 
                  : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400'
              ]"
            >
              <i class="fas fa-store"></i>
              <span>店家介紹</span>
            </button>
            <button 
              @click="activeTab = 'reviews'"
              :class="[
                'py-4 px-2 font-medium border-b-2 transition-colors flex items-center space-x-2',
                activeTab === 'reviews' 
                  ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400' 
                  : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400'
              ]"
            >
              <i class="fas fa-comments"></i>
              <span>顧客評論</span>
            </button>
          </nav>
        </div>

        <!-- 頁籤內容 -->
        <div class="p-6">
          <!-- 基本資訊 -->
          <div v-if="activeTab === 'info'" class="space-y-6">
            <!-- 店家名稱和評分 -->
            <div class="mb-6">
              <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                {{ selectedDrink.name }}
              </h2>
              <div class="flex items-center">
                <span class="text-yellow-500 mr-1">★</span>
                <span class="text-gray-600 dark:text-gray-300">{{ selectedDrink.rating }}</span>
                <span class="ml-2 text-gray-600 dark:text-gray-400">
                  ({{ selectedDrink.review_number }}次瀏覽)
                </span>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 class="font-semibold text-gray-900 dark:text-white mb-2">飲料店資訊</h3>
                <div class="space-y-2 text-gray-600 dark:text-gray-400">
                  <p><i class="fas fa-map w-6"></i> 縣市：{{ selectedDrink.city_CN || selectedDrink.city }}</p>
                  <p><i class="fas fa-map-marker-alt w-6"></i> 地址：{{ selectedDrink.address }}</p>
                  <p><i class="fas fa-phone w-6"></i> 電話：{{ selectedDrink.phone }}</p>
                  <p><i class="fas fa-clock w-6"></i> 開始營業時間：{{ formatDateTime(selectedDrink.start_time) || '暫無資訊' }}</p>
                </div>
              </div>
              <div>
                <h3 class="font-semibold text-gray-900 dark:text-white mb-2">店家標誌</h3>
                <div v-if="selectedDrink.tag" class="flex flex-wrap gap-2">
                  <span class="px-3 py-1 text-sm bg-purple-500 text-white rounded-full flex items-center shadow-md">
                    <i class="fas fa-tag text-xs mr-1.5"></i>
                    {{ selectedDrink.tag }}
                  </span>
                </div>
              </div>
            </div>
            
            <!-- 操作按鈕 -->
            <div class="mt-6 flex justify-end space-x-4">
              <a :href="selectedDrink.navigation_url" 
                 target="_blank"
                 class="p-2 text-gray-600 hover:text-indigo-500 dark:text-gray-400 dark:hover:text-indigo-400 transition-colors duration-300"
                 title="查看地圖">
                <i class="fas fa-map-marker-alt text-xl"></i>
              </a>
              <a :href="selectedDrink.foodpanda_url" 
                 target="_blank"
                 class="p-2 text-gray-600 hover:text-pink-500 dark:text-gray-400 dark:hover:text-pink-400 transition-colors duration-300"
                 title="前往點餐">
                <i class="fas fa-utensils text-xl"></i>
              </a>
            </div>
          </div>

          <!-- 店家介紹 -->
          <div v-else-if="activeTab === 'description'" class="space-y-6">
            <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-6">
              <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                店家介紹
              </h3>
              <div class="text-gray-700 dark:text-gray-300 whitespace-pre-line">
                {{ formatDescription(selectedDrink.description) }}
              </div>
            </div>
          </div>

          <!-- 顧客評論 -->
          <div v-else-if="activeTab === 'reviews'" class="space-y-6">
            <!-- 評論統計 -->
            <div class="flex items-center justify-between mb-6">
              <div class="flex items-center space-x-4">
                <div class="text-3xl font-bold text-gray-900 dark:text-white">
                  {{ selectedDrink.rating }}
                </div>
                <div class="flex items-center text-yellow-400 cursor-pointer">
                  <i v-for="n in 5" :key="n"
                     @click="setRating(n)"
                     @mouseover="hoverRating = n"
                     @mouseleave="hoverRating = 0"
                     :class="[
                       'fas',
                       'fa-star',
                       (hoverRating || selectedDrink.rating) >= n ? 'text-yellow-400' : 'text-gray-200'
                     ]">
                  </i>
                </div>
                <div class="text-gray-500">
                  {{ getReviewCount }} 次瀏覽
                </div>
              </div>
              <button 
                @click="showReviewForm = true"
                class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
              >
                撰寫評論
              </button>
            </div>

            <!-- 評論列表 -->
            <div class="max-h-[400px] overflow-y-auto pr-2">
              <div v-if="getReviewCount > 0" 
                   class="space-y-4">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="text-lg font-medium text-gray-900">最新評論</h3>
                  <span class="text-sm text-gray-500">
                    (顯示最新 3 則評論)
                  </span>
                </div>
                <div v-for="review in displayedReviews" 
                     :key="review.id" 
                     class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
                  <div class="flex items-start">
                    <img :src="review.user_avatar || defaultAvatar" 
                         :alt="review.username"
                         class="w-10 h-10 rounded-full">
                    <div class="ml-4 flex-1">
                      <div class="flex items-center justify-between">
                        <h4 class="font-medium text-gray-900 dark:text-white">
                          {{ review.username }}
                        </h4>
                        <span class="text-sm text-gray-500">
                          {{ formatDate(review.created_at) }}
                        </span>
                      </div>
                      <div class="flex items-center mt-1">
                        <div class="flex items-center text-yellow-400">
                          <span v-for="i in 5" :key="i">
                            <i :class="[
                              'fas',
                              i <= review.rating ? 'fa-star' : 'fa-star-o'
                            ]"></i>
                          </span>
                        </div>
                      </div>
                      <p class="mt-2 text-gray-600 dark:text-gray-400">
                        {{ review.content }}
                      </p>
                    </div>
                  </div>
                </div>
                <div v-if="getReviewCount > 3" 
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
import { ref, onMounted, watch, computed } from 'vue'
import { recommendAPI } from '@/api'
import favoriteAPI from '@/api/modules/favorite'
import Swal from 'sweetalert2'
import { messageAPI } from '@/api'

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
    },
    drinks: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    console.log('props', props)
    const drinks = ref([])
    const loading = ref(false)
    const error = ref(null)
    const defaultImage = 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=500'
    const selectedDrink = ref(null)
    const activeTab = ref('info')
    const isSubmitting = ref(false)
    const showReviewForm = ref(false)
    const newReview = ref({
      rating: 0,
      content: ''
    })
    const favoriteStates = ref({})
    const defaultAvatar = 'https://api.dicebear.com/7.x/avataaars/svg?seed=default'
    const rating = ref(0)
    const hoverRating = ref(0)
    const comment = ref('')

    const handleImageError = (event) => {
      event.target.src = defaultImage
    }

    const showDrinkDetail = (drink) => {
      console.log('選擇的店家:', drink)
      if (!drink.id) {
        console.error('店家ID不存在:', drink)
        Swal.fire({
          icon: 'error',
          title: '系統錯誤',
          text: '無法取得店家資訊'
        })
        return
      }
      selectedDrink.value = drink
      const storeId = Number(drink.id)
      console.log('準備檢查最愛狀態，店家ID:', storeId)
      checkFavoriteStatus(storeId)
    }

    const checkFavoriteStatus = async (storeId) => {
      try {
        const response = await favoriteAPI.checkFavorite(storeId)
        if (response.data.favorites && response.data.favorites.length > 0) {
          favoriteStates.value[storeId] = true
        } else {
          favoriteStates.value[storeId] = false
        }
      } catch (error) {
        console.error('檢查收藏狀態失敗:', error)
        favoriteStates.value[storeId] = false
      }
    }

    const toggleFavorite = async (drink) => {
      try {
        const isFavorited = favoriteStates.value[drink.id]
        // 從 localStorage 獲取用戶資訊
        const userInfo = JSON.parse(localStorage.getItem('user'))
        if (!userInfo || !userInfo.username) {
          throw new Error('請先登入')
        }
        
        if (isFavorited) {
          const response = await favoriteAPI.checkFavorite(drink.id)
          if (response.data.favorites && response.data.favorites.length > 0) {
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
          const response = await favoriteAPI.addFavorite({
            store_id: drink.id,
            store_name: drink.name,
            store_image: drink.store_image || defaultImage,
            username: userInfo.username  // 使用 localStorage 中的用戶名
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
        let errorMessage = '請稍後再試'
        if (error.message === '請先登入') {
          errorMessage = '請先登入後再收藏'
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message
        }
        Swal.fire({
          icon: 'error',
          title: '操作失敗',
          text: errorMessage
        })
      }
    }

    const setRating = (value) => {
      rating.value = value
    }

    const handleSubmitComment = async () => {
      if (!props.userId) {
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
          rating: rating.value
        }
        
        const response = await messageAPI.createMessage(commentData)
        
        // 關閉評論表單
        showReviewForm.value = false
        
        // 更新評論列表
        if (!selectedDrink.value.reviews) {
          selectedDrink.value.reviews = []
        }
        
        // 添加新評論到列表開頭
        selectedDrink.value.reviews.unshift({
          id: response.data.id,
          content: comment.value.trim(),
          rating: rating.value,
          created_at: new Date().toISOString(),
          username: JSON.parse(localStorage.getItem('user')).username,
          user_avatar: `${import.meta.env.VITE_BACKEND_URL}/api/users/avatar/${JSON.parse(localStorage.getItem('user')).avatar.split('/').pop()}`
        })
        
        // 清空表單
        rating.value = 0
        comment.value = ''
        
        // 切換到評論頁籤
        activeTab.value = 'reviews'
        
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

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('zh-TW', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const formatDateTime = (dateTime) => {
      if (!dateTime) return '暫無資訊'
      const date = new Date(dateTime)
      if (isNaN(date.getTime())) return '暫無資訊'
      
      return date.toLocaleString('zh-TW', {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
      })
    }

    const formatDescription = (description) => {
      if (!description) return '暫無店家介紹'
      
      // 處理換行符
      return description
        .replace(/\\n/g, '\n')  // 處理 JSON 字符串中的換行符
        .replace(/\n\n+/g, '\n\n')  // 將多個連續換行減少為最多兩個
        .trim()  // 移除首尾空白
    }

    const truncateDescription = (description) => {
      if (!description) return '暫無店家介紹'
      
      // 處理換行符
      const truncatedDescription = description
        .replace(/\\n/g, '\n')  // 處理 JSON 字符串中的換行符
        .replace(/\n\n+/g, '\n\n')  // 將多個連續換行減少為最多兩個
        .trim()  // 移除首尾空白
      
      // 限制描述長度
      const maxLength = 100
      if (truncatedDescription.length > maxLength) {
        return truncatedDescription.slice(0, maxLength) + '...'
      }
      return truncatedDescription
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
          case 'favorite':
            response = await favoriteAPI.getFavorites()
            console.log('收藏列表資料:', response.data)
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
          if (props.sortBy === 'favorite') {
            console.log('收藏列表資料:', response.data)
            // 處理收藏列表的資料格式
            storesData = response.data.favorites.map(favorite => ({
              store_id: favorite.store_id,
              name: favorite.store_name,
              store_image: favorite.store_image,
              // 其他必要欄位設置預設值
              rating: favorite.rating,
              review_number: favorite.review_number,
              city: favorite.city,
              city_CN: favorite.city_CN,
              description: favorite.description,
              navigation_url: favorite.navigation_url,
              redirection_url: favorite.redirection_url
            }))
          } else if (response.data.stores) {
            storesData = response.data.stores
          } else if (response.data.data) {
            storesData = response.data.data
          }
        }

        // 統一數據格式
        drinks.value = storesData.map(shop => ({
          id: shop.store_id || shop.id,
          name: shop.name || shop.store_name,
          rating: shop.rating || 0,
          review_number: shop.review_number || 0,
          city: shop.city || '',
          city_CN: shop.city_CN || '',
          navigation_url: shop.navigation_url || '#',
          foodpanda_url: shop.redirection_url || '#',
          image_url: shop.hero_image || shop.hero_listing_image || shop.store_image,
          address: shop.address || '暫無地址資訊',
          phone: shop.customer_phone || '暫無電話資訊',
          start_time: shop.is_new_until || '暫無營業時間資訊',
          description: shop.description || '暫無店家介紹',
          tag: shop.tag || '',
        }))

        // 如果是最愛排序，設置所有店家的收藏狀態為 true
        if (props.sortBy === 'favorite') {
          drinks.value.forEach(drink => {
            favoriteStates.value[drink.id] = true
          })
        }

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

    const closeReviewForm = () => {
      showReviewForm.value = false
      rating.value = 0
      comment.value = ''
    }

    const closeDetailModal = () => {
      selectedDrink.value = null
      activeTab.value = 'info'
      showReviewForm.value = false
      rating.value = 0
      comment.value = ''
    }

    const displayedReviews = computed(() => {
      if (!selectedDrink.value?.reviews) return []
      // 只顯示狀態為 approved 的評論，並取前3筆
      const approvedReviews = selectedDrink.value.reviews
        .filter(review => review.status === 'approved')
        .slice(0, 3)
      return approvedReviews
    })

    // 修改評論列表顯示邏輯
    const getReviewCount = computed(() => {
      if (!selectedDrink.value?.reviews) return 0
      return selectedDrink.value.reviews.filter(review => review.status === 'approved').length
    })

    return {
      drinks,
      loading,
      error,
      handleImageError,
      selectedDrink,
      showDrinkDetail,
      activeTab,
      newReview,
      isSubmitting,
      favoriteStates,
      toggleFavorite,
      defaultAvatar,
      formatDate,
      formatDateTime,
      showReviewForm,
      closeReviewForm,
      closeDetailModal,
      formatDescription,
      truncateDescription,
      rating,
      hoverRating,
      comment,
      setRating,
      handleSubmitComment,
      displayedReviews,
      getReviewCount
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

/* 添加彈窗動畫 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* 添加懸停效果 */
.cursor-pointer:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
</style> 