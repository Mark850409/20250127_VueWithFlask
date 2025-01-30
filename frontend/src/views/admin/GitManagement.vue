<template>
  <div class="space-y-6">
    <!-- Git 倉庫狀態 -->
    <div v-if="isRepoConfigured" class="bg-white rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold mb-4">倉庫狀態</h2>
      <div class="space-y-4">
        <div class="flex flex-col space-y-4">
          <div class="flex items-center space-x-4">
            <button @click="checkStatus" 
                    class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
              <i class="fas fa-sync-alt mr-2"></i>檢查狀態
            </button>
            <span class="text-gray-500 text-sm">
              <i class="fas fa-info-circle mr-1"></i>
              當前分支：<span class="font-semibold">{{ currentBranch }}</span>
            </span>
          </div>

          <div v-if="status" class="w-full">
            <!-- 未追蹤的文件 -->
            <div v-if="parsedStatus.untracked.length" class="mb-4">
              <h3 class="text-sm font-semibold text-gray-600 mb-2">
                <i class="fas fa-question-circle text-yellow-500 mr-2"></i>未追蹤的文件
              </h3>
              <div class="bg-yellow-50 rounded-lg p-4 border border-yellow-100">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
                  <div v-for="file in parsedStatus.untracked" :key="file" 
                       class="flex items-center text-sm text-gray-600 bg-white px-3 py-2 rounded">
                    <i class="fas fa-file mr-2 text-yellow-500"></i>
                    <span class="truncate">{{ file }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 已修改的文件 -->
            <div v-if="parsedStatus.modified.length" class="mb-4">
              <h3 class="text-sm font-semibold text-gray-600 mb-2">
                <i class="fas fa-edit text-blue-500 mr-2"></i>已修改的文件
              </h3>
              <div class="bg-blue-50 rounded-lg p-4 border border-blue-100">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
                  <div v-for="file in parsedStatus.modified" :key="file" 
                       class="flex items-center text-sm text-gray-600 bg-white px-3 py-2 rounded">
                    <i class="fas fa-pencil-alt mr-2 text-blue-500"></i>
                    <span class="truncate">{{ file }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Git 配置 -->
    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold mb-4">Git 配置</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700">
            用戶名稱 <span class="text-red-500">*</span>
          </label>
          <input v-model="config.name" type="text" 
                 class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                 :class="{ 'border-red-500': showConfigError && !config.name }">
          <p v-if="showConfigError && !config.name" class="text-red-500 text-xs mt-1">
            請輸入用戶名稱
          </p>
        </div>
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700">
            電子郵件 <span class="text-red-500">*</span>
          </label>
          <input v-model="config.email" type="email" 
                 class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                 :class="{ 'border-red-500': showConfigError && !config.email }">
          <p v-if="showConfigError && !config.email" class="text-red-500 text-xs mt-1">
            請輸入電子郵件
          </p>
        </div>
      </div>
      <button @click="configureGit" 
              class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
        保存配置
      </button>
    </div>

    <!-- 遠程倉庫配置 -->
    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold mb-4">遠程倉庫配置</h2>
      <div class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">
              遠程名稱 <span class="text-red-500">*</span>
            </label>
            <input v-model="remote.name" type="text" 
                   class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                   :class="{ 'border-red-500': showRemoteError && !remote.name }">
            <p v-if="showRemoteError && !remote.name" class="text-red-500 text-xs mt-1">
              請輸入遠程名稱
            </p>
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">
              遠程 URL <span class="text-red-500">*</span>
            </label>
            <input v-model="remote.url" type="text" 
                   class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                   :class="{ 'border-red-500': showRemoteError && !remote.url }">
            <p v-if="showRemoteError && !remote.url" class="text-red-500 text-xs mt-1">
              請輸入遠程 URL
            </p>
          </div>
        </div>
        <button @click="addRemote" 
                class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
          添加遠程倉庫
        </button>
      </div>
    </div>

    <!-- 其他 Git 操作區塊，只在配置完成後顯示 -->
    <template v-if="isRepoConfigured">
      <!-- 提交操作 -->
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-4">提交操作</h2>
        <div class="space-y-4">
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">
              提交信息 <span class="text-red-500">*</span>
            </label>
            <textarea v-model="commitMessage" 
                      class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                      :class="{ 'border-red-500': showCommitError && !commitMessage }"
                      rows="3"></textarea>
            <p v-if="showCommitError && !commitMessage" class="text-red-500 text-xs mt-1">
              請輸入提交信息
            </p>
          </div>
          <div class="flex space-x-4">
            <button @click="addFiles" 
                    class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition">
              <i class="fas fa-plus mr-2"></i>添加文件
            </button>
            <button @click="commit" 
                    class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
              <i class="fas fa-check mr-2"></i>提交更改
            </button>
          </div>
        </div>
      </div>

      <!-- 分支管理 -->
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-4">分支管理</h2>
        <div class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">
                分支名稱 <span class="text-red-500">*</span>
              </label>
              <input v-model="branchName" type="text" 
                     class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                     :class="{ 'border-red-500': showBranchError && !branchName }">
              <p v-if="showBranchError && !branchName" class="text-red-500 text-xs mt-1">
                請輸入分支名稱
              </p>
            </div>
          </div>
          <div class="flex space-x-4">
            <button @click="createBranch" 
                    class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition">
              <i class="fas fa-code-branch mr-2"></i>創建分支
            </button>
            <button @click="switchBranch" 
                    class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
              <i class="fas fa-exchange-alt mr-2"></i>切換分支
            </button>
          </div>
        </div>
      </div>

      <!-- 推送與拉取 -->
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-4">推送與拉取</h2>
        <div class="flex space-x-4">
          <button @click="pull" 
                  class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
            <i class="fas fa-download mr-2"></i>拉取更新
          </button>
          <button @click="push" 
                  class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition">
            <i class="fas fa-upload mr-2"></i>推送更改
          </button>
          <button @click="forcePush" 
                  class="px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition">
            <i class="fas fa-exclamation-triangle mr-2"></i>強制推送
          </button>
        </div>
      </div>

      <!-- 提交歷史 -->
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-4">提交歷史</h2>
        <div class="space-y-4">
          <!-- 工具列 -->
          <div class="flex justify-between items-center">
            <div class="flex items-center space-x-4">
              <button @click="getHistory" 
                      class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
                <i class="fas fa-history mr-2"></i>刷新歷史
              </button>
              <!-- 搜尋框 -->
              <div class="relative">
                <input v-model="searchQuery"
                       type="text"
                       placeholder="搜尋提交..."
                       class="pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
                <i class="fas fa-search absolute left-3 top-3 text-gray-400"></i>
              </div>
            </div>
            <!-- 每頁顯示筆數 -->
            <div class="flex items-center space-x-2">
              <span class="text-sm text-gray-600">每頁顯示：</span>
              <select v-model="pageSize" 
                      class="border rounded-lg pl-3 pr-8 py-1 focus:ring-2 focus:ring-blue-500 appearance-none bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTMgNWg2TDYgOXoiIGZpbGw9IiM2QjcyODAiLz48L3N2Zz4=')] bg-no-repeat bg-right-1 pr-8">
                <option :value="10">10</option>
                <option :value="20">20</option>
                <option :value="50">50</option>
                <option :value="100">100</option>
              </select>
            </div>
          </div>

          <div class="overflow-x-auto">
            <table v-if="filteredCommits.length" class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th @click="sortBy('hash')" 
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase cursor-pointer hover:bg-gray-100">
                    提交哈希
                    <i :class="getSortIcon('hash')" class="ml-1"></i>
                  </th>
                  <th @click="sortBy('author')" 
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase cursor-pointer hover:bg-gray-100">
                    作者
                    <i :class="getSortIcon('author')" class="ml-1"></i>
                  </th>
                  <th @click="sortBy('date')" 
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase cursor-pointer hover:bg-gray-100">
                    日期
                    <i :class="getSortIcon('date')" class="ml-1"></i>
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">操作</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="commit in paginatedCommits" :key="commit.hash">
                  <td class="px-6 py-4 whitespace-nowrap font-mono text-sm">{{ commit.hash.substring(0, 7) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm">{{ commit.author }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm">{{ commit.date }}</td>
                  <td class="px-6 py-4 text-sm">
                    <div class="flex space-x-2">
                      <button @click="resetToCommit(commit.hash)" 
                              class="text-blue-600 hover:text-blue-800 tooltip"
                              data-tooltip="回退到此版本">
                        <i class="fas fa-history"></i>
                      </button>
                      <button @click="viewCommitDetails(commit)" 
                              class="text-gray-600 hover:text-gray-800 tooltip"
                              data-tooltip="查看詳情">
                        <i class="fas fa-eye"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-else class="text-center text-gray-500 py-4">
              {{ searchQuery ? '沒有符合搜尋條件的提交記錄' : '暫無提交記錄' }}
            </div>
          </div>

          <!-- 分頁控制 -->
          <div v-if="filteredCommits.length" class="flex justify-between items-center mt-4">
            <div class="text-sm text-gray-600">
              顯示 {{ startIndex + 1 }} 到 {{ endIndex }} 筆，共 {{ filteredCommits.length }} 筆
            </div>
            <div class="flex space-x-2">
              <button @click="currentPage--" 
                      :disabled="currentPage === 1"
                      class="px-3 py-1 border rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed">
                上一頁
              </button>
              <button v-for="page in totalPages" 
                      :key="page"
                      @click="currentPage = page"
                      :class="['px-3 py-1 border rounded-lg hover:bg-gray-100', 
                               currentPage === page ? 'bg-blue-500 text-white hover:bg-blue-600' : '']">
                {{ page }}
              </button>
              <button @click="currentPage++" 
                      :disabled="currentPage === totalPages"
                      class="px-3 py-1 border rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed">
                下一頁
              </button>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- 未配置時的提示 -->
    <div v-else class="bg-white rounded-lg shadow p-6">
      <div class="text-center text-gray-500 py-4">
        請先完成 Git 配置並添加遠程倉庫以啟用所有功能
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/utils/axios'
import { ElMessage } from 'element-plus'
import Swal from 'sweetalert2'

export default {
  name: 'GitManagement',
  data() {
    return {
      status: '',
      config: {
        name: '',
        email: ''
      },
      remote: {
        name: 'origin',
        url: ''
      },
      commitMessage: '',
      branchName: '',
      commits: [],
      isRepoConfigured: false,
      showConfigError: false,
      showRemoteError: false,
      showCommitError: false,
      showBranchError: false,
      repoPath: 'D:/AI_project/20250127_VueWithFlask',  // 添加倉庫路徑
      currentBranch: 'master',  // 添加當前分支狀態
      parsedStatus: {
        untracked: [],
        modified: []
      },
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      sortKey: 'date',
      sortOrder: 'desc'
    }
  },
  computed: {
    filteredCommits() {
      let result = [...this.commits]
      
      // 搜尋過濾
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(commit => 
          commit.hash.toLowerCase().includes(query) ||
          commit.author.toLowerCase().includes(query) ||
          commit.date.toLowerCase().includes(query)
        )
      }
      
      // 排序
      result.sort((a, b) => {
        let aVal = a[this.sortKey]
        let bVal = b[this.sortKey]
        
        if (this.sortKey === 'date') {
          aVal = new Date(aVal)
          bVal = new Date(bVal)
        }
        
        if (this.sortOrder === 'asc') {
          return aVal > bVal ? 1 : -1
        } else {
          return aVal < bVal ? 1 : -1
        }
      })
      
      return result
    },
    paginatedCommits() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredCommits.slice(start, end)
    },
    totalPages() {
      return Math.ceil(this.filteredCommits.length / this.pageSize)
    },
    startIndex() {
      return (this.currentPage - 1) * this.pageSize
    },
    endIndex() {
      return Math.min(this.startIndex + this.pageSize, this.filteredCommits.length)
    }
  },
  methods: {
    async initRepo() {
      try {
        await axios.post('/init', { path: this.repoPath })
        Swal.fire({
          icon: 'success',
          title: '倉庫初始化成功',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
      } catch (error) {
        // 錯誤處理已在 axios 攔截器中完成
      }
    },

    async configureGit() {
      this.showConfigError = true
      if (!this.config.name || !this.config.email) {
        return
      }

      try {
        await axios.post('/config', this.config)
        Swal.fire({
          icon: 'success',
          title: 'Git 配置已更新',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
        this.showConfigError = false
      } catch (error) {
        // 錯誤處理已在 axios 攔截器中完成
      }
    },

    async addRemote() {
      this.showRemoteError = true
      if (!this.remote.name || !this.remote.url) {
        return
      }

      try {
        await axios.post('/remote/add', this.remote)
        Swal.fire({
          icon: 'success',
          title: '遠程倉庫已添加',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
        this.isRepoConfigured = true
        this.showRemoteError = false
        this.checkStatus()
      } catch (error) {
        this.isRepoConfigured = false
      }
    },

    async checkStatus() {
      try {
        const response = await axios.get('/status')
        this.status = response.data.message
        console.log('Git status:', this.status)
        this.parsedStatus = this.parseGitStatus(this.status)
        console.log('Parsed status:', this.parsedStatus)
        Swal.fire({
          icon: 'success',
          title: '成功獲取倉庫狀態',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
      } catch (error) {
        // 錯誤處理已在 axios 攔截器中完成
      }
    },

    async addFiles() {
      try {
        await axios.post('/add')
        Swal.fire({
          icon: 'success',
          title: '文件已添加到暫存區',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
      } catch (error) {
        // 錯誤處理已在 axios 攔截器中完成
      }
    },

    async commit() {
      this.showCommitError = true
      if (!this.commitMessage) {
        return
      }
      try {
        await axios.post('/commit', { message: this.commitMessage })
        this.commitMessage = ''
        this.showCommitError = false
        Swal.fire({
          icon: 'success',
          title: '更改已提交',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
        this.getHistory()
      } catch (error) {
        // 錯誤處理已在 axios 攔截器中完成
      }
    },

    async createBranch() {
      this.showBranchError = true
      if (!this.branchName) return
      try {
        await axios.post('/branch/create', { name: this.branchName })
        this.branchName = ''
        this.showBranchError = false
      } catch (error) {
        // 錯誤處理已在 axios 攔截器中完成
      }
    },

    async switchBranch() {
      this.showBranchError = true
      if (!this.branchName) return
      try {
        await axios.post('/branch/switch', { name: this.branchName })
        this.branchName = ''
        this.showBranchError = false
        await this.checkStatus()
      } catch (error) {
        // 錯誤處理已在 axios 攔截器中完成
      }
    },

    async pull() {
      try {
        // 添加請求頭，指定 Content-Type
        const response = await axios.post('/pull', {}, {
          headers: {
            'Content-Type': 'application/json'
          }
        })
        
        // 更新狀態和歷史
        await this.checkStatus()
        await this.getHistory()
        
        // 成功提示
        Swal.fire({
          icon: 'success',
          title: '已成功拉取更新',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
      } catch (error) {
        // 錯誤處理已在 axios 攔截器中完成
      }
    },

    async push() {
      try {
        const response = await axios.post('/push')
        await this.checkStatus()
        await this.getHistory()
        
        // 添加成功提示
        Swal.fire({
          icon: 'success',
          title: '已成功推送更改',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
      } catch (error) {
        // 錯誤處理已在 axios 攔截器中完成
      }
    },

    async forcePush() {
      // 添加確認提示
      const result = await Swal.fire({
        title: '確認強制推送？',
        html: `
          <div class="text-left">
            <div class="bg-yellow-50 p-4 rounded-lg border border-yellow-100">
              <i class="fas fa-exclamation-triangle text-yellow-500 mr-2"></i>
              <span class="text-sm text-yellow-700">
                強制推送會覆蓋遠程倉庫的更改，可能導致其他協作者的工作丟失。
                <br>請確保您了解此操作的風險。
              </span>
            </div>
          </div>
        `,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: '確認強制推送',
        cancelButtonText: '取消'
      })

      if (result.isConfirmed) {
        try {
          const response = await axios.post('/force-push')
          await this.checkStatus()
          await this.getHistory()
          
          // 添加成功提示
          Swal.fire({
            icon: 'success',
            title: '已成功強制推送',
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000
          })
        } catch (error) {
          // 錯誤處理已在 axios 攔截器中完成
        }
      }
    },

    async getHistory() {
      if (!this.isRepoConfigured) return
      try {
        const response = await axios.get('/commits')
        this.commits = response.data.commits
      } catch (error) {
        // 錯誤處理已在 axios 攔截器中完成
      }
    },

    async resetToCommit(hash) {
      // 添加確認提示視窗
      const result = await Swal.fire({
        title: '確認回退版本？',
        html: `
          <div class="text-left">
            <p class="mb-4 text-gray-600">您即將回退到提交 <span class="font-mono bg-gray-100 px-2 py-1 rounded">${hash.substring(0, 7)}</span></p>
            <div class="bg-yellow-50 p-4 rounded-lg border border-yellow-100">
              <i class="fas fa-exclamation-triangle text-yellow-500 mr-2"></i>
              <span class="text-sm text-yellow-700">
                此操作將會重置當前工作目錄到選定的版本，且無法復原。
                <br>請確保您已經提交或備份了所有重要更改。
              </span>
            </div>
          </div>
        `,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: '確認回退',
        cancelButtonText: '取消',
        customClass: {
          popup: 'rounded-lg shadow-xl',
        }
      })

      // 如果用戶確認，則執行回退操作
      if (result.isConfirmed) {
        try {
          await axios.post('/reset', { hash })
          await this.checkStatus() // 更新倉庫狀態
          await this.getHistory() // 更新提交歷史
          Swal.fire({
            icon: 'success',
            title: '已回退到指定版本',
            text: `成功回退到 ${hash.substring(0, 7)}`,
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000
          })
        } catch (error) {
          // 錯誤處理已在 axios 攔截器中完成
        }
      }
    },

    // 格式化提交信息
    formatCommitMessage(message) {
      // 處理 feat: 和 fix: 開頭的信息
      return message.replace(/(feat:|fix:)(.+?)($|\n)/, (match, prefix, content) => {
        return `${prefix}\n${content.trim()}`
      })
    },

    // 查看提交詳情
    viewCommitDetails(commit) {
      Swal.fire({
        title: '提交詳情',
        html: `
          <div class="text-left">
            <div class="mb-4 p-4 bg-gray-50 rounded-lg">
              <div class="grid grid-cols-1 gap-3">
                <div class="flex items-center">
                  <span class="font-semibold w-24 text-gray-600">提交哈希：</span>
                  <span class="font-mono bg-gray-100 px-2 py-1 rounded">${commit.hash}</span>
                </div>
                <div class="flex items-center">
                  <span class="font-semibold w-24 text-gray-600">作者：</span>
                  <span class="text-gray-800">${commit.author}</span>
                </div>
                <div class="flex items-center">
                  <span class="font-semibold w-24 text-gray-600">日期：</span>
                  <span class="text-gray-800">${commit.date}</span>
                </div>
              </div>
            </div>
            <div class="mb-2 font-semibold text-gray-600">提交信息：</div>
            <pre class="whitespace-pre-line bg-blue-50 p-4 rounded-lg text-gray-800 border border-blue-100 text-sm leading-relaxed">${this.formatCommitMessage(commit.message)}</pre>
          </div>
        `,
        confirmButtonText: '關閉',
        confirmButtonColor: '#3085d6',
        customClass: {
          container: 'commit-details-modal',
          popup: 'rounded-lg shadow-xl',
          header: 'border-b pb-3',
          title: 'text-xl font-semibold text-gray-800',
          content: 'pt-4',
          confirmButton: 'px-6'
        },
        width: '600px'
      })
    },

    // 解析 Git 狀態
    parseGitStatus(status) {
      const lines = status.split('\n')
      const result = {
        untracked: [],
        modified: []
      }

      // 解析當前分支
      const branchMatch = status.match(/On branch (.+)/);
      if (branchMatch) {
        this.$nextTick(() => {
          this.currentBranch = branchMatch[1].trim();
        });
      }

      // 解析未追蹤的文件
      if (status.includes('Untracked files:')) {
        const untrackedSection = status.split('Untracked files:')[1].split(/\n\n|\nChanges/)[0];
        result.untracked = untrackedSection
          .split('\n')
          .map(line => line.trim())
          .filter(line => line && !line.includes('(use "git add'))
          .filter(line => line !== 'to include in what will be committed)')
          .filter(line => line !== '') // 過濾空行
      }

      // 解析已修改的文件（包括工作區和暫存區）
      const modifiedFiles = new Set();

      // 檢查工作區的修改
      if (status.includes('Changes not staged for commit:')) {
        const workingSection = status.split('Changes not staged for commit:')[1].split(/\n\n|\nUntracked/)[0];
        workingSection
          .split('\n')
          .filter(line => line.includes('modified:'))
          .map(line => line.replace('modified:', '').trim())
          .forEach(file => modifiedFiles.add(file));
      }

      // 檢查暫存區的修改
      if (status.includes('Changes to be committed:')) {
        const stagedSection = status.split('Changes to be committed:')[1].split(/\n\n|\nChanges not staged/)[0];
        stagedSection
          .split('\n')
          .filter(line => line.includes('modified:'))
          .map(line => line.replace('modified:', '').trim())
          .forEach(file => modifiedFiles.add(file));
      }

      // 將所有修改過的文件添加到結果中
      result.modified = Array.from(modifiedFiles)
        .filter(file => !file.includes('node_modules')) // 排除 node_modules
        .filter(file => !file.includes('__pycache__')); // 排除 __pycache__

      return result;
    },
    sortBy(key) {
      if (this.sortKey === key) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortKey = key
        this.sortOrder = 'desc'
      }
    },
    getSortIcon(key) {
      if (this.sortKey !== key) return 'fas fa-sort'
      return this.sortOrder === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down'
    }
  },
  watch: {
    // 當搜尋條件或每頁筆數改變時，重置頁碼
    searchQuery() {
      this.currentPage = 1
    },
    pageSize() {
      this.currentPage = 1
    }
  },
  mounted() {
    // 添加初始化倉庫的調用
    this.initRepo()
  }
}
</script>

<style>
/* 提交詳情彈窗樣式 */
.commit-details-modal .swal2-popup {
  padding: 2rem;
}

.commit-details-modal .swal2-html-container {
  margin: 1rem 0 0 0;
  text-align: left;
}

.commit-details-modal pre {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.875rem;
  line-height: 1.6;
}

/* 滾動條美化 */
.commit-details-modal pre::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.commit-details-modal pre::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

.commit-details-modal pre::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

.commit-details-modal pre::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style> 