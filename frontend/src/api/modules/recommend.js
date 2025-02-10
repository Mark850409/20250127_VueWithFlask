import axios from '@/utils/axios'

export default {
  // 獲取熱門飲料店列表
  getPopularDrinks(params) {
    const sortBy = params.sort_by === 'default' ? 'review_number' : params.sort_by
    return axios.get('/stores/query', {
      params: {
        limit: params.limit || 12,
        sort_by: sortBy,
        order: 'desc'
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