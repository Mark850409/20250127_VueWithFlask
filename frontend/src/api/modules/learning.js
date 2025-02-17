import axios from '@/utils/axios'

export default {
  // 獲取所有學習區塊
  getLearningBlocks() {
    return axios.get('/v1/learning/')
      .catch(error => {
        console.error('GetLearningBlocks Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 創建主標題區塊
  createSection(data) {
    return axios.post('/v1/learning/sections', data)
      .catch(error => {
        console.error('CreateSection Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 創建次標題區塊
  createSubsection(data) {
    return axios.post('/v1/learning/subsections', data)
      .catch(error => {
        console.error('CreateSubsection Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 更新主標題區塊
  updateSection(id, data) {
    return axios.put(`/v1/learning/sections/${id}`, data)
      .catch(error => {
        console.error('UpdateSection Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 更新次標題區塊
  updateSubsection(id, data) {
    return axios.put(`/v1/learning/subsections/${id}`, data)
      .catch(error => {
        console.error('UpdateSubsection Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 刪除主標題區塊
  deleteSection(id) {
    return axios.delete(`/v1/learning/sections/${id}`)
      .catch(error => {
        console.error('DeleteSection Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 刪除次標題區塊
  deleteSubsection(id) {
    return axios.delete(`/v1/learning/subsections/${id}`)
      .catch(error => {
        console.error('DeleteSubsection Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 上傳圖片
  uploadImage(formData) {
    return axios.post('/v1/learning/images', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).catch(error => {
      console.error('UploadImage Error:', error.response?.data || error.message)
      throw error
    })
  }
} 