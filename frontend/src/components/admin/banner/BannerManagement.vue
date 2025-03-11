<template>
  <div class="space-y-6">
    <!-- 頂部工具列 -->
    <div class="bg-white rounded-lg shadow-sm p-4">
      <div class="flex flex-col space-y-4">
        <!-- 標題和新增按鈕 -->
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-bold text-gray-800">輪播圖管理</h2>
          <button @click="openCreateModal"
                  class="banner-create-btn px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 
                         transition-colors duration-200 flex items-center">
            <i class="fas fa-plus mr-2 text-white"></i>新增輪播圖
          </button>
        </div>

        <!-- 分隔線 -->
        <div class="border-b border-gray-200"></div>

        <!-- 功能區 -->
        <div class="flex justify-between items-center">
          <!-- 左側：頁籤 -->
          <div class="flex space-x-4">
            <!-- 主要頁籤 -->
            <div class="flex space-x-1">
              <button v-for="tab in mainTabs" 
                      :key="tab.value"
                      @click="handleTabChange(tab.value)"
                      :class="[
                        'px-4 py-2 rounded-md text-sm font-medium transition-colors flex items-center space-x-2',
                        currentTab === tab.value 
                          ? 'bg-blue-50 text-blue-600 shadow-sm border border-blue-200' 
                          : 'text-gray-600 hover:bg-gray-50 hover:text-gray-800'
                      ]">
                <i :class="getTabIcon(tab.value)" class="w-4"></i>
                <span>{{ tab.label }}</span>
              </button>
            </div>
            
            <!-- 更多頁籤下拉選單 -->
            <div class="relative">
              <button @click="showMoreTabs = !showMoreTabs"
                      class="px-4 py-2 rounded-md text-sm font-medium transition-colors flex items-center space-x-1
                             text-gray-600 hover:bg-gray-50 hover:text-gray-800">
                <span>更多</span>
                <i class="fas fa-chevron-down text-xs"></i>
              </button>
              
              <!-- 下拉選單內容 -->
              <div v-if="showMoreTabs" 
                   class="absolute top-full left-0 mt-1 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-10
                          min-w-[160px]">
                <button v-for="tab in moreTabs" 
                        :key="tab.value"
                        @click="handleMoreTabSelect(tab.value)"
                        class="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 transition-colors
                               flex items-center space-x-2"
                        :class="{'text-blue-600 bg-blue-50': currentTab === tab.value}">
                  <i :class="getTabIcon(tab.value)" class="w-4"></i>
                  <span>{{ tab.label }}</span>
                </button>
              </div>
            </div>
          </div>

          <!-- 右側：搜尋和視圖切換 -->
          <div class="flex items-center space-x-4">
            <!-- 搜尋框 -->
            <div class="relative">
              <input v-model="searchQuery"
                     type="text"
                     class="w-64 px-4 py-2 pr-10 border rounded-lg focus:ring-2 
                            focus:ring-blue-500 focus:border-transparent"
                     placeholder="搜尋輪播圖...">
              <span class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
                <i class="fas fa-search"></i>
              </span>
            </div>

            <!-- 視圖切換 -->
            <div class="flex border rounded-lg overflow-hidden">
              <button @click="viewMode = 'card'"
                      :class="[
                        'px-4 py-2 flex items-center transition-colors',
                        viewMode === 'card'
                          ? 'bg-gray-100 text-gray-800'
                          : 'bg-white text-gray-600 hover:bg-gray-50'
                      ]">
                <i class="fas fa-th-large mr-2"></i>卡片
              </button>
              <button @click="viewMode = 'list'"
                      :class="[
                        'px-4 py-2 flex items-center transition-colors border-l',
                        viewMode === 'list'
                          ? 'bg-gray-100 text-gray-800'
                          : 'bg-white text-gray-600 hover:bg-gray-50'
                      ]">
                <i class="fas fa-list mr-2"></i>列表
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 內容區域 -->
    <div class="relative bg-white rounded-lg shadow-sm p-4 min-h-[300px]">
      <!-- 當前位置提示 -->
      <div class="mb-4 text-sm text-gray-500" :class="{ 'opacity-50': isLoading }">
        <span class="font-medium text-gray-700">當前位置：</span>
        {{ getBannerTypeLabel(currentTab) }}
      </div>

      <!-- 卡片視圖 -->
      <div class="relative">
        <!-- 載入動畫覆蓋層 -->
        <div v-if="isLoading" 
             class="absolute inset-0 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm z-10 rounded-lg">
          <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
            <div class="flex flex-col items-center space-y-4">
              <div class="relative">
                <div class="absolute inset-0 rounded-full border-4 border-indigo-100 dark:border-indigo-900"></div>
                <div class="w-16 h-16 rounded-full border-4 border-indigo-600 dark:border-indigo-400 border-t-transparent animate-spin"></div>
                <div class="absolute inset-3 rounded-full bg-indigo-500/20 dark:bg-indigo-400/20 animate-pulse"></div>
              </div>
              <div class="text-gray-600 dark:text-gray-300 text-lg font-medium tracking-wider animate-pulse whitespace-nowrap">
                載入中...
              </div>
            </div>
          </div>
        </div>

        <TransitionGroup 
          v-if="viewMode === 'card'"
          name="layout-card" 
          tag="div" 
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          :class="{ 'opacity-50': isLoading }">
          <!-- 無資料提示 -->
          <div v-if="filteredBanners.length === 0"
               class="col-span-full">
            <div class="bg-white rounded-xl shadow-sm p-8 text-center">
              <div class="text-gray-400 mb-4">
                <i class="fas fa-image text-4xl"></i>
              </div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">
                {{ searchQuery ? '找不到相關內容' : '尚無輪播圖' }}
              </h3>
              <p class="text-gray-500 mb-4">
                {{ searchQuery ? '請嘗試其他關鍵字' : '點擊上方按鈕開始新增輪播圖' }}
              </p>
            </div>
          </div>

          <div v-else
               v-for="banner in filteredBanners" 
               :key="banner.id"
               class="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-lg transition-shadow duration-300">
            <!-- 圖片預覽 -->
            <div class="relative aspect-video group">
              <!-- 懶加載容器 -->
              <div class="w-full h-full bg-gray-100 dark:bg-gray-800 animate-pulse" 
                   v-if="!imageLoadedMap[banner.id]">
                <div class="absolute inset-0 flex items-center justify-center">
                  <i class="fas fa-image text-gray-400 text-3xl"></i>
                </div>
              </div>
              <img :src="getBannerImage(banner)"
                   :alt="banner.alt || banner.title"
                   loading="lazy"
                   :key="banner.id + '_' + currentTab"
                   class="w-full h-full object-cover transition-all duration-300"
                   :class="{ 
                     'opacity-0': !imageLoadedMap[banner.id], 
                     'opacity-100 scale-100': imageLoadedMap[banner.id],
                     'filter blur-sm': !imageLoadedMap[banner.id]
                   }"
                   @load="handleImageLoad(banner.id)"
                   @error="(e) => handleImageError(e, banner.id)"
                   @click="previewImage(banner.image_url)">
              <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 
                          transition-opacity duration-300 flex items-center justify-center space-x-4">
                <button @click.stop="openEditModal(banner)"
                        class="p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors transform hover:scale-110">
                  <i class="fas fa-edit"></i>
                </button>
                <button @click.stop="confirmDelete(banner)"
                        class="p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors transform hover:scale-110">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>

            <!-- 內容資訊 -->
            <div class="p-4">
              <div class="flex justify-between items-center mb-2">
                <h3 class="font-medium text-gray-800">{{ banner.title }}</h3>
                <span class="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">
                  {{ getBannerTypeLabel(banner.banner_type) }}
                </span>
              </div>
              <p class="text-sm text-gray-600 line-clamp-2 mb-4">{{ banner.subtitle }}</p>
              <div class="flex justify-between items-center">
                <span :class="[
                  'px-2 py-1 rounded-full text-xs',
                  banner.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                ]">
                  {{ banner.is_active ? '啟用中' : '已停用' }}
                </span>
                <span class="text-sm text-gray-500">
                  排序: {{ banner.sort_order }}
                </span>
              </div>
            </div>
          </div>
        </TransitionGroup>

        <!-- 列表視圖 -->
        <div v-else class="bg-white rounded-lg shadow-sm overflow-hidden" :class="{ 'opacity-50': isLoading }">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">圖片</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">標題</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">類型</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">排序</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">狀態</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">更新時間</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <!-- 無資料提示 -->
              <tr v-if="filteredBanners.length === 0">
                <td colspan="6" class="px-6 py-12 text-center">
                  <i class="fas fa-image text-4xl text-gray-300 mb-2 block"></i>
                  <p class="text-gray-500">暫無輪播圖資料</p>
                </td>
              </tr>

              <tr v-else
                  v-for="banner in filteredBanners" 
                  :key="banner.id">
                <td class="px-6 py-4 whitespace-nowrap">
                  <img :src="getBannerImage(banner)"
                       :alt="banner.alt"
                       class="h-16 w-24 object-cover rounded cursor-pointer"
                       @click="previewImage(banner.image_url)"
                       @error="(e) => handleImageError(e, banner.id)">
                </td>
                <td class="px-6 py-4">
                  <div class="text-sm font-medium text-gray-900">{{ banner.title }}</div>
                  <div class="text-sm text-gray-500">{{ banner.subtitle }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">
                    {{ getBannerTypeLabel(banner.banner_type) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ banner.sort_order }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="[
                    'px-2 py-1 rounded-full text-xs',
                    banner.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                  ]">
                    {{ banner.is_active ? '啟用中' : '已停用' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ new Date(banner.updated_at).toLocaleDateString() }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div class="flex justify-end space-x-2">
                    <button @click="openEditModal(banner)"
                            class="inline-flex items-center px-3 py-1.5 bg-blue-50 text-blue-600 rounded-md hover:bg-blue-100 transition-colors">
                      <i class="fas fa-edit text-sm mr-1.5"></i>
                      編輯
                    </button>
                    <button @click="confirmDelete(banner)"
                            class="inline-flex items-center px-3 py-1.5 bg-red-50 text-red-600 rounded-md hover:bg-red-100 transition-colors">
                      <i class="fas fa-trash text-sm mr-1.5"></i>
                      刪除
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- 新增/編輯 Modal -->
    <div v-if="showModal" 
         class="fixed inset-0 z-[9999]">
       <!-- 背景遮罩 -->
       <div class="fixed inset-0 bg-black bg-opacity-50"></div>
       
       <!-- Modal 內容 -->
       <div class="absolute inset-0 overflow-y-auto">
         <div class="flex min-h-full items-center justify-center p-4">
           <div class="relative bg-white rounded-lg shadow-lg w-full max-w-xl">
              <!-- Modal 標題 -->
              <div class="flex justify-between items-center px-6 py-4 border-b">
                <h3 class="text-lg font-semibold">{{ modalTitle }}</h3>
                <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
                  <i class="fas fa-times"></i>
                </button>
              </div>
  
              <!-- Modal 內容 -->
              <div class="px-6 py-4 space-y-4 max-h-[calc(85vh-8rem)] overflow-y-auto">
                <!-- 輪播圖類型 -->
                <div class="mb-4">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Banner 類型
                    <span class="text-red-500">*</span>
                  </label>
                  <select v-model="form.banner_type"
                          class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500
                                 dark:bg-gray-700 dark:border-gray-600 dark:text-white">
                    <option value="">請選擇類型</option>
                    <option v-for="option in bannerTypeOptions" 
                            :key="option.value" 
                            :value="option.value">
                      {{ option.label }}
                    </option>
                  </select>
                </div>

                <!-- 後台路由選擇 -->
                <div v-if="form.banner_type === 'admin'" class="mb-4">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    後台頁面
                    <span class="text-red-500">*</span>
                  </label>
                  <select v-model="form.menu_route"
                          class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500
                                 dark:bg-gray-700 dark:border-gray-600 dark:text-white
                                 [&>optgroup]:font-bold [&>optgroup]:bg-gray-50 dark:[&>optgroup]:bg-gray-800
                                 [&>optgroup]:px-2 [&>optgroup]:py-2
                                 [&>optgroup>option]:font-normal [&>optgroup>option]:bg-white dark:[&>optgroup>option]:bg-gray-700
                                 [&>optgroup>option]:pl-3 [&>optgroup>option]:py-1
                                 [&>optgroup]:border-b [&>optgroup]:border-gray-200 dark:[&>optgroup]:border-gray-600">
                    <option value="">請選擇頁面</option>
                    <optgroup v-for="[category, menus] in groupedMenus"
                              :key="category"
                              :class="'!text-gray-700 dark:!text-gray-200'"
                              :label="category">
                      <option class="border-t border-gray-100 dark:border-gray-600 first:border-t-0"
                              v-for="menu in menus"
                              :key="menu.path"
                              :value="menu.path">
                        {{ menu.name || '未命名頁面' }}
                      </option>
                    </optgroup>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    標題
                    <span class="text-red-500">*</span>
                  </label>
                  <input v-model="form.title"
                         type="text"
                         class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                         :class="{'border-red-500': errors.title}"
                         placeholder="請輸入標題">
                  <p v-if="errors.title" class="mt-1 text-sm text-red-500">
                    {{ errors.title }}
                  </p>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    副標題
                    <span class="text-red-500">*</span>
                  </label>
                  <input v-model="form.subtitle"
                         type="text"
                         class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                         :class="{'border-red-500': errors.subtitle}"
                         placeholder="請輸入副標題">
                  <p v-if="errors.subtitle" class="mt-1 text-sm text-red-500">
                    {{ errors.subtitle }}
                  </p>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    描述
                    <span class="text-red-500">*</span>
                  </label>
                  <textarea v-model="form.description"
                           rows="3"
                           class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                           :class="{'border-red-500': errors.description}"
                           placeholder="請輸入描述"></textarea>
                  <p v-if="errors.description" class="mt-1 text-sm text-red-500">
                    {{ errors.description }}
                  </p>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    圖片網址
                    <span class="text-red-500">*</span>
                  </label>
                  <div class="flex space-x-2">
                    <input v-model="form.image_url"
                           type="text"
                           class="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                           :class="{'border-red-500': errors.image_url}"
                           placeholder="請輸入圖片網址">
                    <button type="button"
                            @click="previewImage(form.image_url)"
                            :disabled="!form.image_url || !isValidUrl(form.image_url)"
                            class="px-3 py-2 rounded-lg transition-colors"
                            :class="[
                              form.image_url && isValidUrl(form.image_url)
                                ? 'bg-gray-100 text-gray-600 hover:bg-gray-200 cursor-pointer' 
                                : 'bg-gray-50 text-gray-400 cursor-not-allowed'
                            ]">
                      <i class="fas fa-eye"></i>
                    </button>
                  </div>
                  <p v-if="errors.image_url" class="mt-1 text-sm text-red-500">
                    {{ errors.image_url }}
                  </p>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    替代文字
                  </label>
                  <input v-model="form.alt"
                         type="text"
                         class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                         placeholder="請輸入替代文字">
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    排序
                    <span class="text-red-500">*</span>
                  </label>
                  <input v-model.number="form.sort_order"
                         type="number"
                         min="1"
                         class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                         :class="{'border-red-500': errors.sort_order}"
                         placeholder="請輸入排序">
                  <p v-if="errors.sort_order" class="mt-1 text-sm text-red-500">
                    {{ errors.sort_order }}
                  </p>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    狀態
                  </label>
                  <div class="flex items-center space-x-2 h-[42px]">
                    <button type="button"
                            @click="form.is_active = !form.is_active"
                            :class="[
                              'px-4 py-2 rounded-lg transition-colors w-full',
                              form.is_active 
                                ? 'bg-green-500 text-white hover:bg-green-600'
                                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                            ]">
                      {{ form.is_active ? '啟用' : '停用' }}
                    </button>
                  </div>
                </div>
              </div>
  
              <!-- Modal 底部按鈕 -->
              <div class="px-6 py-4 bg-gray-50 border-t rounded-b-lg flex justify-end space-x-3">
                <button @click="closeModal" 
                        class="px-4 py-2 text-gray-600 hover:text-gray-800 rounded-lg hover:bg-gray-100 transition-colors">
                  取消
                </button>
                <button @click="handleSubmit"
                        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-sm">
                  確定
                </button>
              </div>
            </div>
         </div>
       </div>
    </div>

    <!-- 圖片預覽 Modal -->
    <Transition name="modal">
      <div v-if="previewImageUrl" 
           class="fixed top-[-25px] left-0 right-0 bottom-0 z-[9999] bg-gray-900/75 backdrop-blur-sm"
           @click="closePreview">
        <div class="fixed top-[-25px] left-0 right-0 bottom-0 overflow-y-auto">
          <div class="flex items-center justify-center min-h-full p-4">
            <div class="relative max-w-4xl w-full my-8">
              <!-- 關閉按鈕 -->
              <button class="absolute -top-2 -right-2 w-8 h-8 bg-white/10 hover:bg-white/20 rounded-full flex items-center justify-center text-white/80 hover:text-white transition-colors"
                      @click="closePreview">
                <i class="fas fa-times"></i>
              </button>
              <!-- 圖片容器 -->
              <img :src="previewImageUrl"
                   class="w-full max-h-[80vh] object-contain select-none rounded-lg shadow-2xl"
                   @click.stop
                   @error="handleImageError"
                   alt="圖片預覽">
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { bannerAPI, menuAPI } from '@/api'
import Swal from 'sweetalert2'
import { useLogger } from '@/composables/useLogger'

