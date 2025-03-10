import axios from '@/utils/axios'

export default {
  // 獲取基本統計數據
  getBasicStats() {
    return axios.get('/dashboard/basic-stats/')
      .catch(error => {
        console.error('Get basic stats Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 獲取熱門店家
  getTopShops() {
    return axios.get('/dashboard/top-shops/')
      .catch(error => {
        console.error('Get top shops Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 獲取最新評論
  getLatestReviews() {
    return axios.get('/dashboard/latest-reviews/')
      .catch(error => {
        console.error('Get latest reviews Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 獲取系統日誌
  getSystemLogs() {
    return axios.get('/dashboard/system-logs/')
      .catch(error => {
        console.error('Get system logs Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 獲取活動數據
  getActivityData() {
    return axios.get('/dashboard/activity-data/')
      .catch(error => {
        console.error('Get activity data Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 保留原有的完整數據獲取方法（用於向後兼容）
  getDashboardStats() {
    console.log('Calling dashboardAPI')
    return axios.get('/dashboard/stats/')
      .catch(error => {
        console.error('GetdashboardAPI Error:', error.response?.data || error.message)
        throw error
      })
  }
}
