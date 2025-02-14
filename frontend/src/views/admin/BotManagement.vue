<template>
  <div>
    <!-- 無資料時顯示 -->
    <div v-if="!bots || bots.length === 0" 
         class="bg-white rounded-lg shadow-sm p-8 text-center">
      <div class="text-gray-500 mb-4">
        <i class="fas fa-robot text-4xl"></i>
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">
        尚無快速提問資料
      </h3>
      <p class="text-gray-500 mb-4">
        目前還沒有任何快速提問或預設訊息，點擊下方按鈕新增。
      </p>
      <button @click="showAddModal = true"
              class="inline-flex items-center px-4 py-2 bg-blue-50 text-blue-600 rounded-md hover:bg-blue-100 transition-colors duration-200">
        <i class="fas fa-plus mr-2"></i>
        新增問答
      </button>
    </div>

    <!-- 有資料時顯示表格 -->
    <div v-else>
      <DataTable
        :columns="columns"
        :data="bots"
        :showAddButton="true"
        :selectable="true"
        @add="showAddModal = true"
        @edit="editBot"
        @delete="deleteBot"
        @batch-delete="batchDeleteBots">
        <!-- 自定義狀態列 -->
        <template #is_active="{ item }">
          <span :class="[
            'px-2 py-1 text-xs rounded-full',
            item.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          ]">
            {{ item.is_active ? '啟用' : '停用' }}
          </span>
        </template>
        <!-- 自定義預設訊息列 -->
        <template #is_default="{ item }">
          <span :class="[
            'px-2 py-1 text-xs rounded-full',
            item.is_default ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
          ]">
            {{ item.is_default ? '預設訊息' : '快速提問' }}
          </span>
        </template>
        <!-- 自定義圖示列 -->
        <template #icon="{ item }">
          <div class="w-8 h-8 flex items-center justify-center">
            <i :class="[item.icon || 'fas fa-robot', 'text-xl text-gray-600']"></i>
          </div>
        </template>
      </DataTable>
    </div>

    <!-- 新增/編輯彈窗 -->
    <div v-if="showAddModal" 
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center overflow-y-auto py-8">
      <div class="bg-white rounded-xl p-6 w-full max-w-2xl mx-4 relative">
        <!-- 標題列 -->
        <div class="flex justify-between items-center mb-6 pb-4 border-b">
          <h2 class="text-xl font-bold">{{ editingBot ? '編輯問答' : '新增問答' }}</h2>
          <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
            <i class="fas fa-times text-xl"></i>
          </button>
        </div>

        <!-- 表單內容區域 -->
        <div class="max-h-[calc(100vh-200px)] overflow-y-auto pr-2">
          <div class="space-y-4">
            <!-- Icon 選擇器 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">選擇圖示</label>
              <div class="flex items-center space-x-2 mb-2">
                <div class="w-10 h-10 flex items-center justify-center bg-gray-100 rounded-lg">
                  <i :class="[botForm.icon || 'fas fa-robot', 'text-xl text-gray-600']"></i>
                </div>
                <span class="text-sm text-gray-500">已選擇的圖示</span>
              </div>
              <div class="border rounded-lg p-3">
                <div class="grid grid-cols-2 gap-4 mb-4">
                  <button 
                    v-for="(category, index) in iconCategories" 
                    :key="index"
                    @click="selectedCategory = category.name"
                    :class="[
                      'px-3 py-2 rounded-lg text-sm font-medium',
                      selectedCategory === category.name 
                        ? 'bg-blue-500 text-white' 
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    ]">
                    <i :class="category.icon" class="mr-2"></i>
                    {{ category.label }}
                  </button>
                </div>
                <div class="h-32 overflow-y-auto">
                  <div class="grid grid-cols-8 gap-2">
                    <button
                      v-for="icon in getCurrentCategoryIcons"
                      :key="icon"
                      @click="selectIcon(icon)"
                      :class="[
                        'w-8 h-8 rounded-lg flex items-center justify-center',
                        botForm.icon === icon 
                          ? 'bg-blue-500 text-white' 
                          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                      ]">
                      <i :class="icon"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">快速問答名稱</label>
              <input type="text"
                     v-model="botForm.title"
                     :class="{'border-red-500': errors.title}"
                     class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
              <span v-if="errors.title" class="text-red-500 text-xs mt-1">{{ errors.title }}</span>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">訊息內容</label>
              <textarea v-model="botForm.message"
                        :class="{'border-red-500': errors.message}"
                        class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                        rows="4"></textarea>
              <span v-if="errors.message" class="text-red-500 text-xs mt-1">{{ errors.message }}</span>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">排序</label>
              <input type="number"
                     v-model="botForm.sort_order"
                     :class="{'border-red-500': errors.sort_order}"
                     class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
              <span v-if="errors.sort_order" class="text-red-500 text-xs mt-1">{{ errors.sort_order }}</span>
            </div>
            <div class="flex items-center space-x-4">
              <div class="flex items-center">
                <input type="checkbox"
                       v-model="botForm.is_active"
                       class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                <label class="ml-2 text-sm text-gray-700">啟用</label>
              </div>
              <div class="flex items-center">
                <input type="checkbox"
                       v-model="botForm.is_default"
                       class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                <label class="ml-2 text-sm text-gray-700">設為預設訊息</label>
              </div>
            </div>
          </div>
        </div>

        <!-- 底部按鈕區域 -->
        <div class="mt-6 pt-4 border-t flex justify-end space-x-4 bg-white">
          <button @click="closeModal"
                  class="px-4 py-2 text-gray-600 hover:text-gray-800 border rounded-lg">
            取消
          </button>
          <button @click="saveBot"
                  class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
            確定
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import DataTable from '@/components/admin/common/DataTable.vue'
import { botAPI } from '@/api'
import { useLogger } from '@/composables/useLogger'
import Swal from 'sweetalert2'

