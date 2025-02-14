<template>
  <div class="min-h-screen max-w-4xl mx-auto px-4">
    <!-- 頁籤切換 -->
    <div class="mb-6 bg-white/50 backdrop-blur-sm rounded-xl shadow-sm overflow-hidden border border-white/20">
      <nav class="flex">
        <button v-for="tab in tabs" 
                :key="tab.key"
                @click="currentTab = tab.key"
                :class="[
                  'flex-1 px-6 py-4 text-sm font-medium transition-all duration-200 border-b-2 flex items-center justify-center space-x-2',
                  currentTab === tab.key 
                    ? 'text-blue-600 border-blue-600' 
                    : 'text-gray-500 border-transparent hover:text-gray-700 hover:border-gray-300'
                ]">
          <i :class="tab.icon"></i>
          <span>{{ tab.name }}</span>
        </button>
      </nav>
    </div>

    <!-- 知識庫上傳 -->
    <div v-if="currentTab === 'upload'" 
         class="bg-white/50 backdrop-blur-sm rounded-xl shadow-sm overflow-hidden border border-white/20">
      <!-- 表單標題 -->
      <div class="px-8 py-6 border-b border-gray-100/50 bg-white/80 transition-all duration-300">
        <h2 class="text-xl font-semibold text-gray-800">上傳知識庫文件</h2>
        <p class="mt-1 text-sm text-gray-500">請填寫必要資訊並選擇要上傳的檔案</p>
      </div>

      <div class="p-8 bg-white/80 transition-all duration-300">
        <div class="grid gap-8">
          <!-- 知識庫流程ID -->
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700 required-field">
              知識庫流程ID
            </label>
            <div class="relative">
              <i class="fas fa-hashtag absolute left-3 top-3 text-gray-400"></i>
              <input type="text"
                     v-model="uploadForm.flowId"
                     placeholder="請輸入知識庫流程ID"
                     class="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300">
            </div>
          </div>

          <!-- 上傳檔案區域 -->
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700 required-field">
              上傳檔案
            </label>
            <div class="border-2 border-dashed border-gray-200 rounded-xl bg-gray-50 p-8 text-center 
                transition-all duration-300 cursor-pointer"
                :class="[
                  isDragging ? 'border-blue-500 bg-blue-50 shadow-lg scale-[1.02]' : 'hover:border-blue-500 hover:bg-blue-50 hover:shadow-lg hover:-translate-y-1',
                  dragError ? 'border-red-500 bg-red-50' : ''
                ]"
                @click="$refs.fileInput.click()"
                @dragover.prevent="handleDragOver"
                @dragleave.prevent="handleDragLeave"
                @drop.prevent="handleFileDrop">
              <div class="space-y-4">
                <div class="w-16 h-16 mx-auto bg-blue-100 rounded-full flex items-center justify-center 
                            transform transition-transform duration-300 group-hover:scale-110">
                  <i :class="[
                    'text-2xl transition-all',
                    dragError ? 'fas fa-times text-red-500' : 'fas fa-cloud-upload-alt text-blue-500'
                  ]"></i>
                </div>
                <div>
                  <p class="text-sm font-medium" :class="dragError ? 'text-red-600' : 'text-gray-700'">
                    {{ dragError ? '不支援的檔案類型' : '拖曳檔案至此處或點擊上傳' }}
                  </p>
                  <p class="text-xs text-gray-500 mt-1">
                    支援的檔案類型：CSV、Excel、PDF、Markdown、Word、Text
                  </p>
                </div>
              </div>
              <input type="file"
                     @change="handleFileChange"
                     class="hidden"
                     ref="fileInput"
                     accept=".csv,.xlsx,.xls,.pdf,.md,.docx,.txt"
                     multiple>
            </div>
          </div>

          <!-- 已選檔案列表 -->
          <div v-if="selectedFiles.length > 0" class="space-y-3">
            <div class="flex justify-between items-center">
              <div class="flex items-center space-x-4">
                <div class="text-sm font-medium text-gray-700">已選擇的檔案</div>
                <!-- 視圖切換按鈕 -->
                <div class="flex bg-gray-100 rounded-lg p-1">
                  <button @click="viewMode = 'list'"
                          :class="[
                            'px-2 py-1 rounded text-sm transition-colors',
                            viewMode === 'list' 
                              ? 'bg-white text-gray-800 shadow-sm' 
                              : 'text-gray-600 hover:text-gray-800'
                          ]">
                    <i class="fas fa-list"></i>
                  </button>
                  <button @click="viewMode = 'card'"
                          :class="[
                            'px-2 py-1 rounded text-sm transition-colors',
                            viewMode === 'card' 
                              ? 'bg-white text-gray-800 shadow-sm' 
                              : 'text-gray-600 hover:text-gray-800'
                          ]">
                    <i class="fas fa-th-large"></i>
                  </button>
                </div>
              </div>
              <button @click="removeAllFiles"
                      class="px-3 py-1.5 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors flex items-center space-x-2 text-sm">
                <i class="fas fa-trash-alt"></i>
                <span>批次移除</span>
              </button>
            </div>

            <!-- 列表視圖 -->
            <div v-if="viewMode === 'list'" class="space-y-2">
              <div v-for="(file, index) in selectedFiles" 
                   :key="index"
                   class="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200 hover:border-blue-200 transition-colors">
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                    <i :class="[getFileIcon(file.name), 'text-blue-600']"></i>
                  </div>
                  <div>
                    <div class="text-sm font-medium text-gray-700">{{ file.name }}</div>
                    <div class="text-xs text-gray-500">{{ formatFileSize(file.size) }}</div>
                  </div>
                </div>
                <button @click="removeFile(index)"
                        class="w-8 h-8 rounded-full hover:bg-red-50 text-red-500 flex items-center justify-center transition-colors">
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </div>

            <!-- 卡片視圖 -->
            <div v-else class="grid grid-cols-2 sm:grid-cols-3 gap-4">
              <div v-for="(file, index) in selectedFiles"
                   :key="index"
                   class="group relative bg-white p-4 rounded-xl border border-gray-200 hover:border-blue-200 transition-all">
                <div class="flex flex-col items-center text-center space-y-3">
                  <div class="w-16 h-16 rounded-xl bg-blue-50 flex items-center justify-center">
                    <i :class="[getFileIcon(file.name), 'text-blue-600 text-2xl']"></i>
                  </div>
                  <div>
                    <div class="text-sm font-medium text-gray-700 truncate max-w-[150px]">{{ file.name }}</div>
                    <div class="text-xs text-gray-500 mt-1">{{ formatFileSize(file.size) }}</div>
                  </div>
                </div>
                <button @click="removeFile(index)"
                        class="absolute top-2 right-2 w-6 h-6 rounded-full bg-red-50 text-red-500 
                               opacity-0 group-hover:opacity-100 hover:bg-red-100 
                               flex items-center justify-center transition-all">
                  <i class="fas fa-times text-xs"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 上傳按鈕 -->
        <div class="mt-8 flex justify-end">
          <button @click="uploadFiles"
                  :disabled="!canUpload"
                  class="px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 flex items-center space-x-2">
            <i class="fas fa-upload"></i>
            <span>開始上傳</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 知識庫管理 -->
    <div v-else-if="currentTab === 'manage'" 
         class="bg-white/50 backdrop-blur-sm rounded-xl shadow-sm overflow-hidden border border-white/20">
      <!-- 查詢條件 -->
      <div class="px-8 py-6 border-b border-gray-100/50 bg-white/80">
        <div class="flex justify-between items-center">
          <div>
            <h2 class="text-xl font-semibold text-gray-800">查詢知識庫文件</h2>
            <p class="mt-1 text-sm text-gray-500">請輸入查詢條件</p>
          </div>
        </div>
      </div>

      <div class="p-8 bg-white">
        <div class="grid gap-6">
          <!-- 知識庫流程ID -->
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700 required-field">
              知識庫流程ID
            </label>
            <div class="relative">
              <i class="fas fa-hashtag absolute left-3 top-3 text-gray-400"></i>
              <input type="text"
                     v-model="searchForm.flowId"
                     placeholder="請輸入知識庫流程ID"
                     class="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            </div>
          </div>
        </div>

        <!-- 查詢按鈕 -->
        <div class="mt-6 flex justify-end">
          <button @click="handleSearch"
                  :disabled="!canSearch"
                  class="px-8 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 flex items-center space-x-2">
            <i class="fas fa-search"></i>
            <span>查詢</span>
          </button>
        </div>

        <!-- 查詢結果 -->
        <div v-if="hasSearched" class="mt-8">
          <div v-if="searchResults.length > 0">
            <div class="flex justify-between items-center mb-4">
              <div class="flex items-center space-x-4">
                <h3 class="text-lg font-medium text-gray-800">查詢結果</h3>
                <!-- 全選功能 -->
                <div class="flex items-center space-x-2">
                  <input type="checkbox"
                         :checked="isAllSelected"
                         @change="toggleSelectAll"
                         class="w-4 h-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500">
                  <span class="text-sm text-gray-600">全選</span>
                </div>
                <!-- 視圖切換按鈕 -->
                <div class="flex bg-gray-100 rounded-lg p-1">
                  <button @click="searchViewMode = 'list'"
                          :class="[
                            'px-2 py-1 rounded text-sm transition-colors',
                            searchViewMode === 'list' 
                              ? 'bg-white text-gray-800 shadow-sm' 
                              : 'text-gray-600 hover:text-gray-800'
                          ]">
                    <i class="fas fa-list"></i>
                  </button>
                  <button @click="searchViewMode = 'card'"
                          :class="[
                            'px-2 py-1 rounded text-sm transition-colors',
                            searchViewMode === 'card' 
                              ? 'bg-white text-gray-800 shadow-sm' 
                              : 'text-gray-600 hover:text-gray-800'
                          ]">
                    <i class="fas fa-th-large"></i>
                  </button>
                </div>
              </div>
              <div class="flex items-center space-x-2" v-if="selectedFiles.length > 0">
                <button @click="batchDownloadFiles"
                        class="px-4 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors flex items-center space-x-2">
                  <i class="fas fa-download"></i>
                  <span>批次下載 ({{ selectedFiles.length }})</span>
                </button>
                <button @click="batchDeleteFiles"
                        class="px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors flex items-center space-x-2">
                  <i class="fas fa-trash-alt"></i>
                  <span>批次刪除 ({{ selectedFiles.length }})</span>
                </button>
              </div>
            </div>
            <!-- 列表視圖 -->
            <div v-if="searchViewMode === 'list'" class="grid gap-4">
              <div v-for="file in searchResults" 
                   :key="file"
                   class="bg-white border border-gray-200 rounded-xl p-4 hover:border-blue-200 transition-colors">
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-4">
                    <input type="checkbox"
                           :checked="isFileSelected(file)"
                           @change="toggleFileSelection(file)"
                           class="w-4 h-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500">
                    <div class="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center">
                      <i :class="[getFileIcon(file), 'text-blue-600 text-xl']"></i>
                    </div>
                    <div>
                      <div class="text-sm font-medium text-gray-800">{{ file }}</div>
                      <div class="flex items-center space-x-4 mt-1">
                        <!-- 移除檔案大小和上傳時間，因為 API 沒有提供這些資訊 -->
                      </div>
                    </div>
                  </div>
                  <div class="flex items-center space-x-2">
                    <button @click="downloadFile(searchForm.flowId, file)"
                            class="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 hover:bg-blue-100 flex items-center justify-center transition-colors">
                      <i class="fas fa-download"></i>
                    </button>
                    <button @click="deleteFile(searchForm.flowId, file)"
                            class="w-8 h-8 rounded-lg bg-red-50 text-red-600 hover:bg-red-100 flex items-center justify-center transition-colors">
                      <i class="fas fa-trash-alt"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <!-- 卡片視圖 -->
            <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
              <div v-for="file in searchResults"
                   :key="file"
                   class="group relative bg-white p-4 rounded-xl border border-gray-200 hover:border-blue-200 transition-all">
                <div class="absolute top-2 right-2 flex space-x-1">
                  <input type="checkbox"
                         :checked="isFileSelected(file)"
                         @change="toggleFileSelection(file)"
                         class="w-4 h-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500">
                </div>
                <div class="flex flex-col items-center text-center space-y-3 mb-12">
                  <div class="w-16 h-16 rounded-xl bg-blue-50 flex items-center justify-center">
                    <i :class="[getFileIcon(file), 'text-blue-600 text-2xl']"></i>
                  </div>
                  <div>
                    <div class="text-sm font-medium text-gray-800 break-all line-clamp-2 max-w-[150px]">
                      {{ file }}
                    </div>
                  </div>
                </div>
                <div class="absolute bottom-2 left-0 right-0 flex justify-center space-x-2 px-2">
                  <button @click="downloadFile(searchForm.flowId, file)"
                          class="w-7 h-7 rounded-lg bg-blue-50 text-blue-600 hover:bg-blue-100 flex items-center justify-center transition-colors">
                    <i class="fas fa-download text-sm"></i>
                  </button>
                  <button @click="deleteFile(searchForm.flowId, file)"
                          class="w-7 h-7 rounded-lg bg-red-50 text-red-600 hover:bg-red-100 flex items-center justify-center transition-colors">
                    <i class="fas fa-trash-alt text-sm"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-12">
            <div class="w-20 h-20 mx-auto bg-gray-100 rounded-full flex items-center justify-center mb-4">
              <i class="fas fa-search text-3xl text-gray-400"></i>
            </div>
            <p class="text-gray-500">沒有找到相關檔案</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { knowledgeAPI } from '@/api'
