<template>
  <div class="min-h-screen max-w-7xl mx-auto px-4">

    <!-- 搜尋條件 -->
    <div class="mb-6 bg-white/50 backdrop-blur-sm rounded-xl shadow-sm overflow-hidden border border-white/20">
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700 required-field">Flow ID</label>
            <input type="text" 
                   v-model="searchForm.flow_id"
                   placeholder="請輸入 Flow ID"
                   class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">Session ID</label>
            <input type="text"
                   v-model="searchForm.session_id"
                   placeholder="請輸入 Session ID"
                   class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">發送者</label>
            <select v-model="searchForm.sender"
                    class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="">全部</option>
              <option value="User">使用者</option>
              <option value="Machine">機器人</option>
            </select>
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">發送者名稱</label>
            <input type="text"
                   v-model="searchForm.sender_name"
                   placeholder="請輸入發送者名稱"
                   class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">排序欄位</label>
            <select v-model="searchForm.order_by"
                    class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="-timestamp">時間戳記 (新到舊)</option>
              <option value="timestamp">時間戳記 (舊到新)</option>
            </select>
          </div>
        </div>
        <div class="mt-2 flex justify-end">
          <button @click="handleSearch"
                  class="monitor-search-btn px-6 py-2.5 bg-purple-500 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 flex items-center space-x-2">
            <i class="fas fa-search text-white"></i>
            <span>查詢</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 查詢結果 -->
    <div class="bg-white/50 backdrop-blur-sm rounded-xl shadow-sm overflow-hidden border border-white/20">
      <div class="p-6">
        <!-- 批量操作 -->
        <div v-if="selectedMessages.length > 0" 
             class="mb-4 flex justify-between items-center">
          <span class="text-sm text-gray-600">
            已選擇 {{ selectedMessages.length }} 筆對話
          </span>
          <button @click="batchDeleteMessages"
                  class="px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors flex items-center space-x-2">
            <i class="fas fa-trash-alt"></i>
            <span>批量刪除</span>
          </button>
        </div>

        <!-- 對話列表 -->
        <div class="space-y-6">
          <div v-for="group in groupedMessages" 
               :key="group.sessionId"
               class="bg-white rounded-xl border border-gray-100 shadow-sm hover:border-blue-200 transition-all">
            <!-- 對話群組標題 -->
            <div class="px-4 py-3 border-b border-gray-100 bg-gray-50 rounded-t-xl flex justify-between items-center">
              <div class="flex items-center space-x-3">
                <span class="text-sm font-medium text-gray-700">對話時間：{{ formatTime(group.messages[0].timestamp) }}</span>
                <span class="text-xs text-gray-500">對話編號: {{ group.sessionId }}</span>
              </div>
              <button @click="handleDelete(group.sessionId)"
                      class="text-gray-400 hover:text-red-500 transition-colors">
                <i class="fas fa-trash-alt"></i>
              </button>
            </div>
            
            <!-- 對話內容列表 -->
            <div class="divide-y divide-gray-100">
              <div v-for="message in group.messages"
                   :key="message.id"
                   class="p-4 hover:bg-gray-50 transition-colors">
                <div class="flex items-start space-x-3">
                  <!-- 發送者頭像 -->
                  <div :class="[
                    'w-8 h-8 rounded-full flex items-center justify-center',
                    message.sender === 'Machine' ? 'bg-blue-100' : 'bg-gray-100'
                  ]">
                    <i :class="[
                      'text-sm',
                      message.sender === 'Machine' ? 'fas fa-robot text-blue-500' : 'fas fa-user text-gray-500'
                    ]"></i>
                  </div>
                  <!-- 訊息內容 -->
                  <div class="flex-1">
                    <div class="flex items-center space-x-2 mb-1">
                      <span class="text-sm font-medium" 
                            :class="message.sender === 'Machine' ? 'text-blue-600' : 'text-gray-700'">
                        {{ getSenderDisplayName(message.sender) }}
                      </span>
                      <span class="text-xs text-gray-400">{{ formatTime(message.timestamp) }}</span>
                    </div>
                    <p class="text-gray-600 text-sm">{{ getMessageContent(message) }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 無資料提示 -->
        <div v-if="messages.length === 0" 
             class="py-12 text-center text-gray-500">
          <i class="fas fa-inbox text-4xl mb-3"></i>
          <p>尚無對話記錄</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import monitorAPI from '@/api/modules/monitor'
import { useLogger } from '@/composables/useLogger'
import Swal from 'sweetalert2'
import dayjs from 'dayjs'
import { ElMessage } from 'element-plus'

export default {
  name: 'MonitorManagement',
  
  setup() {
    const { logOperation } = useLogger()

    const searchForm = ref({
      flow_id: '',  // 預設值
      session_id: '',
      sender: '',
      sender_name: '',
      order_by: '-timestamp'  // 預設為新到舊
    })
    
    const messages = ref([])
    const selectedMessages = ref([])
    
    // 計算排序後的訊息列表
    const groupedMessages = computed(() => {
      // 先將訊息按時間排序
      const sortedMessages = [...messages.value].sort((a, b) => {
        return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
      })
      
      // 根據時間間隔分組
      const groups = []
      let currentGroup = []
      
      sortedMessages.forEach((message, index) => {
        if (index === 0) {
          currentGroup.push(message)
          return
        }
        
        const currentTime = new Date(message.timestamp).getTime()
        const prevTime = new Date(sortedMessages[index - 1].timestamp).getTime()
        const timeDiff = (currentTime - prevTime) / (1000 * 60) // 轉換為分鐘
        
        // 如果時間間隔超過1分鐘，創建新的群組
        if (timeDiff > 1) {
          if (currentGroup.length > 0) {
            groups.push({
              sessionId: currentGroup[0].session_id,
              messages: currentGroup,
              firstMessageTime: new Date(currentGroup[0].timestamp).getTime()
            })
          }
          currentGroup = []
        }
        
        currentGroup.push(message)
      })
      
      // 添加最後一組對話
      if (currentGroup.length > 0) {
        groups.push({
          sessionId: currentGroup[0].session_id,
          messages: currentGroup,
          firstMessageTime: new Date(currentGroup[0].timestamp).getTime()
        })
      }

      // 根據排序設定對群組進行排序
      return groups.sort((a, b) => {
        return searchForm.value.order_by === '-timestamp'
          ? b.firstMessageTime - a.firstMessageTime
          : a.firstMessageTime - b.firstMessageTime
      })
    })
    
    // 查詢對話記錄
    const handleSearch = async () => {
      try {
        const response = await monitorAPI.getMonitorMessages({
          flow_id: searchForm.value.flow_id,
          session_id: searchForm.value.session_id,
          sender: searchForm.value.sender,
          sender_name: searchForm.value.sender_name
        })
        messages.value = response.data.messages || []
        await logOperation('【對話監控】查詢對話記錄', '查詢')
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: '查詢失敗',
          text: error.response?.data?.message || '請稍後再試'
        })
      }
    }
    
    // 刪除單筆對話
    const deleteMessage = async (messageId) => {
      try {
        await Swal.fire({
          title: '確定要刪除此對話嗎？',
          text: '此操作無法復原',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: '確定刪除',
          cancelButtonText: '取消'
        }).then(async (result) => {
          if (result.isConfirmed) {
            await monitorAPI.deleteMessage(messageId)
            messages.value = messages.value.filter(msg => msg.id !== messageId)
            Swal.fire('刪除成功', '', 'success')
          }
        })
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: '刪除失敗',
          text: error.response?.data?.message || '請稍後再試'
        })
      }
    }
    
    // 批量刪除對話
    const batchDeleteMessages = async () => {
      try {
        await Swal.fire({
          title: `確定要刪除 ${selectedMessages.value.length} 筆對話嗎？`,
          text: '此操作無法復原',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: '確定刪除',
          cancelButtonText: '取消'
        }).then(async (result) => {
          if (result.isConfirmed) {
            await monitorAPI.batchDeleteMessages(selectedMessages.value)
            messages.value = messages.value.filter(msg => !selectedMessages.value.includes(msg.id))
            selectedMessages.value = []
            Swal.fire('刪除成功', '', 'success')
          }
        })
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: '批量刪除失敗',
          text: error.response?.data?.message || '請稍後再試'
        })
      }
    }
    
    // 檢查訊息是否被選中
    const isMessageSelected = (messageId) => {
      return selectedMessages.value.includes(messageId)
    }
    
    // 切換訊息選擇狀態
    const toggleMessageSelection = (messageId) => {
      const index = selectedMessages.value.indexOf(messageId)
      if (index === -1) {
        selectedMessages.value.push(messageId)
      } else {
        selectedMessages.value.splice(index, 1)
      }
    }
    
    // 格式化時間
    const formatTime = (timestamp) => {
      return dayjs(timestamp).format('YYYY-MM-DD HH:mm:ss')
    }
    
    // 在顯示訊息時轉換發送者名稱
    const getSenderDisplayName = (sender) => {
      switch(sender) {
        case 'Machine':
          return '機器人'
        case 'User':
          return '使用者'
        default:
          return sender
      }
    }
    
    // 取得訊息內容
    const getMessageContent = (message) => {
      try {
        // 檢查是否有 content_blocks
        if (message.content_blocks && message.content_blocks.length > 0) {
          // 取得第一個 content block 的 text
          return message.content_blocks[0].text || '無內容'
        }
        // 如果沒有 content_blocks，嘗試直接取得 text
        if (message.text) {
          return message.text
        }
        return '無內容'
      } catch (error) {
        console.error('解析訊息內容錯誤:', error)
        return '無法顯示內容'
      }
    }
    
    // 處理刪除
    const handleDelete = async (sessionId) => {
      try {
        // 使用 SweetAlert2 顯示確認對話框
        const result = await Swal.fire({
          title: '確定要刪除此對話嗎？',
          text: '此操作無法復原',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: '確定刪除',
          cancelButtonText: '取消',
          confirmButtonColor: '#d33',
          cancelButtonColor: '#3085d6'
        })
        
        // 如果用戶確認刪除
        if (result.isConfirmed) {
          await monitorAPI.deleteMessage(sessionId)
          await Swal.fire({
            title: '刪除成功！',
            icon: 'success',
            timer: 1500,
            showConfirmButton: false
          })
          // 重新加載對話列表
          await handleSearch()
        }
      } catch (error) {
        console.error('Delete Error:', error)
        await Swal.fire({
          title: '刪除失敗',
          text: error.response?.data?.message || error.message,
          icon: 'error'
        })
      }
    }
    
    onMounted(async () => {
      await logOperation('【對話監控】訪問對話監控頁面', '查看')
    })
    
    return {
      searchForm,
      messages,
      groupedMessages,
      selectedMessages,
      handleSearch,
      deleteMessage,
      batchDeleteMessages,
      isMessageSelected,
      toggleMessageSelection,
      formatTime,
      getSenderDisplayName,
      getMessageContent,
      handleDelete
    }
  }
}
</script> 