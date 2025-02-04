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

    <!-- 管理員列表 -->
    <transition-group 
      :name="viewMode === 'card' ? 'card-list' : 'list'"
      tag="div"
      :class="[
        viewMode === 'card' 
          ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6' 
          : 'space-y-4'
      ]"
    >
      <!-- 調試信息 -->
      <div v-if="!admins || admins.length === 0" class="col-span-full text-center py-8 text-gray-500">
        {{ admins === null ? '載入中...' : '沒有管理員數據' }}
      </div>

      <!-- 卡片/列表項目 -->
      <div v-for="admin in admins" 
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
            最後更新：{{ formatDateTime(admin.updated_at) || '-' }}
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
              最後更新：{{ formatDateTime(admin.updated_at) || '-' }}
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
      <div class="bg-white rounded-xl p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-bold">{{ editingAdmin ? '編輯管理員' : '新增管理員' }}</h2>
          <button @click="showAddModal = false" class="text-gray-500 hover:text-gray-700">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- 左側：頭像和基本信息 -->
          <div class="space-y-6">
            <!-- 頭像上傳 -->
            <div class="flex flex-col items-center p-6 bg-gray-50 rounded-lg">
              <img :src="previewAvatar || adminForm.avatar" 
                   class="w-32 h-32 rounded-full mb-4 border-4 border-white shadow-lg"
                   alt="預覽頭像">
              <label class="px-4 py-2 bg-white rounded-lg cursor-pointer hover:bg-gray-100 transition-colors">
                <input type="file" 
                       class="hidden" 
                       accept="image/*"
                       @change="handleAvatarUpload">
                <i class="fas fa-camera mr-2"></i>更換頭像
              </label>
            </div>

            <!-- 基本信息 -->
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  管理員名稱 <span class="text-red-500">*</span>
                </label>
                <input type="text" 
                       v-model="adminForm.username" 
                       :class="{'border-red-500': errors.username}"
                       class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
                <span v-if="errors.username" class="text-red-500 text-xs mt-1">{{ errors.username }}</span>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Email <span class="text-red-500">*</span>
                </label>
                <input type="email" 
                       v-model="adminForm.email" 
                       :class="{'border-red-500': errors.email}"
                       class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
                <span v-if="errors.email" class="text-red-500 text-xs mt-1">{{ errors.email }}</span>
              </div>
            </div>
          </div>

          <!-- 右側：密碼和權限設置 -->
          <div class="space-y-6">
            <!-- 密碼設置 -->
            <div class="p-6 bg-gray-50 rounded-lg space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  密碼 <span v-if="!editingAdmin" class="text-red-500">*</span>
                </label>
                <input type="password" 
                       v-model="adminForm.password" 
                       :class="{'border-red-500': errors.password}"
                       :placeholder="editingAdmin ? '不修改請留空' : '請輸入密碼'"
                       class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
                <span v-if="errors.password" class="text-red-500 text-xs mt-1">{{ errors.password }}</span>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  確認密碼 <span v-if="!editingAdmin" class="text-red-500">*</span>
                </label>
                <input type="password" 
                       v-model="adminForm.confirmPassword" 
                       :class="{'border-red-500': errors.confirmPassword}"
                       :placeholder="editingAdmin ? '不修改請留空' : '請再次輸入密碼'"
                       class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
                <span v-if="errors.confirmPassword" class="text-red-500 text-xs mt-1">{{ errors.confirmPassword }}</span>
              </div>
            </div>

            <!-- 權限設置 -->
            <div class="p-6 bg-gray-50 rounded-lg space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  權限等級 <span class="text-red-500">*</span>
                </label>
                <select v-model="adminForm.role" 
                        class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
                  <option value="admin">一般管理員</option>
                  <option value="super_admin">超級管理員</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  狀態 <span class="text-red-500">*</span>
                </label>
                <select v-model="adminForm.status" 
                        class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
                  <option value="active">啟用</option>
                  <option value="inactive">停用</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- 操作按鈕 -->
        <div class="mt-6 pt-4 border-t flex justify-end space-x-4">
          <button @click="showAddModal = false" 
                  class="px-6 py-2 text-gray-700 border rounded-lg hover:bg-gray-50">
            取消
          </button>
          <button @click="saveAdmin" 
                  class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
            確認
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, watch, onMounted, computed } from 'vue'
import axios from '@/utils/axios'
import Swal from 'sweetalert2'

