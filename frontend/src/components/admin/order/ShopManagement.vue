<template>
  <div>
    <!-- 無資料時顯示 -->
    <div v-if="!shops || shops.length === 0" 
         class="bg-white rounded-lg shadow-sm p-8 text-center">
      <div class="text-gray-500 mb-4">
        <i class="fas fa-store text-4xl"></i>
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">
        尚無飲料店資料
      </h3>
      <p class="text-gray-500 mb-4">
        目前還沒有任何飲料店資訊，點擊下方按鈕新增飲料店。
      </p>
      <button @click="showAddModal = true"
              class="inline-flex items-center px-4 py-2 bg-blue-50 text-blue-600 rounded-md hover:bg-blue-100 transition-colors duration-200">
        <i class="fas fa-plus mr-2"></i>
        新增飲料店
      </button>
    </div>

    <!-- 有資料時顯示表格 -->
    <div v-else>
    <DataTable
      :columns="columns"
      :data="shops"
        @add="handleAdd"
      @edit="editShop"
      @delete="deleteShop"
      @batch-delete="batchDeleteShops">
      <!-- 自定義圖片列 -->
        <template #hero_image="{ item }">
          <div class="w-20 flex-shrink-0">
            <img :src="getShopImage(item)" 
                 class="w-20 h-20 rounded-lg object-cover shadow-sm"
                 alt="店家圖片">
          </div>
      </template>
      <!-- 自定義星級列 -->
      <template #rating="{ item }">
        <div class="flex items-center">
          <div class="flex text-yellow-400">
            <i v-for="n in 5" :key="n" 
               :class="['fas', n <= Math.floor(item.rating) ? 'fa-star' : 'fa-star-o']"></i>
          </div>
          <span class="ml-2 text-gray-600">{{ item.rating }}</span>
        </div>
      </template>
      <!-- 自定義狀態列 -->
        <template #is_new_until="{ item }">
        <span :class="[
          'px-2 py-1 text-xs rounded-full',
            isNewStore(item.is_new_until) ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
        ]">
            {{ isNewStore(item.is_new_until) ? '新開幕' : '已開幕' }}
        </span>
      </template>
      <!-- 自定義瀏覽次數列 -->
        <template #review_number="{ item }">
        <div class="flex items-center text-gray-600">
          <i class="fas fa-eye mr-2"></i>
            {{ item.review_number }}
        </div>
      </template>
    </DataTable>
    </div>

    <!-- 新增/編輯彈窗 -->
    <div v-if="showAddModal" 
         class="fixed inset-0 z-[9999]">
      <!-- 背景遮罩 -->
      <div class="absolute inset-0 bg-black bg-opacity-50"></div>
      
      <!-- Modal 內容 -->
      <div class="absolute inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <div class="relative bg-white rounded-lg shadow-lg w-full max-w-4xl">
            <!-- Modal 標題 -->
            <div class="flex justify-between items-center px-6 py-4 border-b">
              <h3 class="text-xl font-semibold">{{ editingShop ? '編輯店家' : '新增店家' }}</h3>
              <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
                <i class="fas fa-times"></i>
              </button>
            </div>

            <!-- Modal 內容 -->
            <div class="px-6 py-4 space-y-4 max-h-[calc(85vh-8rem)] overflow-y-auto">
              <!-- 分類標籤 -->
              <div class="border-b mb-6">
                <div class="flex space-x-4">
                  <button v-for="tab in tabs" 
                          :key="tab.key"
                          @click="currentTab = tab.key"
                          :class="[
                            'px-4 py-2 -mb-px',
                            currentTab === tab.key 
                              ? 'border-b-2 border-blue-500 text-blue-600'
                              : 'text-gray-500 hover:text-gray-700'
                          ]">
                    {{ tab.label }}
                  </button>
                </div>
              </div>

              <!-- 基本資料 -->
              <div v-show="currentTab === 'basic'" class="space-y-4">
                <!-- 店家圖片上傳 -->
                <div class="flex items-start space-x-6">
                  <div class="flex flex-col items-center">
                    <div class="relative w-32 h-32 mb-4">
                      <img :src="previewImage || shopForm.hero_image" 
                           class="w-full h-full rounded-lg object-cover shadow-sm">
                      <!-- 未上傳圖片時顯示提示 -->
                      <div v-if="!previewImage && shopForm.hero_image === defaultImage.url"
                           class="absolute inset-0 flex flex-col items-center justify-center 
                                  bg-black bg-opacity-50 rounded-lg text-white">
                        <i class="fas fa-camera text-2xl mb-2"></i>
                        <span class="text-xs text-center font-medium">點擊上傳<br>主要圖片</span>
                      </div>
                    </div>
                    <label class="px-4 py-2 bg-gray-100 rounded-lg cursor-pointer hover:bg-gray-200">
                      <input type="file" class="hidden" accept="image/*" @change="handleImageUpload">
                      <i class="fas fa-camera mr-2"></i>主要圖片
                    </label>
                  </div>
                <div class="flex flex-col items-center">
                    <div class="relative w-32 h-32 mb-4">
                      <img :src="previewListingImage || shopForm.hero_listing_image" 
                           class="w-full h-full rounded-lg object-cover shadow-sm">
                      <!-- 未上傳圖片時顯示提示 -->
                      <div v-if="!previewListingImage && shopForm.hero_listing_image === defaultImage.url"
                           class="absolute inset-0 flex flex-col items-center justify-center 
                                  bg-black bg-opacity-50 rounded-lg text-white">
                        <i class="fas fa-camera text-2xl mb-2"></i>
                        <span class="text-xs text-center font-medium">點擊上傳<br>列表圖片</span>
                      </div>
                    </div>
                  <label class="px-4 py-2 bg-gray-100 rounded-lg cursor-pointer hover:bg-gray-200">
                      <input type="file" class="hidden" accept="image/*" @change="handleListingImageUpload">
                      <i class="fas fa-camera mr-2"></i>列表圖片
                  </label>
                </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="required-field">店家名稱</label>
                  <input type="text" 
                         v-model="shopForm.name" 
                         @input="handleNameInput"
                         @blur="validateName(shopForm.name)"
                         class="form-input"
                         :class="{'border-red-500': formErrors.name}">
                  <p v-if="formErrors.name" class="mt-1 text-sm text-red-500">
                    {{ formErrors.name }}
                  </p>
                </div>
                  <div>
                    <label>正規化名稱</label>
                    <input type="text" v-model="shopForm.normalized_name" 
                           class="form-input" readonly>
                </div>
                <div>
                    <label class="required-field">城市</label>
                    <select v-model="shopForm.city_CN" 
                            @change="handleCityChange"
                            @blur="validateCity(shopForm.city_CN)"
                            class="form-select"
                            :class="{'border-red-500': formErrors.city_CN}">
                      <option v-for="city in cityOptions" 
                              :key="city" 
                              :value="city">{{ city }}</option>
                </select>
                <p v-if="formErrors.city_CN" class="mt-1 text-sm text-red-500">
                  {{ formErrors.city_CN }}
                </p>
              </div>
              <div>
                  <label class="required-field">地址</label>
                  <input type="text" v-model="shopForm.address" class="form-input">
                </div>
                </div>
              </div>

              <!-- 營業資訊 -->
              <div v-show="currentTab === 'business'" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="required-field">預算</label>
                    <input type="number" 
                           v-model="shopForm.budget" 
                           min="1" 
                           class="form-input"
                           @input="validateBudget">
                  </div>
                  <div>
                    <label>電話</label>
                    <input type="text" v-model="shopForm.customer_phone" class="form-input">
                  </div>
                  <div>
                    <label>最低外送費</label>
                    <input type="number" v-model="shopForm.minimum_delivery_fee" class="form-input">
                  </div>
                  <div>
                    <label>最低訂單金額</label>
                    <input type="number" v-model="shopForm.minimum_order_amount" class="form-input">
                  </div>
                  <div>
                    <label>最短外送時間</label>
                    <input type="number" v-model="shopForm.minimum_delivery_time" class="form-input">
                  </div>
                  <div>
                    <label>最短自取時間</label>
                    <input type="number" v-model="shopForm.minimum_pickup_time" class="form-input">
                  </div>
                </div>
              </div>

              <!-- 位置資訊 -->
              <div v-show="currentTab === 'location'" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="required-field">緯度</label>
                    <input type="number" 
                           v-model="shopForm.latitude" 
                           min="1" 
                           step="any"
                           class="form-input"
                           @input="validateLatitude">
                  </div>
                  <div>
                    <label class="required-field">經度</label>
                    <input type="number" 
                           v-model="shopForm.longitude" 
                           min="1" 
                           step="any"
                           class="form-input"
                           @input="validateLongitude">
                </div>
                <div>
                    <label>距離</label>
                    <input type="number" v-model="shopForm.distance" 
                           min="1" class="form-input">
                  </div>
                </div>
              </div>

              <!-- 評分資訊 -->
              <div v-show="currentTab === 'rating'" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="required-field">評分</label>
                    <div class="flex items-center space-x-2">
                      <template v-for="n in 5" :key="n">
                        <i class="fas fa-star cursor-pointer"
                           :class="n <= shopForm.rating ? 'text-yellow-400' : 'text-gray-300'"
                           @click="shopForm.rating = n"></i>
                      </template>
                    </div>
                </div>
                <div>
                    <label class="required-field">瀏覽次數</label>
                    <input type="number" 
                           v-model="shopForm.review_number" 
                           min="1" 
                           class="form-input"
                           @input="validateReviewNumber">
                  </div>
                </div>
              </div>

              <!-- 其他資訊 -->
              <div v-show="currentTab === 'other'" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label>開幕時間</label>
                    <input type="datetime-local" 
                           v-model="shopForm.is_new_until" 
                           class="form-input">
                  </div>
                  <div>
                    <label>料理類型ID</label>
                    <input type="text" v-model="shopForm.primary_cuisine_id" class="form-input">
                  </div>
                  <div>
                    <label>重定向URL</label>
                    <input type="text" v-model="shopForm.redirection_url" class="form-input">
                </div>
                <div>
                    <label>標籤</label>
                    <input type="text" v-model="shopForm.tag" class="form-input">
                  </div>
                  <div class="col-span-2">
                    <label>描述</label>
                    <textarea v-model="shopForm.description" 
                             rows="3" 
                             class="form-textarea w-full"></textarea>
                  </div>
                </div>
              </div>
            </div>

            <!-- Modal 底部按鈕 -->
            <div class="px-6 py-4 bg-gray-50 border-t rounded-b-lg flex justify-end space-x-3">
              <button @click="closeModal" 
                      class="px-4 py-2 text-gray-600 hover:text-gray-800 rounded-lg hover:bg-gray-100 transition-colors">
                取消
              </button>
              <button @click="saveShop" 
                      class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-sm">
                確認
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <BackToHome />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import Swal from 'sweetalert2'
import DataTable from '../common/DataTable.vue'
import BackToHome from '../common/BackToHome.vue'
import { useLogger } from '@/composables/useLogger'
import { shopAPI } from '@/api'

