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
      <div v-for="category in uniqueCategories" :key="category" class="space-y-3 bg-white rounded-lg p-6">
        <h3 class="text-lg font-medium text-gray-700 px-2 mb-4">{{ category }}</h3>
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
          class="space-y-3 px-2"
          handle=".handle">
          <template #item="{ element: menu }">
            <div>
              <div class="flex items-center bg-gray-50 p-4 rounded-lg hover:shadow transition-shadow duration-200">
                <div class="handle cursor-move mr-4 text-gray-400 hover:text-gray-600">
                  <i class="fas fa-grip-vertical"></i>
                </div>
                <!-- 主選單 -->
                <div class="flex items-center space-x-3">
                  <i :class="['text-xl', menu.icon]"></i>
                  <div>
                    <h3 class="font-medium text-gray-900">{{ menu.name }}</h3>
                    <p class="text-sm text-gray-500">{{ menu.path }}</p>
                  </div>
                </div>
                <div class="ml-auto flex items-center space-x-2">
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
                     class="flex justify-between items-center bg-white rounded-lg p-4">
                  <div class="flex items-center space-x-3">
                    <i :class="['text-lg', submenu.icon]"></i>
                    <div>
                      <h4 class="font-medium text-gray-800">{{ submenu.name }}</h4>
                      <p class="text-sm text-gray-500">{{ submenu.path }}</p>
                    </div>
                  </div>
                  <div class="flex items-center space-x-2">
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
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white rounded-xl p-8 w-full max-w-md">
        <h2 class="text-xl font-bold mb-6">
          {{ editingMenu ? '編輯選單' : isSubmenu ? '新增子選單' : '新增主選單' }}
        </h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">選單名稱</label>
            <input type="text" v-model="menuForm.name" 
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">選單類別</label>
            <select v-model="menuForm.category" 
                    class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                    @change="handleCategoryChange">
              <option value="">請選擇類別</option>
              <option v-for="category in categories" 
                      :key="category" 
                      :value="category">
                {{ category }}
              </option>
              <option value="new">+ 新增類別</option>
            </select>
          </div>
          <!-- 新增類別的輸入框 -->
          <div v-if="menuForm.category === 'new'">
            <label class="block text-sm font-medium text-gray-700 mb-2">新類別名稱</label>
            <input type="text" v-model="newCategory" 
                    class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">路徑</label>
            <input type="text" v-model="menuForm.path" 
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">圖示</label>
            <div class="flex space-x-2">
              <input type="text" v-model="menuForm.icon" 
                     class="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
              <button @click="showIconPicker = true"
                      class="px-4 py-2 bg-gray-100 rounded-lg hover:bg-gray-200">
                <i class="fas fa-icons"></i>
              </button>
            </div>
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
        <div class="mt-8 flex justify-end space-x-4">
          <button @click="closeModal" 
                  class="px-4 py-2 text-gray-700 border rounded-lg hover:bg-gray-50">
            取消
          </button>
          <button @click="saveMenu" 
                  class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
            確認
          </button>
        </div>
      </div>
    </div>

    <!-- 圖示選擇器 -->
    <div v-if="showIconPicker"
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white rounded-xl p-6 w-full max-w-2xl">
        <h3 class="text-lg font-bold mb-4">選擇圖示</h3>
        <div class="grid grid-cols-8 gap-4 max-h-96 overflow-y-auto">
          <button v-for="icon in commonIcons" 
                  :key="icon"
                  @click="selectIcon(icon)"
                  class="p-3 hover:bg-gray-100 rounded-lg text-xl">
            <i :class="icon"></i>
          </button>
        </div>
        <div class="mt-6 flex justify-end">
          <button @click="showIconPicker = false" 
                  class="px-4 py-2 text-gray-700 border rounded-lg hover:bg-gray-50">
            關閉
          </button>
        </div>
      </div>
    </div>

    <BackToHome />
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import draggable from 'vuedraggable'
import BackToHome from '../common/BackToHome.vue'
import { menuAPI } from '@/api'
import { useLogger } from '@/composables/useLogger'
import Swal from 'sweetalert2'

export default defineComponent({
  name: 'MenuManagement',
  components: {
    draggable,
    BackToHome
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
      menuForm: {
        name: '',
        path: '',
        icon: '',
        description: '',
        status: 'active',
        category: ''
      },
      commonIcons: [
        // 導航和基礎圖示
        'fas fa-home', 'fas fa-dashboard', 'fas fa-compass', 'fas fa-map',
        'fas fa-bars', 'fas fa-th-large', 'fas fa-th-list', 'fas fa-list',
        
        // 系統和設置
        'fas fa-cog', 'fas fa-wrench', 'fas fa-tools', 'fas fa-sliders-h',
        'fas fa-database', 'fas fa-server', 'fas fa-shield-alt', 'fas fa-lock',
        
        // 用戶和人員
        'fas fa-user', 'fas fa-users', 'fas fa-user-circle', 'fas fa-user-cog',
        'fas fa-user-shield', 'fas fa-user-tie', 'fas fa-user-tag', 'fas fa-id-card',
        
        // 商務和金融
        'fas fa-shopping-cart', 'fas fa-cash-register', 'fas fa-credit-card', 'fas fa-wallet',
        'fas fa-dollar-sign', 'fas fa-chart-line', 'fas fa-chart-bar', 'fas fa-chart-pie',
        
        // 通訊和社交
        'fas fa-envelope', 'fas fa-comment', 'fas fa-comments', 'fas fa-bell',
        'fas fa-phone', 'fas fa-video', 'fas fa-share-alt', 'fas fa-rss',
        
        // 文件和編輯
        'fas fa-file', 'fas fa-file-alt', 'fas fa-folder', 'fas fa-folder-open',
        'fas fa-edit', 'fas fa-pen', 'fas fa-trash', 'fas fa-copy',
        
        // 餐飲和服務
        'fas fa-utensils', 'fas fa-coffee', 'fas fa-glass-cheers', 'fas fa-hamburger',
        'fas fa-pizza-slice', 'fas fa-wine-glass', 'fas fa-concierge-bell', 'fas fa-cookie',
        
        // 其他實用圖示
        'fas fa-star', 'fas fa-heart', 'fas fa-bookmark', 'fas fa-tag',
        'fas fa-gift', 'fas fa-trophy', 'fas fa-crown', 'fas fa-award',
        
        // 箭頭和導航
        'fas fa-arrow-right', 'fas fa-arrow-left', 'fas fa-chevron-right', 'fas fa-chevron-down',
        'fas fa-plus', 'fas fa-minus', 'fas fa-times', 'fas fa-check',
        
        // 時間和日期
        'fas fa-clock', 'fas fa-calendar', 'fas fa-calendar-alt', 'fas fa-history',
        'fas fa-hourglass', 'fas fa-stopwatch', 'fas fa-bell-slash', 'fas fa-sync'
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
      const errors = []
      if (!this.menuForm.name?.trim()) {
        errors.push('選單名稱不能為空')
      }
      if (!this.menuForm.path?.trim()) {
        errors.push('路徑不能為空')
      }
      if (!this.menuForm.icon?.trim()) {
        errors.push('圖示不能為空')
      }
      
      if (errors.length > 0) {
        await Swal.fire({
          icon: 'warning',
          title: '表單驗證錯誤',
          html: errors.join('<br>'),
          confirmButtonText: '確定'
        })
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
      this.resetForm()
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
</style> 