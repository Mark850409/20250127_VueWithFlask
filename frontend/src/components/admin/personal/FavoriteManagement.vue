<template>
  <div>
    <DataTable
      :columns="columns"
      :data="favorites"
      @add="showAddModal = true"
      @edit="editFavorite"
      @delete="deleteFavorite"
      @batch-delete="batchDeleteFavorites">
      <!-- 自定義商品圖片列 -->
      <template #productImage="{ item }">
        <img :src="item.productImage" class="w-12 h-12 rounded-lg object-cover">
      </template>
    </DataTable>
  </div>
</template>

<script>
import DataTable from '../common/DataTable.vue'

export default {
  name: 'FavoriteManagement',
  components: {
    DataTable
  },
  data() {
    return {
      columns: [
        { key: 'user', label: '用戶' },
        { key: 'productImage', label: '商品圖片' },
        { key: 'productName', label: '商品名稱' },
        { key: 'shop', label: '店家' },
        { key: 'addTime', label: '收藏時間' }
      ],
      favorites: [
        {
          id: 1,
          user: '王小明',
          productName: '珍珠奶茶',
          shop: '春水堂',
          addTime: '2024-01-15 16:30:22',
          productImage: 'https://via.placeholder.com/150'
        },
        // ... 更多收藏數據
      ]
    }
  },
  methods: {
    // ... CRUD 方法實作
  }
}
</script> 