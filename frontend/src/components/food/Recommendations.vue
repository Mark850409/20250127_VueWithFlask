<template>
  <div v-if="isLoggedIn">
    <!-- 熱門飲料店推薦 -->
    <section class="popular-drink-section bg-white dark:bg-gray-900">
      <div class="container mx-auto px-4">
        <!-- 排序和視圖切換選項 -->
        <div class="max-w-7xl mx-auto">
          <div class="flex flex-col md:flex-row md:justify-between md:items-center mb-8 space-y-4 md:space-y-0">
            <!-- 排序選項 -->
            <div class="grid grid-cols-2 gap-2 md:flex md:space-x-4">
              <button 
                v-for="sort in sortOptions" 
                :key="sort.value"
                @click="currentSort = sort.value"
                :class="[
                  'sort-btn px-4 py-2 rounded-full transition duration-300 flex items-center justify-center space-x-2 text-sm md:text-base',
                  currentSort === sort.value 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-blue-50 text-blue-600 hover:bg-blue-100'
                ]"
              >
                <i :class="sort.icon"></i>
                <span>{{ sort.label }}</span>
              </button>
            </div>
            
            <div class="flex space-x-2 justify-center md:justify-end">
              <button 
                @click="viewMode = 'grid'"
                :class="[
                  'p-2 rounded transition duration-300 grid-btn',
                  viewMode === 'grid' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-blue-50 text-blue-600 hover:bg-blue-100'
                ]"
              >
                <i class="fas fa-th"></i>
              </button>
              <button 
                @click="viewMode = 'list'"
                :class="[
                  'p-2 rounded transition duration-300 list-btn',
                  viewMode === 'list' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-blue-50 text-blue-600 hover:bg-blue-100'
                ]"
              >
                <i class="fas fa-list"></i>
              </button>
            </div>
          </div>
        </div>
        
        <!-- 修改 transition-group -->
        <transition-group
          name="fade"
          tag="div"
          class="max-w-7xl mx-auto"
          appear
        >
          <PopularDrinkList 
            :key="viewMode"
            :viewMode="viewMode"
            :sortBy="currentSort"
          />
        </transition-group>
      </div>
    </section>

    <!-- 推薦飲料店區塊 -->
    <section class="py-16 bg-gray-50 dark:bg-gray-800">
      <div class="container mx-auto px-4">
        <!-- 標題區塊 -->
        <div class="text-center mb-16">
          <span class="span-title inline-block px-4 py-1 bg-blue-50 text-blue-500 font-medium rounded-full mb-4">
            RECOMMENDED DRINKS
          </span>
          <h2 class="text-4xl font-bold text-gray-900">
            為您推薦 <span class="span-subtitle text-blue-500">的飲料店</span>
          </h2>
        </div>

        <!-- 排序和視圖切換選項 -->
        <div class="max-w-7xl mx-auto">
          <div class="flex flex-col md:flex-row md:justify-between md:items-center mb-8 space-y-4 md:space-y-0">
            <!-- 排序選項 -->
            <div class="grid grid-cols-2 gap-2 md:flex md:space-x-4">
              <button 
                v-for="sort in recommendSortOptions" 
                :key="sort.value"
                @click="recommendSort = sort.value"
                :class="[
                  'sort-btn px-4 py-2 rounded-full transition duration-300 flex items-center justify-center space-x-2 text-sm md:text-base',
                  recommendSort === sort.value 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-blue-50 text-blue-600 hover:bg-blue-100'
                ]"
              >
                <i :class="sort.icon"></i>
                <span>{{ sort.label }}</span>
              </button>
            </div>

            <div class="flex space-x-2 justify-center md:justify-end">
              <button 
                @click="recommendViewMode = 'grid'"
                :class="[
                  'p-2 rounded transition duration-300 grid-btn',
                  recommendViewMode === 'grid' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-blue-50 text-blue-600 hover:bg-blue-100'
                ]"
              >
                <i class="fas fa-th"></i>
              </button>
              <button 
                @click="recommendViewMode = 'list'"
                :class="[
                  'p-2 rounded transition duration-300 list-btn',
                  recommendViewMode === 'list' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-blue-50 text-blue-600 hover:bg-blue-100'
                ]"
              >
                <i class="fas fa-list"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- 修改第二個 transition-group -->
        <transition-group
          name="fade"
          tag="div"
          class="max-w-7xl mx-auto"
          appear
        >
          <DrinkShopList 
            :key="recommendViewMode"
            :viewMode="recommendViewMode"
            :sortBy="recommendSort"
            :userId="userId"
          />
        </transition-group>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import DrinkShopList from './DrinkShopList.vue'
import PopularDrinkList from './PopularDrinkList.vue'

export default {
  name: 'Recommendations',
  components: {
    DrinkShopList,
    PopularDrinkList
  },

  setup() {
    const authStore = useAuthStore()
    const isLoggedIn = computed(() => authStore.isLoggedIn)
    const userId = computed(() => {
      // 從 localStorage 中獲取用戶資訊
      const userInfo = localStorage.getItem('user')
      if (userInfo) {
        try {
          const user = JSON.parse(userInfo)
          console.log('解析用戶資訊:', user)
          return user.id || 1

        } catch (e) {
          console.error('解析用戶資訊失敗:', e)
          return 1
        }
      }
      return 1
    })

    // 熱門飲料店視圖控制
    const viewMode = ref('grid')
    const currentSort = ref('default')

    // 推薦飲料店視圖控制
    const recommendViewMode = ref('grid')
    const recommendSort = ref('default')

    const sortOptions = [
      { 
        label: '預設排序', 
        value: 'default',
        icon: 'fas fa-sort'
      },
      { 
        label: '評分排序', 
        value: 'rating',
        icon: 'fas fa-star'
      },
      { 
        label: '瀏覽次數排序', 
        value: 'review_number',
        icon: 'fas fa-eye'
      },
      { 
        label: '距離排序', 
        value: 'distance',
        icon: 'fas fa-route'
      }
    ]

    const recommendSortOptions = [
      { label: '預設排序', value: 'default', icon: 'fas fa-sort' },
      { label: '評分排序', value: 'rating', icon: 'fas fa-star' },
      { label: '好感度排序', value: 'preference', icon: 'fas fa-thumbs-up' },
      { label: '最愛排序', value: 'favorite', icon: 'fas fa-heart' },
    ]

    return {
      isLoggedIn,
      viewMode,
      currentSort,
      recommendViewMode,
      recommendSort,
      sortOptions,
      recommendSortOptions,
      userId
    }
  }
}
</script>

<style scoped>
/* 淡入淡出動畫 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.6s ease-in-out, transform 0.6s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}

/* 確保容器樣式 */
.container {
  position: relative;
  min-height: 400px;
  overflow: hidden;
}

section {
  overflow: hidden;
}
</style> 