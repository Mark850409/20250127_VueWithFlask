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

  // 檢查店家是否已收藏
  checkFavorite(storeId) {
    return axios.get(`/favorites/check/${storeId}`)
      .catch(error => {
        console.error('CheckFavorite Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 添加收藏
  addFavorite(data) {
    // 檢查必要欄位
    if (!data.store_id || !data.store_name || !data.username) {
      console.error('缺少必要欄位:', data)
      throw new Error('缺少必要欄位')
    }

    // 確保 store_id 是數字
    const payload = {
      store_id: Number(data.store_id),
      store_image: data.store_image || '',
      store_name: data.store_name,
      username: data.username
    }

    console.log('addFavorite 請求資料:', {
      url: '/favorites/',
      method: 'POST',
      data: payload
    })

    return axios.post('/favorites/', payload).catch(error => {
      console.error('AddFavorite Error:', {
        response: error.response?.data,
        status: error.response?.status,
        message: error.message,
        config: error.config
      })
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