<template>
  <div>
    <!-- 無資料時顯示 -->
    <div v-if="!accounts || accounts.length === 0" 
         class="bg-white rounded-lg shadow-sm p-8 text-center">
      <div class="text-gray-500 mb-4">
        <i class="fas fa-users text-4xl"></i>
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">
        尚無帳號資料
      </h3>
      <p class="text-gray-500 mb-4">
        目前還沒有任何使用者帳號，點擊下方按鈕新增帳號。
      </p>
      <button @click="showAddModal = true"
              class="inline-flex items-center px-4 py-2 bg-blue-50 text-blue-600 rounded-md hover:bg-blue-100 transition-colors duration-200">
        <i class="fas fa-plus mr-2"></i>
        新增帳號
      </button>
    </div>

    <!-- 有資料時顯示表格 -->
    <div v-else>
      <DataTable
      :columns="columns"
      :data="accounts"
      :showAddButton="true"
      :selectable="true"
      @add="showAddModal = true"
      @edit="editAccount"
      @delete="deleteAccount"
      @batch-delete="batchDeleteAccounts">
        <!-- 自定義頭像列 -->
        <template #avatar="{ item }">
          <img :src="item.avatar || defaultAvatar" 
               class="w-10 h-10 rounded-full">
        </template>
        <!-- 自定義狀態列 -->
        <template #status="{ item }">

          <span :class="[
            'px-2 py-1 text-xs rounded-full',
            item.status === 'Enabled' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          ]">
            {{ item.status }}
          </span>
        </template>
      </DataTable>
    </div>

    <!-- 新增/編輯帳號彈窗 -->
    <div v-if="showAddModal" 
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white rounded-xl p-8 w-full max-w-md">
        <h2 class="text-xl font-bold mb-6">{{ editingAccount ? '編輯帳號' : '新增帳號' }}</h2>
        <div class="space-y-4">
          <!-- 頭像上傳 -->
          <div class="flex items-center space-x-4">
            <img :src="previewAvatar || defaultAvatar" 
                 class="w-20 h-20 rounded-full object-cover border-2 border-gray-200">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">頭像</label>
              <input type="file" 
                     @change="handleAvatarChange" 
                     accept="image/*"
                     class="block w-full text-sm text-gray-500
                            file:mr-4 file:py-2 file:px-4
                            file:rounded-full file:border-0
                            file:text-sm file:font-semibold
                            file:bg-blue-50 file:text-blue-700
                            hover:file:bg-blue-100">
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">帳號名稱</label>
            <input type="text" 
                   v-model="accountForm.username" 
                   :class="{'border-red-500': errors.username}"
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
            <span v-if="errors.username" class="text-red-500 text-xs mt-1">{{ errors.username }}</span>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input type="email" 
                   v-model="accountForm.email" 
                   :class="{'border-red-500': errors.email}"
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
            <span v-if="errors.email" class="text-red-500 text-xs mt-1">{{ errors.email }}</span>
          </div>
          <div v-if="!editingAccount">
            <label class="block text-sm font-medium text-gray-700 mb-2">密碼</label>
            <input type="password" 
                   v-model="accountForm.password"
                   :class="{'border-red-500': errors.password}"
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
            <span v-if="errors.password" class="text-red-500 text-xs mt-1">{{ errors.password }}</span>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">狀態</label>
            <select v-model="accountForm.status" 
                    :class="{'border-red-500': errors.status}"
                    class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
              <option value="Enabled">啟用</option>
              <option value="Disabled">停用</option>
            </select>
            <span v-if="errors.status" class="text-red-500 text-xs mt-1">{{ errors.status }}</span>
          </div>
        </div>
        <div class="mt-8 flex justify-end space-x-4">
          <button @click="closeModal" 
                  class="px-4 py-2 text-gray-700 border rounded-lg hover:bg-gray-50">
            取消
          </button>
          <button @click="saveAccount" 
                  class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
            確認
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import DataTable from '../common/DataTable.vue'
import axios from '@/utils/axios'
import Swal from 'sweetalert2'
import { useRouter } from 'vue-router'
import { useLogger } from '@/composables/useLogger'