// 視圖模式
const viewMode = ref('card')
// 搜尋關鍵字
const searchQuery = ref('')
// 表單參考
// const formRef = ref(null)
// 數據
const banners = ref([])
const showModal = ref(false)
const showPreview = ref(false)
const isEditing = ref(false)
const currentBannerId = ref(null)

// 輪播圖類型選項
const bannerTypeOptions = [
  { label: '全部', value: 'all' },
  { label: '首頁', value: 'home' },
  { label: '特色功能', value: 'feature' },
  { label: '學習中心', value: 'learning' },
  { label: '定價方案', value: 'pricing' },
  { label: '尋找美食', value: 'food' },
  { label: '頁腳', value: 'footer' },
  { label: '登入', value: 'login' },
  { label: '忘記密碼', value: 'forgot-password' },
  { label: '後台', value: 'admin' }
]

// 表單數據
const form = ref({
  title: '',
  subtitle: '',
  description: '',
  image_url: '',
  alt: '',
  banner_type: '',
  sort_order: 1,
  is_active: true,
  menu_route: ''
})

// 添加 errors ref
const errors = ref({})

// 記錄已經處理過錯誤的圖片
const handledErrors = ref(new Set())

// 當前選中的頁籤
const currentTab = ref('all')

// 後台選單列表
const menuList = ref([])

