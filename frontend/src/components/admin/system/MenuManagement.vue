<template>
  <div class="container mx-auto px-4">
    <!-- 主功能區塊排序 -->
    <div class="mb-8">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold">主功能區塊排序</h2>
        <div class="text-sm text-gray-500">拖曳調整順序</div>
      </div>
      <draggable
        v-model="menuSections"
        @change="onSectionDragChange"
        item-key="category"
        handle=".section-handle"
        :animation="200"
        ghost-class="ghost-section"
        class="space-y-3">
        <template #item="{ element: section }">
          <div class="flex items-center bg-white p-4 rounded-lg shadow-sm hover:shadow transition-shadow duration-200">
            <div class="section-handle cursor-move mr-4 text-gray-400 hover:text-gray-600">
              <i class="fas fa-grip-vertical"></i>
            </div>
            <div class="flex items-center space-x-3">
              <i :class="[getSectionIcon(section.category), 'text-lg text-gray-600']"></i>
              <span class="font-medium text-gray-700">{{ section.category }}</span>
            </div>
            <div class="ml-auto text-sm text-gray-500">
              {{ getMenuCountByCategory(section.category) }} 個選單項目
            </div>
          </div>
        </template>
      </draggable>
    </div>

    <!-- 次功能區塊排序 -->
    <div class="space-y-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold">次功能區塊排序</h2>
        <div class="text-sm text-gray-500">拖曳調整順序</div>
      </div>
      
      <!-- 按類別分組顯示選單 -->
      <div v-for="category in uniqueCategories" :key="category" class="bg-white rounded-lg p-6">
        <h3 class="text-lg font-medium text-gray-700 mb-4">{{ category }}</h3>
        <draggable 
          v-model="menusByCategory[category]"
          :component-data="{
            tag: 'div',
            type: 'transition-group',
            name: 'menu-list'
          }"
          item-key="id"
          :group="{ name: 'menus' }"
          @start="drag=true" 
          @end="drag=false"
          @change="onDragChange"
          class="space-y-3"
          handle=".handle">
          <template #item="{ element: menu }">
            <div class="w-full">
              <!-- 主選單項目 -->
              <div class="flex items-center bg-gray-50 p-4 rounded-lg hover:shadow transition-shadow duration-200">
                <div class="handle cursor-move mr-4 text-gray-400 hover:text-gray-600">
                  <i class="fas fa-grip-vertical"></i>
                </div>
                
                <!-- 選單資訊 -->
                <div class="flex-1 min-w-0 flex items-center space-x-3">
                  <i :class="['text-xl', menu.icon]"></i>
                  <div class="min-w-0 flex-1">
                    <h3 class="font-medium text-gray-900 truncate">{{ menu.name }}</h3>
                    <p class="text-sm text-gray-500 truncate">{{ menu.path }}</p>
                  </div>
                </div>

                <!-- 操作按鈕 -->
                <div class="flex items-center space-x-2 flex-shrink-0">
                  <button @click="addSubmenu(menu)" 
                          class="p-1.5 text-gray-600 hover:text-green-600 rounded-full hover:bg-green-50">
                    <i class="fas fa-plus"></i>
                  </button>
                  <button @click="editMenu(menu)" 
                          class="p-1.5 text-gray-600 hover:text-blue-600 rounded-full hover:bg-blue-50">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button @click="deleteMenu(menu)" 
                          class="p-1.5 text-gray-600 hover:text-red-600 rounded-full hover:bg-red-50">
                    <i class="fas fa-trash"></i>
                  </button>
                </div>
              </div>
              
              <!-- 子選單列表 -->
              <div v-if="menu.children && menu.children.length" 
                   class="mt-3 ml-12 space-y-3">
                <div v-for="submenu in menu.children" 
                     :key="submenu.id" 
                     class="flex items-center bg-white rounded-lg p-4 hover:shadow transition-shadow duration-200">
                  <div class="flex-1 min-w-0 flex items-center space-x-3">
                    <i :class="['text-lg', submenu.icon]"></i>
                    <div class="min-w-0 flex-1">
                      <h4 class="font-medium text-gray-800 truncate">{{ submenu.name }}</h4>
                      <p class="text-sm text-gray-500 truncate">{{ submenu.path }}</p>
                    </div>
                  </div>
                  
                  <!-- 子選單操作按鈕 -->
                  <div class="flex items-center space-x-2 flex-shrink-0">
                    <button @click="editMenu(submenu)" 
                            class="p-1.5 text-gray-600 hover:text-blue-600 rounded-full hover:bg-blue-50">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="deleteSubmenu(menu, submenu)" 
                            class="p-1.5 text-gray-600 hover:text-red-600 rounded-full hover:bg-red-50">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </draggable>
      </div>
    </div>

    <!-- 新增選單按鈕 -->
    <div @click="showAddModal = true"
         class="mt-4 bg-white rounded-lg shadow-sm p-4 border-2 border-dashed border-gray-300 hover:border-blue-500 cursor-pointer flex items-center justify-center transition-colors">
      <i class="fas fa-plus text-blue-500 mr-2"></i>
      <span class="text-gray-600">新增主選單</span>
    </div>

    <!-- 新增/編輯選單彈窗 -->
    <div v-if="showAddModal" 
        class="fixed inset-0 z-[9999]">
      <!-- 背景遮罩 -->
      <div class="fixed inset-0 bg-black bg-opacity-50"></div>
      
      <!-- Modal 內容 -->
      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <div class="relative bg-white rounded-lg shadow-lg w-full max-w-md">
            <!-- Modal 標題 -->
            <div class="flex justify-between items-center px-6 py-4 border-b">
              <h3 class="text-lg font-semibold">
                {{ editingMenu ? '編輯選單' : isSubmenu ? '新增子選單' : '新增主選單' }}
              </h3>
              <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
                <i class="fas fa-times"></i>
              </button>
            </div>

            <!-- Modal 內容 -->
            <div class="px-6 py-4 space-y-4 max-h-[calc(85vh-8rem)] overflow-y-auto">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  選單名稱 <span class="text-red-500">*</span>
                </label>
                <input type="text" 
                       v-model="menuForm.name"
                       :class="{'border-red-500': errors.title}"
                       class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
                <span v-if="errors.title" class="text-red-500 text-xs mt-1">{{ errors.title }}</span>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  選單類別 <span class="text-red-500">*</span>
                </label>
                <select v-model="menuForm.category" 
                        :class="{'border-red-500': errors.category, 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500': true}"
                        @change="handleCategoryChange">
                  <option value="">請選擇類別</option>
                  <option v-for="category in categories" 
                          :key="category" 
                          :value="category">
                    {{ category }}
                  </option>
                  <option value="new">+ 新增類別</option>
                </select>
                <span v-if="errors.category" class="text-red-500 text-xs mt-1">{{ errors.category }}</span>
              </div>
              <!-- 新增類別的輸入框 -->
              <div v-if="menuForm.category === 'new'">
                <label class="block text-sm font-medium text-gray-700 mb-2">新類別名稱</label>
                <input type="text" v-model="newCategory" 
                        class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  路徑 <span class="text-red-500">*</span>
                </label>
                <input type="text" 
                       v-model="menuForm.path" 
                       :class="{'border-red-500': errors.path, 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500': true}">
                <span v-if="errors.path" class="text-red-500 text-xs mt-1">{{ errors.path }}</span>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  圖示 <span class="text-red-500">*</span>
                </label>
                <div class="flex space-x-2">
                  <input type="text" 
                         v-model="menuForm.icon" 
                         :class="{'border-red-500': errors.icon, 'flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500': true}">
                  <button @click="showIconPicker = true"
                          class="icon-select-label px-4 py-2 bg-gray-100 rounded-lg hover:bg-gray-200">
                    <i class="fas fa-icons"></i>
                  </button>
                </div>
                <span v-if="errors.icon" class="text-red-500 text-xs mt-1">{{ errors.icon }}</span>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">描述</label>
                <textarea v-model="menuForm.description" rows="3"
                          class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"></textarea>
              </div>
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  狀態
                </label>
                <select v-model="menuForm.status"
                        class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option value="active">啟用</option>
                  <option value="disabled">停用</option>
                </select>
              </div>
            </div>

            <!-- Modal 底部按鈕 -->
            <div class="px-6 py-4 bg-gray-50 border-t rounded-b-lg flex justify-end space-x-3">
              <button @click="closeModal" 
                      class="px-4 py-2 text-gray-600 hover:text-gray-800 rounded-lg hover:bg-gray-100 transition-colors">
                取消
              </button>
              <button @click="saveMenu" 
                      class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-sm">
                確認
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 圖示選擇器 -->
    <div v-if="showIconPicker"
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[99999]">
      <div class="bg-white rounded-xl p-6 w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col relative z-[100000]">
        <h3 class="text-lg font-bold mb-4">選擇圖示</h3>
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
                      class="choose-icon p-3 hover:bg-blue-50 rounded-lg text-xl relative group/icon">
            <i :class="icon"></i>
                <span class="absolute bottom-0 left-1/2 -translate-x-1/2 transform px-2 py-1 bg-gray-800 text-white text-xs rounded 
                           opacity-0 group-hover/icon:opacity-100 transition-opacity whitespace-nowrap">
                  {{ icon }}
                </span>
          </button>
            </div>
          </div>
        </div>
        <div class="mt-6 flex justify-end">
          <button @click="showIconPicker = false" 
                  class="px-4 py-2 text-gray-700 border rounded-lg hover:bg-gray-50">
            關閉
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { defineComponent } from 'vue'
import draggable from 'vuedraggable'
import { menuAPI } from '@/api'
import { useLogger } from '@/composables/useLogger'
import Swal from 'sweetalert2'

