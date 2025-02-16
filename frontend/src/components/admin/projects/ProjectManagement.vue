<template>
  <div class="space-y-6">
    <!-- 頂部工具列 -->
    <div class="flex justify-between items-center gap-4">
      <!-- 搜尋框 -->
      <div class="relative w-64">
        <input 
          type="text" 
          v-model="searchQuery"
          placeholder="搜尋專案..."
          class="w-full px-4 py-2 pl-10 bg-white dark:bg-gray-800 border dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
        <i class="fas fa-search absolute left-3 top-3 text-gray-400"></i>
      </div>
      
      <!-- 視圖切換 -->
      <div class="flex items-center bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
        <button 
          @click="viewMode = 'card'"
          :class="[
            'px-3 py-1 rounded-md transition-all duration-200',
            viewMode === 'card' 
              ? 'bg-white dark:bg-gray-600 text-blue-600 dark:text-blue-400 shadow-sm' 
              : 'text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400'
          ]"
        >
          <i class="fas fa-th-large mr-2"></i>卡片
        </button>
        <button 
          @click="viewMode = 'list'"
          :class="[
            'px-3 py-1 rounded-md transition-all duration-200',
            viewMode === 'list' 
              ? 'bg-white dark:bg-gray-600 text-blue-600 dark:text-blue-400 shadow-sm' 
              : 'text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400'
          ]"
        >
          <i class="fas fa-list mr-2"></i>列表
        </button>
      </div>
      
      <!-- 新增按鈕 -->
      <button 
        @click="showAddModal = true"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transform hover:scale-105 transition-all duration-200"
      >
        <i class="fas fa-plus mr-2"></i>新增專案
      </button>
    </div>

    <!-- 無資料時顯示 -->
    <div v-if="!filteredProjects.length" 
         class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-8 text-center">
      <div class="text-gray-500 dark:text-gray-400 mb-4">
        <i class="fas fa-project-diagram text-4xl"></i>
      </div>
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
        尚無專案資料
      </h3>
      <p class="text-gray-500 dark:text-gray-400 mb-4">
        目前還沒有任何專案，點擊上方按鈕新增專案。
      </p>
    </div>

    <!-- 專案列表 -->
    <transition-group 
      name="project-list" 
      tag="div" 
      :class="[
        viewMode === 'card' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6' : 'space-y-3'
      ]"
    >
      <div v-for="project in filteredProjects" 
           :key="project.id"
           :class="[
             'bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden group cursor-pointer',
             viewMode === 'list' ? 'flex items-center px-6 py-4' : ''
           ]"
      >
        <!-- 卡片/列表內容 -->
        <div 
          :class="[
            'flex flex-col h-full',
            viewMode === 'card' ? 'p-6' : 'flex-1'
          ]"
        >
          <!-- 列表視圖 -->
          <template v-if="viewMode === 'list'">
            <div class="flex items-center justify-between flex-1 relative" @click="showProjectDetail(project.id)">
              <div class="flex items-center space-x-4 flex-1">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white min-w-[200px]">
                  {{ project.name }}
                </h3>
                <p class="text-gray-600 dark:text-gray-400 flex-1 line-clamp-1">
                  {{ project.description }}
                </p>
              </div>
              <div class="flex items-center space-x-4 ml-4 relative">
                <span class="text-sm text-gray-500 dark:text-gray-400 font-mono text-left min-w-[300px]">
                  <i class="fas fa-fingerprint mr-1"></i>
                  {{ project.id }}
                </span>
                <!-- 操作選單 -->
                <div class="relative menu-container" @click.stop>
                  <button @click="toggleMenu(project.id)" 
                          class="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 rounded-full
                                 hover:bg-gray-100 dark:hover:bg-gray-700">
                    <i class="fas fa-ellipsis-v"></i>
                  </button>
                  <!-- 下拉選單 -->
                  <div v-if="activeMenu === project.id"
                       class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-700 rounded-lg shadow-lg 
                              animate__animated animate__fadeIn animate__faster"
                       style="z-index: 9999; position: fixed;">
                    <div class="py-1">
                      <button @click="editProject(project)"
                              class="w-full px-4 py-2 text-left text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600">
                        <i class="fas fa-edit mr-2"></i>編輯
                      </button>
                      <button @click="deleteProject(project)"
                              class="w-full px-4 py-2 text-left text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-600">
                        <i class="fas fa-trash-alt mr-2"></i>刪除
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>

          <!-- 卡片視圖 -->
          <template v-else>
            <!-- 標題和操作選單 -->
            <div class="flex justify-between items-start mb-4">
              <div class="flex-1 cursor-pointer" @click="showProjectDetail(project.id)">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white truncate">
                  {{ project.name }}
                </h3>
              </div>
              <!-- 操作選單 -->
              <div class="relative menu-container" @click.stop>
                <button @click="toggleMenu(project.id)" 
                        class="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 rounded-full">
                  <i class="fas fa-ellipsis-v"></i>
                </button>
                <!-- 下拉選單 -->
                <div v-if="activeMenu === project.id"
                     class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-700 rounded-lg shadow-lg z-10 
                            animate__animated animate__fadeIn animate__faster">
                  <div class="py-1">
                    <button @click="editProject(project)"
                            class="w-full px-4 py-2 text-left text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600">
                      <i class="fas fa-edit mr-2"></i>編輯
                    </button>
                    <button @click="deleteProject(project)"
                            class="w-full px-4 py-2 text-left text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-600">
                      <i class="fas fa-trash-alt mr-2"></i>刪除
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 描述和其他資訊 -->
            <div class="flex-1 cursor-pointer" @click="showProjectDetail(project.id)">
              <p class="text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
                {{ project.description }}
              </p>
              
              <div class="flex justify-start items-center text-sm text-gray-500 dark:text-gray-400 mt-2">
                <span class="font-mono">
                  <i class="fas fa-fingerprint mr-1"></i>
                  {{ project.id }}
                </span>
              </div>
            </div>
          </template>
        </div>
      </div>
    </transition-group>

    <!-- 新增/編輯專案彈窗 -->
    <div v-if="showAddModal" 
         class="fixed inset-0 flex items-center justify-center z-50">
      <!-- 背景遮罩 -->
      <div class="absolute inset-0 bg-black bg-opacity-50 -mt-[64px]"></div>
      <!-- Modal 內容 -->
      <div class="bg-white dark:bg-gray-800 rounded-xl p-8 w-full max-w-md m-4 
                  animate__animated animate__fadeInUp animate__faster relative z-10">
        <h2 class="text-xl font-bold mb-6 text-gray-900 dark:text-white">
          {{ editingProject ? '編輯專案' : '新增專案' }}
        </h2>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">專案名稱</label>
            <input type="text" 
                   v-model="projectForm.name" 
                   :class="{'border-red-500': errors.name}"
                   class="w-full px-4 py-2 border dark:border-gray-600 rounded-lg 
                          focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white">
            <span v-if="errors.name" class="text-red-500 text-xs mt-1">{{ errors.name }}</span>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">描述</label>
            <textarea v-model="projectForm.description" 
                      :class="{'border-red-500': errors.description}"
                      class="w-full px-4 py-2 border dark:border-gray-600 rounded-lg 
                             focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                      rows="4"></textarea>
            <span v-if="errors.description" class="text-red-500 text-xs mt-1">{{ errors.description }}</span>
          </div>
        </div>

        <div class="mt-8 flex justify-end space-x-4">
          <button @click="closeModal" 
                  class="px-4 py-2 text-gray-700 dark:text-gray-300 border dark:border-gray-600 rounded-lg 
                         hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
            取消
          </button>
          <button @click="saveProject" 
                  class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 
                         transform hover:scale-105 transition-all duration-200">
            確認
          </button>
        </div>
      </div>
    </div>

    <!-- 專案詳情彈窗 -->
    <div v-if="showDetailModal" 
         class="fixed inset-0 flex items-center justify-center z-50">
      <!-- 背景遮罩 -->
      <div class="absolute inset-0 bg-black bg-opacity-50 -mt-[64px]"></div>
      <!-- Modal 內容 -->
      <div class="bg-white dark:bg-gray-800 rounded-xl p-8 w-full max-w-4xl m-4 
                  animate__animated animate__fadeInUp animate__faster relative
                  max-h-[calc(100vh-2rem)] overflow-y-auto z-10">
        <div class="flex justify-between items-start mb-6">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">專案詳情</h2>
          <button @click="closeDetailModal" 
                  class="p-2 text-gray-500 hover:text-gray-700 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <div v-if="projectDetail" class="space-y-6">
          <!-- 標題區塊 -->
          <div class="border-b dark:border-gray-700 pb-6">
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white">
              {{ projectDetail.name }}
            </h3>
            <p class="mt-2 text-gray-600 dark:text-gray-400">
              {{ projectDetail.description }}
            </p>
          </div>

          <!-- 基本資訊區塊 -->
          <div class="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-750 
                      rounded-xl p-6 border border-blue-100 dark:border-gray-700 shadow-sm">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <i class="fas fa-info-circle mr-3 text-blue-500 text-xl"></i>
              <span>基本資訊</span>
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
              <div class="space-y-2">
                <p class="text-sm font-medium text-gray-500 dark:text-gray-400">專案 ID</p>
                <p class="text-gray-900 dark:text-white bg-white dark:bg-gray-700 px-4 py-2 rounded-lg font-mono text-sm">
                  {{ projectDetail.id }}
                </p>
              </div>
              <div class="space-y-2">
                <p class="text-sm font-medium text-gray-500 dark:text-gray-400">建立時間</p>
                <p class="text-gray-900 dark:text-white bg-white dark:bg-gray-700 px-4 py-2 rounded-lg">
                  {{ formatDate(projectDetail.updated_at) }}
                </p>
              </div>
            </div>
          </div>

          <!-- 流程資訊區塊 -->
          <div class="bg-gradient-to-br from-green-50 to-emerald-50 dark:from-gray-800 dark:to-gray-750 
                      rounded-xl p-6 border border-green-100 dark:border-gray-700 shadow-sm">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <i class="fas fa-project-diagram mr-3 text-green-500 text-xl"></i>
              <span>流程資訊</span>
            </h3>
            <div v-if="projectDetail.flows && projectDetail.flows.length > 0">
              <div v-for="flow in projectDetail.flows" :key="flow.id" 
                   class="bg-white dark:bg-gray-700 rounded-lg p-4 mb-4 border border-green-100 dark:border-gray-600
                          hover:shadow-md transition-shadow duration-200">
                <div class="flex justify-between items-start">
                  <div>
                    <h4 class="font-medium text-gray-900 dark:text-white flex items-center">
                      <i class="fas fa-code-branch mr-2 text-green-500"></i>
                      {{ flow.name }}
                    </h4>
                    <p class="text-sm text-gray-500 dark:text-gray-400">{{ flow.description }}</p>
                  </div>
                  <span class="text-xs bg-green-100 dark:bg-gray-600 text-green-800 dark:text-green-300 
                               px-3 py-1 rounded-full font-mono">
                    ID: {{ flow.id }}
                  </span>
                </div>
              </div>
            </div>
            <div v-else class="text-center text-gray-500 dark:text-gray-400 py-4">
              尚無流程資料
            </div>
          </div>
        </div>

        <div v-else class="flex justify-center items-center h-32">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { projectAPI } from '@/api'