// 獲取後台選單
const fetchMenus = async () => {
  try {
    const response = await menuAPI.getMenus()
    if (response.data?.menus?.length > 0) {
      // 添加儀表板選項
      const dashboardMenu = {
        name: '儀表板管理',
        path: 'dashboard',
        category: '', // 空類別
        status: 'active',
        sort_order: -1  // 確保排在最前面
      }
      
      menuList.value = response.data.menus
        .filter(menu => menu.status === 'active') // 只顯示啟用的選單
        .concat([dashboardMenu])  // 加入儀表板選項
        .sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0)) // 依照排序順序
      
      console.log('處理後的選單列表:', menuList.value)
    }
  } catch (error) {
    console.error('獲取選單失敗:', error)
  }
}

// 將選單依類別分組
const groupedMenus = computed(() => {
  const groups = {}
  // 先處理沒有類別的選項（儀表板）
  const uncategorized = menuList.value.filter(menu => !menu.category)
  if (uncategorized.length > 0) {
    groups[''] = uncategorized
  }
  
  // 再處理其他有類別的選項
  menuList.value
    .filter(menu => menu.category)
    .forEach(menu => {
      if (!groups[menu.category]) {
        groups[menu.category] = []
      }
      groups[menu.category].push(menu)
    })

  // 依照 section_order 排序類別
  return Object.entries(groups)
    .sort(([categoryA, menuA], [categoryB, menuB]) => {
      // 確保空類別（儀表板）永遠在最前面
      if (categoryA === '') return -1
      if (categoryB === '') return 1
      return (menuA[0]?.section_order || 0) - (menuB[0]?.section_order || 0)
    })
})

