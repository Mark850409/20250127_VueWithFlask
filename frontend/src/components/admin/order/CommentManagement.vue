<template>
  <div>
    <!-- 篩選器 -->
    <div class="bg-white rounded-lg shadow-md mb-6 border border-gray-100">
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
                 placeholder="搜尋店家或評論..." 
                 class="pl-10 pr-4 py-2 border rounded-lg w-64 focus:ring-2 focus:ring-blue-500">
          <i class="fas fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
        </div>
      </div>
    </div>

    <!-- 評論列表 -->
    <div class="space-y-6">
      <!-- 無評論時的提示 -->
      <div v-if="!filteredComments.length" 
           class="bg-white rounded-lg shadow-md p-8 text-center border border-gray-100">
        <div class="text-gray-400 mb-3">
          <i class="fas fa-comments text-6xl"></i>
        </div>
        <h3 class="text-xl font-medium text-gray-600 mb-2">尚無留言</h3>
        <p class="text-gray-500">目前還沒有任何評論</p>
      </div>

      <!-- 有評論時顯示列表 -->
      <div v-for="comment in paginatedComments" 
           :key="comment.id" 
           class="bg-white rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-shadow duration-300">
        <!-- 店家資訊 -->
        <div class="border-b bg-gray-50/80 p-4">
          <div class="flex items-center space-x-4">
            <img :src="comment.store_image" 
                 class="w-16 h-16 object-cover rounded-lg shadow-sm">
            <div>
              <h3 class="font-medium text-lg text-gray-800">{{ comment.store_name }}</h3>
              <div class="flex items-center mt-1">
                <div class="flex text-yellow-400 mr-2">
                  <i v-for="n in 5" :key="n" 
                     :class="['fas', n <= comment.rating ? 'fa-star' : 'fa-star-o']">
                  </i>
                </div>
                <span class="text-sm text-gray-600">{{ comment.rating }} 分</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 評論主體 -->
        <div class="p-6 bg-white">
          <div class="flex justify-between items-start mb-4">
            <div class="flex items-center space-x-4">
              <img :src="comment.userAvatar" 
                   class="w-12 h-12 rounded-full shadow-sm ring-2 ring-gray-100">
              <div>
                <h3 class="font-medium text-gray-800">{{ comment.userName }}</h3>
                <p class="text-sm text-gray-500">{{ comment.userEmail }}</p>
                <p class="text-sm text-gray-500">{{ comment.createTime }}</p>
              </div>
            </div>
            <div class="flex items-center space-x-3">
              <span :class="[
                'px-3 py-1 text-xs rounded-full font-medium shadow-sm',
                {
                  'bg-yellow-100 text-yellow-800 border border-yellow-200': comment.status === 'pending',
                  'bg-green-100 text-green-800 border border-green-200': comment.status === 'approved',
                  'bg-red-100 text-red-800 border border-red-200': comment.status === 'rejected'
                }
              ]">
                {{ getStatusText(comment.status) }}
              </span>
              <div class="flex items-center space-x-2" v-if="comment.status === 'pending'">
                <button @click="approveComment(comment)" 
                        class="p-1.5 text-green-600 hover:text-green-800 rounded-full hover:bg-green-50 shadow-sm transition-colors duration-200">
                  <i class="fas fa-check"></i>
                </button>
                <button @click="rejectComment(comment)" 
                        class="p-1.5 text-red-600 hover:text-red-800 rounded-full hover:bg-red-50 shadow-sm transition-colors duration-200">
                  <i class="fas fa-times"></i>
                </button>
              </div>
              <button @click="handleDeleteComment(comment)" 
                      class="p-1.5 text-gray-600 hover:text-gray-800 rounded-full hover:bg-gray-100 shadow-sm transition-colors duration-200">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
          <!-- 評分和評論內容 -->
          <div class="mb-4">
            <div class="flex text-yellow-400 mb-2">
              <i v-for="n in 5" :key="n" 
                 :class="['fas', 'fa-star', n <= comment.rating ? 'text-yellow-400' : 'text-gray-200']">
              </i>
            </div>
            <p class="text-gray-700 bg-gray-50/50 p-4 rounded-lg">{{ comment.content }}</p>
          </div>
        </div>

        <!-- 回覆列表 -->
        <div v-if="comment.replies && comment.replies.length" class="bg-gray-50/80 border-t">
          <div class="p-4 space-y-4">
            <div v-for="reply in comment.replies" :key="reply.id" class="flex items-start space-x-3">
              <img :src="shopAvatar" class="w-8 h-8 rounded-full mt-1 shadow-sm">
              <div class="flex-1 bg-white rounded-lg p-4 shadow-sm border border-gray-100">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <h4 class="font-medium text-gray-800">
                      <span class="bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full mr-2 shadow-sm">店家</span>
                      {{ reply.user_name }}
                    </h4>
                    <p class="text-xs text-gray-500">{{ reply.create_time }}</p>
                  </div>
                  <button @click="deleteReply(comment, reply)" 
                          class="p-1.5 text-gray-600 hover:text-gray-800 rounded-full hover:bg-gray-100 shadow-sm transition-colors duration-200">
                    <i class="fas fa-trash"></i>
                  </button>
                </div>
                <p class="text-gray-700">{{ reply.content }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 回覆輸入框 -->
        <div class="p-4 bg-gray-50/80 border-t">
          <div class="flex items-center space-x-3">
            <img :src="shopAvatar" 
                 class="w-8 h-8 rounded-full shadow-sm">
            <div class="flex-1 relative">
              <input type="text" 
                     v-model="comment.replyText" 
                     placeholder="店家回覆..." 
                     class="w-full pl-4 pr-20 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 shadow-sm">
              <button @click="addReply(comment)" 
                      class="absolute right-2 top-1/2 -translate-y-1/2 px-4 py-1 bg-blue-500 text-white rounded-lg hover:bg-blue-600 text-sm shadow-sm transition-colors duration-200">
                回覆
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分頁控制 -->
    <div v-if="filteredComments.length" 
         class="mt-6 flex justify-center">
      <nav class="flex items-center space-x-2 bg-white p-2 rounded-lg shadow-sm">
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
import { messageAPI } from '@/api'
import Swal from 'sweetalert2'

export default {
  name: 'CommentManagement',
  data() {
    return {
      searchQuery: '',
      filterStatus: 'all',
      currentPage: 1,
      pageSize: 5, // 預設顯示5筆
      shopAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=shop1',
      comments: [],
      userInfoMap: {}, // 用於存儲用戶資訊的映射
      loading: false,
      defaultAvatar: 'https://api.dicebear.com/9.x/bottts/svg?seed=Sara'
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
    // 獲取用戶資訊
    async getUserInfo(userId) {
      if (this.userInfoMap[userId]) {
        return this.userInfoMap[userId]
      }
      try {
        const userResponse = await messageAPI.getUserInfo(userId)
        const userData = userResponse.data
        console.log(userData)
        const userInfo = {
          userAvatar: this.getAvatarUrl(userData),
          userName: userData.username,
          userEmail: userData.email
        }
        this.userInfoMap[userId] = userInfo
        return userInfo
      } catch (error) {
        console.error(`獲取用戶 ${userId} 資料失敗:`, error)
        return {
          userAvatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${userId}`,
          userName: '未知用戶',
          userEmail: ''
        }
      }
    },
    // 新增頭像 URL 處理方法
    getAvatarUrl(user) {
      if (!user) return this.defaultAvatar
      if (!user.avatar) return this.defaultAvatar
      
      // 判斷是否為完整的 URL（Google 頭像）
      if (user.avatar.startsWith('http')) {
        return user.avatar
      }
      
      // 判斷是否包含路徑分隔符
      if (user.avatar.includes('/')) {
        return `${import.meta.env.VITE_BACKEND_URL}/api/users/avatar/${user.avatar.split('/').pop()}`
      } else {
        // 只有檔名的情況
        return `${import.meta.env.VITE_BACKEND_URL}/uploads/avatars/${user.avatar}`
      }
    },
    async fetchComments() {
      if (this.loading) return
      this.loading = true
      try {
        const response = await messageAPI.getMessages()
        const messages = response.data.messages
        
        const commentsWithUserInfo = await Promise.all(
          messages.map(async (message) => {
            const userInfo = await this.getUserInfo(message.user_id)
            return {
              ...message,
              ...userInfo
            }
          })
        )
        
        this.comments = commentsWithUserInfo
      } catch (error) {
        console.error('獲取評論失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '獲取評論失敗',
          text: error.response?.data?.message || '請稍後再試',
          confirmButtonText: '確定'
        })
      } finally {
        this.loading = false
      }
    },
    async handleReply(comment) {
      if (!comment.replyText.trim()) return
      
      try {
        await messageAPI.addReply(comment.id, {
          content: comment.replyText,
          user_name: '店家'
        })
        comment.replyText = ''
        // 直接更新本地數據
        const commentIndex = this.comments.findIndex(c => c.id === comment.id)
        if (commentIndex !== -1) {
          if (!this.comments[commentIndex].replies) {
            this.comments[commentIndex].replies = []
          }
          this.comments[commentIndex].replies.push({
            id: Date.now(), // 臨時ID
            content: comment.replyText,
            user_name: '店家',
            create_time: new Date().toISOString().replace('T', ' ').split('.')[0]
          })
        }
      } catch (error) {
        console.error('回覆失敗:', error)
      }
    },
    async handleDeleteReply(comment, reply) {
      if (!confirm('確定要刪除此回覆嗎？')) return
      
      try {
        await messageAPI.deleteReply(comment.id, reply.id)
        // 直接更新本地數據
        const commentIndex = this.comments.findIndex(c => c.id === comment.id)
        if (commentIndex !== -1) {
          this.comments[commentIndex].replies = this.comments[commentIndex].replies.filter(r => r.id !== reply.id)
        }
      } catch (error) {
        console.error('刪除回覆失敗:', error)
      }
    },
    async handleDeleteComment(comment) {
      const result = await Swal.fire({
        title: '確定要刪除此評論嗎？',
        text: '此操作無法復原！',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: '確定刪除',
        cancelButtonText: '取消'
      })
      
      if (!result.isConfirmed) return
      
      try {
        await messageAPI.deleteMessage(comment.id)
        // 直接從本地移除評論，不重新請求
        this.comments = this.comments.filter(c => c.id !== comment.id)
        Swal.fire({
          icon: 'success',
          title: '刪除成功',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
      } catch (error) {
        console.error('刪除評論失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '刪除失敗',
          text: error.response?.data?.message || '請稍後再試',
          confirmButtonText: '確定'
        })
      }
    },
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
    async approveComment(comment) {
      const result = await Swal.fire({
        title: '確定要通過此評論嗎？',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: '確定通過',
        cancelButtonText: '取消',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33'
      })
      
      if (!result.isConfirmed) return
      
      try {
        await messageAPI.updateMessage(comment.id, { status: 'approved' })
        const index = this.comments.findIndex(c => c.id === comment.id)
        if (index !== -1) {
          this.comments[index].status = 'approved'
          // 如果需要更新用戶資訊
          const userInfo = await this.getUserInfo(comment.user_id)
          this.comments[index] = { ...this.comments[index], ...userInfo }
        }
        Swal.fire({
          icon: 'success',
          title: '已通過評論',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
      } catch (error) {
        console.error('通過評論失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '操作失敗',
          text: error.response?.data?.message || '請稍後再試',
          confirmButtonText: '確定'
        })
      }
    },
    async rejectComment(comment) {
      const result = await Swal.fire({
        title: '確定要拒絕此評論嗎？',
        text: '此操作將使評論無法顯示',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '確定拒絕',
        cancelButtonText: '取消',
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6'
      })
      
      if (!result.isConfirmed) return
      
      try {
        await messageAPI.updateMessage(comment.id, { status: 'rejected' })
        const index = this.comments.findIndex(c => c.id === comment.id)
        if (index !== -1) {
          this.comments[index].status = 'rejected'
          // 如果需要更新用戶資訊
          const userInfo = await this.getUserInfo(comment.user_id)
          this.comments[index] = { ...this.comments[index], ...userInfo }
        }
        Swal.fire({
          icon: 'success',
          title: '已拒絕評論',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
      } catch (error) {
        console.error('拒絕評論失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '操作失敗',
          text: error.response?.data?.message || '請稍後再試',
          confirmButtonText: '確定'
        })
      }
    },
    async deleteReply(comment, reply) {
      const result = await Swal.fire({
        title: '確定要刪除此回覆嗎？',
        text: '此操作無法復原！',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: '確定刪除',
        cancelButtonText: '取消'
      })
      
      if (!result.isConfirmed) return
      
      try {
        await messageAPI.deleteReply(comment.id, reply.id)
        // 直接更新本地數據
        const commentIndex = this.comments.findIndex(c => c.id === comment.id)
        if (commentIndex !== -1) {
          this.comments[commentIndex].replies = this.comments[commentIndex].replies.filter(r => r.id !== reply.id)
        }
        Swal.fire({
          icon: 'success',
          title: '刪除成功',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
      } catch (error) {
        console.error('刪除回覆失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '刪除失敗',
          text: error.response?.data?.message || '請稍後再試',
          confirmButtonText: '確定'
        })
      }
    },
    async addReply(comment) {
      if (!comment.replyText.trim()) {
        Swal.fire({
          icon: 'warning',
          title: '請輸入回覆內容',
          confirmButtonText: '確定'
        })
        return
      }
      
      try {
        const replyData = {
          content: comment.replyText,
          user_name: '店家',
          user_id: 0,
          avatar: 'shop.png'
        }
        
        const response = await messageAPI.addReply(comment.id, replyData)
        comment.replyText = ''
        // 直接更新本地數據
        const commentIndex = this.comments.findIndex(c => c.id === comment.id)
        if (commentIndex !== -1) {
          if (!this.comments[commentIndex].replies) {
            this.comments[commentIndex].replies = []
          }
          // 添加新回覆到列表
          this.comments[commentIndex].replies.push({
            id: response.data.replies[response.data.replies.length - 1].id,
            content: replyData.content,
            user_name: replyData.user_name,
            create_time: new Date().toISOString().replace('T', ' ').split('.')[0]
          })
        }
        Swal.fire({
          icon: 'success',
          title: '回覆成功',
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000
        })
      } catch (error) {
        console.error('添加回覆失敗:', error)
        Swal.fire({
          icon: 'error',
          title: '回覆失敗',
          text: error.response?.data?.message || '請稍後再試',
          confirmButtonText: '確定'
        })
      }
    }
  },
  mounted() {
    this.fetchComments()
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