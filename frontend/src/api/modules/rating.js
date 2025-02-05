import axios from '@/utils/axios'

export default {
  // 獲取評分列表
  getRatings() {
    return axios.get('/ratings/')
      .catch(error => {
        console.error('GetRatings Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 更新評分
  updateRating(id, data) {
    return axios.put(`/ratings/${id}`, data)
      .catch(error => {
        console.error('UpdateRating Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 刪除評分
  deleteRating(id) {
    return axios.delete(`/ratings/${id}`)
      .catch(error => {
        console.error('DeleteRating Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 批量刪除評分
  batchDeleteRatings(ids) {
    return Promise.all(ids.map(id => this.deleteRating(id)))
      .catch(error => {
        console.error('BatchDeleteRatings Error:', error.response?.data || error.message)
        throw error
      })
  }
} 