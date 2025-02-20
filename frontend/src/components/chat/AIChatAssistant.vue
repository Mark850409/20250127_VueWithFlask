<template>
  <div class="chatbot fixed bottom-4 right-4 z-[9999]">
    <!-- 聊天氣泡按鈕 - 始終顯示 -->
    <button @click="toggleChat" :class="[
      'toggleChat w-14 h-14 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full shadow-lg flex items-center justify-center text-white hover:shadow-xl transition-all duration-200',
      isOpen ? 'opacity-50' : 'transform hover:-translate-y-1'
    ]">
      <i class="fas fa-robot text-2xl"></i>
    </button>

    <!-- 沉浸式聊天頁面 -->
    <div v-if="isFullscreen"
      class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/20 backdrop-blur-sm">
      <div class="w-[80%] h-[80%] bg-white dark:bg-gray-900 rounded-2xl shadow-2xl flex flex-col 
                  transform transition-all duration-300 ease-out animate-chat-window">
        <!-- 頂部導航欄 -->
        <div class="flex items-center justify-between px-6 py-4 border-b dark:border-gray-800 rounded-t-2xl">
          <div class="flex items-center space-x-3">
            <i class="fas fa-robot text-2xl text-indigo-500"></i>
            <h2 class="text-xl font-semibold dark:text-white">AI小助手</h2>
          </div>
          <div class="flex items-center gap-2">
            <!-- 清除歷史按鈕 -->
            <button @click="clearHistory"
                    class="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-colors"
                    title="清除歷史對話">
              <i class="fas fa-trash-alt text-gray-600 dark:text-gray-400"></i>
            </button>
            <!-- 關閉按鈕 -->
            <button @click="toggleFullscreen"
                    class="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-colors"
                    title="關閉視窗">
              <i class="fas fa-times text-gray-600 dark:text-gray-400 text-xl"></i>
            </button>
          </div>
        </div>

        <!-- 聊天內容區域 -->
        <div class="flex-1 overflow-y-auto p-6" ref="fullscreenChatContainer">
          <div class="max-w-3xl mx-auto">
            <!-- 快速提問區塊 -->
            <div v-if="quickQuestions.length > 0" class="mb-8 bg-gray-50 dark:bg-gray-800/50 rounded-xl p-4">
              <div class="flex items-center justify-between mb-3">
                <div class="text-base font-medium text-gray-700 dark:text-gray-300">
                  快速提問
                </div>
                <button @click="toggleQuickQuestions"
                  class="text-gray-500 dark:text-gray-400 hover:text-indigo-500 dark:hover:text-indigo-400 transition-colors">
                  <i :class="['fas', isQuickQuestionsOpen ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                </button>
              </div>
              <div v-show="isQuickQuestionsOpen"
                class="grid grid-cols-1 sm:grid-cols-2 gap-2 transition-all duration-300"
                :class="{ 'opacity-0 h-0': !isQuickQuestionsOpen, 'opacity-100': isQuickQuestionsOpen }">
                <button v-for="question in quickQuestions" :key="question.id" @click="handleQuickQuestion(question)"
                  class="flex items-center space-x-2 px-4 py-2 text-left bg-white dark:bg-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors">
                  <i v-if="question.icon" :class="[question.icon, 'text-indigo-500 dark:text-indigo-400']">
                  </i>
                  <span class="text-gray-700 dark:text-gray-200">{{ question.title }}</span>
                </button>
              </div>
            </div>

            <div v-for="(message, index) in chatHistory" :key="index" class="mb-6">
              <!-- 用戶訊息 -->
              <div v-if="message.isUser" class="flex justify-end">
                <div class="flex items-end space-x-2">
                  <div class="max-w-xl bg-indigo-500 text-white px-6 py-3 rounded-2xl rounded-br-sm">
                    {{ message.content }}
                  </div>
                  <div class="w-10 h-10 rounded-full bg-indigo-500 flex items-center justify-center text-white">
                    <i class="fas fa-user"></i>
                  </div>
                </div>
              </div>
              <!-- AI 回應 -->
              <div v-else class="flex justify-start">
                <div class="flex items-start space-x-2">
                  <div
                    class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-indigo-500">
                    <i class="fas fa-robot"></i>
                  </div>
                  <div
                    class="max-w-xl bg-gray-50 dark:bg-gray-800/50 text-gray-800 dark:text-gray-200 px-6 py-4 rounded-xl shadow-sm">
                    <div v-if="message.content" class="space-y-3">
                      <!-- 一般文字內容 -->
                      <template v-if="!message.content.includes('★')">
                        <div class="text-base text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap">
                          {{ message.content }}
                        </div>
                      </template>

                      <!-- 結構化回答 -->
                      <template v-else>
                        <template v-for="(part, idx) in message.content.split('★').filter(Boolean)" :key="idx">
                          <!-- 答案區塊 -->
                          <template v-if="part.includes('答案：')">
                            <div class="space-y-2">
                              <div class="font-medium text-gray-900">★ 答案：</div>
                              <div class="text-gray-700 whitespace-pre-wrap">
                                {{ part.replace('答案：', '').trim() }}
                              </div>
                            </div>
                          </template>

                          <!-- 其他內容區塊 -->
                          <template v-else-if="!part.includes('資料來源：')">
                            <div class="border-t border-gray-200 my-4"></div>
                            <div class="text-gray-700 whitespace-pre-wrap mt-4">
                              {{ part.trim() }}
                            </div>
                          </template>

                          <!-- 資料來源區塊 -->
                          <template v-else>
                            <div class="border-t border-gray-200 my-4"></div>
                            <div class="text-sm text-gray-500">
                              ★ {{ part.trim() }}
                            </div>
                          </template>
                        </template>
                      </template>
                    </div>
                    <div v-else class="flex items-center space-x-2">
                      <div class="typing-dots">
                        <span></span><span></span><span></span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 底部輸入區域 -->
        <div class="border-t dark:border-gray-800 p-6 rounded-b-2xl">
          <div class="max-w-3xl mx-auto flex gap-4">
            <input v-model="userInput" @keyup.enter="sendMessage" type="text"
              class="fullscreen-input flex-1 px-6 py-3 bg-gray-100 dark:bg-gray-800 border-0 rounded-full focus:ring-2 focus:ring-indigo-500 dark:text-white"
              placeholder="請輸入您的問題...">
            <button @click="sendMessage" :disabled="isLoading"
              class="px-6 py-3 bg-indigo-500 text-white rounded-full hover:bg-indigo-600 disabled:bg-gray-400 transition-colors">
              <i :class="['fas', isLoading ? 'fa-spinner fa-spin' : 'fa-paper-plane']"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 聊天視窗 -->
    <div v-show="isOpen" class="absolute bottom-20 right-0 w-96 bg-white dark:bg-gray-800 rounded-lg shadow-xl animate-fade-in z-[9999]">
      <!-- 聊天視窗標題 -->
      <div
        class="chatbot-title flex justify-between items-center p-4 border-b bg-gradient-to-r from-blue-500 to-blue-600 rounded-t-lg">
        <div class="flex items-center">
          <i class="fas fa-robot text-white mr-2"></i>
          <h3 class="font-semibold text-white">AI小助手</h3>
        </div>
        <div class="flex items-center gap-2">
          <!-- 全螢幕按鈕 -->
          <button @click="toggleFullscreen"
            class="text-white hover:text-gray-200 w-8 h-8 flex items-center justify-center rounded-full hover:bg-blue-700 transition-colors"
            title="全螢幕模式">
            <i class="fas fa-expand-arrows-alt text-lg"></i>
          </button>
          <!-- 清除歷史按鈕 -->
          <button @click="clearHistory"
            class="text-white hover:text-gray-200 w-8 h-8 flex items-center justify-center rounded-full hover:bg-blue-700 transition-colors"
            title="清除歷史對話">
            <i class="fas fa-trash-alt"></i>
          </button>
          <!-- 關閉按鈕 -->
          <button @click="toggleChat"
            class="text-white hover:text-gray-200 w-8 h-8 flex items-center justify-center rounded-full hover:bg-blue-700 transition-colors">
            <i class="fas fa-times"></i>
          </button>
        </div>
      </div>

      <!-- 聊天內容區域 -->
      <div class="flex flex-col h-96">
        <!-- 聊天訊息列表 -->
        <div class="flex-1 p-4 overflow-y-auto" ref="chatContainer">
          <div v-for="(message, index) in chatHistory" :key="index" class="mb-4">
            <!-- 用戶訊息 -->
            <div v-if="message.isUser" class="flex justify-end">
              <div class="flex items-end space-x-2">
                <div class="max-w-[70%] bg-indigo-500 text-white px-4 py-2 rounded-2xl rounded-br-sm">
                  {{ message.content }}
                </div>
                <div class="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center text-white text-sm">
                  <i class="fas fa-user"></i>
                </div>
              </div>
            </div>
            <!-- AI 回應 -->
            <div v-else class="flex justify-start">
              <div class="flex items-start space-x-2">
                <div class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-indigo-500">
                  <i class="fas fa-robot"></i>
                </div>
                <div class="max-w-[70%] bg-gray-50 text-gray-800 px-4 py-2 rounded-xl">
                  <div v-if="message.content" class="space-y-3">
                    <!-- 一般文字內容 -->
                    <template v-if="!message.content.includes('★')">
                      <div class="text-base text-gray-700 leading-relaxed whitespace-pre-wrap">
                        {{ message.content }}
                      </div>
                    </template>

                    <!-- 結構化回答 -->
                    <template v-else>
                      <template v-for="(part, idx) in message.content.split('★').filter(Boolean)" :key="idx">
                        <!-- 答案區塊 -->
                        <template v-if="part.includes('答案：')">
                          <div class="space-y-2">
                            <div class="font-medium text-gray-900">★ 答案：</div>
                            <div class="text-gray-700 whitespace-pre-wrap">
                              {{ part.replace('答案：', '').trim() }}
                            </div>
                          </div>
                        </template>

                        <!-- 其他內容區塊 -->
                        <template v-else-if="!part.includes('資料來源：')">
                          <div class="border-t border-gray-200 my-4"></div>
                          <div class="text-gray-700 whitespace-pre-wrap mt-4">
                            {{ part.trim() }}
                          </div>
                        </template>

                        <!-- 資料來源區塊 -->
                        <template v-else>
                          <div class="border-t border-gray-200 my-4"></div>
                          <div class="text-sm text-gray-500">
                            ★ {{ part.trim() }}
                          </div>
                        </template>
                      </template>
                    </template>
                  </div>
                  <div v-else class="flex items-center space-x-2">
                    <div class="typing-dots">
                      <span></span><span></span><span></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 快速問答區塊 -->
        <div v-if="quickQuestions.length > 0" class="quick-section p-3 border-t border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50">
          <div class="flex items-center justify-between mb-2 px-2">
            <div class="text-sm font-medium text-gray-600 dark:text-gray-300">
              快速問答：
            </div>
            <button @click="toggleQuickQuestions"
              class="text-gray-500 dark:text-gray-400 hover:text-blue-500 dark:hover:text-blue-400 transition-colors duration-200">
              <i :class="['fas', isQuickQuestionsOpen ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
            </button>
          </div>
          <div v-show="isQuickQuestionsOpen"
            class="overflow-x-auto whitespace-nowrap pb-2 transition-all duration-300 custom-scrollbar"
            :class="{ 'opacity-0 h-0': !isQuickQuestionsOpen, 'opacity-100 h-auto': isQuickQuestionsOpen }">
            <div class="flex gap-2">
              <button v-for="question in quickQuestions" :key="question.id"
                class="flex-none px-4 py-2 bg-white dark:bg-gray-600 rounded-lg border border-gray-200 dark:border-gray-500 hover:bg-gray-50 dark:hover:bg-gray-500 transition-colors text-sm text-gray-700 dark:text-gray-200 flex items-center gap-2"
                @click="handleQuickQuestion(question)">
                <i v-if="question.icon" :class="[question.icon, 'text-indigo-500 dark:text-indigo-400']"></i>
                {{ question.title }}
              </button>
            </div>
          </div>
        </div>

        <!-- 輸入區域 -->
        <div class="p-4 border-t border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-800 chatbot-input">
          <div class="flex gap-2">
            <input v-model="userInput" @keyup.enter="sendMessage" type="text"
              class="chatbot-input flex-1 px-4 py-2 border border-gray-200 dark:border-gray-600 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              placeholder="請輸入您的問題...">
            <button @click="sendMessage" :disabled="isLoading"
              class="chatbot-btn px-4 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 disabled:bg-gray-400 transition-colors duration-200">
              <i :class="['fas', isLoading ? 'fa-spinner fa-spin' : 'fa-paper-plane']"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, watch } from 'vue'
