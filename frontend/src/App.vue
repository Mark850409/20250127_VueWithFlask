<template>
  <div class="min-h-screen">
    <!-- 主要內容區域 -->
    <div v-if="showGitHelper" class="min-h-screen bg-git-dark text-gray-200">
      <nav class="bg-git-light border-b border-gray-700 px-4 py-3">
        <div class="container mx-auto flex justify-between items-center">
          <h1 class="text-2xl font-bold text-blue-400">Git 小助手</h1>
          <div class="flex space-x-2">
            <button @click="toggleView" 
                    class="btn btn-primary">
              返回美食推薦
            </button>
            <button @click="showConfigModal = true" class="btn btn-primary">
              配置 Git
            </button>
          </div>
        </div>
      </nav>

      <main class="container mx-auto px-4 py-6">
        <!-- 倉庫操作區域 -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- 初始化倉庫 -->
          <div class="card">
            <h2 class="text-xl font-semibold mb-4 text-blue-400">倉庫初始化</h2>
            <div class="space-y-4">
              <input 
                v-model="repoPath"
                class="input-field"
                placeholder="請輸入倉庫路徑"
              >
              <button @click="initRepo" class="btn btn-primary w-full">
                初始化倉庫
              </button>
            </div>
          </div>

          <!-- Git 操作面板 -->
          <div class="card">
            <h2 class="text-xl font-semibold mb-4 text-blue-400">Git 操作</h2>
            <div class="space-y-3">
              <button @click="checkStatus" class="btn btn-primary w-full">
                查看狀態
              </button>
              <button @click="addFiles" class="btn btn-success w-full">
                添加文件
              </button>
              <button @click="commit" class="btn btn-warning w-full">
                提交更改
              </button>
              <button @click="showBranchModal = true" class="btn btn-primary w-full">
                分支操作
              </button>
              <button @click="showRemoteModal = true" class="btn btn-primary w-full">
                配置遠程倉庫
              </button>
              <button @click="pushToRemote" class="btn btn-success w-full">
                推送到遠程
              </button>
              <button @click="pullFromRemote" class="btn btn-primary w-full">
                拉取遠程更新
              </button>
              <button @click="showCommitHistoryModal = true" class="btn btn-primary w-full">
                查看提交歷史
              </button>
            </div>
          </div>

          <!-- 狀態輸出 -->
          <div class="card md:col-span-2 lg:col-span-1">
            <h2 class="text-xl font-semibold mb-4 text-blue-400">狀態與輸出</h2>
            <div class="output-container">
              <pre class="output-content" v-html="formattedOutput"></pre>
            </div>
          </div>
        </div>
      </main>

      <!-- 分支操作模態框 -->
      <div v-if="showBranchModal" 
           class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="card w-96">
          <h3 class="text-xl font-semibold mb-4 text-blue-400">分支操作</h3>
          <input 
            v-model="branchName"
            class="input-field mb-4"
            placeholder="分支名稱"
          >
          <div class="flex space-x-3">
            <button @click="createBranch" class="btn btn-success flex-1">
              創建分支
            </button>
            <button @click="switchBranch" class="btn btn-primary flex-1">
              切換分支
            </button>
            <button @click="showBranchModal = false" class="btn btn-danger">
              關閉
            </button>
          </div>
        </div>
      </div>

      <!-- Git 配置模態框 -->
      <div v-if="showConfigModal" 
           class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="card w-96">
          <h3 class="text-xl font-semibold mb-4 text-blue-400">Git 配置</h3>
          <input 
            v-model="gitConfig.name"
            class="input-field mb-3"
            placeholder="用戶名"
          >
          <input 
            v-model="gitConfig.email"
            class="input-field mb-4"
            placeholder="郵箱"
          >
          <div class="flex space-x-3">
            <button @click="saveConfig" class="btn btn-success flex-1">
              保存
            </button>
            <button @click="showConfigModal = false" class="btn btn-danger">
              關閉
            </button>
          </div>
        </div>
      </div>

      <!-- 添加遠程倉庫模態框 -->
      <div v-if="showRemoteModal" 
           class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="card w-96">
          <h3 class="text-xl font-semibold mb-4 text-blue-400">配置遠程倉庫</h3>
          <input 
            v-model="remoteConfig.name"
            class="input-field mb-3"
            placeholder="遠程倉庫名稱 (預設: origin)"
          >
          <input 
            v-model="remoteConfig.url"
            class="input-field mb-4"
            placeholder="遠程倉庫URL"
          >
          <div class="flex space-x-3">
            <button @click="addRemote" class="btn btn-success flex-1">
              添加
            </button>
            <button @click="showRemoteModal = false" class="btn btn-danger">
              關閉
            </button>
          </div>
        </div>
      </div>

      <!-- 添加提交歷史模態框 -->
      <div v-if="showCommitHistoryModal" 
           class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="card commit-history-modal max-h-[80vh] overflow-hidden flex flex-col">
          <h3 class="text-xl font-semibold mb-4 text-blue-400">提交歷史</h3>
          <div class="overflow-auto flex-1">
            <table class="w-full text-left border-separate border-spacing-0">
              <thead class="bg-gray-700">
                <tr>
                  <th class="sticky top-0 z-10 bg-gray-700 p-3 whitespace-nowrap w-24">提交哈希</th>
                  <th class="sticky top-0 z-10 bg-gray-700 p-3 whitespace-nowrap w-[50%]">提交信息</th>
                  <th class="sticky top-0 z-10 bg-gray-700 p-3 whitespace-nowrap w-40">作者</th>
                  <th class="sticky top-0 z-10 bg-gray-700 p-3 whitespace-nowrap w-32">日期</th>
                  <th class="sticky top-0 z-10 bg-gray-700 p-3 whitespace-nowrap w-24">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="commit in commits" :key="commit.hash" 
                    class="hover:bg-gray-700/50 transition-colors">
                  <td class="p-3 font-mono whitespace-nowrap text-sm">{{ commit.hash }}</td>
                  <td class="p-3 min-w-[400px]">
                    <div class="commit-message">
                      <div class="commit-message-title">
                        {{ commit.message.split('\n')[0] }}
                      </div>
                      <div v-if="commit.message.includes('\n')" class="commit-message-body">
                        {{ commit.message.split('\n').slice(1).join('\n') }}
                      </div>
                    </div>
                  </td>
                  <td class="p-3 whitespace-nowrap text-sm">{{ commit.author }}</td>
                  <td class="p-3 whitespace-nowrap text-sm">{{ commit.date }}</td>
                  <td class="p-3 whitespace-nowrap space-x-2 text-center">
                    <button @click="resetToCommit(commit.hash)" 
                            class="p-2 rounded-full hover:bg-red-600 transition-colors"
                            title="回退到此版本">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="mt-4 flex justify-end">
            <button @click="showCommitHistoryModal = false" class="btn btn-danger">
              關閉
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 點餐推薦系統 -->
    <div v-else>
      <nav class="bg-white/80 backdrop-blur-md shadow-lg fixed w-full z-50 transition-all duration-300">
        <div class="container mx-auto px-4">
          <div class="flex justify-between items-center h-16">
            <div class="flex items-center space-x-2">
              <img src="@/assets/food/food-logo.png" alt="Logo" class="w-8 h-8 object-contain">
              <span class="text-xl font-bold bg-gradient-to-r from-red-500 to-orange-500 
                           bg-clip-text text-transparent">美食推薦</span>
            </div>
            <div class="flex items-center space-x-4">
              <a href="#home" class="nav-link">首頁</a>
              <a href="#recommend" class="nav-link">推薦</a>
              <a href="#about" class="nav-link">關於我們</a>
              <button @click="toggleView" 
                      class="ml-4 px-4 py-2 bg-gradient-to-r from-blue-500 to-blue-600 
                             text-white rounded-lg hover:from-blue-600 hover:to-blue-700 
                             transition-all duration-300 transform hover:scale-105 
                             shadow-md hover:shadow-lg">
                Git 小助手
              </button>
            </div>
          </div>
        </div>
      </nav>

      <FoodRecommendation />
    </div>
  </div>
