import { defineStore } from 'pinia'
import { auth } from '@/config/firebase'
import { signOut } from 'firebase/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    user: null,
    isAuthenticated: false
  }),

  actions: {
    async setAuth(data) {
      if (!data || !data.token || !data.user) {
        throw new Error('Invalid auth data')
      }
      
      this.token = data.token
      this.user = data.user
      this.isAuthenticated = true
    },
    
    async clearAuth() {
      try {
        // 先登出 Firebase
        await signOut(auth)
        console.log('Firebase 登出成功')
      } catch (error) {
        console.error('Firebase 登出錯誤:', error)
      } finally {
        // 清除本地狀態
        this.token = null
        this.user = null
        this.isAuthenticated = false
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        localStorage.removeItem('isAdmin')
      }
    }
  },

  getters: {
    getUser: (state) => state.user,
    getLoginStatus: (state) => state.isAuthenticated
  }
}) 