// 獲取類型標籤
const getBannerTypeLabel = (type) => {
  // 如果包含 admin，一律顯示後台
  if (type?.includes('admin')) {
    return '後台'
  }
  
  switch (type) {
    case 'home':
      return '首頁'
    case 'feature':
      return '特色功能'
    case 'learning':
      return '學習中心'
    case 'pricing':
      return '定價方案'
    case 'food':
      return '尋找美食'
    case 'footer':
      return '頁腳'
    case 'login':
      return '登入'
    case 'forgot-password':
      return '忘記密碼'
    case 'all':
      return '全部'
    default:
      return '未知類型'
  }
}

// 添加圖片載入狀態管理
const imageLoadedMap = ref({})

// 添加載入狀態
const isLoading = ref(false)

// 修改頁籤切換函數
const handleTabChange = async (tab) => {
  try {
    if (isLoading.value) return
    isLoading.value = true
    
    // 先重置圖片載入狀態
    imageLoadedMap.value = {}
    
    // 延遲更新 currentTab，讓動畫有時間顯示
    await new Promise(resolve => setTimeout(resolve, 100))
    currentTab.value = tab
    
    await logOperation(`【Banner管理】切換到${getBannerTypeLabel(tab)}頁籤`, '查看')
    
    if (tab === 'all') {
      await fetchAllActiveBanners()
    } else {
      await fetchBannersByType(tab)
    }
    
    // 預加載圖片
    if (banners.value.length > 0) {
      const loadPromises = banners.value.map(banner => {
        return new Promise((resolve) => {
          const img = new Image()
          img.onload = () => {
            imageLoadedMap.value[banner.id] = true
            resolve()
          }
          img.onerror = () => {
            handleImageError({ target: img }, banner.id)
            resolve()
          }
          img.src = getBannerImage(banner)
        })
      })
      
      // 等待所有圖片預加載完成或超時
      await Promise.race([
        Promise.all(loadPromises),
        new Promise(resolve => setTimeout(resolve, 2000)) // 2秒超時
      ])
    }
    
  } catch (error) {
    console.error('切換頁籤失敗:', error)
  } finally {
    // 添加小延遲確保動畫流暢
    setTimeout(() => {
      isLoading.value = false
    }, 300)
  }
}

