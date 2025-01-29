<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 py-12 px-4 sm:px-6 lg:px-8 flex items-center">
    <div class="max-w-md w-full mx-auto space-y-8 bg-white rounded-2xl shadow-xl p-8">
      <!-- Logo -->
      <div class="text-center">
        <img class="mx-auto h-16 w-auto" src="https://api.dicebear.com/7.x/bottts/svg?seed=food" alt="Logo">
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
          <div v-if="!isLogin">
            <label for="name" class="block text-sm font-medium text-gray-700">名稱</label>
            <input id="name" v-model="form.name" type="text" required 
                   class="appearance-none relative block w-full px-3 py-2 border border-gray-300 
                          placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none 
                          focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                   placeholder="請輸入您的名稱">
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
            <input id="email" v-model="form.email" type="email" required
                   class="appearance-none relative block w-full px-3 py-2 border border-gray-300 
                          placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none 
                          focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                   placeholder="請輸入Email">
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">密碼</label>
            <input id="password" v-model="form.password" type="password" required
                   class="appearance-none relative block w-full px-3 py-2 border border-gray-300 
                          placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none 
                          focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                   placeholder="請輸入密碼">
          </div>

          <div v-if="!isLogin">
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700">確認密碼</label>
            <input id="confirmPassword" v-model="form.confirmPassword" type="password" required
                   class="appearance-none relative block w-full px-3 py-2 border border-gray-300 
                          placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none 
                          focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                   placeholder="請再次輸入密碼">
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
            <a href="#" class="font-medium text-indigo-600 hover:text-indigo-500">
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
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const isLogin = ref(true)
    const form = reactive({
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
      remember: false
    })

    const handleSubmit = async () => {
      try {
        if (!isLogin.value && form.password !== form.confirmPassword) {
          alert('兩次輸入的密碼不一致')
          return
        }

        // TODO: 實作登入/註冊邏輯
        console.log('Form submitted:', form)
        
        // 模擬登入成功
        router.push('/admin/dashboard')
      } catch (error) {
        console.error('Error:', error)
        alert('發生錯誤，請稍後再試')
      }
    }

    const socialLogin = async (provider) => {
      try {
        // TODO: 實作社群登入邏輯
        console.log('Social login with:', provider)
      } catch (error) {
        console.error('Error:', error)
        alert('社群登入失敗，請稍後再試')
      }
    }

    return {
      isLogin,
      form,
      handleSubmit,
      socialLogin
    }
  }
}
</script> 