<template>
  <div class="dashboard-card-title space-y-6">
    <!-- 快速導航區 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <template v-if="stats && stats.length > 0">
        <router-link v-for="stat in stats" :key="stat.title" 
             :to="stat.path"
             class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-gray-600">{{ stat.title }}</h3>
            <i :class="[stat.icon, stat.iconColor, 'text-xl']"></i>
          </div>
          <p class="text-3xl font-bold">{{ stat.value }}{{ stat.unit }}</p>
          <p :class="[stat.trend > 0 ? 'text-green-500' : 'text-red-500', 'text-sm mt-2']">
            <i :class="[stat.trend > 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down', 'mr-1']"></i>
            較上月{{ stat.trend > 0 ? '增加' : '減少' }} {{ Math.abs(stat.trend).toFixed(1) }}%
          </p>
        </router-link>
      </template>
      <template v-else>
        <div class="col-span-4 text-center py-8 text-gray-500">
          載入中...
        </div>
      </template>
    </div>

    <!-- 圖表區域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 用戶活躍度趨勢 -->
      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">用戶活躍度趨勢</h3>
          <div class="space-x-2">
            <button v-for="period in periods" :key="period"
                    @click="changePeriod(period)"
                    :class="[
                      'px-3 py-1 rounded-full text-sm',
                      currentPeriod === period ? 'bg-blue-500 text-white' : 'bg-gray-100'
                    ]">
              {{ period }}
            </button>
          </div>
        </div>
        <LineChart 
          :data="processedActivityData" 
          :period="currentPeriod" 
        />
      </div>

      <!-- 熱門店家排行 -->
      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">熱門店家排行</h3>
          <router-link to="/admin/shops" 
                       class="text-blue-500 hover:text-blue-600 text-sm">
            查看全部 <i class="fas fa-arrow-right ml-1"></i>
          </router-link>
        </div>
        <div class="space-y-4">
          <div v-for="(shop, index) in topShops" :key="shop.id" 
               class="flex items-center p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
               @click="goToStore(shop.id)">
            <span :class="[
              'w-8 h-8 flex items-center justify-center rounded-full mr-4 text-white',
              index < 3 ? 'bg-yellow-400' : 'bg-gray-400'
            ]">
              {{ index + 1 }}
            </span>
            <div class="flex-1">
              <h4 class="font-medium">{{ shop.name }}</h4>
              <p class="text-sm text-gray-500">{{ shop.city_CN }} - {{ shop.address }}</p>
              <div class="flex items-center text-sm text-gray-500">
                <star-rating :rating="shop.rating" :read-only="true" :star-size="15" />
                <span class="ml-2">{{ shop.rating }}</span>
              </div>
            </div>
            <div class="text-right">
              <p class="text-sm font-medium">{{ shop.review_number }}則評論</p>
              <p :class="[
                'text-sm',
                shop.increase >= 0 ? 'text-green-500' : 'text-red-500'
              ]">
                <i :class="[
                  shop.increase >= 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down',
                  'mr-1'
                ]"></i>
                {{ Math.abs(shop.increase) }}%
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 最新動態區 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 最新評論 -->
      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">最新評論</h3>
          <router-link to="/admin/ratings" class="text-blue-500 hover:text-blue-600 text-sm">
            查看全部 <i class="fas fa-arrow-right ml-1"></i>
          </router-link>
        </div>

        <div class="space-y-4">
          <div v-for="review in latestReviews" :key="review.id"
               class="p-4 bg-gray-50 rounded-lg">
            <div class="flex items-start justify-between">
              <div class="flex items-center">
                <div class="ml-3">
                  <p class="font-medium">{{ review.user }}</p>
                  <p class="text-sm text-gray-500">{{ review.restaurant_name }}</p>
                </div>
              </div>
              <star-rating :rating="review.rating" :read-only="true" :star-size="15" />
            </div>
            <p class="mt-2 text-gray-600">{{ review.text }}</p>
            <p class="mt-1 text-gray-400 text-sm">{{ review.english_texts }}</p>
            <p class="mt-2 text-sm text-gray-400">{{ review.createdAt }}</p>
          </div>
        </div>
      </div>

      <!-- 系統日誌 -->
      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">系統日誌</h3>
          <router-link to="/admin/logs" class="text-blue-500 hover:text-blue-600 text-sm">
            查看全部 <i class="fas fa-arrow-right ml-1"></i>
          </router-link>
        </div>
        <div class="space-y-3">
          <div v-for="log in systemLogs" :key="log.id"
               :class="[
                 'flex items-center p-3 rounded-lg',
                 log.type === 'error' ? 'bg-red-50' : 'bg-gray-50'
               ]">
            <i :class="[
              'mr-3 text-lg',
              log.type === 'error' ? 'fas fa-exclamation-circle text-red-500' :
              log.type === 'warning' ? 'fas fa-exclamation-triangle text-yellow-500' :
              'fas fa-info-circle text-blue-500'
            ]"></i>
            <div class="flex-1">
              <p :class="[
                'font-medium',
                log.type === 'error' ? 'text-red-700' : 'text-gray-700'
              ]">{{ log.message }}</p>
              <p class="text-sm text-gray-500">{{ log.timestamp }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import StarRating from 'vue-star-rating'
import LineChart from '@/components/charts/LineChart.vue'
import { dashboardAPI } from '@/api'

export default {
  name: 'Dashboard',
  components: {
    StarRating,
    LineChart
  },
  
  setup() {
    const router = useRouter()
    const stats = ref([])
    const topShops = ref([])
    const latestReviews = ref([])
    const systemLogs = ref([])
    const activityData = ref({})
    const currentPeriod = ref('日')
    
    const periods = ['日', '週', '月']

    const fetchDashboardData = async () => {
      try {
        const response = await dashboardAPI.getDashboardStats()
        console.log('Dashboard data:', response)
        stats.value = response.data.stats
        console.log('Stats after assignment:', stats.value)
        topShops.value = response.data.topShops
        console.log('topShops assignment:', topShops.value)
        latestReviews.value = response.data.latestReviews
        console.log('latestReviews assignment:', latestReviews.value)
        systemLogs.value = response.data.systemLogs
        console.log('systemLogs assignment:', systemLogs.value)
        activityData.value = response.data.activityData
        console.log('activityData assignment:', activityData.value)
      } catch (error) {
        console.error('獲取儀表板數據失敗:', error)
      }
    }

    // 處理活躍度數據
    const processedActivityData = computed(() => {
      if (!activityData.value?.dates || !activityData.value?.values) {
        return {
          dates: [],
          values: []
        }
      }
      
      const { dates, values } = activityData.value
      console.log('Processing activity data:', { dates, values })
      
      // 根據不同時間範圍處理數據
      if (currentPeriod.value === '日') {
        // 只顯示今天的數據
        const today = new Date()
        const todayStr = today.toISOString().split('T')[0]  // 格式: YYYY-MM-DD
        
        // 生成24小時的時間點
        const hours = Array.from({ length: 24 }, (_, i) => 
          `${String(i).padStart(2, '0')}:00`
        )
        
        // 初始化所有小時的數據為0
        const hourlyData = hours.reduce((acc, hour) => {
          acc.dates.push(hour)
          acc.values.push(0)
          return acc
        }, { dates: [], values: [] })
        
        // 使用後端返回的 hourly 數據
        if (activityData.value.hourly) {
          const { dates: hourlyDates, values: hourlyValues } = activityData.value.hourly
          hourlyDates.forEach((date, index) => {
            const [dateStr, timeStr] = date.split(' ')  // 分離日期和時間
            if (dateStr === todayStr) {
              const hour = timeStr.split(':')[0] + ':00'  // 只取小時部分
              const hourIndex = hourlyData.dates.findIndex(h => h === hour)
              if (hourIndex !== -1) {
                hourlyData.values[hourIndex] = hourlyValues[index]
              }
            }
          })
        }
        
        return hourlyData
      } else if (currentPeriod.value === '週') {
        // 顯示包含今天在內的最近7天數據
        return {
          dates: dates.slice(-7).map(date => {
            // 將日期格式從 YYYY-MM-DD 轉換為 MM/DD
            const [_, month, day] = date.split('-')
            return `${month}/${day}`
          }),
          values: values.slice(-7)
        }
      } else if (currentPeriod.value === '月') {
        return {
          dates: dates.map(date => date.split(' ')[0]),  // 只顯示日期部分
          values: values
        }
      }
    })

    const changePeriod = (period) => {
      currentPeriod.value = period
    }

    const goToStore = (storeId) => {
      router.push(`/admin/stores/${storeId}`)
    }

    onMounted(() => {
      fetchDashboardData()
    })

    return {
      stats,
      topShops,
      latestReviews,
      systemLogs,
      activityData,
      periods,
      currentPeriod,
      processedActivityData,
      changePeriod,
      goToStore
    }
  }
}
</script> 