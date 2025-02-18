<template>
  <div class="space-y-6">
    <!-- 頂部工具列 -->
    <div class="bg-white rounded-lg shadow-sm p-4">
      <div class="flex flex-col space-y-4">
        <!-- 標題和新增按鈕 -->
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-bold text-gray-800">輪播圖管理</h2>
          <button @click="openCreateModal"
                  class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 
                         transition-colors duration-200 flex items-center">
            <i class="fas fa-plus mr-2"></i>新增輪播圖
          </button>
        </div>

        <!-- 分隔線 -->
        <div class="border-b border-gray-200"></div>

        <!-- 功能區 -->
        <div class="flex justify-between items-center">
          <!-- 左側：頁籤 -->
          <div class="flex space-x-1">
            <button v-for="tab in bannerTypeOptions" 
                    :key="tab.value"
                    @click="handleTabChange(tab.value)"
                    :class="[
                      'px-4 py-2 rounded-md text-sm font-medium transition-colors',
                      currentTab === tab.value 
                        ? 'bg-blue-50 text-blue-600 shadow-sm border border-blue-200' 
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-800'
                    ]">
              {{ tab.label }}
            </button>
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
    <div class="bg-white rounded-lg shadow-sm p-4">
      <!-- 當前位置提示 -->
      <div class="mb-4 text-sm text-gray-500">
        <span class="font-medium text-gray-700">當前位置：</span>
        {{ getBannerTypeLabel(currentTab) }}
      </div>

      <!-- 卡片視圖 -->
      <TransitionGroup 
        v-if="viewMode === 'card'"
        name="layout-card" 
        tag="div" 
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
      >
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
            <img :src="getBannerImage(banner)"
                 :alt="banner.alt"
                 class="w-full h-full object-cover"
                 @click="previewImage(banner.image_url)"
                 @error="(e) => handleImageError(e, banner.id)">
            <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 
                        transition-opacity duration-300 flex items-center justify-center space-x-4">
              <button @click.stop="openEditModal(banner)"
                      class="p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors">
                <i class="fas fa-edit"></i>
              </button>
              <button @click.stop="confirmDelete(banner)"
                      class="p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors">
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
      <div v-else class="bg-white rounded-lg shadow-sm overflow-hidden">
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
                <h3 class="text-lg font-semibold">{{ editingBanner ? '編輯輪播圖' : '新增輪播圖' }}</h3>
                <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
                  <i class="fas fa-times"></i>
                </button>
              </div>
  
              <!-- Modal 內容 -->
              <div class="px-6 py-4 space-y-4 max-h-[calc(85vh-8rem)] overflow-y-auto">
                <!-- 輪播圖類型 -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1 required-field">
                    輪播圖類型
                  </label>
                  <select v-model="form.banner_type"
                          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="" disabled>請選擇類型</option>
                    <option v-for="option in bannerTypeOptions"
                            :key="option.value"
                            :value="option.value">
                      {{ option.label }}
                    </option>
                  </select>
                  <div v-if="errors.banner_type" class="mt-1 text-sm text-red-500">
                    {{ errors.banner_type }}
                  </div>
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
import { bannerAPI } from '@/api'
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
  { value: 'home', label: '首頁' },
  { value: 'features', label: '特色功能' },
  { value: 'learning', label: '學習中心' },
  { value: 'pricing', label: '定價方案' }
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
  is_active: true
})

// 添加 errors ref
const errors = ref({})

// 記錄已經處理過錯誤的圖片
const handledErrors = ref(new Set())

// 添加預設圖片常量
const DEFAULT_BANNER_IMAGE = 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&q=80&w=1920&h=600'

// 當前選中的頁籤
const currentTab = ref('home')

// 獲取類型標籤
const getBannerTypeLabel = (type) => {
  const option = bannerTypeOptions.find(opt => opt.value === type)
  return option ? option.label : '未知類型'
}

// 處理頁籤切換
const handleTabChange = async (tab) => {
  currentTab.value = tab
  await logOperation(`【Banner管理】切換到${getBannerTypeLabel(tab)}頁籤`, '查看')
  await fetchBannersByType(tab)
}

// 根據類型獲取輪播圖
const fetchBannersByType = async (type) => {
  try {
    const response = await bannerAPI.getBannersByType(type)
    banners.value = response.data.data
    // 清除錯誤記錄
    handledErrors.value.clear()
    await logOperation(`【Banner管理】查看${getBannerTypeLabel(type)}輪播圖列表`, '查看')
  } catch (error) {
    console.error('Failed to fetch banners:', error)
    Swal.fire({
      icon: 'error',
      title: '錯誤',
      text: '獲取輪播圖失敗',
      confirmButtonText: '確定'
    })
  }
}

// 修改原有的 fetchBanners
const fetchBanners = () => fetchBannersByType(currentTab.value)

const { logOperation } = useLogger()

// 打開新增 Modal
const openCreateModal = () => {
  isEditing.value = false
  resetForm()
  showModal.value = true
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
    is_active: true
  }
  errors.value = {}
}

// 打開編輯 Modal
const openEditModal = (banner) => {
  isEditing.value = true
  currentBannerId.value = banner.id
  form.value = {
    ...banner,
    banner_type: banner.banner_type
  }
  showModal.value = true
  logOperation(`【Banner管理】開始編輯輪播圖: ${banner.title}`, '編輯')
}

// 添加 URL 驗證函數
const isValidUrl = (url) => {
  return /^https?:\/\/.+/.test(url)
}