</template>

<script>
import Swal from 'sweetalert2'
import FoodRecommendation from './components/food/FoodRecommendation.vue'

export default {
  name: 'App',
  components: {
    FoodRecommendation
  },
  data() {
    return {
      repoPath: '',
      output: '',
      showBranchModal: false,
      showConfigModal: false,
      showRemoteModal: false,
      branchName: '',
      gitConfig: {
        name: '',
        email: ''
      },
      remoteConfig: {
        name: '',
        url: ''
      },
      showCommitHistoryModal: false,
      commits: [],
      showGitHelper: false
    }
  },
  methods: {
    toggleView() {
      this.showGitHelper = !this.showGitHelper;
      // 如果切換到 Git 小助手，滾動到頂部
      if (this.showGitHelper) {
        window.scrollTo(0, 0);
      }
    },
    async initRepo() {
      try {
        const response = await fetch('http://localhost:5000/init', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ path: this.repoPath })
        });
        const data = await response.json();
        this.output = data.message;
      } catch (error) {
        this.output = `錯誤: ${error.message}`;
      }
    },
    async checkStatus() {
      try {
        const response = await fetch('http://localhost:5000/status');
        const data = await response.json();
        this.output = data.message;
      } catch (error) {
        this.output = `錯誤: ${error.message}`;
      }
    },
    async addFiles() {
      try {
        const response = await fetch('http://localhost:5000/add', {
          method: 'POST'
        });
        const data = await response.json();
        this.output = data.message;
      } catch (error) {
        this.output = `錯誤: ${error.message}`;
      }
    },
    async commit() {
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
      });

      if (!result.isConfirmed) return;
      const message = result.value;
      
      try {
        const response = await fetch('http://localhost:5000/commit', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message })
        });
        const data = await response.json();
        this.output = data.message;
        await Swal.fire({
          icon: 'success',
          title: '提交成功',
          timer: 1500,
          showConfirmButton: false
        });
      } catch (error) {
        await Swal.fire({
          icon: 'error',
          title: '提交失敗',
          text: error.message
        });
      }
    },
    async createBranch() {
      try {
        const response = await fetch('http://localhost:5000/branch/create', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name: this.branchName })
        });
        const data = await response.json();
        this.output = data.message;
        this.showBranchModal = false;
      } catch (error) {
        this.output = `錯誤: ${error.message}`;
      }
    },
    async switchBranch() {
      try {
        const response = await fetch('http://localhost:5000/branch/switch', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name: this.branchName })
        });
        const data = await response.json();
        this.output = data.message;
        this.showBranchModal = false;
      } catch (error) {
        this.output = `錯誤: ${error.message}`;
      }
    },
    async saveConfig() {
      try {
        const response = await fetch('http://localhost:5000/config', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.gitConfig)
        });
        const data = await response.json();
        this.output = data.message;
        this.showConfigModal = false;
      } catch (error) {
        this.output = `錯誤: ${error.message}`;
      }
    },
    async addRemote() {
      try {
        const response = await fetch('http://localhost:5000/remote/add', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.remoteConfig)
        });
        const data = await response.json();
        this.output = data.message;
        this.showRemoteModal = false;
      } catch (error) {
        this.output = `錯誤: ${error.message}`;
      }
    },
    async pushToRemote() {
      try {
        const response = await fetch('http://localhost:5000/push', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            remote: this.remoteConfig.name || 'origin',
            branch: 'master'
          })
        });
        const data = await response.json();
        
        if (response.status === 409) {
          const result = await Swal.fire({
            icon: 'warning',
            title: '版本不同步',
            text: '遠程倉庫有新的更新，需要先拉取最新代碼',
            showCancelButton: true,
            confirmButtonText: '拉取更新',
            cancelButtonText: '取消'
          });
          
          if (result.isConfirmed) {
            await this.pullFromRemote();
          }
          return;
        }
        
        if (!response.ok) {
          throw new Error(data.message);
        }
        
        await Swal.fire({
          icon: 'success',
          title: '推送成功',
          text: data.message,
          timer: 1500,
          showConfirmButton: false
        });
      } catch (error) {
        await Swal.fire({
          icon: 'error',
          title: '推送失敗',
          text: error.message
        });
      }
    },
    async pullFromRemote() {
      try {
        const response = await fetch('http://localhost:5000/pull', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            remote: this.remoteConfig.name || 'origin',
            branch: 'master'
          })
        });
        const data = await response.json();
        
        if (response.ok) {
          await Swal.fire({
            icon: 'success',
            title: '拉取成功',
            text: data.message,
            timer: 1500,
            showConfirmButton: false
          });
          await this.checkStatus();
          await this.getCommitHistory();
        } else {
          throw new Error(data.message);
        }
      } catch (error) {
        await Swal.fire({
          icon: 'error',
          title: '拉取失敗',
          text: error.message,
          showConfirmButton: true
        });
      }
    },
    async getCommitHistory() {
      try {
        const response = await fetch('http://localhost:5000/commits');
        const data = await response.json();
        if (data.commits) {
          this.commits = data.commits;
        } else {
          this.output = data.message;
        }
      } catch (error) {
        this.output = `錯誤: ${error.message}`;
      }
    },
    async resetToCommit(hash) {
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
      });

      if (!result.isConfirmed) return;
      
      try {
        const response = await fetch('http://localhost:5000/reset', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ hash })
        });
        const data = await response.json();
        this.output = data.message;
        this.showCommitHistoryModal = false;
        // 重新獲取狀態
        await this.checkStatus();
        await Swal.fire({
          icon: 'success',
          title: '回退成功',
          text: '已恢復到選定的版本狀態',
          timer: 1500,
          showConfirmButton: false
        });
      } catch (error) {
        await Swal.fire({
          icon: 'error',
          title: '回退失敗',
          text: error.message
        });
      }
    }
  },
  watch: {
    showCommitHistoryModal(newVal) {
      if (newVal) {
        this.getCommitHistory();
      }
    }
  },
  computed: {
    formattedOutput() {
      if (!this.output) {
        return '<span class="text-gray-500">等待操作...</span>';
      }
      
      // 將git status的輸出進行格式化
      return this.output
        .split('\n')
        .map(line => {
          if (line.includes('modified:')) {
            return line.replace('modified:', '<span class="text-yellow-400">modified:</span>');
          }
          if (line.includes('new file:')) {
            return line.replace('new file:', '<span class="text-green-400">new file:</span>');
          }
          if (line.includes('deleted:')) {
            return line.replace('deleted:', '<span class="text-red-400">deleted:</span>');
          }
          if (line.includes('On branch')) {
            return line.replace('On branch', '<span class="text-blue-400">On branch</span>');
          }
          if (line.includes('Changes to be committed:')) {
            return '<span class="text-green-400">' + line + '</span>';
          }
          if (line.includes('Changes not staged for commit:')) {
            return '<span class="text-yellow-400">' + line + '</span>';
          }
          if (line.includes('Untracked files:')) {
            return '<span class="text-gray-400">' + line + '</span>';
          }
          return line;
        })
        .join('\n');
    }
  }
}
</script> 