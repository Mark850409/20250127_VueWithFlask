import axios from '@/utils/axios'

export default {
  // 獲取店家列表
  getShops() {
    return axios.get('/stores/')
  },

  // 獲取單一店家
  getShop(id) {
    return axios.get(`/stores/${id}`)
  },

  // 新增店家
  createShop(data) {
    return axios.post('/stores/', data)
  },

  // 更新店家
  updateShop(id, data) {
    return axios.put(`/stores/${id}`, data)
  },

  // 刪除店家
  deleteShop(id) {
    return axios.delete(`/stores/${id}`)
  },

  // 上傳圖片
  uploadImage(formData) {
    return axios.post('/stores/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
} 