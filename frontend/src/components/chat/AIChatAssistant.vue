<template>
  <div class="chatbot fixed bottom-4 right-4 z-[9999]">
    <!-- 聊天氣泡按鈕 - 始終顯示 -->
    <button @click="toggleChat" :class="[
      'toggleChat w-14 h-14 bg-gradient-to-r from-blue-400 to-indigo-400 rounded-full shadow-lg flex items-center justify-center text-white hover:shadow-xl transition-all duration-200 relative',
      isOpen ? 'opacity-50' : 'transform hover:-translate-y-1'
    ]">
      <i :class="['text-2xl', isOpen ? 'fas fa-times' : 'fas fa-robot']"></i>
      
      <!-- 思考狀態指示器 - 優雅樣式 -->
      <div v-if="isDeepReasoningEnabled" class="absolute -top-1 -right-1 flex items-center justify-center">
        <div class="pulse-ring"></div>
        <div class="w-5 h-5 rounded-full bg-gradient-to-r from-indigo-500 to-blue-500 flex items-center justify-center shadow-md">
          <i class="fas fa-brain text-[10px] text-white"></i>
        </div>
      </div>
    </button>

    <!-- 沉浸式聊天頁面 -->
    <div v-if="isFullscreen"
      class="fixed inset-0 z-[9999] flex items-center justify-center bg-white dark:bg-gray-900">
      <div class="w-full h-full flex flex-col transform transition-all duration-300 ease-out">
        <!-- 頂部導航欄 - 白色背景 -->
        <div class="flex items-center justify-between px-6 py-4 border-b dark:border-gray-800 bg-white">
          <div class="flex items-center space-x-3">
            <i class="fas fa-robot text-2xl text-blue-400"></i>
            <h2 class="text-xl font-semibold text-blue-500">AI小助手</h2>
          </div>
          <div class="flex items-center gap-3">
            <!-- 清除歷史按鈕 -->
            <button @click="clearHistory"
                    class="p-2 hover:bg-gray-100 rounded-full transition-colors"
                    title="清除歷史對話">
              <i class="fas fa-trash-alt text-blue-400"></i>
            </button>
            <!-- 關閉按鈕 -->
            <button @click="toggleFullscreen"
                    class="p-2 hover:bg-gray-100 rounded-full transition-colors"
                    title="關閉全螢幕">
              <i class="fas fa-times text-blue-400 text-xl"></i>
            </button>
          </div>
        </div>

        <!-- 聊天內容區域 -->
        <div class="flex-1 overflow-y-auto p-4 md:p-6" ref="fullscreenChatContainer">
          <div class="max-w-4xl mx-auto">
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
                class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2 transition-all duration-300"
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
                  <div class="max-w-[70%] bg-blue-400 text-white px-4 py-2 rounded-2xl rounded-br-sm">
                    <!-- 處理圖片和文字組合的訊息 -->
                    <template v-if="message.type === 'image_with_text'">
                      <div class="space-y-2">
                        <div class="relative w-full">
                          <img 
                            :src="message.content.image" 
                            class="w-full max-h-[300px] object-contain rounded-lg cursor-pointer hover:opacity-90 transition-opacity bg-white/50"
                            @click="previewStoredImage(message.content.image)"
                            alt="用戶上傳的圖片"
                          >
                        </div>
                        <div class="text-white mt-2">
                          {{ message.content.text }}
                        </div>
                      </div>
                    </template>
                    <!-- 處理純文字訊息 -->
                    <template v-else>
                      {{ message.content }}
                    </template>
                  </div>
                  <div class="relative">
                    <div class="w-10 h-10 rounded-full bg-blue-400 flex items-center justify-center text-white text-sm">
                      <i class="fas fa-user"></i>
                    </div>
                  </div>
                </div>
              </div>
              <!-- AI 回應 -->
              <div v-else class="flex justify-start">
                <div class="flex items-start space-x-2">
                  <div class="relative">
                    <div class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-indigo-500">
                      <i class="fas fa-robot"></i>
                    </div>
                  </div>
                  <!-- 如果有內容，顯示聊天氣泡 -->
                  <div v-if="message.content || message.toolInfo || message.generatedImage || (message.hasDeepReasoning && message.reasoningProcess)" class="max-w-2xl bg-gray-50 dark:bg-gray-800 text-gray-800 dark:text-gray-200 px-6 py-4 rounded-xl shadow-sm">
                    <!-- 工具調用信息 -->
                    <div v-if="message.toolInfo" 
                         class="mb-4 bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-100 dark:border-blue-800 animate-fade-in">
                      <div class="flex items-center mb-3">
                        <div class="w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center text-white">
                          <i class="fas fa-tools text-xs"></i>
                        </div>
                        <div class="ml-2">
                          <div class="text-sm font-medium text-blue-700 dark:text-blue-300">工具調用</div>
                          <div class="text-xs text-blue-600 dark:text-blue-400 font-mono">{{ message.toolInfo.name }}</div>
                        </div>
                      </div>
                      
                      <div class="mt-3">
                        <div class="text-xs font-medium text-blue-700 dark:text-blue-300 mb-2">參數：</div>
                        <div class="text-xs text-gray-600 dark:text-gray-400 font-mono bg-white/80 dark:bg-gray-800/80 p-3 rounded-lg border border-blue-100/60 dark:border-blue-800/60 overflow-x-auto">
                          <pre class="whitespace-pre-wrap break-words">{{ formatToolArguments(message.toolInfo.arguments) }}</pre>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 生成的圖片 -->
                    <div v-if="message.generatedImage" 
                         class="mb-4 bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg border border-purple-100 dark:border-purple-800 animate-fade-in-delay">
                      <div class="text-sm font-medium text-purple-700 dark:text-purple-300 mb-3">生成的圖片：</div>
                      <div class="flex justify-center">
                        <a :href="message.generatedImage" target="_blank" class="block hover:opacity-90 transition-opacity">
                          <img :src="message.generatedImage" class="max-w-full h-auto rounded-lg shadow-md cursor-pointer max-h-96 object-contain" alt="AI生成的圖片">
                        </a>
                      </div>
                    </div>
                    
                    <!-- 深度推理模式的回應 -->
                    <template v-if="message.hasDeepReasoning">
                      <div class="space-y-4">
                        <!-- 顯示推理過程 -->
                        <div v-if="message.reasoningProcess" class="bg-gradient-to-r from-indigo-50 to-blue-50 dark:from-indigo-900/20 dark:to-blue-900/10 p-5 rounded-lg border border-indigo-100 dark:border-indigo-800 mt-2 shadow-sm">
                          <div class="flex items-center mb-3">
                            <div class="w-8 h-8 rounded-full bg-gradient-to-r from-indigo-500 to-blue-500 flex items-center justify-center text-white shadow-md">
                              <i class="fas fa-brain"></i>
                            </div>
                            <div class="ml-3">
                              <div class="text-sm font-medium text-indigo-700 dark:text-indigo-300">推理過程</div>
                              <div class="text-xs text-indigo-500 dark:text-indigo-400">AI 的思考邏輯</div>
                            </div>
                          </div>
                          
                          <div class="relative">
                            <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-gradient-to-b from-indigo-300 to-blue-300 dark:from-indigo-700 dark:to-blue-700"></div>
                            
                            <div class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap font-mono pl-8 pr-4 py-3 bg-white/70 dark:bg-gray-800/70 rounded-lg backdrop-blur-sm overflow-auto max-h-80 leading-relaxed border border-indigo-100/60 dark:border-indigo-800/60">
                              {{ message.reasoningProcess }}
                            </div>
                          </div>
                          
                          <div class="mt-3 flex justify-between items-center">
                            <div v-if="message.thinkingTime" class="text-xs text-indigo-500 dark:text-indigo-400 font-medium">
                              <i class="fas fa-clock mr-1"></i> 思考時間: {{ message.thinkingTime }}秒
                            </div>
                            <div class="text-xs text-right text-indigo-400 dark:text-indigo-500 italic">
                              <i class="fas fa-lightbulb mr-1"></i> 深度思考模式
                            </div>
                          </div>
                        </div>
                        
                        <!-- 顯示最終答案 -->
                        <div v-if="message.content" class="bg-gradient-to-r from-emerald-50 to-green-50 dark:from-emerald-900/20 dark:to-green-900/10 p-5 rounded-lg border border-green-100 dark:border-green-800 mt-4 shadow-sm">
                          <div class="flex items-center mb-3">
                            <div class="w-8 h-8 rounded-full bg-gradient-to-r from-emerald-500 to-green-500 flex items-center justify-center text-white shadow-md">
                              <i class="fas fa-lightbulb"></i>
                            </div>
                            <div class="ml-3">
                              <div class="text-sm font-medium text-green-700 dark:text-green-300">最終答案</div>
                              <div class="text-xs text-green-500 dark:text-green-400">思考結果</div>
                            </div>
                          </div>
                          
                          <div class="text-base text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap p-4 bg-white/70 dark:bg-gray-800/70 rounded-lg backdrop-blur-sm border border-green-100/60 dark:border-green-800/60">
                            {{ message.content }}
                          </div>
                        </div>
                      </div>
                    </template>
                    
                    <!-- 一般文字內容 (只有在非深度推理模式下顯示) -->
                    <template v-else-if="message.content">
                      <!-- 結構化回答 -->
                      <template v-if="message.content.includes('★')">
                        <template v-for="(part, idx) in message.content.split('★').filter(Boolean)" :key="idx">
                          <!-- 答案區塊 -->
                          <template v-if="part.includes('答案：')">
                            <div class="space-y-2">
                              <div class="font-medium text-gray-900 dark:text-gray-100">★ 答案：</div>
                              <div class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                                {{ part.replace('答案：', '').trim() }}
                              </div>
                            </div>
                          </template>

                          <!-- 其他內容區塊 -->
                          <template v-else-if="!part.includes('資料來源：') && !part.includes('工具調用：')">
                            <div class="border-t border-gray-200 dark:border-gray-700 my-4"></div>
                            <div class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap mt-4">
                              {{ part.trim() }}
                            </div>
                          </template>

                          <!-- 資料來源區塊 -->
                          <template v-else-if="part.includes('資料來源：')">
                            <div class="border-t border-gray-200 dark:border-gray-700 my-4"></div>
                            <div class="text-sm text-gray-500 dark:text-gray-400">
                              ★ {{ part.trim() }}
                            </div>
                          </template>
                        </template>
                      </template>
                      
                      <!-- 一般文字內容 -->
                      <template v-else>
                        <div class="text-base text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap">
                          {{ message.content }}
                        </div>
                      </template>
                    </template>
                  </div>
                  <!-- 當消息正在加載時，顯示打字指示器 -->
                  <div v-else class="flex items-center justify-center">
                    <div class="thinking-dots">
                      <span></span><span></span><span></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 底部輸入區域 -->
        <div class="border-t dark:border-gray-800 p-4 md:p-6 bg-white dark:bg-gray-900">
          <div class="max-w-4xl mx-auto">
            <!-- 功能開關區域 -->
            <div class="flex items-center justify-end mb-3 space-x-2">
              <!-- 深度推理開關 -->
              <button @click="toggleDeepReasoning"
                :class="[
                  'px-4 py-2 rounded-full flex items-center gap-2 transition-all',
                  isDeepReasoningEnabled 
                    ? 'bg-gradient-to-r from-indigo-500 to-blue-500 text-white shadow-md hover:shadow-lg' 
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                ]">
                <i class="fas fa-brain"></i>
                <span class="text-sm font-medium">深入研究</span>
              </button>
              
              <!-- 網路搜尋開關 -->
              <button @click="toggleWebSearch"
                :class="[
                  'px-4 py-2 rounded-full flex items-center gap-2 transition-all',
                  isWebSearchEnabled 
                    ? 'bg-gradient-to-r from-indigo-500 to-blue-500 text-white shadow-md hover:shadow-lg' 
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                ]">
                <i class="fas fa-search"></i>
                <span class="text-sm font-medium">網路搜尋</span>
              </button>

              <!-- 圖像生成開關 -->
              <button @click="toggleImageGeneration"
                :class="[
                  'px-4 py-2 rounded-full flex items-center gap-2 transition-all',
                  isImageGenerationEnabled 
                    ? 'bg-gradient-to-r from-indigo-500 to-blue-500 text-white shadow-md hover:shadow-lg' 
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                ]">
                <i class="fas fa-image"></i>
                <span class="text-sm font-medium">圖像生成</span>
              </button>
            </div>
            
            <!-- 在輸入區域的 flex 容器中添加圖片上傳按鈕之前，添加預覽區域 -->
            <div class="flex gap-4">
              <!-- 圖片預覽區域 -->
              <div v-if="previewImage" class="w-full flex flex-col items-center mb-4">
                <div class="w-[80%] bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800/50 dark:to-gray-700/50 rounded-xl border border-gray-200/50 dark:border-gray-700/50 backdrop-blur-sm shadow-lg overflow-hidden">
                  <div class="flex items-center justify-between p-3 border-b border-gray-200/50 dark:border-gray-700/50">
                    <div class="flex items-center gap-2">
                      <i class="fas fa-image text-blue-500 dark:text-blue-400"></i>
                      <span class="text-sm font-medium text-gray-700 dark:text-gray-300">預覽圖片</span>
                    </div>
                    <button @click="clearPreview" 
                      class="w-8 h-8 flex items-center justify-center rounded-full text-gray-500 hover:text-red-500 hover:bg-gray-200/50 dark:hover:bg-gray-600/50 transition-all">
                      <i class="fas fa-times"></i>
                    </button>
                  </div>
                  <div class="relative p-4">
                    <div class="relative group">
                      <img :src="previewImage" 
                           class="max-h-48 w-auto mx-auto rounded-lg object-contain bg-white/50 dark:bg-gray-800/50 shadow-md transition-transform hover:scale-[1.02]" 
                           alt="預覽圖片">
                      <div class="absolute inset-0 rounded-lg bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    </div>
                    <div class="mt-3 text-center">
                      <span class="text-xs text-gray-500 dark:text-gray-400">
                        <i class="fas fa-info-circle mr-1"></i>
                        點擊發送按鈕，將圖片與文字一起傳送
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 原有的輸入區域 -->
            <div class="flex gap-4">
              <!-- 圖片上傳按鈕 -->
              <button @click="triggerImageUpload" 
                class="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors flex items-center justify-center"
                title="上傳圖片">
                <i class="fas fa-image"></i>
              </button>
              <!-- 隱藏的文件輸入 -->
              <input
                type="file"
                ref="imageInput"
                @change="handleImageUpload"
                accept="image/*"
                class="hidden"
              />
              <!-- 原有的文字輸入框 -->
              <input v-model="userInput" @keyup.enter="handleSend" type="text"
                class="fullscreen-input flex-1 px-6 py-3 bg-gray-100 dark:bg-gray-800 border-0 rounded-full focus:ring-2 focus:ring-blue-400 dark:text-white"
                placeholder="請輸入您的問題...">
              <!-- 原有的發送按鈕 -->
              <button @click="handleSend" :disabled="isLoading"
                class="px-6 py-3 bg-blue-400 text-white rounded-full hover:bg-blue-500 disabled:bg-gray-400 transition-colors">
                <i :class="['fas', isLoading ? 'fa-spinner fa-spin chat-icon-color' : 'fa-paper-plane chat-icon-color']"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 聊天視窗 -->
    <div v-show="isOpen" class="absolute bottom-20 right-0 w-96 bg-white dark:bg-gray-800 rounded-lg shadow-xl animate-fade-in z-[9999]">
      <!-- 聊天視窗標題 - 白色背景 -->
      <div
        class="chatbot-title flex justify-between items-center p-4 border-b bg-white rounded-t-lg">
        <div class="flex items-center">
          <i class="fas fa-robot text-blue-400 mr-2"></i>
          <h3 class="font-semibold text-blue-500">AI小助手</h3>
        </div>
        <div class="flex items-center gap-2">
          <!-- 全螢幕按鈕 -->
          <button @click="toggleFullscreen"
            class="text-blue-400 hover:text-blue-500 w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors"
            title="全螢幕模式">
            <i class="fas fa-expand-arrows-alt text-lg"></i>
          </button>
          <!-- 清除歷史按鈕 -->
          <button @click="clearHistory"
            class="text-blue-400 hover:text-blue-500 w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors"
            title="清除歷史對話">
            <i class="fas fa-trash-alt"></i>
          </button>
          <!-- 關閉按鈕 -->
          <button @click="toggleChat"
            class="text-blue-400 hover:text-blue-500 w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors">
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
                <div class="max-w-[70%] bg-blue-400 text-white px-4 py-2 rounded-2xl rounded-br-sm">
                  <!-- 處理圖片和文字組合的訊息 -->
                  <template v-if="message.type === 'image_with_text'">
                    <div class="space-y-2">
                      <div class="relative w-full">
                        <img 
                          :src="message.content.image" 
                          class="w-full max-h-[300px] object-contain rounded-lg cursor-pointer hover:opacity-90 transition-opacity bg-white/50"
                          @click="previewStoredImage(message.content.image)"
                          alt="用戶上傳的圖片"
                        >
                      </div>
                      <div class="text-white mt-2">
                        {{ message.content.text }}
                      </div>
                    </div>
                  </template>
                  <!-- 處理純文字訊息 -->
                  <template v-else>
                    {{ message.content }}
                  </template>
                </div>
                <div class="relative">
                  <div class="w-10 h-10 rounded-full bg-blue-400 flex items-center justify-center text-white text-sm">
                    <i class="fas fa-user"></i>
                  </div>
                </div>
              </div>
            </div>
            <!-- AI 回應 -->
            <div v-else class="flex justify-start">
              <div class="flex items-start space-x-2">
                <div class="relative">
                  <div class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-indigo-500">
                    <i class="fas fa-robot"></i>
                  </div>

                </div>
                <!-- 如果有內容，顯示聊天氣泡 -->
                <div v-if="message.content || message.toolInfo || message.generatedImage || (message.hasDeepReasoning && message.reasoningProcess)" class="max-w-2xl bg-gray-50 dark:bg-gray-800 text-gray-800 dark:text-gray-200 px-6 py-4 rounded-xl shadow-sm">
                  <!-- 工具調用信息 -->
                  <div v-if="message.toolInfo" 
                       class="mb-4 bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-100 dark:border-blue-800 animate-fade-in">
                    <div class="flex items-center mb-3">
                      <div class="w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center text-white">
                        <i class="fas fa-tools text-xs"></i>
                      </div>
                      <div class="ml-2">
                        <div class="text-sm font-medium text-blue-700 dark:text-blue-300">工具調用</div>
                        <div class="text-xs text-blue-600 dark:text-blue-400 font-mono">{{ message.toolInfo.name }}</div>
                      </div>
                    </div>
                    
                    <div class="mt-3">
                      <div class="text-xs font-medium text-blue-700 dark:text-blue-300 mb-2">參數：</div>
                      <div class="text-xs text-gray-600 dark:text-gray-400 font-mono bg-white/80 dark:bg-gray-800/80 p-3 rounded-lg border border-blue-100/60 dark:border-blue-800/60 overflow-x-auto">
                        <pre class="whitespace-pre-wrap break-words">{{ formatToolArguments(message.toolInfo.arguments) }}</pre>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 生成的圖片 -->
                  <div v-if="message.generatedImage" 
                       class="mb-4 bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg border border-purple-100 dark:border-purple-800 animate-fade-in-delay">
                    <div class="text-sm font-medium text-purple-700 dark:text-purple-300 mb-3">生成的圖片：</div>
                    <div class="flex justify-center">
                      <a :href="message.generatedImage" target="_blank" class="block hover:opacity-90 transition-opacity">
                        <img :src="message.generatedImage" class="max-w-full h-auto rounded-lg shadow-md cursor-pointer max-h-96 object-contain" alt="AI生成的圖片">
                      </a>
                    </div>
                  </div>
                  
                  <!-- 深度推理模式的回應 -->
                  <template v-if="message.hasDeepReasoning">
                    <div class="space-y-4">
                      <!-- 顯示推理過程 -->
                      <div v-if="message.reasoningProcess" class="bg-gradient-to-r from-indigo-50 to-blue-50 dark:from-indigo-900/20 dark:to-blue-900/10 p-5 rounded-lg border border-indigo-100 dark:border-indigo-800 mt-2 shadow-sm">
                        <div class="flex items-center mb-3">
                          <div class="w-8 h-8 rounded-full bg-gradient-to-r from-indigo-500 to-blue-500 flex items-center justify-center text-white shadow-md">
                            <i class="fas fa-brain"></i>
                          </div>
                          <div class="ml-3">
                            <div class="text-sm font-medium text-indigo-700 dark:text-indigo-300">推理過程</div>
                            <div class="text-xs text-indigo-500 dark:text-indigo-400">AI 的思考邏輯</div>
                          </div>
                        </div>
                        
                        <div class="relative">
                          <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-gradient-to-b from-indigo-300 to-blue-300 dark:from-indigo-700 dark:to-blue-700"></div>
                          
                          <div class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap font-mono pl-8 pr-4 py-3 bg-white/70 dark:bg-gray-800/70 rounded-lg backdrop-blur-sm overflow-auto max-h-80 leading-relaxed border border-indigo-100/60 dark:border-indigo-800/60">
                            {{ message.reasoningProcess }}
                          </div>
                        </div>
                        
                        <div class="mt-3 flex justify-between items-center">
                          <div v-if="message.thinkingTime" class="text-xs text-indigo-500 dark:text-indigo-400 font-medium">
                            <i class="fas fa-clock mr-1"></i> 思考時間: {{ message.thinkingTime }}秒
                          </div>
                          <div class="text-xs text-right text-indigo-400 dark:text-indigo-500 italic">
                            <i class="fas fa-lightbulb mr-1"></i> 深度思考模式
                          </div>
                        </div>
                      </div>
                      
                      <!-- 顯示最終答案 -->
                      <div v-if="message.content" class="bg-gradient-to-r from-emerald-50 to-green-50 dark:from-emerald-900/20 dark:to-green-900/10 p-5 rounded-lg border border-green-100 dark:border-green-800 mt-4 shadow-sm">
                        <div class="flex items-center mb-3">
                          <div class="w-8 h-8 rounded-full bg-gradient-to-r from-emerald-500 to-green-500 flex items-center justify-center text-white shadow-md">
                            <i class="fas fa-lightbulb"></i>
                          </div>
                          <div class="ml-3">
                            <div class="text-sm font-medium text-green-700 dark:text-green-300">最終答案</div>
                            <div class="text-xs text-green-500 dark:text-green-400">思考結果</div>
                          </div>
                        </div>
                        
                        <div class="text-base text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap p-4 bg-white/70 dark:bg-gray-800/70 rounded-lg backdrop-blur-sm border border-green-100/60 dark:border-green-800/60">
                          {{ message.content }}
                        </div>
                      </div>
                    </div>
                  </template>
                  
                  <!-- 一般文字內容 (只有在非深度推理模式下顯示) -->
                  <template v-else-if="message.content">
                    <!-- 結構化回答 -->
                    <template v-if="message.content.includes('★')">
                      <template v-for="(part, idx) in message.content.split('★').filter(Boolean)" :key="idx">
                        <!-- 答案區塊 -->
                        <template v-if="part.includes('答案：')">
                          <div class="space-y-2">
                            <div class="font-medium text-gray-900 dark:text-gray-100">★ 答案：</div>
                            <div class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                              {{ part.replace('答案：', '').trim() }}
                            </div>
                          </div>
                        </template>

                        <!-- 其他內容區塊 -->
                        <template v-else-if="!part.includes('資料來源：') && !part.includes('工具調用：')">
                          <div class="border-t border-gray-200 dark:border-gray-700 my-4"></div>
                          <div class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap mt-4">
                            {{ part.trim() }}
                          </div>
                        </template>

                        <!-- 資料來源區塊 -->
                        <template v-else-if="part.includes('資料來源：')">
                          <div class="border-t border-gray-200 dark:border-gray-700 my-4"></div>
                          <div class="text-sm text-gray-500 dark:text-gray-400">
                            ★ {{ part.trim() }}
                          </div>
                        </template>
                      </template>
                    </template>
                    
                    <!-- 一般文字內容 -->
                    <template v-else>
                      <div class="text-base text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap">
                        {{ message.content }}
                      </div>
                    </template>
                  </template>
                </div>
                <!-- 當消息正在加載時，顯示打字指示器 -->
                <div v-else class="flex items-center justify-center">
                  <div class="thinking-dots">
                    <span></span><span></span><span></span>
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
          <!-- 功能開關區域 -->
          <div class="flex items-center justify-end mb-3 space-x-2">
            <button @click="toggleDeepReasoning"
              :class="[
                'px-4 py-2 rounded-full flex items-center gap-2 transition-all',
                isDeepReasoningEnabled 
                  ? 'bg-gradient-to-r from-indigo-500 to-blue-500 text-white shadow-md hover:shadow-lg' 
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              ]">
              <i class="fas fa-brain"></i>
              <span class="text-sm font-medium">深入研究</span>
            </button>
            
            <button @click="toggleWebSearch"
              :class="[
                'px-4 py-2 rounded-full flex items-center gap-2 transition-all',
                isWebSearchEnabled 
                  ? 'bg-gradient-to-r from-indigo-500 to-blue-500 text-white shadow-md hover:shadow-lg' 
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              ]">
              <i class="fas fa-search"></i>
              <span class="text-sm font-medium">網路搜尋</span>
            </button>

            <!-- 圖像生成開關 -->
            <button @click="toggleImageGeneration"
              :class="[
                'px-4 py-2 rounded-full flex items-center gap-2 transition-all',
                isImageGenerationEnabled 
                  ? 'bg-gradient-to-r from-indigo-500 to-blue-500 text-white shadow-md hover:shadow-lg' 
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              ]">
              <i class="fas fa-image"></i>
              <span class="text-sm font-medium">圖像生成</span>
            </button>
          </div>
          
          <!-- 在輸入區域上方添加圖片預覽區域 -->
          <div v-if="previewImage" class="w-full flex flex-col items-center mb-4">
            <div class="w-[80%] bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800/50 dark:to-gray-700/50 rounded-xl border border-gray-200/50 dark:border-gray-700/50 backdrop-blur-sm shadow-lg overflow-hidden">
              <div class="flex items-center justify-between p-3 border-b border-gray-200/50 dark:border-gray-700/50">
                <div class="flex items-center gap-2">
                  <i class="fas fa-image text-blue-500 dark:text-blue-400"></i>
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300">預覽圖片</span>
                </div>
                <button @click="clearPreview" 
                  class="w-8 h-8 flex items-center justify-center rounded-full text-gray-500 hover:text-red-500 hover:bg-gray-200/50 dark:hover:bg-gray-600/50 transition-all">
                  <i class="fas fa-times"></i>
                </button>
              </div>
              <div class="relative p-4">
                <div class="relative group">
                  <img :src="previewImage" 
                       class="max-h-48 w-auto mx-auto rounded-lg object-contain bg-white/50 dark:bg-gray-800/50 shadow-md transition-transform hover:scale-[1.02]" 
                       alt="預覽圖片">
                  <div class="absolute inset-0 rounded-lg bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                </div>
                <div class="mt-3 text-center">
                  <span class="text-xs text-gray-500 dark:text-gray-400">
                    <i class="fas fa-info-circle mr-1"></i>
                    點擊發送按鈕，將圖片與文字一起傳送
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 原有的輸入區域 -->
          <div class="flex gap-4">
            <!-- 圖片上傳按鈕 -->
            <button @click="triggerImageUpload" 
              class="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors flex items-center justify-center"
              title="上傳圖片">
              <i class="fas fa-image"></i>
            </button>
            <!-- 隱藏的文件輸入 -->
            <input
              type="file"
              ref="imageInput"
              @change="handleImageUpload"
              accept="image/*"
              class="hidden"
            />
            <!-- 原有的文字輸入框 -->
            <input v-model="userInput" @keyup.enter="handleSend" type="text"
              class="chatbot-input flex-1 px-4 py-2 border border-gray-200 dark:border-gray-600 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              placeholder="請輸入您的問題...">
            <!-- 原有的發送按鈕 -->
            <button @click="handleSend" :disabled="isLoading"
              class="chatbot-btn px-4 py-2 bg-blue-400 text-white rounded-full hover:bg-blue-500 disabled:bg-gray-400 transition-colors duration-200">
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
import { s2t } from 'chinese-s2t'
import { getStorage, ref as storageRef, uploadBytes, getDownloadURL } from 'firebase/storage'

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
    const isQuickQuestionsOpen = ref(false)

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

    // 深度推理相關狀態
    const isDeepReasoningEnabled = ref(false)

    // 網路搜尋開關
    const isWebSearchEnabled = ref(false)

    // 首先在 setup 函數中添加新的狀態
    const isImageGenerationEnabled = ref(false)
    // 添加新的圖像生成請求函數
    const sendImageGenerationRequest = async (message, currentMessageIndex) => {
      try {
        const response = await fetch(
          `https://mynocodbapi.zeabur.app/image?prompt=${encodeURIComponent(message)}`,
          {
            method: 'GET',
            headers: {
              'accept': 'application/json'
            }
          }
        )

        const data = await response.json()
        console.log('圖像生成 API 回應:', data)

        if (data.status === 'success' && data.result && data.result.messages) {
          const messages = data.result.messages
          
          // 找出最終的文字回應
          const textMessages = messages.filter(msg => 
            msg.type === 'TextMessage' && msg.source === 'assistant_agent'
          )
          
          // 找出工具調用請求
          const toolCallRequests = messages.filter(msg => 
            msg.type === 'ToolCallRequestEvent'
          )
          
          // 找出工具執行結果
          const toolCallExecutions = messages.filter(msg => 
            msg.type === 'ToolCallExecutionEvent'
          )
          
          // 提取工具名稱和參數
          let toolName = ''
          let toolArguments = ''
          let finalContent = ''
          let imageUrl = null
          
          // 提取工具信息
          if (toolCallRequests.length > 0) {
            const toolCall = toolCallRequests[0]
            if (toolCall.content && Array.isArray(toolCall.content) && toolCall.content.length > 0) {
              const tool = toolCall.content[0]
              
              if (tool) {
                toolName = tool.name || ''
                toolArguments = tool.arguments || ''
              }
            }
          }
          
          // 提取圖片URL
          if (toolCallExecutions.length > 0) {
            const execution = toolCallExecutions[0]
            if (execution.content && Array.isArray(execution.content)) {
              const content = execution.content[0].content
              const imgMatch = content.match(/!\[.*?\]\((https:\/\/[^)]+)\)/)
              if (imgMatch && imgMatch[1]) {
                imageUrl = imgMatch[1]
              }
            }
          }
          
          // 獲取最終回應內容
          if (textMessages.length > 0) {
            const lastTextMessage = textMessages[textMessages.length - 1]
            if (typeof lastTextMessage.content === 'string') {
              finalContent = lastTextMessage.content.replace(/TERMINATE\.?$/, '').trim()
            }
          }
          
          // 更新聊天記錄
          chatHistory.value[currentMessageIndex] = {
            content: finalContent || '圖片生成完成',
            isUser: false,
            toolInfo: toolName ? {
              name: toolName,
              arguments: toolArguments
            } : null,
            generatedImage: imageUrl
          }
        } else {
          throw new Error('圖像生成請求失敗')
        }
      } catch (error) {
        console.error('圖像生成 API 錯誤:', error)
        chatHistory.value[currentMessageIndex] = {
          content: '抱歉，圖像生成過程中發生錯誤，請稍後再試。',
          isUser: false
        }
      }
    }

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

    // 發送訊息到 Langflow API 或深度推理 API
    const handleSend = async () => {
      if ((!userInput.value.trim() && !previewImage.value) || isLoading.value) return

      const currentInput = userInput.value.trim()
      const currentImage = previewImage.value

      // 立即清空輸入框和預覽圖片
      userInput.value = ''
      clearPreview()

      if (currentImage) {
        try {
          // 添加一個空的消息作為佔位符
          chatHistory.value.push({
            content: '',
            isUser: false
          })

          isLoading.value = true
          const currentMessageIndex = chatHistory.value.length - 1

          // 上傳圖片到 Firebase Storage 並獲取 URL
          const imageUrl = await uploadImageToFirebase(currentImage)

          // 先添加用戶的圖片和文字消息到聊天記錄
          chatHistory.value[currentMessageIndex] = {
            content: {
              image: imageUrl,
              text: currentInput || "分析這張圖片"
            },
            type: 'image_with_text',
            isUser: true
          }

          // 添加新的 AI 回應佔位符
          chatHistory.value.push({
            content: '',
            isUser: false
          })

          const aiMessageIndex = chatHistory.value.length - 1

          // 使用獲取到的 URL 構建消息
          const messages = [
            {
              role: "user",
              content: [
                {
                  type: "image_url",
                  image_url: {
                    url: imageUrl
                  }
                },
                {
                  type: "text",
                  text: currentInput || "請描述這張圖片"
                }
              ]
            }
          ]

          // 發送請求到 Mistral API
          try {
            const response = await fetch(import.meta.env.VITE_MISTRAL_API_URL, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": `Bearer ${import.meta.env.VITE_MISTRAL_API_KEY}`
              },
              body: JSON.stringify({
                model: "mistral-small-latest",
                messages: messages
              })
            })

            if (!response.ok) {
              throw new Error(`API錯誤: ${response.status}`)
            }

            const data = await response.json()
            const aiResponse = data.choices[0].message.content

            chatHistory.value[aiMessageIndex] = {
              content: s2t(aiResponse),
              isUser: false
            }
          } catch (error) {
            console.error('Mistral API 錯誤:', error)
            chatHistory.value[aiMessageIndex] = {
              content: '抱歉，圖片分析過程中發生錯誤，請稍後再試。',
              isUser: false
            }
          }
        } catch (error) {
          console.error('處理圖片上傳失敗:', error)
          chatHistory.value.push({
            content: '圖片上傳失敗，請稍後再試。',
            isUser: false
          })
        } finally {
          isLoading.value = false
        }
      } else {
        // 原有的文字訊息處理邏輯
        chatHistory.value.push({
          content: currentInput,
          isUser: true
        })

        chatHistory.value.push({
          content: '',
          isUser: false
        })

        isLoading.value = true
        
        const currentMessageIndex = chatHistory.value.length - 1

        try {
          if (isImageGenerationEnabled.value) {
            await sendImageGenerationRequest(currentInput, currentMessageIndex)
          } else if (isWebSearchEnabled.value) {
            await sendSearchRequest(currentInput, currentMessageIndex)
          } else if (isDeepReasoningEnabled.value) {
            await sendDeepReasoningRequest(currentInput, currentMessageIndex)
          } else {
            await sendRegularRequest(currentInput, currentMessageIndex)
          }
        } catch (error) {
          console.error('請求失敗:', error)
          chatHistory.value[currentMessageIndex].content = '抱歉，我現在無法回應。請稍後再試。'
        } finally {
          isLoading.value = false
        }
      }
    }
    
    // 發送深度推理請求
    const sendDeepReasoningRequest = async (message, currentMessageIndex) => {
      // 建立計時起點
      const startTime = Date.now()
      
      // 構建對話歷史
      const chatMessages = []
      
      // 添加最近 5 條對話紀錄（如果有）
      let recentHistory = []
      for (let i = chatHistory.value.length - 3; i >= 0 && recentHistory.length < 10; i--) {
        const msg = chatHistory.value[i]
        if (msg.isUser) {
          recentHistory.unshift({ role: "user", content: msg.content })
        } else if (msg.content) {
          recentHistory.unshift({ role: "assistant", content: msg.content })
        }
      }
      
      // 合併對話歷史
      chatMessages.push(...recentHistory)
      
      // 添加當前問題
      chatMessages.push({ role: "user", content: message })
      
      // 構建請求體
      const requestBody = {
        model: "jina-deepsearch-v1",
        messages: chatMessages,
        stream: true,
        reasoning_effort: "low",
        no_direct_answer: false
      }
      
      try {
        console.log('發送深度推理請求:', requestBody)
        
        const response = await fetch(
          import.meta.env.VITE_JINA_API_URL,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
          }
        )
        
        if (!response.ok) {
          throw new Error(`API 錯誤: ${response.status}`)
        }
        
        if (!response.body) {
          throw new Error('ReadableStream not supported')
        }
        
        // 處理流式響應
        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        let reasoningProcess = ""
        let finalAnswer = ""
        let isThinking = false
        let rawContent = ""
        
        while (true) {
          const { value, done } = await reader.read()
          if (done) break
          
          const chunk = decoder.decode(value)
          const lines = chunk.split('\n').filter(line => line.trim() !== '')
          
          for (const line of lines) {
            if (line.startsWith('data:')) {
              try {
                const jsonStr = line.slice(5).trim()
                if (jsonStr === '[DONE]') continue
                
                const json = JSON.parse(jsonStr)
                console.log("深度推理詳細回應:", json)
                
                if (json.choices && json.choices.length > 0) {
                  const delta = json.choices[0].delta
                  
                  if (delta.type === "think") {
                    isThinking = true
                    if (delta.content) {
                      // 將思考內容轉換為繁體中文
                      reasoningProcess += s2t(delta.content)
                    }
                  }
                  else if (delta.type === "text") {
                    isThinking = false
                    if (delta.content) {
                      // 將最終答案轉換為繁體中文
                      finalAnswer += s2t(delta.content)
                    }
                  }
                  else if (delta.content) {
                    rawContent += delta.content
                    
                    if (delta.content.includes("<think>")) {
                      isThinking = true
                      const cleanedContent = delta.content.replace(/<think>/g, "")
                      if (cleanedContent.trim()) {
                        // 將思考內容轉換為繁體中文
                        reasoningProcess += s2t(cleanedContent)
                      }
                    }
                    else if (delta.content.includes("</think>")) {
                      isThinking = false
                      const cleanedContent = delta.content.replace(/<\/think>/g, "")
                      if (cleanedContent.trim()) {
                        // 將思考內容轉換為繁體中文
                        reasoningProcess += s2t(cleanedContent)
                      }
                    }
                    else if (isThinking) {
                      const cleanedContent = delta.content.replace(/<\/?think>/g, "")
                      // 將思考內容轉換為繁體中文
                      reasoningProcess += s2t(cleanedContent)
                    }
                    else {
                      // 將最終答案轉換為繁體中文
                      finalAnswer += s2t(delta.content)
                    }
                  }
                  
                  // 即時更新聊天記錄
                  chatHistory.value[currentMessageIndex] = {
                    content: finalAnswer || '思考中...',
                    reasoningProcess: reasoningProcess,
                    hasDeepReasoning: true,
                    isUser: false
                  }
                }
              } catch (e) {
                console.error('解析流式響應錯誤:', e, line)
              }
            }
          }
        }
        
        // 最終處理：確保移除所有標籤並清理內容
        if (rawContent) {
          const thinkMatch = rawContent.match(/<think>([\s\S]*?)<\/think>/);
          if (thinkMatch && thinkMatch[1]) {
            // 將思考過程轉換為繁體中文
            reasoningProcess = s2t(thinkMatch[1].trim());
          }
          
          // 將最終答案轉換為繁體中文
          finalAnswer = s2t(rawContent.replace(/<think>[\s\S]*?<\/think>/, '').trim());
        }
        
        // 最後一道防線 - 確保所有<think>標籤都被移除
        reasoningProcess = reasoningProcess.replace(/<\/?think>/g, "");
        
        // 計算思考所花費的時間（毫秒轉換為秒，保留2位小數）
        const thinkingTime = ((Date.now() - startTime) / 1000).toFixed(2)
        
        // 確保有推理過程
        if (!reasoningProcess && finalAnswer) {
          reasoningProcess = "無推理過程提供";
        }
        
        // 確保有答案
        if (!finalAnswer && reasoningProcess) {
          finalAnswer = "推理完成，但未得出明確結論";
        }
        
        // 更新最終回應，包含思考時間
        chatHistory.value[currentMessageIndex] = {
          content: finalAnswer || '抱歉，我無法產生有效答案。',
          reasoningProcess: reasoningProcess,
          hasDeepReasoning: true,
          isUser: false,
          thinkingTime: thinkingTime
        }
        
        console.log("深度推理結果:", {
          思考: reasoningProcess,
          答案: finalAnswer,
          思考時間: `${thinkingTime}秒`
        });
      } catch (error) {
        console.error('深度推理 API 錯誤:', error)
        chatHistory.value[currentMessageIndex] = {
          content: '深度推理功能暫時無法使用，請稍後再試或關閉深度推理模式。',
          isUser: false
        }
      }
    }
    
    // 進一步優化 sendRegularRequest 函數，著重修復文字回應提取問題
    const sendRegularRequest = async (message, currentMessageIndex) => {
      try {
        // 使用API端點
        const response = await fetch(
          `${import.meta.env.VITE_AUTOGEN_API_URL}/knowledge?question=${encodeURIComponent(message)}`,
          {
            method: 'GET',
            headers: {
              'accept': 'application/json'
            }
          }
        )

        const data = await response.json()
        console.log('API 完整回應:', data)

        // 檢查是否有錯誤
        if (data.status !== 'success') {
          throw new Error('API請求失敗')
        }

        // 處理回應
        if (data.result && data.result.messages) {
          const messages = data.result.messages
          
          // 找出最終的文字回應 (從後往前找最後一條 TextMessage)
          const textMessages = messages.filter(msg => 
            msg.type === 'TextMessage' && msg.source === 'assistant_agent'
          )
          
          // 找出工具調用請求
          const toolCallRequests = messages.filter(msg => 
            msg.type === 'ToolCallRequestEvent'
          )
          
          // 找出工具執行結果
          const toolCallExecutions = messages.filter(msg => 
            msg.type === 'ToolCallExecutionEvent'
          )
          
          // 找出工具調用摘要
          const toolCallSummaries = messages.filter(msg => 
            msg.type === 'ToolCallSummaryMessage'
          )
          
          // 初始化變數
          let imageUrl = null
          let toolName = ''
          let toolArguments = ''
          let finalContent = ''
          
          // 提取工具名稱和參數
          if (toolCallRequests.length > 0) {
            const toolCall = toolCallRequests[0]
            if (toolCall.content && Array.isArray(toolCall.content) && toolCall.content.length > 0) {
              const tool = toolCall.content[0]
              
              if (tool) {
                toolName = tool.name || ''
                
                if (typeof tool.arguments === 'string') {
                  try {
                    // 嘗試解析JSON字符串
                    const parsedArgs = JSON.parse(tool.arguments)
                    toolArguments = JSON.stringify(parsedArgs, null, 2)
                  } catch (e) {
                    // 如果解析失敗，直接使用原字符串
                    toolArguments = tool.arguments
                  }
                } else if (tool.arguments) {
                  // 如果已經是對象，直接轉為格式化JSON
                  toolArguments = JSON.stringify(tool.arguments, null, 2)
                }
              }
            }
          }
          
          // 檢查是否為圖片生成工具
          const isImageGeneration = toolName === 'generate_image'
          
          // 如果是圖片生成，提取圖片URL
          if (isImageGeneration) {
            // 1. 優先從執行結果中查找
            if (toolCallExecutions.length > 0) {
              for (const execution of toolCallExecutions) {
                if (!execution.content) continue
                
                let contentText = ''
                
                if (Array.isArray(execution.content)) {
                  // 處理數組形式的內容
                  for (const item of execution.content) {
                    if (typeof item === 'object' && item.content) {
                      contentText = item.content
                      break
                    } else if (typeof item === 'string') {
                      contentText = item
                      break
                    }
                  }
                } else if (typeof execution.content === 'string') {
                  // 直接使用字符串內容
                  contentText = execution.content
                }
                
                // 使用正則表達式提取圖片URL
                const imgMatch = contentText.match(/!\[.*?\]\((https:\/\/[^)]+)\)/)
                if (imgMatch && imgMatch[1]) {
                  imageUrl = imgMatch[1]
                  break
                }
              }
            }
            
            // 2. 如果執行結果中沒找到，從摘要中查找
            if (!imageUrl && toolCallSummaries.length > 0) {
              for (const summary of toolCallSummaries) {
                if (!summary.content) continue
                
                let summaryText = ''
                if (typeof summary.content === 'string') {
                  summaryText = summary.content
                } else if (Array.isArray(summary.content)) {
                  // 處理可能的數組形式
                  summaryText = summary.content.join('\n')
                }
                
                // 使用正則表達式提取圖片URL
                const imgMatch = summaryText.match(/!\[.*?\]\((https:\/\/[^)]+)\)/)
                if (imgMatch && imgMatch[1]) {
                  imageUrl = imgMatch[1]
                  break
                }
              }
            }
          }
          
          // 獲取最終回應內容 - 修改提取方式
          if (textMessages.length > 0) {
            // 使用最後一條文字訊息
            const lastTextMessage = textMessages[textMessages.length - 1]
            console.log('最後一條文字訊息:', lastTextMessage)
            
            // 檢查內容的數據類型和處理
            if (typeof lastTextMessage.content === 'string') {
              finalContent = lastTextMessage.content.replace(/TERMINATE\.?$/, '').trim()
              console.log('從文字訊息提取的回應:', finalContent)
            } else if (Array.isArray(lastTextMessage.content)) {
              finalContent = lastTextMessage.content.join('\n').replace(/TERMINATE\.?$/, '').trim()
            } else if (lastTextMessage.content && typeof lastTextMessage.content === 'object') {
              finalContent = JSON.stringify(lastTextMessage.content)
            }
          } else if (toolCallSummaries.length > 0 && !isImageGeneration) {
            // 如果沒有文字訊息但有非圖片生成的摘要
            const summary = toolCallSummaries[0]
            
            if (typeof summary.content === 'string') {
              finalContent = summary.content.replace(/TERMINATE\.?$/, '').trim()
              console.log('從摘要提取的回應:', finalContent)
            } else if (Array.isArray(summary.content)) {
              finalContent = summary.content.join('\n').replace(/TERMINATE\.?$/, '').trim()
            } else if (summary.content && typeof summary.content === 'object') {
              finalContent = JSON.stringify(summary.content)
            }
          } else if (toolCallExecutions.length > 0 && !isImageGeneration) {
            // 嘗試從工具執行結果提取文字回應
            for (const execution of toolCallExecutions) {
              if (!execution.content) continue
              
              if (Array.isArray(execution.content) && execution.content.length > 0) {
                const item = execution.content[0]
                if (typeof item === 'object' && item.content && typeof item.content === 'string') {
                  finalContent = item.content.replace(/TERMINATE\.?$/, '').trim()
                  console.log('從執行結果提取的回應:', finalContent)
                  break
                }
              } else if (typeof execution.content === 'string') {
                finalContent = execution.content.replace(/TERMINATE\.?$/, '').trim()
                break
              }
            }
          }
          
          // 如果所有嘗試都失敗，使用一個預設消息
          if (!finalContent) {
            finalContent = '操作已完成，但未獲得具體回應內容'
          }
          
          // 構建工具信息對象
          let toolInfo = null
          if (toolName) {
            toolInfo = {
              name: toolName,
              arguments: toolArguments
            }
          }
          
          // 更新聊天消息
          chatHistory.value[currentMessageIndex] = {
            content: finalContent,
            isUser: false,
            toolInfo: toolInfo,
            generatedImage: imageUrl
          }
          
          console.log('更新聊天記錄:', chatHistory.value[currentMessageIndex])
        } else {
          // 如果沒有找到預期的回應格式，使用原始回應
          chatHistory.value[currentMessageIndex].content = data.result || '抱歉，我無法理解您的問題。'
        }
      } catch (error) {
        console.error('API 請求處理錯誤:', error)
        throw error
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

    // 在 setup 函數中修改 isImageUrl 方法
    const extractImageSrc = (content) => {
      if (typeof content !== 'string') return content;
      
      // 如果是 HTML img 標籤，提取 src
      if (content.startsWith('<img')) {
        const match = content.match(/src="([^"]+)"/)
        return match ? match[1] : content
      }
      return content
    }

    const isImageUrl = (content) => {
      // 檢查是否為圖片URL格式
      return typeof content === 'string' && (
        content.startsWith('<img') || // 處理HTML標籤格式
        content.match(/\.(jpg|jpeg|png|gif|webp)/) || // 處理一般圖片URL
        content.includes('storage.googleapis.com') // 處理Google Storage圖片
      )
    }

    // 在 setup 函數中添加 sendSearchRequest 方法
    const sendSearchRequest = async (message, currentMessageIndex) => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_AUTOGEN_API_URL}/search?query=${encodeURIComponent(message)}&num_results=5&category=web&search_type=keyword`,
          {
            method: 'GET',
            headers: {
              'accept': 'application/json'
            }
          }
        )

        const data = await response.json()
        console.log('搜尋 API 回應:', data)

        if (data.status === 'success' && data.result && data.result.messages) {
          const messages = data.result.messages
          
          // 找出最終的文字回應
          const textMessages = messages.filter(msg => 
            msg.type === 'TextMessage' && msg.source === 'assistant_agent'
          )
          
          // 找出工具調用請求
          const toolCallRequests = messages.filter(msg => 
            msg.type === 'ToolCallRequestEvent'
          )
          
          // 找出工具調用摘要
          const toolCallSummaries = messages.filter(msg => 
            msg.type === 'ToolCallSummaryMessage'
          )
          
          // 提取工具名稱和參數
          let toolName = ''
          let toolArguments = ''
          let finalContent = ''
          
          if (toolCallRequests.length > 0) {
            const toolCall = toolCallRequests[0]
            if (toolCall.content && Array.isArray(toolCall.content) && toolCall.content.length > 0) {
              const tool = toolCall.content[0]
              
              if (tool) {
                toolName = tool.name || ''
                
                if (typeof tool.arguments === 'string') {
                  try {
                    const parsedArgs = JSON.parse(tool.arguments)
                    toolArguments = JSON.stringify(parsedArgs, null, 2)
                  } catch (e) {
                    toolArguments = tool.arguments
                  }
                } else if (tool.arguments) {
                  toolArguments = JSON.stringify(tool.arguments, null, 2)
                }
              }
            }
          }
          
          // 獲取最終回應內容
          if (textMessages.length > 0) {
            const lastTextMessage = textMessages[textMessages.length - 1]
            
            if (typeof lastTextMessage.content === 'string') {
              // 移除 TERMINATE 標籤並轉換為繁體中文
              finalContent = s2t(lastTextMessage.content.replace(/TERMINATE/gi, '').trim())
            } else if (Array.isArray(lastTextMessage.content)) {
              // 移除 TERMINATE 標籤並轉換為繁體中文
              finalContent = s2t(lastTextMessage.content.join('\n').replace(/TERMINATE/gi, '').trim())
            }
          } else if (toolCallSummaries.length > 0) {
            const summary = toolCallSummaries[0]
            
            if (typeof summary.content === 'string') {
              // 移除 TERMINATE 標籤並轉換為繁體中文
              finalContent = s2t(summary.content.replace(/TERMINATE/gi, '').trim())
            } else if (Array.isArray(summary.content)) {
              // 移除 TERMINATE 標籤並轉換為繁體中文
              finalContent = s2t(summary.content.join('\n').replace(/TERMINATE/gi, '').trim())
            }
          }
          
          // 如果沒有找到內容
          if (!finalContent) {
            finalContent = '抱歉，沒有找到相關的搜尋結果。'
          }
          
          // 更新聊天記錄
          chatHistory.value[currentMessageIndex] = {
            content: finalContent,
            isUser: false,
            toolInfo: toolName ? {
              name: toolName,
              arguments: toolArguments || JSON.stringify({
                query: message,
                category: 'web',
                num_results: 1,
                search_type: 'keyword'
              }, null, 2)
            } : null
          }
        } else {
          throw new Error('搜尋請求失敗')
        }
      } catch (error) {
        console.error('搜尋 API 錯誤:', error)
        chatHistory.value[currentMessageIndex] = {
          content: '抱歉，搜尋過程中發生錯誤，請稍後再試。',
          isUser: false
        }
      }
    }

    // 修改三個切換函數
    const toggleDeepReasoning = () => {
      if (isWebSearchEnabled.value) {
        isWebSearchEnabled.value = false;
      }
      if (isImageGenerationEnabled.value) {
        isImageGenerationEnabled.value = false;
      }
      isDeepReasoningEnabled.value = !isDeepReasoningEnabled.value;
    };

    const toggleWebSearch = () => {
      if (isDeepReasoningEnabled.value) {
        isDeepReasoningEnabled.value = false;
      }
      if (isImageGenerationEnabled.value) {
        isImageGenerationEnabled.value = false;
      }
      isWebSearchEnabled.value = !isWebSearchEnabled.value;
    };

    const toggleImageGeneration = () => {
      if (isWebSearchEnabled.value) {
        isWebSearchEnabled.value = false;
      }
      if (isDeepReasoningEnabled.value) {
        isDeepReasoningEnabled.value = false;
      }
      isImageGenerationEnabled.value = !isImageGenerationEnabled.value;
    };

    // 在 setup 函數中添加格式化函數
    const formatToolArguments = (args) => {
      try {
        if (typeof args === 'string') {
          // 嘗試解析 JSON 字符串
          const parsed = JSON.parse(args)
          return JSON.stringify(parsed, null, 2)
        }
        // 如果已經是對象，直接格式化
        return JSON.stringify(args, null, 2)
      } catch (e) {
        // 如果解析失敗，返回原始字符串
        return args
      }
    }

    // 在 setup 函數中添加
    const imageInput = ref(null)

    // 觸發文件選擇
    const triggerImageUpload = () => {
      imageInput.value.click()
    }

    // 處理圖片上傳
    const handleImageUpload = async (event) => {
      const file = event.target.files[0]
      if (!file) return

      try {
        // 轉換圖片為 base64 並顯示預覽
        const base64Image = await convertImageToBase64(file)
        previewImage.value = base64Image
      } catch (error) {
        console.error('圖片處理錯誤:', error)
      } finally {
        // 清除文件輸入，允許重複選擇同一文件
        event.target.value = ''
      }
    }

    // 添加清除預覽的方法
    const clearPreview = () => {
      previewImage.value = null
    }

    // 將圖片轉換為 base64
    const convertImageToBase64 = (file) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = () => resolve(reader.result)
        reader.onerror = reject
        reader.readAsDataURL(file)
      })
    }

    // 在 setup 函數中添加新的狀態
    const previewImage = ref(null)

    // 修改 uploadImageToFirebase 函數
    const uploadImageToFirebase = async (base64Image) => {
      try {
        const storage = getStorage()
        
        // 修改時間戳格式為 YYYYMMDD_HHMMSS
        const now = new Date()
        const timestamp = now.getFullYear() +
          String(now.getMonth() + 1).padStart(2, '0') +
          String(now.getDate()).padStart(2, '0') + '_' +
          String(now.getHours()).padStart(2, '0') +
          String(now.getMinutes()).padStart(2, '0') +
          String(now.getSeconds()).padStart(2, '0')
        
        // 修改檔案名稱格式
        const filename = `ChatBot_image_${timestamp}.png`
        const imageRef = storageRef(storage, `images/${filename}`)
        
        // 從 base64 創建 Blob
        const base64Content = base64Image.split(',')[1]
        const byteCharacters = atob(base64Content)
        const byteNumbers = new Array(byteCharacters.length)
        
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i)
        }
        
        const byteArray = new Uint8Array(byteNumbers)
        const blob = new Blob([byteArray], { type: 'image/png' })
        
        await uploadBytes(imageRef, blob, {
          contentType: 'image/png'
        })
        
        const image_url = await getDownloadURL(imageRef)
        
        console.log('Image URL:', image_url)
        return image_url
        
      } catch (error) {
        console.error('上傳圖片到 Firebase 失敗:', error)
        throw error
      }
    }

    // 修改圖片預覽方法
    const previewStoredImage = (imageUrl) => {
      if (!imageUrl) return
      window.open(imageUrl, '_blank')
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
      handleSend,
      toggleQuickQuestions,
      handleQuickQuestion,
      clearHistory,
      quickQuestions,
      isImageUrl,
      extractImageSrc,
      isDeepReasoningEnabled,
      isWebSearchEnabled,
      sendSearchRequest,
      toggleDeepReasoning,
      toggleWebSearch,
      formatToolArguments,
      isImageGenerationEnabled,
      toggleImageGeneration,
      imageInput,
      triggerImageUpload,
      handleImageUpload,
      previewImage,
      clearPreview,
      previewStoredImage,
    }
  }
}
</script>