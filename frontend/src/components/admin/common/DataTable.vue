<template>
  <div class="bg-white rounded-lg shadow-sm overflow-hidden">
    <!-- 表格控制列 -->
    <div class="p-4 border-b flex justify-between items-center bg-gray-900 text-white">
      <div class="flex items-center space-x-2">
        <span class="text-sm">顯示</span>
        <select v-model="pageSize" 
                class="bg-gray-800 border-gray-700 text-white text-sm rounded px-3 py-1 pr-8 focus:ring-1 focus:ring-blue-500 appearance-none">
          <option value="10">10</option>
          <option value="25">25</option>
          <option value="50">50</option>
          <option value="100">100</option>
        </select>
        <span class="text-sm">筆資料</span>
      </div>
      <div class="flex items-center space-x-4">
        <button v-if="selectedItems.length" 
                @click="batchDelete"
                class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 text-sm">
          <i class="fas fa-trash-alt mr-2"></i>批次刪除
        </button>
        <button @click="$emit('add')" 
                class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm">
          <i class="fas fa-plus mr-2"></i>新增
        </button>
        <div class="relative">
          <input type="text" 
                 v-model="searchQuery" 
                 placeholder="搜尋使用者..." 
                 class="bg-gray-800 border-gray-700 text-white pl-8 pr-4 py-1 rounded w-64 focus:ring-1 focus:ring-blue-500">
          <i class="fas fa-search absolute left-3 top-2.5 text-gray-400"></i>
        </div>
      </div>
    </div>

    <!-- 表格內容 -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left">
              <input type="checkbox" 
                     v-model="selectAll"
                     @change="toggleSelectAll"
                     class="rounded border-gray-300">
            </th>
            <th v-for="column in columns" 
                :key="column.key"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ column.label }}
            </th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              操作
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="item in paginatedData" :key="item.id" class="hover:bg-gray-50">
            <td class="px-6 py-4">
              <input type="checkbox" 
                     v-model="selectedItems"
                     :value="item.id"
                     class="rounded border-gray-300">
            </td>
            <td v-for="column in columns" 
                :key="column.key"
                class="px-6 py-4 whitespace-nowrap">
              <slot :name="column.key" :item="item">
                {{ item[column.key] }}
              </slot>
            </td>
            <td class="px-6 py-4 text-right space-x-2">
              <button @click="$emit('edit', item)" 
                      class="text-blue-600 hover:text-blue-900">
                <i class="fas fa-edit"></i>
              </button>
              <button @click="$emit('delete', item)" 
                      class="text-red-600 hover:text-red-900">
                <i class="fas fa-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分頁區域 -->
    <div class="px-6 py-4 mt-2 flex justify-between items-center border-t">
      <div class="text-sm text-gray-700">
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
                  'px-4 py-2 rounded-lg border min-w-[40px]',
                  currentPage === page 
                    ? 'bg-blue-500 text-white border-blue-500'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
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
    }
  },
  data() {
    return {
      searchQuery: '',
      pageSize: 10,
      currentPage: 1,
      selectedItems: [],
      selectAll: false
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
      if (this.selectAll) {
        this.selectedItems = this.paginatedData.map(item => item.id)
      } else {
        this.selectedItems = []
      }
    },
    batchDelete() {
      this.$emit('batch-delete', this.selectedItems)
      this.selectedItems = []
      this.selectAll = false
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