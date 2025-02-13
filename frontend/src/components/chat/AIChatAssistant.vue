<template>
  <div class="fixed bottom-4 right-4">
    <!-- 聊天氣泡按鈕 - 始終顯示 -->
    <button @click="toggleChat"
            :class="[
              'w-14 h-14 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full shadow-lg flex items-center justify-center text-white hover:shadow-xl transition-all duration-200',
              isOpen ? 'opacity-50' : 'transform hover:-translate-y-1'
            ]">
      <i class="fas fa-robot text-2xl"></i>
    </button>

    <!-- 聊天視窗 -->
    <div v-show="isOpen" 
         class="absolute bottom-20 right-0 w-96 bg-white rounded-lg shadow-xl animate-fade-in">
      <!-- 聊天視窗標題 -->
      <div class="flex justify-between items-center p-4 border-b bg-gradient-to-r from-blue-500 to-blue-600 rounded-t-lg">
        <div class="flex items-center">
          <i class="fas fa-robot text-white mr-2"></i>
          <h3 class="font-semibold text-white">AI小助手</h3>
        </div>
        <div class="flex items-center gap-2">
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
          <div v-for="(message, index) in chatHistory" 
               :key="index" 
               class="mb-4">
            <!-- 用戶訊息 -->
            <div v-if="message.isUser" class="flex justify-end">
              <div class="flex items-end space-x-2">
                <div class="max-w-[70%] bg-blue-500 text-white px-4 py-2 rounded-2xl rounded-br-sm">
                  {{ message.content }}
                </div>
                <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm">
                  <i class="fas fa-user"></i>
                </div>
              </div>
            </div>
            <!-- AI 回應 -->
            <div v-else class="flex justify-start">
              <div class="flex items-end space-x-2">
                <div class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-blue-500">
                  <i class="fas fa-robot"></i>
                </div>
                <div class="max-w-[70%] bg-gray-100 text-gray-800 px-4 py-2 rounded-2xl rounded-bl-sm">
                  <div v-if="message.content" class="break-words" v-html="message.content">
                  </div>
                  <div v-else class="flex items-center space-x-2">
                    <div class="typing-dots">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 快速問答區塊 -->
        <div class="p-3 border-t border-gray-100 bg-gray-50">
          <div class="flex items-center justify-between mb-2 px-2">
            <div class="text-sm font-medium text-gray-600">
              快速問答：
            </div>
            <button @click="toggleQuickQuestions" 
                    class="text-gray-500 hover:text-blue-500 transition-colors duration-200">
              <i :class="['fas', isQuickQuestionsOpen ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
            </button>
          </div>
          <div v-show="isQuickQuestionsOpen" 
               class="quick-questions-list transition-all duration-300"
               :class="{ 'opacity-0 h-0': !isQuickQuestionsOpen, 'opacity-100 h-auto': isQuickQuestionsOpen }">
            <button 
              v-for="question in quickQuestions" 
              :key="question.id"
              class="quick-question-btn"
              @click="handleQuickQuestion(question.title)"
            >
              <i v-if="question.icon" :class="question.icon"></i>
              {{ question.title }}
            </button>
          </div>
        </div>

        <!-- 輸入區域 -->
        <div class="p-4 border-t bg-white">
          <div class="flex gap-2">
            <input v-model="userInput"
                   @keyup.enter="sendMessage"
                   type="text"
                   placeholder="請輸入您的問題..."
                   class="flex-1 px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            <button @click="sendMessage"
                    :disabled="isLoading"
                    class="px-4 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 disabled:bg-gray-400 transition-colors duration-200">
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
import axios from 'axios'