import DataTable from '../common/DataTable.vue'
import Swal from 'sweetalert2'
import { useLogger } from '@/composables/useLogger'

export default {
  name: 'KnowledgeManagement',
  components: { DataTable },
  
  setup() {
    const { logOperation } = useLogger()
    const files = ref([])
    const currentTab = ref('upload')
    const selectedFiles = ref([])
    const fileInput = ref(null)
    const searchForm = ref({
      flowId: ''
    })
    const hasSearched = ref(false)
    const searchResults = ref([])
    const viewMode = ref('list')
    const searchViewMode = ref('list')
    const isDragging = ref(false)
    const dragError = ref(false)

    const tabs = [
      { 
        key: 'upload', 
        name: '知識庫上傳',
        icon: 'fas fa-cloud-upload-alt'
      },
      { 
        key: 'manage', 
        name: '知識庫管理',
        icon: 'fas fa-cog'
      }
    ]

    const uploadForm = ref({
      flowId: '',
    })

    const columns = [
      { key: 'file_name', label: '檔案名稱' },
      { key: 'file_size', label: '檔案大小' },
      { key: 'created_at', label: '上傳時間' },
      { key: 'actions', label: '操作' }
    ]

    const canUpload = computed(() => {
      return uploadForm.value.flowId && 
             selectedFiles.value.length > 0
    })

    const canSearch = computed(() => {
      return searchForm.value.flowId.trim() !== ''
    })

    // 允許的檔案類型
    const allowedFileTypes = [
      'text/csv',
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'application/pdf',
      'text/markdown',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain'
    ]

    // 檢查檔案類型是否允許
    const isFileTypeAllowed = (file) => {
      return allowedFileTypes.includes(file.type)
    }

    // 處理檔案選擇
    const handleFileChange = (event) => {
      const files = Array.from(event.target.files)
      
      // 檢查是否有不支援的檔案類型
      const hasInvalidFile = files.some(file => !isFileTypeAllowed(file))
      
      if (hasInvalidFile) {
        Swal.fire({
          icon: 'error',
          title: '不支援的檔案類型',
          text: '請上傳支援的檔案類型：CSV、Excel、PDF、Markdown、Word、Text',
          timer: 3000
        })
        event.target.value = ''
        return
      }
      
      selectedFiles.value.push(...files)
      event.target.value = ''
    }

    // 移除已選檔案
    const removeFile = (index) => {
      selectedFiles.value.splice(index, 1)
    }

    // 批次移除所有已選檔案
    const removeAllFiles = async () => {
      try {
        const result = await Swal.fire({
          title: '確定要移除所有已選檔案嗎？',
          text: '此操作將清空已選擇的檔案列表',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: '確定',
          cancelButtonText: '取消'
        })

        if (result.isConfirmed) {
          selectedFiles.value = []
          Swal.fire({
            icon: 'success',
            title: '已清空檔案列表',
            timer: 1500,
            showConfirmButton: false
          })
        }
      } catch (error) {
        console.error('批次移除失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '批次移除失敗'
        })
      }
    }

    // 上傳檔案
    const uploadFiles = async () => {
      try {
        for (const file of selectedFiles.value) {
          const formData = new FormData()
          formData.append('file', file)
          formData.append('flow_id', uploadForm.value.flowId)

          await knowledgeAPI.uploadFile(uploadForm.value.flowId, formData)
          await logOperation(`【知識庫】上傳檔案 ${file.name}`, '上傳')
        }

        // 重置表單
        uploadForm.value = { flowId: '' }
        selectedFiles.value = []
        
        Swal.fire({
          icon: 'success',
          title: '上傳成功',
          timer: 1500,
          showConfirmButton: false
        })
      } catch (error) {
        console.error('上傳檔案失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '上傳檔案失敗'
        })
      }
    }

    // 獲取檔案列表
    const fetchFiles = async () => {
      try {
        const response = await knowledgeAPI.listFiles()
        files.value = response.data.files || []
      } catch (error) {
        console.error('獲取檔案列表失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '獲取檔案列表失敗'
        })
      }
    }

    // 處理查詢
    const handleSearch = async () => {
      try {
        // 檢查是否有輸入 flow_id
        if (!searchForm.value.flowId) {
          Swal.fire({
            icon: 'warning',
            title: '請輸入知識庫流程ID',
            timer: 1500,
            showConfirmButton: false
          })
          return
        }

        // 呼叫 API 列出檔案
        const response = await knowledgeAPI.listFiles(searchForm.value.flowId)
        
        // 更新搜尋結果
        searchResults.value = response.data.files || []
        hasSearched.value = true
        
        // 如果沒有檔案，顯示提示
        if (searchResults.value.length === 0) {
          Swal.fire({
            icon: 'info',
            title: '沒有找到檔案',
            timer: 1500,
            showConfirmButton: false
          })
        }

      } catch (error) {
        console.error('搜尋檔案失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '搜尋失敗',
          text: error.response?.data?.message || '請稍後再試'
        })
      }
    }

    // 下載檔案
    const downloadFile = async (flowId, fileName) => {
      try {
        const response = await knowledgeAPI.downloadFile(flowId, fileName)
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', fileName)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        await logOperation(`【知識庫】下載檔案 ${fileName}`, '下載')
      } catch (error) {
        console.error('下載檔案失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '下載檔案失敗'
        })
      }
    }

    // 刪除檔案
    const deleteFile = async (flowId, fileName) => {
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
          await knowledgeAPI.deleteFile(flowId, fileName)
          await logOperation(`【知識庫】刪除檔案 ${fileName}`, '刪除')
          await handleSearch()
          
          Swal.fire({
            icon: 'success',
            title: '刪除成功',
            timer: 1500,
            showConfirmButton: false
          })
        }
      } catch (error) {
        console.error('刪除檔案失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '刪除檔案失敗'
        })
      }
    }

    // 格式化檔案大小
    const formatFileSize = (bytes) => {
      if (!bytes) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
    }

    // 獲取檔案圖標
    const getFileIcon = (fileName) => {
      const ext = fileName.split('.').pop().toLowerCase()
      const icons = {
        pdf: 'fas fa-file-pdf',
        doc: 'fas fa-file-word',
        docx: 'fas fa-file-word',
        xls: 'fas fa-file-excel',
        xlsx: 'fas fa-file-excel',
        txt: 'fas fa-file-alt',
        jpg: 'fas fa-file-image',
        jpeg: 'fas fa-file-image',
        png: 'fas fa-file-image',
        gif: 'fas fa-file-image'
      }
      return icons[ext] || 'fas fa-file'
    }

    // 測試用假資料
    const mockFiles = [
      {
        id: 1,
        name: 'document.pdf',
        size: 1024576,
        uploadTime: '2024-03-13 14:30:00'
      },
      {
        id: 2,
        name: 'data.xlsx',
        size: 2048576,
        uploadTime: '2024-03-13 15:45:00'
      }
    ]

    // 處理檔案拖放
    const handleFileDrop = (event) => {
      isDragging.value = false
      const files = Array.from(event.dataTransfer.files)
      
      // 檢查是否有不支援的檔案類型
      const hasInvalidFile = files.some(file => !isFileTypeAllowed(file))
      
      if (hasInvalidFile) {
        dragError.value = true
        Swal.fire({
          icon: 'error',
          title: '不支援的檔案類型',
          text: '請上傳支援的檔案類型：CSV、Excel、PDF、Markdown、Word、Text',
          timer: 3000
        })
        return
      }
      
      selectedFiles.value.push(...files)
      dragError.value = false
    }

    // 檢查檔案是否被選中
    const isFileSelected = (file) => {
      return selectedFiles.value.includes(file)
    }

    // 切換檔案選中狀態
    const toggleFileSelection = (file) => {
      const index = selectedFiles.value.indexOf(file)
      if (index === -1) {
        selectedFiles.value.push(file)
      } else {
        selectedFiles.value.splice(index, 1)
      }
    }

    // 批次刪除檔案
    const batchDeleteFiles = async () => {
      try {
        const result = await Swal.fire({
          title: '確定要刪除選中的檔案嗎？',
          text: `將會刪除 ${selectedFiles.value.length} 個檔案，此操作無法復原`,
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: '確定',
          cancelButtonText: '取消'
        })

        if (result.isConfirmed) {
          await Promise.all(selectedFiles.value.map(fileName => 
            knowledgeAPI.deleteFile(searchForm.value.flowId, fileName)
          ))
          
          await logOperation(`【知識庫】批次刪除檔案：${selectedFiles.value.join(', ')}`, '刪除')
          selectedFiles.value = []
          await handleSearch()

          Swal.fire({
            icon: 'success',
            title: '批次刪除成功',
            timer: 1500,
            showConfirmButton: false
          })
        }
      } catch (error) {
        console.error('批次刪除失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '批次刪除失敗'
        })
      }
    }

    // 批次下載功能
    const batchDownloadFiles = async () => {
      try {
        // 顯示進度提示
        const toast = Swal.mixin({
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000,
          timerProgressBar: true
        })

        toast.fire({
          icon: 'info',
          title: '正在準備下載...'
        })

        // 呼叫批次下載 API
        const response = await knowledgeAPI.batchDownload(
          searchForm.value.flowId,
          selectedFiles.value
        )
        
        // 建立下載連結
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `knowledge_files_${new Date().getTime()}.zip`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        // 記錄下載操作
        await logOperation(`【知識庫】批次下載檔案：${selectedFiles.value.join(', ')}`, '下載')

        // 下載完成提示
        toast.fire({
          icon: 'success',
          title: '檔案打包下載完成'
        })

        // 清空選中的檔案
        selectedFiles.value = []
      } catch (error) {
        console.error('批次下載失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '批次下載失敗',
          text: error.response?.data?.message || '請稍後再試'
        })
      }
    }

    // 處理拖曳進入
    const handleDragOver = () => {
      isDragging.value = true
      dragError.value = false
    }

    // 處理拖曳離開
    const handleDragLeave = () => {
      isDragging.value = false
      dragError.value = false
    }

    // 計算是否全部選中
    const isAllSelected = computed(() => {
      return searchResults.value.length > 0 && 
             searchResults.value.every(file => selectedFiles.value.includes(file))
    })

    // 切換全選狀態
    const toggleSelectAll = () => {
      if (isAllSelected.value) {
        // 如果當前是全選狀態，則清空選擇
        selectedFiles.value = []
      } else {
        // 如果當前不是全選狀態，則選擇所有檔案
        selectedFiles.value = [...searchResults.value]
      }
    }

    onMounted(async () => {
      await logOperation('【知識庫】訪問知識庫管理頁面', '查看')
    })

    return {
      currentTab,
      tabs,
      uploadForm,
      selectedFiles,
      fileInput,
      files,
      columns,
      canUpload,
      handleFileChange,
      removeFile,
      uploadFiles,
      fetchFiles,
      downloadFile,
      deleteFile,
      formatFileSize,
      getFileIcon,
      searchForm,
      hasSearched,
      searchResults,
      canSearch,
      handleSearch,
      handleFileDrop,
      isFileSelected,
      toggleFileSelection,
      batchDeleteFiles,
      removeAllFiles,
      viewMode,
      batchDownloadFiles,
      searchViewMode,
      isDragging,
      dragError,
      handleDragOver,
      handleDragLeave,
      isAllSelected,
      toggleSelectAll
    }
  }
}
</script>

<style scoped>
.required-field::after {
  content: '*';
  @apply text-red-500 ml-1;
}

/* 美化滾動條 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 美化卡片陰影 */
.shadow-sm {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* 玻璃擬態效果 */
.backdrop-blur-sm {
  backdrop-filter: blur(8px);
}

/* 添加微妙的動畫效果 */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* 美化按鈕懸停效果 */
button:not(:disabled):hover {
  transform: translateY(-1px);
}

/* 改進輸入框樣式 */
input, textarea {
  transition: all 0.2s ease;
}

input:focus, textarea:focus {
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

/* 添加卡片hover效果 */
.rounded-xl {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.rounded-xl:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
</style> 