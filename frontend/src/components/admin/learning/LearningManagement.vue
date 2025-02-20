<template>
  <div class="space-y-6">
    <!-- 頂部工具列 -->
    <div class="bg-white rounded-lg shadow-sm p-4">
      <div class="flex flex-col space-y-4">
        <!-- 標題和新增按鈕 -->
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-bold text-gray-800">學習內容管理</h2>
          <button @click="showModal = true; editingSection = null"
                  class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 
                         transition-colors duration-200 flex items-center">
            <i class="fas fa-plus mr-2"></i>新增主標題
          </button>
        </div>

        <!-- 分隔線 -->
        <div class="border-b border-gray-200"></div>

        <!-- 功能區 -->
        <div class="flex justify-between items-center">
          <!-- 左側：視圖切換 -->
          <div class="flex space-x-1">
            <button @click="viewMode = 'card'"
                    :class="[
                      'px-4 py-2 rounded-md text-sm font-medium transition-colors',
                      viewMode === 'card' 
                        ? 'bg-blue-50 text-blue-600 shadow-sm border border-blue-200' 
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-800'
                    ]">
              <i class="fas fa-th-large mr-2"></i>卡片
            </button>
            <button @click="viewMode = 'list'"
                    :class="[
                      'px-4 py-2 rounded-md text-sm font-medium transition-colors',
                      viewMode === 'list'
                        ? 'bg-blue-50 text-blue-600 shadow-sm border border-blue-200'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-800'
                    ]">
              <i class="fas fa-list mr-2"></i>列表
            </button>
          </div>
          
          <!-- 右側：搜尋框 -->
          <div class="flex items-center space-x-4">
            <div class="relative">
              <input v-model="searchQuery"
                     type="text"
                     class="w-64 px-4 py-2 pr-10 border rounded-lg focus:ring-2 
                            focus:ring-blue-500 focus:border-transparent"
                     placeholder="搜尋標題或內容...">
              <span class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
                <i class="fas fa-search"></i>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 學習區塊列表 -->
    <div class="bg-white rounded-lg shadow-sm p-4">
      <!-- 當前位置提示 -->
      <div class="mb-4 text-sm text-gray-500">
        <span class="font-medium text-gray-700">當前位置：</span>
        學習內容管理
      </div>

      <TransitionGroup 
        :name="viewMode === 'card' ? 'layout-card' : 'layout-list'"
        tag="div"
        :class="[
          viewMode === 'card' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6' : 'space-y-4'
        ]">
        <!-- 無資料時顯示 -->
        <div v-if="!filteredSections.length" 
             :class="viewMode === 'card' ? 'col-span-full' : ''">
          <div class="bg-white rounded-xl shadow-sm p-8 text-center">
            <div class="text-gray-400 mb-4">
              <i class="fas fa-book-open text-4xl"></i>
            </div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">
              {{ searchQuery ? '找不到相關內容' : '尚無學習內容' }}
            </h3>
            <p class="text-gray-500 mb-4">
              {{ searchQuery ? '請嘗試其他關鍵字' : '點擊上方按鈕開始新增學習內容' }}
            </p>
          </div>
        </div>

        <!-- 學習區塊卡片/列表項目 -->
        <div v-for="section in filteredSections" 
             :key="section.id" 
             :class="[
               'bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition-shadow duration-200 border-2 border-blue-100',
               viewMode === 'list' ? 'max-w-5xl mx-auto' : ''
             ]">
          <!-- 卡片標題區 -->
          <div class="p-6 bg-gradient-to-r from-blue-50 to-indigo-50 border-b-2 border-blue-100">
            <div class="flex justify-between items-start mb-4">
              <div>
                <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full mb-2 inline-block">
                  主標題
                </span>
                <h3 class="text-xl font-semibold text-gray-800">{{ section.title }}</h3>
              </div>
              <div class="flex space-x-2">
                <button @click="showAddSubsectionModal(section)"
                        class="p-2 text-blue-600 hover:bg-blue-100 rounded-lg transition-colors"
                        title="新增次標題">
                  <i class="fas fa-plus-circle"></i>
                </button>
                <button @click="editSection(section)"
                        class="p-2 text-gray-600 hover:bg-gray-50 rounded-lg transition-colors">
                  <i class="fas fa-edit"></i>
                </button>
                <button @click="deleteSection(section.id)"
                        class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
            <p class="text-gray-600 text-sm mt-2">{{ section.description }}</p>
          </div>

          <!-- 子區塊列表 -->
          <div :class="[
            'p-4',
            viewMode === 'card' ? 'space-y-4' : 'space-y-2'
          ]">
            <!-- 無次標題時顯示 -->
            <div v-if="!section.subsections || section.subsections.length === 0" 
                 class="text-center py-8 text-gray-500">
              <i class="fas fa-list-ul text-2xl mb-2"></i>
              <p>尚無次標題內容</p>
            </div>
            
            <!-- 次標題列表 -->
            <div v-else class="grid gap-4"
                 :class="[
                   viewMode === 'card' ? 'grid-cols-1' : 'grid-cols-1',
                   section.subsections.length > 1 ? 'max-h-[300px] overflow-y-auto pr-2' : ''
                 ]">
              <div v-for="subsection in section.subsections" 
                   :key="subsection.id"
                   class="group p-4 bg-white rounded-lg border border-gray-200 
                          hover:border-blue-200 hover:shadow-md transition-all duration-200">
                <div class="flex justify-between items-start">
                  <div class="flex-1 mr-4">
                    <!-- 標題區域 -->
                    <div class="flex items-center space-x-2 mb-2">
                      <span class="px-2 py-1 bg-gray-100 text-gray-600 text-xs 
                                 font-medium rounded-full">
                        次標題
                      </span>
                      <h4 class="font-medium text-gray-800 text-lg">
                        {{ subsection.title }}
                      </h4>
                    </div>
                    
                    <!-- 內容區域 -->
                    <p class="text-sm text-gray-600 mb-3 line-clamp-2 group-hover:line-clamp-none 
                              transition-all duration-300">
                      {{ subsection.content }}
                    </p>
                    
                    <!-- 圖片預覽 -->
                    <div v-if="subsection.images && subsection.images.length > 0" 
                         class="flex flex-wrap gap-2">
                      <div v-for="(image, index) in subsection.images.slice(0, 4)" 
                           :key="index"
                           class="relative group/image">
                        <img :src="getImageUrl(image)"
                             class="w-16 h-16 rounded-lg object-cover cursor-zoom-in 
                                    hover:opacity-75 transition-opacity shadow-sm"
                             @click="previewImage(getImageUrl(image))"
                             @error="handleImageError($event)">
                        <!-- 如果有更多圖片，顯示數量提示 -->
                        <div v-if="index === 3 && subsection.images.length > 4"
                             class="absolute inset-0 bg-black/50 rounded-lg flex items-center 
                                    justify-center text-white text-sm font-medium">
                          +{{ subsection.images.length - 4 }}
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 操作按鈕 -->
                  <div class="flex space-x-1">
                    <button @click="editSubsection(subsection)"
                            class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg 
                                   transition-colors">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="deleteSubsection(subsection.id)"
                            class="p-2 text-red-600 hover:bg-red-100 rounded-lg 
                                   transition-colors">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </TransitionGroup>
    </div>

    <!-- 新增/編輯彈窗 -->
    <div v-if="showModal" 
        class="fixed inset-0 z-[9999]">
      <!-- 背景遮罩 -->
      <div class="fixed inset-0 bg-black bg-opacity-50"></div>
      
      <!-- Modal 內容 -->
      <div class="absolute inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <div class="relative bg-white rounded-lg shadow-lg w-full max-w-2xl">
            <!-- Modal 標題 -->
            <div class="flex justify-between items-center px-6 py-4 border-b">
              <h3 class="text-lg font-semibold">{{ editingSection ? '編輯學習內容' : '新增學習內容' }}</h3>
              <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
                <i class="fas fa-times"></i>
              </button>
            </div>

            <!-- Modal 內容 -->
            <div class="px-6 py-4 space-y-4 max-h-[calc(85vh-8rem)] overflow-y-auto">
              <!-- 標題 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1 required-field">
                  主標題
                </label>
                <input type="text" 
                       v-model="form.title"
                       class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                       :class="{'border-red-500': errors.title}"
                       placeholder="請輸入主標題">
                <span v-if="errors.title" class="text-red-500 text-xs mt-1">{{ errors.title }}</span>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  描述
                </label>
                <textarea v-model="form.description"
                         rows="4"
                         class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                         placeholder="請輸入描述"></textarea>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  排序
                  <span class="text-red-500">*</span>
                </label>
                <input v-model="form.sort_order"
                       type="number"
                       min="1"
                       class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                       :class="{'border-red-500': errors.sort_order}"
                       placeholder="請輸入排序">
                <p v-if="errors.sort_order" class="mt-1 text-sm text-red-500">
                  {{ errors.sort_order }}
                </p>
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

    <!-- 新增/編輯次標題對話框 -->
    <div v-if="showSubsectionModal" 
        class="fixed inset-0 z-[9999]">
      <!-- 背景遮罩 -->
      <div class="fixed inset-0 bg-black bg-opacity-50"></div>
      
      <!-- Modal 內容 -->
      <div class="absolute inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <div class="relative bg-white rounded-lg shadow-lg w-full max-w-2xl">
            <!-- 標題列 -->
            <div class="px-6 py-4 border-b flex justify-between items-center">
              <h3 class="text-xl font-semibold text-gray-800">
                {{ editingSubsection ? '編輯次標題' : '新增次標題' }}
              </h3>
              <button @click="closeSubsectionModal" 
                      class="text-gray-400 hover:text-gray-500 transition-colors">
                <i class="fas fa-times text-xl"></i>
              </button>
            </div>
            
            <!-- 表單內容 -->
            <div class="p-6">
              <form @submit.prevent="handleSubsectionSubmit" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    標題
                    <span class="text-red-500">*</span>
                  </label>
                  <input v-model="subsectionForm.title"
                         type="text"
                         class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                         :class="{'border-red-500': subsectionErrors.title}"
                         placeholder="請輸入標題">
                  <p v-if="subsectionErrors.title" class="mt-1 text-sm text-red-500">
                    {{ subsectionErrors.title }}
                  </p>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    內容
                    <span class="text-red-500">*</span>
                  </label>
                  <textarea v-model="subsectionForm.content"
                           rows="4"
                           class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                           :class="{'border-red-500': subsectionErrors.content}"
                           placeholder="請輸入內容"></textarea>
                  <p v-if="subsectionErrors.content" class="mt-1 text-sm text-red-500">
                    {{ subsectionErrors.content }}
                  </p>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    圖片
                  </label>
                  <input type="file"
                         ref="fileInput"
                         @change="handleFileChange"
                         multiple
                         accept="image/*"
                         class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                </div>

                <!-- 已上傳圖片預覽 -->
                <div v-if="subsectionForm.images?.length" class="grid grid-cols-4 gap-2">
                  <div v-for="(image, index) in subsectionForm.images"
                       :key="index"
                       class="relative group">
                    <img :src="getImageUrl(image)"
                         class="w-full h-20 object-cover rounded-lg"
                         @error="handleImageError">
                    <button @click="removeImage(index)"
                            class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-red-600">
                      <i class="fas fa-times"></i>
                    </button>
                  </div>
                </div>
              </form>
            </div>

            <!-- 按鈕列 -->
            <div class="px-6 py-4 border-t bg-gray-50 rounded-b-xl flex justify-end space-x-3">
              <button @click="closeSubsectionModal"
                      class="px-4 py-2 border rounded-lg hover:bg-gray-100 transition-colors">
                取消
              </button>
              <button @click="handleSubsectionSubmit"
                      class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
                {{ editingSubsection ? '更新' : '新增' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 圖片預覽 Modal -->
    <div v-if="previewImageUrl" 
        class="fixed inset-0 z-[9999]">
      <!-- 背景遮罩 -->
      <div class="absolute inset-0 bg-black bg-opacity-90 backdrop-blur-sm"></div>
      
      <!-- Modal 內容 -->
      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex items-center justify-center min-h-full p-4">
          <!-- 關閉按鈕 -->
          <button class="absolute top-4 right-4 text-white/80 hover:text-white transition-colors z-[100000]"
                  @click="closePreview">
            <i class="fas fa-times text-2xl"></i>
          </button>
          <!-- 圖片容器 -->
          <img :src="previewImageUrl"
               class="max-w-[90vw] max-h-[80vh] object-contain select-none rounded-lg shadow-2xl"
               @click.stop
               alt="圖片預覽">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, reactive, computed, onUnmounted } from 'vue'
import { learningAPI } from '@/api'
import Swal from 'sweetalert2'
import { useLogger } from '@/composables/useLogger'

export default {
  name: 'LearningManagement',
  
  setup() {
    const sections = ref([])
    const viewMode = ref('card')
    const searchQuery = ref('')
    const showModal = ref(false)
    const editingSection = ref(null)
    const errors = reactive({})
    const showSubsectionModal = ref(false)
    const editingSubsection = ref(null)
    const currentSectionId = ref(null)
    const subsectionErrors = reactive({})
    const fileInput = ref(null)
    const previewImageUrl = ref(null)
    
    const form = reactive({
      title: '',
      description: '',
      sort_order: 1
    })

    const subsectionForm = reactive({
      title: '',
      content: '',
      images: []
    })

    const defaultAvatar = 'https://api.dicebear.com/7.x/avataaars/svg?seed=default'

    const { logOperation } = useLogger()

    // 處理圖片 URL
    const getImageUrl = (avatar) => {
      if (!avatar) return defaultAvatar
      if (avatar.startsWith('http')) return avatar
      return `${import.meta.env.VITE_BACKEND_URL}/api/learning/uploads/${avatar.split('/').pop()}`
    }

    // 處理圖片載入錯誤
    const handleImageError = (event) => {
      event.target.src = defaultAvatar
    }

    // 獲取所有區塊
    const fetchSections = async () => {
      try {
        const response = await learningAPI.getLearningBlocks()
        sections.value = response.data.sections || []
        await logOperation('【學習管理】查看學習區塊列表', '查看')
      } catch (error) {
        console.error('獲取學習區塊失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '獲取資料失敗',
          text: error.response?.data?.message || '請稍後再試'
        })
      }
    }

    // 檢查排序是否重複
    const checkSortOrderDuplicate = (sortOrder, sectionId = null) => {
      return sections.value.some(section => 
        section.sort_order === Number(sortOrder) && section.id !== sectionId
      )
    }

    // 表單提交
    const handleSubmit = async () => {
      // 驗證
      errors.value = {}
      
      if (!form.title) {
        errors.title = '請輸入標題'
        return
      }
      
      if (!form.sort_order) {
        errors.sort_order = '請輸入排序'
        return
      }
      
      if (form.sort_order < 1) {
        errors.sort_order = '排序不能小於1'
        return
      }
      
      // 檢查排序是否重複
      if (checkSortOrderDuplicate(form.sort_order, editingSection.value?.id)) {
        errors.sort_order = '此排序已被使用'
        return
      }

      try {
        if (editingSection.value) {
          await learningAPI.updateSection(editingSection.value.id, form)
          await logOperation(`【學習管理】更新主標題: ${form.title}`, '修改')
        } else {
          await learningAPI.createSection(form)
          await logOperation(`【學習管理】新增主標題: ${form.title}`, '新增')
        }
        
        await fetchSections()
        closeModal()
        
        Swal.fire({
          icon: 'success',
          title: `${editingSection.value ? '更新' : '新增'}成功`,
          timer: 1500,
          showConfirmButton: false
        })
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: `${editingSection.value ? '更新' : '新增'}失敗`,
          text: error.response?.data?.message || '請稍後再試'
        })
      }
    }

    // 初始化表單
    const resetForm = () => {
      form.title = ''
      form.description = ''
      form.sort_order = 1
      Object.keys(errors).forEach(key => delete errors[key])
    }

    // 打開編輯對話框
    const editSection = (section) => {
      editingSection.value = section
      form.title = section.title
      form.description = section.description
      form.sort_order = section.sort_order
      showModal.value = true
    }

    // 關閉對話框
    const closeModal = () => {
      showModal.value = false
      editingSection.value = null
      resetForm()
    }

    // 初始化次標題表單
    const initSubsectionForm = () => {
      subsectionForm.title = ''
      subsectionForm.content = ''
      subsectionForm.images = []
      Object.keys(subsectionErrors).forEach(key => delete subsectionErrors[key])
    }

    // 打開新增次標題對話框
    const showAddSubsectionModal = (section) => {
      currentSectionId.value = section.id
      editingSubsection.value = null
      initSubsectionForm()
      showSubsectionModal.value = true
    }

    // 打開編輯次標題對話框
    const editSubsection = (subsection) => {
      editingSubsection.value = subsection
      currentSectionId.value = subsection.section_id
      subsectionForm.title = subsection.title
      subsectionForm.content = subsection.content
      subsectionForm.images = [...(subsection.images || [])]
      showSubsectionModal.value = true
    }

    // 關閉次標題對話框
    const closeSubsectionModal = () => {
      showSubsectionModal.value = false
      editingSubsection.value = null
      currentSectionId.value = null
      initSubsectionForm()
    }

    // 處理文件選擇
    const handleFileChange = async (event) => {
      const files = event.target.files
      if (!files.length) return

      for (const file of files) {
        const formData = new FormData()
        formData.append('file', file)
        try {
          const response = await learningAPI.uploadImage(formData)
          subsectionForm.images.push(response.data.url)
        } catch (error) {
          Swal.fire({
            icon: 'error',
            title: '圖片上傳失敗',
            text: error.response?.data?.message || '請稍後再試'
          })
        }
      }
      // 清空 input，允許重複上傳相同文件
      fileInput.value.value = ''
    }

    // 移除圖片
    const removeImage = (index) => {
      subsectionForm.images.splice(index, 1)
    }

    // 提交次標題表單
    const handleSubsectionSubmit = async () => {
      // 驗證
      if (!subsectionForm.title) {
        subsectionErrors.title = '請輸入標題'
        return
      }
      if (!subsectionForm.content) {
        subsectionErrors.content = '請輸入內容'
        return
      }

      try {
        if (editingSubsection.value) {
          await learningAPI.updateSubsection(editingSubsection.value.id, subsectionForm)
          await logOperation(`【學習管理】更新次標題: ${subsectionForm.title}`, '修改')
        } else {
          await learningAPI.createSubsection({
            ...subsectionForm,
            section_id: currentSectionId.value
          })
          await logOperation(`【學習管理】新增次標題: ${subsectionForm.title}`, '新增')
        }
        
        await fetchSections()
        closeSubsectionModal()
        
        Swal.fire({
          icon: 'success',
          title: `${editingSubsection.value ? '更新' : '新增'}成功`,
          timer: 1500,
          showConfirmButton: false
        })
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: `${editingSubsection.value ? '更新' : '新增'}失敗`,
          text: error.response?.data?.message || '請稍後再試'
        })
      }
    }

    // 刪除主標題區塊
    const deleteSection = async (id) => {
      const result = await Swal.fire({
        title: '確定要刪除嗎？',
        text: '此操作將同時刪除該區塊下的所有內容',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '確定刪除',
        cancelButtonText: '取消',
        confirmButtonColor: '#dc2626'
      })

      if (result.isConfirmed) {
        try {
          const section = sections.value.find(s => s.id === id)
          await learningAPI.deleteSection(id)
          await logOperation(`【學習管理】刪除主標題: ${section.title}`, '刪除')
          await fetchSections()
          Swal.fire({
            icon: 'success',
            title: '刪除成功',
            timer: 1500,
            showConfirmButton: false
          })
        } catch (error) {
          Swal.fire({
            icon: 'error',
            title: '刪除失敗',
            text: error.response?.data?.message || '請稍後再試'
          })
        }
      }
    }

    // 刪除次標題區塊
    const deleteSubsection = async (id) => {
      const result = await Swal.fire({
        title: '確定要刪除嗎？',
        text: '此操作無法復原',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '確定刪除',
        cancelButtonText: '取消',
        confirmButtonColor: '#dc2626'
      })

      if (result.isConfirmed) {
        try {
          const section = sections.value.find(s => 
            s.subsections.some(sub => sub.id === id)
          )
          const subsection = section.subsections.find(sub => sub.id === id)
          await learningAPI.deleteSubsection(id)
          await logOperation(`【學習管理】刪除次標題: ${subsection.title}`, '刪除')
          await fetchSections()
          Swal.fire({
            icon: 'success',
            title: '刪除成功',
            timer: 1500,
            showConfirmButton: false
          })
        } catch (error) {
          Swal.fire({
            icon: 'error',
            title: '刪除失敗',
            text: error.response?.data?.message || '請稍後再試'
          })
        }
      }
    }

    // 圖片預覽
    const previewImage = (url) => {
      previewImageUrl.value = url
      document.body.style.overflow = 'hidden'
    }

    // 關閉預覽
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

    // 過濾區塊
    const filteredSections = computed(() => {
      if (!searchQuery.value) return sections.value
      
      const query = searchQuery.value.toLowerCase()
      return sections.value.filter(section => {
        // 搜尋主標題和描述
        const matchSection = section.title.toLowerCase().includes(query) ||
                            section.description?.toLowerCase().includes(query)
        
        // 搜尋次標題和內容
        const matchSubsections = section.subsections?.some(sub => 
          sub.title.toLowerCase().includes(query) ||
          sub.content.toLowerCase().includes(query)
        )
        
        return matchSection || matchSubsections
      })
    })

    onMounted(async () => {
      await fetchSections()
      await logOperation('【學習管理】訪問學習管理頁面', '查看')
      window.addEventListener('keydown', handleKeyDown)
    })

    onUnmounted(() => {
      window.removeEventListener('keydown', handleKeyDown)
      document.body.style.overflow = ''
    })

    return {
      sections,
      viewMode,
      searchQuery,
      showModal,
      editingSection,
      form,
      errors,
      editSection,
      closeModal,
      handleSubmit,
      showAddSubsectionModal,
      deleteSection,
      deleteSubsection,
      previewImage,
      getImageUrl,
      handleImageError,
      showSubsectionModal,
      editingSubsection,
      subsectionForm,
      subsectionErrors,
      fileInput,
      editSubsection,
      closeSubsectionModal,
      handleSubsectionSubmit,
      handleFileChange,
      removeImage,
      filteredSections,
      previewImageUrl,
      closePreview
    }
  }
}
</script>

