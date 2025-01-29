<template>
  <div>
    <!-- 點餐推薦系統 -->
    <div class="min-h-screen bg-gray-50">
      <!-- 使用共用 Navbar -->
      <Navbar />
      
      <!-- 主要內容區域 -->
      <div class="flex">
        <!-- 左側 Git 操作側邊欄 -->
        <div v-if="showGitHelper" 
             class="w-80 bg-gray-900 text-gray-100 h-[calc(100vh-64px)] fixed left-0 top-16 
                    border-r border-gray-700 overflow-y-auto">
          <div class="p-6 space-y-6">
            <!-- 倉庫初始化 -->
            <div class="space-y-3">
              <h3 class="text-lg font-semibold text-gray-300 flex items-center space-x-2">
                <i class="fas fa-folder-plus text-blue-400"></i>
                <span>倉庫初始化</span>
              </h3>
              <input v-model="repoPath" 
                     type="text" 
                     placeholder="輸入倉庫路徑" 
                     class="w-full px-4 py-2 bg-gray-800 border border-gray-600 rounded-lg 
                            focus:border-blue-500 focus:ring-1 focus:ring-blue-500">
              <button @click="initRepo" 
                      class="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg 
                             transition-colors duration-200">
                初始化倉庫
              </button>
            </div>

            <!-- Git 基本操作 -->
            <div class="space-y-3">
              <h3 class="text-lg font-semibold text-gray-300 flex items-center space-x-2">
                <i class="fas fa-code text-green-400"></i>
                <span>基本操作</span>
              </h3>
              <div class="space-y-2">
                <button @click="checkStatus" 
                        class="w-full py-2 px-4 bg-gray-800 hover:bg-gray-700 rounded-lg 
                               flex items-center space-x-2 transition-colors duration-200">
                  <i class="fas fa-info-circle text-blue-400"></i>
                  <span>查看狀態</span>
                </button>
                <button @click="addFiles" 
                        class="w-full py-2 px-4 bg-gray-800 hover:bg-gray-700 rounded-lg 
                               flex items-center space-x-2 transition-colors duration-200">
                  <i class="fas fa-plus text-green-400"></i>
                  <span>添加文件</span>
                </button>
                <button @click="commit" 
                        class="w-full py-2 px-4 bg-gray-800 hover:bg-gray-700 rounded-lg 
                               flex items-center space-x-2 transition-colors duration-200">
                  <i class="fas fa-save text-yellow-400"></i>
                  <span>提交更改</span>
                </button>
              </div>
            </div>

            <!-- Git 進階操作 -->
            <div class="space-y-3">
              <h3 class="text-lg font-semibold text-gray-300 flex items-center space-x-2">
                <i class="fas fa-tools text-purple-400"></i>
                <span>進階操作</span>
              </h3>
              <div class="space-y-2">
                <button @click="showBranchModal = true" 
                        class="w-full py-2 px-4 bg-gray-800 hover:bg-gray-700 rounded-lg 
                               flex items-center space-x-2 transition-colors duration-200">
                  <i class="fas fa-code-branch text-purple-400"></i>
                  <span>分支操作</span>
                </button>
                <button @click="showRemoteModal = true" 
                        class="w-full py-2 px-4 bg-gray-800 hover:bg-gray-700 rounded-lg 
                               flex items-center space-x-2 transition-colors duration-200">
                  <i class="fas fa-cloud text-indigo-400"></i>
                  <span>遠程倉庫</span>
                </button>
                <button @click="showCommitHistory" 
                        class="w-full py-2 px-4 bg-gray-800 hover:bg-gray-700 rounded-lg 
                               flex items-center space-x-2 transition-colors duration-200">
                  <i class="fas fa-history text-blue-400"></i>
                  <span>提交歷史</span>
                </button>
              </div>
            </div>

            <!-- Git 輸出區域 -->
            <div class="space-y-3">
              <h3 class="text-lg font-semibold text-gray-300 flex items-center space-x-2">
                <i class="fas fa-terminal text-gray-400"></i>
                <span>輸出信息</span>
              </h3>
              <div class="bg-gray-800 rounded-lg p-4 min-h-[200px] font-mono text-sm">
                <pre v-html="formattedOutput" class="whitespace-pre-wrap"></pre>
              </div>
            </div>
          </div>
        </div>

        <!-- 主要內容區域 -->
        <div :class="{ 'ml-80': showGitHelper }" class="flex-1 transition-all duration-300">
          <router-view></router-view>
        </div>
      </div>

      <!-- 添加共用 Footer -->
      <Footer />

      <!-- Git 小助手開關按鈕 -->
      <button @click="toggleGitHelper" 
              class="fixed bottom-6 left-6 bg-gradient-to-r from-blue-600 to-indigo-600 
                     text-white p-4 rounded-full shadow-lg hover:from-blue-700 hover:to-indigo-700 
                     transition-all duration-200 flex items-center justify-center z-50 
                     transform hover:scale-110">
        <i class="fas fa-code-branch text-xl"></i>
      </button>

      <!-- 分支操作 Modal -->
      <div v-if="showBranchModal" 
           class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-gray-900 text-white rounded-xl shadow-lg w-full max-w-md p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-bold">分支操作</h3>
            <button @click="showBranchModal = false" class="text-gray-400 hover:text-white">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">分支名稱</label>
              <input v-model="branchName" 
                     type="text" 
                     placeholder="輸入新分支名稱"
                     class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg">
            </div>
            <div class="flex space-x-3">
              <button @click="createBranch" 
                      class="flex-1 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg">
                創建分支
              </button>
              <button @click="switchBranch" 
                      class="flex-1 py-2 bg-green-600 hover:bg-green-700 rounded-lg">
                切換分支
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 遠程倉庫 Modal -->
      <div v-if="showRemoteModal" 
           class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-gray-900 text-white rounded-xl shadow-lg w-full max-w-md p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-bold">遠程倉庫設置</h3>
            <button @click="showRemoteModal = false" class="text-gray-400 hover:text-white">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">遠程名稱</label>
              <input v-model="remoteConfig.name" 
                     type="text" 
                     placeholder="例如：origin"
                     class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg">
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">遠程 URL</label>
              <input v-model="remoteConfig.url" 
                     type="text" 
                     placeholder="例如：https://github.com/user/repo.git"
                     class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg">
            </div>
            <div class="flex space-x-3">
              <button @click="addRemote" 
                      class="flex-1 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg">
                添加遠程
              </button>
              <button @click="pushToRemote" 
                      class="flex-1 py-2 bg-green-600 hover:bg-green-700 rounded-lg">
                推送到遠程
              </button>
              <button @click="pullFromRemote" 
                      class="flex-1 py-2 bg-yellow-600 hover:bg-yellow-700 rounded-lg">
                拉取更新
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 提交歷史 Modal -->
      <div v-if="showCommitHistoryModal" 
           class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-gray-900 text-white rounded-xl shadow-lg w-full max-w-4xl p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-bold">提交歷史</h3>
            <button @click="showCommitHistoryModal = false" class="text-gray-400 hover:text-white">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="overflow-auto max-h-[60vh]">
            <table class="w-full">
              <thead class="bg-gray-800">
                <tr>
                  <th class="px-4 py-2 text-left w-20">提交 Hash</th>
                  <th class="px-4 py-2 text-left w-40">作者</th>
                  <th class="px-4 py-2 text-left w-36">日期</th>
                  <th class="px-4 py-2 text-left min-w-[400px]">提交信息</th>
                  <th class="px-4 py-2 text-center w-12">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="commit in commits" 
                    :key="commit.hash" 
                    class="border-t border-gray-800 hover:bg-gray-800">
                  <td class="px-4 py-2 font-mono whitespace-nowrap">{{ commit.hash.slice(0, 7) }}</td>
                  <td class="px-4 py-2 whitespace-nowrap">{{ commit.author }}</td>
                  <td class="px-4 py-2 whitespace-nowrap">{{ new Date(commit.date).toLocaleString() }}</td>
                  <td class="px-4 py-2">
                    <div class="whitespace-pre-line">
                      {{ commit.message.split(':')[0] }}:
                      {{ commit.message.split(':').slice(1).join(':') }}
                    </div>
                  </td>
                  <td class="px-4 py-2 text-center">
                    <button @click="resetToCommit(commit.hash)" 
                            class="text-red-400 hover:text-red-300 transition-colors duration-200"
                            title="回退到此版本">
                      <i class="fas fa-history"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './components/common/Navbar.vue'
