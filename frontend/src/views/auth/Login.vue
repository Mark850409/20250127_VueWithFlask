<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 py-12 px-4 sm:px-6 lg:px-8 flex items-center">
    <div class="max-w-md w-full mx-auto space-y-8 bg-white rounded-2xl shadow-xl p-8">
      <!-- Logo -->
      <div class="text-center">
        <i class="fas fa-utensils text-6xl text-indigo-600"></i>
        <h2 class="mt-6 text-3xl font-extrabold text-gray-900">
          {{ isLogin ? '歡迎回來' : '建立新帳號' }}
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          {{ isLogin ? '使用您的帳號登入系統' : '填寫以下資料以建立帳號' }}
        </p>
      </div>

      <!-- 表單 -->
      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div class="rounded-md shadow-sm space-y-4">
          <div v-if="!isLogin" class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">頭像</label>
            <div class="flex items-center space-x-4">
              <img :src="avatarPreview || defaultAvatar" 
                   class="h-20 w-20 rounded-full object-cover border-2 border-gray-200"
                   alt="頭像預覽">
              <div class="flex flex-col space-y-2">
                <label class="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500">
                  <span>上傳頭像</span>
                  <input type="file" 
                         class="sr-only" 
                         accept="image/*"
                         @change="handleAvatarChange">
                </label>
                <p class="text-xs text-gray-500">PNG, JPG 格式 (最大 2MB)</p>
              </div>
            </div>
          </div>

          <div v-if="!isLogin">
            <label for="username" class="block text-sm font-medium text-gray-700">
              名稱 <span class="text-red-500">*</span>
            </label>
            <input id="username" 
                   v-model="form.username"
                   type="text"
                   required
                   :class="{'border-red-500': errors.username}"
                   class="appearance-none relative block w-full px-3 py-2 border border-gray-300 
                          placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none 
                          focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                   placeholder="請輸入您的名稱">
            <p v-if="errors.username" class="mt-1 text-xs text-red-500">{{ errors.username }}</p>
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              Email <span class="text-red-500">*</span>
            </label>
            <input id="email" 
                   v-model="form.email" 
                   type="email" 
                   required
                   :class="{'border-red-500': errors.email}"
                   class="appearance-none relative block w-full px-3 py-2 border border-gray-300 
                          placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none 
                          focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                   placeholder="請輸入Email">
            <p v-if="errors.email" class="mt-1 text-xs text-red-500">{{ errors.email }}</p>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              密碼 <span class="text-red-500">*</span>
            </label>
            <input id="password" 
                   v-model="form.password" 
                   type="password" 
                   required
                   :class="{'border-red-500': errors.password}"
                   class="appearance-none relative block w-full px-3 py-2 border border-gray-300 
                          placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none 
                          focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                   placeholder="請輸入密碼">
            <p v-if="errors.password" class="mt-1 text-xs text-red-500">{{ errors.password }}</p>
            <p class="mt-1 text-xs text-gray-500">密碼需要6-12碼，包含大小寫字母、數字及特殊符號</p>
          </div>

          <div v-if="!isLogin">
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700">
              確認密碼 <span class="text-red-500">*</span>
            </label>
            <input id="confirmPassword" 
                   v-model="form.confirmPassword" 
                   type="password" 
                   required
                   :class="{'border-red-500': errors.confirmPassword}"
                   class="appearance-none relative block w-full px-3 py-2 border border-gray-300 
                          placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none 
                          focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                   placeholder="請再次輸入密碼">
            <p v-if="errors.confirmPassword" class="mt-1 text-xs text-red-500">{{ errors.confirmPassword }}</p>
          </div>
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center" v-if="isLogin">
            <input id="remember-me" type="checkbox" v-model="form.remember"
                   class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded">
            <label for="remember-me" class="ml-2 block text-sm text-gray-900">
              記住我
            </label>
          </div>

          <div class="text-sm" v-if="isLogin">
            <a @click="showForgotPasswordModal = true" 
               class="font-medium text-indigo-600 hover:text-indigo-500 cursor-pointer">
              忘記密碼？
            </a>
          </div>
        </div>

        <div>
          <button type="submit" 
                  class="group relative w-full flex justify-center py-2 px-4 border border-transparent 
                         text-sm font-medium rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 
                         focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <i class="fas fa-lock text-indigo-500 group-hover:text-indigo-400"></i>
            </span>
            {{ isLogin ? '登入' : '註冊' }}
          </button>
        </div>
      </form>

      <!-- 分隔線 -->
      <div class="relative my-6">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-300"></div>
        </div>
        <div class="relative flex justify-center text-sm">
          <span class="px-2 bg-white text-gray-500">或使用以下方式</span>
        </div>
      </div>

      <!-- 社群登入按鈕 -->
      <div class="grid grid-cols-3 gap-3">
        <button @click="socialLogin('google')"
                class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-lg 
                       shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
          <i class="fab fa-google text-red-500"></i>
        </button>
        <button @click="socialLogin('facebook')"
                class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-lg 
                       shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
          <i class="fab fa-facebook text-blue-600"></i>
        </button>
        <button @click="socialLogin('line')"
                class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-lg 
                       shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
          <i class="fab fa-line text-green-500"></i>
        </button>
      </div>

      <!-- 切換登入/註冊 -->
      <div class="text-center">
        <button @click="isLogin = !isLogin" class="text-sm text-indigo-600 hover:text-indigo-500">
          {{ isLogin ? '還沒有帳號？立即註冊' : '已有帳號？立即登入' }}
        </button>
      </div>

      <!-- 忘記密碼 Modal -->
      <div v-if="showForgotPasswordModal" 
           class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg p-8 max-w-md w-full mx-4">
          <h3 class="text-xl font-bold mb-4">重設密碼</h3>
          <p class="text-gray-600 mb-4">請輸入您的 Email，我們將發送重設密碼連結給您。</p>
          
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <input type="email" 
                   v-model="forgotPasswordEmail"
                   class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                   placeholder="請輸入您的 Email">
          </div>
          
          <div class="flex justify-end space-x-3">
            <button @click="showForgotPasswordModal = false"
                    class="px-4 py-2 text-gray-600 hover:text-gray-800">
              取消
            </button>
            <button @click="handleForgotPassword"
                    class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
              發送重設連結
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'
import accountApi from '@/api/modules/account'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const isLogin = ref(true)
    const defaultAvatar = 'https://api.dicebear.com/7.x/bottts/svg?seed=default'
    const avatarPreview = ref('')
    const avatarFile = ref(null)
    
    const form = reactive({
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      remember: false,
      status: 'Enabled'
    })

    const errors = reactive({
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      avatar: ''
    })

    const showForgotPasswordModal = ref(false)
    const forgotPasswordEmail = ref('')

    const validatePassword = (password) => {
      // 密碼驗證規則
      const rules = {
        length: password.length >= 6 && password.length <= 12,
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        number: /[0-9]/.test(password),
        special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
      }

      const errors = []
      if (!rules.length) errors.push('密碼長度需要在6-12碼之間')
      if (!rules.uppercase) errors.push('需要包含大寫字母')
      if (!rules.lowercase) errors.push('需要包含小寫字母')
      if (!rules.number) errors.push('需要包含數字')
      if (!rules.special) errors.push('需要包含特殊符號')

      return {
        isValid: Object.values(rules).every(rule => rule),
        errors: errors
      }
    }

    const validateForm = () => {
      let isValid = true
      errors.username = ''
      errors.email = ''
      errors.password = ''
      errors.confirmPassword = ''
      errors.avatar = ''

      if (!isLogin.value) {
        if (!form.username) {
          errors.username = '請輸入名稱'
          isValid = false
        } else if (form.username.length < 2) {
          errors.username = '名稱至少需要2個字符'
          isValid = false
        }
      }

      if (!form.email) {
        errors.email = '請輸入Email'
        isValid = false
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
        errors.email = '請輸入有效的Email格式'
        isValid = false
      }

      // 加強密碼驗證
      const passwordValidation = validatePassword(form.password)
      if (!passwordValidation.isValid) {
        errors.password = passwordValidation.errors.join('、')
        isValid = false
      }

      if (!isLogin.value && form.password !== form.confirmPassword) {
        errors.confirmPassword = '兩次輸入的密碼不一致'
        isValid = false
      }

      // 頭像驗證
      if (avatarFile.value) {
        if (avatarFile.value.size > 2 * 1024 * 1024) {
          errors.avatar = '圖片大小不能超過2MB'
          isValid = false
        }
        const fileType = avatarFile.value.type.toLowerCase()
        if (!['image/jpeg', 'image/jpg', 'image/png'].includes(fileType)) {
          errors.avatar = '只支援 JPG 和 PNG 格式'
          isValid = false
        }
      }

      return isValid
    }

    const handleAvatarChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        // 驗證文件大小（2MB）
        if (file.size > 2 * 1024 * 1024) {
          Swal.fire({
            icon: 'error',
            title: '檔案太大',
            text: '圖片大小不能超過2MB',
            confirmButtonText: '確定'
          })
          event.target.value = ''  // 清空選擇
          return
        }

        // 驗證文件類型
        const fileType = file.type.toLowerCase()
        if (!['image/jpeg', 'image/jpg', 'image/png'].includes(fileType)) {
          Swal.fire({
            icon: 'error',
            title: '檔案格式錯誤',
            text: '只支援 JPG 和 PNG 格式',
            confirmButtonText: '確定'
          })
          event.target.value = ''  // 清空選擇
          return
        }

        // 儲存文件對象
        avatarFile.value = file
        
        // 預覽頭像
        const reader = new FileReader()
        reader.onload = (e) => {
          avatarPreview.value = e.target.result
        }
        reader.readAsDataURL(file)
      } else {
        avatarFile.value = null
        avatarPreview.value = defaultAvatar
      }
    }

    const handleSubmit = async () => {
      try {
        if (!validateForm()) {
          const errorMessages = Object.values(errors)
            .filter(msg => msg)
            .join('\n')
          
          if (errorMessages) {
            await Swal.fire({
              icon: 'error',
              title: '表單驗證失敗',
              text: errorMessages,
              confirmButtonText: '確定'
            })
          }
          return
        }

        if (!isLogin.value) {
          // 先進行用戶註冊
          const registerResponse = await accountApi.createAccount({
            username: form.username,
            email: form.email,
            password: form.password,
            status: form.status
          })
          
          // 保存 token 和用戶信息
          if (registerResponse.data.token) {
            localStorage.setItem('token', registerResponse.data.token)
            localStorage.setItem('user', JSON.stringify(registerResponse.data.user))
          }
          
          // 如果註冊成功且有上傳頭像，則更新頭像
          if (registerResponse.status === 201 && avatarFile.value) {
            const formData = new FormData()
            formData.append('file', avatarFile.value)
            
            const token = localStorage.getItem('token')
            console.log('從 Login 獲取的 token:', token)
            
            await accountApi.uploadAvatar(formData, token)
          }
          
          // 註冊成功
          await Swal.fire({
            icon: 'success',
            title: '註冊成功',
            text: '請使用新帳號登入',
            confirmButtonText: '確定'
          })
          isLogin.value = true
          form.password = ''
          form.confirmPassword = ''
        } else {
          // 處理登入
          const response = await accountApi.login({
            email: form.email,
            password: form.password
          })

          if (response.data.token) {
            localStorage.setItem('token', response.data.token)
            localStorage.setItem('user', JSON.stringify(response.data.user))
            console.log('保存的用戶信息:', response.data.user)
            
            await Swal.fire({
              icon: 'success',
              title: '登入成功',
              text: '歡迎回來',
              timer: 1500,
              showConfirmButton: false
            })
            router.push('/admin')
          }
        }
      } catch (error) {
        console.error('Login Error:', error)
      }
    }

    const socialLogin = async (provider) => {
      try {
        // TODO: 實作社群登入邏輯
        console.log('Social login with:', provider)
      } catch (error) {
        console.error('Social Login Error:', error)
        // 特殊的社群登入錯誤處理
        await Swal.fire({
          icon: 'error',
          title: '社群登入失敗',
          text: '請稍後再試',
          confirmButtonText: '確定'
        })
      }
    }

    const handleForgotPassword = async () => {
      try {
        if (!forgotPasswordEmail.value) {
          Swal.fire({
            icon: 'warning',
            title: '請輸入 Email',
            text: 'Email 不能為空',
            confirmButtonText: '確定'
          })
          return
        }
        
        const response = await accountApi.requestPasswordReset(forgotPasswordEmail.value)
        
        if (response.data.success) {
          showForgotPasswordModal.value = false
          Swal.fire({
            icon: 'success',
            title: '重設密碼郵件已發送',
            text: '請檢查您的信箱',
            confirmButtonText: '確定'
          })
        }
      } catch (error) {
        console.error('忘記密碼錯誤:', error)
        Swal.fire({
          icon: 'error',
          title: '發送失敗',
          text: error.response?.data?.message || '請稍後再試',
          confirmButtonText: '確定'
        })
      }
    }

    return {
      isLogin,
      form,
      errors,
      defaultAvatar,
      avatarPreview,
      avatarFile,
      handleAvatarChange,
      handleSubmit,
      socialLogin,
      showForgotPasswordModal,
      forgotPasswordEmail,
      handleForgotPassword
    }
  }
}
</script> 