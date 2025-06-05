<template>
  <!-- 修改背景和遮罩 -->
  <div class="min-h-screen relative flex items-center">
    <!-- 背景圖片 -->
    <div class="absolute inset-0 z-0">
      <img 
        src="https://images.unsplash.com/photo-1515059810521-a1d411d8517f?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        class="w-full h-full object-cover"
        alt="背景圖片"
      >
      <!-- 遮罩層 -->
      <div class="absolute inset-0 bg-black/60"></div>
    </div>

    <!-- 主要內容 -->
    <div class="relative z-10 w-full max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col md:flex-row relative">
        <!-- 左側圖片區域 -->
        <div class="w-full md:w-1/2 transition-transform duration-500 p-8 md:p-16" 
             :class="{ 'md:translate-x-full': !isLogin }">
          <div class="text-white space-y-6 md:space-y-8">
            <!-- Logo 和標題區域 -->
            <div class="text-center space-y-4 md:space-y-6">
              <i class="ri-cup-line text-5xl md:text-7xl text-white"></i>
              <h2 class="text-3xl md:text-5xl font-extrabold tracking-wide text-white drop-shadow-lg">
                今天喝什麼呢?
              </h2>
              <p class="text-lg md:text-xl text-white drop-shadow-md">
                使用您的帳號登入系統
              </p>
            </div>
            
            <!-- 關於網站說明 -->
            <div class="mt-6 md:mt-12 space-y-4 text-center">
              <p class="text-base md:text-lg text-white text-left drop-shadow-md leading-relaxed">
                在我們的飲品推薦平台，每一杯飲品都是一次獨特的體驗。透過先進的文字探勘技術和情感分析， 我們精準解讀用戶的評價和偏好，為您提供最貼心的推薦服務。
              </p>
            </div>
          </div>
        </div>

        <!-- 右側表單區域 -->
        <div class="w-full md:w-1/2 transition-transform duration-500 p-6 md:p-8 backdrop-blur-sm bg-white/10 rounded-2xl mt-6 md:mt-0"
             :class="{ 'md:-translate-x-full': !isLogin }">
          <!-- 表單內容 -->
          <form class="space-y-4" @submit.prevent="handleSubmit">
            <div class="rounded-md shadow-sm space-y-3">
              <div v-if="!isLogin" class="space-y-1">
                <label class="block text-sm font-medium text-white/90">頭像</label>
                <div class="flex items-center space-x-4">
                  <img :src="avatarPreview || defaultAvatar" 
                       class="h-16 w-16 rounded-full object-cover border-2 border-gray-200"
                       alt="頭像預覽">
                  <div class="flex flex-col space-y-1">
                    <label class="relative cursor-pointer rounded-md font-medium text-indigo-600 text-white/90">
                      <span>上傳頭像</span>
                      <input type="file" 
                             class="sr-only" 
                             accept="image/*"
                             @change="handleAvatarChange">
                    </label>
                    <p class="text-xs text-white/90">PNG, JPG 格式 (最大 2MB)</p>
                  </div>
                </div>
              </div>

              <div v-if="!isLogin">
                <label for="username" class="block text-sm font-medium text-white/90">
                  名稱 <span class="text-red-500">*</span>
                </label>
                <input id="username" 
                       v-model="form.username"
                       type="text"
                       required
                       :class="{'border-red-500': errors.username}"
                       class="appearance-none relative block w-full px-3 py-2 
                              border border-white/30 bg-white/20 backdrop-blur-md
                              placeholder-gray-300 text-white rounded-xl
                              focus:outline-none focus:ring-2 focus:ring-indigo-400 
                              focus:border-transparent transition-all duration-200
                              hover:bg-white/30"
                       placeholder="請輸入您的名稱">
                <p v-if="errors.username" class="mt-1 text-xs text-red-500">{{ errors.username }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-white/90">
                  Email <span class="text-red-300">*</span>
                </label>
                <input id="email" 
                       v-model="form.email" 
                       type="email" 
                       required
                       :class="{'border-red-500': errors.email}"
                       class="appearance-none relative block w-full px-3 py-2 
                              border border-white/30 bg-white/30 backdrop-blur-md
                              placeholder-white/60 text-white rounded-xl
                              focus:outline-none focus:ring-2 focus:ring-indigo-400 
                              focus:border-transparent transition-all duration-200
                              hover:bg-white/40"
                       placeholder="請輸入Email">
                <p v-if="errors.email" class="mt-1 text-xs text-red-500">{{ errors.email }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-white/90">
                  密碼 <span class="text-red-500">*</span>
                </label>
                <div class="relative">
                  <input :type="showPassword ? 'text' : 'password'"
                         v-model="form.password"
                         class="appearance-none relative block w-full px-3 py-2 
                                border border-white/30 bg-white/20 backdrop-blur-md
                                placeholder-gray-300 text-white rounded-xl
                                focus:outline-none focus:ring-2 focus:ring-indigo-400 
                                focus:border-transparent transition-all duration-200
                                hover:bg-white/30"
                         :class="{'border-red-500': errors.password}"
                         placeholder="請輸入密碼">
                  <button type="button"
                          @click="showPassword = !showPassword"
                          class="absolute right-3 top-1/2 -translate-y-1/2 text-white/70 hover:text-white/90">
                    <i :class="showPassword ? 'ri-eye-line' : 'ri-eye-off-line'"></i>
                  </button>
                </div>
                <p v-if="errors.password" class="mt-1 text-xs text-red-300">
                  {{ errors.password }}
                </p>
                <p class="mt-1 text-xs text-white/80">
                  密碼需要6-12碼，包含大小寫字母、數字及特殊符號
                </p>
              </div>

              <div v-if="!isLogin">
                <label for="confirmPassword" class="block text-sm font-medium text-white/90">
                  確認密碼 <span class="text-red-500">*</span>
                </label>
                <div class="relative">
                  <input id="confirmPassword" 
                         v-model="form.confirmPassword" 
                         :type="showConfirmPassword ? 'text' : 'password'"
                         required
                         :class="{'border-red-500': errors.confirmPassword}"
                         class="appearance-none relative block w-full px-3 py-2 
                                border border-white/30 bg-white/20 backdrop-blur-md
                                placeholder-gray-300 text-white rounded-xl
                                focus:outline-none focus:ring-2 focus:ring-indigo-400 
                                focus:border-transparent transition-all duration-200
                                hover:bg-white/30"
                         placeholder="請再次輸入密碼">
                  <button type="button"
                          @click="showConfirmPassword = !showConfirmPassword"
                          class="absolute right-3 top-1/2 -translate-y-1/2 text-white/70 hover:text-white/90">
                    <i :class="showConfirmPassword ? 'ri-eye-line' : 'ri-eye-off-line'"></i>
                  </button>
                </div>
                <p v-if="errors.confirmPassword" class="mt-1 text-xs text-red-500">{{ errors.confirmPassword }}</p>
              </div>
            </div>

            <div class="flex items-center justify-between">
              <div class="flex items-center" v-if="isLogin">
                <input id="remember-me" type="checkbox" v-model="form.remember"
                       class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded">
                <label for="remember-me" class="ml-2 block text-sm text-white/90">
                  記住我
                </label>
              </div>

              <div class="text-sm" v-if="isLogin">
                <a @click="showForgotPasswordModal = true" 
                   class="font-medium text-indigo-300 hover:text-indigo-200 cursor-pointer">
                  忘記密碼？
                </a>
              </div>
            </div>

            <div>
              <button type="submit" 
                      class="w-full py-3 px-4 border border-white/30
                             text-sm font-medium rounded-xl text-white 
                             bg-gradient-to-r from-indigo-500 to-purple-500
                             hover:from-indigo-600 hover:to-purple-600
                             backdrop-blur-sm transition-all duration-200
                             focus:outline-none focus:ring-2 
                             focus:ring-offset-2 focus:ring-indigo-500
                             shadow-lg shadow-indigo-500/30">
                {{ isLogin ? '登入' : '註冊' }}
              </button>
            </div>
          </form>

          <!-- 社群登入按鈕樣式調整 -->
          <div class="mt-6">
            <div class="relative">
              <div class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-gray-300 dark:border-gray-700 opacity-50"></div>
              </div>
              <div class="relative flex justify-center text-sm">
                <span class="px-4 text-gray-400">
                  或使用以下方式登入
                </span>
              </div>
            </div>

            <div class="mt-6 grid grid-cols-3 gap-3">
              <!-- Google 登入 -->
              <button
                @click="handleGoogleSignIn"
                class="w-full inline-flex justify-center items-center py-2 px-4 rounded-md shadow-sm 
                        bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700
                        text-white transition-all duration-200 transform hover:scale-105"
              >
                <i class="ri-google-line text-xl"></i>
              </button>

              <!-- Facebook 登入 -->
              <button
                @click="handleFacebookSignIn"
                class="w-full inline-flex justify-center items-center py-2 px-4 rounded-md shadow-sm 
                        bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700
                        text-white transition-all duration-200 transform hover:scale-105"
              >
                <i class="ri-messenger-line text-xl"></i>
              </button>

              <!-- GitHub 登入 -->
              <button
                @click="handleGithubSignIn"
                class="w-full inline-flex justify-center items-center py-2 px-4 rounded-md shadow-sm 
                        bg-gradient-to-r from-gray-700 to-gray-800 hover:from-gray-800 hover:to-gray-900
                        text-white transition-all duration-200 transform hover:scale-105"
              >
                <i class="ri-github-line text-xl"></i>
              </button>
            </div>
          </div>

          <!-- 切換登入/註冊按鈕 -->
          <div class="text-center mt-4 md:mt-6">
            <button @click="isLogin = !isLogin" 
                    class="text-sm text-white hover:text-indigo-200 transition-colors">
              {{ isLogin ? '還沒有帳號？立即註冊' : '已有帳號？立即登入' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 忘記密碼 Modal -->
    <div v-if="showForgotPasswordModal" 
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 px-4">
      <div class="bg-white rounded-lg p-6 md:p-8 max-w-md w-full mx-auto">
        <h3 class="text-xl font-bold mb-4">重設密碼</h3>
        <p class="text-gray-600 mb-4">請輸入您的 Email，我們將發送重設密碼連結給您。</p>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Email
          </label>
          <input type="email" 
                 v-model="forgotPasswordEmail"
                 class="w-full px-3 py-2 border border-gray-300 text-gray-700 rounded-lg focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
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
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'
import accountApi from '@/api/modules/account'
import { useAuthStore } from '@/stores/auth'
import { auth } from '@/config/firebase'
import { 
  GoogleAuthProvider, 
  FacebookAuthProvider,
  GithubAuthProvider,
  signInWithPopup,
  fetchSignInMethodsForEmail
} from 'firebase/auth'
import bannerApi from '@/api/modules/banner'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const isLogin = ref(true)
    const defaultAvatar = 'https://api.dicebear.com/9.x/bottts/svg?seed=Sara'
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

    const bannerData = ref({})

    const showPassword = ref(false)
    const showConfirmPassword = ref(false)
  

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
            const userData = response.data.user
            localStorage.setItem('token', response.data.token)
            localStorage.setItem('user', JSON.stringify(userData))
            console.log('保存的用戶信息:', response.data.user)
            
            await Swal.fire({
              icon: 'success',
              title: '登入成功',
              text: '歡迎回來',
              timer: 1500,
              showConfirmButton: false
            })

            // 判斷是否為管理員帳號
            // if (userData.username === 'MarkHSU') {
            //   localStorage.setItem('isAdmin', 'true')
            //   router.push('/admin')
            // } else {
            //   localStorage.setItem('isAdmin', 'false')
            //   router.push('/')
            // }
            router.push('/admin')
          }
        }
      } catch (error) {
        console.error('Login Error:', error)
        await Swal.fire({
          icon: 'error',
          title: '登入失敗',
          text: error.response?.data?.message || '請檢查您的帳號密碼',
          confirmButtonText: '確定'
        })
      }
    }

    const handleGoogleSignIn = async () => {
      try {
        const provider = new GoogleAuthProvider()
        provider.addScope('profile')
        provider.addScope('email')
        
        const result = await signInWithPopup(auth, provider)
        console.log('Google 登入結果:', result)  // 調試用
        
        const token = await result.user.getIdToken()
        console.log('Firebase token:', token)  // 調試用
        
        const response = await accountApi.firebaseLogin({
          token,
          provider: 'google'
        })
        
        console.log('後端回應:', response.data)  // 調試用
        
        if (response.data && response.data.token) {
          // 先設置 localStorage
          localStorage.setItem('token', response.data.token)
          localStorage.setItem('user', JSON.stringify(response.data.user))

          const userData = response.data.user
          
          // 更新 auth store
          await authStore.setAuth({
            token: response.data.token,
            user: response.data.user
          })

          // 判斷是否為管理員帳號
          // if (userData.username === '徐小彥') {
          //     localStorage.setItem('isAdmin', 'true')
          //     router.push('/admin')
          //   } else {
          //     localStorage.setItem('isAdmin', 'false')
          //     router.push('/')
          // }
          localStorage.setItem('isAdmin', 'true')
          router.push('/admin')
          
        } else {
          throw new Error('登入回應格式錯誤')
        }
        
      } catch (error) {
        console.error('Google 登入錯誤:', error)
        
        // 根據錯誤類型顯示不同的錯誤訊息
        let errorMessage = '使用 Google 登入時發生錯誤，請稍後再試'
        
        if (error.code === 'auth/popup-closed-by-user') {
          errorMessage = '登入視窗被關閉'
        } else if (error.code === 'auth/cancelled-popup-request') {
          errorMessage = '登入請求已取消'
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message
        }
        
        Swal.fire({
          icon: 'error',
          title: '登入失敗',
          text: errorMessage,
          confirmButtonText: '確定'
        })
      }
    }

    const handleFacebookSignIn = async () => {
      try {
        const provider = new FacebookAuthProvider()
        const result = await signInWithPopup(auth, provider)
        console.log('Facebook 登入結果:', result)  // 調試用
        
        const token = await result.user.getIdToken()
        console.log('Firebase token:', token)  // 調試用
        
        const response = await accountApi.firebaseLogin({
          token,
          provider: 'facebook'
        })
        
        console.log('Facebook 登入結果:', response.data)
        
        if (response.data && response.data.token) {
          // 先設置 localStorage
          localStorage.setItem('token', response.data.token)
          localStorage.setItem('user', JSON.stringify(response.data.user))
          
          const userData = response.data.user
          
          // 更新 auth store
          await authStore.setAuth({
            token: response.data.token,
            user: response.data.user
          })
          
          // 判斷是否為管理員帳號
          // if (userData.username === '徐小彥') {
          //   localStorage.setItem('isAdmin', 'true')
          //   router.push('/admin')
          // } else {
          //   localStorage.setItem('isAdmin', 'false')
          //   router.push('/')
          // }
          localStorage.setItem('isAdmin', 'true')
          router.push('/admin')
        } else {
          throw new Error('登入回應格式錯誤')
        }
        
      } catch (error) {
        console.error('Facebook 登入失敗:', error)
        
        // 根據錯誤類型顯示不同的錯誤訊息
        let errorMessage = '使用 Facebook 登入時發生錯誤，請稍後再試'
        
        if (error.code === 'auth/popup-closed-by-user') {
          errorMessage = '登入視窗被關閉'
        } else if (error.code === 'auth/cancelled-popup-request') {
          errorMessage = '登入請求已取消'
        } else if (error.code === 'auth/account-exists-with-different-credential') {
          errorMessage = '此 Email 已使用其他方式登入，請使用原有的登入方式'
        } else if (error.code === 'auth/user-disabled') {
          errorMessage = '此 Facebook 帳號已被系統停用，請聯繫管理員或使用其他方式登入'
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message
        }
        
        Swal.fire({
          icon: 'error',
          title: '登入失敗',
          text: errorMessage,
          confirmButtonText: '確定'
        })
      }
    }

    const handleGithubSignIn = async () => {
      try {
        const provider = new GithubAuthProvider()
        provider.addScope('user:email')
        
        const result = await signInWithPopup(auth, provider)
        console.log('GitHub 登入結果:', result.user)
        
        if (result) {
          try {
            const token = await result.user.getIdToken()
            console.log('Firebase token:', token)
            
            // 準備要傳給後端的用戶資料
            const userData = {
              username: result.user.displayName || result.user.email.split('@')[0],
              email: result.user.email,
              avatar: result.user.photoURL,
              provider: 'github',
              status: 'Enabled',
              uid: result.user.uid  // 添加 Firebase UID
            }
            console.log('準備發送給後端的用戶資料:', userData)
            
            // 呼叫後端 API 進行登入或註冊
            const response = await accountApi.firebaseLogin({
              token: token,
              provider: 'github',
              userData: userData
            })
            console.log('後端回應:', response.data)
            
            if (response.data && response.data.token) {
              // 確保資料正確存儲
              localStorage.setItem('token', response.data.token)
              localStorage.setItem('user', JSON.stringify(response.data.user))
              console.log('已存儲用戶資料:', response.data.user)
              
              await authStore.setAuth(response.data)
              
              // 判斷是否為管理員帳號
              // if (response.data.user.username === '徐小彥') {
              //   localStorage.setItem('isAdmin', 'true')
              //   console.log('管理員登入，準備跳轉到後台')
              //   router.push('/admin')
              // } else {
              //   localStorage.setItem('isAdmin', 'false')
              //   console.log('一般用戶登入，準備跳轉到首頁')
              //   router.push('/')
              // }
              localStorage.setItem('isAdmin', 'true')
              router.push('/admin')
              // 顯示登入成功訊息
              await Swal.fire({
                icon: 'success',
                title: '登入成功',
                text: `歡迎回來，${response.data.user.username}！`,
                timer: 1500,
                showConfirmButton: false
              })
            } else {
              console.error('後端回應缺少必要資料')
              throw new Error('登入回應格式錯誤')
            }
          } catch (error) {
            // 處理特定的 Firebase 錯誤
            if (error.code === 'auth/user-disabled') {
              Swal.fire({
                icon: 'error',
                title: '帳號已被停用',
                text: '此 GitHub 帳號已被系統停用，請聯繫管理員或使用其他方式登入',
                confirmButtonText: '確定'
              })
              return
            }
            
            if (error.code === 'auth/account-exists-with-different-credential') {
              const methods = await fetchSignInMethodsForEmail(auth, result.user.email)
              
              Swal.fire({
                icon: 'warning',
                title: '此 Email 已被使用',
                text: `請使用 ${methods.join(', ')} 登入`,
                confirmButtonText: '確定'
              })
            } else {
              throw error
            }
          }
        }
      } catch (error) {
        console.error('GitHub 登入錯誤:', error)
        let errorMessage = '使用 GitHub 登入時發生錯誤，請稍後再試'
        
        if (error.code === 'auth/popup-closed-by-user') {
          errorMessage = '登入視窗被關閉'
        } else if (error.code === 'auth/cancelled-popup-request') {
          errorMessage = '登入請求已取消'
        } else if (error.code === 'auth/account-exists-with-different-credential') {
          errorMessage = '此 Email 已使用其他方式登入，請使用原有的登入方式'
        } else if (error.code === 'auth/user-disabled') {
          errorMessage = '此 GitHub 帳號已被系統停用，請聯繫管理員或使用其他方式登入'
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message
        }
        
        Swal.fire({
          icon: 'error',
          title: '登入失敗',
          text: errorMessage,
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

    const fetchBannerData = async () => {
      try {
        const response = await bannerApi.getBannersByType('login')
        if (response.data?.data?.length > 0) {
          bannerData.value = response.data.data[0]
        }
      } catch (error) {
        console.error('獲取登入頁面數據失敗:', error)
      }
    }

    // 初始化暗色模式
    onMounted(() => {
      // 檢查本地存儲的主題設置
      if (localStorage.theme === 'dark' || 
          (!('theme' in localStorage) && 
           window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }

      fetchBannerData()
    })

    return {
      isLogin,
      form,
      errors,
      defaultAvatar,
      avatarPreview,
      avatarFile,
      handleAvatarChange,
      handleSubmit,
      showForgotPasswordModal,
      forgotPasswordEmail,
      handleForgotPassword,
      handleGoogleSignIn,
      handleFacebookSignIn,
      handleGithubSignIn,
      bannerData,
      showPassword,
      showConfirmPassword
    }
  }
}
</script>

<style scoped>
/* 輸入框 placeholder 顏色調整 */
::placeholder {
  color: rgba(255, 255, 255, 0.6);
}


/* 輸入框自動填充樣式 */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {
  -webkit-text-fill-color: white;
  -webkit-box-shadow: 0 0 0px 1000px rgba(255, 255, 255, 0.2) inset;
  transition: background-color 5000s ease-in-out 0s;
}

/* 調整錯誤提示文字顏色 */
.text-red-500 {
  color: rgb(252, 165, 165);
}

/* 調整必填星號顏色 */
.text-red-500 {
  color: rgb(252, 165, 165);
}

/* 調整 checkbox 樣式 */
input[type="checkbox"] {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

input[type="checkbox"]:checked {
  background-color: rgb(99, 102, 241);
  border-color: rgb(99, 102, 241);
}

/* 漸變背景效果 */
.bg-gradient-custom {
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
}

/* 玻璃擬態效果 */
.glassmorphism {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}


/* 確保背景圖片在所有設備上都能完整顯示 */
.absolute.inset-0 img {
  object-fit: cover;
  width: 100%;
  height: 100%;
}

/* 優化手機版的觸控體驗 */
@media (hover: none) {
  button, a {
    -webkit-tap-highlight-color: transparent;
  }
}

/* 調整玻璃擬態效果在手機版的表現 */
@supports (-webkit-backdrop-filter: none) or (backdrop-filter: none) {
  .backdrop-blur-sm {
    -webkit-backdrop-filter: blur(8px);
    backdrop-filter: blur(8px);
  }
}

/* 眼睛圖標的過渡效果 */
.ri-eye-line,
.ri-eye-off-line {
  transition: opacity 0.2s;
}

/* 眼睛按鈕懸停效果 */
button:hover .ri-eye-line,
button:hover .ri-eye-off-line {
  opacity: 1;
}
</style> 