import Footer from './components/common/Footer.vue'
import { ref } from 'vue'
import Swal from 'sweetalert2'

export default {
  name: 'App',
  components: {
    Navbar,
    Footer
  },
  setup() {
    const showGitHelper = ref(false)
    const repoPath = ref('')
    const output = ref('')
    const showBranchModal = ref(false)
    const showConfigModal = ref(false)
    const showRemoteModal = ref(false)
    const branchName = ref('')
    const gitConfig = ref({
      name: '',
      email: ''
    })
    const remoteConfig = ref({
      name: '',
      url: ''
    })
    const showCommitHistoryModal = ref(false)
    const commits = ref([])

    const toggleGitHelper = () => {
      showGitHelper.value = !showGitHelper.value
      if (showGitHelper.value) {
        window.scrollTo(0, 0)
      }
    }

    const initRepo = async () => {
      try {
        const response = await fetch('http://localhost:5000/init', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ path: repoPath.value })
        })
        const data = await response.json()
        output.value = data.message
      } catch (error) {
        output.value = `錯誤: ${error.message}`
      }
    }

    const checkStatus = async () => {
      try {
        const response = await fetch('http://localhost:5000/status')
        const data = await response.json()
        output.value = data.message
      } catch (error) {
        output.value = `錯誤: ${error.message}`
      }
    }

    const addFiles = async () => {
      try {
        const response = await fetch('http://localhost:5000/add', {
          method: 'POST'
        })
        const data = await response.json()
        output.value = data.message
      } catch (error) {
        output.value = `錯誤: ${error.message}`
      }
    }

    const commit = async () => {
      const result = await Swal.fire({
        title: '提交更改',
        input: 'textarea',
        inputLabel: '提交信息',
        inputPlaceholder: 'feat: 新功能描述\n\n功能的詳細說明...',
        inputAttributes: {
          'aria-label': '提交信息',
          'style': 'height: 150px; font-family: monospace;'
        },
        customClass: {
          input: 'commit-message-textarea'
        },
        showCancelButton: true,
        confirmButtonText: '提交',
        cancelButtonText: '取消',
        inputValidator: (value) => {
          if (!value) {
            return '請輸入提交信息！'
          }
        }
      })

      if (!result.isConfirmed) return
      const message = result.value
      
      try {
        const response = await fetch('http://localhost:5000/commit', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message })
        })
        const data = await response.json()
        output.value = data.message
        await Swal.fire({
          icon: 'success',
          title: '提交成功',
          timer: 1500,
          showConfirmButton: false
        })
      } catch (error) {
        await Swal.fire({
          icon: 'error',
          title: '提交失敗',
          text: error.message
        })
      }
    }

    const createBranch = async () => {
      try {
        const response = await fetch('http://localhost:5000/branch/create', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name: branchName.value })
        })
        const data = await response.json()
        output.value = data.message
        showBranchModal.value = false
      } catch (error) {
        output.value = `錯誤: ${error.message}`
      }
    }

    const switchBranch = async () => {
      try {
        const response = await fetch('http://localhost:5000/branch/switch', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name: branchName.value })
        })
        const data = await response.json()
        output.value = data.message
        showBranchModal.value = false
      } catch (error) {
        output.value = `錯誤: ${error.message}`
      }
    }

    const saveConfig = async () => {
      try {
        const response = await fetch('http://localhost:5000/config', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(gitConfig.value)
        })
        const data = await response.json()
        output.value = data.message
        showConfigModal.value = false
      } catch (error) {
        output.value = `錯誤: ${error.message}`
      }
    }

    const addRemote = async () => {
      try {
        const response = await fetch('http://localhost:5000/remote/add', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(remoteConfig.value)
        })
        const data = await response.json()
        output.value = data.message
        showRemoteModal.value = false
        
        await getCommitHistory()
        
        await Swal.fire({
          icon: 'success',
          title: '遠程倉庫添加成功',
          text: '已成功添加遠程倉庫並獲取提交歷史',
          timer: 1500,
          showConfirmButton: false
        })
      } catch (error) {
        output.value = `錯誤: ${error.message}`
        await Swal.fire({
          icon: 'error',
          title: '添加遠程倉庫失敗',
          text: error.message
        })
      }
    }

    const pushToRemote = async () => {
      try {
        const response = await fetch('http://localhost:5000/push', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            remote: remoteConfig.value.name || 'origin',
            branch: 'master'
          })
        })
        const data = await response.json()
        
        if (response.status === 409) {
          const result = await Swal.fire({
            icon: 'warning',
            title: '版本不同步',
            text: '遠程倉庫有新的更新，需要先拉取最新代碼',
            showCancelButton: true,
            confirmButtonText: '拉取更新',
            cancelButtonText: '取消'
          })
          
          if (result.isConfirmed) {
            await pullFromRemote()
          }
          return
        }
        
        if (!response.ok) {
          throw new Error(data.message)
        }
        
        await Swal.fire({
          icon: 'success',
          title: '推送成功',
          text: data.message,
          timer: 1500,
          showConfirmButton: false
        })
      } catch (error) {
        await Swal.fire({
          icon: 'error',
          title: '推送失敗',
          text: error.message
        })
      }
    }

    const pullFromRemote = async () => {
      try {
        const response = await fetch('http://localhost:5000/pull', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            remote: remoteConfig.value.name || 'origin',
            branch: 'master'
          })
        })
        const data = await response.json()
        
        if (response.ok) {
          await Swal.fire({
            icon: 'success',
            title: '拉取成功',
            text: data.message,
            timer: 1500,
            showConfirmButton: false
          })
          await checkStatus()
          await getCommitHistory()
        } else {
          throw new Error(data.message)
        }
      } catch (error) {
        await Swal.fire({
          icon: 'error',
          title: '拉取失敗',
          text: error.message,
          showConfirmButton: true
        })
      }
    }

    const getCommitHistory = async () => {
      try {
        const response = await fetch('http://localhost:5000/commits')
        const data = await response.json()
        if (data.commits) {
          commits.value = data.commits
        } else {
          output.value = data.message
        }
      } catch (error) {
        output.value = `錯誤: ${error.message}`
      }
    }

    const resetToCommit = async (hash) => {
      const result = await Swal.fire({
        title: '確認回退版本',
        html: `
          <div class="text-left">
            <p class="mb-2">此操作將會：</p>
            <ul class="list-disc pl-5 space-y-1">
              <li>丟失該版本之後的所有提交記錄</li>
              <li>刪除所有未追蹤的文件</li>
              <li>將工作目錄恢復到該版本的狀態</li>
            </ul>
            <p class="mt-4 text-red-400">此操作無法撤銷，確定要繼續嗎？</p>
          </div>
        `,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: '是的，回退！',
        cancelButtonText: '取消'
      })

      if (!result.isConfirmed) return
      
      try {
        const response = await fetch('http://localhost:5000/reset', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ hash })
        })
        const data = await response.json()
        output.value = data.message
        showCommitHistoryModal.value = false
        await checkStatus()
        await Swal.fire({
          icon: 'success',
          title: '回退成功',
          text: '已恢復到選定的版本狀態',
          timer: 1500,
          showConfirmButton: false
        })
      } catch (error) {
        await Swal.fire({
          icon: 'error',
          title: '回退失敗',
          text: error.message
        })
      }
    }

    const showCommitHistory = async () => {
      try {
        await getCommitHistory()
        showCommitHistoryModal.value = true
      } catch (error) {
        await Swal.fire({
          icon: 'error',
          title: '獲取提交歷史失敗',
          text: error.message
        })
      }
    }

    return {
      showGitHelper,
      repoPath,
      output,
      showBranchModal,
      showConfigModal,
      showRemoteModal,
      branchName,
      gitConfig,
      remoteConfig,
      showCommitHistoryModal,
      commits,
      toggleGitHelper,
      initRepo,
      checkStatus,
      addFiles,
      commit,
      createBranch,
      switchBranch,
      saveConfig,
      addRemote,
      pushToRemote,
      pullFromRemote,
      getCommitHistory,
      resetToCommit,
      showCommitHistory
    }
  },
  computed: {
    formattedOutput() {
      if (!this.output) {
        return '<span class="text-gray-500">等待操作...</span>'
      }
      
      return this.output
        .split('\n')
        .map(line => {
          if (line.includes('modified:')) {
            return line.replace('modified:', '<span class="text-yellow-400">modified:</span>')
          }
          if (line.includes('new file:')) {
            return line.replace('new file:', '<span class="text-green-400">new file:</span>')
          }
          if (line.includes('deleted:')) {
            return line.replace('deleted:', '<span class="text-red-400">deleted:</span>')
          }
          if (line.includes('On branch')) {
            return line.replace('On branch', '<span class="text-blue-400">On branch</span>')
          }
          if (line.includes('Changes to be committed:')) {
            return '<span class="text-green-400">' + line + '</span>'
          }
          if (line.includes('Changes not staged for commit:')) {
            return '<span class="text-yellow-400">' + line + '</span>'
          }
          if (line.includes('Untracked files:')) {
            return '<span class="text-gray-400">' + line + '</span>'
          }
          return line
        })
        .join('\n')
    }
  }
}
</script>

<style>
/* 頁面切換動畫 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 其他樣式... */
</style> 