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

export default {
  name: 'AccountManagement',
  components: {
    DataTable
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
      accounts: [
        {
          id: 1,
          username: '王小明',
          email: 'wang@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=1',
          registerTime: '2023-01-06 17:04:43',
          updateTime: '2023-01-08 17:04:43',
          status: 'Enabled'
        },
        {
          id: 2,
          username: '李小華',
          email: 'lee@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=2',
          registerTime: '2023-01-06 17:05:45',
          updateTime: '2023-01-10 17:04:43',
          status: 'Disabled'
        },
        {
          id: 3,
          username: '張小美',
          email: 'chang@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=3',
          registerTime: '2023-02-15 09:30:22',
          updateTime: '2023-02-15 09:30:22',
          status: 'Enabled'
        },
        {
          id: 4,
          username: '劉大華',
          email: 'liu@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=4',
          registerTime: '2023-02-20 14:22:15',
          updateTime: '2023-02-22 11:15:30',
          status: 'Enabled'
        },
        {
          id: 5,
          username: '陳小玲',
          email: 'chen@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=5',
          registerTime: '2023-03-01 10:45:33',
          updateTime: '2023-03-05 16:20:18',
          status: 'Disabled'
        },
        {
          id: 6,
          username: '林小豪',
          email: 'lin@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=6',
          registerTime: '2023-03-10 08:15:42',
          updateTime: '2023-03-12 09:30:25',
          status: 'Enabled'
        },
        {
          id: 7,
          username: '吳小菁',
          email: 'wu@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=7',
          registerTime: '2023-03-15 13:25:16',
          updateTime: '2023-03-18 14:40:33',
          status: 'Enabled'
        },
        {
          id: 8,
          username: '黃小明',
          email: 'huang@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=8',
          registerTime: '2023-03-20 11:35:28',
          updateTime: '2023-03-22 15:50:42',
          status: 'Disabled'
        },
        {
          id: 9,
          username: '趙小雯',
          email: 'zhao@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=9',
          registerTime: '2023-04-01 09:20:17',
          updateTime: '2023-04-03 10:15:31',
          status: 'Enabled'
        },
        {
          id: 10,
          username: '周小倫',
          email: 'zhou@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=10',
          registerTime: '2023-04-05 16:45:23',
          updateTime: '2023-04-08 17:30:44',
          status: 'Enabled'
        },
        {
          id: 11,
          username: '楊小光',
          email: 'yang@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=11',
          registerTime: '2023-04-10 14:30:19',
          updateTime: '2023-04-12 11:25:37',
          status: 'Disabled'
        },
        {
          id: 12,
          username: '謝小婷',
          email: 'xie@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=12',
          registerTime: '2023-04-15 10:15:28',
          updateTime: '2023-04-18 09:40:22',
          status: 'Enabled'
        },
        {
          id: 13,
          username: '郭小峰',
          email: 'guo@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=13',
          registerTime: '2023-04-20 15:50:33',
          updateTime: '2023-04-22 16:35:48',
          status: 'Enabled'
        },
        {
          id: 14,
          username: '許小靜',
          email: 'xu@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=14',
          registerTime: '2023-04-25 11:40:26',
          updateTime: '2023-04-28 13:20:35',
          status: 'Disabled'
        },
        {
          id: 15,
          username: '蔡小德',
          email: 'cai@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=15',
          registerTime: '2023-04-30 08:25:14',
          updateTime: '2023-05-02 10:45:29',
          status: 'Enabled'
        }
      ],
      showAddModal: false,
      editingAccount: null,
      accountForm: {
        username: '',
        email: '',
        status: 'Enabled'
      }
    }
  },
  methods: {
    editAccount(account) {
      this.editingAccount = account
      this.accountForm = { ...account }
      this.showAddModal = true
    },
    deleteAccount(account) {
      if(confirm('確定要刪除此帳號嗎？')) {
        this.accounts = this.accounts.filter(a => a.id !== account.id)
      }
    },
    batchDeleteAccounts(ids) {
      if(confirm(`確定要刪除選中的 ${ids.length} 個帳號嗎？`)) {
        this.accounts = this.accounts.filter(a => !ids.includes(a.id))
      }
    },
    saveAccount() {
      if(this.editingAccount) {
        const index = this.accounts.findIndex(a => a.id === this.editingAccount.id)
        this.accounts[index] = { ...this.editingAccount, ...this.accountForm }
      } else {
        this.accounts.push({
          id: this.accounts.length + 1,
          ...this.accountForm,
          registerTime: new Date().toISOString().slice(0, 19).replace('T', ' '),
          updateTime: new Date().toISOString().slice(0, 19).replace('T', ' '),
          avatar: 'https://via.placeholder.com/40'
        })
      }
      this.showAddModal = false
      this.editingAccount = null
      this.accountForm = {
        username: '',
        email: '',
        status: 'Enabled'
      }
    }
  }
}
</script> 