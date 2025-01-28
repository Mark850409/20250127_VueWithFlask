<template>
  <div>
    <DataTable
      :columns="columns"
      :data="ratings"
      @add="showAddModal = true"
      @edit="editRating"
      @delete="deleteRating"
      @batch-delete="batchDeleteRatings">
      <!-- 自定義評分列 -->
      <template #rating="{ item }">
        <div class="flex items-center">
          <span class="text-yellow-400">
            <i v-for="n in 5" :key="n" 
               :class="['fas', n <= item.rating ? 'fa-star' : 'fa-star-o']"></i>
          </span>
          <span class="ml-2">{{ item.rating }}/5</span>
        </div>
      </template>
    </DataTable>
  </div>
</template>

<script>
import DataTable from '../common/DataTable.vue'

export default {
  name: 'RatingManagement',
  components: {
    DataTable
  },
  data() {
    return {
      columns: [
        { key: 'user', label: '用戶' },
        { key: 'shop', label: '店家' },
        { key: 'product', label: '商品' },
        { key: 'rating', label: '評分' },
        { key: 'comment', label: '評論內容' },
        { key: 'createTime', label: '評分時間' }
      ],
      ratings: [
        {
          id: 1,
          user: '王小明',
          shop: '春水堂',
          product: '珍珠奶茶',
          rating: 4.5,
          comment: '珍珠很Q彈，奶茶香醇不會太甜',
          createTime: '2024-01-15 14:30:22'
        },
        // ... 更多評分數據
      ]
    }
  },
  methods: {
    // ... CRUD 方法實作
  }
}
</script> 