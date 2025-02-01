<template>
  <div>
    <!-- 頂部工具列 -->
    <div class="flex justify-between items-center mb-6">
      <!-- 搜尋框 -->
      <div class="relative w-64">
        <input 
          type="text" 
          v-model="searchQuery"
          placeholder="搜尋管理員..."
          class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
        >
        <i class="fas fa-search absolute right-3 top-3 text-gray-400"></i>
      </div>
      
      <div class="flex items-center space-x-4">
        <!-- 視圖切換按鈕 -->
        <div class="bg-white rounded-lg shadow-sm p-1 inline-flex space-x-1">
          <button @click="viewMode = 'card'" 
                  :class="[
                    'px-3 py-1.5 rounded transition-colors duration-200 flex items-center',
                    viewMode === 'card' ? 'bg-blue-500 text-white' : 'text-gray-600 hover:bg-gray-100'
                  ]">
            <i class="fas fa-th-large mr-2"></i>卡片
          </button>
          <button @click="viewMode = 'list'" 
                  :class="[
                    'px-3 py-1.5 rounded transition-colors duration-200 flex items-center',
                    viewMode === 'list' ? 'bg-blue-500 text-white' : 'text-gray-600 hover:bg-gray-100'
                  ]">
            <i class="fas fa-list mr-2"></i>列表
          </button>
        </div>
        
        <!-- 新增按鈕 -->
        <button 
          @click="showAddModal = true"
          class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          <i class="fas fa-plus mr-2"></i>新增管理員
        </button>
      </div>
    </div>

    <!-- 管理員列表 - 使用 transition-group 實現動畫 -->
    <transition-group 
      :name="viewMode === 'card' ? 'card-list' : 'list'"
      tag="div"
      :class="[
        viewMode === 'card' 
          ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6' 
          : 'space-y-4'
      ]"
    >
      <!-- 卡片/列表項目 -->
      <div v-for="admin in filteredAdmins" 
           :key="admin.id" 
           :class="[
             'bg-white rounded-xl shadow-lg transition-all duration-300',
             viewMode === 'card' ? 'p-6' : 'p-4'
           ]">
        <!-- 卡片視圖 -->
        <div v-if="viewMode === 'card'" class="flex flex-col items-center">
          <img :src="admin.avatar" 
               class="w-24 h-24 rounded-full mb-4"
               alt="管理員頭像">
          <h3 class="text-lg font-semibold">{{ admin.username }}</h3>
          <p class="text-gray-600 mb-2">{{ admin.email }}</p>
          <div class="flex items-center space-x-2 mb-4">
            <span :class="[
              'px-2 py-1 text-xs rounded-full',
              admin.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            ]">
              {{ admin.status === 'active' ? '啟用' : '停用' }}
            </span>
            <span class="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">
              {{ admin.role === 'super_admin' ? '超級管理員' : '一般管理員' }}
            </span>
          </div>
          <p class="text-sm text-gray-500 mb-4">
            最後登入：{{ admin.lastLoginTime }}
          </p>
          <div class="flex space-x-2">
            <button @click="editAdmin(admin)"
                    class="px-3 py-1 text-sm border border-blue-500 text-blue-500 rounded hover:bg-blue-50">
              編輯
            </button>
            <button v-if="admin.role !== 'super_admin'"
                    @click="deleteAdmin(admin)"
                    class="px-3 py-1 text-sm border border-red-500 text-red-500 rounded hover:bg-red-50">
              刪除
            </button>
          </div>
        </div>

        <!-- 列表視圖 -->
        <div v-else class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <img :src="admin.avatar" 
                 class="w-12 h-12 rounded-full"
                 alt="管理員頭像">
            <div>
              <h3 class="font-semibold">{{ admin.username }}</h3>
              <p class="text-sm text-gray-600">{{ admin.email }}</p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <span :class="[
              'px-2 py-1 text-xs rounded-full',
              admin.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            ]">
              {{ admin.status === 'active' ? '啟用' : '停用' }}
            </span>
            <span class="text-sm text-gray-500">
              最後登入：{{ admin.lastLoginTime }}
            </span>
            <div class="flex space-x-2">
              <button @click="editAdmin(admin)"
                      class="p-1.5 text-blue-600 hover:text-blue-800 rounded-full hover:bg-blue-50">
                <i class="fas fa-edit"></i>
              </button>
              <button v-if="admin.role !== 'super_admin'"
                      @click="deleteAdmin(admin)"
                      class="p-1.5 text-red-600 hover:text-red-800 rounded-full hover:bg-red-50">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition-group>

    <!-- 新增/編輯管理員彈窗 -->
    <div v-if="showAddModal" 
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-8 w-full max-w-md">
        <h2 class="text-xl font-bold mb-6">{{ editingAdmin ? '編輯管理員' : '新增管理員' }}</h2>
        <div class="space-y-6">
          <!-- 頭像上傳 -->
          <div class="flex flex-col items-center">
            <img :src="previewAvatar || adminForm.avatar" 
                 class="w-24 h-24 rounded-full mb-4"
                 alt="預覽頭像">
            <label class="px-4 py-2 bg-gray-100 rounded-lg cursor-pointer hover:bg-gray-200">
              <input type="file" 
                     class="hidden" 
                     accept="image/*"
                     @change="handleAvatarUpload">
              <i class="fas fa-camera mr-2"></i>更換頭像
            </label>
          </div>

          <!-- 基本資料表單 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">管理員名稱</label>
            <input type="text" 
                   v-model="adminForm.username" 
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input type="email" 
                   v-model="adminForm.email" 
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">密碼</label>
            <input type="password" 
                   v-model="adminForm.password" 
                   :placeholder="editingAdmin ? '不修改請留空' : '請輸入密碼'"
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">確認密碼</label>
            <input type="password" 
                   v-model="adminForm.confirmPassword" 
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

        <!-- 操作按鈕 -->
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
  </div>
</template>

<script>
export default {
  name: 'UserManagement',
  data() {
    return {
      viewMode: 'card',
      searchQuery: '',
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
      },
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
      ]
    }
  },
  computed: {
    filteredAdmins() {
      return this.admins.filter(admin => 
        admin.username.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        admin.email.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    }
  },
  methods: {
    handleAvatarUpload(event) {
      const file = event.target.files[0]
      if (file) {
        this.previewAvatar = URL.createObjectURL(file)
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
    saveAdmin() {
      // 表單驗證
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
        // 更新現有管理員
        const index = this.admins.findIndex(a => a.id === this.editingAdmin.id)
        this.admins[index] = {
          ...this.editingAdmin,
          ...this.adminForm,
          avatar: this.previewAvatar || this.adminForm.avatar
        }
      } else {
        // 新增管理員
        this.admins.push({
          id: this.admins.length + 1,
          ...this.adminForm,
          avatar: this.previewAvatar || this.adminForm.avatar,
          lastLoginTime: '-'
        })
      }

      // 重置表單
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

<style scoped>
/* 卡片視圖動畫 */
.card-list-enter-active,
.card-list-leave-active {
  transition: all 0.5s ease;
}
.card-list-enter-from,
.card-list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
.card-list-move {
  transition: transform 0.5s ease;
}

/* 列表視圖動畫 */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
.list-move {
  transition: transform 0.5s ease;
}
</style> 