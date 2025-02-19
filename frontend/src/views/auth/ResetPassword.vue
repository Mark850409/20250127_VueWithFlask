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
        <div class="w-full md:w-1/2 transition-transform duration-500 p-8 md:p-16">
          <div class="text-white space-y-6 md:space-y-8">
            <!-- Logo 和標題區域 -->
            <div class="text-center space-y-4 md:space-y-6">
              <i class="ri-key-2-line text-5xl md:text-7xl text-white"></i>
              <h2 class="text-3xl md:text-5xl font-extrabold tracking-wide text-white drop-shadow-lg">
                重設密碼
              </h2>
              <p class="text-lg md:text-xl text-white drop-shadow-md">
                請輸入新密碼
              </p>
            </div>
            
            <!-- 關於密碼重設的說明 -->
            <div class="mt-6 md:mt-12 space-y-4 text-center">
              <p class="text-base md:text-lg text-white text-left drop-shadow-md leading-relaxed">
                為了確保您的帳戶安全，請設定一個強度足夠的新密碼。建議使用包含大小寫字母、數字和特殊符號的組合。
              </p>
            </div>
          </div>
        </div>

        <!-- 右側表單區域 -->
        <div class="w-full md:w-1/2 transition-transform duration-500 p-6 md:p-8 backdrop-blur-sm bg-white/10 rounded-2xl mt-6 md:mt-0">
          <!-- 表單內容 -->
          <form class="space-y-4" @submit.prevent="handleSubmit">
            <div class="rounded-md shadow-sm space-y-3">
              <div>
                <label for="password" class="block text-sm font-medium text-white/90">
                  新密碼 <span class="text-red-500">*</span>
                </label>
                <div class="relative">
                  <input id="password" 
                         v-model="form.password" 
                         :type="showPassword ? 'text' : 'password'"
                         required
                         :class="{'border-red-500': errors.password}"
                         class="appearance-none relative block w-full px-3 py-2 
                                border border-white/30 bg-white/20 backdrop-blur-md
                                placeholder-gray-300 text-white rounded-xl
                                focus:outline-none focus:ring-2 focus:ring-indigo-400 
                                focus:border-transparent transition-all duration-200
                                hover:bg-white/30"
                         placeholder="請輸入新密碼">
                  <button type="button"
                          @click="showPassword = !showPassword"
                          class="absolute inset-y-0 right-0 pr-3 flex items-center text-white/70 hover:text-white/90">
                    <i :class="[showPassword ? 'ri-eye-line' : 'ri-eye-off-line']"></i>
                  </button>
                </div>
                <p v-if="errors.password" class="mt-1 text-xs text-red-300">
                  {{ errors.password }}
                </p>
                <p class="mt-1 text-xs text-white/80">
                  密碼需要6-12碼，包含大小寫字母、數字及特殊符號
                </p>
              </div>

              <div>
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
                         placeholder="請再次輸入新密碼">
                  <button type="button"
                          @click="showConfirmPassword = !showConfirmPassword"
                          class="absolute inset-y-0 right-0 pr-3 flex items-center text-white/70 hover:text-white/90">
                    <i :class="[showConfirmPassword ? 'ri-eye-line' : 'ri-eye-off-line']"></i>
                  </button>
                </div>
                <p v-if="errors.confirmPassword" class="mt-1 text-xs text-red-500">
                  {{ errors.confirmPassword }}
                </p>
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
                <i class="ri-key-2-line mr-2"></i>
                重設密碼
              </button>
            </div>

            <!-- 返回登入頁面 -->
            <div class="text-center mt-4 md:mt-6">
              <router-link to="/login" 
                          class="text-sm text-white hover:text-indigo-200 transition-colors">
                返回登入頁面
              </router-link>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import accountApi from '@/api/modules/account'
import Swal from 'sweetalert2'

export default {
  name: 'ResetPassword',
  
  beforeRouteEnter(to, from, next) {
    // 在進入路由前驗證 token
    const token = to.params.token
    accountApi.verifyResetToken(token)
      .then(() => {
        next()
      })
      .catch(() => {
        next({
          name: 'NotFound',
          params: { 
            message: '重設密碼連結已過期，請重新申請' 
          }
        })
      })
  },
  
  setup() {
    const route = useRoute()
    const router = useRouter()
    const token = route.params.token

    const form = reactive({
      password: '',
      confirmPassword: ''
    })

    const errors = reactive({
      password: '',
      confirmPassword: ''
    })

    // 添加密碼可見性控制
    const showPassword = ref(false)
    const showConfirmPassword = ref(false)

    const validatePassword = (password) => {
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
      errors.password = ''
      errors.confirmPassword = ''

      const passwordValidation = validatePassword(form.password)
      if (!passwordValidation.isValid) {
        errors.password = passwordValidation.errors.join('、')
        isValid = false
      }

      if (form.password !== form.confirmPassword) {
        errors.confirmPassword = '兩次輸入的密碼不一致'
        isValid = false
      }

      return isValid
    }

    const handleSubmit = async () => {
      try {
        if (!validateForm()) {
          return
        }

        await accountApi.resetPassword(token, form.password)

        await Swal.fire({
          icon: 'success',
          title: '密碼重設成功',
          text: '請使用新密碼登入',
          confirmButtonText: '確定'
        })
        router.push('/login')
      } catch (error) {
        console.error('Reset Password Error:', error)
        let errorMessage = '重設密碼失敗'
        if (error.response?.status === 404) {
          errorMessage = '找不到用戶'
        } else if (error.response?.status === 400) {
          const message = error.response.data.message
          if (message.includes('新密碼不能與最近')) {
            errorMessage = message
          } else {
            router.push({ 
              name: 'NotFound',
              params: { 
                message: '重設密碼連結已過期，請重新申請' 
              }
            })
            return
          }
        } else if (error.response?.status === 500) {
          errorMessage = '服務器錯誤，請稍後再試'
        }
        
        await Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: errorMessage,
          confirmButtonText: '確定'
        })
        
        if (error.response?.status === 400) {
          router.push('/login')
        }
      }
    }

    return {
      form,
      errors,
      handleSubmit,
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

/* 手機版特定樣式 */
@media (max-width: 768px) {
  .min-h-screen {
    min-height: 100vh;
    padding: 1rem 0;
  }

  /* 調整輸入框在手機版的大小 */
  input {
    font-size: 16px; /* 防止 iOS 自動縮放 */
  }

  /* 調整錯誤提示文字在手機版的大小 */
  .text-xs {
    font-size: 0.7rem;
  }

  /* 調整密碼提示文字在手機版的大小 */
  .text-sm {
    font-size: 0.8rem;
  }
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

/* 添加眼睛圖標的過渡效果 */
.ri-eye-line,
.ri-eye-off-line {
  transition: opacity 0.2s;
}

/* 眼睛按鈕懸停效果 */
button:hover .ri-eye-line,
button:hover .ri-eye-off-line {
  opacity: 1;
}

/* 調整手機版按鈕大小 */
@media (max-width: 768px) {
  .ri-eye-line,
  .ri-eye-off-line {
    font-size: 1.1rem;
  }
  
  button.absolute {
    padding: 0.5rem;
  }
}
</style> 