export default defineComponent({
  name: 'MenuManagement',
  components: {
    draggable
  },
  setup() {
    const { logOperation } = useLogger()
    return { logOperation }
  },
  data() {
    return {
      showAddModal: false,
      showIconPicker: false,
      editingMenu: null,
      isSubmenu: false,
      parentMenu: null,
      drag: false,
      categories: [],
      newCategory: '',
      menus: [],
      menuSections: [],
      isUpdatingOrder: false,
      errors: {
        title: '',
        path: '',
        icon: '',
        category: ''
      },
      menuForm: {
        name: '',
        path: '',
        icon: '',
        description: '',
        status: 'active',
        category: ''
      },
      iconGroups: [
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
      ],
      // 預設類別和路徑的映射
      categoryPathMap: {
        '系統管理': '/admin/system',
        '點餐管理': '/admin/order',
        '個人設定管理': '/admin/personal'
      },
    }
  },
  computed: {
    // 從現有選單中獲取所有唯一的類別
    availableCategories() {
      // 獲取現有選單中的所有類別
      const existingCategories = new Set(this.menus.map(menu => menu.category).filter(Boolean));
      // 合併預設類別和現有類別
      const defaultCategories = ['系統管理', '點餐管理', '個人設定管理'];
      const allCategories = new Set([...defaultCategories, ...existingCategories]);
      return Array.from(allCategories).sort();
    },
    // 獲取所有唯一的類別
    uniqueCategories() {
      // 使用 Set 來確保類別唯一性，並按照 section_order 排序
      const categoryMap = new Map()
      this.menus.forEach(menu => {
        if (menu.category && (!categoryMap.has(menu.category) || menu.section_order < categoryMap.get(menu.category).section_order)) {
          categoryMap.set(menu.category, menu)
        }
      })
      return Array.from(categoryMap.keys())
    },
    // 按類別分組的選單，並保持父子關係
    menusByCategory() {
      return this.uniqueCategories.reduce((acc, category) => {
        // 只過濾頂層選單（沒有父選單的）
        acc[category] = this.menus.filter(menu => 
          menu.category === category && !menu.parent_id
        ).map(menu => ({
          ...menu,
          // 找出所有屬於這個父選單的子選單
          children: this.menus.filter(m => m.parent_id === menu.id)
        }))
        return acc
      }, {})
    }
  },
  watch: {
    // 即時驗證
    'menuForm.name'(val) {
      if (!val) {
        this.errors.title = '請輸入選單名稱'
      } else {
        this.errors.title = ''
      }
    },
    'menuForm.path'(val) {
      if (!val) {
        this.errors.path = '請輸入路徑'
      } else {
        this.errors.path = ''
      }
    },
    'menuForm.icon'(val) {
      if (!val) {
        this.errors.icon = '請選擇圖示'
      } else {
        this.errors.icon = ''
      }
    },
    'menuForm.category'(val) {
      if (!val) {
        this.errors.category = '請選擇類別'
      } else {
        this.errors.category = ''
      }
    }
  },
  methods: {
    editMenu(menu) {
      this.editingMenu = menu
      const status = menu.status === 'active' ? 'active' : 'disabled'
      this.menuForm = { 
        ...menu,
        status: status
      }
      this.showAddModal = true
    },
    addSubmenu(menu) {
      this.isSubmenu = true
      this.parentMenu = menu
      this.menuForm = {
        name: '',
        path: '',
        icon: '',
        description: '',
        status: 'active',
        category: ''
      }
      this.showAddModal = true
    },
    async deleteMenu(menu) {
      try {
        const result = await Swal.fire({
          title: '確定要刪除嗎？',
          text: '此操作無法復原',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: '確定',
          cancelButtonText: '取消'
        })
        
        if (result.isConfirmed) {
          await menuAPI.deleteMenu(menu.id)
          await this.fetchMenus()
          await this.logOperation(`【選單管理】刪除選單 ${menu.name}`, '刪除')
          
          await Swal.fire({
            icon: 'success',
            title: '已刪除',
            text: '選單已成功刪除',
            timer: 1500,
            showConfirmButton: false
          })
        }
      } catch (error) {
        await Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: error.response?.data?.message || '刪除失敗'
        })
        console.error('刪除選單錯誤:', error)
      }
    },
    async deleteSubmenu(parentMenu, submenu) {
      try {
        const result = await Swal.fire({
          title: '確定要刪除嗎？',
          text: '此操作無法復原',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: '確定',
          cancelButtonText: '取消'
        })
        
        if (result.isConfirmed) {
          await menuAPI.deleteMenu(submenu.id)
          await this.fetchMenus()
          await this.logOperation(`【選單管理】刪除子選單 ${submenu.name}`, '刪除')
          
          await Swal.fire({
            icon: 'success',
            title: '已刪除',
            text: '子選單已成功刪除',
            timer: 1500,
            showConfirmButton: false
          })
        }
      } catch (error) {
        await Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: error.response?.data?.message || '刪除失敗'
        })
        console.error('刪除子選單錯誤:', error)
      }
    },
    selectIcon(icon) {
      this.menuForm.icon = icon
      this.showIconPicker = false
    },
    async saveMenu() {
      // 表單驗證
      const isValid = this.validateForm()
      
      if (!isValid) {
        return
      }

      try {
        const formData = {
          ...this.menuForm,
          name: String(this.menuForm.name).trim(),
          path: String(this.menuForm.path).trim(),
          icon: String(this.menuForm.icon).trim(),
          description: String(this.menuForm.description || '').trim(),
          status: this.menuForm.status,
          category: this.menuForm.category === 'new' ? this.newCategory : this.menuForm.category
        }

        // 如果是新類別，添加到類別列表中
        if (this.menuForm.category === 'new' && this.newCategory) {
          // 更新類別列表
          await this.fetchMenus()
          formData.category = this.newCategory
          this.newCategory = ''
        }

        if(this.editingMenu) {
          await menuAPI.updateMenu(this.editingMenu.id, formData)
          await this.logOperation(`【選單管理】編輯選單 ${this.menuForm.name}`, '修改')
        } else if(this.isSubmenu) {
          const data = {
            ...formData,
            parent_id: this.parentMenu.id
          }
          await menuAPI.createMenu(data)
          await this.logOperation(`【選單管理】新增子選單 ${this.menuForm.name}`, '新增')
        } else {
          await menuAPI.createMenu(formData)
          await this.logOperation(`【選單管理】新增主選單 ${this.menuForm.name}`, '新增')
        }

        await this.fetchMenus()
        this.closeModal()
        
        await Swal.fire({
          icon: 'success',
          title: '成功',
          text: '選單已保存',
          timer: 1500,
          showConfirmButton: false
        })

        // 確保資料已更新
        await this.fetchMenus()
      } catch (error) {
        let errorMessage = '保存失敗'
        if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message
        }
        
        await Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: errorMessage,
          confirmButtonText: '確定'
        })
        console.error('保存選單錯誤:', error)
      }
    },
    resetForm() {
      this.menuForm = {
        name: '',
        path: '',
        icon: '',
        description: '',
        status: 'active',
        category: ''
      }
      this.newCategory = ''
      this.editingMenu = null
      this.isSubmenu = false
      this.parentMenu = null
    },
    async fetchMenus() {
      try {
        const response = await menuAPI.getMenus()
        console.log('Raw menus data:', response.data)
        
        // 確保 menus 是數組
        this.menus = response.data.menus || []
        // 更新類別列表
        this.categories = this.availableCategories
        console.log('Processed menus:', this.menus)
      } catch (error) {
        await Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: error.response?.data?.message || '獲取選單列表失敗',
          confirmButtonText: '確定'
        })
        console.error('獲取選單列表錯誤:', error)
      }
    },
    // 初始化類別列表
    initializeCategories() {
      this.categories = this.availableCategories
    },
    closeModal() {
      this.showAddModal = false
      // 重置表單
      this.menuForm = {
        name: '',
        path: '',
        icon: '',
        description: '',
        status: 'active',
        category: ''
      }
      // 重置錯誤訊息
      this.errors = {
        title: '',
        path: '',
        icon: '',
        category: ''
      }
      // 重置其他狀態
      this.editingMenu = null
      this.isSubmenu = false
      this.parentMenu = null
      this.newCategory = ''
      // 清空所有錯誤提示的 border 樣式
      const inputs = document.querySelectorAll('.border-red-500')
      inputs.forEach(input => {
        input.classList.remove('border-red-500')
      })
    },
    async onDragChange(evt) {
      if (!evt.moved && !evt.added && !evt.removed) return
      
      // 如果是移動操作
      if (evt.moved || evt.added || evt.removed) {
        try {
          // 獲取所有選單的最新順序
          const allMenus = []
          
          // 先處理主功能區塊排序
          this.menuSections.forEach((section, index) => {
            const sectionMenus = this.menus.filter(menu => 
              menu.category === section.category && !menu.parent_id
            )
            
            if (sectionMenus.length > 0) {
              sectionMenus.forEach(menu => {
                allMenus.push({
                  id: menu.id,
                  category: section.category,
                  section_order: index + 1,  // 使用 1-based 索引
                  sort_order: menu.sort_order || 0,
                  parent_id: menu.parent_id || null
                })
              })
            }
          })
          
          // 然後處理每個類別內的排序
          Object.entries(this.menusByCategory).forEach(([category, menus]) => {
            menus.forEach((menu, index) => {
              const existingMenu = allMenus.find(m => m.id === menu.id)
              if (existingMenu) {
                existingMenu.sort_order = index
              } else {
                allMenus.push({
                  id: menu.id,
                  category: menu.category,
                  section_order: this.menuSections.findIndex(s => s.category === category) + 1,
                  sort_order: index,
                  parent_id: menu.parent_id || null
                })
              }
            })
          })
          
          // 更新後端排序
          console.log('Updating menu order:', allMenus)
          await menuAPI.updateMenuOrder({ menus: allMenus })
          
          // 重新獲取選單列表以確保順序正確
          await this.fetchMenus()
          await this.fetchMenuSections()
        } catch (error) {
          console.error('更新排序失敗:', error)
          await Swal.fire({
            icon: 'error',
            title: '錯誤',
            text: '更新排序失敗',
            confirmButtonText: '確定'
          })
        }
      }
    },
    // 處理類別選擇變更
    handleCategoryChange() {
      // 如果選擇了預設類別，自動帶出對應路徑
      if (this.menuForm.category && this.menuForm.category !== 'new') {
        const defaultPath = this.categoryPathMap[this.menuForm.category];
        if (defaultPath) {
          this.menuForm.path = defaultPath;
        }
      }
    },
    // 獲取主功能區塊列表
    async fetchMenuSections() {
      try {
        const response = await menuAPI.getMenuSections()
        console.log('Fetched sections:', response.data)
        // 按照 section_order 排序
        const sortedSections = response.data.sections.sort((a, b) => a.section_order - b.section_order)
        // 確保每個類別只出現一次
        const uniqueSections = []
        const seenCategories = new Set()
        sortedSections.forEach(section => {
          if (!seenCategories.has(section.category)) {
            uniqueSections.push(section)
            seenCategories.add(section.category)
          }
        })
        this.menuSections = uniqueSections
      } catch (error) {
        console.error('獲取主功能區塊失敗:', error)
        await Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '獲取主功能區塊列表失敗'
        })
      }
    },
    // 處理主功能區塊拖曳結束
    async onSectionDragChange(evt) {
      if (!evt.moved && !evt.added && !evt.removed) return
      if (this.isUpdatingOrder) return
      
      try {
        this.isUpdatingOrder = true
        console.log('Drag event:', evt)
        
        // 獲取所有選單
        const allMenus = []
        
        // 確保按照當前顯示順序更新
        this.menuSections.forEach((section, index) => {
          // 獲取該類別下的所有頂層選單（沒有父選單的）
          const sectionMenus = this.menus.filter(menu => 
            menu.category === section.category && !menu.parent_id
          )
          
          // 更新該類別的所有選單
          if (sectionMenus.length > 0) {
            sectionMenus.forEach(menu => {
              allMenus.push({
                id: menu.id,
                category: section.category,
                section_order: index + 1,  // 使用 1-based 索引確保不會有 0
                sort_order: menu.sort_order || 0,
                parent_id: menu.parent_id || null
              })
            })
          }
        })
        
        console.log('Updating menu order:', allMenus)
        try {
          await menuAPI.updateMenuOrder({ menus: allMenus })
          
          // 重新獲取數據
          await this.fetchMenus()
          await this.fetchMenuSections()
          await this.logOperation('【選單管理】更新主功能區塊排序', '修改')
        } catch (error) {
          console.error('API Error:', error.response?.data || error)
          throw new Error(error.response?.data?.message || '更新排序失敗')
        }
      } catch (error) {
        console.error('更新主功能區塊排序失敗:', error)
        await Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: error.message || '更新排序失敗'
        })
        // 還原順序
        await this.fetchMenuSections()
      } finally {
        this.isUpdatingOrder = false
      }
    },
    // 獲取主功能區塊圖標
    getSectionIcon(category) {
      const menu = this.menus.find(m => m.category === category)
      return menu?.icon || 'fas fa-folder'
    },
    // 獲取該類別下的選單數量
    getMenuCountByCategory(category) {
      return this.menus.filter(menu => menu.category === category).length
    },
    validateForm() {
      this.errors = {
        title: '',
        path: '',
        icon: '',
        category: ''
      }
      
      let isValid = true
      
      // 驗證選單名稱
      if (!this.menuForm.name) {
        this.errors.title = '請輸入選單名稱'
        isValid = false
      }
      
      // 驗證路徑
      if (!this.menuForm.path) {
        this.errors.path = '請輸入路徑'
        isValid = false
      }
      
      // 驗證圖示
      if (!this.menuForm.icon) {
        this.errors.icon = '請選擇圖示'
        isValid = false
      }
      
      // 驗證類別
      if (!this.menuForm.category) {
        this.errors.category = '請選擇類別'
        isValid = false
      }
      
      return isValid
    },
  },
  async mounted() {
    console.log('MenuManagement mounted')
    await this.fetchMenus()
    this.initializeCategories()
    await this.fetchMenuSections()
    await this.logOperation('【選單管理】訪問選單管理頁面', '查看')
  }
})
</script>

