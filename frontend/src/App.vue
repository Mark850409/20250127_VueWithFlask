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
  </div>
</template>

<script>
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
      }
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
      const message = prompt('請輸入提交信息：');
      if (!message) return;
      
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
      } catch (error) {
        this.output = `錯誤: ${error.message}`;
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
          method: 'POST'
        });
        const data = await response.json();
        this.output = data.message;
      } catch (error) {
        this.output = `錯誤: ${error.message}`;
      }
    },
    exit() {
      window.close();
    }
  }
}
</script> 