<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 py-12 px-4 sm:px-6 lg:px-8 flex items-center">
    <div class="max-w-md w-full mx-auto space-y-8 bg-white rounded-2xl shadow-xl p-8">
      <!-- Logo -->
      <div class="text-center">
        <i class="fas fa-key text-6xl text-indigo-600"></i>
        <h2 class="mt-6 text-3xl font-extrabold text-gray-900">
          重設密碼
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          請輸入新密碼
        </p>
      </div>

      <!-- 表單 -->
      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div class="rounded-md shadow-sm space-y-4">
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              新密碼 <span class="text-red-500">*</span>
            </label>
            <input id="password" 
                   v-model="form.password" 
                   type="password" 
                   required
                   :class="{'border-red-500': errors.password}"
                   class="appearance-none relative block w-full px-3 py-2 border border-gray-300 
                          placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none 
                          focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                   placeholder="請輸入新密碼">
            <p v-if="errors.password" class="mt-1 text-xs text-red-500">{{ errors.password }}</p>
            <p class="mt-1 text-xs text-gray-500">密碼需要6-12碼，包含大小寫字母、數字及特殊符號</p>
          </div>

          <div>
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
                   placeholder="請再次輸入新密碼">
            <p v-if="errors.confirmPassword" class="mt-1 text-xs text-red-500">{{ errors.confirmPassword }}</p>
          </div>
        </div>

        <div>
          <button type="submit" 
                  class="group relative w-full flex justify-center py-2 px-4 border border-transparent 
                         text-sm font-medium rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 
                         focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <i class="fas fa-key text-indigo-500 group-hover:text-indigo-400"></i>
            </span>
            重設密碼
          </button>
        </div>
      </form>
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
      handleSubmit
    }
  }
}
</script> 