<template>
  <div>
    <!-- 移除視圖切換按鈕 -->
    
    <!-- 系統管理區塊 -->
    <div class="bg-white rounded-lg p-6 mb-6">
      <h2 class="text-lg font-medium mb-4">系統管理</h2>
      <div class="space-y-4">
        <draggable 
          v-model="systemMenus"
          :component-data="{
            tag: 'div',
            type: 'transition-group',
            name: 'menu-list'
          }"
          item-key="id"
          :group="{ name: 'system-menus' }"
          @start="drag=true" 
          @end="drag=false"
          handle=".handle"
        >
          <template #item="{element: menu}">
            <div class="bg-white rounded-lg border border-gray-200 p-4 hover:bg-gray-50">
              <div class="flex justify-between items-start">
                <div class="flex items-center space-x-3">
                  <div class="handle cursor-move text-gray-400 hover:text-gray-600">
                    <i class="fas fa-grip-vertical"></i>
                  </div>
                  <i :class="['text-xl', menu.icon]"></i>
                  <div>
                    <h3 class="font-medium text-gray-900">{{ menu.name }}</h3>
                    <p class="text-sm text-gray-500">{{ menu.path }}</p>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
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
                   class="mt-4 pl-8 space-y-3">
                <draggable 
                  v-model="menu.children"
                  :component-data="{
                    tag: 'div',
                    type: 'transition-group',
                    name: 'submenu-list'
                  }"
                  item-key="id"
                  :group="{ name: 'submenus' }"
                  handle=".handle"
                >
                  <template #item="{element: submenu}">
                    <div class="bg-gray-50 rounded-lg p-3 flex justify-between items-center">
                      <div class="flex items-center space-x-3">
                        <div class="handle cursor-move text-gray-400 hover:text-gray-600">
                          <i class="fas fa-grip-vertical"></i>
                        </div>
                        <i :class="['text-lg', submenu.icon]"></i>
                        <div>
                          <h4 class="font-medium text-gray-800">{{ submenu.name }}</h4>
                          <p class="text-xs text-gray-500">{{ submenu.path }}</p>
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
                  </template>
                </draggable>
              </div>
            </div>
          </template>
        </draggable>
      </div>
    </div>

    <!-- 點餐管理區塊 -->
    <div class="bg-white rounded-lg p-6">
      <h2 class="text-lg font-medium mb-4">點餐管理</h2>
      <div :class="[
        viewMode === 'card' ? 'grid grid-cols-1 md:grid-cols-2 gap-4' : 'space-y-4'
      ]">
        <draggable 
          v-model="orderMenus"
          :component-data="{
            tag: 'div',
            type: 'transition-group',
            name: 'menu-list'
          }"
          item-key="id"
          :group="{ name: 'order-menus' }"
          @start="drag=true" 
          @end="drag=false"
          handle=".handle"
        >
          <template #item="{element: menu}">
            <div :class="[
              'transition-all duration-300 ease-in-out',
              viewMode === 'card' 
                ? 'bg-white rounded-lg shadow-sm hover:shadow-md p-6' 
                : 'bg-white rounded-lg border border-gray-200 p-4 hover:bg-gray-50'
            ]">
              <div :class="[
                viewMode === 'card' ? 'flex flex-col space-y-4' : 'flex justify-between items-start'
              ]">
                <div :class="[
                  'flex items-center',
                  viewMode === 'card' ? 'justify-between w-full' : 'space-x-3'
                ]">
                  <div class="flex items-center space-x-3">
                    <div class="handle cursor-move text-gray-400 hover:text-gray-600">
                      <i class="fas fa-grip-vertical"></i>
                    </div>
                    <i :class="['text-xl', menu.icon]"></i>
                    <div>
                      <h3 class="font-medium text-gray-900">{{ menu.name }}</h3>
                      <p class="text-sm text-gray-500">{{ menu.path }}</p>
                    </div>
                  </div>
                  <div class="flex items-center space-x-2">
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
                
                <!-- 卡片視圖額外顯示描述 -->
                <div v-if="viewMode === 'card'" class="text-gray-600 text-sm">
                  {{ menu.description }}
                </div>
              </div>
              
              <!-- 子選單列表 -->
              <div v-if="menu.children && menu.children.length" 
                   :class="[
                     'mt-4',
                     viewMode === 'card' ? 'border-t pt-4' : 'pl-8'
                   ]">
                <draggable 
                  v-model="menu.children"
                  :component-data="{
                    tag: 'div',
                    type: 'transition-group',
                    name: !drag ? 'flip-list' : null
                  }"
                  item-key="id"
                  :group="{ name: 'submenus' }"
                  @start="drag=true" 
                  @end="drag=false"
                  handle=".handle"
                >
                  <template #item="{element: submenu}">
                    <div class="bg-gray-50 rounded-lg p-3 flex justify-between items-center">
                      <div class="flex items-center space-x-3">
                        <div class="handle cursor-move text-gray-400 hover:text-gray-600">
                          <i class="fas fa-grip-vertical"></i>
                        </div>
                        <i :class="['text-lg', submenu.icon]"></i>
                        <div>
                          <h4 class="font-medium text-gray-800">{{ submenu.name }}</h4>
                          <p class="text-xs text-gray-500">{{ submenu.path }}</p>
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
                  </template>
                </draggable>
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
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">狀態</label>
            <select v-model="menuForm.status" 
                    class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
              <option :value="true">啟用</option>
              <option :value="false">停用</option>
            </select>
          </div>
        </div>
        <div class="mt-8 flex justify-end space-x-4">
          <button @click="showAddModal = false" 
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