import { botAPI } from '@/api'

export default {
  name: 'AIChatAssistant',
  setup() {
    const isOpen = ref(false)
    const isFullscreen = ref(false)
    const userInput = ref('')
    const chatHistory = ref([])
    const isLoading = ref(false)
    const chatContainer = ref(null)
    const fullscreenChatContainer = ref(null)
    const isQuickQuestionsOpen = ref(true)

    // 快速提問選項
    const quickQuestions = ref([])

    const defaultMessage = {
      content: `您好！我是您的 AI小助手。我可以：
1. 協助您了解平台功能與操作方式
2. 提供專業的數據分析建議
請問有什麼我可以幫您的嗎？`,
      isUser: false
    }

    // 初始化聊天歷史
    chatHistory.value = [defaultMessage]

    // 切換聊天視窗
    const toggleChat = () => {
      isOpen.value = !isOpen.value
      // 關閉時清空輸入框
      if (!isOpen.value) {
        userInput.value = ''
      }
    }

    // 切換快速問答選單
    const toggleQuickQuestions = () => {
      isQuickQuestionsOpen.value = !isQuickQuestionsOpen.value
    }

    // 處理快速提問
    const handleQuickQuestion = async (question) => {
      // 將問題內容填入輸入框
      userInput.value = question.message || question.title
      // 聚焦輸入框
      const inputElement = document.querySelector('.chatbot-input input, .fullscreen-input input')
      if (inputElement) {
        inputElement.focus()
      }
    }

    // 監聽聊天記錄變化
    watch(chatHistory, () => {
      nextTick(() => {
        // 滾動到底部
        if (chatContainer.value) {
          chatContainer.value.scrollTop = chatContainer.value.scrollHeight
        }
        if (fullscreenChatContainer.value) {
          fullscreenChatContainer.value.scrollTop = fullscreenChatContainer.value.scrollHeight
        }
      })
    }, { deep: true })

    // 發送訊息到 Langflow API
    const sendMessage = async () => {
      if (!userInput.value.trim() || isLoading.value) return

      const message = userInput.value
      chatHistory.value.push({
        content: message,
        isUser: true
      })

      // 添加 AI 思考中的佔位訊息
      chatHistory.value.push({
        content: '',
        isUser: false
      })

      userInput.value = ''
      isLoading.value = true
      console.log(message)

      // 提取請求體為單獨的變數
      const requestBody = {
        input_value: message,
        output_type: 'chat',
        input_type: 'chat'
      }

      try {
        const response = await fetch(
          import.meta.env.VITE_LANGFLOW_API_URL,
          {
            method: 'POST',
            headers: {
              'Authorization': 'Bearer ' + import.meta.env.VITE_LANGFLOW_AUTH_TOKEN,
              'Content-Type': 'application/json',
              'x-api-key': import.meta.env.VITE_LANGFLOW_API_KEY
            },
            body: JSON.stringify(requestBody)
          }
        )

        const data = await response.json()
        console.log('Langflow response:', data)

        // 檢查是否有錯誤
        if (data.error) {
          throw new Error(data.error)
        }

        // 嘗試從不同可能的路徑獲取回應
        const botResponse = data.result?.output ||
          data.result?.response ||
          data.outputs?.[0]?.output ||
          data.outputs?.[0]?.outputs?.[0]?.artifacts?.message ||
          '抱歉，我無法理解您的問題。'

        // 更新最後一條 AI 訊息
        chatHistory.value[chatHistory.value.length - 1].content = botResponse

      } catch (error) {
        console.error('API 請求失敗:', error)
        chatHistory.value[chatHistory.value.length - 1].content = '抱歉，我現在無法回應。請稍後再試。'
      } finally {
        isLoading.value = false
      }
    }

    // 獲取預設訊息
    const fetchDefaultMessage = async () => {
      try {
        const response = await botAPI.getBots({
          is_active: false,
          is_default: true
        })
        const data = response.data.bots
        if (data && data.length > 0) {
          defaultMessage.content = data[0].message
          chatHistory.value = [defaultMessage]
        }
      } catch (error) {
        console.error('獲取預設訊息失敗:', error)
      }
    }

    // 獲取快速問答
    const fetchQuickQuestions = async () => {
      try {
        const response = await botAPI.getBots({
          is_active: true,
          is_default: false
        })
        const data = response.data.bots
        if (data) {
          quickQuestions.value = data.map(item => ({
            id: item.id,
            title: item.title,
            message: item.message,
            icon: item.icon
          }))
        }
      } catch (error) {
        console.error('獲取快速問答失敗:', error)
      }
    }

    // 清除歷史對話
    const clearHistory = () => {
      // 保留預設歡迎訊息
      chatHistory.value = [defaultMessage]
      // 重置輸入框
      userInput.value = ''
    }

    // 組件掛載時獲取數據
    onMounted(() => {
      fetchDefaultMessage()
      fetchQuickQuestions()
    })

    // 切換全螢幕模式
    const toggleFullscreen = () => {
      isFullscreen.value = !isFullscreen.value
      if (isFullscreen.value) {
        isOpen.value = false
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = ''
        // 關閉全螢幕時清空輸入框
        userInput.value = ''
      }
    }

    return {
      isOpen,
      isFullscreen,
      userInput,
      chatHistory,
      isLoading,
      chatContainer,
      fullscreenChatContainer,
      isQuickQuestionsOpen,
      toggleChat,
      toggleFullscreen,
      sendMessage,
      toggleQuickQuestions,
      handleQuickQuestion,
      clearHistory,
      quickQuestions
    }
  }
}
</script>

