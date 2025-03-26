<template>
  <transition-group 
    :name="viewMode === 'grid' ? 'layout-grid' : 'layout-list'"
    tag="div"
    :class="{
      'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8': viewMode === 'grid',
      'space-y-4': viewMode === 'list'
    }"
  >
    <!-- 載入中動畫 -->
    <div v-if="loading" key="loading" class="col-span-full flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
    </div>

    <!-- 當是最愛排序且沒有資料時顯示提示 -->
    <div v-else-if="sortBy === 'favorite' && (!drinks || drinks.length === 0)"
         class="col-span-full flex flex-col items-center justify-center py-12 bg-white rounded-lg shadow">
      <i class="fas fa-heart text-6xl text-gray-300 mb-4"></i>
      <p class="text-xl text-gray-600 mb-2">目前尚未加入最愛</p>
      <p class="text-gray-500">趕快新增一個吧！</p>
    </div>

    <div v-else v-for="drink in drinks" :key="drink.id" 
        class="bg-white rounded-lg shadow-lg overflow-hidden cursor-pointer hover:shadow-xl transform transition-all duration-300"
        :data-drink-id="drink.id"
        @click="showDrinkDetail(drink)">
      <!-- 店家圖片 -->
      <div class="relative">
        <img 
          :src="drink.image_url" 
          :alt="drink.name" 
          class="w-full h-48 object-cover transition-opacity duration-300"
          :class="{ 'opacity-0': !imageLoaded[drink.id] }"
          loading="lazy"
          @load="handleImageLoad(drink.id)"
          @error="handleImageError"
        >
        <div v-if="!imageLoaded[drink.id]" class="absolute inset-0 bg-gray-200 animate-pulse"></div>
        <!-- 商品標籤 -->
        <div v-if="drink.tag" class="absolute top-4 left-4">
          <span class="px-3 py-1 text-sm bg-purple-600 bg-opacity-70 text-white rounded-full flex items-center shadow-md">
            <i class="fas fa-tag text-xs mr-1.5"></i>
            {{ drink.tag }}
          </span>
        </div>
      </div>

      <!-- 店家資訊 -->
      <div class="p-6">
        <!-- 店家名稱和收藏按鈕 -->
        <div class="flex justify-between items-start mb-4">
          <h3 class="text-xl font-bold text-gray-900">{{ drink.name }}</h3>
          <button @click.stop="toggleFavorite(drink)" 
                  class="text-2xl focus:outline-none transition-colors duration-300">
            <i class="fas fa-heart" 
              :class="{ 'text-red-500': favoriteStates[drink.id], 'text-gray-400': !favoriteStates[drink.id] }">
            </i>
          </button>
        </div>

        <!-- 評分和情緒分析資訊 -->
        <div class="grid grid-cols-2 gap-3 mb-3">
          <!-- 評分資訊 -->
          <div class="bg-white rounded-lg p-2 shadow-sm border border-gray-100">
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-500">評分</span>
              <div class="flex items-center">
                <span class="text-yellow-400 mr-1"><i class="fas fa-star"></i></span>
                <span class="font-bold text-lg">{{ drink.rating }}</span>
              </div>
            </div>
            <div class="text-xs text-gray-400">
              {{ drink.review_number }}次瀏覽
            </div>
          </div>
          
          <!-- 情緒分析分數 -->
          <div class="bg-white rounded-lg p-2 shadow-sm border border-gray-100">
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-500">情緒指數</span>
              <div class="flex items-center">
                <span class="text-purple-400 mr-1"><i class="fas fa-heart"></i></span>
                <span class="font-bold text-lg">{{ (drink.composite_score || 0).toFixed(2) }}</span>
              </div>
            </div>
            <div class="text-xs text-gray-400">
              情緒分析評估
            </div>
          </div>
        </div>

        <!-- 地址資訊 -->
        <div class="flex items-center text-gray-600 mb-3">
          <i class="fas fa-map-marker-alt mr-2"></i>
          <span>{{ drink.city_CN }}</span>
        </div>

        <!-- 店家標籤 -->
        <div v-if="drink.tag" class="mb-3">
          <div class="flex flex-wrap gap-2">
            <span v-for="(tag, index) in drink.tag.split(',')" :key="index"
                  class="px-3 py-1 text-sm bg-purple-400 bg-opacity-20 text-purple-600 rounded-full flex items-center">
              <i class="fas fa-tag text-xs mr-1.5"></i>
              {{ tag.trim() }}
            </span>
          </div>
        </div>

        <!-- 店家描述 -->
        <!-- <p class="text-gray-600 mb-4 line-clamp-2">
          {{ truncateDescription(drink.description) }}
        </p> -->

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
        <!-- 店家圖片容器 -->
        <div class="relative h-64">
          <img :src="selectedDrink.image_url" 
               :alt="selectedDrink.name"
               class="w-full h-full object-cover"
               loading="lazy"
               @error="handleImageError">
        </div>

        <!-- 店家資訊 -->
        <div class="p-6">
          <!-- 頁籤選項固定在頂部 -->
          <div class="border-b border-gray-200 dark:border-gray-700 sticky top-0 bg-white z-10 mb-4">
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

          <!-- 頁籤內容區域 -->
          <div class="space-y-6 mt-6">
            <!-- 基本資訊 -->
            <div v-if="activeTab === 'info'" class="space-y-6">
              <!-- 店家名稱和評分區塊 -->
              <div class="mb-8">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                  {{ selectedDrink.name }}
                </h2>
                
                <!-- 評分和情緒分析卡片 -->
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
                      {{ selectedDrink.review_number }}次瀏覽
                    </div>
                  </div>

                  <!-- 情緒分析卡片 -->
                  <div class="bg-white dark:bg-gray-700 rounded-lg p-4 shadow-sm border border-gray-100">
                    <div class="flex items-center justify-between mb-2">
                      <span class="text-gray-600 dark:text-gray-300">情緒指數</span>
                      <div class="flex items-center">
                        <span class="text-purple-400 mr-2">
                          <i class="fas fa-heart text-xl"></i>
                        </span>
                        <span class="text-2xl font-bold text-gray-900 dark:text-white">
                          {{ (selectedDrink.composite_score || 0).toFixed(2) }}
                        </span>
                      </div>
                    </div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">
                      情緒分析評估
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
              <div class="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <!-- 標題區塊 -->
                <div class="flex items-center mb-6">
                  <div class="flex-shrink-0 w-10 h-10 bg-indigo-100 rounded-full flex items-center justify-center">
                    <i class="fas fa-store text-indigo-600"></i>
                  </div>
                  <h3 class="text-xl font-semibold text-gray-900 ml-4">
                    店家介紹
                  </h3>
                </div>

                <!-- 證號資訊區塊 -->
                <div class="bg-gray-50 rounded-lg p-4 mb-6 space-y-3">
                  <div class="flex items-center text-gray-700">
                    <div class="w-32 flex-shrink-0 text-gray-500 text-sm">
                      <i class="fas fa-certificate mr-2"></i>
                      登錄字號
                    </div>
                    <span class="text-sm">{{ selectedDrink.registration_number || '暫無資訊' }}</span>
                  </div>
                  <div class="flex items-center text-gray-700">
                    <div class="w-32 flex-shrink-0 text-gray-500 text-sm">
                      <i class="fas fa-shield-alt mr-2"></i>
                      保險字號
                    </div>
                    <span class="text-sm">{{ selectedDrink.insurance_number || '暫無資訊' }}</span>
                  </div>
                </div>

                <!-- 店家描述區塊 -->
                <div class="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-lg p-5">
                  <div class="relative">
                    <i class="fas fa-quote-left text-indigo-200 text-xl absolute -top-2 -left-2"></i>
                    <div class="text-gray-700 leading-relaxed whitespace-pre-line pl-6 pr-4">
                      {{ formatDescription(selectedDrink.description) }}
                    </div>
                    <i class="fas fa-quote-right text-indigo-200 text-xl absolute -bottom-2 -right-2"></i>
                  </div>
                </div>

                <!-- 環保政策提示 -->
                <div class="mt-6 flex items-start p-4 bg-green-50 rounded-lg">
                  <div class="flex-shrink-0">
                    <i class="fas fa-leaf text-green-500 mt-1"></i>
                  </div>
                  <div class="ml-3">
                    <h4 class="text-sm font-medium text-green-800">環保政策</h4>
                    <p class="mt-1 text-sm text-green-600">
                      本店每筆訂單的收餐點包裝費2元，因應環保署政策，店家不得免費提供購物用環保袋，為確保送餐品質，餐點皆由塑膠袋包裝。
                    </p>
                  </div>
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
                  class="px-4 py-2 bg-indigo-100 text-indigo-600 rounded-lg hover:bg-indigo-200 transition-all duration-300 ease-in-out transform hover:scale-105 flex items-center"
                >
                  <i class="fas fa-pencil-alt mr-2"></i>
                  撰寫評論
                </button>
              </div>

              <!-- 評論列表 -->
              <div class="max-h-[400px] overflow-y-auto pr-2">
                <div v-if="processedReviews && processedReviews.length > 0" 
                     class="space-y-4">
                  <div class="flex justify-between items-center mb-4">
                    <h3 class="text-lg font-medium text-gray-900">最新評論</h3>
                    <span class="text-sm text-gray-500">
                      (顯示最新 3 則評論)
                    </span>
                  </div>
                  <div v-for="review in processedReviews" 
                       :key="review.id" 
                       class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
                    <div class="flex items-start">
                      <img :src="review.user_avatar" 
                           :alt="review.user"
                           class="w-10 h-10 rounded-full"
                           @error="handleImageError">
                      <div class="ml-4 flex-1">
                        <div class="flex items-center justify-between">
                          <h4 class="font-medium text-gray-900 dark:text-white">
                            {{ review.user }}
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
    <div class="bg-white dark:bg-gray-800 rounded-lg w-full max-w-lg mx-4 relative">
      <!-- 關閉按鈕 -->
      <button @click="closeReviewForm" 
              class="absolute -top-2 -right-2 bg-white text-gray-600 rounded-full p-2 hover:bg-gray-100 shadow-md z-50 transition-colors duration-200">
        <i class="fas fa-times"></i>
      </button>

      <!-- 表單內容 -->
      <div class="p-6">
        <!-- 標題 -->
        <div class="mb-6">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
            撰寫評論
          </h3>
        </div>

        <!-- 評分區域 -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            評分
          </label>
          <div class="flex items-center">
            <div class="flex text-2xl text-yellow-400">
              <button v-for="n in 5"
                      :key="n"
                      @click="setRating(n)"
                      @mouseover="hoverRating = n"
                      @mouseleave="hoverRating = 0"
                      class="focus:outline-none mr-2">
                <i class="fas fa-star" 
                 :class="{
                   'text-yellow-400': hoverRating >= n || (!hoverRating && rating >= n),
                   'text-gray-300': (hoverRating && hoverRating < n) || (!hoverRating && rating < n)
                 }">
                </i>
              </button>
            </div>
            <span class="ml-3 text-sm text-gray-600 dark:text-gray-400">
              {{ rating }} 分
            </span>
          </div>
        </div>

        <!-- 評論文字區域 -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            評論內容
          </label>
          <textarea 
            v-model="comment"
            placeholder="請寫下您的評論..."
            class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            rows="4"
          ></textarea>
        </div>

        <!-- 按鈕區域 -->
        <div class="flex justify-end space-x-3">
          <button 
            @click="closeReviewForm"
            class="px-4 py-2 bg-gray-50 text-gray-600 rounded-lg hover:bg-gray-100 transition-all duration-300 ease-in-out transform hover:scale-105">
            取消
          </button>
          <button 
            @click="handleSubmitComment"
            class="px-4 py-2 bg-indigo-100 text-indigo-600 rounded-lg hover:bg-indigo-200 transition-all duration-300 ease-in-out transform hover:scale-105">
            發布評論
          </button>
        </div>
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
import accountAPI from '@/api/modules/account'

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
    const loading = ref(true)
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
    const imageLoaded = ref({})
    const modalImageLoaded = ref(false)
    const preloadedImages = ref(new Map()) // 新增圖片預加載 Map
    const cacheKey = ref('')
    const cacheData = ref(new Map())
    const cacheExpiry = 5 * 60 * 1000 // 5分鐘快取時間
    const lastFetchTime = ref(new Map())
    const viewCache = ref(new Map()) // 新增視圖快取
    const processedReviews = ref([])
    
    const handleImageLoad = (id) => {
      imageLoaded.value[id] = true
    }

    const handleModalImageLoad = () => {
      modalImageLoaded.value = true
    }

    const handleImageError = (event) => {
      const drinkId = event.target.closest('[data-drink-id]')?.dataset.drinkId
      if (drinkId) {
        imageLoaded.value[drinkId] = true
      }
      event.target.src = defaultImage
    }

    const showDrinkDetail = async (drink) => {
      try {
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
        modalImageLoaded.value = false
        const storeId = Number(drink.id)
        
        // 檢查收藏狀態
        checkFavoriteStatus(storeId)
        
        // 獲取特定店家的評論
        try {
          const response = await messageAPI.getMessages()
          console.log('店家評論數據:', response.data)
          if (response.data && response.data.messages) {
            selectedDrink.value = {
              ...drink,
              reviews: response.data.messages
            }
          }
        } catch (error) {
          console.error('獲取店家評論失敗:', error)
          selectedDrink.value = {
            ...drink,
            reviews: []
          }
        }
      } catch (error) {
        console.error('顯示店家詳情失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '系統錯誤',
          text: '無法載入店家資訊'
        })
      }
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

    // 修改快取 key 生成方法，移除視圖模式
    const getCacheKey = (sortBy, userId) => {
      return `drinks_${sortBy}_${userId}`
    }

    const getFromCache = (key) => {
      const cached = cacheData.value.get(key)
      const lastFetch = lastFetchTime.value.get(key)
      
      if (cached && lastFetch && (Date.now() - lastFetch < cacheExpiry)) {
        console.log('從快取讀取數據:', key)
        return cached
      }
      return null
    }

    const setToCache = (key, data) => {
      cacheData.value.set(key, data)
      lastFetchTime.value.set(key, Date.now())
      console.log('數據已快取:', key)
    }

    // 新增圖片預加載函數
    const preloadImages = (images) => {
      images.forEach(imageUrl => {
        if (!preloadedImages.value.has(imageUrl)) {
          const img = new Image()
          img.src = imageUrl
          img.onload = () => {
            preloadedImages.value.set(imageUrl, true)
          }
        }
      })
    }

    // 修改 preloadNextData 函數，加入圖片預加載
    const preloadNextData = async (currentSortBy) => {
      const sortTypes = ['hybrid', 'rating', 'preference', 'favorite']
      const nextSortIndex = (sortTypes.indexOf(currentSortBy) + 1) % sortTypes.length
      const nextSortBy = sortTypes[nextSortIndex]
      
      const nextSortCacheKey = getCacheKey(nextSortBy, props.userId)
      
      if (!getFromCache(nextSortCacheKey)) {
        console.log('預熱數據:', nextSortCacheKey)
        try {
          let response
          // ... existing API calls ...
          if (response?.data) {
            const processedData = processApiResponse(response.data, nextSortBy)
            setToCache(nextSortCacheKey, processedData)
            // 預加載下一頁籤的圖片
            const imageUrls = processedData.map(drink => drink.image_url).filter(Boolean)
            preloadImages(imageUrls)
          }
        } catch (error) {
          console.error('預熱數據失敗:', error)
        }
      }
    }

    // 處理 API 響應數據的統一方法
    const processApiResponse = (data, sortBy) => {
      let storesData = []
      if (sortBy === 'favorite') {
        storesData = data.favorites.map(favorite => ({
          id: favorite.store_id,
          name: favorite.store_name,
          rating: favorite.rating || 0,
          review_number: favorite.review_number || 0,
          city: favorite.city || '',
          city_CN: favorite.city_CN || '',
          navigation_url: favorite.navigation_url || '#',
          foodpanda_url: favorite.redirection_url || '#',
          image_url: favorite.store_image,
          address: favorite.address || '暫無地址資訊',
          phone: favorite.customer_phone || '暫無電話資訊',
          start_time: favorite.is_new_until || '暫無營業時間資訊',
          description: favorite.description || '暫無店家介紹',
          tag: favorite.tag || '',
        }))
      } else {
        const stores = data.stores || data.data || []
        storesData = stores.map(shop => ({
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
          composite_score: shop.composite_score || 0
        }))
      }
      return storesData
    }

    const fetchRecommendations = async () => {
      const sortBy = props.sortBy || 'hybrid'
      const currentCacheKey = getCacheKey(sortBy, props.userId)
      const cachedData = getFromCache(currentCacheKey)

      if (cachedData) {
        drinks.value = cachedData
        loading.value = false
        preloadNextData(sortBy)
        return
      }

      loading.value = true
      drinks.value = []
      imageLoaded.value = {}

      try {
        await new Promise(resolve => setTimeout(resolve, 300))
        let response

        switch (sortBy) {
          case 'rating':
            response = await recommendAPI.getContentRecommendations({
              limit: 10,
              user_id: props.userId,
              sort_by: 'rating',
              sort_order: 'desc'
            })
            break
          case 'preference':
            response = await recommendAPI.getCollaborativeRecommendations({
              limit: 10,
              user_id: props.userId,
              sort_by: 'composite_score',
              sort_order: 'desc'
            })
            break
          case 'favorite':
            response = await favoriteAPI.getFavorites()
            break
          case 'hybrid':
          default:
            response = await recommendAPI.getHybridRecommendations({
              limit: 10,
              user_id: props.userId
            })
        }

        if (response?.data) {
          const processedData = processApiResponse(response.data, sortBy)
          drinks.value = processedData
          
          // 儲存到快取
          setToCache(currentCacheKey, processedData)

          // 設置收藏狀態
          if (sortBy === 'favorite') {
            processedData.forEach(drink => {
              favoriteStates.value[drink.id] = true
            })
          }

          // 在背景預熱下一個頁籤的數據
          preloadNextData(sortBy)
        }
      } catch (err) {
        error.value = err.message
        console.error('獲取推薦飲料店失敗:', err)
      } finally {
        loading.value = false
      }
    }

    // 清除快取的方法
    const clearCache = () => {
      cacheData.value.clear()
      lastFetchTime.value.clear()
      console.log('快取已清除')
    }

    // 初始化數據
    const initializeData = async () => {
      const sortBy = props.sortBy || 'hybrid'
      const currentCacheKey = getCacheKey(sortBy, props.userId)
      const cachedData = getFromCache(currentCacheKey)

      if (cachedData) {
        drinks.value = cachedData
        loading.value = false
        preloadNextData(sortBy)
        return
      }

      // 如果沒有快取數據，則獲取新數據
      await fetchRecommendations()
    }

    // 監聽排序變化、用戶 ID 和視圖模式變化
    watch([() => props.sortBy, () => props.userId, () => props.viewMode], 
      ([newSort, newUserId, newViewMode], [oldSort, oldUserId, oldViewMode]) => {
      // 當用戶 ID 改變時，清除所有快取並重新初始化
      if (newUserId !== oldUserId) {
        clearCache()
        initializeData()
        return
      }

      // 如果只是視圖模式改變，直接返回，不做任何操作
      if (newViewMode !== oldViewMode) {
        return
      }

      // 排序方式改變時，先檢查快取
      if (newSort !== oldSort) {
        const currentCacheKey = getCacheKey(newSort, props.userId)
        const cachedData = getFromCache(currentCacheKey)
        
        if (cachedData) {
          drinks.value = cachedData
          loading.value = false
          preloadNextData(newSort)
        } else {
          fetchRecommendations()
        }
      }
    })

    // 監聽 props.drinks 的變化
    watch(() => props.drinks, (newDrinks) => {
      if (newDrinks && newDrinks.length > 0) {
        drinks.value = newDrinks
        // 預加載所有圖片
        const imageUrls = newDrinks.map(drink => drink.image_url).filter(Boolean)
        preloadImages(imageUrls)
        
        const sortBy = props.sortBy || 'hybrid'
        const currentCacheKey = getCacheKey(sortBy, props.userId)
        if (!getFromCache(currentCacheKey)) {
          setToCache(currentCacheKey, newDrinks)
          preloadNextData(sortBy)
        }
      }
    }, { immediate: true })

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
            let avatarUrl = defaultAvatar

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

    onMounted(() => {
      // 首次載入時初始化數據
      initializeData()
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

    const getReviewCount = computed(() => {
      return processedReviews.value ? processedReviews.value.length : 0
    })

    return {
      drinks,
      loading,
      error,
      handleImageError,
      handleImageLoad,
      imageLoaded,
      modalImageLoaded,
      handleModalImageLoad,
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
      processedReviews,
      getReviewCount
    }
  }
}
</script>

