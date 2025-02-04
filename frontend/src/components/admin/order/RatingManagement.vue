<template>
  <div>
    <!-- 數據表格 -->
    <DataTable
      :columns="columns"
      :data="ratings"
      :show-add-button="false"
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
        <span class="truncate block max-w-md">
          {{ truncateText(item.text, 30) }}
        </span>
      </template>
    </DataTable>

    <!-- 新增/編輯彈窗 -->
    <el-dialog
      title="編輯評分"
      v-model="showAddModal"
      width="500px"
      :close-on-click-modal="false"
      destroy-on-close>
      <div class="p-4">
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
      
      <template #footer>
        <div class="flex justify-end space-x-3">
          <button 
            @click="showAddModal = false"
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
            取消
          </button>
          <button 
            @click="validateAndSubmit"
            class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">
            確定
          </button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import DataTable from '../common/DataTable.vue'
import axios from '@/utils/axios'
import Swal from 'sweetalert2'

export default {
  name: 'RatingManagement',
  components: {
    DataTable
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

    // 監聽 showAddModal 的變化
    watch(showAddModal, (newVal) => {
      if (!newVal) {
        resetForm()
      }
    })

    // 獲取評分列表
    const fetchRatings = async () => {
      try {
        const response = await axios.get('/ratings/')
        ratings.value = response.data.ratings
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
          await axios.delete(`/ratings/${rating.id}`)
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
          await Promise.all(ids.map(id => axios.delete(`/ratings/${id}`)))
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
        await axios.put(`/ratings/${editingRating.value.id}`, ratingForm.value)
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
      truncateText
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