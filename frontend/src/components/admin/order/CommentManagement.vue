<template>
  <div>
    <!-- 篩選器 -->
    <div class="bg-white rounded-lg shadow-sm mb-6">
      <div class="p-4 flex justify-between items-center">
        <div class="flex items-center space-x-4">
          <!-- 每頁顯示筆數選擇 -->
          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-600">顯示</span>
            <select v-model="pageSize" 
                    class="px-3 py-2 pr-8 bg-white border rounded-lg focus:ring-2 focus:ring-blue-500 appearance-none">
              <option value="5">5</option>
              <option value="10">10</option>
              <option value="20">20</option>
              <option value="50">50</option>
            </select>
            <span class="text-sm text-gray-600">筆</span>
          </div>
          <!-- 狀態篩選 -->
          <select v-model="filterStatus" 
                  class="px-4 py-2 pr-10 bg-white border rounded-lg focus:ring-2 focus:ring-blue-500 appearance-none">
            <option value="all">全部狀態</option>
            <option value="pending">待審核</option>
            <option value="approved">已審核</option>
            <option value="rejected">已拒絕</option>
          </select>
        </div>
        <div class="relative">
          <input type="text" 
                 v-model="searchQuery" 
                 placeholder="搜尋留言..." 
                 class="pl-10 pr-4 py-2 border rounded-lg w-64 focus:ring-2 focus:ring-blue-500">
          <i class="fas fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
        </div>
      </div>
    </div>

    <!-- 留言列表 -->
    <div class="space-y-6">
      <div v-for="comment in paginatedComments" 
           :key="comment.id" 
           class="bg-white rounded-lg shadow-sm overflow-hidden">
        <!-- 留言主體 -->
        <div class="p-6">
          <div class="flex justify-between items-start mb-4">
            <div class="flex items-center space-x-4">
              <img :src="comment.userAvatar" 
                   class="w-12 h-12 rounded-full ring-2 ring-gray-100">
              <div>
                <h3 class="font-medium text-gray-900">{{ comment.userName }}</h3>
                <p class="text-sm text-gray-500">{{ comment.createTime }}</p>
              </div>
            </div>
            <div class="flex items-center space-x-3">
              <span :class="[
                'px-3 py-1 text-xs rounded-full font-medium',
                getStatusClass(comment.status)
              ]">
                {{ getStatusText(comment.status) }}
              </span>
              <div class="flex items-center space-x-2" v-if="comment.status === 'pending'">
                <button @click="approveComment(comment)" 
                        class="p-1.5 text-green-600 hover:text-green-800 rounded-full hover:bg-green-50">
                  <i class="fas fa-check"></i>
                </button>
                <button @click="rejectComment(comment)" 
                        class="p-1.5 text-red-600 hover:text-red-800 rounded-full hover:bg-red-50">
                  <i class="fas fa-times"></i>
                </button>
              </div>
              <button @click="deleteComment(comment)" 
                      class="p-1.5 text-gray-600 hover:text-gray-800 rounded-full hover:bg-gray-100">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
          <p class="text-gray-700">{{ comment.content }}</p>
        </div>

        <!-- 回覆列表 -->
        <div v-if="comment.replies && comment.replies.length" 
             class="bg-gray-50 border-t">
          <div class="p-4 space-y-4">
            <div v-for="reply in comment.replies" 
                 :key="reply.id" 
                 class="flex items-start space-x-3">
              <img :src="reply.userAvatar" 
                   class="w-8 h-8 rounded-full mt-1">
              <div class="flex-1 bg-white rounded-lg p-4 shadow-sm">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <h4 class="font-medium text-gray-900">{{ reply.userName }}</h4>
                    <p class="text-xs text-gray-500">{{ reply.createTime }}</p>
                  </div>
                  <button @click="deleteReply(comment, reply)" 
                          class="p-1.5 text-gray-600 hover:text-gray-800 rounded-full hover:bg-gray-100">
                    <i class="fas fa-trash"></i>
                  </button>
                </div>
                <p class="text-gray-700">{{ reply.content }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 回覆輸入框 -->
        <div class="p-4 bg-gray-50 border-t">
          <div class="flex items-center space-x-3">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=shop1" 
                 class="w-8 h-8 rounded-full">
            <div class="flex-1 relative">
              <input type="text" 
                     v-model="comment.replyText" 
                     placeholder="輸入回覆..." 
                     class="w-full pl-4 pr-20 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
              <button @click="addReply(comment)" 
                      class="absolute right-2 top-1/2 -translate-y-1/2 px-4 py-1 bg-blue-500 text-white rounded-lg hover:bg-blue-600 text-sm">
                回覆
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分頁控制 -->
    <div class="mt-6 flex justify-center">
      <nav class="flex items-center space-x-2">
        <button @click="currentPage--" 
                :disabled="currentPage === 1"
                class="px-3 py-1 rounded border transition-colors duration-200"
                :class="currentPage === 1 ? 'text-gray-400 bg-gray-50' : 'hover:bg-gray-50'">
          <i class="fas fa-chevron-left"></i>
        </button>
        <button v-for="page in totalPages" 
                :key="page"
                @click="currentPage = page"
                class="px-3 py-1 rounded transition-colors duration-200"
                :class="currentPage === page ? 'bg-blue-500 text-white' : 'border hover:bg-gray-50'">
          {{ page }}
        </button>
        <button @click="currentPage++" 
                :disabled="currentPage === totalPages"
                class="px-3 py-1 rounded border transition-colors duration-200"
                :class="currentPage === totalPages ? 'text-gray-400 bg-gray-50' : 'hover:bg-gray-50'">
          <i class="fas fa-chevron-right"></i>
        </button>
      </nav>
    </div>

    <!-- 返回首頁按鈕 -->
    <BackToHome />
  </div>
</template>

<script>
import BackToHome from '../common/BackToHome.vue'

export default {
  name: 'CommentManagement',
  components: {
    BackToHome
  },
  data() {
    return {
      searchQuery: '',
      filterStatus: 'all',
      currentPage: 1,
      pageSize: 5, // 預設顯示5筆
      comments: [
        {
          id: 1,
          userName: '王小明',
          userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=1',
          content: '這家店的珍珠奶茶真的很好喝！',
          createTime: '2024-01-15 15:30:22',
          status: 'approved',
          replies: [
            {
              id: 1,
              userName: '店家',
              userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=shop1',
              content: '謝謝您的支持！',
              createTime: '2024-01-15 16:00:00'
            }
          ],
          replyText: ''
        },
        {
          id: 2,
          userName: '李小華',
          userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=2',
          content: '奶茶濃度剛剛好，珍珠也很Q彈',
          createTime: '2024-01-15 16:45:33',
          status: 'pending',
          replies: [],
          replyText: ''
        },
        {
          id: 3,
          userName: '張小美',
          userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=3',
          content: '服務態度很好，店員很親切',
          createTime: '2024-01-16 09:15:20',
          status: 'approved',
          replies: [
            {
              id: 2,
              userName: '店家',
              userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=shop1',
              content: '感謝您的肯定，我們會繼續努力！',
              createTime: '2024-01-16 09:30:15'
            }
          ],
          replyText: ''
        },
        {
          id: 4,
          userName: '陳大寶',
          userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=4',
          content: '價格有點貴，但是品質確實不錯',
          createTime: '2024-01-16 14:22:45',
          status: 'approved',
          replies: [],
          replyText: ''
        },
        {
          id: 5,
          userName: '林小玉',
          userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=5',
          content: '希望可以增加一些新口味',
          createTime: '2024-01-17 11:05:38',
          status: 'pending',
          replies: [],
          replyText: ''
        },
        {
          id: 6,
          userName: '黃小龍',
          userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=6',
          content: '飲料太甜了，建議可以再少糖一點',
          createTime: '2024-01-17 15:40:12',
          status: 'rejected',
          replies: [],
          replyText: ''
        },
        {
          id: 7,
          userName: '吳小菁',
          userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=7',
          content: '包裝很精美，很適合送禮',
          createTime: '2024-01-18 10:25:55',
          status: 'approved',
          replies: [
            {
              id: 3,
              userName: '店家',
              userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=shop1',
              content: '謝謝支持，之後會推出更多禮盒包裝！',
              createTime: '2024-01-18 10:40:30'
            }
          ],
          replyText: ''
        },
        {
          id: 8,
          userName: '蔡小雯',
          userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=8',
          content: '等候時間有點久，但是飲料品質不錯',
          createTime: '2024-01-18 16:15:40',
          status: 'pending',
          replies: [],
          replyText: ''
        },
        {
          id: 9,
          userName: '周小倫',
          userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=9',
          content: '店面環境很舒適，很適合朋友聚會',
          createTime: '2024-01-19 13:30:25',
          status: 'approved',
          replies: [],
          replyText: ''
        },
        {
          id: 10,
          userName: '謝小芳',
          userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=10',
          content: '外送服務很準時，飲料保溫效果也很好',
          createTime: '2024-01-19 17:50:15',
          status: 'approved',
          replies: [
            {
              id: 4,
              userName: '店家',
              userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=shop1',
              content: '感謝您的支持，我們會持續提供優質的外送服務！',
              createTime: '2024-01-19 18:00:00'
            }
          ],
          replyText: ''
        }
      ]
    }
  },
  computed: {
    filteredComments() {
      return this.comments.filter(comment => {
        const matchesSearch = comment.content.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                            comment.userName.toLowerCase().includes(this.searchQuery.toLowerCase())
        const matchesStatus = this.filterStatus === 'all' || comment.status === this.filterStatus
        return matchesSearch && matchesStatus
      })
    },
    paginatedComments() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredComments.slice(start, end)
    },
    totalPages() {
      return Math.ceil(this.filteredComments.length / this.pageSize)
    }
  },
  watch: {
    pageSize() {
      // 當每頁顯示筆數改變時，重置當前頁碼
      this.currentPage = 1
    }
  },
  methods: {
    getStatusClass(status) {
      const classes = {
        pending: 'bg-yellow-100 text-yellow-800',
        approved: 'bg-green-100 text-green-800',
        rejected: 'bg-red-100 text-red-800'
      }
      return classes[status]
    },
    getStatusText(status) {
      const texts = {
        pending: '待審核',
        approved: '已審核',
        rejected: '已拒絕'
      }
      return texts[status]
    },
    approveComment(comment) {
      comment.status = 'approved'
    },
    rejectComment(comment) {
      comment.status = 'rejected'
    },
    deleteComment(comment) {
      if(confirm('確定要刪除此留言嗎？')) {
        this.comments = this.comments.filter(c => c.id !== comment.id)
      }
    },
    deleteReply(comment, reply) {
      if(confirm('確定要刪除此回覆嗎？')) {
        comment.replies = comment.replies.filter(r => r.id !== reply.id)
      }
    },
    addReply(comment) {
      if(!comment.replyText.trim()) return
      
      comment.replies.push({
        id: Date.now(),
        userName: '店家',
        userAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=shop1',
        content: comment.replyText,
        createTime: new Date().toISOString().slice(0, 19).replace('T', ' ')
      })
      comment.replyText = ''
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