<style scoped>
/* 網格布局動畫 */
.layout-grid-move,
.layout-list-move {
  transition: all 0.3s cubic-bezier(0.33, 1, 0.68, 1);
}

/* 進入和離開動畫 */
.layout-grid-enter-active,
.layout-grid-leave-active,
.layout-list-enter-active,
.layout-list-leave-active {
  transition: opacity 0.3s cubic-bezier(0.33, 1, 0.68, 1);
  position: absolute;
  width: 100%;
  will-change: opacity;
}

.layout-grid-enter-from,
.layout-grid-leave-to,
.layout-list-enter-from,
.layout-list-leave-to {
  opacity: 0;
}

.layout-grid-enter-to,
.layout-list-enter-to {
  position: relative;
}

/* 容器樣式 */
.grid,
.space-y-4 {
  position: relative;
  min-height: 200px;
}

/* 確保元素在過渡期間的定位 */
.grid > *,
.space-y-4 > * {
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
}

/* 圖片載入過渡效果 */
.image-fade-enter-active,
.image-fade-leave-active {
  transition: opacity 0.25s cubic-bezier(0.4, 0, 0.6, 1);
}

.image-fade-enter-from,
.image-fade-leave-to {
  opacity: 0;
}

/* 優化圖片容器 */
.drink-image-container {
  position: relative;
  overflow: hidden;
  background-color: #f5f5f5;
  transform: translateZ(0);
  -webkit-transform: translateZ(0);
}

.drink-image-container img {
  transition: opacity 0.25s cubic-bezier(0.4, 0, 0.6, 1);
  transform: translateZ(0);
  -webkit-transform: translateZ(0);
}

/* 載入中動畫優化 */
.loading-skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* 優化卡片效果 */
.cursor-pointer {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.6, 1);
  transform: translateZ(0);
  -webkit-transform: translateZ(0);
}

.cursor-pointer:hover {
  transform: translateY(-2px) translateZ(0);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* 彈窗動畫 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.25s cubic-bezier(0.4, 0, 0.6, 1);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* 工具提示動畫 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

a:hover::after {
  animation: fadeIn 0.25s cubic-bezier(0.4, 0, 0.6, 1) forwards;
}
</style> 