export default {
  name: 'AccountManagement',
  components: {
    DataTable
  },
  setup() {
    const router = useRouter()
    const accounts = ref([])
    const showAddModal = ref(false)
    const { logOperation } = useLogger()
    const currentUser = ref(JSON.parse(localStorage.getItem('user') || '{}'))

    return { router, accounts, showAddModal, logOperation, currentUser }
  },
  data() {
    return {
      columns: [
        { key: 'avatar', label: '頭像' },
        { key: 'username', label: '帳號名稱' },
        { key: 'email', label: '電子郵件' },
        { key: 'created_at', label: '註冊時間' },
        { key: 'updated_at', label: '更新時間' },
        { key: 'status', label: '狀態' }
      ],
      editingAccount: null,
      accountForm: {
        username: '',
        email: '',
        password: '',
        status: 'Enabled'
      },
      defaultAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=default',
      previewAvatar: null,
      avatarFile: null,
      errors: {
        username: '',
        email: '',
        password: '',
        status: ''
      }
    }
  },
  async created() {
    await this.fetchAccounts()
    // 記錄訪問帳號管理頁面
    await this.logOperation('【帳號管理】訪問帳號管理頁面', '查看')
  },
  methods: {
    async fetchAccounts() {
      try {
        const token = localStorage.getItem('token')
        console.log('從 AccountManagement 獲取的 token:', token)
        console.log('從 AccountManagement 獲取的 backend_url:', import.meta.env.VITE_BACKEND_URL)
        if (!token) {
          Swal.fire({
            icon: 'warning',
            title: '請先登入',
            text: '您需要登入才能查看用戶列表',
            confirmButtonText: '確定'
          })
          this.router.push('/login')
          return
        }

        const response = await axios.get('/users/')
        console.log('useravatar', response.data.users[1].avatar)
        this.accounts = response.data.users.map(user => ({
          
          id: user.id,
          username: user.username,
          email: user.email,
          avatar: user.avatar 
            ? `${import.meta.env.VITE_BACKEND_URL}/api/users/avatar/${user.avatar.split('/').pop()}`
            : 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + user.username,  // 使用用戶名作為種子生成預設頭像
          created_at: user.register_time,
          updated_at: user.update_time,
          status: user.status
        }))
      } catch (error) {
        // 如果是 401 錯誤，表示 token 無效或過期
        if (error.response?.status === 401) {
          localStorage.removeItem('token')
          Swal.fire({
            icon: 'warning',
            title: '登入已過期',
            text: '請重新登入',
            confirmButtonText: '確定'
          }).then(() => {
            this.router.push('/login')
          })
          return
        }
        
        console.error('獲取用戶列表失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '獲取用戶列表失敗',
          text: error.response?.data?.message || '請稍後再試',
          confirmButtonText: '確定'
        })
      }
    },
    showAddForm() {
      this.editingAccount = null
      this.accountForm = {
        username: '',
        email: '',
        password: '',
        status: 'Enabled'
      }
      this.resetAvatarForm()
      this.showAddModal = true
    },
    editAccount(account) {
      this.editingAccount = account
      this.accountForm = {
        username: account.username,
        email: account.email,
        status: account.status,
        password: ''
      }
      if (account.avatar && !account.avatar.includes('dicebear')) {
        this.previewAvatar = account.avatar
      } else {
        this.previewAvatar = null
      }
      this.showAddModal = true
    },
    async deleteAccount(account) {
      // 檢查是否為當前登入帳號
      if (account.username === this.currentUser.username) {
        Swal.fire({
          icon: 'error',
          title: '無法刪除當前帳號',
          text: '為了系統安全，不能刪除您正在使用的帳號',
          confirmButtonText: '確定'
        })
        return
      }

      const result = await Swal.fire({
        title: '確定要刪除嗎？',
        text: '此操作無法復原',
        html: `
          <div class="text-left">
            <p class="mb-2">即將刪除以下帳號：</p>
            <ul class="list-disc pl-5">
              <li>${account.username} (${account.email})</li>
            </ul>
          </div>
        `,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '確定刪除',
        cancelButtonText: '取消',
        confirmButtonColor: '#dc2626'
      })

      if (result.isConfirmed) {
        try {
          await axios.delete(`/users/${account.id}`)
          await this.fetchAccounts()
          await this.logOperation(`【帳號管理】刪除帳號 ${account.username}`, '刪除')
          Swal.fire({
            icon: 'success',
            title: '刪除成功',
            timer: 1500,
            showConfirmButton: false
          })
        } catch (error) {
          Swal.fire({
            icon: 'error',
            title: '刪除失敗',
            text: error.response?.data?.message || '請稍後再試',
            confirmButtonText: '確定'
          })
        }
      }
    },
    async batchDeleteAccounts(ids) {
      if (!ids || ids.length === 0) {
        Swal.fire({
          icon: 'warning',
          title: '請選擇要刪除的帳號',
          text: '您尚未選擇任何帳號',
          confirmButtonText: '確定'
        })
        return
      }

      // 檢查是否包含當前登入帳號
      const selectedAccounts = this.accounts.filter(account => ids.includes(account.id))
      const hasCurrentUser = selectedAccounts.some(account => account.username === this.currentUser.username)
      
      if (hasCurrentUser) {
        Swal.fire({
          icon: 'error',
          title: '無法刪除當前帳號',
          text: '為了系統安全，不能刪除您正在使用的帳號',
          confirmButtonText: '確定'
        })
        return
      }

      const result = await Swal.fire({
        title: `確定要刪除選中的 ${ids.length} 個帳號嗎？`,
        text: '此操作無法復原',
        html: `
          <div class="text-left">
            <p class="mb-2">即將刪除以下帳號：</p>
            <ul class="list-disc pl-5">
              ${selectedAccounts.map(account => `
                <li>${account.username} (${account.email})</li>
              `).join('')}
            </ul>
          </div>
        `,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '確定刪除',
        cancelButtonText: '取消',
        confirmButtonColor: '#dc2626'
      })

      if (result.isConfirmed) {
        try {
          // 過濾掉當前用戶的ID
          const idsToDelete = ids.filter(id => {
            const account = this.accounts.find(a => a.id === id)
            return account.username !== this.currentUser.username
          })
          
          // 使用 Promise.all 並行處理刪除請求
          await Promise.all(idsToDelete.map(id => axios.delete(`/users/${id}`)))

          await this.fetchAccounts()
          await this.logOperation(`【帳號管理】批量刪除帳號 (${ids.length} 筆)`, '刪除')
          Swal.fire({
            icon: 'success',
            title: '批量刪除成功',
            timer: 1500,
            showConfirmButton: false
          })
        } catch (error) {
          console.error('批量刪除失敗:', error)
          Swal.fire({
            icon: 'error',
            title: '批量刪除失敗',
            text: '刪除過程中發生錯誤，請稍後再試',
            confirmButtonText: '確定'
          })
        }
      }
    },
    validateForm() {
      this.errors = {
        username: '',
        email: '',
        password: '',
        status: ''
      }
      
      let isValid = true
      
      // 驗證用戶名
      if (!this.accountForm.username) {
        this.errors.username = '請輸入帳號名稱'
        isValid = false
      } else if (this.accountForm.username.length < 2) {
        this.errors.username = '帳號名稱至少需要2個字符'
        isValid = false
      }
      
      // 驗證郵箱
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!this.accountForm.email) {
        this.errors.email = '請輸入電子郵件'
        isValid = false
      } else if (!emailRegex.test(this.accountForm.email)) {
        this.errors.email = '請輸入有效的電子郵件地址'
        isValid = false
      }
      
      // 新增時驗證密碼
      if (!this.editingAccount) {
        if (!this.accountForm.password) {
          this.errors.password = '請輸入密碼'
          isValid = false
        } else if (this.accountForm.password.length < 6) {
          this.errors.password = '密碼至少需要6個字符'
          isValid = false
        }
      }
      
      // 驗證狀態
      if (!this.accountForm.status) {
        this.errors.status = '請選擇狀態'
        isValid = false
      }
      
      return isValid
    },
    async saveAccount() {
      try {
        if (!this.validateForm()) {
          return
        }
        
        let avatarPath = ''
        
        // 如果有選擇頭像，先上傳
        if (this.avatarFile) {
          const token = localStorage.getItem('token')
          if (!token) {
            Swal.fire({
              icon: 'error',
              title: '上傳失敗',
              text: '請先登入',
              confirmButtonText: '確定'
            })
            this.router.push('/login')
            return
          }
          
          try {
            console.log('準備上傳的檔案:', this.avatarFile)
            const formData = new FormData()
            formData.append('file', this.avatarFile)
            const response = await axios.post('/users/avatar', formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': `Bearer ${token}`
              }
            })
            console.log('上傳回應:', response.data)
            if (response.data && response.data.avatar_url) {
              avatarPath = response.data.avatar_url
            } else if (response.data && response.data.avatar_path) {
              avatarPath = response.data.avatar_path
            } else {
              throw new Error('上傳回應中缺少頭像路徑')
            }
            console.log('取得的頭像路徑:', avatarPath)
          } catch (error) {
            console.error('上傳錯誤:', error)
            console.error('上傳回應:', error.response?.data)
            // 如果是 401 錯誤，表示 token 無效或過期
            if (error.response?.status === 401) {
              localStorage.removeItem('token')
              Swal.fire({
                icon: 'warning',
                title: '登入已過期',
                text: '請重新登入',
                confirmButtonText: '確定'
              }).then(() => {
                this.router.push('/login')
              })
              return
            }
            
            console.error('頭像上傳失敗:', error)
            Swal.fire({
              icon: 'error',
              title: '頭像上傳失敗',
              text: error.response?.data?.message || '請稍後再試',
              confirmButtonText: '確定'
            })
            return
          }
        }

        let data = {
          username: this.accountForm.username,
          email: this.accountForm.email,
          status: this.accountForm.status
        }
        
        // 只在新增時添加密碼
        if (!this.editingAccount) {
          data.password = this.accountForm.password
        }

        if (this.editingAccount) {
          await axios.put(`/users/${this.editingAccount.id}`, data)
          await this.fetchAccounts()
          await this.logOperation(`【帳號管理】編輯帳號 ${this.editingAccount.username}`, '修改')
          
          Swal.fire({
            icon: 'success',
            title: '更新成功',
            timer: 1500,
            showConfirmButton: false
          })
        } else {
          const registerData = {
            username: this.accountForm.username,
            email: this.accountForm.email,
            password: this.accountForm.password,
            confirm_password: this.accountForm.password,
            status: this.accountForm.status
          }
          
          // 1. 先進行註冊
          const registerResponse = await axios.post('/users/register', registerData)
          console.log('註冊回應:', registerResponse.data)
          
          // 2. 如果有頭像且註冊成功，再上傳頭像
          if (registerResponse.status === 201 && this.avatarFile) {
            // 儲存註冊返回的 token
            localStorage.setItem('token', registerResponse.data.token)

            try {
              const formData = new FormData()
              formData.append('file', this.avatarFile)
              
              const avatarResponse = await axios.post('/users/avatar', formData, {
                headers: {
                  'Content-Type': 'multipart/form-data',
                  'Authorization': `Bearer ${registerResponse.data.token}`
                }
              })
              console.log('頭像上傳回應:', avatarResponse.data)
            } catch (error) {
              console.error('頭像上傳失敗:', error)
              Swal.fire({
                icon: 'warning',
                title: '頭像上傳失敗',
                text: '帳號已創建，但頭像上傳失敗',
                confirmButtonText: '確定'
              })
            }
          }

          await this.fetchAccounts()
          await this.logOperation(`【帳號管理】新增帳號 ${this.accountForm.username}`, '新增')
          
          Swal.fire({
            icon: 'success',
            title: '新增成功',
            timer: 1500,
            showConfirmButton: false
          })
        }
        
        // 成功後才關閉模態框和重置表單
        this.showAddModal = false
        this.editingAccount = null
        this.accountForm = {
          username: '',
          email: '',
          password: '',
          status: 'Enabled'
        }
        this.resetAvatarForm()
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: this.editingAccount ? '更新失敗' : '新增失敗',
          text: error.response?.data?.message || '請稍後再試',
          confirmButtonText: '確定'
        })
      }
    },
    handleAvatarChange(event) {
      const file = event.target.files[0]
      if (file) {
        this.avatarFile = file
        this.previewAvatar = URL.createObjectURL(file)
      }
    },
    resetAvatarForm() {
      this.previewAvatar = null
      this.avatarFile = null
    },
    resetForm() {
      this.accountForm = {
        username: '',
        email: '',
        password: '',
        status: 'Enabled'
      }
      this.editingAccount = null
      this.showAddModal = false
      this.resetAvatarForm()
    },
    closeModal() {
      this.showAddModal = false
      this.resetForm()
    }
  }
}
</script> 