// 修改圖片載入處理函數
const handleImageLoad = (bannerId) => {
  if (bannerId) {
    imageLoadedMap.value[bannerId] = true
  }
}

// 獲取所有啟用的輪播圖
const fetchAllActiveBanners = async () => {
  try {
    const response = await bannerAPI.getActiveBanners()
    if (response.data?.data) {
      banners.value = response.data.data
    }
  } catch (error) {
    console.error('獲取所有輪播圖失敗:', error)
    Swal.fire({
      icon: 'error',
      title: '獲取數據失敗',
      text: '請稍後再試',
      confirmButtonText: '確定'
    })
  }
}

// 獲取指定類型的輪播圖
const fetchBannersByType = async (type) => {
  try {
    const response = await bannerAPI.getBannersByType(type)
    if (response.data?.data) {
      banners.value = response.data.data
      console.log('獲取輪播圖:', banners.value)
    }
  } catch (error) {
    console.error('獲取輪播圖失敗:', error)
    Swal.fire({
      icon: 'error',
      title: '獲取數據失敗',
      text: '請稍後再試',
      confirmButtonText: '確定'
    })
  }
}

const { logOperation } = useLogger()

// 打開新增 Modal
const openCreateModal = () => {
  isEditing.value = false
  resetForm()
  showModal.value = true
  if (!menuList.value.length) {
    fetchMenus()
  }
}

