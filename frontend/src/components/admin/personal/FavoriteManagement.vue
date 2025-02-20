<template>
  <div>
    <!-- 無資料時顯示 -->
    <div v-if="!favorites || favorites.length === 0" 
         class="bg-white rounded-lg shadow-sm p-8 text-center">
      <div class="text-gray-500 mb-4">
        <i class="fas fa-heart-broken text-4xl"></i>
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">
        尚無收藏資料
      </h3>
      <p class="text-gray-500">
        目前還沒有任何使用者收藏店家。
      </p>
    </div>

    <!-- 有資料時顯示表格 -->
    <div v-else>
      <!-- 資料表格 -->
      <DataTable
        :columns="columns"
        :data="favorites || []"
        :showAddButton="false"
        :showEditButton="false"
        :showDefaultActions="true"
        :customActionsOnly="true"
        :searchable="true"
        :searchFields="['store_name', 'username']"
        @delete="deleteFavorite"
        @batch-delete="batchDeleteFavorites">
        <!-- 自定義商品圖片列 -->
        <template #store_image="{ item }">
          <img 
            :src="item.store_image || defaultImage" 
            class="w-12 h-12 rounded-lg object-cover"
            @error="handleImageError"
          >
        </template>
        
        <!-- 自定義操作欄 -->
        <template #custom-actions="{ item }">
          <div class="flex space-x-2">
            <el-tooltip
              content="刪除"
              placement="top"
            >
              <button
                @click="deleteFavorite(item.id)"
                class="text-red-600 hover:text-red-800"
              >
                <i class="fas fa-trash"></i>
              </button>
            </el-tooltip>
          </div>
        </template>
      </DataTable>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import DataTable from '../common/DataTable.vue'
import { useLogger } from '@/composables/useLogger'
import { favoriteAPI } from '@/api'
import Swal from 'sweetalert2'

export default {
  name: 'FavoriteManagement',
  components: {
    DataTable
  },
  setup() {
    const { logOperation } = useLogger()
    const columns = [
      { key: 'username', label: '用戶' },
      { key: 'store_image', label: '商品圖片' },
      { key: 'store_name', label: '店家名稱' },
      { 
        key: 'created_at', 
        label: '收藏時間',
        formatter: (value) => {
          if (!value) return '';
          return new Date(value).toLocaleString('zh-TW', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
          });
        }
      },
      { key: 'custom-actions', label: '操作', width: '120px' }
    ]

    const favorites = ref([])
    const defaultImage = 'https://via.placeholder.com/150'

    // 獲取最愛列表
    const fetchFavorites = async () => {
      try {
        const response = await favoriteAPI.getFavorites()
        favorites.value = response.data.favorites || []
        console.log('收藏列表:', favorites.value)
      } catch (error) {
        console.error('獲取最愛列表失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '獲取最愛列表失敗'
        })
      }
    }

    // 刪除最愛
    const deleteFavorite = async (id) => {
      try {
        const result = await Swal.fire({
          title: '確定要刪除嗎？',
          text: '此操作無法復原',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: '確定',
          cancelButtonText: '取消'
        })

        if (result.isConfirmed) {
          await favoriteAPI.deleteFavorite(id)
          await fetchFavorites()
          await logOperation('【收藏管理】刪除收藏', '刪除')
          Swal.fire({
            icon: 'success',
            title: '已刪除',
            text: '該項目已成功刪除',
            timer: 1500,
            showConfirmButton: false
          })
        }
      } catch (error) {
        console.error('刪除失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: error.response?.data?.message || '刪除失敗'
        })
      }
    }

    // 批量刪除
    const batchDeleteFavorites = async (ids) => {
      try {
        const result = await Swal.fire({
          title: '確定要刪除選中項目嗎？',
          text: '此操作無法復原',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: '確定',
          cancelButtonText: '取消'
        })

        if (result.isConfirmed) {
          await favoriteAPI.batchDeleteFavorites(ids)
          await fetchFavorites()
          await logOperation(`【收藏管理】批量刪除收藏 (${ids.length} 筆)`, '刪除')
          Swal.fire({
            icon: 'success',
            title: '已刪除',
            text: '選中項目已成功刪除',
            timer: 1500,
            showConfirmButton: false
          })
        }
      } catch (error) {
        console.error('批量刪除失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '批量刪除失敗'
        })
      }
    }

    // 圖片載入失敗處理
    const handleImageError = (event) => {
      event.target.src = defaultImage
    }

    onMounted(async () => {
      await fetchFavorites()
      await logOperation('【收藏管理】訪問收藏管理頁面', '查看')
    })

    return {
      columns,
      favorites,
      defaultImage,
      deleteFavorite,
      batchDeleteFavorites,
      handleImageError
    }
  }
}
</script>

<style scoped>
.form-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
}

.form-input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 1px #4f46e5;
}
</style> 