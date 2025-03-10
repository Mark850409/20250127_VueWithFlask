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
              <div class="flex items-center mt-1 space-x-4">
                <!-- 原始評分 -->
                <div class="flex items-center">
                  <span class="text-sm text-gray-500 mr-2">評分:</span>
                  <star-rating :rating="5" :read-only="true" :star-size="15" />
                </div>
                <!-- 平均評分 -->
                <div class="flex items-center">
                  <span class="text-sm text-gray-500 mr-2">平均:</span>
                  <star-rating :rating="shop.rating" :read-only="true" :star-size="15" />
                </div>
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
    const currentPeriod = ref('月')
    const loading = ref({
      stats: true,
      shops: true,
      reviews: true,
      logs: true,
      activity: true
    })
    
    const periods = ['日', '週', '月']

    const fetchDashboardData = async () => {
      try {
        // 使用 Promise.all 並行請求所有數據
        const [
          statsResponse,
          shopsResponse,
          reviewsResponse,
          logsResponse,
          activityResponse
        ] = await Promise.all([
          dashboardAPI.getBasicStats(),
          dashboardAPI.getTopShops(),
          dashboardAPI.getLatestReviews(),
          dashboardAPI.getSystemLogs(),
          dashboardAPI.getActivityData()
        ])

        // 更新各個部分的數據
        stats.value = statsResponse.data.stats
        loading.value.stats = false
        console.log('Stats loaded:', stats.value)

        topShops.value = shopsResponse.data.topShops
        loading.value.shops = false
        console.log('Shops loaded:', topShops.value)

        latestReviews.value = reviewsResponse.data.latestReviews
        loading.value.reviews = false
        console.log('Reviews loaded:', latestReviews.value)

        systemLogs.value = logsResponse.data.systemLogs
        loading.value.logs = false
        console.log('Logs loaded:', systemLogs.value)

        activityData.value = activityResponse.data.activityData
        loading.value.activity = false
        console.log('Activity data loaded:', activityData.value)

      } catch (error) {
        console.error('獲取儀表板數據失敗:', error)
        // 在錯誤時也要更新載入狀態
        Object.keys(loading.value).forEach(key => {
          loading.value[key] = false
        })
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
        // 只顯示今天的24小時數據
        const today = new Date()
        const todayStr = today.toISOString().split('T')[0]
        
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
          activityData.value.hourly.dates.forEach((date, index) => {
            const [dateStr, timeStr] = date.split(' ')
            if (dateStr === todayStr) {
              const hour = timeStr.split(':')[0] + ':00'
              const hourIndex = hourlyData.dates.findIndex(h => h === hour)
              if (hourIndex !== -1) {
                hourlyData.values[hourIndex] = activityData.value.hourly.values[index]
              }
            }
          })
        }
        
        return hourlyData
        
      } else if (currentPeriod.value === '週') {
        // 獲取最近7天的數據
        const endDate = new Date()
        const startDate = new Date()
        startDate.setDate(endDate.getDate() - 7)
        
        // 生成最近7天的日期陣列
        const weekDates = []
        const weekValues = []
        
        for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
          const dateStr = d.toISOString().split('T')[0]
          const index = dates.findIndex(date => date.startsWith(dateStr))
          
          weekDates.push(`${d.getMonth() + 1}/${d.getDate()}`)
          weekValues.push(index !== -1 ? values[index] : 0)
        }
        
        return {
          dates: weekDates,
          values: weekValues
        }
        
      } else if (currentPeriod.value === '月') {
        // 獲取最近30天的數據
        const endDate = new Date()
        const startDate = new Date()
        startDate.setDate(endDate.getDate() - 30)
        
        // 生成最近30天的日期陣列
        const monthDates = []
        const monthValues = []
        let dayCount = 0
        
        for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
          const dateStr = d.toISOString().split('T')[0]
          const index = dates.findIndex(date => date.startsWith(dateStr))
          
          // 每6天顯示一次日期，最後一天也顯示
          const showDate = dayCount % 6 === 0 || d.getTime() === endDate.getTime()
          monthDates.push(showDate ? `${d.getMonth() + 1}/${d.getDate()}` : '')
          monthValues.push(index !== -1 ? values[index] : 0)
          dayCount++
        }
        
        return {
          dates: monthDates,
          values: monthValues
        }
      }
      
      return { dates: [], values: [] }
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
      goToStore,
      loading
    }
  }
}
</script> 