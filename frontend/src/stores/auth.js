import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: false,
    user: null
  }),

  actions: {
    setLoginStatus(status) {
      this.isLoggedIn = status
    },

    setUser(user) {
      this.user = user
    },

    logout() {
      this.isLoggedIn = false
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  },

  getters: {
    getUser: (state) => state.user,
    getLoginStatus: (state) => state.isLoggedIn
  }
}) 