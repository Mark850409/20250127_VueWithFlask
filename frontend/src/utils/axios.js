import axios from 'axios'
import Swal from 'sweetalert2'
import router from '@/router'

// 根據環境設置基礎 URL
const getBaseURL = () => {
  // 調試信息
  console.group('API Configuration')
  console.log('Complete Environment:', import.meta.env)
  console.log('VITE_API_URL:', import.meta.env.VITE_API_URL)
  console.log('VITE_BACKEND_URL:', import.meta.env.VITE_BACKEND_URL)
  console.log('MODE:', import.meta.env.MODE)
  console.groupEnd()

  if (!import.meta.env.VITE_API_URL) {
    console.warn('VITE_API_URL is undefined!')
  }
  return import.meta.env.VITE_API_URL
}

// 創建 axios 實例
const instance = axios.create({
  baseURL: getBaseURL(),
  timeout: 5000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 請求攔截器
instance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    // 添加時間戳防止緩存
    if (config.method === 'get') {
      config.params = { ...config.params, _t: Date.now() }
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 響應攔截器
instance.interceptors.response.use(
  response => {
    return response
  },
  error => {
    console.group('API Error Details')
    console.error('Error:', error)
    console.error('Error Response:', error.response)
    console.error('Error Data:', error.response?.data)
    console.groupEnd()

    // 獲取錯誤信息
    const status = error.response?.status
    let title = '錯誤'
    let message = ''

    // 解析錯誤信息
    if (error.response?.data?.message) {
      message = error.response.data.message
    } else if (typeof error.response?.data === 'string') {
      message = error.response.data
    } else if (error.message) {
      message = error.message
    }

    // 根據不同狀態碼處理錯誤
    switch (status) {
      case 400:
        title = '請求錯誤'
        // 處理業務邏輯錯誤（如：郵箱已存在）
        Swal.fire({
          icon: 'error',
          title: title,
          html: `<div class="text-center">
                  <p class="text-lg font-semibold text-red-500">${message}</p>
                </div>`,
          confirmButtonText: '確定',
          background: '#1a1a1a',
          customClass: {
            popup: 'swal2-show',
            title: 'text-white',
            htmlContainer: 'text-white',
            confirmButton: 'bg-blue-500 hover:bg-blue-600'
          }
        })
        break

      case 422:
        title = '驗證錯誤'
        // 處理表單驗證錯誤
        let validationErrors = []
        if (error.response?.data?.detail) {
          validationErrors = Array.isArray(error.response.data.detail) 
            ? error.response.data.detail 
            : [error.response.data.detail]
        }
        
        Swal.fire({
          icon: 'error',
          title: title,
          html: `<div class="text-center">
                  <p class="text-lg font-semibold text-red-500">${message}</p>
                  ${validationErrors.map(err => 
                    `<p class="text-sm text-gray-300 mt-2">${err.msg || err}</p>`
                  ).join('')}
                </div>`,
          confirmButtonText: '確定',
          background: '#1a1a1a',
          customClass: {
            popup: 'swal2-show',
            title: 'text-white',
            htmlContainer: 'text-white',
            confirmButton: 'bg-blue-500 hover:bg-blue-600'
          }
        })
        break

      case 401:
        title = '認證失敗'
        Swal.fire({
          icon: 'warning',
          title: title,
          html: `<div class="text-center">
                  <p class="text-lg font-semibold text-yellow-500">${message || '請重新登入'}</p>
                </div>`,
          confirmButtonText: '確定',
          background: '#1a1a1a',
          customClass: {
            popup: 'swal2-show',
            title: 'text-white',
            htmlContainer: 'text-white',
            confirmButton: 'bg-blue-500 hover:bg-blue-600'
          }
        }).then(() => {
          localStorage.removeItem('token')
          router.push('/login')
        })
        break

      default:
        // 處理其他錯誤
        Swal.fire({
          icon: 'error',
          title: title,
          html: `<div class="text-center">
                  <p class="text-lg font-semibold text-red-500">${message || '發生錯誤，請稍後再試'}</p>
                  <p class="text-sm text-gray-300 mt-2">錯誤代碼: ${status || '未知'}</p>
                </div>`,
          confirmButtonText: '確定',
          background: '#1a1a1a',
          customClass: {
            popup: 'swal2-show',
            title: 'text-white',
            htmlContainer: 'text-white',
            confirmButton: 'bg-blue-500 hover:bg-blue-600'
          }
        })
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