// 重置表單
const resetForm = () => {
  form.value = {
    title: '',
    subtitle: '',
    description: '',
    image_url: '',
    alt: '',
    banner_type: '',
    sort_order: 1,
    is_active: true,
    menu_route: ''
  }
  errors.value = {}
}

// 打開編輯 Modal
const openEditModal = async (banner) => {
  isEditing.value = true
  currentBannerId.value = banner.id
  
  // 確保有選單數據
  if (!menuList.value.length) {
    await fetchMenus()
  }
  
  // 處理後台類型的 banner
  if (banner.banner_type?.startsWith('admin_')) {
    const routePath = banner.banner_type.replace('admin_', '')
    
    // 在設置表單值之前，先找到對應的選單項
    const menuItem = menuList.value.find(menu => 
      menu.path === routePath || 
      menu.path === `admin/${routePath}` || 
      menu.path.endsWith(`/${routePath}`)
    )
    
    console.log('找到的選單項:', menuItem)
    
    form.value = {
      ...banner,
      banner_type: 'admin',
      menu_route: menuItem ? menuItem.path : (
        routePath === 'dashboard' ? 'dashboard' : routePath
      )
    }
    
    console.log('後台類型 banner:', {
      原始類型: banner.banner_type,
      處理後類型: form.value.banner_type,
      路由: form.value.menu_route,
      選單列表: menuList.value
    })
  } else {
    form.value = { ...banner }
  }
  
  showModal.value = true
  logOperation(`【Banner管理】開始編輯輪播圖: ${banner.title}`, '編輯')
}

// 添加 URL 驗證函數
const isValidUrl = (url) => {
  return /^https?:\/\/.+/.test(url)
}

// 添加預設圖片常量
const defaultImage = 'https://placehold.co/600x400/e2e8f0/475569?text=無法載入圖片'

// 修改圖片錯誤處理函數
const handleImageError = (event, bannerId) => {
  console.error('圖片載入失敗:', event.target.src)
  event.target.src = defaultImage
  if (bannerId) {
    imageLoadedMap.value[bannerId] = true
  }
}

// 修改獲取圖片 URL 的函數
const getBannerImage = (banner) => {
  if (!banner.image_url) return defaultImage
  
  // 檢查是否為完整的 URL
  if (banner.image_url.startsWith('http')) {
    return banner.image_url
  }
  
  // 如果是相對路徑，添加基礎 URL
  return `${import.meta.env.VITE_BACKEND_URL}${banner.image_url}`
}

// 修改圖片預覽函數
const previewImage = (url) => {
  if (!url) return
  
  const img = new Image()
  img.onload = () => {
    previewImageUrl.value = url
    document.body.style.overflow = 'hidden'
  }
  
  img.onerror = () => {
    previewImageUrl.value = defaultImage
    document.body.style.overflow = 'hidden'
  }
  
  img.src = url.startsWith('http') ? url : `${import.meta.env.VITE_BACKEND_URL}${url}`
}

// 修改圖片預覽相關功能
const previewImageUrl = ref(null)

const closePreview = () => {
  previewImageUrl.value = null
  document.body.style.overflow = ''
}

// 監聽 ESC 鍵關閉預覽
const handleKeyDown = (e) => {
  if (e.key === 'Escape' && previewImageUrl.value) {
    closePreview()
  }
}

onMounted(() => {
  const init = async () => {
    if (currentTab.value === 'all') {
      await fetchAllActiveBanners()
    } else {
      await fetchBannersByType(currentTab.value)
    }
    await logOperation('【Banner管理】訪問Banner管理頁面', '查看')
  }
  init()
  window.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
  document.body.style.overflow = ''
})

