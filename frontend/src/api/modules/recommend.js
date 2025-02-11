import axios from '@/utils/axios'

export default {
  // 計算路線距離
  calculateDistance(params) {
    return axios.get('/v1/maps/distance-matrix', {
      params: {
        origins: [params.origin],  // 改為陣列格式
        destinations: [params.destination],  // 改為陣列格式
        mode: 'driving',
        language: 'zh-TW'
      }
    }).catch(error => {
      console.error('Calculate Distance Error:', error)
      if (error.response) {
        // 伺服器回應錯誤
        console.error('Response Error:', error.response.data)
        throw new Error(error.response.data.message || '計算距離失敗')
      } else if (error.request) {
        // 請求發送失敗
        console.error('Request Error:', error.request)
        throw new Error('網路連接失敗')
      } else {
        // 其他錯誤
        console.error('Error:', error.message)
        throw new Error('發生未知錯誤')
      }
    })
  },

  // 經緯度轉地址
  reverseGeocode(params) {
    return axios.get('/v1/maps/geocode/reverse', {
      params: {
        latitude: params.latitude,
        longitude: params.longitude,
        language: params.language || 'zh-TW'
      }
    }).catch(error => {
      console.error('ReverseGeocode Error:', error.response?.data || error.message)
      throw error
    })
  },

  // 獲取熱門飲料店列表
  getPopularDrinks(params) {
    const sortBy = params.sort_by === 'default' ? 'review_number' : params.sort_by
    return axios.get('/stores/query', {
      params: {
        limit: params.limit || 12,
        sort_by: sortBy,
        order: 'desc',
        city: params.city
      }
    }).catch(error => {
      console.error('GetPopularDrinks Error:', error.response?.data || error.message)
      throw error
    })
  },

  // 混合推薦 API (預設)
  getHybridRecommendations(params) {
    console.log('getHybridRecommendations', params)
    return axios.get('/hybrid_recommend_data', {
      params: {
        user_id: params.user_id || 1,
        num_recommendations: params.limit || 10
      }
    }).catch(error => {
      console.error('GetHybridRecommendations Error:', error.response?.data || error.message)
      throw error
    })
  },

  // 內容推薦 API (評分排序)
  getContentRecommendations(params) {
    return axios.get('/content_recommendations', {
      params: {
        user_id: params.user_id || 1,
        num_recommendations: params.limit || 10
      }
    }).catch(error => {
      console.error('GetContentRecommendations Error:', error.response?.data || error.message)
      throw error
    })
  },

  // 協同過濾推薦 API (好感度排序)
  getCollaborativeRecommendations(params) {
    return axios.get('/collaborative_recommendations', {
      params: {
        user_id: params.user_id || 1,
        num_recommendations: params.limit || 10
      }
    }).catch(error => {
      console.error('GetCollaborativeRecommendations Error:', error.response?.data || error.message)
      throw error
    })
  }
} 