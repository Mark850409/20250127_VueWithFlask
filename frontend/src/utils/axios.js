import axios from 'axios'
import Swal from 'sweetalert2'
import router from '@/router'

// 根據環境設置基礎 URL
const getBaseURL = () => {
  switch (process.env.NODE_ENV) {
    case 'development':
      return 'http://localhost:5000/api'
    case 'test':
      return 'http://test-api.example.com/api'
    case 'production':
      return 'https://api.example.com/api'
    default:
      return '/'
  }
}

// 創建 axios 實例
const instance = axios.create({
  baseURL: getBaseURL(),
  timeout: 60000,  // 增加超時時間到 15 秒
  withCredentials: true,  // 添加這行
  headers: {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'  // 標識 AJAX 請求
  }
})

// 請求攔截器
instance.interceptors.request.use(
  config => {
    // 添加 token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // 防止快取
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }

    return config
  },
  error => {
    console.error('Request Error:', error)
    return Promise.reject(error)
  }
)

// 響應攔截器
instance.interceptors.response.use(
  response => {
    return response
  },
  error => {
    console.error('Response Error:', error)

    // 如果請求被取消
    if (axios.isCancel(error)) {
      console.log('Request canceled:', error.message)
      return Promise.reject(error)
    }

    // 獲取錯誤狀態碼
    const status = error.response?.status
    const message = error.response?.data?.message || '請求失敗'

    // 根據不同狀態碼處理錯誤
    switch (status) {
      case 400:
        Swal.fire({
          icon: 'error',
          title: '請求錯誤',
          text: message,
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
        break

      case 401:
        Swal.fire({
          icon: 'warning',
          title: '未授權',
          text: '請重新登入',
          confirmButtonText: '確定'
        }).then(() => {
          localStorage.removeItem('token')
          router.push('/login')
        })
        break

      case 403:
        Swal.fire({
          icon: 'error',
          title: '拒絕訪問',
          text: '您沒有權限執行此操作',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
        break

      case 404:
        Swal.fire({
          icon: 'error',
          title: '資源不存在',
          text: message,
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
        break

      case 409:
        Swal.fire({
          icon: 'warning',
          title: '資源衝突',
          text: message,
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
        break

      case 422:
        Swal.fire({
          icon: 'error',
          title: '驗證錯誤',
          text: message,
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
        break

      case 500:
        Swal.fire({
          icon: 'error',
          title: '伺服器錯誤',
          text: '請稍後再試或聯繫管理員',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
        break

      case 502:
        Swal.fire({
          icon: 'error',
          title: '網關錯誤',
          text: '伺服器可能正在維護中，請稍後再試',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
        break

      case 503:
        Swal.fire({
          icon: 'error',
          title: '服務不可用',
          text: '系統可能正在維護中，請稍後再試',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
        break

      default:
        if (!window.navigator.onLine) {
          // 處理離線情況
          Swal.fire({
            icon: 'error',
            title: '網路連接失敗',
            text: '請檢查您的網路連接',
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000
          })
        } else {
          // 其他未知錯誤
          Swal.fire({
            icon: 'error',
            title: '發生錯誤',
            text: message,
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000
          })
        }
    }

    return Promise.reject(error)
  }
)

// 添加請求取消功能
export const createCancelToken = () => {
  const source = axios.CancelToken.source()
  return source
}

export default instance 