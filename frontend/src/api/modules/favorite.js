import axios from '@/utils/axios'

export default {
  // 獲取收藏列表
  getFavorites() {
    return axios.get('/favorites/')
      .catch(error => {
        console.error('GetFavorites Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 刪除收藏
  deleteFavorite(id) {
    return axios.delete(`/favorites/${id}`)
      .catch(error => {
        console.error('DeleteFavorite Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 批量刪除收藏
  batchDeleteFavorites(ids) {
    return Promise.all(ids.map(id => this.deleteFavorite(id)))
      .catch(error => {
        console.error('BatchDeleteFavorites Error:', error.response?.data || error.message)
        throw error
      })
  }
} 