// 修改提交表單函數
const handleSubmit = async () => {
  if (!validateForm()) return
  
  try {
    const formData = { ...form.value }
    // 如果是後台類型，將路由加入 banner_type
    if (formData.banner_type === 'admin' && formData.menu_route) {
      // 如果選擇的是儀表板，固定使用 admin_dashboard
      if (formData.menu_route === 'dashboard') {
        formData.banner_type = 'admin_dashboard'
      } else {
        // 確保路徑格式正確
        const routePath = formData.menu_route.startsWith('/') ? formData.menu_route.slice(1) : formData.menu_route
        formData.banner_type = `admin_${routePath.replace('admin/', '')}`
      }
    }
    delete formData.menu_route // 刪除額外的欄位
    
    if (isEditing.value) {
      await bannerAPI.updateBanner(currentBannerId.value, formData)
      await logOperation(`【Banner管理】更新輪播圖: ${formData.title}`, '更新')
    } else {
      await bannerAPI.createBanner(formData)
      await logOperation(`【Banner管理】新增輪播圖: ${formData.title}`, '新增')
    }
    
    closeModal()
    await fetchBannersByType(currentTab.value)
    
    Swal.fire({
      icon: 'success',
      title: `${isEditing.value ? '更新' : '新增'}成功`,
      showConfirmButton: false,
      timer: 1500
    })
  } catch (error) {
    console.error('表單提交失敗:', error)
    Swal.fire({
      icon: 'error',
      title: '操作失敗',
      text: error.response?.data?.message || '請稍後再試',
      confirmButtonText: '確定'
    })
  }
}

// 確認刪除
const confirmDelete = async (banner) => {
  const result = await Swal.fire({
    title: '確認刪除',
    text: `確定要刪除 "${banner.title}" 嗎？`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: '確定刪除',
    cancelButtonText: '取消',
    customClass: {
      container: 'swal2-container',
      popup: 'swal2-popup',
      backdrop: 'swal2-backdrop-show'
    }
  })
  
  if (result.isConfirmed) {
    try {
      await bannerAPI.deleteBanner(banner.id)
      await logOperation(`【Banner管理】刪除輪播圖: ${banner.title}`, '刪除')
      banners.value = banners.value.filter(b => b.id !== banner.id)
      Swal.fire({
        icon: 'success',
        title: '成功',
        text: '刪除成功',
        timer: 1500,
        showConfirmButton: false,
        customClass: {
          container: 'swal2-container',
          popup: 'swal2-popup',
          backdrop: 'swal2-backdrop-show'
        }
      })
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: '錯誤',
        text: '刪除失敗',
        customClass: {
          container: 'swal2-container',
          popup: 'swal2-popup',
          backdrop: 'swal2-backdrop-show'
        }
      })
    }
  }
}

// 修改關閉 Modal 函數
const closeModal = () => {
  showModal.value = false
  resetForm()
}

// 修改表單驗證邏輯
const validateForm = () => {
  errors.value = {}
  
  if (!form.value.banner_type) {
    errors.value.banner_type = '請選擇輪播圖類型'
  }
  if (!form.value.title) {
    errors.value.title = '請輸入標題'
  } else if (form.value.title.length > 100) {
    errors.value.title = '標題長度不能超過100個字符'
  }
  
  if (!form.value.subtitle) {
    errors.value.subtitle = '請輸入副標題'
  } else if (form.value.subtitle.length > 200) {
    errors.value.subtitle = '副標題長度不能超過200個字符'
  }
  
  if (!form.value.description) {
    errors.value.description = '請輸入描述'
  }
  
  if (!form.value.image_url) {
    errors.value.image_url = '請輸入圖片網址'
  } else if (!/^https?:\/\/.+/.test(form.value.image_url)) {
    errors.value.image_url = '請輸入有效的URL'
  }
  
  // 添加排序驗證
  if (!form.value.sort_order) {
    errors.value.sort_order = '請輸入排序'
    return false
  }
  
  if (form.value.sort_order < 1) {
    errors.value.sort_order = '排序不能小於1'
    return false
  }
  
  // 檢查排序是否重複
  if (checkSortOrderDuplicate(form.value.sort_order, isEditing.value ? currentBannerId.value : null)) {
    errors.value.sort_order = '此排序已被使用'
    return false
  }
  
  return Object.keys(errors.value).length === 0
}

// 檢查排序是否重複
const checkSortOrderDuplicate = (sortOrder, bannerId = null) => {
  return banners.value.some(banner => 
    banner.sort_order === sortOrder && banner.id !== bannerId
  )
}

