<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm overflow-hidden">
    <!-- 表格控制列 -->
    <div class="px-6 py-4 border-b dark:border-gray-700 flex justify-between items-center bg-gradient-to-r from-indigo-100 to-blue-100 dark:from-gray-700 dark:to-gray-800">
      <div class="flex items-center space-x-2">
        <span class="text-sm text-gray-700 dark:text-gray-300">顯示</span>
        <select v-model="pageSize" 
                class="bg-white dark:bg-gray-700 border border-indigo-200 dark:border-gray-600 text-gray-700 dark:text-gray-300 text-sm rounded-md px-3 py-1.5 pr-8 focus:ring-1 focus:ring-indigo-400 dark:focus:ring-indigo-500 focus:border-indigo-400 dark:focus:border-indigo-500">
          <option value="10">10</option>
          <option value="25">25</option>
          <option value="50">50</option>
          <option value="100">100</option>
        </select>
        <span class="text-sm text-gray-700 dark:text-gray-300">筆資料</span>
      </div>
      <!-- 使用具名插槽來自定義工具欄 -->
      <slot name="toolbar">
        <div class="flex items-center space-x-4">
          <button v-if="selectedItems.length" 
                  @click="batchDelete"
                  class="px-4 py-2 bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded-md hover:bg-red-200 dark:hover:bg-red-900/50 text-sm transition-colors duration-200 border border-red-200 dark:border-red-800">
            <i class="fas fa-trash-alt mr-2"></i>批次刪除
          </button>
          <button v-if="showAddButton" 
                  @click="$emit('add')"
                  class="inline-flex items-center px-4 py-2 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 text-sm rounded-md hover:bg-emerald-200 dark:hover:bg-emerald-900/50 transition-colors duration-200 border border-emerald-200 dark:border-emerald-800">
            <i class="fas fa-plus mr-1.5"></i>新增
          </button>
          <div class="relative">
            <input type="text" 
                   v-model="searchQuery" 
                   placeholder="搜尋..." 
                   class="bg-white dark:bg-gray-700 border border-indigo-200 dark:border-gray-600 text-gray-700 dark:text-gray-300 pl-8 pr-4 py-1.5 rounded-md w-64 focus:ring-1 focus:ring-indigo-400 dark:focus:ring-indigo-500 focus:border-indigo-400 dark:focus:border-indigo-500 placeholder-gray-500 dark:placeholder-gray-400">
            <i class="fas fa-search absolute left-3 top-2.5 text-gray-500 dark:text-gray-400"></i>
          </div>
        </div>
      </slot>
    </div>

    <!-- 表格內容 -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gradient-to-r from-indigo-100 to-blue-100 dark:from-gray-700 dark:to-gray-800 sticky top-0">
          <tr>
            <th v-if="selectable" scope="col" class="w-12 px-3 py-3">
              <input type="checkbox" 
                     @change="toggleSelectAll"
                     :checked="isAllSelected"
                     :indeterminate="selectedItems.length > 0 && !isAllSelected"
                     class="rounded border-indigo-300 dark:border-gray-600 text-indigo-600 dark:text-indigo-500 focus:ring-indigo-500 dark:focus:ring-indigo-400 focus:ring-offset-0">
            </th>
            <th v-for="column in columns" 
                :key="column.key"
                scope="col"
                class="px-6 py-3.5 text-left text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider">
              {{ column.label }}
            </th>
            <!-- 如果不是只使用自定義操作欄，則顯示預設操作欄標題 -->
            <th v-if="!customActionsOnly && showDefaultActions" 
                class="px-6 py-3.5 text-right text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider">
              操作
            </th>
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="item in paginatedData" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-150">
            <td v-if="selectable" class="w-12 px-3 py-4">
              <input type="checkbox" 
                     v-model="selectedItems"
                     :value="item.id"
                     class="rounded border-gray-300 text-blue-600 focus:ring-blue-500 focus:ring-offset-0">
            </td>
            <td v-for="column in columns" 
                :key="column.key"
                class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              <slot :name="column.key" :item="item">
                {{ column.formatter ? column.formatter(item[column.key]) : item[column.key] }}
              </slot>
            </td>
            <!-- 如果不是只使用自定義操作欄，則顯示預設操作按鈕 -->
            <td v-if="!customActionsOnly && showDefaultActions" 
                class="px-6 py-4 text-right space-x-3">
              <button v-if="showEditButton"
                      @click="$emit('edit', item)" 
                      class="inline-flex items-center px-3 py-1.5 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-sm rounded-md hover:bg-blue-200 dark:hover:bg-blue-900/50 transition-colors duration-200 border border-blue-200 dark:border-blue-800">
                <i class="fas fa-edit mr-1.5"></i>編輯
              </button>
              <button @click="$emit('delete', item)" 
                      class="inline-flex items-center px-3 py-1.5 bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 text-sm rounded-md hover:bg-red-200 dark:hover:bg-red-900/50 transition-colors duration-200 border border-red-200 dark:border-red-800">
                <i class="fas fa-trash mr-1.5"></i>刪除
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分頁區域 -->
    <div class="px-6 py-4 flex justify-between items-center border-t dark:border-gray-700 bg-gradient-to-r from-indigo-100 to-blue-100 dark:from-gray-700 dark:to-gray-800">
      <div class="text-sm text-gray-700 dark:text-gray-300">
        顯示第 {{ startIndex + 1 }} 至 {{ endIndex }} 筆，共 {{ totalItems }} 筆資料
      </div>
      <div class="flex items-center space-x-2">
        <!-- 首頁按鈕 -->
        <button @click="goToFirstPage"
                :disabled="currentPage === 1"
                :class="[
                  'px-3 py-2 rounded-lg border',
                  currentPage === 1 
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                ]">
          <i class="fas fa-angle-double-left"></i>
        </button>
        
        <!-- 上一頁按鈕 -->
        <button @click="previousPage"
                :disabled="currentPage === 1"
                :class="[
                  'px-3 py-2 rounded-lg border',
                  currentPage === 1 
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                ]">
          <i class="fas fa-angle-left"></i>
        </button>
        
        <!-- 頁碼按鈕 -->
        <button v-for="page in displayedPages"
                :key="page"
                @click="goToPage(page)"
                :class="[
                  'px-4 py-2 rounded-lg border transition-colors duration-200 min-w-[40px]',
                  currentPage === page 
                    ? 'bg-indigo-500 dark:bg-indigo-600 text-white border-indigo-500 dark:border-indigo-600 hover:bg-indigo-600 dark:hover:bg-indigo-700'
                    : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-gray-200 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-600'
                ]">
          {{ page }}
        </button>
        
        <!-- 下一頁按鈕 -->
        <button @click="nextPage"
                :disabled="currentPage === totalPages"
                :class="[
                  'px-3 py-2 rounded-lg border',
                  currentPage === totalPages 
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                ]">
          <i class="fas fa-angle-right"></i>
        </button>
        
        <!-- 末頁按鈕 -->
        <button @click="goToLastPage"
                :disabled="currentPage === totalPages"
                :class="[
                  'px-3 py-2 rounded-lg border',
                  currentPage === totalPages 
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                ]">
          <i class="fas fa-angle-double-right"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataTable',
  props: {
    columns: {
      type: Array,
      required: true
    },
    data: {
      type: Array,
      required: true
    },
    selectable: {
      type: Boolean,
      default: true
    },
    showAddButton: {
      type: Boolean,
      default: true
    },
    showEditButton: {
      type: Boolean,
      default: true
    },
    customActionsOnly: {
      type: Boolean,
      default: false
    },
    showDefaultActions: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      searchQuery: '',
      pageSize: 10,
      currentPage: 1,
      selectedItems: [],
    }
  },
  computed: {
    filteredData() {
      return this.data.filter(item => {
        return this.columns.some(column => {
          const value = item[column.key]
          return value && value.toString().toLowerCase().includes(this.searchQuery.toLowerCase())
        })
      })
    },
    totalItems() {
      return this.filteredData.length
    },
    totalPages() {
      return Math.ceil(this.totalItems / this.pageSize)
    },
    startIndex() {
      return (this.currentPage - 1) * this.pageSize
    },
    endIndex() {
      return Math.min(this.startIndex + this.pageSize, this.totalItems)
    },
    paginatedData() {
      return this.filteredData.slice(this.startIndex, this.endIndex)
    },
    displayedPages() {
      const pages = []
      let start = Math.max(1, this.currentPage - 2)
      let end = Math.min(this.totalPages, start + 4)
      
      if (end - start < 4) {
        start = Math.max(1, end - 4)
      }
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
    },
    hasDefaultActions() {
      return true
    },
    showDefaultActions() {
      return !this.customActionsOnly && this.$props.showDefaultActions
    },
    isAllSelected() {
      return this.paginatedData.length > 0 && this.selectedItems.length === this.paginatedData.length
    },
    currentPageIds() {
      return this.paginatedData.map(item => item.id)
    }
  },
  methods: {
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
      }
    },
    goToPage(page) {
      this.currentPage = page
    },
    toggleSelectAll() {
      if (this.isAllSelected) {
        this.selectedItems = this.selectedItems.filter(id => !this.currentPageIds.includes(id))
      } else {
        const newSelectedItems = new Set([...this.selectedItems, ...this.currentPageIds])
        this.selectedItems = Array.from(newSelectedItems)
      }
    },
    batchDelete() {
      this.$emit('batch-delete', this.selectedItems)
      this.selectedItems = []
    },
    // 跳轉到首頁
    goToFirstPage() {
      if (this.currentPage !== 1) {
        this.currentPage = 1
        this.$emit('page-change', this.currentPage)
      }
    },
    // 跳轉到末頁
    goToLastPage() {
      if (this.currentPage !== this.totalPages) {
        this.currentPage = this.totalPages
        this.$emit('page-change', this.currentPage)
      }
    }
  },
  watch: {
    pageSize() {
      this.currentPage = 1
    },
    searchQuery() {
      this.currentPage = 1
    },
    currentPage() {
      this.selectedItems = []
    },
    pageSize() {
      this.selectedItems = []
    }
  }
}
</script>

<style scoped>
/* 自定義下拉選單箭頭 */
select {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
}
</style> 