export default {
  name: 'UserManagement',
  setup() {
    const viewMode = ref('card')
    const searchQuery = ref('')
    const showAddModal = ref(false)
    const editingAdmin = ref(null)
    const previewAvatar = ref(null)
    const admins = ref([])
    const errors = ref({})

    // 過濾後的管理員列表
    const filteredAdmins = computed(() => {
      if (!admins.value || !Array.isArray(admins.value)) {
        console.log('Current admins value:', admins.value)
        return []
      }
      // 直接使用 admins.value 進行過濾
      return admins.value.filter(admin => 
        admin.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        admin.email.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    // 初始表單狀態
    const initialFormState = {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      role: 'admin',
      status: 'active',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=default'
    }

    const adminForm = reactive({...initialFormState})

    // 表單驗證規則
    const validateForm = () => {
      const newErrors = {}
      
      // 用戶名驗證
      if (!adminForm.username?.trim()) {
        newErrors.username = '請輸入管理員名稱'
      }

      // Email驗證
      if (!adminForm.email?.trim()) {
        newErrors.email = '請輸入Email'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(adminForm.email)) {
        newErrors.email = '請輸入有效的Email格式'
      }

      // 密碼驗證
      if (!editingAdmin.value) {
        if (!adminForm.password) {
          newErrors.password = '請輸入密碼'
        } else if (adminForm.password.length < 6) {
          newErrors.password = '密碼長度至少6個字符'
        }

        if (!adminForm.confirmPassword) {
          newErrors.confirmPassword = '請確認密碼'
        } else if (adminForm.password !== adminForm.confirmPassword) {
          newErrors.confirmPassword = '兩次密碼輸入不一致'
        }
      } else if (adminForm.password && adminForm.password.length < 6) {
        newErrors.password = '密碼長度至少6個字符'
      } else if (adminForm.password !== adminForm.confirmPassword) {
        newErrors.confirmPassword = '兩次密碼輸入不一致'
      }

      errors.value = newErrors
      return Object.keys(newErrors).length === 0
    }

    // 重置表單
    const resetForm = () => {
      Object.assign(adminForm, initialFormState)
      editingAdmin.value = null
      previewAvatar.value = null
      errors.value = {}
    }

    // 獲取管理員列表
    const fetchAdmins = async () => {
      try {
        const response = await axios.get('/admins/')
        // 確保我們獲取到正確的數據結構
        if (response.data && Array.isArray(response.data)) {
          admins.value = response.data
        } else if (response.data && Array.isArray(response.data.admins)) {
          admins.value = response.data.admins
        } else {
          console.error('Unexpected API response structure:', response.data)
          admins.value = []
        }
        console.log('Fetched admins:', admins.value)
      } catch (error) {
        console.error('Error fetching admins:', error)
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '獲取管理員列表失敗',
          confirmButtonText: '確定'
        })
      }
    }

    // 處理頭像上傳
    const handleAvatarUpload = (event) => {
      const file = event.target.files[0]
      if (file) {
        if (file.size > 2 * 1024 * 1024) {
          Swal.fire({
            icon: 'error',
            title: '錯誤',
            text: '圖片大小不能超過2MB',
            confirmButtonText: '確定'
          })
          return
        }
        previewAvatar.value = URL.createObjectURL(file)
        adminForm.avatar = file
      }
    }

    // 編輯管理員
    const editAdmin = async (admin) => {
      try {
        // 獲取最新的管理員資料
        const response = await axios.get(`/admins/${admin.id}`)
        const adminData = response.data

        // 更新編輯狀態
        editingAdmin.value = adminData
        Object.assign(adminForm, {
          ...adminData,
          password: '',
          confirmPassword: ''
        })

        previewAvatar.value = null
        showAddModal.value = true

      } catch (error) {
        console.error('Error fetching admin details:', error)
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '獲取管理員資料失敗',
          confirmButtonText: '確定'
        })
      }
    }

    // 刪除管理員
    const deleteAdmin = async (admin) => {
      if (admin.role === 'super_admin') {
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '無法刪除超級管理員',
          confirmButtonText: '確定'
        })
        return
      }

      const result = await Swal.fire({
        title: '確定要刪除嗎？',
        text: '此操作無法復原',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: '確定刪除',
        cancelButtonText: '取消'
      })

      if (result.isConfirmed) {
        try {
          await axios.delete(`/admins/${admin.id}`)
          Swal.fire({
            icon: 'success',
            title: '成功',
            text: '管理員已刪除',
            timer: 1500,
            showConfirmButton: false
          })
          fetchAdmins()
        } catch (error) {
          Swal.fire({
            icon: 'error',
            title: '錯誤',
            text: '刪除失敗',
            confirmButtonText: '確定'
          })
          console.error(error)
        }
      }
    }

    // 保存管理員
    const saveAdmin = async () => {
      if (!validateForm()) {
        return
      }

      try {
        const formData = new FormData()
        Object.keys(adminForm).forEach(key => {
          if (key !== 'confirmPassword' && (key !== 'password' || adminForm[key])) {
            formData.append(key, adminForm[key])
          }
        })

        if (editingAdmin.value) {
          await axios.put(`/admins/${editingAdmin.value.id}`, formData)
        } else {
          await axios.post('/admins', formData)
        }

        Swal.fire({
          icon: 'success',
          title: '成功',
          text: `${editingAdmin.value ? '編輯' : '新增'}管理員成功`,
          timer: 1500,
          showConfirmButton: false
        })

        showAddModal.value = false
        resetForm()
        fetchAdmins()
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: `${editingAdmin.value ? '編輯' : '新增'}失敗`,
          confirmButtonText: '確定'
        })
        console.error(error)
      }
    }

    // 監聽 modal 關閉
    watch(showAddModal, (newVal) => {
      if (!newVal) {
        resetForm()
      }
    })

    // 時間格式化函數
    const formatDateTime = (dateString) => {
      if (!dateString) return '-'
      const date = new Date(dateString)
      return date.toLocaleString('zh-TW', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
      })
    }

    onMounted(() => {
      fetchAdmins()
    })

    return {
      viewMode,
      searchQuery,
      showAddModal,
      editingAdmin,
      previewAvatar,
      adminForm,
      admins: computed(() => filteredAdmins.value),  // 確保返回響應式數據
      errors,
      handleAvatarUpload,
      editAdmin,
      deleteAdmin,
      saveAdmin,
      resetForm,
      formatDateTime
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