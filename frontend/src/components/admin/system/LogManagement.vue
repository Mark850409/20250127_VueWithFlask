<template>
  <div>
    <!-- 無資料時顯示 -->
    <div v-if="!logs || logs.length === 0" 
         class="bg-white rounded-lg shadow-sm p-8 text-center">
      <div class="text-gray-500 mb-4">
        <i class="fas fa-clipboard-list text-4xl"></i>
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">
        尚無操作日誌
      </h3>
      <p class="text-gray-500">
        目前還沒有任何系統操作記錄。
      </p>
    </div>

    <!-- 有資料時顯示表格 -->
    <div v-else>
      <DataTable
        :columns="columns"
        :data="logs"
        :showAddButton="false"
        :showEditButton="false"
        :showDefaultActions="false"
        :selectable="false"
        :searchable="true"
        :searchFields="['description', 'username', 'ip_address']">
        
        <!-- 類型欄位自定義 -->
        <template #action="{ item }">
          <span :class="[
            'px-2 py-1 text-xs rounded-full whitespace-nowrap',
            item.action === '新增' ? 'bg-green-100 text-green-800' : 
            item.action === '修改' ? 'bg-blue-100 text-blue-800' :
            item.action === '刪除' ? 'bg-red-100 text-red-800' :
            item.action === '登入' ? 'bg-purple-100 text-purple-800' :
            item.action === '登出' ? 'bg-yellow-100 text-yellow-800' :
            'bg-gray-100 text-gray-800'
          ]">
            {{ item.action }}
          </span>
        </template>
      </DataTable>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import DataTable from '../common/DataTable.vue'
import axios from '@/utils/axios'
import Swal from 'sweetalert2'

export default {
  name: 'LogManagement',
  components: {
    DataTable
  },
  setup() {
    const logs = ref([])
    const columns = [
      { key: 'created_at', label: '時間' },
      { key: 'action', label: '類型' },
      { key: 'username', label: '操作者' },
      { key: 'description', label: '操作內容' },
      { key: 'ip_address', label: 'IP位址' },
    ]

    // 獲取日誌列表
    const fetchLogs = async () => {
      try {
        const response = await axios.get('/logs/')
        logs.value = response.data.logs || []
      } catch (error) {
        console.error('獲取日誌列表失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '獲取日誌列表失敗'
        })
      }
    }

    onMounted(() => {
      fetchLogs()
    })

    return {
      logs,
      columns,
    }
  }
}
</script> 