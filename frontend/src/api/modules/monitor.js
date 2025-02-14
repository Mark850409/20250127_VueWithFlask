import axios from '@/utils/axios'

export default {
  // 獲取監控訊息列表
  getMonitorMessages(params) {
    return axios.get('v1/monitor/messages', { params })
      .catch(error => {
        console.error('GetMonitorMessages Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 刪除監控訊息
  deleteMessage(sessionId) {
    return axios.delete(`v1/monitor/messages/session/${sessionId}`)
      .catch(error => {
        console.error('DeleteMessage Error:', error.response?.data || error.message)
        throw error
      })
  }
} 