export default {
  name: 'ShopManagement',
  components: {
    DataTable,
    BackToHome
  },
  setup() {
    const shops = ref([])
    const showAddModal = ref(false)
    const { logOperation } = useLogger()

    return { shops, showAddModal, logOperation }
  },
  async created() {
    await this.fetchShops()
    // 記錄訪問飲料店管理頁面
    await this.logOperation('【飲料店管理】訪問飲料店管理頁面', '查看')
  },
  data() {
    return {
      defaultImage: 'https://placehold.co/600x400/png?text=No+Image',  // 預設假圖
      columns: [
        { 
          key: 'hero_image', 
          label: '店家圖片',
          width: '100px',  // 固定寬度
          className: 'whitespace-nowrap' // 防止換行
        },
        { key: 'name', label: '店家名稱' },
        { key: 'city', label: '城市' },
        { key: 'address', label: '地址', className: 'w-full' }, // 地址欄位可以佔據剩餘空間
        { key: 'rating', label: '星級', width: '100px' },
        { key: 'review_number', label: '瀏覽次數', width: '120px' },
        { key: 'is_new_until', label: '開幕狀態', width: '100px' }
      ],
      editingShop: null,
      previewImage: null,
      previewListingImage: null,  // 添加列表圖片預覽
      shopForm: {
        name: '',
        normalized_name: '',
        city: '台北市',
        city_CN: '台北市',
        address: '',
        customer_phone: '',
        description: '',
        budget: 0,
        hero_image: 'https://api.dicebear.com/7.x/initials/svg?seed=DrinkShop&backgroundColor=b7e4c7',
        hero_listing_image: 'https://api.dicebear.com/7.x/initials/svg?seed=DrinkShop&backgroundColor=b7e4c7',
        latitude: 0.0,
        longitude: 0.0,
        minimum_delivery_fee: null,
        minimum_delivery_time: null,
        minimum_order_amount: null,
        minimum_pickup_time: null,
        primary_cuisine_id: '',
        tag: '',
        is_new_until: null,
        rating: 1,
        review_number: 0
      },
      currentTab: 'basic',
      tabs: [
        { key: 'basic', label: '基本資料' },
        { key: 'business', label: '營業資訊' },
        { key: 'location', label: '位置資訊' },
        { key: 'rating', label: '評分資訊' },
        { key: 'other', label: '其他資訊' }
      ],
      // 所有縣市選項
      cityOptions: [
        '台北市', '新北市', '桃園市', '台中市', '台南市', 
        '高雄市', '新竹縣', '新竹市', '苗栗縣', '彰化縣',
        '南投縣', '雲林縣', '嘉義縣', '嘉義市', '屏東縣',
        '宜蘭縣', '花蓮縣', '台東縣', '澎湖縣', '金門縣', '連江縣'
      ],
      // 城市中英文對照
      cityTranslation: {
        '台北市': 'Taipei City',
        '新北市': 'New Taipei City',
        '桃園市': 'Taoyuan City',
        '台中市': 'Taichung City',
        '台南市': 'Tainan City',
        '高雄市': 'Kaohsiung City',
        '新竹縣': 'Hsinchu County',
        '新竹市': 'Hsinchu City',
        '苗栗縣': 'Miaoli County',
        '彰化縣': 'Changhua County',
        '南投縣': 'Nantou County',
        '雲林縣': 'Yunlin County',
        '嘉義縣': 'Chiayi County',
        '嘉義市': 'Chiayi City',
        '屏東縣': 'Pingtung County',
        '宜蘭縣': 'Yilan County',
        '花蓮縣': 'Hualien County',
        '台東縣': 'Taitung County',
        '澎湖縣': 'Penghu County',
        '金門縣': 'Kinmen County',
        '連江縣': 'Lienchiang County'
      },
      formErrors: {
        name: '',
        city_CN: '',
        address: '',
        budget: '',
        latitude: '',
        longitude: '',
        review_number: '',
        customer_phone: '',
        minimum_delivery_fee: '',
        minimum_order_amount: '',
        minimum_delivery_time: '',
        minimum_pickup_time: '',
        distance: '',
        primary_cuisine_id: '',
        redirection_url: '',
        tag: '',
        description: ''
      }
    }
  },
  methods: {
    // 獲取所有店家
    async fetchShops() {
      try {
        const response = await shopAPI.getShops()
        this.shops = response.data.stores
        console.log('店家列表:', this.shops)
      } catch (error) {
        console.error('獲取店家列表失敗:', error)
        this.$message.error('獲取店家列表失敗')
      }
    },

    // 處理圖片上傳
    async handleImageUpload(event) {
      const file = event.target.files[0]
      if (file) {
        console.log('準備上傳的文件:', file)  // 調試用
        
        // 檢查文件類型
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if (!allowedTypes.includes(file.type)) {
          this.$message.error('不支援的圖片格式')
          return
        }
        
        // 檢查文件大小 (例如限制 5MB)
        const maxSize = 5 * 1024 * 1024
        if (file.size > maxSize) {
          this.$message.error('圖片大小不能超過 5MB')
          return
        }
        
        this.previewImage = URL.createObjectURL(file)
        
        const formData = new FormData()
        formData.append('file', file)
        
        // 檢查 FormData 內容
        for (let pair of formData.entries()) {
          console.log('FormData 內容:', pair[0], pair[1])
        }
        
        try {
          const response = await shopAPI.uploadImage(formData)
          this.shopForm.hero_image = response.data.url
        } catch (error) {
          console.log('完整錯誤信息:', error.response || error)
          if (error.response) {
            this.$message.error(error.response.data.message || '圖片上傳失敗')
          } else if (error.request) {
            this.$message.error('無法連接到伺服器')
          } else {
            this.$message.error('圖片上傳過程發生錯誤')
          }
          console.error('圖片上傳失敗:', error)
          this.shopForm.hero_image = this.defaultImage.url
          this.previewImage = null
        }
      }
    },

    // 新增按鈕處理
    handleAdd() {
      this.resetForm()  // 先重置表單
      this.showAddModal = true
    },

    // 編輯店家
    async editShop(shop) {
      try {
        const response = await shopAPI.getShop(shop.id)
        this.editingShop = response.data
        this.shopForm = { ...response.data }
        this.previewImage = null
        this.previewListingImage = null
        this.showAddModal = true
      } catch (error) {
        console.error('獲取店家詳情失敗:', error)
        this.$message.error('獲取店家詳情失敗')
      }
    },

    // 刪除店家
    async deleteShop(shop) {
      const result = await Swal.fire({
        title: '確定要刪除嗎？',
        text: `即將刪除店家：${shop.name}`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '確定刪除',
        cancelButtonText: '取消',
        background: '#1a1a1a',
        customClass: {
          popup: 'swal2-show',
          title: 'text-white',
          htmlContainer: 'text-white',
          confirmButton: 'bg-red-500 hover:bg-red-600',
          cancelButton: 'bg-gray-500 hover:bg-gray-600'
        }
      })
      
      if (result.isConfirmed) {
        try {
          await shopAPI.deleteShop(shop.id)
          await this.fetchShops()
          await this.logOperation(`【飲料店管理】刪除飲料店 ${shop.name}`, '刪除')
          Swal.fire({
            icon: 'success',
            title: '刪除成功',
            text: '店家已成功刪除',
            timer: 1500,
            showConfirmButton: false,
            background: '#1a1a1a',
            customClass: {
              popup: 'swal2-show',
              title: 'text-white',
              htmlContainer: 'text-white'
            }
          })
        } catch (error) {
          console.error('刪除店家失敗:', error)
          Swal.fire({
            icon: 'error',
            title: '刪除失敗',
            text: '刪除店家時發生錯誤',
            confirmButtonText: '確定',
            background: '#1a1a1a',
            customClass: {
              popup: 'swal2-show',
              title: 'text-white',
              htmlContainer: 'text-white',
              confirmButton: 'bg-blue-500 hover:bg-blue-600'
            }
          })
        }
      }
    },

    // 批量刪除店家
    async batchDeleteShops(ids) {
      const result = await Swal.fire({
        title: '確定要批量刪除嗎？',
        text: `即將刪除 ${ids.length} 筆店家資料`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '確定刪除',
        cancelButtonText: '取消',
        background: '#1a1a1a',
        customClass: {
          popup: 'swal2-show',
          title: 'text-white',
          htmlContainer: 'text-white',
          confirmButton: 'bg-red-500 hover:bg-red-600',
          cancelButton: 'bg-gray-500 hover:bg-gray-600'
        }
      })
      
      if (result.isConfirmed) {
        try {
          await Promise.all(ids.map(id => shopAPI.deleteShop(id)))
          await this.fetchShops()
          await this.logOperation(`【飲料店管理】批量刪除飲料店 (${ids.length} 筆)`, '刪除')
          Swal.fire({
            icon: 'success',
            title: '批量刪除成功',
            text: `已成功刪除 ${ids.length} 筆店家資料`,
            timer: 1500,
            showConfirmButton: false,
            background: '#1a1a1a',
            customClass: {
              popup: 'swal2-show',
              title: 'text-white',
              htmlContainer: 'text-white'
            }
          })
        } catch (error) {
          console.error('批量刪除失敗:', error)
          Swal.fire({
            icon: 'error',
            title: '批量刪除失敗',
            text: '刪除過程中發生錯誤',
            confirmButtonText: '確定',
            background: '#1a1a1a',
            customClass: {
              popup: 'swal2-show',
              title: 'text-white',
              htmlContainer: 'text-white',
              confirmButton: 'bg-blue-500 hover:bg-blue-600'
            }
          })
        }
      }
    },

    // 保存店家（新增或更新）
    async saveShop() {
      if (!this.validateForm()) {
        return
      }

      try {
        // 準備要發送的數據
        const formData = { ...this.shopForm }
        
        // 移除可能為空的欄位
        Object.keys(formData).forEach(key => {
          if (formData[key] === null || formData[key] === '') {
            delete formData[key]
          }
        })
        
        console.log('準備發送的數據:', formData)  // 調試用

      if(this.editingShop) {
          // 更新店家
          await shopAPI.updateShop(this.editingShop.id, formData)
          await this.logOperation(`【飲料店管理】編輯飲料店 ${this.shopForm.name}`, '修改')
          Swal.fire({
            icon: 'success',
            title: '更新成功',
            text: '店家資料已成功更新',
            timer: 1500,
            showConfirmButton: false,
            background: '#1a1a1a',
            customClass: {
              popup: 'swal2-show',
              title: 'text-white',
              htmlContainer: 'text-white'
            }
          })
        } else {
          // 創建店家
          await shopAPI.createShop(formData)
          await this.logOperation(`【飲料店管理】新增飲料店 ${this.shopForm.name}`, '新增')
          Swal.fire({
            icon: 'success',
            title: '創建成功',
            text: '新店家已成功創建',
            timer: 1500,
            showConfirmButton: false,
            background: '#1a1a1a',
            customClass: {
              popup: 'swal2-show',
              title: 'text-white',
              htmlContainer: 'text-white'
            }
          })
        }
        
        await this.fetchShops()
        this.showAddModal = false
        this.resetForm()
      } catch (error) {
        console.error('保存店家失敗:', error.response || error)
        if (error.response) {
          // 服務器返回的錯誤
          Swal.fire({
            icon: 'error',
            title: '保存失敗',
            text: error.response.data.message || '保存店家失敗',
            confirmButtonText: '確定',
            background: '#1a1a1a',
            customClass: {
              popup: 'swal2-show',
              title: 'text-white',
              htmlContainer: 'text-white',
              confirmButton: 'bg-blue-500 hover:bg-blue-600'
            }
          })
        } else if (error.request) {
          // 請求發出但沒有收到響應
          Swal.fire({
            icon: 'error',
            title: '連接錯誤',
            text: '無法連接到伺服器，請檢查網絡連接',
            confirmButtonText: '確定',
            background: '#1a1a1a',
            customClass: {
              popup: 'swal2-show',
              title: 'text-white',
              htmlContainer: 'text-white',
              confirmButton: 'bg-blue-500 hover:bg-blue-600'
            }
          })
      } else {
          // 其他錯誤
          Swal.fire({
            icon: 'error',
            title: '系統錯誤',
            text: '保存過程發生錯誤',
            confirmButtonText: '確定',
            background: '#1a1a1a',
            customClass: {
              popup: 'swal2-show',
              title: 'text-white',
              htmlContainer: 'text-white',
              confirmButton: 'bg-blue-500 hover:bg-blue-600'
            }
          })
        }
      }
    },

    // 重置表單
    resetForm() {
      // 重置所有狀態
      this.editingShop = null
      this.previewImage = null
      this.previewListingImage = null
      this.currentTab = 'basic'  // 重置當前標籤頁
      this.shopForm = {
        name: '',
        normalized_name: '',
        city: '',
        city_CN: '台北市',
        address: '',
        customer_phone: '',
        description: '',
        budget: 1,
        hero_image: this.defaultImage.url,
        hero_listing_image: this.defaultImage.url,
        latitude: 1,
        longitude: 1,
        minimum_delivery_fee: null,
        minimum_delivery_time: null,
        minimum_order_amount: null,
        minimum_pickup_time: null,
        primary_cuisine_id: '',
        tag: '',
        is_new_until: null,
        rating: 1,
        review_number: 1
      }
      // 清空所有錯誤訊息
      Object.keys(this.formErrors).forEach(key => {
        this.formErrors[key] = ''
      })
      // 自動設置城市英文名稱
      this.handleCityChange({ target: { value: this.shopForm.city_CN } })
    },

    // 判斷是否為新店
    isNewStore(isNewUntil) {
      if (!isNewUntil) return false;
      const untilDate = new Date(isNewUntil);
      const now = new Date();
      return untilDate > now;
    },

    handleNameInput(e) {
      // 自動生成 normalized_name
      this.shopForm.normalized_name = e.target.value.trim()
    },

    handleCityChange(e) {
      // 自動轉換中英文城市名
      this.shopForm.city = this.cityTranslation[e.target.value]
    },

    // 修改列表圖片上傳處理
    async handleListingImageUpload(event) {
      const file = event.target.files[0]
      if (file) {
        console.log('準備上傳的文件:', file)
        
        // 檢查文件類型
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if (!allowedTypes.includes(file.type)) {
          this.$message.error('不支援的圖片格式')
          return
        }
        
        // 檢查文件大小 (例如限制 5MB)
        const maxSize = 5 * 1024 * 1024
        if (file.size > maxSize) {
          this.$message.error('圖片大小不能超過 5MB')
          return
        }
        
        // 設置預覽圖片
        this.previewListingImage = URL.createObjectURL(file)
        
        const formData = new FormData()
        formData.append('file', file)
        
        try {
          const response = await shopAPI.uploadImage(formData)
          this.shopForm.hero_listing_image = response.data.url
        } catch (error) {
          console.log('完整錯誤信息:', error.response || error)
          if (error.response) {
            this.$message.error(error.response.data.message || '圖片上傳失敗')
          } else if (error.request) {
            this.$message.error('無法連接到伺服器')
          } else {
            this.$message.error('圖片上傳過程發生錯誤')
          }
          console.error('圖片上傳失敗:', error)
          this.shopForm.hero_listing_image = this.defaultImage.url
          this.previewListingImage = null  // 清除預覽
        }
      }
    },

    validateForm() {
      let isValid = true
      
      // 驗證必填欄位
      isValid = this.validateName(this.shopForm.name) && isValid
      isValid = this.validateCity(this.shopForm.city_CN) && isValid
      isValid = this.validateAddress(this.shopForm.address) && isValid
      
      // 驗證數字欄位
      isValid = this.validateNumber(this.shopForm.budget, 'budget', 1) && isValid
      isValid = this.validateNumber(this.shopForm.latitude, 'latitude', 1) && isValid
      isValid = this.validateNumber(this.shopForm.longitude, 'longitude', 1) && isValid
      isValid = this.validateNumber(this.shopForm.review_number, 'review_number', 1) && isValid
      
      // 驗證選填數字欄位
      if (this.shopForm.minimum_delivery_fee) {
        isValid = this.validateNumber(this.shopForm.minimum_delivery_fee, 'minimum_delivery_fee', 0) && isValid
      }
      if (this.shopForm.minimum_order_amount) {
        isValid = this.validateNumber(this.shopForm.minimum_order_amount, 'minimum_order_amount', 0) && isValid
      }
      if (this.shopForm.minimum_delivery_time) {
        isValid = this.validateNumber(this.shopForm.minimum_delivery_time, 'minimum_delivery_time', 0) && isValid
      }
      if (this.shopForm.minimum_pickup_time) {
        isValid = this.validateNumber(this.shopForm.minimum_pickup_time, 'minimum_pickup_time', 0) && isValid
      }
      
      // 驗證其他選填欄位
      if (this.shopForm.customer_phone) {
        isValid = this.validatePhone(this.shopForm.customer_phone) && isValid
      }
      if (this.shopForm.redirection_url) {
        isValid = this.validateUrl(this.shopForm.redirection_url) && isValid
      }
      
      return isValid
    },

    validateName(value) {
      this.formErrors.name = ''
      if (!value) {
        this.formErrors.name = '請輸入店家名稱'
        return false
      }
      if (value.length > 50) {
        this.formErrors.name = '店家名稱不能超過50個字符'
        return false
      }
      return true
    },

    validateCity(value) {
      this.formErrors.city_CN = ''
      if (!value) {
        this.formErrors.city_CN = '請選擇城市'
        return false
      }
      return true
    },

    validateAddress(value) {
      this.formErrors.address = ''
      if (!value) {
        this.formErrors.address = '請輸入地址'
        return false
      }
      if (value.length > 100) {
        this.formErrors.address = '地址不能超過100個字符'
        return false
      }
      return true
    },

    validatePhone(value) {
      this.formErrors.customer_phone = ''
      if (value) {
        const phoneRegex = /^[0-9-+()]*$/
        if (!phoneRegex.test(value)) {
          this.formErrors.customer_phone = '請輸入有效的電話號碼'
          return false
        }
      }
      return true
    },

    validateUrl(value) {
      this.formErrors.redirection_url = ''
      if (value) {
        try {
          new URL(value)
        } catch (e) {
          this.formErrors.redirection_url = '請輸入有效的URL'
          return false
        }
      }
      return true
    },

    validateNumber(value, fieldName, min = 0, max = null) {
      this.formErrors[fieldName] = ''
      if (value === null || value === '') return true

      const num = Number(value)
      if (isNaN(num)) {
        this.formErrors[fieldName] = '請輸入有效數字'
        return false
      }
      if (num < min) {
        this.formErrors[fieldName] = `不能小於 ${min}`
        return false
      }
      if (max !== null && num > max) {
        this.formErrors[fieldName] = `不能大於 ${max}`
        return false
      }
      return true
    },

    getShopImage(shop) {
      console.log('處理的店家圖片:', {
        hero_image: shop.hero_image,
        isUpload: shop.hero_image?.includes('/uploads/stores/'),
        backend_url: import.meta.env.VITE_BACKEND_URL
      })
      
      // 如果有上傳的圖片，使用完整的 URL
      if (shop.hero_image?.includes('/uploads/stores/')) {
        // 從完整路徑中提取文件名
        const filename = shop.hero_image.split('/').pop()
        console.log('構建的圖片URL:', 
          `${import.meta.env.VITE_BACKEND_URL}/api/stores/uploads/stores/${filename}`)
        return `${import.meta.env.VITE_BACKEND_URL}/api/stores/uploads/stores/${filename}`
      }
      
      // 如果有外部圖片連結，直接使用
      if (shop.hero_image && (shop.hero_image.startsWith('http://') || shop.hero_image.startsWith('https://'))) {
        console.log('使用外部圖片連結:', shop.hero_image)
        return shop.hero_image
      }
      
      // 都沒有則使用預設假圖
      console.log('使用預設圖片:', this.defaultImage)
      return this.defaultImage
    },

    closeModal() {
      this.showAddModal = false
      this.resetForm()  // 確保關閉時重置表單和清空錯誤訊息
    }
  }
}
</script> 

<style scoped>
/* 確保表格內容不會換行 */
:deep(.table-cell-hero_image) {
  white-space: nowrap;
  width: 100px;
  min-width: 100px;
  padding: 0.5rem !important;
}

/* 讓地址欄位自適應寬度 */
:deep(.table-cell-address) {
  width: auto;
  min-width: 200px;
}

/* 其他固定寬度欄位 */
:deep(.table-cell-rating),
:deep(.table-cell-review_number),
:deep(.table-cell-is_new_until) {
  white-space: nowrap;
}

.form-input,
.form-select,
.form-textarea {
  @apply w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500;
}

.required-field::after {
  content: '*';
  @apply text-red-500 ml-1;
}
</style> 