export default {
  name: 'BotManagement',
  components: {
    DataTable
  },
  setup() {
    const { logOperation } = useLogger()
    const bots = ref([])
    const showAddModal = ref(false)
    const editingBot = ref(null)
    const selectedCategory = ref('common')
    const botForm = ref({
      title: '',
      message: '',
      sort_order: 1,
      is_active: true,
      is_default: false,
      icon: 'fas fa-robot'
    })
    const errors = ref({})

    // Icon 分類
    const iconCategories = [
      { 
        name: 'common',
        label: '常用圖示',
        icon: 'fas fa-star',
        icons: [
          'fas fa-robot', 'fas fa-comment', 'fas fa-comments', 
          'fas fa-question-circle', 'fas fa-info-circle', 'fas fa-exclamation-circle',
          'fas fa-lightbulb', 'fas fa-bell'
        ]
      },
      {
        name: 'food',
        label: '餐飲圖示',
        icon: 'fas fa-utensils',
        icons: [
          'fas fa-utensils', 'fas fa-coffee', 'fas fa-glass-martini',
          'fas fa-beer', 'fas fa-wine-glass', 'fas fa-hamburger',
          'fas fa-pizza-slice', 'fas fa-ice-cream'
        ]
      },
      {
        name: 'interface',
        label: '介面圖示',
        icon: 'fas fa-desktop',
        icons: [
          'fas fa-home', 'fas fa-search', 'fas fa-cog', 
          'fas fa-user', 'fas fa-heart', 'fas fa-star',
          'fas fa-bookmark', 'fas fa-envelope'
        ]
      },
      {
        name: 'action',
        label: '動作圖示',
        icon: 'fas fa-play',
        icons: [
          'fas fa-plus', 'fas fa-minus', 'fas fa-edit',
          'fas fa-trash', 'fas fa-save', 'fas fa-download',
          'fas fa-upload', 'fas fa-sync'
        ]
      }
    ]

    // 獲取當前分類的圖示
    const getCurrentCategoryIcons = computed(() => {
      const category = iconCategories.find(c => c.name === selectedCategory.value)
      return category ? category.icons : []
    })

    // 選擇圖示
    const selectIcon = (icon) => {
      botForm.value.icon = icon
    }

    // 在 columns 中加入 icon 列
    const columns = [
      { key: 'icon', label: '圖示' },
      { key: 'title', label: '快速問答名稱' },
      { key: 'message', label: '訊息內容' },
      { key: 'sort_order', label: '排序' },
      { key: 'is_active', label: '狀態' },
      { key: 'is_default', label: '類型' }
    ]

    // 獲取問答列表
    const fetchBots = async () => {
      try {
        const response = await botAPI.getBots()
        bots.value = response.data.bots || []
      } catch (error) {
        console.error('獲取問答列表失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '獲取問答列表失敗'
        })
      }
    }

    // 編輯問答
    const editBot = (bot) => {
      editingBot.value = bot
      botForm.value = { ...bot }
      showAddModal.value = true
    }

    // 刪除問答
    const deleteBot = async (bot) => {
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
          await botAPI.deleteBot(bot.id)
          await fetchBots()
          await logOperation(`【快速提問管理】刪除問答 ${bot.id}`, '刪除')
          Swal.fire({
            icon: 'success',
            title: '已刪除',
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
    const batchDeleteBots = async (ids) => {
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
          await Promise.all(ids.map(id => botAPI.deleteBot(id)))
          await fetchBots()
          await logOperation(`【快速提問管理】批量刪除問答 (${ids.length} 筆)`, '刪除')
          Swal.fire({
            icon: 'success',
            title: '已刪除',
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

    // 儲存問答
    const saveBot = async () => {
      try {
        // 驗證
        errors.value = {}
        if (!botForm.value.title?.trim()) {
          errors.value.title = '請輸入快速問答名稱'
          return
        }
        if (!botForm.value.message?.trim()) {
          errors.value.message = '請輸入訊息內容'
          return
        }
        // 驗證排序
        const sortOrder = parseInt(botForm.value.sort_order)
        if (isNaN(sortOrder) || sortOrder < 1) {
          errors.value.sort_order = '排序必須大於等於1'
          return
        }
        // 檢查排序是否重複
        const existingBot = bots.value.find(bot => 
          bot.sort_order === sortOrder && 
          (!editingBot.value || bot.id !== editingBot.value.id)
        )
        if (existingBot) {
          errors.value.sort_order = '此排序已被使用'
          return
        }

        if (editingBot.value) {
          await botAPI.updateBot(editingBot.value.id, botForm.value)
          await logOperation(`【快速提問管理】更新問答 ${editingBot.value.id}`, '修改')
        } else {
            console.log(botForm.value)
          await botAPI.createBot(botForm.value)
          await logOperation('【快速提問管理】新增問答', '新增')
        }

        await fetchBots()
        showAddModal.value = false
        Swal.fire({
          icon: 'success',
          title: `${editingBot.value ? '更新' : '新增'}成功`,
          timer: 1500,
          showConfirmButton: false
        })
      } catch (error) {
        console.error('儲存失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: error.response?.data?.message || '儲存失敗'
        })
      }
    }

    const closeModal = () => {
      showAddModal.value = false
      editingBot.value = null
      botForm.value = {
        title: '',
        message: '',
        sort_order: 1,
        is_active: true,
        is_default: false,
        icon: 'fas fa-robot'
      }
      errors.value = {}
      selectedCategory.value = 'common'
    }

    onMounted(async () => {
      await fetchBots()
      await logOperation('【快速提問管理】訪問快速提問管理頁面', '查看')
    })

    return {
      bots,
      columns,
      showAddModal,
      editingBot,
      botForm,
      errors,
      editBot,
      deleteBot,
      batchDeleteBots,
      saveBot,
      closeModal,
      iconCategories,
      selectedCategory,
      getCurrentCategoryIcons,
      selectIcon
    }
  }
}
</script>

<style scoped>
/* 自定義滾動條樣式 */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style> 