export default defineComponent({
  name: 'MenuManagement',
  components: {
    draggable,
    BackToHome
  },
  data() {
    return {
      showAddModal: false,
      showIconPicker: false,
      editingMenu: null,
      isSubmenu: false,
      parentMenu: null,
      drag: false,
      menuForm: {
        name: '',
        path: '',
        icon: '',
        description: '',
        status: true
      },
      systemMenus: [
        {
          id: 1,
          name: '系統管理',
          path: '/admin/system',
          icon: 'fas fa-cog',
          description: '系統相關設定與管理功能',
          status: true,
          children: [
            {
              id: 11,
              name: '帳號管理',
              path: '/admin/accounts',
              icon: 'fas fa-users',
              description: '管理系統用戶帳號',
              status: true
            },
            {
              id: 12,
              name: '日誌管理',
              path: '/admin/logs',
              icon: 'fas fa-history',
              description: '查看系統操作日誌',
              status: true
            }
          ]
        }
      ],
      orderMenus: [
        {
          id: 2,
          name: '點餐管理',
          path: '/admin/order',
          icon: 'fas fa-coffee',
          description: '飲料店與點餐相關管理',
          status: true,
          children: [
            {
              id: 21,
              name: '飲料店管理',
              path: '/admin/shops',
              icon: 'fas fa-store',
              description: '管理合作飲料店',
              status: true
            },
            {
              id: 22,
              name: '評分管理',
              path: '/admin/ratings',
              icon: 'fas fa-star',
              description: '管理用戶評分',
              status: true
            }
          ]
        }
      ],
      commonIcons: [
        'fas fa-home', 'fas fa-cog', 'fas fa-users', 'fas fa-coffee',
        'fas fa-store', 'fas fa-star', 'fas fa-history', 'fas fa-chart-bar',
        'fas fa-book', 'fas fa-calendar', 'fas fa-envelope', 'fas fa-bell',
        'fas fa-file', 'fas fa-folder', 'fas fa-image', 'fas fa-video',
        'fas fa-link', 'fas fa-map', 'fas fa-comment', 'fas fa-heart',
        'fas fa-shopping-cart', 'fas fa-tag', 'fas fa-gift', 'fas fa-trophy'
      ]
    }
  },
  computed: {
    menus: {
      get() {
        return [...this.systemMenus, ...this.orderMenus]
      },
      set(value) {
        // 根據某些條件將菜單分配到對應的數組中
        this.systemMenus = value.filter(menu => menu.path.includes('/system'))
        this.orderMenus = value.filter(menu => menu.path.includes('/order'))
      }
    }
  },
  methods: {
    editMenu(menu) {
      this.editingMenu = menu
      this.menuForm = { ...menu }
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
        status: true
      }
      this.showAddModal = true
    },
    deleteMenu(menu) {
      if(confirm('確定要刪除此選單嗎？')) {
        this.menus = this.menus.filter(m => m.id !== menu.id)
      }
    },
    deleteSubmenu(parentMenu, submenu) {
      if(confirm('確定要刪除此子選單嗎？')) {
        parentMenu.children = parentMenu.children.filter(s => s.id !== submenu.id)
      }
    },
    selectIcon(icon) {
      this.menuForm.icon = icon
      this.showIconPicker = false
    },
    saveMenu() {
      if(!this.menuForm.name || !this.menuForm.path) {
        alert('請填寫必要欄位')
        return
      }

      if(this.editingMenu) {
        // 編輯現有選單
        const updateMenu = (menus, targetId) => {
          for(let i = 0; i < menus.length; i++) {
            if(menus[i].id === targetId) {
              menus[i] = { ...menus[i], ...this.menuForm }
              return true
            }
            if(menus[i].children) {
              if(updateMenu(menus[i].children, targetId)) return true
            }
          }
          return false
        }
        updateMenu(this.menus, this.editingMenu.id)
      } else if(this.isSubmenu) {
        // 新增子選單
        if(!this.parentMenu.children) {
          this.parentMenu.children = []
        }
        this.parentMenu.children.push({
          id: Date.now(),
          ...this.menuForm
        })
      } else {
        // 新增主選單
        this.menus.push({
          id: Date.now(),
          ...this.menuForm,
          children: []
        })
      }

      this.showAddModal = false
      this.editingMenu = null
      this.isSubmenu = false
      this.parentMenu = null
      this.menuForm = {
        name: '',
        path: '',
        icon: '',
        description: '',
        status: true
      }
    }
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
</style> 