// 過濾後的輪播圖列表
const filteredBanners = computed(() => {
  if (!searchQuery.value) return banners.value
  const query = searchQuery.value.toLowerCase()
  return banners.value.filter(banner => 
    banner.title.toLowerCase().includes(query) ||
    banner.subtitle.toLowerCase().includes(query) ||
    banner.description.toLowerCase().includes(query)
  )
})

// Modal 標題計算屬性
const modalTitle = computed(() => {
  return isEditing.value ? '編輯輪播圖' : '新增輪播圖'
})

// 新增下拉選單狀態
const showMoreTabs = ref(false)

// 主要頁籤
const mainTabs = [
  { label: '全部', value: 'all', icon: 'ri-apps-line' },
  { label: '首頁', value: 'home', icon: 'ri-home-4-line' },
  { label: '特色功能', value: 'feature', icon: 'ri-star-line' },
  { label: '學習中心', value: 'learning', icon: 'ri-book-open-line' }
]

// 更多頁籤
const moreTabs = [
  { label: '定價方案', value: 'pricing', icon: 'ri-money-dollar-circle-line' },
  { label: '尋找美食', value: 'food', icon: 'ri-restaurant-2-line' },
  { label: '頁腳', value: 'footer', icon: 'ri-layout-bottom-line' },
  { label: '登入', value: 'login', icon: 'ri-login-circle-line' },
  { label: '忘記密碼', value: 'forgot-password', icon: 'ri-key-2-line' },
  { label: '後台', value: 'admin', icon: 'ri-settings-3-line' }
]

// 獲取頁籤圖標
const getTabIcon = (value) => {
  const tab = [...mainTabs, ...moreTabs].find(t => t.value === value)
  return tab?.icon || 'ri-question-line'
}

// 處理更多頁籤選擇
const handleMoreTabSelect = (value) => {
  handleTabChange(value)
  showMoreTabs.value = false
}
</script>

<style scoped>
/* 移除原有的卡片視圖動畫 */
.layout-card-move {
  transition: transform 0.5s ease, opacity 0.5s ease;
}

.layout-card-enter-active {
  transition: transform 0.5s ease, opacity 0.5s ease;
  transform-origin: center;
}

.layout-card-leave-active {
  transition: transform 0.5s ease, opacity 0.5s ease;
  position: absolute;
  transform-origin: center;
}

.layout-card-enter-from {
  opacity: 0;
  transform: scale(0.8) translateY(20px);
}

.layout-card-leave-to {
  opacity: 0;
  transform: scale(0.8) translateY(-20px);
}

/* 列表視圖動畫優化 */
.layout-list-move {
  transition: transform 0.5s ease, opacity 0.5s ease;
}

.layout-list-enter-active {
  transition: transform 0.5s ease, opacity 0.5s ease;
}

.layout-list-leave-active {
  transition: transform 0.5s ease, opacity 0.5s ease;
  position: absolute;
}

.layout-list-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.layout-list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* 圖片載入動畫 */
@keyframes imageFadeIn {
  from {
    opacity: 0;
    transform: scale(1.05);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

img.opacity-100 {
  animation: imageFadeIn 0.3s ease-out forwards;
}

/* 懶加載佔位元素動畫 */
@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.animate-pulse {
  background: linear-gradient(
    90deg,
    rgba(226, 232, 240, 0.4) 0%,
    rgba(226, 232, 240, 0.7) 50%,
    rgba(226, 232, 240, 0.4) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 2s infinite linear;
}

.dark .animate-pulse {
  background: linear-gradient(
    90deg,
    rgba(55, 65, 81, 0.4) 0%,
    rgba(55, 65, 81, 0.7) 50%,
    rgba(55, 65, 81, 0.4) 100%
  );
}

/* 優化圖片載入效果 */
img {
  will-change: transform, opacity;
  backface-visibility: hidden;
}

.opacity-0 {
  opacity: 0;
  transform: scale(1.05);
}

.opacity-100 {
  opacity: 1;
  transform: scale(1);
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* 添加頁面載入動畫相關樣式 */
.fixed {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    backdrop-filter: blur(0);
  }
  to {
    opacity: 1;
    backdrop-filter: blur(8px);
  }
}

/* 內容區域過渡效果 */
.opacity-50 {
  transition: opacity 0.3s ease-in-out;
}

/* 優化載入指示器動畫 */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* 優化旋轉動畫 */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 修改載入動畫相關樣式 */
/* .min-h-[400px] {
  min-height: 400px;
} */

/* 優化載入指示器定位 */
.sticky {
  position: sticky;
}

/* 確保載入文字不會換行 */
.whitespace-nowrap {
  white-space: nowrap;
}
</style> 