<style scoped>
/* 移除卡片視圖相關樣式，保留列表動畫效果 */
.flip-list-move {
  transition: transform 0.5s;
}
.ghost {
  opacity: 0.5;
  background: #c8ebfb;
}
.drag {
  opacity: 0.9;
}

/* 移除卡片視圖樣式 */
/* 保留列表視圖樣式 */
.list-view {
  @apply space-y-2;
}

.ghost-section {
  opacity: 0.5;
  background: #eef2ff;
}

.section-handle {
  opacity: 0;
  transition: opacity 0.2s;
}

.section-handle:hover {
  opacity: 1;
}

/* 當父元素hover時也顯示拖曳圖標 */
div:hover .section-handle {
  opacity: 1;
}

/* 調整拖曳區域樣式 */
.draggable-container {
  min-height: 50px;
  width: 100%;
}

/* 確保選單項目不會擠壓 */
.menu-item {
  width: 100%;
  min-width: 0;
}

/* 防止文字溢出 */
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 拖曳時的視覺效果 */
.ghost {
  opacity: 0.5;
  background: #f3f4f6 !important;
}

.sortable-chosen {
  background: #ffffff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* 確保子選單縮進正確 */
.submenu-list {
  margin-left: 3rem;
  width: calc(100% - 3rem);
}

/* 確保內容不會溢出容器 */
.menu-content {
  min-width: 0;
  flex: 1;
}
</style> 