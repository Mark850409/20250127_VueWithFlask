<template>
  <div>
    <DataTable
      :columns="columns"
      :data="accounts"
      @add="showAddModal = true"
      @edit="editAccount"
      @delete="deleteAccount"
      @batch-delete="batchDeleteAccounts">
      <!-- 自定義頭像列 -->
      <template #avatar="{ item }">
        <img :src="item.avatar || 'https://via.placeholder.com/40'" 
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
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">帳號名稱</label>
            <input type="text" v-model="accountForm.username" 
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input type="email" v-model="accountForm.email" 
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">狀態</label>
            <select v-model="accountForm.status" 
                    class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
              <option value="Enabled">啟用</option>
              <option value="Disabled">停用</option>
            </select>
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
        status: 'Enabled'
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

        const response = await axios.get('/users')
        
        this.accounts = response.data.users.map(user => ({
          id: user.id,
          username: user.username,
          email: user.email,
          avatar: user.avatar || 'https://api.dicebear.com/7.x/avataaars/svg?seed=default',
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
    editAccount(account) {
      this.editingAccount = account
      this.accountForm = { ...account }
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
    async saveAccount() {
      try {
        if (this.editingAccount) {
          await axios.put(`/users/${this.editingAccount.id}`, this.accountForm)
        } else {
          await axios.post('/users/register', this.accountForm)
        }
        await this.fetchAccounts()
        this.showAddModal = false
        this.editingAccount = null
        this.accountForm = {
          username: '',
          email: '',
          status: 'Enabled'
        }
        Swal.fire({
          icon: 'success',
          title: this.editingAccount ? '更新成功' : '新增成功',
          timer: 1500,
          showConfirmButton: false
        })
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: this.editingAccount ? '更新失敗' : '新增失敗',
          text: error.response?.data?.message || '請稍後再試',
          confirmButtonText: '確定'
        })
      }
    }
  }
}
</script> 