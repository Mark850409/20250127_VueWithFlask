<template>
  <div>
    <!-- 無資料時顯示 -->
    <div v-if="!ratings || ratings.length === 0" 
         class="bg-white rounded-lg shadow-sm p-8 text-center">
      <div class="text-gray-500 mb-4">
        <i class="fas fa-star text-4xl"></i>
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">
        尚無評分資料
      </h3>
      <p class="text-gray-500 mb-4">
        目前還沒有任何評分記錄。
        <br>
        當使用者對飲料店進行評分後，評分資料會顯示在這裡。
      </p>
    </div>

    <!-- 有資料時顯示表格 -->
    <div v-else>
      <!-- 數據表格 -->
      <DataTable
        :columns="columns"
        :data="ratings"
        :show-add-button="false"
        :show-default-actions="true"
        :custom-actions-only="false"
        @edit="handleEdit"
        @delete="handleDelete"
        @batch-delete="handleBatchDelete">
        <!-- 自定義評分列 -->
        <template #rating="{ item }">
          <div class="flex items-center">
            <span class="text-yellow-400">
              <i v-for="n in 5" :key="n" 
                 :class="['fas', n <= Math.floor(item.rating) ? 'fa-star' : 'fa-star-o']"></i>
            </span>
            <span class="ml-2 text-gray-600 text-sm">{{ item.rating }}</span>
          </div>
        </template>
        <!-- 自定義評論內容列 -->
        <template #text="{ item }">
          <span class="truncate inline-block max-w-[300px]">
            {{ truncateText(item.text, 30) }}
          </span>
        </template>
      </DataTable>

      <!-- 新增/編輯彈窗 -->
      <div v-if="showAddModal" 
           class="fixed inset-0 z-[9999]">
        <!-- 背景遮罩 -->
        <div class="absolute inset-0 bg-black bg-opacity-50"></div>
        
        <!-- Modal 內容 -->
        <div class="absolute inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4">
            <div class="relative bg-white rounded-lg shadow-lg w-full max-w-xl">
              <!-- Modal 標題 -->
              <div class="flex justify-between items-center px-6 py-4 border-b">
                <h3 class="text-lg font-semibold">編輯評分</h3>
                <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
                  <i class="fas fa-times"></i>
                </button>
              </div>

              <!-- Modal 內容 -->
              <div class="px-6 py-4 space-y-4 max-h-[calc(85vh-8rem)] overflow-y-auto">
                <div class="mb-4">
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    用戶 <span class="text-red-500">*</span>
                  </label>
                  <input 
                    v-model="ratingForm.user"
                    type="text"
                    class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    :class="{'border-red-500': errors.user}"
                    placeholder="請輸入用戶名稱">
                  <span v-if="errors.user" class="text-red-500 text-xs mt-1">{{ errors.user }}</span>
                </div>
                
                <div class="mb-4">
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    店家 <span class="text-red-500">*</span>
                  </label>
                  <input 
                    v-model="ratingForm.restaurant_name"
                    type="text"
                    class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    :class="{'border-red-500': errors.restaurant_name}"
                    placeholder="請輸入店家名稱">
                  <span v-if="errors.restaurant_name" class="text-red-500 text-xs mt-1">{{ errors.restaurant_name }}</span>
                </div>
                
                <div class="mb-4">
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    評分 <span class="text-red-500">*</span>
                  </label>
                  <el-rate 
                    v-model="ratingForm.rating"
                    :max="5"
                    class="mt-1">
                  </el-rate>
                  <span v-if="errors.rating" class="text-red-500 text-xs mt-1">{{ errors.rating }}</span>
                </div>
                
                <div class="mb-4">
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    評論內容 <span class="text-red-500">*</span>
                  </label>
                  <textarea 
                    v-model="ratingForm.text"
                    rows="6"
                    class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                    :class="{'border-red-500': errors.text}"
                    placeholder="請輸入評論內容">
                  </textarea>
                  <span v-if="errors.text" class="text-red-500 text-xs mt-1">{{ errors.text }}</span>
                </div>
              </div>

              <!-- Modal 底部按鈕 -->
              <div class="px-6 py-4 bg-gray-50 border-t rounded-b-lg flex justify-end space-x-3">
                <button 
                  @click="closeModal"
                  class="px-4 py-2 text-gray-600 hover:text-gray-800 rounded-lg hover:bg-gray-100 transition-colors">
                  取消
                </button>
                <button 
                  @click="validateAndSubmit"
                  class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-sm">
                  確定
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import DataTable from '../common/DataTable.vue'
import BackToHome from '../common/BackToHome.vue'
import { useLogger } from '@/composables/useLogger'
import { ratingAPI } from '@/api'
import Swal from 'sweetalert2'

