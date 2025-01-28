<template>
  <div>
    <DataTable
      :columns="columns"
      :data="admins"
      @add="showAddModal = true"
      @edit="editAdmin"
      @delete="deleteAdmin"
      @batch-delete="batchDeleteAdmins">
      <!-- 自定義頭像列 -->
      <template #avatar="{ item }">
        <div class="flex items-center">
          <img :src="item.avatar" class="w-10 h-10 rounded-full">
        </div>
      </template>
      <!-- 自定義狀態列 -->
      <template #status="{ item }">
        <span :class="[
          'px-2 py-1 text-xs rounded-full',
          item.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        ]">
          {{ item.status === 'active' ? '啟用' : '停用' }}
        </span>
      </template>
    </DataTable>

    <!-- 新增/編輯管理員彈窗 -->
    <div v-if="showAddModal" 
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white rounded-xl p-8 w-full max-w-md">
        <h2 class="text-xl font-bold mb-6">{{ editingAdmin ? '編輯管理員' : '新增管理員' }}</h2>
        <div class="space-y-6">
          <!-- 頭像上傳 -->
          <div class="flex flex-col items-center">
            <img :src="previewAvatar || adminForm.avatar" 
                 class="w-24 h-24 rounded-full mb-4">
            <label class="px-4 py-2 bg-gray-100 rounded-lg cursor-pointer hover:bg-gray-200">
              <input type="file" 
                     class="hidden" 
                     accept="image/*"
                     @change="handleAvatarUpload">
              <i class="fas fa-camera mr-2"></i>更換頭像
            </label>
          </div>

          <!-- 基本資料 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">管理員名稱</label>
            <input type="text" v-model="adminForm.username" 
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input type="email" v-model="adminForm.email" 
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">密碼</label>
            <input type="password" v-model="adminForm.password" 
                   :placeholder="editingAdmin ? '不修改請留空' : '請輸入密碼'"
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">確認密碼</label>
            <input type="password" v-model="adminForm.confirmPassword" 
                   :placeholder="editingAdmin ? '不修改請留空' : '請再次輸入密碼'"
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">權限等級</label>
            <select v-model="adminForm.role" 
                    class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
              <option value="admin">一般管理員</option>
              <option value="super_admin">超級管理員</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">狀態</label>
            <select v-model="adminForm.status" 
                    class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
              <option value="active">啟用</option>
              <option value="inactive">停用</option>
            </select>
          </div>
        </div>
        <div class="mt-8 flex justify-end space-x-4">
          <button @click="showAddModal = false" 
                  class="px-4 py-2 text-gray-700 border rounded-lg hover:bg-gray-50">
            取消
          </button>
          <button @click="saveAdmin" 
                  class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
            確認
          </button>
        </div>
      </div>
    </div>
    <BackToHome />
  </div>
</template>

<script>
import DataTable from '../common/DataTable.vue'
import BackToHome from '../common/BackToHome.vue'

export default {
  name: 'UserManagement',
  components: {
    DataTable,
    BackToHome
  },
  data() {
    return {
      columns: [
        { key: 'avatar', label: '頭像' },
        { key: 'username', label: '管理員名稱' },
        { key: 'email', label: 'Email' },
        { key: 'role', label: '權限等級' },
        { key: 'lastLoginTime', label: '最後登入時間' },
        { key: 'status', label: '狀態' }
      ],
      admins: [
        {
          id: 1,
          username: '系統管理員',
          email: 'admin@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=admin1',
          role: 'super_admin',
          lastLoginTime: '2024-01-15 15:30:22',
          status: 'active'
        },
        {
          id: 2,
          username: '商品管理員',
          email: 'product@example.com',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=admin2',
          role: 'admin',
          lastLoginTime: '2024-01-15 14:25:18',
          status: 'active'
        }
      ],
      showAddModal: false,
      editingAdmin: null,
      previewAvatar: null,
      adminForm: {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        role: 'admin',
        status: 'active',
        avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=default'
      }
    }
  },
  methods: {
    handleAvatarUpload(event) {
      const file = event.target.files[0]
      if (file) {
        this.previewAvatar = URL.createObjectURL(file)
        // 實際上傳邏輯...
      }
    },
    editAdmin(admin) {
      this.editingAdmin = admin
      this.adminForm = {
        ...admin,
        password: '',
        confirmPassword: ''
      }
      this.previewAvatar = null
      this.showAddModal = true
    },
    deleteAdmin(admin) {
      if(admin.role === 'super_admin') {
        alert('無法刪除超級管理員')
        return
      }
      if(confirm('確定要刪除此管理員嗎？')) {
        this.admins = this.admins.filter(a => a.id !== admin.id)
      }
    },
    batchDeleteAdmins(ids) {
      if(this.admins.some(admin => admin.role === 'super_admin' && ids.includes(admin.id))) {
        alert('無法刪除超級管理員')
        return
      }
      if(confirm(`確定要刪除選中的 ${ids.length} 個管理員嗎？`)) {
        this.admins = this.admins.filter(a => !ids.includes(a.id))
      }
    },
    saveAdmin() {
      // 驗證表單
      if(!this.adminForm.username || !this.adminForm.email) {
        alert('請填寫必要欄位')
        return
      }
      if(!this.editingAdmin && !this.adminForm.password) {
        alert('請設置密碼')
        return
      }
      if(this.adminForm.password !== this.adminForm.confirmPassword) {
        alert('兩次密碼輸入不一致')
        return
      }

      if(this.editingAdmin) {
        const index = this.admins.findIndex(a => a.id === this.editingAdmin.id)
        this.admins[index] = {
          ...this.editingAdmin,
          ...this.adminForm,
          avatar: this.previewAvatar || this.adminForm.avatar
        }
      } else {
        this.admins.push({
          id: this.admins.length + 1,
          ...this.adminForm,
          avatar: this.previewAvatar || this.adminForm.avatar,
          lastLoginTime: '-'
        })
      }
      this.showAddModal = false
      this.editingAdmin = null
      this.previewAvatar = null
      this.adminForm = {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        role: 'admin',
        status: 'active',
        avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=default'
      }
    }
  }
}
</script> 