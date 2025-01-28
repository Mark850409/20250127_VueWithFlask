<template>
  <div>
    <DataTable
      :columns="columns"
      :data="logs"
      @add="showAddModal = true"
      @edit="editLog"
      @delete="deleteLog"
      @batch-delete="batchDeleteLogs">
      <!-- 自定義類型列 -->
      <template #type="{ item }">
        <span :class="[
          'px-2 py-1 text-xs rounded-full',
          getTypeClass(item.type)
        ]">
          {{ item.type }}
        </span>
      </template>
    </DataTable>
  </div>
</template>

<script>
import DataTable from '../common/DataTable.vue'

export default {
  name: 'LogManagement',
  components: {
    DataTable
  },
  data() {
    return {
      columns: [
        { key: 'timestamp', label: '時間' },
        { key: 'type', label: '類型' },
        { key: 'user', label: '操作者' },
        { key: 'action', label: '操作內容' },
        { key: 'ip', label: 'IP位址' }
      ],
      logs: [
        {
          id: 1,
          timestamp: '2024-01-15 10:30:22',
          type: '登入',
          user: '管理員',
          action: '使用者登入系統',
          ip: '192.168.1.1'
        },
        // ... 更多日誌數據
      ]
    }
  },
  methods: {
    getTypeClass(type) {
      const classes = {
        '登入': 'bg-green-100 text-green-800',
        '登出': 'bg-gray-100 text-gray-800',
        '新增': 'bg-blue-100 text-blue-800',
        '修改': 'bg-yellow-100 text-yellow-800',
        '刪除': 'bg-red-100 text-red-800'
      }
      return classes[type] || 'bg-gray-100 text-gray-800'
    },
    editLog(log) {
      // 實作編輯邏輯
    },
    deleteLog(log) {
      if(confirm('確定要刪除此日誌嗎？')) {
        this.logs = this.logs.filter(l => l.id !== log.id)
      }
    },
    batchDeleteLogs(ids) {
      if(confirm(`確定要刪除選中的 ${ids.length} 筆日誌嗎？`)) {
        this.logs = this.logs.filter(l => !ids.includes(l.id))
      }
    }
  }
}
</script> 