import { useLogger } from '@/composables/useLogger'
import Swal from 'sweetalert2'
import dayjs from 'dayjs'

export default {
  name: 'ProjectManagement',
  
  setup() {
    const { logOperation } = useLogger()
    const projects = ref([])
    const showAddModal = ref(false)
    const editingProject = ref(null)
    const errors = ref({})
    const searchQuery = ref('')
    const activeMenu = ref(null)
    const showDetailModal = ref(false)
    const projectDetail = ref(null)
    const viewMode = ref('card')

    const projectForm = ref({
      name: '',
      description: '',
    })

    // 篩選專案
    const filteredProjects = computed(() => {
      const query = searchQuery.value.toLowerCase()
      return projects.value.filter(project => 
        project.name.toLowerCase().includes(query) ||
        project.description.toLowerCase().includes(query)
      )
    })

    // 獲取專案列表
    const fetchProjects = async () => {
      try {
        const response = await projectAPI.getProjects()
        console.log('response.data:', response.data)
        projects.value = response.data
      } catch (error) {
        console.error('獲取專案列表失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '獲取專案列表失敗'
        })
      }
    }

    // 切換選單
    const toggleMenu = (projectId) => {
      console.log('toggleMenu called with:', projectId)  // 添加日誌
      activeMenu.value = activeMenu.value === projectId ? null : projectId
    }

    // 點擊外部關閉選單
    const handleClickOutside = (event) => {
      if (activeMenu.value && !event.target.closest('.menu-container')) {
        activeMenu.value = null
      }
    }

    // 編輯專案
    const editProject = (project) => {
      editingProject.value = project
      projectForm.value = {
        name: project.name,
        description: project.description,
      }
      showAddModal.value = true
      activeMenu.value = null
    }

    // 刪除專案
    const deleteProject = async (project) => {
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
          await projectAPI.deleteProject(project.id)
          await fetchProjects()
          await logOperation(`【專案管理】刪除專案 ${project.name}`, '刪除')
          
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

    // 儲存專案
    const saveProject = async () => {
      try {
        errors.value = {}
        if (!projectForm.value.name?.trim()) {
          errors.value.name = '請輸入專案名稱'
          return
        }
        if (!projectForm.value.description?.trim()) {
          errors.value.description = '請輸入描述'
          return
        }

        if (editingProject.value) {
          await projectAPI.updateProject(editingProject.value.id, projectForm.value)
          await logOperation(`【專案管理】編輯專案 ${projectForm.value.name}`, '修改')
        } else {
          await projectAPI.createProject(projectForm.value)
          await logOperation(`【專案管理】新增專案 ${projectForm.value.name}`, '新增')
        }

        await fetchProjects()
        showAddModal.value = false
        
        Swal.fire({
          icon: 'success',
          title: '成功',
          text: `${editingProject.value ? '更新' : '新增'}成功！`,
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
      editingProject.value = null
      projectForm.value = {
        name: '',
        description: '',
      }
      errors.value = {}
    }

    const formatDate = (date) => {
      return dayjs(date).format('YYYY/MM/DD HH:mm')
    }

    // 顯示專案詳情
    const showProjectDetail = async (projectId) => {
      try {
        showDetailModal.value = true
        const response = await projectAPI.getProject(projectId)
        console.log('response.data:', response.data)
        projectDetail.value = response.data
      } catch (error) {
        console.error('獲取專案詳情失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '錯誤',
          text: '獲取專案詳情失敗'
        })
      }
    }

    // 關閉詳情彈窗
    const closeDetailModal = () => {
      showDetailModal.value = false
      projectDetail.value = null
    }

    onMounted(async () => {
      await fetchProjects()
      await logOperation('【專案管理】訪問專案管理頁面', '查看')
      document.addEventListener('click', handleClickOutside)
    })

    onBeforeUnmount(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    return {
      projects,
      filteredProjects,
      showAddModal,
      editingProject,
      projectForm,
      errors,
      searchQuery,
      activeMenu,
      editProject,
      deleteProject,
      saveProject,
      closeModal,
      toggleMenu,
      formatDate,
      showDetailModal,
      projectDetail,
      showProjectDetail,
      closeDetailModal,
      viewMode
    }
  }
}
</script>

<style scoped>
/* 專案卡片動畫 */
.project-list-enter-active,
.project-list-leave-active {
  transition: all 0.5s ease;
}
.project-list-enter-from,
.project-list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
.project-list-move {
  transition: transform 0.5s ease;
}

/* 模態框動畫 */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(10px);
}

/* 文字省略 */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 滾動條美化 */
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: rgba(203, 213, 225, 0.5) transparent;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(203, 213, 225, 0.5);
  border-radius: 3px;
}
</style> 