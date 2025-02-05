import axios from '@/utils/axios'

export function useLogger() {
  // 獲取客戶端 IP 地址
  const getClientIP = async () => {
    try {
      // 假設後端提供了獲取 IP 的 API 端點
      const response = await axios.get('/client-ip')
      return response.data.ip
    } catch (error) {
      console.error('獲取 IP 地址失敗:', error)
      return ''
    }
  }

  // 獲取當前用戶信息
  const getCurrentUser = () => {
    try {
      const userStr = localStorage.getItem('user')
      return userStr ? JSON.parse(userStr) : null
    } catch (error) {
      console.error('解析用戶信息失敗:', error)
      return null
    }
  }

  const logOperation = async (operation, type = '操作') => {
    try {
      const user = getCurrentUser()
      const username = user?.username || 'unknown'
      const userId = user?.id || null
      const clientIP = await getClientIP()
      
      await axios.post('/logs/', {
        action: type,                // 操作類型
        description: operation,      // 操作描述
        ip_address: clientIP,        // 使用從後端獲取的 IP
        status: 'success',          // 操作狀態
        user_id: userId,
        username: username
      })
    } catch (error) {
      if (error.response?.status !== 401) {
        console.error('記錄操作失敗:', error.response?.data?.message || error.message)
      }
    }
  }

  return {
    logOperation
  }
} 