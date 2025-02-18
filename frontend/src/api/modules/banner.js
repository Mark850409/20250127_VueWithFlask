import axios from '@/utils/axios'

export default {
  // 獲取所有輪播圖（管理員）
  getAllBanners() {
    return axios({
      url: '/v1/admin/banners',
      method: 'get'
    })
  },

  // 創建輪播圖
  createBanner(data) {
    return axios({
      url: '/v1/admin/banners',
      method: 'post',
      data
    })
  },

  // 更新輪播圖
  updateBanner(id, data) {
    return axios({
      url: `/v1/admin/banners/${id}`,
      method: 'put',
      data
    })
  },

  // 刪除輪播圖
  deleteBanner(id) {
    return axios({
      url: `/v1/admin/banners/${id}`,
      method: 'delete'
    })
  },

  // 獲取前台啟用的輪播圖
  getActiveBanners() {
    return axios({
      url: '/v1/banners',
      method: 'get'
    })
  },

  // 獲取指定類型的輪播圖
  getBannersByType(type) {
    return axios({
      url: `/v1/banners/${type}`,
      method: 'get'
    })
  }
}