import axios from '@/utils/axios'

export default {
  // 獲取帳號列表
  getAccounts() {
    console.log('Calling getAccounts API')
    return axios.get('/users/')
      .catch(error => {
        console.error('GetAccounts Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 新增帳號
  createAccount(data) {
    console.log('API createAccount 接收到的數據:', data)
    const requestData = { ...data }
    if (requestData.avatar === '') {
      delete requestData.avatar
    }
    console.log('API 發送創建帳號請求:', requestData)
    return axios.post('/users/register', requestData, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .catch(error => {
        console.error('CreateAccount Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 更新帳號
  updateAccount(id, data) {
    return axios.put(`/users/${id}`, data)
  },

  // 刪除帳號
  deleteAccount(id) {
    return axios.delete(`/users/${id}`)
  },

  // 上傳頭像
  uploadAvatar(formData, token) {
    return axios.post('/users/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${token}`
      }
    })
  }
} 