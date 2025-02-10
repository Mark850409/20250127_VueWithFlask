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
                'px-4 py-2 rounded-full transition duration-300 flex items-center space-x-2',
                currentSort === sort.value 
                  ? 'bg-gray-800 text-white dark:bg-gray-700' 
                  : 'bg-gray-200 text-gray-700 dark:bg-gray-600 dark:text-gray-300'
              ]"
            >
              <i :class="sort.icon"></i>
              <span>{{ sort.label }}</span>
            </button>
          </div>
          
          <div class="flex space-x-2">
            <button 
              @click="viewMode = 'grid'"
              :class="[
                'p-2 rounded transition duration-300',
                viewMode === 'grid' 
                  ? 'bg-gray-800 text-white dark:bg-gray-700' 
                  : 'bg-gray-200 text-gray-700 dark:bg-gray-600 dark:text-gray-300'
              ]"
            >
              <i class="fas fa-th"></i>
            </button>
            <button 
              @click="viewMode = 'list'"
              :class="[
                'p-2 rounded transition duration-300',
                viewMode === 'list' 
                  ? 'bg-gray-800 text-white dark:bg-gray-700' 
                  : 'bg-gray-200 text-gray-700 dark:bg-gray-600 dark:text-gray-300'
              ]"
            >
              <i class="fas fa-list"></i>
            </button>
          </div>
        </div>
        
        <!-- 熱門飲料店列表 -->
        <PopularDrinkList 
          :viewMode="viewMode"
          :sortBy="currentSort"
          :key="currentSort"
        />
      </div>
    </section>

    <!-- 推薦飲料店區塊 -->
    <section class="py-16 bg-gray-50 dark:bg-gray-800">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-8 text-gray-900 dark:text-white">為您推薦的飲料店</h2>
        
        <!-- 排序和視圖切換選項 -->
        <div class="flex justify-between items-center mb-8">
          <div class="flex space-x-4">
            <button 
              v-for="sort in recommendSortOptions" 
              :key="sort.value"
              @click="recommendSort = sort.value"
              :class="[
                'px-4 py-2 rounded-full transition duration-300 flex items-center space-x-2',
                recommendSort === sort.value 
                  ? 'bg-gray-800 text-white dark:bg-gray-700' 
                  : 'bg-gray-200 text-gray-700 dark:bg-gray-600 dark:text-gray-300'
              ]"
            >
              <i :class="sort.icon"></i>
              <span>{{ sort.label }}</span>
            </button>
          </div>
          
          <div class="flex space-x-2">
            <button 
              @click="recommendViewMode = 'grid'"
              :class="[
                'p-2 rounded transition duration-300',
                recommendViewMode === 'grid' 
                  ? 'bg-gray-800 text-white dark:bg-gray-700' 
                  : 'bg-gray-200 text-gray-700 dark:bg-gray-600 dark:text-gray-300'
              ]"
            >
              <i class="fas fa-th"></i>
            </button>
            <button 
              @click="recommendViewMode = 'list'"
              :class="[
                'p-2 rounded transition duration-300',
                recommendViewMode === 'list' 
                  ? 'bg-gray-800 text-white dark:bg-gray-700' 
                  : 'bg-gray-200 text-gray-700 dark:bg-gray-600 dark:text-gray-300'
              ]"
            >
              <i class="fas fa-list"></i>
            </button>
          </div>
        </div>
        
        <!-- 推薦飲料店列表 -->
        <DrinkShopList 
          :viewMode="recommendViewMode"
          :sortBy="recommendSort"
          :userId="userId"
        />
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
        label: '瀏覽次數', 
        value: 'review_number',
        icon: 'fas fa-eye'
      }
    ]

    const recommendSortOptions = [
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
        label: '好感度排序', 
        value: 'preference',
        icon: 'fas fa-heart'
      }
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
/* 容器樣式 */
.container {
  position: relative;
  min-height: 400px; /* 設置最小高度以避免切換時的跳動 */
}

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
  width: 100%;
}

/* 確保列表視圖的容器寬度正確 */
section {
  overflow: hidden;
}
</style> 