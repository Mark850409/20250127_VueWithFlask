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
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold">Git 配置</h2>
        <button @click="setRepoPath" 
                class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition">
          <i class="fas fa-folder mr-2"></i>設置倉庫路徑
        </button>
      </div>
      <!-- 顯示當前路徑 -->
      <div class="mb-4 p-4 bg-gray-50 rounded-lg">
        <div class="flex items-center text-sm text-gray-600">
          <i class="fas fa-folder-open mr-2"></i>
          <span class="font-medium mr-2">當前倉庫路徑：</span>
          <span class="font-mono">{{ repoPath || '尚未設置' }}</span>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700">
            用戶名稱 <span class="text-red-500">*</span>
          </label>
          <input 
            v-model="config.name" 
            type="text" 
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.config.name }"
            @input="validateConfig"
            @blur="validateConfig"
          >
          <p v-if="validationErrors.config.name" 
             class="text-red-500 text-xs mt-1">
            {{ validationErrors.config.name }}
          </p>
        </div>
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700">
            電子郵件 <span class="text-red-500">*</span>
          </label>
          <input 
            v-model="config.email" 
            type="email" 
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': validationErrors.config.email }"
            @input="validateConfig"
            @blur="validateConfig"
          >
          <p v-if="validationErrors.config.email" 
             class="text-red-500 text-xs mt-1">
            {{ validationErrors.config.email }}
          </p>
        </div>
      </div>
      <button @click="configureGit" 
              class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
              >
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
            <input 
              v-model="remote.name" 
              type="text" 
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              :class="{ 'border-red-500': validationErrors.remote.name }"
              @input="validateRemote"
              @blur="validateRemote"
            >
            <p v-if="validationErrors.remote.name" 
               class="text-red-500 text-xs mt-1">
              {{ validationErrors.remote.name }}
            </p>
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">
              遠程 URL <span class="text-red-500">*</span>
            </label>
            <input 
              v-model="remote.url" 
              type="text" 
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              :class="{ 'border-red-500': validationErrors.remote.url }"
              @input="validateRemote"
              @blur="validateRemote"
            >
            <p v-if="validationErrors.remote.url" 
               class="text-red-500 text-xs mt-1">
              {{ validationErrors.remote.url }}
            </p>
          </div>
        </div>
        <button @click="addRemote" 
                class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
                >
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
            <div class="flex justify-between items-center">
              <label class="block text-sm font-medium text-gray-700">
                提交信息 <span class="text-red-500">*</span>
              </label>
              <button @click="openCommitDialog" 
                      class="text-blue-500 hover:text-blue-600">
                <i class="fas fa-edit"></i> 編輯
              </button>
            </div>
            <!-- 預覽區域 -->
            <div class="w-full px-3 py-2 border rounded-lg bg-gray-50 min-h-[4rem]">
              <p v-if="commitMessage" class="whitespace-pre-line text-gray-700">{{ commitMessage }}</p>
              <p v-else class="text-gray-400 italic">尚未輸入提交信息</p>
            </div>
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
                      <button @click="openCommitDetails(commit)" 
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

    <!-- 提交信息對話框 -->
    <dialog ref="commitDialog" class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 rounded-lg shadow-xl p-0 w-full max-w-2xl">
      <div class="p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-900">輸入提交信息</h3>
          <button @click="closeCommitDialog" class="text-gray-400 hover:text-gray-500">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="space-y-4">
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">提交信息</label>
            <textarea
              v-model="commitMessage"
              rows="6"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 font-mono"
              :class="{ 
                'border-red-500 focus:ring-red-500': commitMessage && !isValidCommitMessage,
                'border-green-500 focus:ring-green-500': commitMessage && isValidCommitMessage
              }"
              placeholder="例如：&#10;feat: 添加新功能&#10;&#10;- 實現了XXX功能&#10;- 優化了YYY流程"
              @input="validateCommitMessage"
            ></textarea>
            <div v-if="commitMessage" 
                 class="text-sm mt-1"
                 :class="{
                   'text-red-500': !isValidCommitMessage,
                   'text-green-500': isValidCommitMessage
                 }"
            >
              <i :class="[
                isValidCommitMessage ? 'fas fa-check-circle' : 'fas fa-exclamation-circle',
                'mr-1'
              ]"></i>
              <span v-if="!isValidCommitMessage">
                提交信息格式不正確，請使用正確的格式：
                <ul class="list-disc ml-5 mt-1">
                  <li>必須以 feat:、fix:、docs:、style:、refactor:、test:、chore: 等開頭</li>
                  <li>冒號後需要空格</li>
                  <li>需要包含具體的更改描述</li>
                </ul>
              </span>
              <span v-else>
                提交信息格式正確
              </span>
            </div>
          </div>
          <div class="flex justify-end space-x-3">
            <button
              @click="closeCommitDialog"
              class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              取消
            </button>
            <button
              @click="confirmCommit"
              class="px-4 py-2 text-white rounded-lg transition-colors"
              :class="{
                'bg-blue-500 hover:bg-blue-600': isValidCommitMessage && commitMessage,
                'bg-gray-400 cursor-not-allowed': !isValidCommitMessage || !commitMessage
              }"
              :disabled="!isValidCommitMessage || !commitMessage"
            >
              確認
            </button>
          </div>
        </div>
      </div>
    </dialog>

    <!-- 倉庫路徑設置對話框 -->
    <dialog ref="repoPathDialog" class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 rounded-lg shadow-xl p-0 w-full max-w-xl">
      <div class="p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-900">設置倉庫路徑</h3>
          <button @click="closeRepoPathDialog" class="text-gray-400 hover:text-gray-500">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="space-y-4">
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">Git 倉庫路徑</label>
            <input
              v-model="tempRepoPath"
              type="text"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              :class="{ 'border-red-500 focus:ring-red-500': !tempRepoPath }"
              placeholder="例如: C:/Projects/my-repo"
            />
            <div v-if="!tempRepoPath" 
                 class="text-red-500 text-sm mt-1">
              <i class="fas fa-exclamation-circle mr-1"></i>
              請輸入倉庫路徑
            </div>
          </div>
          <div class="flex justify-end space-x-3">
            <button
              @click="closeRepoPathDialog"
              class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              取消
            </button>
            <button
              @click="confirmRepoPath"
              class="px-4 py-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600"
              :disabled="!tempRepoPath"
            >
              確認
            </button>
          </div>
        </div>
      </div>
    </dialog>

    <!-- 未添加文件提示對話框 -->
    <dialog ref="unstagedDialog" class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 rounded-lg shadow-xl p-0 w-full max-w-2xl">
      <div class="p-6">
        <div class="flex flex-col">
          <div class="flex items-center mb-4 text-yellow-500">
            <i class="fas fa-exclamation-triangle text-3xl mr-3"></i>
            <h3 class="text-lg font-semibold text-gray-900">發現未添加的文件</h3>
          </div>
          <div class="space-y-4">
            <div class="text-left">
              <p class="mb-2">以下文件尚未添加到暫存區：</p>
              <div class="bg-yellow-50 p-4 rounded-lg border border-yellow-100 max-h-48 overflow-auto">
                <template v-for="file in unstagedFiles" :key="file">
                  <div class="text-sm mb-1">
                    <i class="fas fa-file text-yellow-500 mr-2"></i>{{ file }}
                  </div>
                </template>
              </div>
            </div>
            <p class="text-gray-600">是否要將這些文件添加到暫存區？</p>
            <div class="flex justify-end space-x-3">
              <button @click="handleUnstagedCancel"
                      class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200">
                否，僅提交暫存的更改
              </button>
              <button @click="handleUnstagedConfirm"
                      class="px-4 py-2 text-white bg-yellow-500 rounded-lg hover:bg-yellow-600">
                是，添加文件
              </button>
            </div>
          </div>
        </div>
      </div>
    </dialog>

    <!-- 提示訊息對話框 -->
    <dialog ref="alertDialog" class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 rounded-lg shadow-xl p-0 w-full max-w-md">
      <div class="p-6">
        <div class="flex flex-col items-center">
          <div class="mb-4">
            <i :class="[
              alertType === 'success' ? 'text-green-500 fas fa-check-circle' : '',
              alertType === 'error' ? 'text-red-500 fas fa-exclamation-circle' : '',
              alertType === 'warning' ? 'text-yellow-500 fas fa-exclamation-triangle' : '',
              'text-4xl'
            ]"></i>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ alertTitle }}</h3>
          <p class="text-gray-600 text-center mb-6" v-if="alertMessage">{{ alertMessage }}</p>
          <div class="flex justify-center space-x-3">
            <button v-if="showCancelButton"
                    @click="handleAlertCancel"
                    class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200">
              取消
            </button>
            <button @click="handleAlertConfirm"
                    :class="[
                      'px-4 py-2 text-white rounded-lg',
                      alertType === 'success' ? 'bg-green-500 hover:bg-green-600' : '',
                      alertType === 'error' ? 'bg-red-500 hover:bg-red-600' : '',
                      alertType === 'warning' ? 'bg-yellow-500 hover:bg-yellow-600' : ''
                    ]">
              確認
            </button>
          </div>
        </div>
      </div>
    </dialog>

    <!-- 添加提交詳情對話框 -->
    <dialog ref="commitDetailsDialog" class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 rounded-lg shadow-xl p-0 w-full max-w-2xl">
      <div class="p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-900">提交詳情</h3>
          <button @click="closeCommitDetailsDialog" class="text-gray-400 hover:text-gray-500">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="space-y-4">
          <!-- 基本信息卡片 -->
          <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
            <div class="grid grid-cols-1 gap-3">
              <div class="flex items-center">
                <span class="font-semibold w-24 text-gray-600">提交哈希：</span>
                <code class="font-mono bg-white px-3 py-1 rounded border border-gray-200 text-sm">{{ selectedCommit?.hash }}</code>
              </div>
              <div class="flex items-center">
                <span class="font-semibold w-24 text-gray-600">作者：</span>
                <span class="text-gray-800">{{ selectedCommit?.author }}</span>
              </div>
              <div class="flex items-center">
                <span class="font-semibold w-24 text-gray-600">日期：</span>
                <span class="text-gray-800">{{ selectedCommit?.date }}</span>
              </div>
            </div>
          </div>
          
          <!-- 提交信息 -->
          <div>
            <div class="font-semibold text-gray-700 mb-2">提交信息：</div>
            <pre class="whitespace-pre-wrap bg-white p-4 rounded-lg border border-gray-200 text-gray-800 text-base leading-relaxed font-mono max-h-[400px] overflow-y-auto">{{ formatCommitMessage(selectedCommit?.message || '') }}</pre>
          </div>

          <div class="flex justify-end space-x-3 mt-4">
            <button
              @click="closeCommitDetailsDialog"
              class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              關閉
            </button>
          </div>
        </div>
      </div>
    </dialog>

    <!-- 添加回退版本確認對話框 -->
    <dialog ref="resetConfirmDialog" class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 rounded-lg shadow-xl p-0 w-full max-w-xl">
      <div class="p-6">
        <div class="flex items-center mb-4">
          <i class="fas fa-exclamation-triangle text-yellow-500 text-3xl mr-3"></i>
          <h3 class="text-lg font-semibold text-gray-900">確認回退版本？</h3>
        </div>
        <div class="space-y-4">
          <p class="mb-4 text-gray-600">
            您即將回退到提交 <code class="font-mono bg-gray-100 px-2 py-1 rounded">{{ selectedCommitHash?.substring(0, 7) }}</code>
          </p>
          <div class="bg-yellow-50 p-4 rounded-lg border border-yellow-100">
            <i class="fas fa-exclamation-triangle text-yellow-500 mr-2"></i>
            <span class="text-sm text-yellow-700">
              此操作將會重置當前工作目錄到選定的版本，且無法復原。
              <br>請確保您已經提交或備份了所有重要更改。
            </span>
          </div>
          <div class="flex justify-end space-x-3 mt-4">
            <button
              @click="closeResetConfirmDialog"
              class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              取消
            </button>
            <button
              @click="confirmReset"
              class="px-4 py-2 text-white bg-red-500 rounded-lg hover:bg-red-600"
            >
              確認回退
            </button>
          </div>
        </div>
      </div>
    </dialog>
  </div>
