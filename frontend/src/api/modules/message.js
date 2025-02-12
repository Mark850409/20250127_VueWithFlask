import axios from '@/utils/axios'

export default {
  // 獲取用戶資料
  getUserInfo(userId) {
    return axios.get(`/users/${userId}`)
      .catch(error => {
        console.error('GetUserInfo Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 獲取所有評論
  getMessages() {
    return axios.get('/messages/')
      .catch(error => {
        console.error('GetMessages Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 創建評論
  createMessage(data) {
    return axios.post('/messages/', data)
      .catch(error => {
        console.error('CreateMessage Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 更新評論
  updateMessage(id, data) {
    return axios.put(`/messages/${id}`, data)
      .catch(error => {
        console.error('UpdateMessage Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 刪除評論
  deleteMessage(id) {
    return axios.delete(`/messages/${id}`)
      .catch(error => {
        console.error('DeleteMessage Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 添加回覆
  addReply(messageId, data) {
    return axios.post(`/messages/${messageId}/replies`, data)
      .catch(error => {
        console.error('AddReply Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 刪除回覆
  deleteReply(messageId, replyId) {
    return axios.delete(`/messages/${messageId}/replies/${replyId}`)
      .catch(error => {
        console.error('DeleteReply Error:', error.response?.data || error.message)
        throw error
      })
  }
} 