// 修改圖片預覽函數
const previewImage = (url) => {
  if (!url || !isValidUrl(url)) return

  const img = new Image()
  
  img.onload = () => {
    previewImageUrl.value = url
    document.body.style.overflow = 'hidden'
  }
  
  img.onerror = () => {
    // 如果是從新增/編輯 modal 中預覽的，就關閉該 modal
    if (showModal.value) {
      closeModal()
    }
    
    Swal.fire({
      icon: 'error',
      title: '錯誤',
      text: '圖片載入失敗，請確認網址是否正確',
      confirmButtonText: '確定',
      confirmButtonColor: '#3085d6',
      customClass: {
        container: 'swal2-container',
        popup: 'swal2-popup',
        backdrop: 'swal2-backdrop-show'
      }
    })
  }

  img.src = url
}

// 修改圖片錯誤處理函數
const handleImageError = (event, bannerId) => {
  // 不管是否處理過，都設置預設圖片
  event.target.src = DEFAULT_BANNER_IMAGE
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
    await fetchBannersByType(currentTab.value)
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
    if (isEditing.value) {
      const response = await bannerAPI.updateBanner(currentBannerId.value, form.value)
      await logOperation(`【Banner管理】更新輪播圖: ${form.value.title}`, '修改')
      if (response.data.data) {
        const updatedBanner = response.data.data
        const index = banners.value.findIndex(b => b.id === updatedBanner.id)
        if (index !== -1) {
          banners.value[index] = updatedBanner
        }
      }
      Swal.fire({
        icon: 'success',
        title: '成功',
        text: '更新成功',
        timer: 1500,
        showConfirmButton: false,
        customClass: {
          container: 'swal2-container',
          popup: 'swal2-popup',
          backdrop: 'swal2-backdrop-show'
        }
      })
    } else {
      const response = await bannerAPI.createBanner(form.value)
      await logOperation(`【Banner管理】新增輪播圖: ${form.value.title}`, '新增')
      if (response.data.data) {
        banners.value.push(response.data.data)
      }
      Swal.fire({
        icon: 'success',
        title: '成功',
        text: '新增成功',
        timer: 1500,
        showConfirmButton: false,
        customClass: {
          container: 'swal2-container',
          popup: 'swal2-popup',
          backdrop: 'swal2-backdrop-show'
        }
      })
    }
    closeModal()
  } catch (error) {
    // 先關閉 modal
    closeModal()
    
    // 然後顯示錯誤訊息
    Swal.fire({
      icon: 'error',
      title: '錯誤',
      text: error.message || '操作失敗',
      confirmButtonText: '確定',
      confirmButtonColor: '#3085d6',
      customClass: {
        container: 'swal2-container',
        popup: 'swal2-popup',
        backdrop: 'swal2-backdrop-show'
      }
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

// 修改為使用 computed 來處理圖片 URL
const getBannerImage = (banner) => {
  return banner.image_url || DEFAULT_BANNER_IMAGE
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
</script>

<style scoped>
/* 移除原有的卡片視圖動畫 */
.layout-card-move {
  transition: all 0.3s ease;
}

.layout-card-enter-active,
.layout-card-leave-active {
  transition: all 0.3s ease;
}

.layout-card-enter-from,
.layout-card-leave-to {
  opacity: 0;
  transform: translateY(10px);  /* 改用輕微的上下位移 */
}

/* 列表視圖動畫 */
.layout-list-move {
  transition: all 0.3s ease;
}

.layout-list-enter-active,
.layout-list-leave-active {
  transition: all 0.3s ease;
}

.layout-list-enter-from,
.layout-list-leave-to {
  opacity: 0;
  transform: translateY(10px);  /* 統一使用相同的動畫效果 */
}

/* 淡入淡出動畫 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 圖片預覽時禁用選取 */
.select-none {
  user-select: none;
  -webkit-user-select: none;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Dialog 樣式 */
:deep(.custom-dialog .el-dialog) {
  @apply rounded-lg shadow-xl;
}

:deep(.custom-dialog .el-dialog__header) {
  @apply px-6 py-4 border-b border-gray-200;
}

:deep(.custom-dialog .el-dialog__body) {
  @apply p-6;
}

:deep(.custom-dialog .el-dialog__footer) {
  @apply px-6 py-4 border-t border-gray-200;
}

/* 表單元素樣式 */
:deep(.custom-input .el-input__wrapper) {
  @apply shadow-none border border-gray-300 rounded-md transition-colors;
}

:deep(.custom-input .el-input__wrapper:hover) {
  @apply border-gray-400;
}

:deep(.custom-input-number) {
  @apply w-full;
}

:deep(.custom-input-number .el-input__wrapper) {
  @apply shadow-none border border-gray-300 rounded-md;
}

:deep(.custom-btn-primary) {
  @apply bg-blue-500 border-blue-500 hover:bg-blue-600 hover:border-blue-600;
}

:deep(.custom-btn-cancel) {
  @apply border-gray-300 text-gray-700 hover:bg-gray-50;
}

/* 修改 z-index 層級 */
.swal2-high-z-index {
  z-index: 100000 !important; /* 提高到比 modal 更高的層級 */
}

.swal2-container {
  z-index: 100000 !important; /* 提高到比 modal 更高的層級 */
}

/* Modal 相關的 z-index */
.modal-backdrop {
  z-index: 9999;
}

.modal-content {
  z-index: 10000;
}

/* 將 Sweetalert2 的樣式設置為全局 */
:root {
  --z-modal: 9999;
  --z-sweetalert: 999999;
}

/* Sweetalert2 相關樣式 */
.swal2-container {
  z-index: var(--z-sweetalert) !important;
}

.swal2-popup {
  z-index: calc(var(--z-sweetalert) + 1) !important;
}

.swal2-backdrop-show {
  background: rgba(0, 0, 0, 0.4) !important;
}

/* Modal 相關樣式 */
.modal-backdrop {
  z-index: var(--z-modal);
}

.modal-content {
  z-index: calc(var(--z-modal) + 1);
}
</style> 