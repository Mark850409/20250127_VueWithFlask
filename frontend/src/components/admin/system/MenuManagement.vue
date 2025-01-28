<template>
  <div>
    <!-- 視圖切換按鈕 -->
    <div class="mb-6 flex justify-end">
      <div class="bg-white rounded-lg shadow-sm p-1 inline-flex space-x-1">
        <button @click="viewMode = 'card'" 
                :class="[
                  'px-3 py-1.5 rounded transition-colors duration-200 flex items-center',
                  viewMode === 'card' ? 'bg-blue-500 text-white' : 'text-gray-600 hover:bg-gray-100'
                ]">
          <i class="fas fa-th-large mr-2"></i>卡片
        </button>
        <button @click="viewMode = 'list'" 
                :class="[
                  'px-3 py-1.5 rounded transition-colors duration-200 flex items-center',
                  viewMode === 'list' ? 'bg-blue-500 text-white' : 'text-gray-600 hover:bg-gray-100'
                ]">
          <i class="fas fa-list mr-2"></i>列表
        </button>
      </div>
    </div>

    <!-- 選單內容 -->
    <transition-group 
      name="view-switch"
      tag="div"
      :class="{
        'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6': viewMode === 'card',
        'space-y-4': viewMode === 'list'
      }">
      <!-- 選單項目 -->
      <template v-for="menu in menus" :key="menu.id">
        <!-- 卡片樣式 -->
        <div v-if="viewMode === 'card'"
             class="bg-white rounded-lg shadow-sm p-6 transition-all duration-300">
          <div class="flex justify-between items-start mb-4">
            <div class="flex items-center space-x-3">
              <i :class="['text-xl', menu.icon]"></i>
              <div>
                <h3 class="font-medium text-gray-900">{{ menu.name }}</h3>
                <p class="text-sm text-gray-500">{{ menu.path }}</p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
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
          <p class="text-gray-600 text-sm mb-4">{{ menu.description }}</p>
          <div class="flex justify-between items-center text-sm text-gray-500">
            <span>排序: {{ menu.sort }}</span>
            <span :class="[
              'px-2 py-1 rounded-full text-xs',
              menu.status ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            ]">
              {{ menu.status ? '啟用' : '停用' }}
            </span>
          </div>
        </div>

        <!-- 列表樣式 -->
        <div v-else
             class="bg-white rounded-lg shadow-sm p-4 transition-all duration-300">
          <div class="flex justify-between items-center">
            <div class="flex items-center space-x-4">
              <i :class="['text-xl', menu.icon]"></i>
              <div>
                <div class="flex items-center space-x-2">
                  <h3 class="font-medium text-gray-900">{{ menu.name }}</h3>
                  <span class="text-sm text-gray-500">{{ menu.path }}</span>
                </div>
                <p class="text-sm text-gray-600 mt-1">{{ menu.description }}</p>
              </div>
            </div>
            <div class="flex items-center space-x-4">
              <span class="text-sm text-gray-500">排序: {{ menu.sort }}</span>
              <span :class="[
                'px-2 py-1 rounded-full text-xs',
                menu.status ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              ]">
                {{ menu.status ? '啟用' : '停用' }}
              </span>
              <div class="flex items-center space-x-2">
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
          </div>
        </div>
      </template>

      <!-- 新增選單按鈕 -->
      <div v-if="viewMode === 'card'"
           :key="'add'"
           @click="showAddModal = true"
           class="bg-white rounded-lg shadow-sm p-6 border-2 border-dashed border-gray-300 hover:border-blue-500 cursor-pointer flex flex-col items-center justify-center space-y-2 transition-colors">
        <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center">
          <i class="fas fa-plus text-blue-500"></i>
        </div>
        <span class="text-gray-600">新增選單</span>
      </div>
      <div v-else
           :key="'add-list'"
           @click="showAddModal = true"
           class="bg-white rounded-lg shadow-sm p-4 border-2 border-dashed border-gray-300 hover:border-blue-500 cursor-pointer flex items-center justify-center transition-colors">
        <i class="fas fa-plus text-blue-500 mr-2"></i>
        <span class="text-gray-600">新增選單</span>
      </div>
    </transition-group>

    <!-- 新增/編輯選單彈窗 -->
    <div v-if="showAddModal" 
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white rounded-xl p-8 w-full max-w-md">
        <h2 class="text-xl font-bold mb-6">{{ editingMenu ? '編輯選單' : '新增選單' }}</h2>
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
            <input type="text" v-model="menuForm.icon" 
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">描述</label>
            <textarea v-model="menuForm.description" rows="3"
                      class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">排序</label>
            <input type="number" v-model="menuForm.sort" 
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
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

    <BackToHome />
  </div>
</template>

<script>
import BackToHome from '../common/BackToHome.vue'

export default {
  name: 'MenuManagement',
  components: {
    BackToHome
  },
  data() {
    return {
      viewMode: 'card',
      showAddModal: false,
      editingMenu: null,
      menuForm: {
        name: '',
        path: '',
        icon: '',
        description: '',
        sort: 0,
        status: true
      },
      menus: [
        {
          id: 1,
          name: '系統管理',
          path: '/admin/system',
          icon: 'fas fa-cog',
          description: '系統相關設定與管理功能',
          sort: 1,
          status: true
        },
        {
          id: 2,
          name: '點餐管理',
          path: '/admin/order',
          icon: 'fas fa-coffee',
          description: '飲料店與點餐相關管理',
          sort: 2,
          status: true
        },
        // ... 更多選單數據
      ]
    }
  },
  methods: {
    editMenu(menu) {
      this.editingMenu = menu
      this.menuForm = { ...menu }
      this.showAddModal = true
    },
    deleteMenu(menu) {
      if(confirm('確定要刪除此選單嗎？')) {
        this.menus = this.menus.filter(m => m.id !== menu.id)
      }
    },
    saveMenu() {
      if(!this.menuForm.name || !this.menuForm.path) {
        alert('請填寫必要欄位')
        return
      }

      if(this.editingMenu) {
        const index = this.menus.findIndex(m => m.id === this.editingMenu.id)
        this.menus[index] = { ...this.editingMenu, ...this.menuForm }
      } else {
        this.menus.push({
          id: this.menus.length + 1,
          ...this.menuForm
        })
      }
      this.showAddModal = false
      this.editingMenu = null
      this.menuForm = {
        name: '',
        path: '',
        icon: '',
        description: '',
        sort: 0,
        status: true
      }
    }
  }
}
</script>

<style scoped>
/* 視圖切換動畫 */
.view-switch-enter-active,
.view-switch-leave-active {
  transition: all 0.3s ease;
}

.view-switch-enter-from,
.view-switch-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.view-switch-leave-active {
  position: absolute;
}

.view-switch-move {
  transition: transform 0.3s ease;
}
</style> 