<style scoped>
/* 自定義捲動軸樣式 */
.custom-scrollbar::-webkit-scrollbar {
  height: 6px;
  background-color: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(203, 213, 225, 0.5);
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(203, 213, 225, 0.8);
}

/* Firefox 捲動軸樣式 */
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: rgba(203, 213, 225, 0.5) transparent;
}

.chat-container::-webkit-scrollbar {
  width: 4px;
}

/* 添加訊息動畫 */
.message-enter-active,
.message-leave-active {
  transition: all 0.3s ease;
}

.message-enter-from,
.message-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 添加淡入動畫 */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}

/* 添加彈跳動畫 */
@keyframes bounce {

  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-5px);
  }
}

button:hover .fas.fa-robot {
  animation: bounce 1s infinite;
}

/* 添加打字動畫樣式 */
.typing-dots {
  display: flex;
  align-items: center;
  column-gap: 4px;
  padding: 4px 0;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  background-color: #93c5fd;
  border-radius: 50%;
  animation: typing 1s infinite ease-in-out;
}

.typing-dots span:nth-child(1) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.4s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.6s;
}

@keyframes typing {

  0%,
  100% {
    transform: scale(1);
    opacity: 0.4;
  }

  50% {
    transform: scale(1.2);
    opacity: 1;
  }
}

/* 添加平滑滾動效果 */
.overflow-y-auto {
  scroll-behavior: smooth;
}

/* 添加摺疊動畫 */
.h-0 {
  margin: 0;
  padding-top: 0;
  padding-bottom: 0;
}

/* 確保過渡效果平滑 */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

.quick-questions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  overflow: hidden;
  padding-bottom: 0.5rem;
}

.quick-questions-list.h-0 {
  padding: 0;
  margin: 0;
}

.quick-question-btn {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  background-color: white;
  color: #4a5568;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.quick-question-btn:hover {
  background-color: #f7fafc;
  border-color: #cbd5e0;
}

.quick-question-btn i {
  font-size: 1rem;
}

.break-words {
  white-space: pre-wrap;
  word-break: break-word;
}

/* 添加垃圾桶按鈕動畫 */
.fa-trash-alt {
  transition: transform 0.2s ease;
}

button:hover .fa-trash-alt {
  transform: scale(1.1);
}

/* 大視窗展開動畫 */
@keyframes chat-window {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }

  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.animate-chat-window {
  animation: chat-window 0.3s ease-out forwards;
}

/* 背景模糊淡入效果 */
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}
</style>