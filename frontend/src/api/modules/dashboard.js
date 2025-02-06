import axios from '@/utils/axios'

export default {
// 獲取儀表板統計數據
getDashboardStats() {
  console.log('Calling dashboardAPI')
  return axios.get('/dashboard/stats/')
    .catch(error => {
      console.error('GetdashboardAPI Error:', error.response?.data || error.message)
      throw error
    })
}
}
