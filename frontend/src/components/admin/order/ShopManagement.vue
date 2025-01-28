<template>
  <div>
    <DataTable
      :columns="columns"
      :data="shops"
      @add="showAddModal = true"
      @edit="editShop"
      @delete="deleteShop"
      @batch-delete="batchDeleteShops">
      <!-- 自定義圖片列 -->
      <template #image="{ item }">
        <img :src="item.image" class="w-16 h-16 rounded-lg object-cover shadow-sm">
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
      <template #status="{ item }">
        <span :class="[
          'px-2 py-1 text-xs rounded-full',
          item.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        ]">
          {{ item.status === 'active' ? '營業中' : '已關閉' }}
        </span>
      </template>
      <!-- 自定義瀏覽次數列 -->
      <template #views="{ item }">
        <div class="flex items-center text-gray-600">
          <i class="fas fa-eye mr-2"></i>
          {{ item.views }}
        </div>
      </template>
    </DataTable>

    <!-- 新增/編輯彈窗 -->
    <div v-if="showAddModal" 
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white rounded-xl p-8 w-full max-w-md">
        <h2 class="text-xl font-bold mb-6">{{ editingShop ? '編輯店家' : '新增店家' }}</h2>
        <div class="space-y-4">
          <!-- 店家圖片上傳 -->
          <div class="flex flex-col items-center">
            <img :src="previewImage || shopForm.image" 
                 class="w-32 h-32 rounded-lg object-cover mb-4 shadow-sm">
            <label class="px-4 py-2 bg-gray-100 rounded-lg cursor-pointer hover:bg-gray-200">
              <input type="file" 
                     class="hidden" 
                     accept="image/*"
                     @change="handleImageUpload">
              <i class="fas fa-camera mr-2"></i>更換圖片
            </label>
          </div>
          <!-- 基本資料 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">店家名稱</label>
            <input type="text" v-model="shopForm.name" 
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">城市</label>
            <select v-model="shopForm.city" 
                    class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
              <option value="台北市">台北市</option>
              <option value="新北市">新北市</option>
              <option value="桃園市">桃園市</option>
              <!-- 更多城市選項 -->
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">地址</label>
            <input type="text" v-model="shopForm.address" 
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">電話</label>
            <input type="text" v-model="shopForm.phone" 
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">營業時間</label>
            <input type="text" v-model="shopForm.businessHours" 
                   class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">狀態</label>
            <select v-model="shopForm.status" 
                    class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
              <option value="active">營業中</option>
              <option value="closed">已關閉</option>
            </select>
          </div>
        </div>
        <div class="mt-8 flex justify-end space-x-4">
          <button @click="showAddModal = false" 
                  class="px-4 py-2 text-gray-700 border rounded-lg hover:bg-gray-50">
            取消
          </button>
          <button @click="saveShop" 
                  class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
            確認
          </button>
        </div>
      </div>
    </div>
    <BackToHome />
  </div>
</template>

<script>
import DataTable from '../common/DataTable.vue'
import BackToHome from '../common/BackToHome.vue'

export default {
  name: 'ShopManagement',
  components: {
    DataTable,
    BackToHome
  },
  data() {
    return {
      columns: [
        { key: 'image', label: '店家圖片' },
        { key: 'name', label: '店家名稱' },
        { key: 'city', label: '城市' },
        { key: 'address', label: '地址' },
        { key: 'rating', label: '星級' },
        { key: 'views', label: '瀏覽次數' },
        { key: 'status', label: '狀態' }
      ],
      shops: [
        {
          id: 1,
          name: '春水堂',
          city: '台北市',
          address: '信義區信義路五段7號',
          phone: '02-2345-6789',
          businessHours: '10:00-22:00',
          status: 'active',
          rating: 4.5,
          views: 1580,
          image: 'https://via.placeholder.com/150'
        },
        {
          id: 2,
          name: '五桐號',
          city: '台北市',
          address: '大安區忠孝東路四段216號',
          phone: '02-2345-6789',
          businessHours: '11:00-21:30',
          status: 'active',
          rating: 4.6,
          views: 2460,
          image: 'https://via.placeholder.com/150'
        },
        {
          id: 3,
          name: '可不可熟成紅茶',
          city: '台北市',
          address: '中山區南京東路二段12號',
          phone: '02-2345-6789',
          businessHours: '10:30-21:00',
          status: 'closed',
          rating: 4.7,
          views: 1890,
          image: 'https://via.placeholder.com/150'
        }
      ],
      showAddModal: false,
      editingShop: null,
      previewImage: null,
      shopForm: {
        name: '',
        city: '台北市',
        address: '',
        phone: '',
        businessHours: '',
        status: 'active',
        image: 'https://via.placeholder.com/150'
      }
    }
  },
  methods: {
    handleImageUpload(event) {
      const file = event.target.files[0]
      if (file) {
        this.previewImage = URL.createObjectURL(file)
      }
    },
    editShop(shop) {
      this.editingShop = shop
      this.shopForm = { ...shop }
      this.previewImage = null
      this.showAddModal = true
    },
    deleteShop(shop) {
      if(confirm('確定要刪除此店家嗎？')) {
        this.shops = this.shops.filter(s => s.id !== shop.id)
      }
    },
    batchDeleteShops(ids) {
      if(confirm(`確定要刪除選中的 ${ids.length} 筆店家嗎？`)) {
        this.shops = this.shops.filter(s => !ids.includes(s.id))
      }
    },
    saveShop() {
      if(!this.shopForm.name || !this.shopForm.address) {
        alert('請填寫必要欄位')
        return
      }

      if(this.editingShop) {
        const index = this.shops.findIndex(s => s.id === this.editingShop.id)
        this.shops[index] = {
          ...this.editingShop,
          ...this.shopForm,
          image: this.previewImage || this.shopForm.image
        }
      } else {
        this.shops.push({
          id: this.shops.length + 1,
          ...this.shopForm,
          image: this.previewImage || this.shopForm.image,
          rating: 0,
          views: 0
        })
      }
      this.showAddModal = false
      this.editingShop = null
      this.previewImage = null
      this.shopForm = {
        name: '',
        city: '台北市',
        address: '',
        phone: '',
        businessHours: '',
        status: 'active',
        image: 'https://via.placeholder.com/150'
      }
    }
  }
}
</script> 