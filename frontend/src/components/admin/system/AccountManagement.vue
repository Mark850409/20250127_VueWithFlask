<template>
  <div>
    <DataTable
      :columns="columns"
      :data="accounts"
      @add="showAddForm"
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
          <button @click="showAddModal = false" 
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
import DataTable from '../common/DataTable.vue'
import axios from '@/utils/axios'
import Swal from 'sweetalert2'
import { useRouter } from 'vue-router'

export default {
  name: 'AccountManagement',
  components: {
    DataTable
  },
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
      columns: [
        { key: 'avatar', label: '頭像' },
        { key: 'username', label: '帳號名稱' },
        { key: 'email', label: '電子郵件' },
        { key: 'registerTime', label: '註冊時間' },
        { key: 'updateTime', label: '更新時間' },
        { key: 'status', label: '狀態' }
      ],
      accounts: [],
      showAddModal: false,
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
  },
  methods: {
    async fetchAccounts() {
      try {
        const token = localStorage.getItem('token')
        console.log('從 AccountManagement 獲取的 token:', token)
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
        
        this.accounts = response.data.users.map(user => ({
          id: user.id,
          username: user.username,
          email: user.email,
          avatar: user.avatar 
            ? `${import.meta.env.VITE_BACKEND_URL}/api/users/avatar/${user.avatar.split('/').pop()}`
            : 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + user.username,  // 使用用戶名作為種子生成預設頭像
          registerTime: user.register_time,
          updateTime: user.update_time,
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
      const result = await Swal.fire({
        title: '確定要刪除此帳號嗎？',
        text: '此操作無法復原',
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
      const result = await Swal.fire({
        title: `確定要刪除選中的 ${ids.length} 個帳號嗎？`,
        text: '此操作無法復原',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '確定刪除',
        cancelButtonText: '取消',
        confirmButtonColor: '#dc2626'
      })

      if (result.isConfirmed) {
        try {
          await Promise.all(ids.map(id => axios.delete(`/users/${id}`)))
          await this.fetchAccounts()
          Swal.fire({
            icon: 'success',
            title: '批量刪除成功',
            timer: 1500,
            showConfirmButton: false
          })
        } catch (error) {
          Swal.fire({
            icon: 'error',
            title: '批量刪除失敗',
            text: error.response?.data?.message || '請稍後再試',
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
          // 等待獲取最新數據
          await this.fetchAccounts()
          
          Swal.fire({
            icon: 'success',
            title: '更新成功',
            timer: 1500,
            showConfirmButton: false
          })
        } else {
          await axios.post('/users/register', {
            username: this.accountForm.username,
            email: this.accountForm.email,
            password: this.accountForm.password,
            confirm_password: this.accountForm.password
          })
          await this.fetchAccounts()
          
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
    }
  }
}
</script> 