<style scoped>
/* 對話框容器 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* 對話框內容動畫 */
.modal-enter-active .bg-white,
.modal-leave-active .bg-white {
  transition: all 0.3s ease;
}

.modal-enter-from .bg-white,
.modal-leave-to .bg-white {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}

/* 背景遮罩動畫 */
.modal-enter-from::before,
.modal-leave-to::before {
  opacity: 0;
}

.modal-enter-active::before,
.modal-leave-active::before {
  transition: opacity 0.2s ease;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 美化 SweetAlert2 的輸入框 */
:deep(.swal2-input),
:deep(.swal2-textarea) {
  margin: 1em auto;
  width: 100%;
  max-width: none;
}

:deep(.swal2-textarea) {
  height: 120px;
}

/* 卡片視圖動畫 */
.layout-card-move {
  transition: all 0.6s ease;
}

.layout-card-enter-active,
.layout-card-leave-active {
  transition: all 0.6s ease;
  position: absolute;
}

.layout-card-enter-from,
.layout-card-leave-to {
  opacity: 0;
  transform: scale(0.3);
}

/* 列表視圖動畫 */
.layout-list-move {
  transition: all 0.6s ease;
}

.layout-list-enter-active,
.layout-list-leave-active {
  transition: all 0.6s ease;
}

.layout-list-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.layout-list-leave-to {
  opacity: 0;
  transform: translateX(30px);
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

/* 自定義滾動條樣式 */
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: rgba(203, 213, 225, 0.5) transparent;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(203, 213, 225, 0.5);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background-color: rgba(203, 213, 225, 0.8);
}

/* 平滑過渡效果 */
.line-clamp-2 {
  transition: -webkit-line-clamp 0.3s ease;
}
</style> 