export default {
  name: 'RatingManagement',
  components: {
    DataTable,
    BackToHome
  },
  setup() {
    const columns = [
      { key: 'user', label: '用戶' },
      { key: 'restaurant_name', label: '店家' },
      { key: 'rating', label: '評分' },
      { key: 'text', label: '評論內容' },
      { key: 'time', label: '評分時間' }
    ]

    // 初始表單數據
    const initialFormState = {
      user: '',
      restaurant_name: '',
      rating: 0,
      text: ''
    }

    const ratings = ref([])
    const showAddModal = ref(false)
    const editingRating = ref(null)
    const ratingForm = ref({ ...initialFormState })

    // 錯誤訊息
    const errors = ref({})

    // 重置表單
    const resetForm = () => {
      ratingForm.value = { ...initialFormState }
      editingRating.value = null
      errors.value = {}
    }

    // 獲取評分列表
    const fetchRatings = async () => {
      try {
        const response = await ratingAPI.getRatings()
        ratings.value = response.data.ratings
        console.log('評分列表:', ratings.value)
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '獲取評分列表失敗',
          confirmButtonText: '確定'
        })
        console.error(error)
      }
    }

    // 驗證表單
    const validateForm = () => {
      const newErrors = {}

      if (!ratingForm.value.user?.trim()) {
        newErrors.user = '請輸入用戶名稱'
      }

      if (!ratingForm.value.restaurant_name?.trim()) {
        newErrors.restaurant_name = '請輸入店家名稱'
      }

      if (!ratingForm.value.rating) {
        newErrors.rating = '請選擇評分'
      }

      if (!ratingForm.value.text?.trim()) {
        newErrors.text = '請輸入評論內容'
      } else if (ratingForm.value.text.length < 10) {
        newErrors.text = '評論內容至少需要10個字'
      }

      errors.value = newErrors
      return Object.keys(newErrors).length === 0
    }

    // 驗證並提交
    const validateAndSubmit = async () => {
      if (validateForm()) {
        await handleSubmit()
      } 
    }

    // 編輯
    const handleEdit = (rating) => {
      editingRating.value = rating
      ratingForm.value = { ...rating }
      showAddModal.value = true
    }

    // 刪除
    const handleDelete = async (rating) => {
      try {
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
          await ratingAPI.deleteRating(rating.id)
          Swal.fire({
            icon: 'success',
            title: '已刪除',
            text: '評分已成功刪除',
            timer: 1500,
            showConfirmButton: false
          })
          fetchRatings()
        }
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

    // 批量刪除
    const handleBatchDelete = async (ids) => {
      try {
        const result = await Swal.fire({
          title: '批量刪除確認',
          text: `確定要刪除這 ${ids.length} 條評分嗎？此操作無法復原`,
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: '確定刪除',
          cancelButtonText: '取消'
        })

        if (result.isConfirmed) {
          await ratingAPI.batchDeleteRatings(ids)
          Swal.fire({
            icon: 'success',
            title: '已刪除',
            text: '所選評分已成功刪除',
            timer: 1500,
            showConfirmButton: false
          })
          fetchRatings()
        }
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '批量刪除失敗',
          confirmButtonText: '確定'
        })
        console.error(error)
      }
    }

    // 文字截斷函數
    const truncateText = (text, length) => {
      if (!text) return ''
      return text.length > length ? text.slice(0, length) + '...' : text
    }

    const handleSubmit = async () => {
      try {
        if (editingRating.value) {
          await ratingAPI.updateRating(editingRating.value.id, ratingForm.value)
        } else {
          await ratingAPI.createRating(ratingForm.value)
        }
        Swal.fire({
          icon: 'success',
          title: '成功',
          text: '編輯成功',
          timer: 1500,
          showConfirmButton: false
        })
        showAddModal.value = false
        fetchRatings()
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '編輯失敗',
          confirmButtonText: '確定'
        })
        console.error(error)
      }
    }

    const closeModal = () => {
      showAddModal.value = false
      resetForm()
    }

    onMounted(() => {
      fetchRatings()
    })

    return {
      columns,
      ratings,
      showAddModal,
      editingRating,
      ratingForm,
      errors,
      validateAndSubmit,
      handleEdit,
      handleDelete,
      handleBatchDelete,
      truncateText,
      closeModal,
      resetForm
    }
  }
}
</script>

<style scoped>
.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 調整 el-rate 組件的樣式 */
:deep(.el-rate) {
  display: flex;
  align-items: center;
  height: 32px;
}

/* 調整對話框內容的樣式 */
:deep(.el-dialog__body) {
  padding: 0;
}

/* 錯誤狀態的輸入框樣式 */
.border-red-500 {
  border-color: rgb(239, 68, 68);
}

/* 必填星號樣式 */
.text-red-500 {
  color: rgb(239, 68, 68);
}
</style> 