export default {
  name: 'AIChatAssistant',
  setup() {
    const isOpen = ref(false)
    const userInput = ref('')
    const chatHistory = ref([])
    const isLoading = ref(false)
    const chatContainer = ref(null)
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
    }

    // 切換快速問答選單
    const toggleQuickQuestions = () => {
      isQuickQuestionsOpen.value = !isQuickQuestionsOpen.value
    }

    // 處理快速提問
    const handleQuickQuestion = (question) => {
      userInput.value = question
      sendMessage()
    }

    // 監聽聊天歷史變化，自動滾動到底部
    watch(() => chatHistory.value.length, async () => {
      await nextTick()
      scrollToBottom()
    })

    // 滾動到底部的函數
    const scrollToBottom = () => {
      if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight
      }
    }

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
        input_type: 'chat',
        tweaks: {
          "ChatInput-lg44S": {
            "background_color": "",
            "chat_icon": "",
            "files": "",
            "sender": "User",
            "sender_name": "User",
            "session_id": "",
            "should_store_message": true,
            "text_color": ""
          },
          "Prompt-EF0ZF": {
            "context": message,
            "question": message,
            "template": "{context}\n\n---\n\nGiven the context above, answer the question as best as possible.\n\nQuestion: {question}\n\nAnswer: "
          },
          "OpenAIModel-7rz2d": {
            "api_key": import.meta.env.VITE_OPENAI_API_KEY,
            "model_name": "gpt-4o-mini",
            "system_message": "你是一個AI助手，請回答用戶的問題。",
            "temperature": 0.5
          },
          "Chroma-B2dAI": {
            "collection_name": "myai",
            "number_of_results": 10,
            "persist_directory": "ai_0119_4",
            "search_query": message,
            "search_type": "Similarity"
          },
          "ParseData-vPZnv": {
            "sep": "\n",
            "template": "{text}"
          },
          "SplitText-nwhoY": {
            "chunk_overlap": 200,
            "chunk_size": 1000,
            "separator": "\n"
          },
          "ChatOutput-J5E4r": {
            "background_color": "",
            "chat_icon": "",
            "data_template": "{text}",
            "input_value": "",
            "sender": "Machine",
            "sender_name": "AI",
            "session_id": "",
            "should_store_message": true,
            "text_color": ""
          },
          "OpenAIEmbeddings-fk8d2": {
            "chunk_size": 1000,
            "client": "",
            "default_headers": {},
            "default_query": {},
            "deployment": "",
            "dimensions": null,
            "embedding_ctx_length": 1536,
            "max_retries": 3,
            "model": "text-embedding-3-small",
            "model_kwargs": {},
            "openai_api_base": "",
            "openai_api_key": import.meta.env.VITE_OPENAI_API_KEY,
            "openai_api_type": "",
            "openai_api_version": "",
            "openai_organization": "",
            "openai_proxy": "",
            "request_timeout": null,
            "show_progress_bar": false,
            "skip_empty": false,
            "tiktoken_enable": true,
            "tiktoken_model_name": ""
          },
          "OpenAIEmbeddings-qricR": {
            "chunk_size": 1000,
            "client": "",
            "default_headers": {},
            "default_query": {},
            "deployment": "",
            "dimensions": null,
            "embedding_ctx_length": 1536,
            "max_retries": 3,
            "model": "text-embedding-3-small",
            "model_kwargs": {},
            "openai_api_base": "",
            "openai_api_key": import.meta.env.VITE_OPENAI_API_KEY,
            "openai_api_type": "",
            "openai_api_version": "",
            "openai_organization": "",
            "openai_proxy": "",
            "request_timeout": null,
            "show_progress_bar": false,
            "skip_empty": false,
            "tiktoken_enable": true,
            "tiktoken_model_name": ""
          },
          "Directory-02blE": {
            "depth": 0,
            "load_hidden": false,
            "max_concurrency": 2,
            "path": "/root/.cache/langflow/ae94aa3d-ca48-4d32-afca-3913d1f1669c/",
            "recursive": false,
            "silent_errors": false,
            "types": "",
            "use_multithreading": false
          },
          "Chroma-kMCGf": {
            "allow_duplicates": false,
            "chroma_server_cors_allow_origins": "",
            "chroma_server_grpc_port": null,
            "chroma_server_host": "",
            "chroma_server_http_port": null,
            "chroma_server_ssl_enabled": false,
            "collection_name": "myai",
            "limit": null,
            "number_of_results": 10,
            "persist_directory": "ai_0119_4",
            "search_query": message,
            "search_type": "Similarity"
          }
        }
      }

      try {
        const response = await fetch(
          import.meta.env.VITE_LANGFLOW_API_URL,
          {
            method: 'POST',
            headers: {
              'Authorization': 'Bearer '+ import.meta.env.VITE_LANGFLOW_AUTH_TOKEN,
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
        const response = await fetch(
          'http://localhost:5000/api/bots/?is_active=true&is_default=true',
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            }
          }
        )
        
        if (!response.ok) {
          throw new Error('獲取預設訊息失敗')
        }
        
        const data = await response.json()
        if (data.bots && data.bots.length > 0) {
          // 設置預設訊息
          chatHistory.value = [{
            content: data.bots[0].message || defaultMessage.content,
            isUser: false
          }]
        }
      } catch (error) {
        console.error('獲取預設訊息錯誤:', error)
      }
    }

    // 獲取快速問答列表
    const fetchQuickQuestions = async () => {
      try {
        const response = await fetch(
          'http://localhost:5000/api/bots/?is_active=true&is_default=false',
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            }
          }
        )
        
        if (!response.ok) {
          throw new Error('獲取快速問答失敗')
        }
        
        const data = await response.json()
        quickQuestions.value = data.bots
      } catch (error) {
        console.error('獲取快速問答錯誤:', error)
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

    return {
      isOpen,
      userInput,
      chatHistory,
      isLoading,
      chatContainer,
      quickQuestions,
      isQuickQuestionsOpen,
      toggleChat,
      sendMessage,
      handleQuickQuestion,
      toggleQuickQuestions,
      clearHistory
    }
  }
}
</script>

<style scoped>
.chat-container::-webkit-scrollbar {
  width: 4px;
}

.chat-container::-webkit-scrollbar-track {
  background: transparent;
}

.chat-container::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 2px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}

/* 添加訊息動畫 */
.message-enter-active, .message-leave-active {
  transition: all 0.3s ease;
}

.message-enter-from, .message-leave-to {
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
  0%, 100% {
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
  0%, 100% {
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
</style> 