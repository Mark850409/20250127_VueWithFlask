import axios from '@/utils/axios'

export default {
  // 登入
  login(data) {
    return axios.post('/users/login', {
      email: data.email,
      password: data.password
    })
    .catch(error => {
      console.error('Login Error:', error.response?.data || error.message)
      throw error
    })
  },

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
  },

  // 請求重設密碼
  requestPasswordReset(email) {
    return axios.post('/users/forgot-password', { email })
      .catch(error => {
        console.error('Request Password Reset Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 驗證重設密碼 token
  verifyResetToken(token) {
    return axios.get(`/users/verify-reset-token/${token}`)
      .catch(error => {
        console.error('Verify Reset Token Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 重設密碼
  resetPassword(token, newPassword) {
    return axios.post(`/users/reset-password`, { password: newPassword })
      .catch(error => {
        console.error('Reset Password Error:', error.response?.data || error.message)
        throw error
      })
  }
} 