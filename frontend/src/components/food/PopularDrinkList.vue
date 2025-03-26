<template>
  <transition-group 
    :name="viewMode === 'grid' ? 'layout-grid' : 'layout-list'"
    tag="div"
    :class="{
      'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-20': viewMode === 'grid',
      'space-y-4 pb-20': viewMode === 'list'
    }"
  >
    <div v-if="loading" key="loading" class="col-span-full flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
    </div>
    <template v-else>
      <div v-for="drink in sortedDrinks" :key="drink.id" 
          class="bg-white rounded-lg shadow-lg overflow-hidden cursor-pointer hover:shadow-xl transform transition-all duration-300"
          :data-drink-id="drink.id"
          @click="showDrinkDetail(drink)">
        <!-- 店家圖片 -->
        <div class="relative">
          <img 
            :src="drink.image_url" 
            :alt="drink.name" 
            class="w-full h-52 object-cover transition-opacity duration-300"
            :class="{ 'opacity-0': !imageLoaded[drink.id] }"
            loading="lazy"
            @load="handleImageLoad(drink.id)"
            @error="handleImageError"
          >
          <div v-if="!imageLoaded[drink.id]" class="absolute inset-0 bg-gray-200 animate-pulse"></div>
          
          <!-- 促銷標籤 -->
          <div v-if="drink.promotion" class="absolute top-4 left-4">
            <span class="px-3 py-1 text-sm bg-purple-600 bg-opacity-70 text-white rounded-full inline-flex items-center shadow-md">
              <i class="fas fa-tag text-xs mr-1.5"></i>
              {{ drink.promotion }}
            </span>
          </div>

          <!-- 距離標籤 -->
          <div v-if="drink.distance" class="absolute bottom-4 right-4">
            <span class="px-3 py-1 text-sm bg-black bg-opacity-60 text-white rounded-full inline-flex items-center shadow-md">
              <i class="fas fa-location-arrow text-xs mr-1.5"></i>
              {{ formatDistance(drink.distance) }}
            </span>
          </div>
        </div>

        <!-- 店家資訊 -->
        <div class="p-4">
          <!-- 店家名稱 -->
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-lg font-bold text-gray-900">{{ drink.name }}</h3>
            <button @click.stop="toggleFavorite(drink)" 
                    class="text-2xl focus:outline-none transition-colors duration-300">
              <i class="fas fa-heart" 
                :class="{ 'text-red-500': favoriteStates[drink.id], 'text-gray-400': !favoriteStates[drink.id] }">
              </i>
            </button>
          </div>

          <!-- 縣市 -->
          <div class="flex items-center text-gray-600 mb-4">
            <i class="fas fa-map-marker-alt mr-2"></i>
            <span>{{ drink.city_CN }}</span>
          </div>

          <!-- 評分和瀏覽次數區域 -->
          <div class="flex items-center justify-between mb-3">
            <!-- 評分區塊 -->
            <div class="flex items-center">
              <div class="text-sm text-gray-600 mr-2">評分</div>
              <div class="flex items-center">
                <span class="text-purple-600 text-lg font-semibold mr-1">{{ drink.rating }}</span>
                <i class="fas fa-star text-purple-600"></i>
              </div>
            </div>
            
            <!-- 瀏覽次數區塊 -->
            <div class="flex items-center">
              <div class="text-sm text-gray-600 mr-2">瀏覽次數</div>
              <div class="flex items-center">
                <span class="text-purple-600 text-lg font-semibold">{{ drink.review_number }}</span>
                <i class="fas fa-eye text-purple-600 ml-1"></i>
              </div>
            </div>
          </div>

          <!-- 促銷資訊 -->
          <div v-if="drink.promotion" class="mb-3">
            <span class="px-3 py-1 text-sm bg-purple-100 text-purple-600 rounded-full inline-flex items-center">
              <i class="fas fa-tag text-xs mr-1.5"></i>
              {{ drink.promotion }}
            </span>
          </div>

          <!-- 分隔線 -->
          <div class="h-px bg-gray-200 dark:bg-gray-700 mb-3"></div>

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
            <button 
              @click.stop="handleMapClick(drink)"
              class="p-2 text-gray-600 hover:text-indigo-500 transition-colors duration-300"
              title="查看地圖"
            >
              <i class="fas fa-map-marker-alt text-xl"></i>
            </button>
          </div>
        </div>
      </div>
    </template>
  </transition-group>

  <!-- 飲料店詳細資訊彈窗 -->
  <div v-if="selectedDrink" 
       class="fixed inset-0 bg-black bg-opacity-50 flex justify-center z-50 overflow-y-auto pt-20 px-4 pb-4"
       @click.self="closeDetailModal">
    <div class="bg-white dark:bg-gray-800 rounded-lg w-full max-w-4xl relative" 
         style="min-height: 200px; max-height: calc(100vh - 120px);">
      <!-- 關閉按鈕固定在右上角 -->
      <button @click="closeDetailModal"
              class="absolute -top-4 -right-4 bg-white text-gray-600 rounded-full p-2 hover:bg-gray-100 shadow-lg z-[60] transition-colors duration-200">
        <i class="fas fa-times text-xl"></i>
      </button>

      <!-- 內容區塊添加捲動功能 -->
      <div class="h-full overflow-y-auto">
        <!-- 店家圖片容器固定高度 -->
        <div class="relative h-48 bg-gray-100">
          <img :src="selectedDrink.image_url" 
               :alt="selectedDrink.name"
               class="w-full h-full object-cover"
               loading="lazy"
               @error="handleImageError">
        </div>

        <!-- 店家資訊 -->
        <div class="p-6">
          <!-- 頁籤選項固定在頂部 -->
          <div class="border-b border-gray-200 dark:border-gray-700 sticky top-0 bg-white z-10">
            <nav class="flex">
              <button 
                @click="activeTab = 'info'"
                :class="[
                  'py-4 px-6 border-b-2 font-medium text-sm flex items-center',
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
                  'py-4 px-6 border-b-2 font-medium text-sm flex items-center',
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
                  'py-4 px-6 border-b-2 font-medium text-sm flex items-center',
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

          <!-- 頁籤內容區域 -->
          <div class="space-y-6 mt-6">
            <!-- 基本資訊 -->
            <div v-if="activeTab === 'info'" class="space-y-6">
              <!-- 店家名稱和評分區塊 -->
              <div class="mb-8">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                  {{ selectedDrink.name }}
                </h2>
                
                <!-- 評分和瀏覽次數卡片 -->
                <div class="grid grid-cols-2 gap-6">
                  <!-- 評分卡片 -->
                  <div class="bg-white dark:bg-gray-700 rounded-lg p-4 shadow-sm border border-gray-100">
                    <div class="flex items-center justify-between mb-2">
                      <span class="text-gray-600 dark:text-gray-300">整體評分</span>
                      <div class="flex items-center">
                        <span class="text-yellow-400 mr-2">
                          <i class="fas fa-star text-xl"></i>
                        </span>
                        <span class="text-2xl font-bold text-gray-900 dark:text-white">
                          {{ selectedDrink.rating }}
                        </span>
                      </div>
                    </div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">
                      綜合評價
                    </div>
                  </div>

                  <!-- 瀏覽次數卡片 -->
                  <div class="bg-white dark:bg-gray-700 rounded-lg p-4 shadow-sm border border-gray-100">
                    <div class="flex items-center justify-between mb-2">
                      <span class="text-gray-600 dark:text-gray-300">瀏覽次數</span>
                      <div class="flex items-center">
                        <span class="text-purple-400 mr-2">
                          <i class="fas fa-eye text-xl"></i>
                        </span>
                        <span class="text-2xl font-bold text-gray-900 dark:text-white">
                          {{ selectedDrink.review_number }}
                        </span>
                      </div>
                    </div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">
                      總瀏覽人次
                    </div>
                  </div>
                </div>
              </div>

              <!-- 飲料店資訊區塊 -->
              <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-6">飲料店資訊</h3>
                <div class="grid gap-6">
                  <!-- 店家標籤 -->
                  <div v-if="selectedDrink.tag" class="flex items-start">
                    <div class="w-24 flex-shrink-0">
                      <i class="fas fa-tags text-indigo-500 mr-2"></i>
                      <span class="text-gray-600">標籤</span>
                    </div>
                    <div class="flex-1 flex flex-wrap gap-2">
                      <span v-for="(tag, index) in selectedDrink.tag.split(',')" :key="index"
                            class="px-3 py-1 text-sm bg-purple-100 text-purple-700 rounded-full flex items-center">
                        <i class="fas fa-tag text-xs mr-1.5"></i>
                        {{ tag.trim() }}
                      </span>
                    </div>
                  </div>

                  <!-- 距離和預估時間 -->
                  <div v-if="selectedDrink.distance" class="flex items-start">
                    <div class="w-24 flex-shrink-0">
                      <i class="fas fa-route text-indigo-500 mr-2"></i>
                      <span class="text-gray-600">距離</span>
                    </div>
                    <div class="flex-1 flex items-center space-x-8">
                      <span>{{ formatDistance(selectedDrink.distance) }}</span>
                      <div class="flex items-center">
                        <i class="fas fa-clock text-indigo-500 mr-2"></i>
                        <span>預估時間：{{ formatDuration(selectedDrink.duration) }}</span>
                      </div>
                    </div>
                  </div>

                  <!-- 其他資訊 -->
                  <div class="flex items-start">
                    <div class="w-24 flex-shrink-0">
                      <i class="fas fa-map-marker-alt text-indigo-500 mr-2"></i>
                      <span class="text-gray-600">縣市</span>
                    </div>
                    <div class="flex-1">{{ selectedDrink.city_CN }}</div>
                  </div>

                  <div class="flex items-start">
                    <div class="w-24 flex-shrink-0">
                      <i class="fas fa-location-arrow text-indigo-500 mr-2"></i>
                      <span class="text-gray-600">地址</span>
                    </div>
                    <div class="flex-1">{{ selectedDrink.address || '暫無資訊' }}</div>
                  </div>

                  <div class="flex items-start">
                    <div class="w-24 flex-shrink-0">
                      <i class="fas fa-phone text-indigo-500 mr-2"></i>
                      <span class="text-gray-600">電話</span>
                    </div>
                    <div class="flex-1">{{ selectedDrink.customer_phone || '暫無資訊' }}</div>
                  </div>
                </div>
              </div>

              <!-- 分隔線和按鈕 -->
              <div class="pt-4">
                <div class="h-px bg-gray-200 dark:bg-gray-700 mb-4"></div>
                <div class="flex justify-end space-x-4">
                  <a :href="selectedDrink.foodpanda_url" 
                     target="_blank"
                     class="p-2 text-gray-600 hover:text-pink-500 transition-colors duration-300"
                     title="前往點餐">
                    <i class="fas fa-utensils text-xl"></i>
                  </a>
                  <button 
                    @click="handleMapClick(selectedDrink)"
                    class="p-2 text-gray-600 hover:text-blue-500 transition-colors duration-300"
                    title="查看地圖">
                    <i class="fas fa-map-marker-alt text-xl"></i>
                  </button>
                </div>
              </div>
            </div>

            <!-- 店家介紹 -->
            <div v-else-if="activeTab === 'description'" class="space-y-6">
              <div class="bg-white rounded-lg shadow-md border border-gray-200 p-6">
                <!-- 標題區塊 -->
                <div class="flex items-center space-x-3 mb-6">
                  <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                    <i class="fas fa-store text-purple-600"></i>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-gray-900">店家介紹</h3>
                    <p class="text-sm text-gray-500">查看詳細資訊</p>
                  </div>
                </div>

                <!-- 證號資訊區塊 -->
                <div class="bg-gray-50 rounded-lg p-4 mb-6 border border-gray-100 shadow-sm">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="flex items-center">
                      <div class="w-10 h-10 bg-purple-50 rounded-lg flex items-center justify-center">
                        <i class="fas fa-certificate text-purple-500"></i>
                      </div>
                      <div class="ml-3">
                        <div class="text-xs text-gray-500">食品業者登錄字號</div>
                        <div class="text-sm text-gray-700 font-medium">
                          {{ selectedDrink.registration_number || 'A-128408922-00086-7' }}
                        </div>
                      </div>
                    </div>
                    <div class="flex items-center">
                      <div class="w-10 h-10 bg-purple-50 rounded-lg flex items-center justify-center">
                        <i class="fas fa-shield-alt text-purple-500"></i>
                      </div>
                      <div class="ml-3">
                        <div class="text-xs text-gray-500">產品責任險字號</div>
                        <div class="text-sm text-gray-700 font-medium">
                          {{ selectedDrink.insurance_number || '02 第1412PDL00134' }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 店家描述區塊 -->
                <div class="bg-purple-50 rounded-lg p-5 mb-6 border border-purple-100 shadow-sm">
                  <div class="relative">
                    <!-- 左上角引號裝飾 -->
                    <div class="absolute -top-2 -left-2 text-purple-200 text-4xl">"</div>
                    <!-- 右下角引號裝飾 -->
                    <div class="absolute -bottom-2 -right-2 text-purple-200 text-4xl">"</div>
                    <!-- 描述文字 -->
                    <div class="text-gray-700 leading-relaxed whitespace-pre-line px-4 py-2">
                      {{ selectedDrink.description || '暫無店家介紹' }}
                    </div>
                  </div>
                </div>

                <!-- 環保政策提示 -->
                <div class="border-t border-gray-100 pt-6">
                  <div class="flex items-start bg-green-50 rounded-lg p-4 border border-green-100 shadow-sm">
                    <div class="flex-shrink-0">
                      <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                        <i class="fas fa-leaf text-green-500"></i>
                      </div>
                    </div>
                    <div class="ml-4">
                      <h4 class="text-sm font-medium text-green-800">環保政策說明</h4>
                      <p class="mt-1 text-sm text-green-600">
                        本店每筆訂單的收餐點包裝費2元。因應環保署政策，店家不得免費提供購物用環保袋，為確保送餐品質，餐點皆由塑膠袋包裝。
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 顧客評論 -->
            <div v-else-if="activeTab === 'reviews'" class="space-y-6">
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
                        class="px-4 py-2 bg-indigo-100 text-indigo-600 rounded-lg hover:bg-indigo-200 transition-all duration-300 ease-in-out transform hover:scale-105 flex items-center">
                  <i class="fas fa-pencil-alt mr-2"></i>
                  撰寫評論
                </button>
              </div>

              <!-- 評論列表 -->
              <div class="max-h-[400px] overflow-y-auto pr-2">
                <div v-if="processedReviews.length > 0" 
                      class="space-y-4">
                  <div class="flex justify-between items-center mb-4">
                    <h3 class="text-lg font-medium text-gray-900">最新評論</h3>
                    <span class="text-sm text-gray-500">
                      (顯示最新 3 則評論)
                    </span>
                  </div>
                  <!-- 評論內容 -->
                  <div v-for="review in processedReviews" 
                       :key="review.id" 
                       class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
                    <div class="flex items-start">
                      <img :src="review.user_avatar" 
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
                <div v-else class="flex flex-col items-center justify-center py-12 bg-gray-50 dark:bg-gray-800 rounded-lg">
                  <i class="fas fa-comments text-5xl text-gray-300 dark:text-gray-600 mb-4"></i>
                  <p class="text-lg font-medium text-gray-600 dark:text-gray-300 mb-2">
                    暫無評論
                  </p>
                  <p class="text-sm text-gray-500 dark:text-gray-400">
                    成為第一個評論的人吧！
                  </p>
                  <button 
                    @click="showReviewForm = true"
                    class="mt-6 px-6 py-2 bg-indigo-100 text-indigo-600 rounded-full hover:bg-indigo-200 transition-all duration-300 ease-in-out transform hover:scale-105 flex items-center"
                  >
                    <i class="fas fa-pencil-alt mr-2"></i>
                    撰寫評論
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 評論表單彈窗 -->
  <div v-if="showReviewForm" 
       class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[70]"
       @click.self="closeReviewForm">
    <div class="bg-white dark:bg-gray-800 rounded-lg w-full max-w-md mx-4 relative">
      <!-- 關閉按鈕 -->
      <button @click="closeReviewForm" 
              class="absolute -top-2 -right-2 bg-white text-gray-600 rounded-full p-1.5 hover:bg-gray-100 shadow-md z-50 transition-colors duration-200">
        <i class="fas fa-times text-sm"></i>
      </button>

      <!-- 表單內容 -->
      <div class="p-4">
        <!-- 標題 -->
        <h3 class="text-base font-medium text-gray-900 dark:text-white mb-4">
          撰寫評論
        </h3>

        <!-- 評分區域 -->
        <div class="mb-4">
          <div class="flex items-center">
            <span class="text-sm text-gray-600 mr-3">評分：</span>
            <div class="flex text-2xl text-gray-300">
              <button v-for="n in 5"
                      :key="n"
                      @click="setRating(n)"
                      @mouseover="hoverRating = n"
                      @mouseleave="hoverRating = 0"
                      class="focus:outline-none">
                <i class="fas fa-star" 
                 :class="{
                   'text-yellow-400': hoverRating >= n || (!hoverRating && rating >= n),
                   'text-gray-300': (hoverRating && hoverRating < n) || (!hoverRating && rating < n)
                 }">
                </i>
              </button>
            </div>
            <span class="ml-2 text-sm text-gray-600">{{ rating || 0 }} 分</span>
          </div>
        </div>

        <!-- 評論文字區域 -->
        <div class="mb-4">
          <span class="text-sm text-gray-600 block mb-2">評論內容</span>
          <textarea 
            v-model="comment"
            placeholder="請寫下您的評論..."
            class="w-full p-3 text-sm border border-gray-200 rounded-lg focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white resize-none"
            rows="4"
          ></textarea>
        </div>

        <!-- 按鈕區域 -->
        <div class="flex space-x-2">
          <button 
            @click="closeReviewForm"
            class="flex-1 py-2 text-sm bg-gray-50 text-gray-600 rounded-lg hover:bg-gray-100 transition-all duration-300 ease-in-out transform hover:scale-105">
            取消
          </button>
          <button 
            @click="handleSubmitComment"
            class="flex-1 py-2 text-sm bg-indigo-100 text-indigo-600 rounded-lg hover:bg-indigo-200 transition-all duration-300 ease-in-out transform hover:scale-105">
            發布評論
          </button>
        </div>
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
import accountAPI from '@/api/modules/account'

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
    const favoriteCache = ref({})
    const favoritesCacheExpiry = 5 * 60 * 1000
    const lastFavoriteCheck = ref(0)
    const isFirstLoad = ref(true)
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
    const imageLoaded = ref({})
    const modalImageLoaded = ref(false)
    const processedReviews = ref([])
    let cityChangeHandler = null

    const getStoredCity = () => {
      return localStorage.getItem('selectedCity') || '台北市'
    }

    const truncateDescription = (description) => {
      if (!description) return '暫無描述'
      return description
    }

    const handleImageLoad = (id) => {
      imageLoaded.value[id] = true
    }

    const handleImageError = (event) => {
      const drinkId = event.target.closest('[data-drink-id]')?.dataset.drinkId
      if (drinkId) {
        imageLoaded.value[drinkId] = true
      }
      event.target.src = defaultImage
    }

    const handleAvatarError = (event) => {
      event.target.src = defaultAvatar.value
    }

    const handleModalImageLoad = () => {
      modalImageLoaded.value = true
    }

    const showDrinkDetail = async (drink) => {
      try {
        selectedDrink.value = drink
        activeTab.value = 'info'
        modalImageLoaded.value = false

        // 獲取評論數據
        const response = await messageAPI.getMessages()
        if (response.data && response.data.messages) {
          // 將評論數據添加到 selectedDrink 中
          selectedDrink.value = {
            ...drink,
            reviews: response.data.messages
          }
        }
      } catch (error) {
        console.error('獲取評論數據失敗:', error)
        selectedDrink.value = drink
      }
    }

    const closeDetailModal = () => {
      selectedDrink.value = null
      modalImageLoaded.value = false
    }

    const checkFavoriteStatus = async (stores) => {
      try {
        const currentTime = Date.now()
        if (currentTime - lastFavoriteCheck.value < favoritesCacheExpiry && 
            Object.keys(favoriteCache.value).length > 0) {
          favoriteStates.value = { ...favoriteCache.value }
          return
        }

        const userInfo = JSON.parse(localStorage.getItem('user'))
        if (!userInfo || !userInfo.username) {
          stores.forEach(store => {
            favoriteStates.value[store.id] = false
          })
          return
        }

        // 一次性獲取所有收藏狀態
        const response = await favoriteAPI.getFavorites(userInfo.username)
        const favorites = response.data.favorites || []
        
        // 建立收藏店家 ID 的集合，方便快速查找
        const favoriteStoreIds = new Set(favorites.map(fav => fav.store_id))
        
        // 更新所有店家的收藏狀態
        stores.forEach(store => {
          favoriteStates.value[store.id] = favoriteStoreIds.has(store.id)
        })

        // 更新快取
        favoriteCache.value = { ...favoriteStates.value }
        lastFavoriteCheck.value = currentTime
      } catch (error) {
        console.error('檢查收藏狀態失敗:', error)
        stores.forEach(store => {
          favoriteStates.value[store.id] = false
        })
      }
    }

    const toggleFavorite = async (drink) => {
      try {
        const userInfo = JSON.parse(localStorage.getItem('user'))
        if (!userInfo || !userInfo.username) {
          throw new Error('請先登入')
        }

        const isFavorited = favoriteStates.value[drink.id]
        console.log('切換收藏狀態:', {
          store_id: drink.id,
          store_name: drink.name,
          current_state: isFavorited
        })
        
        if (isFavorited) {
          // 如果已收藏，直接獲取所有收藏並找到要刪除的項目
          const response = await favoriteAPI.getFavorites(userInfo.username)
          const favoriteItem = response.data.favorites?.find(f => f.store_id === drink.id)
          
          if (favoriteItem) {
            await favoriteAPI.deleteFavorite(favoriteItem.id)
            favoriteStates.value[drink.id] = false
            favoriteCache.value[drink.id] = false
            
            Swal.fire({
              icon: 'success',
              title: '已取消收藏',
              showConfirmButton: false,
              timer: 1500
            })
          }
        } else {
          // 如果未收藏，直接添加
          const favoriteData = {
            store_id: drink.id,
            store_name: drink.name,
            store_image: drink.image_url || '',
            username: userInfo.username
          }
          
          console.log('準備添加收藏:', favoriteData)
          
          try {
            const addResponse = await favoriteAPI.addFavorite(favoriteData)
            console.log('添加收藏響應:', addResponse)
            
            if (addResponse.data) {
              favoriteStates.value[drink.id] = true
              favoriteCache.value[drink.id] = true
              
              Swal.fire({
                icon: 'success',
                title: '已加入收藏',
                showConfirmButton: false,
                timer: 1500
              })
            }
          } catch (addError) {
            console.error('添加收藏詳細錯誤:', {
              message: addError.message,
              response: addError.response?.data,
              status: addError.response?.status
            })
            throw addError
          }
        }
      } catch (error) {
        console.error('切換收藏狀態失敗:', {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status
        })
        
        // 恢復原始狀態
        favoriteStates.value[drink.id] = !favoriteStates.value[drink.id]
        
        Swal.fire({
          icon: 'error',
          title: '操作失敗',
          text: error.response?.data?.message || error.message || '請稍後再試',
          confirmButtonText: '確定'
        })
      }
    }

    // 新增一個方法來處理地圖點擊
    const handleMapClick = async (store) => {
      try {
        // 如果已經有有效的導航 URL，直接使用
        if (store.navigation_url && store.navigation_url !== '#') {
          window.open(store.navigation_url, '_blank')
          return
        }

        // 否則獲取新的導航 URL
        const navigationResponse = await recommendAPI.getNavigation({
          origin: '東吳大學(城中校區)',
          destination: store.name,
          mode: 'driving'
        })

        if (navigationResponse.data && navigationResponse.data.navigation_url) {
          store.navigation_url = navigationResponse.data.navigation_url
          window.open(store.navigation_url, '_blank')
        } else {
          console.warn(`無法獲取 ${store.name} 的導航連結`)
          Swal.fire({
            icon: 'error',
            title: '無法獲取導航連結',
            text: '請稍後再試'
          })
        }
      } catch (error) {
        console.error(`獲取導航連結失敗 (${store.name}):`, error)
        Swal.fire({
          icon: 'error',
          title: '獲取導航連結失敗',
          text: '請稍後再試'
        })
      }
    }

    const sortedDrinks = computed(() => {
      if (!drinks.value.length) return []
      
      const drinksList = [...drinks.value]
      
      switch (props.sortBy) {
        case 'distance':
          return drinksList.sort((a, b) => {
            if (a.distance === Infinity) return 1
            if (b.distance === Infinity) return -1
            return a.distance - b.distance
          })
        case 'rating':
          return drinksList.sort((a, b) => {
            if (b.rating === a.rating) {
              return b.review_number - a.review_number
            }
            return b.rating - a.rating
          })
        case 'review_number':
          return drinksList.sort((a, b) => b.review_number - a.review_number)
        default:
          return drinksList
      }
    })

    const fetchPopularDrinks = async () => {
      loading.value = true
      drinks.value = []
      imageLoaded.value = {}
      
      try {
        await new Promise(resolve => setTimeout(resolve, 300))
        const params = {
          sort_by: props.sortBy,
          limit: 12
        }
        
        params.city = selectedCity.value || getStoredCity()
        
        const response = await recommendAPI.getPopularDrinks(params)
        console.log('Popular drinks response:', response.data)
        
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
            navigation_url: '#',
            distance: null,
            duration: null
          }))

          // 修改距離計算的觸發條件
          const needToCalculateDistance = props.sortBy === 'distance' && (
            !distanceCalculated.value || 
            currentCity.value !== params.city ||
            storesWithDistance.value.length === 0
          )
          
          console.log('需要計算距離:', needToCalculateDistance)
          console.log('當前排序方式:', props.sortBy)
          console.log('當前城市:', currentCity.value)
          console.log('選擇的城市:', params.city)

          if (needToCalculateDistance) {
            console.log('開始計算距離...')
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
            currentCity.value = params.city
            storesWithDistance.value = [...mappedStores]
          } else if (props.sortBy === 'distance' && storesWithDistance.value.length > 0) {
            console.log('使用已計算的距離數據')
            mappedStores = [...storesWithDistance.value]
          }
          
          // 根據排序方式進行排序
          if (props.sortBy === 'distance') {
            mappedStores.sort((a, b) => {
              if (a.distance === Infinity) return 1
              if (b.distance === Infinity) return -1
              return a.distance - b.distance  // 修改為升序排序，距離近的排前面
            })
          } else if (props.sortBy === 'rating') {
            mappedStores.sort((a, b) => b.rating - a.rating)
          } else if (props.sortBy === 'review_number') {
            mappedStores.sort((a, b) => b.review_number - a.review_number)
          }
          
          drinks.value = mappedStores

          // 只在首次載入時檢查收藏狀態
          if (isFirstLoad.value) {
            await checkFavoriteStatus(mappedStores)
            isFirstLoad.value = false
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

    // 監聽 selectedDrink 的變化
    watch(() => selectedDrink.value?.reviews, async (newReviews) => {
      try {
        if (!newReviews || !Array.isArray(newReviews)) {
          processedReviews.value = []
          return
        }

        // 過濾並處理評論
        const filteredReviews = newReviews
          .filter(review => review.status === 'approved' && review.store_id === selectedDrink.value.id)
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
          .slice(0, 3)

        // 處理每條評論的用戶頭像
        const reviews = await Promise.all(
          filteredReviews.map(async review => {
            let avatarUrl = defaultAvatar.value

            if (review.user_id) {
              try {
                const userResponse = await accountAPI.getUserById(review.user_id)
                if (userResponse.data && userResponse.data.avatar) {
                  const avatar = userResponse.data.avatar
                  if (avatar.startsWith('http')) {
                    avatarUrl = avatar
                  } else {
                    avatarUrl = `${import.meta.env.VITE_BACKEND_URL}/uploads/avatars/${avatar}`
                  }
                }
              } catch (error) {
                console.error('獲取用戶頭像失敗:', error)
              }
            }

            return {
              id: review.id,
              content: review.content,
              rating: review.rating || 0,
              created_at: review.created_at,
              user: review.user || '匿名用戶',
              user_avatar: avatarUrl
            }
          })
        )

        processedReviews.value = reviews
      } catch (error) {
        console.error('處理評論時出錯:', error)
        processedReviews.value = []
      }
    }, { immediate: true })

    watch(() => props.sortBy, (newValue) => {
      console.log('排序方式改變:', newValue)
      if (newValue === 'distance') {
        // 強制重新計算距離
        distanceCalculated.value = false
        storesWithDistance.value = []
      }
      fetchPopularDrinks()
    }, { immediate: true })

    onMounted(() => {
      cityChangeHandler = (event) => {
        selectedCity.value = event.detail
        localStorage.setItem('selectedCity', event.detail)
        // 城市改變時也需要重新計算距離
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
      handleImageLoad,
      imageLoaded,
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
      processedReviews,
      defaultAvatar,
      handleAvatarError,
      handleMapClick,
      modalImageLoaded,
      handleModalImageLoad,
      sortedDrinks
    }
  }
}
</script>

<style scoped>
.layout-grid-move,
.layout-list-move {
  transition: all 0.5s ease;
}

.layout-grid-enter-active,
.layout-grid-leave-active,
.layout-list-enter-active,
.layout-list-leave-active {
  transition: all 0.5s ease-out;
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
  width: 100%;
}

/* 添加新的過渡效果 */
.fade-move,
.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s cubic-bezier(0.55, 0, 0.1, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: scaleY(0.01) translate(30px, 0);
}

.fade-leave-active {
  position: absolute;
}

/* 優化卡片hover效果 */
.cursor-pointer {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: transform, box-shadow;
}

.cursor-pointer:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
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