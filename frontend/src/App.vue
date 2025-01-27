<template>
  <div class="min-h-screen bg-git-dark text-gray-200">
    <nav class="bg-git-light border-b border-gray-700 px-4 py-3">
      <div class="container mx-auto flex justify-between items-center">
        <h1 class="text-2xl font-bold text-blue-400">Git 小助手</h1>
        <div class="flex space-x-2">
          <button @click="showConfigModal = true" class="btn btn-primary">
            配置 Git
          </button>
          <button @click="exit" class="btn btn-danger">
            退出
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
          <pre class="bg-gray-900 p-4 rounded-lg overflow-auto max-h-[300px] text-sm font-mono">
            {{ output || '等待操作...' }}
          </pre>
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
      <div class="card w-[800px] max-h-[80vh] overflow-hidden flex flex-col">
        <h3 class="text-xl font-semibold mb-4 text-blue-400">提交歷史</h3>
        <div class="overflow-auto flex-1">
          <table class="w-full text-left">
            <thead class="bg-gray-700">
              <tr>
                <th class="p-3">提交哈希</th>
                <th class="p-3">提交信息</th>
                <th class="p-3">作者</th>
                <th class="p-3">日期</th>
                <th class="p-3">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="commit in commits" :key="commit.hash" class="border-b border-gray-700">
                <td class="p-3 font-mono">{{ commit.hash }}</td>
                <td class="p-3">{{ commit.message }}</td>
                <td class="p-3">{{ commit.author }}</td>
                <td class="p-3">{{ commit.date }}</td>
                <td class="p-3 space-x-2">
                  <button @click="resetToCommit(commit.hash)" 
                          class="btn btn-danger text-sm">
                    回退到此版本
                  </button>
                  <button @click="deleteCommit(commit.hash)"
                          class="btn btn-warning text-sm">
                    刪除此版本
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
</template>

<script>
import Swal from 'sweetalert2'

export default {
  name: 'App',
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
      commits: []
    }
  },
  methods: {
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
        inputPlaceholder: '請輸入提交信息...',
        inputAttributes: {
          'aria-label': '提交信息'
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
    },
    async deleteCommit(hash) {
      const result = await Swal.fire({
        title: '確認刪除提交',
        html: `
          <div class="text-left">
            <p class="mb-2">警告！此操作將會：</p>
            <ul class="list-disc pl-5 space-y-1">
              <li class="text-red-400">永久刪除該提交記錄</li>
              <li>重寫之後的所有提交歷史</li>
              <li>可能導致與遠程倉庫不同步</li>
            </ul>
            <p class="mt-4 text-red-400 font-bold">此操作無法撤銷且可能破壞倉庫，確定要繼續嗎？</p>
          </div>
        `,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: '是的，刪除！',
        cancelButtonText: '取消',
        input: 'checkbox',
        inputValue: 0,
        inputPlaceholder: '我了解這是危險操作，並已備份重要數據',
        inputValidator: (result) => {
          return new Promise((resolve) => {
            if (result) {
              resolve()
            } else {
              resolve('請確認您了解操作風險')
            }
          })
        }
      });

      if (!result.isConfirmed) return;
      
      try {
        const response = await fetch('http://localhost:5000/commit/delete', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ hash })
        });
        const data = await response.json();
        this.output = data.message;
        this.showCommitHistoryModal = false;
        // 重新獲取提交歷史和狀態
        await this.getCommitHistory();
        await this.checkStatus();
        await Swal.fire({
          icon: 'success',
          title: '刪除成功',
          text: '已刪除指定的提交記錄',
          timer: 1500,
          showConfirmButton: false
        });
      } catch (error) {
        await Swal.fire({
          icon: 'error',
          title: '刪除失敗',
          text: error.message
        });
      }
    },
    exit() {
      window.close();
    }
  },
  watch: {
    showCommitHistoryModal(newVal) {
      if (newVal) {
        this.getCommitHistory();
      }
    }
  }
}
</script> 