</template>

<script>
import { gitAPI } from '@/api'
import { ElMessage } from 'element-plus'
import Swal from 'sweetalert2'
import { useLogger } from '@/composables/useLogger'

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
      repoPath: localStorage.getItem('repoPath') || '',
      currentBranch: 'master',
      parsedStatus: {
        untracked: [],
        modified: []
      },
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      sortKey: 'date',
      sortOrder: 'desc',
      showRepoPathDialog: false,
      tempRepoPath: '',
      isValidCommitMessage: false,
      isValidConfig: false,
      isValidRemote: false,
      alertType: 'success',
      alertTitle: '',
      alertMessage: '',
      showCancelButton: false,
      alertResolve: null,
      alertReject: null,
      unstagedFiles: [],
      hasAttemptedConfig: false,
      hasAttemptedRemote: false,
      validationErrors: {
        config: {
          name: '',
          email: ''
        },
        remote: {
          name: '',
          url: ''
        }
      },
      selectedCommit: null,
      selectedCommitHash: null,
    }
  },
  setup() {
    const { logOperation } = useLogger()
    return { logOperation }
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
      if (!this.repoPath) {
        await this.setRepoPath()
        return
      }

      try {
        await gitAPI.initRepo(this.repoPath)
        await this.logOperation('【Git管理】初始化倉庫', '新增')
        Swal.fire({
          icon: 'success',
          title: '倉庫初始化成功',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
        await this.checkStatus()
      } catch (error) {
        console.error('Error initializing repo:', error)
        // 如果初始化失敗，可能是路徑問題，提示重新設置
        const result = await Swal.fire({
          icon: 'error',
          title: '初始化失敗',
          text: '是否重新設置倉庫路徑？',
          showCancelButton: true,
          confirmButtonText: '重新設置',
          cancelButtonText: '取消'
        })
        
        if (result.isConfirmed) {
          await this.setRepoPath()
        }
      }
    },

    async configureGit() {
      this.hasAttemptedConfig = true
      this.validateConfig()
      if (!this.isValidConfig) {
        return
      }

      try {
        await gitAPI.configureGit(this.config)
        await this.logOperation('【Git管理】更新Git配置', '修改')
        Swal.fire({
          icon: 'success',
          title: 'Git 配置已更新',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
        this.hasAttemptedConfig = false
      } catch (error) {
        // 錯誤處理已在 axios 攔截器中完成
      }
    },

    async addRemote() {
      this.hasAttemptedRemote = true
      this.validateRemote()
      if (!this.isValidRemote) {
        return
      }

      try {
        await gitAPI.addRemote(this.remote)
        await this.logOperation(`【Git管理】添加遠程倉庫 ${this.remote.name}`, '新增')
        Swal.fire({
          icon: 'success',
          title: '遠程倉庫已添加',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
        this.isRepoConfigured = true
        this.hasAttemptedRemote = false
        
        // 添加遠程倉庫後，依序執行：
        await this.checkStatus()  // 1. 檢查倉庫狀態
        await this.getHistory()   // 2. 獲取提交歷史
        
      } catch (error) {
        this.isRepoConfigured = false
      }
    },

    async checkStatus() {
      try {
        const response = await gitAPI.getStatus()
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
        await gitAPI.addFiles()
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
        // 先檢查狀態
        await this.checkStatus()
        
        // 如果有未添加的文件，詢問用戶是否要添加
        if (this.parsedStatus.modified.length || this.parsedStatus.untracked.length) {
          this.unstagedFiles = [...this.parsedStatus.modified, ...this.parsedStatus.untracked]
          this.$refs.unstagedDialog.showModal()
          return
        }

        // 執行提交
        await gitAPI.commit(this.commitMessage)
        this.commitMessage = ''
        this.showCommitError = false
        
        // 提交成功後更新狀態和歷史
        await this.checkStatus()
        await this.getHistory()
        
        await this.logOperation('【Git管理】提交更改', '新增')
        Swal.fire({
          icon: 'success',
          title: '更改已提交',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
      } catch (error) {
        console.error('Error committing:', error)
      }
    },

    async createBranch() {
      this.showBranchError = true
      if (!this.branchName) return
      try {
        await gitAPI.createBranch(this.branchName)
        this.branchName = ''
        this.showBranchError = false
        await this.logOperation(`【Git管理】創建分支 ${this.branchName}`, '新增')
      } catch (error) {
        // 錯誤處理已在 axios 攔截器中完成
      }
    },

    async switchBranch() {
      this.showBranchError = true
      if (!this.branchName) return
      try {
        await gitAPI.switchBranch(this.branchName)
        this.branchName = ''
        this.showBranchError = false
        await this.checkStatus()
        await this.logOperation(`【Git管理】切換到分支 ${this.branchName}`, '修改')
      } catch (error) {
        // 錯誤處理已在 axios 攔截器中完成
      }
    },

    async pull() {
      try {
        // 添加請求頭，指定 Content-Type
        const response = await gitAPI.pull()
        
        // 更新狀態和歷史
        await this.checkStatus()
        await this.getHistory()
        
        await this.logOperation('【Git管理】拉取更新', '更新')
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
        // 添加遠程倉庫名稱和分支名稱作為參數
        const response = await gitAPI.push()
        await this.checkStatus()
        await this.getHistory()
        
        await this.logOperation(`【Git管理】推送更改到 ${this.remote.name}/${this.currentBranch}`, '更新')
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
          // 添加遠程倉庫名稱和分支名稱作為參數
          const response = await gitAPI.push(true)
          await this.checkStatus()
          await this.getHistory()
          
          await this.logOperation(`【Git管理】強制推送到 ${this.remote.name}/${this.currentBranch}`, '更新')
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
      try {
        const response = await gitAPI.getHistory()
        this.commits = response.data.commits
      } catch (error) {
        console.error('Error getting commit history:', error)
        // 錯誤處理已在 axios 攔截器中完成
      }
    },

    async resetToCommit(hash) {
      this.selectedCommitHash = hash
      this.$refs.resetConfirmDialog.showModal()
    },

    closeResetConfirmDialog() {
      this.$refs.resetConfirmDialog.close()
      this.selectedCommitHash = null
    },

    async confirmReset() {
      try {
        await gitAPI.resetToCommit(this.selectedCommitHash)
        await this.checkStatus()
        await this.getHistory()
        
        ElMessage({
          message: `已成功回退到 ${this.selectedCommitHash.substring(0, 7)}`,
          type: 'success'
        })
        
        this.closeResetConfirmDialog()
      } catch (error) {
        // 錯誤處理已在 axios 攔截器中完成
      }
    },

    // 格式化提交信息
    formatCommitMessage(message) {
      // 處理 feat: 和 fix: 開頭的信息
      return message.replace(/(feat:|fix:)(.+?)($|\n)/, (match, prefix, content) => {
        return `${prefix}\n${content.trim()}`
      })
    },

    // 打開提交詳情對話框
    openCommitDetails(commit) {
      this.selectedCommit = commit
      this.$refs.commitDetailsDialog.showModal()
    },

    // 關閉提交詳情對話框
    closeCommitDetailsDialog() {
      this.$refs.commitDetailsDialog.close()
      this.selectedCommit = null
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
    },
    setRepoPath() {
      this.openRepoPathDialog()
    },
    openCommitDialog() {
      this.$refs.commitDialog.showModal()
    },
    closeCommitDialog() {
      this.$refs.commitDialog.close()
    },
    confirmCommit() {
      this.commit()
      this.closeCommitDialog()
    },
    openRepoPathDialog() {
      this.tempRepoPath = this.repoPath
      this.$refs.repoPathDialog.showModal()
    },
    closeRepoPathDialog() {
      this.$refs.repoPathDialog.close()
      this.tempRepoPath = ''
    },
    async confirmRepoPath() {
      if (this.tempRepoPath) {
        this.repoPath = this.tempRepoPath
        localStorage.setItem('repoPath', this.repoPath)
        this.closeRepoPathDialog()
        await this.initRepo()
      }
    },
    validateCommitMessage() {
      // 檢查提交信息格式
      const commitPattern = /^(feat|fix|docs|style|refactor|test|chore):\s.+/
      this.isValidCommitMessage = commitPattern.test(this.commitMessage)
    },
    validateConfig() {
      // 重置錯誤信息
      this.validationErrors.config = {
        name: '',
        email: ''
      }
      
      // 驗證用戶名
      if (!this.config.name) {
        this.validationErrors.config.name = '請輸入用戶名稱'
      }
      
      // 驗證電子郵件
      if (!this.config.email) {
        this.validationErrors.config.email = '請輸入電子郵件'
      } else {
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/
        if (!emailPattern.test(this.config.email)) {
          this.validationErrors.config.email = '請輸入有效的電子郵件地址'
        }
      }
      
      this.isValidConfig = !this.validationErrors.config.name && !this.validationErrors.config.email
    },
    validateRemote() {
      // 重置錯誤信息
      this.validationErrors.remote = {
        name: '',
        url: ''
      }
      
      // 驗證遠程名稱
      if (!this.remote.name) {
        this.validationErrors.remote.name = '請輸入遠程名稱'
      }
      
      // 驗證遠程 URL
      if (!this.remote.url) {
        this.validationErrors.remote.url = '請輸入遠程 URL'
      } else {
        // Git URL 格式驗證
        const urlPattern = /^(https?:\/\/|git@)([^\s:]+)(:|\/)[^\s]+$/
        if (!urlPattern.test(this.remote.url)) {
          this.validationErrors.remote.url = '請輸入有效的 Git 倉庫 URL'
        }
      }
      
      this.isValidRemote = !this.validationErrors.remote.name && !this.validationErrors.remote.url
    },
    async handleUnstagedConfirm() {
      this.$refs.unstagedDialog.close()
      await this.addFiles()
      await this.commit()
    },
    async handleUnstagedCancel() {
      this.$refs.unstagedDialog.close()
      // 用戶選擇不添加文件，繼續提交流程
      await this.commit()
    },
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
  async mounted() {
    await this.logOperation('【Git管理】訪問Git管理頁面', '查看')
  }
}
</script>

<style>
/* 提交詳情彈窗樣式 */
.commit-details-modal .swal2-popup {
  padding: 1.5rem;
  background: #1e293b; /* 深色背景 */
  color: #fff; /* 默認文字顏色為白色 */
}

.commit-details-modal .swal2-title {
  color: #fff !important; /* 強制標題文字為白色 */
}

.commit-details-modal .swal2-html-container {
  margin: 1rem 0 0 0;
  text-align: left;
  color: #fff; /* 內容文字顏色為白色 */
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

/* 動畫效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes fadeOut {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.95);
  }
}

.animate__fadeIn {
  animation: fadeIn 0.2s ease-out;
}

.animate__fadeOut {
  animation: fadeOut 0.2s ease-in;
}
</style>

<style scoped>
dialog::backdrop {
  background-color: rgba(0, 0, 0, 0.5);
}

dialog {
  border: none;
  padding: 0;
  margin: 0;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* 添加滾動條樣式 */
pre::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

pre::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

pre::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

pre::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style> 