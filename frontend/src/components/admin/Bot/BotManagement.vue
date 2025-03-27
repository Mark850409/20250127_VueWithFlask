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
        :showMoreActions="false"
        @add="showAddModal = true"
        @edit="editBot"
        @delete="deleteBot"
        @batch-delete="batchDeleteBots"
        class="overflow-x-auto">
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
        <!-- 自定義訊息內容列 -->
        <template #message="{ item }">
          <div :title="item.message" class="truncate">
            {{ item.message }}
          </div>
        </template>
      </DataTable>
    </div>

    <!-- 新增/編輯彈窗 -->
    <div v-if="showAddModal" 
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-[9999]">
      <div class="bg-white rounded-xl w-full max-w-2xl relative max-h-[85vh] flex flex-col transform transition-all">
        <!-- 標題列 -->
        <div class="flex justify-between items-center px-6 py-4 border-b flex-shrink-0">
          <h2 class="text-xl font-bold">{{ editingBot ? '編輯問答' : '新增問答' }}</h2>
          <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
            <i class="fas fa-times text-xl"></i>
          </button>
        </div>

        <!-- 表單內容區域 -->
        <div class="overflow-y-auto flex-grow px-6 py-4">
          <div class="space-y-4">
            <!-- Icon 選擇器 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">選擇圖示</label>
              <div class="flex items-center space-x-2 mb-2">
                <div class="w-12 h-12 flex items-center justify-center bg-blue-50 rounded-lg 
                            border-2 border-blue-200 shadow-sm transition-all duration-200">
                  <i :class="[botForm.icon || 'fas fa-robot', 'text-2xl text-blue-500']"></i>
                </div>
                <div class="flex flex-col">
                  <span class="text-sm font-medium text-gray-700">已選擇的圖示</span>
                  <span class="text-xs text-gray-500">{{ botForm.icon || '尚未選擇' }}</span>
                </div>
              </div>
              <div class="border rounded-lg p-4">
                <div class="flex-1 overflow-y-auto">
                  <!-- 圖示分類 -->
                  <div v-for="(group, index) in iconGroups" 
                       :key="index" 
                       class="mb-6">
                    <h4 class="text-sm font-medium text-gray-700 mb-3 px-2 flex items-center">
                      <i :class="group.groupIcon" class="mr-2 text-blue-500"></i>
                      {{ group.name }}
                    </h4>
                    <div class="grid grid-cols-8 gap-3">
                      <button v-for="icon in group.icons"
                              :key="icon"
                              @click="selectIcon(icon)"
                              :class="[
                                'p-3 rounded-lg text-xl relative group/icon transition-all duration-200',
                                botForm.icon === icon 
                                  ? 'bg-blue-500 text-white shadow-md transform scale-110' 
                                  : 'hover:bg-blue-50 text-gray-600'
                              ]">
                        <i :class="icon"></i>
                        <span class="absolute bottom-0 left-1/2 -translate-x-1/2 transform px-2 py-1 bg-gray-800 text-white text-xs rounded 
                                 opacity-0 group-hover/icon:opacity-100 transition-all whitespace-nowrap"
                               :class="botForm.icon === icon ? 'bg-blue-600' : 'bg-gray-800'">
                          {{ icon }}
                        </span>
                      </button>
                    </div>
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
        <div class="px-6 py-4 bg-gray-50 border-t rounded-b-xl flex justify-end space-x-3 flex-shrink-0">
          <button @click="closeModal" 
                  class="px-4 py-2 text-gray-600 hover:text-gray-800 rounded-lg hover:bg-gray-100 transition-colors">
            取消
          </button>
          <button @click="saveBot"
                  class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-sm">
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
    const iconGroups = [
    {
          name: 'Arrow 箭頭',
          groupIcon: 'ri-arrow-right-line',
          icons: [
            'ri-arrow-left-line', 'ri-arrow-right-line', 'ri-arrow-up-line', 'ri-arrow-down-line',
            'ri-arrow-left-right-line', 'ri-arrow-up-down-line', 'ri-arrow-drop-left-line',
            'ri-arrow-drop-right-line', 'ri-arrow-go-back-line', 'ri-arrow-go-forward-line'
          ]
        },
        {
          name: 'Buildings 建築',
          groupIcon: 'ri-building-2-line',
          icons: [
            'ri-building-line', 'ri-building-2-line', 'ri-building-3-line', 'ri-building-4-line',
            'ri-hotel-line', 'ri-community-line', 'ri-government-line', 'ri-bank-line',
            'ri-store-2-line', 'ri-hospital-line'
          ]
        },
        {
          name: 'Business 商務',
          groupIcon: 'ri-briefcase-4-line',
          icons: [
            'ri-briefcase-line', 'ri-briefcase-2-line', 'ri-briefcase-4-line', 'ri-calculator-line',
            'ri-calendar-check-line', 'ri-mail-send-line', 'ri-presentation-line', 'ri-pie-chart-line',
            'ri-bar-chart-line', 'ri-line-chart-line'
          ]
        },
        {
          name: 'Communication 通訊',
          groupIcon: 'ri-chat-1-line',
          icons: [
            'ri-message-2-line', 'ri-message-3-line', 'ri-chat-1-line', 'ri-chat-2-line',
            'ri-chat-3-line', 'ri-chat-4-line', 'ri-discuss-line', 'ri-question-answer-line',
            'ri-questionnaire-line', 'ri-chat-voice-line'
          ]
        },
        {
          name: 'Design 設計',
          groupIcon: 'ri-pencil-ruler-2-line',
          icons: [
            'ri-pencil-ruler-2-line', 'ri-paint-brush-line', 'ri-contrast-2-line', 'ri-crop-2-line',
            'ri-drag-move-2-line', 'ri-edit-2-line', 'ri-focus-2-line', 'ri-mark-pen-line',
            'ri-palette-line', 'ri-pantone-line'
          ]
        },
        {
          name: 'Development 開發',
          groupIcon: 'ri-code-s-slash-line',
          icons: [
            'ri-code-line', 'ri-code-s-line', 'ri-code-s-slash-line', 'ri-code-box-line',
            'ri-terminal-box-line', 'ri-bug-2-line', 'ri-git-branch-line', 'ri-git-commit-line',
            'ri-git-merge-line', 'ri-git-pull-request-line'
          ]
        },
        {
          name: 'Document 文件',
          groupIcon: 'ri-file-list-2-line',
          icons: [
            'ri-file-line', 'ri-file-text-line', 'ri-file-list-line', 'ri-file-copy-line',
            'ri-file-pdf-line', 'ri-file-word-line', 'ri-file-excel-line', 'ri-file-ppt-line',
            'ri-folder-line', 'ri-folder-open-line'
          ]
        },
        {
          name: 'Food 食物',
          groupIcon: 'ri-restaurant-2-line',
          icons: [
            'ri-restaurant-line', 'ri-restaurant-2-line', 'ri-cup-line', 'ri-goblet-line',
            'ri-cake-3-line', 'ri-bread-line',  'ri-beer-line',
            'ri-knife-line', 'ri-cooking-pot-line'
          ]
        },
        {
          name: 'Health & Medical 醫療',
          groupIcon: 'ri-heart-pulse-line',
          icons: [
            'ri-heart-pulse-line', 'ri-heart-2-line', 'ri-mental-health-line', 'ri-capsule-line',
            'ri-medicine-bottle-line', 'ri-microscope-line', 'ri-nurse-line', 'ri-pulse-line',
            'ri-stethoscope-line', 'ri-syringe-line'
          ]
        },
        {
          name: 'Logos 品牌',
          groupIcon: 'ri-github-line',
          icons: [
            'ri-github-line', 'ri-google-line', 'ri-facebook-line', 'ri-twitter-line',
            'ri-instagram-line', 'ri-linkedin-line', 'ri-youtube-line', 'ri-discord-line',
            'ri-telegram-line', 'ri-slack-line'
          ]
        },
        {
          name: 'Map 地圖',
          groupIcon: 'ri-map-pin-2-line',
          icons: [
            'ri-map-pin-line', 'ri-map-2-line', 'ri-compass-3-line', 'ri-navigation-line',
            'ri-route-line', 'ri-guide-line', 'ri-earth-line', 'ri-global-line',
            'ri-planet-line', 'ri-flight-takeoff-line'
          ]
        },
        {
          name: 'Media 媒體',
          groupIcon: 'ri-film-line',
          icons: [
            'ri-film-line', 'ri-video-line', 'ri-movie-2-line', 'ri-play-circle-line',
            'ri-music-2-line', 'ri-volume-up-line', 'ri-camera-3-line', 'ri-image-line',
            'ri-gallery-line', 'ri-broadcast-line'
          ]
        },
        {
          name: 'System 系統',
          groupIcon: 'ri-settings-3-line',
          icons: [
            'ri-settings-line', 'ri-settings-2-line', 'ri-settings-3-line', 'ri-settings-4-line',
            'ri-dashboard-line', 'ri-database-2-line', 'ri-server-line', 'ri-cloud-line',
            'ri-shield-line', 'ri-lock-line'
          ]
        },
        {
          name: 'User & Faces 用戶',
          groupIcon: 'ri-user-3-line',
          icons: [
            'ri-user-line', 'ri-user-2-line', 'ri-user-3-line', 'ri-user-4-line',
            'ri-user-settings-line', 'ri-user-search-line', 'ri-team-line', 'ri-group-line',
            'ri-user-heart-line', 'ri-user-star-line'
          ]
        },
        {
          name: 'Git 版控',
          groupIcon: 'ri-git-repository-line',
          icons: [
            'ri-git-repository-line', 'ri-git-repository-private-line', 'ri-git-branch-line',
            'ri-git-commit-line', 'ri-git-merge-line', 'ri-git-pull-request-line',
            'ri-git-repository-commits-line', 'ri-github-line', 'ri-gitlab-line', 'ri-git-fork-line'
          ]
        },
        {
          name: 'Others 其他',
          groupIcon: 'ri-apps-2-line',
          icons: [
            'ri-apps-2-line', 'ri-more-2-line', 'ri-menu-2-line', 'ri-function-line',
            'ri-command-line', 'ri-brush-line', 'ri-magic-line', 'ri-tools-line',
            'ri-box-3-line', 'ri-plug-2-line'
          ]
        },
        {
          name: 'Robot & AI 機器人',
          groupIcon: 'ri-robot-2-line',
          icons: [
            'ri-robot-line', 'ri-robot-2-line', 'ri-robot-3-line', 'ri-ai-generate',
            'ri-brain-line', 'ri-cpu-line',  'ri-code-box-line',
            'ri-android-line', 'ri-openai-line'
          ]
        },
    ]

    // 獲取當前分類的圖示
    const getCurrentCategoryIcons = computed(() => {
      const category = iconGroups.find(c => c.name === selectedCategory.value)
      return category ? category.icons : []
    })

    // 選擇圖示
    const selectIcon = (icon) => {
      botForm.value.icon = icon
    }

    // 在 columns 中加入 icon 列
    const columns = [
      { key: 'icon', label: '圖示', width: '60px' },
      { key: 'title', label: '快速問答名稱', width: '180px' },
      { key: 'message', label: '訊息內容', width: '35%' },
      { key: 'sort_order', label: '排序', width: '80px' },
      { key: 'is_active', label: '狀態', width: '100px' },
      { key: 'is_default', label: '類型', width: '100px' }
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
      logOperation('【快速提問管理】開始編輯問答', '編輯')
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
        
        // 驗證標題
        if (!botForm.value.title?.trim()) {
          errors.value.title = '請輸入快速問答名稱'
          return
        }
        
        // 驗證排序
        const sortOrder = parseInt(botForm.value.sort_order)
        if (!botForm.value.sort_order) {
          errors.value.sort_order = '排序必須大於等於1'
          return
        }
        
        // 驗證排序數字格式
        if (isNaN(sortOrder) || sortOrder < 1) {
          errors.value.sort_order = '排序必須為大於0的數字'
          return
        }
        
        // 檢查排序是否重複
        const existingBot = bots.value.find(bot => 
          bot.sort_order === sortOrder && 
          (!editingBot.value || bot.id !== editingBot.value.id)
        )
        if (existingBot) {
          errors.value.sort_order = `排序 ${sortOrder} 已被使用，請選擇其他數字`
          return
        }
        
        // 驗證圖示
        if (!botForm.value.icon) {
          errors.value.icon = '請選擇圖示'
          return
        }

        // 準備要儲存的資料
        const botData = {
          title: botForm.value.title.trim(),
          message: botForm.value.message?.trim() || '',  // 訊息內容可為空
          sort_order: sortOrder,
          is_active: botForm.value.is_active,
          is_default: botForm.value.is_default,
          icon: botForm.value.icon
        }

        if (editingBot.value) {
          await botAPI.updateBot(editingBot.value.id, botData)
          await logOperation(`【快速提問管理】更新問答 ${editingBot.value.id}`, '修改')
        } else {
          await botAPI.createBot(botData)
          await logOperation('【快速提問管理】新增問答', '新增')
        }

        await fetchBots()
        showAddModal.value = false
        
        // 顯示成功訊息
        Swal.fire({
          icon: 'success',
          title: `${editingBot.value ? '更新' : '新增'}成功！`,
          showConfirmButton: false,
          timer: 1500
        })
      } catch (error) {
        console.error('儲存失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '儲存失敗',
          text: error.response?.data?.message || '請稍後再試'
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
      iconGroups,
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

/* 調整表格容器樣式 */
:deep(.table-container) {
  max-width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

/* 調整表格基本樣式 */
:deep(table) {
  min-width: 1000px;
  width: 100%;
  table-layout: fixed;
  border-collapse: separate;
  border-spacing: 0;
}

/* 調整表格標題和內容的對齊 */
:deep(th),
:deep(td) {
  padding: 12px;
  text-align: left;
  vertical-align: middle;
}

/* 調整訊息內容欄位的顯示 */
:deep(td[data-label="訊息內容"]) {
  max-width: 0; /* 強制使用 text-overflow */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 調整圖示欄位的對齊 */
:deep(td[data-label="圖示"]),
:deep(th[data-label="圖示"]) {
  text-align: center;
  width: 60px;
}

/* 調整排序欄位的對齊 */
:deep(td[data-label="排序"]),
:deep(th[data-label="排序"]) {
  text-align: center;
  width: 80px;
}

/* 調整狀態和類型欄位的對齊 */
:deep(td[data-label="狀態"]),
:deep(th[data-label="狀態"]),
:deep(td[data-label="類型"]),
:deep(th[data-label="類型"]) {
  text-align: center;
  width: 100px;
}

/* 確保標題列樣式 */
:deep(thead) {
  background-color: #f9fafb;
  position: sticky;
  top: 0;
  z-index: 10;
}

:deep(th) {
  font-weight: 600;
  color: #374151;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

/* 移除之前的懸停效果，改用 tooltip */
:deep(td[data-label="訊息內容"]) {
  position: relative;
}

:deep(td[data-label="訊息內容"]):hover::after {
  content: attr(title);
  position: absolute;
  left: 0;
  top: 100%;
  background: white;
  padding: 8px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 20;
  max-width: 400px;
  word-break: break-word;
  white-space: normal;
}
</style> 