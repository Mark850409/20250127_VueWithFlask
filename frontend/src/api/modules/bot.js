import axios from '@/utils/axios'

export default {
  // 獲取所有問答列表
  getBots(params = {}) {
    return axios.get('/bots/', {
      params: params
    })
      .catch(error => {
        console.error('GetBots Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 新增問答
  createBot(data) {
    return axios.post('/bots/', data)
      .catch(error => {
        console.error('CreateBot Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 更新問答
  updateBot(id, data) {
    return axios.put(`/bots/${id}`, data)
      .catch(error => {
        console.error('UpdateBot Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 刪除問答
  deleteBot(id) {
    return axios.delete(`/bots/${id}`)
      .catch(error => {
        console.error('DeleteBot Error:', error.response?.data || error.message)
        throw error
      })
  }
} 